"""
TakaSmart Waste Classifier — fully offline, no internet calls.

Detection pipeline (in order):
  1. YOLO object detection   — best accuracy when a known object is found
  2. Color/texture heuristics — fallback when YOLO finds nothing useful
  3. Reject                   — if both fail with low confidence

WASTE_DB holds rich, multilingual knowledge (desc, steps, safety,
recommendation, market_value, env_impact) for each of the 7 categories.
"""

import os
import math
from pathlib import Path

try:
    from PIL import Image, ImageStat
except ImportError:
    Image = None
    ImageStat = None


# ═══════════════════════════════════════════════════════════════════
#  WASTE KNOWLEDGE DATABASE
# ═══════════════════════════════════════════════════════════════════
WASTE_DB = {

    # ── PLASTIC ───────────────────────────────────────────────────
    "plastic": {
        "type": "Plastiki", "typeEn": "Plastic", "typeFr": "Plastique",
        "badge": "badge-plastic", "icon": "🧴",
        "market_value": {"sw": "Wastani — PET ina thamani ya juu zaidi", "en": "Medium — PET has the highest value", "fr": "Moyen — le PET a la valeur la plus élevée"},
        "env_impact":   {"sw": "Inachukua miaka 100–500 kuoza; inadhuru viumbe vya baharini", "en": "Takes 100–500 years to decompose; harms marine life", "fr": "Met 100–500 ans à se décomposer; nuit à la faune marine"},
        "desc": {
            "sw": "Hii ni taka ya plastiki. Plastiki inachukua miaka 100–500 kuoza na inadhuru mazingira na viumbe vya baharini.",
            "en": "This is plastic waste. Plastic takes 100–500 years to decompose and seriously harms the environment and marine life.",
            "fr": "Ceci est un déchet plastique. Le plastique met 100–500 ans à se décomposer et nuit gravement à l'environnement.",
        },
        "steps": {
            "sw": [
                "Safisha chupa na vyombo — ondoa mabaki ya chakula au vinywaji",
                "Tenganisha kwa aina: PET (chupa wazi/ngumu), HDPE (ndoo/mitungi), PVC (mabomba)",
                "Bana au kunja ili kupunguza nafasi ya kuhifadhi",
                "Hifadhi mahali pakavu mbali na jua moja kwa moja",
                "Peleka kituo cha ukusanyaji au wasiliana na mnunuzi kwenye 'Wananunua'",
            ],
            "en": [
                "Clean bottles and containers — remove food or drink residue",
                "Separate by type: PET (clear hard bottles), HDPE (buckets/cans), PVC (pipes)",
                "Crush or fold to reduce storage volume",
                "Store in a dry place away from direct sunlight",
                "Take to a plastic collection point or contact a buyer in 'Buyers'",
            ],
            "fr": [
                "Nettoyez bouteilles et contenants — retirez les résidus",
                "Séparez par type : PET (bouteilles claires/rigides), HDPE (bidons), PVC (tuyaux)",
                "Écrasez ou pliez pour réduire le volume de stockage",
                "Conservez dans un endroit sec à l'abri du soleil",
                "Apportez à un point de collecte ou contactez un acheteur",
            ],
        },
        "safety": {
            "sw": "🚫 Usichome plastiki — hutoa dioxins na gesi za sumu hatari angani. Vaa kinga ukishughulikia plastiki iliyovunjika au kali.",
            "en": "🚫 Never burn plastic — it releases dioxins and toxic fumes. Wear gloves when handling sharp or broken plastic.",
            "fr": "🚫 Ne brûlez jamais le plastique — il libère des dioxines et des fumées toxiques. Portez des gants si le plastique est brisé.",
        },
        "recommendation": {
            "sw": "✅ Tenganisha plastiki kwa aina, isafishe, kisha uipeleke kwa mnunuzi au kituo cha recycling. PET ina thamani ya juu zaidi sokoni. Epuka kuchoma au kutupa hovyo.",
            "en": "✅ Separate plastic by type, clean it, then take it to a registered buyer or recycling point. PET has the highest market value. Never burn or dump it.",
            "fr": "✅ Séparez le plastique par type, nettoyez-le, puis apportez-le à un acheteur ou centre de recyclage. Le PET a la valeur la plus élevée. Ne brûlez jamais.",
        },
    },

    # ── PAPER ─────────────────────────────────────────────────────
    "paper": {
        "type": "Karatasi", "typeEn": "Paper", "typeFr": "Papier",
        "badge": "badge-paper", "icon": "📦",
        "market_value": {"sw": "Kadibodi nzito ina bei nzuri; karatasi nyembamba ina bei ndogo", "en": "Heavy cardboard fetches good prices; thin paper is lower value", "fr": "Le carton épais a une bonne valeur; le papier fin est moins coté"},
        "env_impact":   {"sw": "Inachukua miaka 2–5 kuoza; kuirecycle kunaokoa miti mingi", "en": "Takes 2–5 years to decompose; recycling saves many trees", "fr": "Met 2–5 ans à se décomposer; le recyclage sauve de nombreux arbres"},
        "desc": {
            "sw": "Hii ni taka ya karatasi au kadibodi. Karatasi inaweza kurecyclewa hadi mara 5–7 kabla ya nyuzi zake kulegea.",
            "en": "This is paper or cardboard waste. Paper can be recycled up to 5–7 times before its fibres weaken.",
            "fr": "Ceci est un déchet papier ou carton. Le papier peut être recyclé 5–7 fois avant que ses fibres ne s'affaiblissent.",
        },
        "steps": {
            "sw": [
                "Tenganisha karatasi kutoka kwa taka nyingine",
                "Ondoa karatasi zenye mafuta, rangi nyingi au kemikali — hazifai recycling",
                "Zikunje au zibane ili kupunguza ukubwa wa kuhifadhi",
                "Hifadhi mahali pakavu — karatasi iliyolowa haifai recycling kamwe",
                "Peleka kituo cha kukusanya karatasi au uuze kwa mnunuzi",
            ],
            "en": [
                "Separate paper from other waste",
                "Remove oily, heavily dyed, or chemical-soaked paper — not recyclable",
                "Flatten or bundle to reduce storage volume",
                "Keep completely dry — wet paper cannot be recycled",
                "Take to a paper collection point or sell to a buyer",
            ],
            "fr": [
                "Séparez le papier des autres déchets",
                "Retirez le papier huileux, très coloré ou chimique — non recyclable",
                "Aplatissez ou liez pour réduire le volume",
                "Gardez absolument au sec — le papier mouillé ne peut pas être recyclé",
                "Apportez à un centre de collecte ou vendez à un acheteur",
            ],
        },
        "safety": {
            "sw": "ℹ️ Karatasi kwa ujumla si hatari. Epuka karatasi zenye kemikali au rangi za sumu — vaa kinga inapohitajika.",
            "en": "ℹ️ Paper is generally not hazardous. Avoid paper with chemical or toxic dye content — wear gloves if unsure.",
            "fr": "ℹ️ Le papier n'est généralement pas dangereux. Évitez le papier avec des produits chimiques — portez des gants si nécessaire.",
        },
        "recommendation": {
            "sw": "✅ Hifadhi karatasi kavu na zilizotengwa, kisha zipeleke kwa mnunuzi. Kadibodi nzito ina thamani zaidi ya karatasi nyembamba. Chunga usiilosche.",
            "en": "✅ Keep paper dry and sorted, then take it to a buyer. Heavy cardboard is worth more than thin paper. Make sure it stays dry.",
            "fr": "✅ Gardez le papier sec et trié, puis portez-le à un acheteur. Le carton épais vaut plus que le papier fin. Ne le laissez pas mouiller.",
        },
    },

    # ── GLASS ─────────────────────────────────────────────────────
    "glass": {
        "type": "Kioo", "typeEn": "Glass", "typeFr": "Verre",
        "badge": "badge-glass", "icon": "🍶",
        "market_value": {"sw": "Wastani — chupa nzima zina bei zaidi kuliko vipande", "en": "Medium — whole bottles worth more than fragments", "fr": "Moyen — les bouteilles entières valent plus que les fragments"},
        "env_impact":   {"sw": "Kioo hakiozi — kinabaki ardhini milele. Kukirecycle kunaokoa nishati nyingi", "en": "Glass never decomposes — stays in soil forever. Recycling saves significant energy", "fr": "Le verre ne se décompose pas — reste dans le sol éternellement. Le recyclage économise beaucoup d'énergie"},
        "desc": {
            "sw": "Hii ni taka ya kioo. Kioo kinaweza kurecyclewa bila kupoteza ubora wake — mara nyingi bila kikomo.",
            "en": "This is glass waste. Glass can be recycled indefinitely without losing quality.",
            "fr": "Ceci est un déchet de verre. Le verre peut être recyclé indéfiniment sans perte de qualité.",
        },
        "steps": {
            "sw": [
                "Vaa kinga (glavu nzito au kitambaa) — kioo kinaweza kukata vibaya",
                "Tenganisha kwa rangi: nyeupe/wazi, kijani, kahawia/manjano",
                "Ondoa uchafu, mabaki ya chakula au vinywaji ndani ya chupa",
                "Usichanganye kioo na taka nyingine za recycling",
                "Hifadhi kwenye sanduku gumu na upeleke kituo cha kukusanya kioo",
            ],
            "en": [
                "Wear heavy gloves or use a thick cloth — glass can cut badly",
                "Separate by colour: clear/white, green, brown/amber",
                "Remove dirt, food or drink residue inside bottles",
                "Do not mix glass with other recyclable waste",
                "Store in a rigid box and take to a glass collection point",
            ],
            "fr": [
                "Portez des gants épais ou utilisez un chiffon épais — le verre coupe",
                "Séparez par couleur : incolore/blanc, vert, brun/ambré",
                "Retirez la saleté, les résidus alimentaires ou de boisson",
                "Ne mélangez pas le verre avec d'autres déchets recyclables",
                "Conservez dans une boîte rigide et apportez à un point de collecte",
            ],
        },
        "safety": {
            "sw": "⚠️ Kioo kilichovunjika ni hatari sana. Kishughulikie kwa tahadhari kubwa — vaa glavu nzito na viatu. Kihifadhi kwenye sanduku gumu kisikokata.",
            "en": "⚠️ Broken glass is very dangerous. Handle with extreme care — wear heavy gloves and shoes. Store in a rigid, non-cutting box.",
            "fr": "⚠️ Le verre brisé est très dangereux. Manipulez avec extrême prudence — portez des gants épais et des chaussures fermées.",
        },
        "recommendation": {
            "sw": "✅ Tenganisha kioo kwa rangi, kisafishe, kisha kipeleke kituo cha kukusanya kioo. Kioo kilichovunjika kishughulikiwe kwa tahadhari. Epuka kuchanganya na taka nyingine.",
            "en": "✅ Separate glass by colour, clean it, then take it to a glass collection point. Handle broken glass with great care. Never mix with other waste.",
            "fr": "✅ Séparez le verre par couleur, nettoyez-le, puis apportez-le à un centre. Manipulez le verre brisé avec soin. Ne mélangez jamais avec d'autres déchets.",
        },
    },

    # ── METAL ─────────────────────────────────────────────────────
    "metal": {
        "type": "Chuma", "typeEn": "Metal", "typeFr": "Métal",
        "badge": "badge-metal", "icon": "🔩",
        "market_value": {"sw": "Juu — aluminium na shaba vina bei nzuri zaidi", "en": "High — aluminium and copper fetch the best prices", "fr": "Élevée — l'aluminium et le cuivre ont les meilleurs prix"},
        "env_impact":   {"sw": "Chuma hakiozi haraka — kinadhuru udongo na maji. Kukirecycle kunaokoa madini mengi", "en": "Metal decomposes very slowly — damages soil and water. Recycling conserves significant mineral resources", "fr": "Le métal se décompose très lentement — endommage le sol. Le recyclage préserve des ressources minérales importantes"},
        "desc": {
            "sw": "Hii ni taka ya chuma kama aluminium, shaba, chuma chakavu au bati. Chuma kina thamani kubwa na kinaweza kurecyclewa mara nyingi bila kupoteza ubora.",
            "en": "This is metal waste such as aluminium, copper, scrap steel, or tin. Metal has high value and can be recycled many times without losing quality.",
            "fr": "Ceci est un déchet métallique (aluminium, cuivre, ferraille, fer-blanc). Le métal a une haute valeur et peut être recyclé de nombreuses fois.",
        },
        "steps": {
            "sw": [
                "Tenganisha aina za metali: aluminium (nyepesi), shaba (rangi ya dhahabu/nyekundu), chuma cha kawaida (nzito, hutu kutu), bati",
                "Ondoa sehemu zisizo za chuma (plastiki, mpira, kioo, karatasi)",
                "Safisha kutu au uchafu inapowezekana — thamani huongezeka",
                "Bana, piga mkuki au funga kwa kamba ili kupunguza ukubwa",
                "Wasiliana na mnunuzi wa scrap metal — aluminium na shaba vina thamani ya juu zaidi",
            ],
            "en": [
                "Separate metal types: aluminium (light), copper (golden/reddish), steel (heavy, rusts), tin",
                "Remove non-metal parts (plastic, rubber, glass, paper)",
                "Clean rust or dirt where possible — improves value",
                "Crush, bundle or tie with rope to reduce volume",
                "Contact a scrap-metal buyer — aluminium and copper command the highest prices",
            ],
            "fr": [
                "Séparez les métaux : aluminium (léger), cuivre (doré/rougeâtre), acier (lourd, rouille), fer-blanc",
                "Retirez les parties non métalliques (plastique, caoutchouc, verre)",
                "Nettoyez la rouille ou la saleté si possible — augmente la valeur",
                "Écrasez, liez ou attachez pour réduire le volume",
                "Contactez un acheteur de ferraille — aluminium et cuivre ont les prix les plus élevés",
            ],
        },
        "safety": {
            "sw": "⚠️ Chuma chenye ncha kali au makali kinaweza kukata au kuchomeka. Vaa glavu za ngozi ukishughulikia. Chuma chenye kutu — usiguze bila kinga (tetanasi).",
            "en": "⚠️ Sharp or jagged metal can cut or puncture skin. Wear leather gloves when handling. Rusty metal — do not touch without protection (tetanus risk).",
            "fr": "⚠️ Le métal tranchant peut couper. Portez des gants en cuir. Métal rouillé — ne touchez pas sans protection (risque de tétanos).",
        },
        "recommendation": {
            "sw": "✅ Tenganisha aina za chuma, isafishe, kisha uiuzie mnunuzi wa scrap metal. Aluminium na shaba vina bei nzuri zaidi — usivipeleke pamoja na chuma cha kawaida.",
            "en": "✅ Separate metal types, clean them, then sell to a scrap-metal buyer. Aluminium and copper fetch the best prices — keep them separate from plain steel.",
            "fr": "✅ Séparez les métaux, nettoyez-les, puis vendez-les à un acheteur de ferraille. Aluminium et cuivre ont les meilleurs prix — gardez-les séparés de l'acier ordinaire.",
        },
    },

    # ── ORGANIC ───────────────────────────────────────────────────
    "organic": {
        "type": "Kikolojia", "typeEn": "Organic", "typeFr": "Organique",
        "badge": "badge-organic", "icon": "🍂",
        "market_value": {"sw": "Mbolea iliyotengenezwa ina thamani kwa kilimo", "en": "Finished compost has value for farming and gardening", "fr": "Le compost fini a de la valeur pour l'agriculture"},
        "env_impact":   {"sw": "Inaweza kugeuzwa mbolea — inapunguza methane kwenye madampo", "en": "Can become fertiliser — reduces methane emissions from landfills", "fr": "Peut devenir de l'engrais — réduit les émissions de méthane des décharges"},
        "desc": {
            "sw": "Hii ni taka ya kikolojia — mabaki ya chakula, majani, matunda au vitu vya asili. Inaweza kugeuzwa kuwa mbolea nzuri ya bustani kupitia compost.",
            "en": "This is organic waste — food scraps, leaves, fruit, or natural materials. It can be turned into excellent garden fertiliser through composting.",
            "fr": "Ceci est un déchet organique — restes alimentaires, feuilles, fruits ou matières naturelles. Il peut être transformé en excellent engrais par le compostage.",
        },
        "steps": {
            "sw": [
                "Tenganisha mabaki ya chakula, majani na matunda kutoka kwa taka nyingine",
                "Weka kwenye kisanduku au shimo la compost (angalau 1m × 1m)",
                "Changanya na majani makavu na udongo kidogo — inasaidia kuoza haraka",
                "Ongeza maji kidogo ikiwa ni kavu sana (unyevu kama sifongo)",
                "Geuza mara kwa mara (kila siku 2–3) kwa hewa ya kutosha",
                "Baada ya wiki 8–12: mbolea nzuri ya bustani iko tayari",
            ],
            "en": [
                "Separate food scraps, leaves and fruit from other waste",
                "Put in a compost bin or pit (at least 1m × 1m)",
                "Mix with dry leaves and a little soil — speeds up decomposition",
                "Add a little water if too dry (moisture like a wrung-out sponge)",
                "Turn every 2–3 days for adequate aeration",
                "After 8–12 weeks: excellent garden fertiliser is ready",
            ],
            "fr": [
                "Séparez restes alimentaires, feuilles et fruits des autres déchets",
                "Mettez dans un bac ou une fosse à compost (au moins 1m × 1m)",
                "Mélangez avec des feuilles sèches et un peu de terre — accélère la décomposition",
                "Ajoutez un peu d'eau si trop sec (humidité comme une éponge essorée)",
                "Retournez tous les 2–3 jours pour une bonne aération",
                "Après 8–12 semaines : excellent engrais naturel prêt à l'emploi",
            ],
        },
        "safety": {
            "sw": "ℹ️ Taka za kikolojia kwa ujumla si hatari. Epuka kuchanganya na plastiki, kemikali au taka hatari — zinafunga mchakato wa kuoza. Osha mikono baada ya kushughulikia.",
            "en": "ℹ️ Organic waste is generally not hazardous. Do not mix with plastic, chemicals, or hazardous waste — stops decomposition. Wash hands after handling.",
            "fr": "ℹ️ Les déchets organiques ne sont généralement pas dangereux. Ne mélangez pas avec plastique, produits chimiques ou déchets dangereux. Lavez-vous les mains.",
        },
        "recommendation": {
            "sw": "✅ Tenganisha taka za kikolojia na uzifanye compost. Hii inapunguza taka na kukupa mbolea bure ya bustani yako. Ni njia nzuri zaidi kuliko kutupa au kuchoma.",
            "en": "✅ Separate organic waste and compost it. This reduces waste and gives you free garden fertiliser. Far better than dumping or burning.",
            "fr": "✅ Séparez les déchets organiques et compostez-les. Cela réduit les déchets et vous donne de l'engrais gratuit. Bien mieux que de jeter ou de brûler.",
        },
    },

    # ── E-WASTE ───────────────────────────────────────────────────
    "ewaste": {
        "type": "E-Waste", "typeEn": "E-Waste", "typeFr": "Déchets électroniques",
        "badge": "badge-ewaste", "icon": "💻",
        "market_value": {"sw": "Juu — ina dhahabu, shaba na fedha ndogo zenye thamani", "en": "High — contains valuable gold, copper and silver traces", "fr": "Élevée — contient de l'or, du cuivre et de l'argent précieux"},
        "env_impact":   {"sw": "Hatari sana — ina sumu kama zebaki, risasi na cadmium", "en": "Very dangerous — contains toxins like mercury, lead and cadmium", "fr": "Très dangereux — contient des toxines comme le mercure, le plomb et le cadmium"},
        "desc": {
            "sw": "Hii ni taka ya elektroniki (e-waste). E-waste ina metali zenye thamani kama dhahabu, shaba na fedha ndogo, lakini pia sumu hatari kama zebaki na risasi.",
            "en": "This is electronic waste (e-waste). E-waste contains valuable metals like gold, copper and silver, but also dangerous toxins like mercury and lead.",
            "fr": "Ceci est un déchet électronique (e-waste). Il contient des métaux précieux comme l'or et le cuivre, mais aussi des toxines dangereuses comme le mercure et le plomb.",
        },
        "steps": {
            "sw": [
                "Usichome au kuvunja betri — zinaweza kulipuka na kutoa gesi za sumu kali",
                "Toa betri kutoka kwa vifaa vyote kabla ya kuhifadhi au kusafirisha",
                "Hifadhi vifaa mahali pakavu — unyevu unafunika mzunguko wa umeme",
                "Usitupe e-waste kwenye taka za kawaida — ni haramu na hatari",
                "Peleka kituo kilichoidhinishwa cha e-waste au duka la vifaa vya elektroniki",
                "Au wasiliana na mnunuzi wa e-waste kwenye sehemu ya 'Wananunua'",
            ],
            "en": [
                "Never burn or break batteries — they can explode and release highly toxic gas",
                "Remove batteries from all devices before storing or transporting",
                "Store in a dry place — moisture damages circuits and accelerates leaching",
                "Never dump e-waste with regular rubbish — illegal and dangerous",
                "Take to a certified e-waste facility or electronics shop",
                "Or contact an e-waste buyer in 'Buyers'",
            ],
            "fr": [
                "Ne brûlez ni ne cassez jamais les piles — risque d'explosion et gaz très toxiques",
                "Retirez les piles de tous les appareils avant de stocker ou transporter",
                "Conservez dans un endroit sec — l'humidité endommage les circuits",
                "Ne jetez jamais avec les ordures ménagères — illégal et dangereux",
                "Apportez à un centre agréé de déchets électroniques ou magasin d'électronique",
                "Ou contactez un acheteur dans 'Acheteurs'",
            ],
        },
        "safety": {
            "sw": "☢️ E-waste ni HATARI SANA. Usichome, usivunje wala kuitupa ovyo. Betri zina sumu kali. Vifaa vya zamani vina zebaki na risasi — zinaweza kusababisha saratani.",
            "en": "☢️ E-waste is HIGHLY HAZARDOUS. Never burn, break, or dump carelessly. Batteries contain strong toxins. Old devices contain mercury and lead — cancer risk.",
            "fr": "☢️ Les déchets électroniques sont TRÈS DANGEREUX. Ne jamais brûler, casser ou jeter. Les piles contiennent des toxines. Les vieux appareils contiennent du mercure et du plomb.",
        },
        "recommendation": {
            "sw": "✅ Peleka e-waste mara moja kwenye kituo kilichoidhinishwa. Usihifadhi kwa muda mrefu nyumbani. Wasiliana na mnunuzi wa e-waste kwa maelekezo. Kumbuka: e-waste ina metali zenye thamani — inaweza kukupa pesa.",
            "en": "✅ Take e-waste immediately to a certified facility. Do not store at home long-term. Contact an e-waste buyer for guidance. Remember: e-waste contains valuable metals — it can earn you money.",
            "fr": "✅ Apportez immédiatement les déchets électroniques à un centre agréé. Ne stockez pas longtemps chez vous. Les déchets électroniques contiennent des métaux précieux — ils peuvent vous rapporter de l'argent.",
        },
    },

    # ── TEXTILE ───────────────────────────────────────────────────
    "textile": {
        "type": "Vazi/Nguo", "typeEn": "Textile", "typeFr": "Textile",
        "badge": "badge-textile", "icon": "👕",
        "market_value": {"sw": "Wastani — nguo nzuri zina bei nzuri; zilizochakaa zina bei ndogo", "en": "Medium — good clothes fetch fair prices; worn-out items are lower value", "fr": "Moyen — les bons vêtements se vendent bien; les usés ont une valeur moindre"},
        "env_impact":   {"sw": "Inachukua miaka 20–200 kuoza kulingana na nyenzo; uzalishaji wa nguo unahitaji maji mengi", "en": "Takes 20–200 years to decompose depending on material; textile production uses enormous water", "fr": "Met 20–200 ans à se décomposer selon le matériau; la production textile consomme énormément d'eau"},
        "desc": {
            "sw": "Hii ni taka ya nguo au vitambaa. Nguo nzuri zinaweza kutumika tena au kuuzwa, na zilizochakaa zinaweza kurecyclewa kuwa vitambaa vipya.",
            "en": "This is textile waste. Good clothes can be reused or sold, and worn-out ones can be recycled into new fabric or insulation material.",
            "fr": "Ceci est un déchet textile. Les bons vêtements peuvent être réutilisés ou vendus, les usés recyclés en nouveau tissu ou en matériau isolant.",
        },
        "steps": {
            "sw": [
                "Chunguza kila kitu — zipi zinaweza kutumika tena na zipi haziwezi",
                "Nzuri na zisizochakaa: toa kwa misaada, uze au badilishana na wengine",
                "Zinazoweza kuoshwa: ziosha kwanza kabla ya kutoa au kurecycle",
                "Zilizochakaa kabisa: peleka vituo vya textile recycling au makampuni ya nguo",
                "Hifadhi katika mfuko safi na kavu hadi unapofikisha kituo",
            ],
            "en": [
                "Sort everything — which items can be reused and which cannot",
                "Good condition: donate to charity, sell, or swap with others",
                "Washable items: wash before donating or recycling",
                "Completely worn-out: take to a textile recycling centre or clothing company",
                "Store in a clean, dry bag until you reach the centre",
            ],
            "fr": [
                "Triez tout — lesquels peuvent être réutilisés et lesquels non",
                "En bon état : donnez à une association, vendez ou échangez",
                "Lavables : lavez avant de donner ou de recycler",
                "Très usés : apportez à un centre de recyclage textile ou une entreprise de vêtements",
                "Rangez dans un sac propre et sec jusqu'au centre",
            ],
        },
        "safety": {
            "sw": "ℹ️ Nguo kwa ujumla si hatari. Nguo zilizochafuliwa na kemikali, mafuta ya gari au rangi za sumu — zishughulikiwe kwa kinga na zitupwe kwa njia sahihi.",
            "en": "ℹ️ Textiles are generally not hazardous. Clothes contaminated with chemicals, motor oil, or toxic dyes — handle with gloves and dispose of properly.",
            "fr": "ℹ️ Les textiles ne sont généralement pas dangereux. Les vêtements contaminés par des produits chimiques, de l'huile moteur ou des teintures toxiques — manipulez avec des gants.",
        },
        "recommendation": {
            "sw": "✅ Toa nguo nzuri kwa misaada au uziuze — zinaweza kukupa pesa badala ya kutupwa. Nguo za pamba (cotton) na sufu ni rahisi zaidi kurecycle. Zipeleke vituo vya textile recycling.",
            "en": "✅ Donate good clothes to charity or sell them — they can earn money instead of being wasted. Cotton and wool recycle most easily. Take worn items to a textile recycling centre.",
            "fr": "✅ Donnez les bons vêtements ou vendez-les — ils peuvent rapporter de l'argent. Le coton et la laine se recyclent le mieux. Portez les usés à un centre de recyclage textile.",
        },
    },
}


# ═══════════════════════════════════════════════════════════════════
#  YOLO MODEL
# ═══════════════════════════════════════════════════════════════════
_YOLO_MODEL = None


def _get_yolo_model():
    global _YOLO_MODEL
    if _YOLO_MODEL is not None:
        return _YOLO_MODEL
    try:
        from ultralytics import YOLO
        model_path = os.getenv("YOLO_MODEL_PATH", "yolo11n.pt")
        if not Path(model_path).is_absolute():
            candidate = Path(__file__).parent / model_path
            if candidate.exists():
                model_path = str(candidate)
        _YOLO_MODEL = YOLO(model_path)
        return _YOLO_MODEL
    except Exception:
        return None


# Comprehensive mapping: every COCO label + common waste-specific labels
LABEL_TO_WASTE: dict[str, str] = {
    # ── Plastic
    "bottle": "plastic", "cup": "plastic", "plastic": "plastic",
    "plastic waste": "plastic", "plastic_waste": "plastic",
    "polyethylene": "plastic", "container": "plastic", "bag": "plastic",
    "plastic bag": "plastic", "straw": "plastic", "jug": "plastic",
    "bucket": "plastic", "bin": "plastic", "jerry can": "plastic",
    "sachet": "plastic", "packaging": "plastic", "polythene": "plastic",
    "pet bottle": "plastic", "hdpe": "plastic", "pvc": "plastic",
    # ── Paper
    "book": "paper", "paper": "paper", "cardboard": "paper",
    "paper waste": "paper", "paper_waste": "paper", "carton": "paper",
    "newspaper": "paper", "magazine": "paper", "box": "paper",
    "envelope": "paper", "tissue": "paper", "pamphlet": "paper",
    # ── Glass
    "wine glass": "glass", "glass": "glass", "glass waste": "glass",
    "glass_waste": "glass", "mirror": "glass", "vase": "glass",
    "jar": "glass", "glass bottle": "glass", "glass jar": "glass",
    # ── Metal
    "can": "metal", "metal": "metal", "fork": "metal", "knife": "metal",
    "spoon": "metal", "scissors": "metal", "metal waste": "metal",
    "metal_waste": "metal", "scrap metal": "metal", "tin": "metal",
    "aluminum": "metal", "aluminium": "metal", "iron": "metal",
    "steel": "metal", "copper": "metal", "wire": "metal",
    "pipe": "metal", "nail": "metal", "screw": "metal",
    "pan": "metal", "pot": "metal",
    # ── Organic
    "banana": "organic", "apple": "organic", "orange": "organic",
    "broccoli": "organic", "carrot": "organic", "hot dog": "organic",
    "pizza": "organic", "sandwich": "organic", "food": "organic",
    "organic waste": "organic", "organic_waste": "organic",
    "food waste": "organic", "fruit": "organic", "vegetable": "organic",
    "leaf": "organic", "leaves": "organic", "grass": "organic",
    "plant": "organic", "flower": "organic", "wood": "organic",
    "cake": "organic", "donut": "organic", "bread": "organic",
    # ── E-Waste
    "laptop": "ewaste", "cell phone": "ewaste", "keyboard": "ewaste",
    "mouse": "ewaste", "remote": "ewaste", "tv": "ewaste",
    "monitor": "ewaste", "e-waste": "ewaste", "ewaste": "ewaste",
    "electronic waste": "ewaste", "electronic_waste": "ewaste",
    "battery": "ewaste", "charger": "ewaste", "cable": "ewaste",
    "phone": "ewaste", "tablet": "ewaste", "computer": "ewaste",
    "speaker": "ewaste", "headphone": "ewaste", "microwave": "ewaste",
    "television": "ewaste", "printer": "ewaste",
    # ── Textile
    "backpack": "textile", "handbag": "textile", "tie": "textile",
    "suitcase": "textile", "umbrella": "textile",
    "textile waste": "textile", "textile_waste": "textile",
    "clothes": "textile", "clothing": "textile", "shoe": "textile",
    "shoes": "textile", "shirt": "textile", "jacket": "textile",
    "pants": "textile", "dress": "textile", "fabric": "textile",
    "cloth": "textile", "rug": "textile", "blanket": "textile",
    "hat": "textile", "cap": "textile",
    # ── Generic waste fallback
    "trash": "plastic", "garbage": "plastic", "waste": "plastic",
    "rubbish": "plastic", "litter": "plastic", "debris": "plastic",
    "dump": "plastic",
}

CONFIDENCE_THRESHOLD = float(os.getenv("YOLO_CONFIDENCE", "0.20"))
ACCEPT_THRESHOLD     = float(os.getenv("YOLO_ACCEPT_CONFIDENCE", "0.28"))


def _classify_with_yolo(file_storage):
    """Run YOLO. Returns (waste_key, confidence, label) or None."""
    model = _get_yolo_model()
    if model is None or Image is None:
        return None
    try:
        file_storage.stream.seek(0)
        img = Image.open(file_storage.stream).convert("RGB")
        results = model.predict(source=img, conf=CONFIDENCE_THRESHOLD, verbose=False)
        if not results:
            return None
        boxes = results[0].boxes
        names = results[0].names
        if boxes is None or len(boxes) == 0:
            return None

        # Collect all detections and sort by confidence
        detections = sorted(
            [(float(b.conf[0]), str(names[int(b.cls[0])]).lower().strip()) for b in boxes],
            reverse=True,
        )

        for conf, label in detections:
            waste_key = LABEL_TO_WASTE.get(label)
            if waste_key is None:
                # partial match
                for key, cat in LABEL_TO_WASTE.items():
                    if key in label or label in key:
                        waste_key = cat
                        break
            if waste_key:
                return waste_key, conf, f"YOLO: {label} ({conf:.0%})"

        return None
    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════
#  COLOR / TEXTURE HEURISTIC FALLBACK
#  Uses PIL image statistics to make a best-guess classification
#  when YOLO cannot identify any known object.
# ═══════════════════════════════════════════════════════════════════

def _heuristic_classify(file_storage) -> tuple[str, float, str] | None:
    """
    Analyse dominant colours and image statistics to classify waste.
    Returns (waste_key, confidence, description) or None.

    Heuristic rules (in priority order):
      1. Very high brightness + transparency hints → glass
      2. Dark, metallic, cool greys with low saturation → metal
      3. Warm browns/greens with high variation → organic
      4. Very bright, solid colours (red/blue/yellow/white) → plastic
      5. Beige/brown tones, low saturation, uniform texture → paper
      6. Dark screen-like proportions with black rectangles → ewaste
      7. Warm/pastel irregular shapes → textile
    """
    if Image is None or ImageStat is None:
        return None
    try:
        file_storage.stream.seek(0)
        img = Image.open(file_storage.stream).convert("RGB")

        # Resize for fast analysis
        img = img.resize((128, 128), Image.LANCZOS)
        stat = ImageStat.Stat(img)

        r_mean, g_mean, b_mean = stat.mean[0], stat.mean[1], stat.mean[2]
        r_std,  g_std,  b_std  = stat.stddev[0], stat.stddev[1], stat.stddev[2]

        brightness   = (r_mean + g_mean + b_mean) / 3.0
        saturation   = max(r_mean, g_mean, b_mean) - min(r_mean, g_mean, b_mean)
        total_std    = (r_std + g_std + b_std) / 3.0   # texture roughness
        warmth       = r_mean - b_mean                  # positive = warm/red, negative = cool/blue
        greenness    = g_mean - (r_mean + b_mean) / 2  # positive = green/organic

        # ── 1. Glass: very bright, low saturation, high b/g channel
        if brightness > 180 and saturation < 30 and total_std < 25:
            return "glass", 0.45, "Heuristic: bright, low-saturation (glass)"

        # ── 2. Metal: mid-grey brightness, very low saturation, cold tone
        if 60 < brightness < 160 and saturation < 25 and warmth < 5 and total_std < 30:
            return "metal", 0.42, "Heuristic: grey, low-saturation (metal)"

        # ── 3. Organic: brown/green tones, warm or green, high variation
        if (greenness > 8 or (warmth > 5 and r_mean > 80 and r_mean < 180)) and total_std > 20:
            return "organic", 0.40, "Heuristic: warm/green tones (organic)"

        # ── 4. E-Waste: dark image with low brightness, cold tone
        if brightness < 70 and saturation < 35 and warmth < 0:
            return "ewaste", 0.38, "Heuristic: dark, cold tone (e-waste)"

        # ── 5. Paper: beige/light-brown, low saturation, low std
        if brightness > 140 and saturation < 45 and warmth > -5 and total_std < 30:
            return "paper", 0.38, "Heuristic: light beige/brown (paper)"

        # ── 6. Textile: pastel/warm, medium brightness, medium variation
        if 80 < brightness < 180 and saturation > 15 and total_std > 15:
            return "textile", 0.36, "Heuristic: warm/pastel medium tones (textile)"

        # ── 7. Plastic: high saturation bright colours
        if saturation > 40 and brightness > 100:
            return "plastic", 0.36, "Heuristic: bright saturated colour (plastic)"

        # ── Default fallback
        return "plastic", 0.32, "Heuristic: default fallback (plastic)"

    except Exception:
        return None


# ═══════════════════════════════════════════════════════════════════
#  PUBLIC API
# ═══════════════════════════════════════════════════════════════════

def classify_waste(file_storage):
    """
    Classify a waste image using YOLO + heuristic fallback.
    Returns a dict always containing:
      accepted    bool
      waste       dict (if accepted)
      source      str
      confidence  float (if accepted)
      needs_review bool (if accepted)
      reason / reasonEn  str (if rejected)
    """
    # ── Step 1: YOLO
    yolo_result = _classify_with_yolo(file_storage)

    if yolo_result:
        waste_key, confidence, source = yolo_result
    else:
        # ── Step 2: Heuristic fallback
        heuristic_result = _heuristic_classify(file_storage)
        if heuristic_result:
            waste_key, confidence, source = heuristic_result
        else:
            # ── Step 3: Full rejection
            return {
                "accepted": False,
                "reason": (
                    "Picha hii haikutambuliwa. Jaribu hivi:\n"
                    "• Piga picha karibu zaidi na taka\n"
                    "• Hakikisha taka inajaza sehemu kubwa ya picha\n"
                    "• Tumia mwanga mzuri, epuka kivuli\n"
                    "• Piga picha ya taka moja kwa wakati mmoja"
                ),
                "reasonEn": (
                    "This image could not be identified. Please try:\n"
                    "• Take a closer photo of the waste\n"
                    "• Make sure the waste fills most of the frame\n"
                    "• Use good lighting, avoid shadows\n"
                    "• Photograph one waste item at a time"
                ),
                "reasonFr": (
                    "Cette image n'a pas pu être identifiée. Essayez :\n"
                    "• Prenez une photo plus proche du déchet\n"
                    "• Le déchet doit occuper la majorité du cadre\n"
                    "• Bon éclairage, évitez les ombres\n"
                    "• Photographiez un seul déchet à la fois"
                ),
                "source": "No detection",
            }

    # Very low confidence — reject
    if confidence < ACCEPT_THRESHOLD:
        return {
            "accepted": False,
            "reason": (
                f"Uhakika wa utambuzi ni mdogo ({confidence:.0%}). "
                "Tafadhali piga picha iliyo wazi zaidi, karibu zaidi na taka, "
                "na kwa mwanga mzuri."
            ),
            "reasonEn": (
                f"Detection confidence is too low ({confidence:.0%}). "
                "Please take a clearer photo, closer to the waste, with good lighting."
            ),
            "reasonFr": (
                f"La confiance de détection est trop faible ({confidence:.0%}). "
                "Prenez une photo plus nette, plus proche du déchet, avec un bon éclairage."
            ),
            "source": source,
            "confidence": confidence,
        }

    # Build result
    waste = dict(WASTE_DB[waste_key])
    waste["key"]        = waste_key
    waste["confidence"] = confidence

    return {
        "accepted":     True,
        "waste":        waste,
        "source":       source,
        "confidence":   confidence,
        "needs_review": confidence < 0.55,   # show "verify visually" warning
        "demo":         "Heuristic" in source,  # flag if heuristic was used
    }
