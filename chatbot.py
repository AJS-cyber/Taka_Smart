"""TakaSmart Chatbot — comprehensive waste & environment knowledge engine.
Handles any question about waste, recycling, environment in sw/en/fr.
Responses use markdown: **bold**, ## heading, numbered lists, bullet points.
"""
import re, unicodedata

KB = {}

KB['plastic'] = {
'sw': """## 🧴 Plastiki

**Plastiki ni nini?**
Plastiki ni nyenzo iliyotengenezwa kutoka kwa kemikali za petroli. Inachukua **miaka 100-500 kuoza** na inadhuru sana mazingira.

**Aina kuu:**
• **PET** - chupa za maji na vinywaji. Thamani ya juu zaidi sokoni
• **HDPE** - ndoo, mitungi, mifuko mizito
• **PVC** - mabomba, fremu za madirisha
• **LDPE** - mifuko minyepesi
• **PP** - vifuniko, vyombo vya chakula

**Hatua za kurecycle:**
1. **Safisha** - ondoa mabaki ya chakula na vinywaji
2. **Tenganisha kwa aina** - PET pamoja, HDPE pamoja
3. **Bana** - kupunguza nafasi ya kuhifadhi
4. **Hifadhi pakavu** - mbali na jua moja kwa moja
5. **Peleka** kwa mnunuzi au kituo cha ukusanyaji

🚫 **Usichome plastiki kamwe** - hutoa dioxins na sumu kali kwa mapafu
💡 Angalia nambari 1-7 chini ya chombo - hii ndiyo aina ya plastiki
💰 PET na HDPE vina thamani zaidi - hifadhi tofauti na nyingine

**Athari kwa mazingira:**
Tani milioni 8 za plastiki huingia baharini kila mwaka. Inagawanyika kuwa microplastics ambazo zinaingia mwilini mwa samaki na hatimaye kwenye chakula chetu.""",

'en': """## 🧴 Plastic

**What is plastic?**
Plastic is a synthetic material made from petroleum chemicals. It takes **100-500 years to decompose** and causes serious environmental harm.

**Main types:**
• **PET** - water and drink bottles. Highest market value
• **HDPE** - buckets, canisters, heavy bags
• **PVC** - pipes, window frames
• **LDPE** - lightweight bags
• **PP** - bottle caps, food containers

**Recycling steps:**
1. **Clean** - remove food and drink residue
2. **Sort by type** - PET together, HDPE together
3. **Crush** - reduce storage volume
4. **Store dry** - away from direct sunlight
5. **Take** to a buyer or plastic collection point

🚫 **Never burn plastic** - releases dioxins and toxins that damage lungs
💡 Check the number 1-7 at the bottom of the container - this is the plastic type
💰 PET and HDPE have the highest value - store separately from other plastics

**Environmental impact:**
8 million tonnes of plastic enter the ocean every year. It breaks down into microplastics that enter fish and eventually our food chain.""",

'fr': """## 🧴 Plastique

**Qu'est-ce que le plastique ?**
Le plastique est un materiau synthetique fabrique a partir de produits chimiques petroliers. Il met **100 a 500 ans a se decomposer** et cause de graves dommages environnementaux.

**Types principaux :**
• **PET** - bouteilles d'eau et de boissons. Valeur marchande la plus elevee
• **HDPE** - seaux, bidons, sacs resistants
• **PVC** - tuyaux, chassis de fenetres
• **LDPE** - sacs legers
• **PP** - bouchons, contenants alimentaires

**Etapes de recyclage :**
1. **Nettoyer** - retirer les residus alimentaires
2. **Trier par type** - PET ensemble, HDPE ensemble
3. **Ecraser** - reduire le volume de stockage
4. **Conserver au sec** - a l'abri du soleil
5. **Apporter** a un acheteur ou point de collecte

🚫 **Ne jamais bruler le plastique** - libere des dioxines et toxines pour les poumons
💡 Verifiez le numero 1-7 en bas du contenant - c'est le type de plastique
💰 PET et HDPE ont la plus haute valeur marchande"""
}

KB['paper'] = {
'sw': """## 📦 Karatasi na Kadibodi

**Ukweli muhimu:**
Karatasi inaweza kurecyclewa **mara 5-7** kabla ya nyuzi zake kukuwa fupi sana.
Kila tani moja iliyorecyclewa inaokoa **miti 17** na lita 26,000 za maji.

**Zinazoweza kurecyclewa:**
• Karatasi nyeupe za ofisi, magazeti, majarida
• Kadibodi na makasha, mifuko ya karatasi

**Haziwezi kurecyclewa:**
• Karatasi zenye mafuta (sanduku la pizza)
• Karatasi iliyolowa kabisa - nyuzi zimeharibiwa
• Tissues na serviettes zilizotumika

**Hatua:**
1. **Tenganisha** karatasi kutoka kwa taka nyingine
2. **Ondoa** staples, clips, na tape
3. **Zikunje au zibane** kwa kamba - kupunguza ukubwa
4. **Hifadhi KAVU kabisa** - unyevu unafunika thamani yake
5. **Peleka** kwa recycler au mnunuzi

💰 Kadibodi nzito ina thamani zaidi kuliko karatasi nyembamba
💡 Okoa makasha ya bidhaa - yanauzwa vizuri""",

'en': """## 📦 Paper and Cardboard

**Key facts:**
Paper can be recycled **5-7 times** before its fibres become too short.
Every tonne of recycled paper saves **17 trees** and 26,000 litres of water.

**Recyclable types:**
• White office paper, newspapers, magazines
• Cardboard boxes, paper bags

**NOT recyclable:**
• Greasy paper (pizza boxes, wrapping paper)
• Completely wet paper - fibres are destroyed
• Used tissues and napkins

**Steps:**
1. **Separate** paper from other waste
2. **Remove** staples, clips, and tape
3. **Flatten or bundle** with string - reduce volume
4. **Keep COMPLETELY DRY** - moisture destroys its value
5. **Take** to a recycler or buyer

💰 Heavy cardboard is worth more than thin paper
💡 Save product boxes - they sell well""",

'fr': """## 📦 Papier et Carton

**Faits importants :**
Le papier peut etre recycle **5 a 7 fois** avant que ses fibres soient trop courtes.
Chaque tonne de papier recycle sauve **17 arbres** et 26 000 litres d'eau.

**Types recyclables :**
• Papier de bureau blanc, journaux, magazines
• Carton et boites, sacs en papier

**NON recyclables :**
• Papier gras (boites a pizza, papier d'emballage)
• Papier completement mouille
• Mouchoirs et serviettes usages

**Etapes :**
1. **Separer** le papier des autres dechets
2. **Retirer** agrafes, trombones et scotch
3. **Aplatir ou lier** en fagots - reduire le volume
4. **Garder COMPLETEMENT SEC** - l'humidite detruit sa valeur
5. **Apporter** a un recycleur ou acheteur

💰 Le carton epais vaut plus que le papier fin
💡 Gardez les boites de produits - elles se vendent bien"""
}

KB['glass'] = {
'sw': """## 🍶 Kioo

**Ukweli wa ajabu:**
Kioo kinaweza kurecyclewa **mara nyingi bila kikomo** bila kupoteza ubora wake.
Kioo **hakiozi kamwe** - kinabaki ardhini milele kama hakijarecyclewa.

**Aina (gawanya kwa rangi):**
• **Nyeupe/wazi** - chupa za maji na vinywaji
• **Kijani** - chupa za mvinyo na bia
• **Kahawia/Amber** - chupa za dawa
• *Kioo cha madirisha - haichanganyiwi na chupa*

**Hatua za usalama:**
1. **Vaa kinga** - glavu nzito au kitambaa - kioo hukata vibaya sana
2. **Tenganisha kwa rangi** - rangi tofauti zinapaswa kutenganishwa
3. **Safisha** - ondoa mabaki ya chakula au vinywaji ndani
4. **Hifadhi** kwenye sanduku gumu au mfuko mzito
5. **Peleka** kituo cha kukusanya kioo

⚠️ **Kioo kilichovunjika** ni hatari kubwa - vaa viatu, weka kwenye sanduku lenye lebo "KIOO HATARI"
💡 Chupa nzima zina thamani zaidi kuliko vipande""",

'en': """## 🍶 Glass

**Amazing fact:**
Glass can be recycled **infinitely** without losing quality.
Glass **never decomposes** - it stays in the ground forever if not recycled.

**Types (separate by colour):**
• **Clear/white** - water and drink bottles
• **Green** - wine and beer bottles
• **Brown/Amber** - medicine bottles
• *Window glass - not mixed with bottles*

**Safety steps:**
1. **Wear protection** - heavy gloves or thick cloth - glass cuts badly
2. **Sort by colour** - different colours must be kept separate
3. **Clean** - remove food or drink residue inside
4. **Store** in a rigid box or heavy bag
5. **Take** to a glass collection point

⚠️ **Broken glass** is very dangerous - wear shoes, store in a box labelled "BROKEN GLASS - DANGER"
💡 Whole bottles are worth more than fragments""",

'fr': """## 🍶 Verre

**Fait remarquable :**
Le verre peut etre recycle **a l'infini** sans perdre de qualite.
Le verre **ne se decompose jamais** - il reste dans le sol eternellement.

**Types (trier par couleur) :**
• **Incolore/blanc** - bouteilles d'eau et de boissons
• **Vert** - bouteilles de vin et de biere
• **Brun/Ambre** - bouteilles de medicaments
• *Verre de fenetre - ne pas melanger avec les bouteilles*

**Etapes de securite :**
1. **Porter une protection** - gants epais ou chiffon - le verre coupe
2. **Trier par couleur** - les couleurs differentes doivent etre separees
3. **Nettoyer** - retirer les residus a l'interieur
4. **Conserver** dans une boite rigide ou un sac resistant
5. **Apporter** a un point de collecte de verre

⚠️ Le **verre brise** est tres dangereux - portez des chaussures, mettez dans une boite etiquetee "VERRE BRISE - DANGER"
💡 Les bouteilles entieres valent plus que les fragments"""
}

KB['metal'] = {
'sw': """## 🔩 Chuma na Metali

**Kwa nini chuma ni muhimu?**
Chuma kinaweza kurecyclewa **mara nyingi bila kupoteza ubora**. Kurecycle aluminium kunaokoa **95% ya nishati** ikilinganishwa na kuzalisha mpya.

**Aina na thamani zao:**
• **Aluminium** - nyepesi, rangi ya fedha. Thamani ya juu zaidi. Chupa za bia, makopo
• **Shaba (Copper)** - rangi ya dhahabu/nyekundu. Thamani ya juu sana. Waya, bomba
• **Chuma cha kawaida (Steel)** - nzito, hutu. Fremu, mabati, vyombo
• **Bati (Tin)** - makopo ya chakula, jaa

**Hatua:**
1. **Tenganisha aina** - aluminium, shaba, chuma - ziwekwe tofauti
2. **Ondoa sehemu zisizo za chuma** - plastiki, mpira, kioo
3. **Safisha kutu** inapowezekana - thamani huongezeka
4. **Bana au funga kwa kamba** - kupunguza ukubwa
5. **Wasiliana na mnunuzi wa scrap metal**

⚠️ Chuma chenye ncha kali **hukata na kuchomeka** - vaa glavu za ngozi
🚫 Chuma chenye kutu - usiguze bila kinga (hatari ya tetanasi)
💰 Aluminium na shaba vina bei nzuri zaidi - zihifadhi tofauti""",

'en': """## 🔩 Metal and Scrap

**Why is metal valuable?**
Metal can be recycled **many times without losing quality**. Recycling aluminium saves **95% of the energy** compared to producing new metal.

**Types and their value:**
• **Aluminium** - lightweight, silver colour. Highest value. Beer cans, foil
• **Copper** - golden/reddish colour. Very high value. Wires, pipes
• **Steel** - heavy, rusts. Frames, corrugated iron, containers
• **Tin** - food cans, lids

**Steps:**
1. **Separate by type** - aluminium, copper, steel - keep apart
2. **Remove non-metal parts** - plastic, rubber, glass
3. **Clean rust** where possible - increases value
4. **Crush or bundle with rope** - reduce volume
5. **Contact a scrap metal buyer**

⚠️ Sharp metal **cuts and punctures** - wear leather gloves
🚫 Rusty metal - do not touch without protection (tetanus risk)
💰 Aluminium and copper fetch the best prices - keep them separate""",

'fr': """## 🔩 Metal et Ferraille

**Pourquoi le metal est-il precieux ?**
Le metal peut etre recycle **de nombreuses fois sans perdre de qualite**. Recycler l'aluminium economise **95% de l'energie** par rapport a la production neuve.

**Types et leurs valeurs :**
• **Aluminium** - leger, couleur argent. Valeur la plus elevee. Canettes, papier aluminium
• **Cuivre** - couleur or/rougeâtre. Tres haute valeur. Fils, tuyaux
• **Acier** - lourd, rouille. Charpentes, toles, contenants
• **Fer-blanc** - boites alimentaires, couvercles

**Etapes :**
1. **Separer par type** - aluminium, cuivre, acier - garder separes
2. **Retirer les parties non metalliques** - plastique, caoutchouc, verre
3. **Nettoyer la rouille** si possible - augmente la valeur
4. **Ecraser ou lier avec une corde** - reduire le volume
5. **Contacter un acheteur de ferraille**

⚠️ Le metal tranchant **coupe et perfore** - portez des gants en cuir
🚫 Metal rouille - ne touchez pas sans protection (risque de tetanos)
💰 Aluminium et cuivre ont les meilleurs prix - gardez-les separes"""
}

KB['organic'] = {
'sw': """## 🍂 Taka za Kikolojia na Compost

**Ni zipi?**
Taka za kikolojia ni vitu vinavyotoka kwa asili: mabaki ya chakula, majani, matunda yaliyooza, magome ya miti.

**Kwa nini compost?**
Badala ya kutupa kwenye madampo (ambapo hutoa methane - gesi ya chafu), compost inageuza taka kuwa **mbolea nzuri ya bure** kwa bustani na shamba.

## Jinsi ya kutengeneza compost:

**Unavyohitaji:**
• Kisanduku au shimo (angalau 1m x 1m x 0.5m)
• Mabaki ya chakula (mboga, matunda, ganda)
• Majani makavu au udongo
• Maji kidogo

**Hatua:**
1. **Tabaka la kwanza** - majani makavu au udongo chini
2. **Ongeza** mabaki ya chakula
3. **Funika** na udongo kidogo au majani makavu
4. **Rudia** tabaka hadi kisanduku kijae
5. **Geuza** kila siku 2-3 kwa hewa - inasaidia kuoza haraka
6. **Ongeza maji kidogo** ikiwa ni kavu sana
7. **Wiki 8-12 baadaye** - mbolea iko tayari

**Epuka kuweka:**
🚫 Plastiki, kioo, chuma au kemikali
🚫 Nyama nyingi au maziwa - huvutia wadudu na kunuka
🚫 Taka za binadamu au wanyama wa kipenzi

💡 Compost nzuri ina harufu ya udongo wa msituni - ikiwa inanuka sana, ongeza udongo na geuza""",

'en': """## 🍂 Organic Waste and Composting

**What is organic waste?**
Organic waste includes anything that comes from nature: food scraps, leaves, rotting fruit, tree bark.

**Why compost?**
Instead of dumping in landfill (which releases methane - a greenhouse gas), composting turns waste into **free, high-quality fertiliser** for gardens and farms.

## How to make compost:

**What you need:**
• A bin or pit (at least 1m x 1m x 0.5m)
• Food scraps (vegetables, fruit, peels)
• Dry leaves or soil
• A little water

**Steps:**
1. **First layer** - dry leaves or soil at the bottom
2. **Add** food scraps
3. **Cover** with a little soil or dry leaves
4. **Repeat** layers until the bin is full
5. **Turn** every 2-3 days for aeration - speeds up decomposition
6. **Add a little water** if too dry
7. **After 8-12 weeks** - fertiliser is ready

**Do NOT add:**
🚫 Plastic, glass, metal or chemicals
🚫 Large amounts of meat or dairy - attracts pests and causes odour
🚫 Human or pet waste

💡 Good compost smells like forest soil - if it smells bad, add soil and turn it""",

'fr': """## 🍂 Dechets Organiques et Compostage

**Qu'est-ce que les dechets organiques ?**
Les dechets organiques comprennent tout ce qui vient de la nature : restes alimentaires, feuilles, fruits pourris, ecorces d'arbres.

**Pourquoi composter ?**
Au lieu de jeter en decharge (ce qui libere du methane), le compostage transforme les dechets en **engrais gratuit de haute qualite**.

## Comment faire du compost :

**Ce dont vous avez besoin :**
• Un bac ou une fosse (au moins 1m x 1m x 0.5m)
• Restes alimentaires (legumes, fruits, epluchures)
• Feuilles seches ou terre
• Un peu d'eau

**Etapes :**
1. **Premiere couche** - feuilles seches ou terre en bas
2. **Ajouter** les restes alimentaires
3. **Couvrir** d'un peu de terre ou feuilles seches
4. **Repeter** les couches jusqu'au remplissage
5. **Retourner** tous les 2-3 jours - accelere la decomposition
6. **Ajouter un peu d'eau** si trop sec
7. **Apres 8-12 semaines** - l'engrais est pret

**Ne PAS ajouter :**
🚫 Plastique, verre, metal ou produits chimiques
🚫 Grande quantite de viande ou produits laitiers
🚫 Dechets humains ou d'animaux domestiques

💡 Un bon compost sent la terre de foret - s'il sent mauvais, ajoutez de la terre et retournez-le"""
}

KB['ewaste'] = {
'sw': """## 💻 E-Waste (Taka za Elektroniki)

**E-waste ni nini?**
E-waste ni vifaa vya elektroniki vilivyochakaa au visivyofanya kazi: simu, kompyuta, televisheni, betri, vichajio, n.k.

**Kwa nini ni hatari sana?**
E-waste ina kemikali hatari kama:
• **Risasi (Lead)** - inasababisha uharibifu wa ubongo, hasa kwa watoto
• **Zebaki (Mercury)** - inasababisha uharibifu wa mfumo wa neva
• **Cadmium** - inasababisha saratani ya figo
• **Arsenic** - sumu kali inayosababisha saratani

**Na pia ina thamani:**
• Dhahabu ndogo (gold), shaba (copper), fedha ndogo (silver)
• Simu moja ina dhahabu zaidi kuliko tani moja ya madini ya dhahabu

**Hatua za kushughulikia kwa usalama:**
1. **Toa betri** kutoka kwa vifaa vyote kabla ya kuhifadhi
2. **Hifadhi mahali pakavu** - unyevu unasababisha kemikali kutiririka
3. **Usitupe** kwenye taka za kawaida - ni haramu na hatari
4. **Peleka** kituo kilichoidhinishwa cha e-waste
5. Au **wasiliana na mnunuzi** wa e-waste kwenye TakaSmart

🚫 **Usichome e-waste kamwe** - betri zinaweza kulipuka, kemikali hutoa moshi wa sumu
🚫 **Usivunje** betri - asidi na kemikali zinaweza kutiririka na kuumiza macho na ngozi
💰 E-waste ina thamani - inaweza kukupa pesa badala ya kutupwa""",

'en': """## 💻 E-Waste (Electronic Waste)

**What is e-waste?**
E-waste is worn-out or broken electronic equipment: phones, computers, televisions, batteries, chargers, etc.

**Why is it very dangerous?**
E-waste contains hazardous chemicals including:
• **Lead** - causes brain damage, especially in children
• **Mercury** - damages the nervous system
• **Cadmium** - causes kidney cancer
• **Arsenic** - a strong poison that causes cancer

**But also valuable:**
• Trace gold, copper, and silver
• One smartphone contains more gold per kg than a tonne of gold ore

**Safe handling steps:**
1. **Remove batteries** from all devices before storing
2. **Store dry** - moisture causes chemicals to leach out
3. **Never dump** with regular waste - illegal and dangerous
4. **Take** to a certified e-waste facility
5. Or **contact a buyer** on TakaSmart

🚫 **Never burn e-waste** - batteries can explode, chemicals release toxic smoke
🚫 **Never break** batteries - acid and chemicals can damage eyes and skin
💰 E-waste has real value - it can earn you money instead of being dumped""",

'fr': """## 💻 Dechets Electroniques (E-Waste)

**Qu'est-ce que les dechets electroniques ?**
Les dechets electroniques sont des equipements usages ou en panne : telephones, ordinateurs, televiseurs, piles, chargeurs, etc.

**Pourquoi sont-ils tres dangereux ?**
Les dechets electroniques contiennent des produits chimiques dangereux :
• **Plomb** - cause des dommages cerebraux, surtout chez les enfants
• **Mercure** - endommage le systeme nerveux
• **Cadmium** - cause le cancer du rein
• **Arsenic** - poison puissant qui cause le cancer

**Mais aussi precieux :**
• Traces d'or, de cuivre et d'argent
• Un smartphone contient plus d'or par kg qu'une tonne de minerai d'or

**Etapes de manipulation securisee :**
1. **Retirer les piles** de tous les appareils avant de stocker
2. **Conserver au sec** - l'humidite fait fuir les produits chimiques
3. **Ne jamais jeter** avec les ordures menageres - illegal et dangereux
4. **Apporter** a un centre agree de dechets electroniques
5. Ou **contacter un acheteur** sur TakaSmart

🚫 **Ne jamais bruler les dechets electroniques** - les piles peuvent exploser
🚫 **Ne jamais casser** les piles - acide et produits chimiques peuvent blesser
💰 Les dechets electroniques ont une vraie valeur - ils peuvent vous rapporter de l'argent"""
}

KB['textile'] = {
'sw': """## 👕 Nguo na Vitambaa

**Kwa nini nguo ni tatizo?**
Utengenezaji wa nguo unachukua **maji mengi sana** - jeans moja inahitaji lita 7,500 za maji. Na nguo zinachukua **miaka 20-200 kuoza** kulingana na nyenzo.

**Aina za nyenzo:**
• **Pamba (Cotton)** - rahisi zaidi kurecycle, inaoza kwa miaka 1-5
• **Sufu (Wool)** - inaweza kurecyclewa na kutengeneza nguo mpya
• **Polyester/Nylon** - plastiki iliyoundwa kuwa nguo - vigumu kurecycle
• **Ngozi (Leather)** - inachukua miaka 50+ kuoza

**Maamuzi:**
1. **Chunguza** - zipi zinaweza kutumika tena? Zipi haziwezi?
2. **Nzuri na zisizochakaa**: Toa kwa misaada, uze, au badilishana
3. **Ziosha** kwanza kabla ya kutoa au kupeleka kurecycle
4. **Zilizochakaa kabisa**: Peleka vituo vya textile recycling
5. **Hifadhi** katika mfuko safi na kavu hadi unapofikisha kituo

💡 Nguo za pamba na sufu ni rahisi zaidi kurecycle - zitenge na nyingine
💰 Nguo nzuri za brand zinaweza kuuzwa na kukupa pesa nzuri
🌍 Kununua nguo za pili (second-hand) ni mchango mkubwa kwa mazingira""",

'en': """## 👕 Textiles and Clothing

**Why are clothes a problem?**
Textile production uses **enormous amounts of water** - one pair of jeans requires 7,500 litres. And clothes take **20-200 years to decompose** depending on the material.

**Material types:**
• **Cotton** - easiest to recycle, decomposes in 1-5 years
• **Wool** - can be recycled into new garments
• **Polyester/Nylon** - plastic made into fabric - hard to recycle
• **Leather** - takes 50+ years to decompose

**Decision guide:**
1. **Sort** - which can be reused? Which cannot?
2. **Good condition items**: Donate to charity, sell, or swap
3. **Wash first** before donating or recycling
4. **Completely worn-out**: Take to a textile recycling centre
5. **Store** in a clean dry bag until you reach the centre

💡 Cotton and wool are easiest to recycle - separate from synthetics
💰 Good branded clothes can sell and earn you good money
🌍 Buying second-hand clothes is a major contribution to the environment""",

'fr': """## 👕 Textiles et Vetements

**Pourquoi les vetements sont-ils un probleme ?**
La production textile utilise **enormement d'eau** - un jean necessite 7 500 litres. Et les vetements mettent **20 a 200 ans a se decomposer** selon le materiau.

**Types de materiaux :**
• **Coton** - le plus facile a recycler, se decompose en 1-5 ans
• **Laine** - peut etre recyclee en nouveaux vetements
• **Polyester/Nylon** - plastique transforme en tissu - difficile a recycler
• **Cuir** - met 50+ ans a se decomposer

**Guide de decision :**
1. **Trier** - lesquels peuvent etre reutilises ? Lesquels non ?
2. **En bon etat** : Donner a une association, vendre ou echanger
3. **Laver d'abord** avant de donner ou recycler
4. **Completement uses** : Apporter a un centre de recyclage textile
5. **Conserver** dans un sac propre et sec jusqu'au centre

💡 Coton et laine sont les plus faciles a recycler - separez des synthetiques
💰 Les bons vetements de marque peuvent se vendre et vous rapporter de l'argent
🌍 Acheter des vetements d'occasion est une grande contribution a l'environnement"""
}

KB['recycle'] = {
'sw': """## ♻️ Recycling - Jinsi na Kwa Nini

**Recycling ni nini?**
Recycling ni mchakato wa kubadilisha taka kuwa nyenzo mpya au bidhaa mpya. Ni hatua ya tatu katika kanuni ya **3R: Reduce, Reuse, Recycle**.

**Kwa nini recycling ni muhimu?**
• **Inaokoa rasilimali asili** - miti, madini, mafuta
• **Inapunguza uchafuzi** - hewa, maji, udongo
• **Inaokoa nishati** - kuzalisha kutoka taka inahitaji nishati kidogo
• **Inaunda ajira** - sekta ya recycling inaajiri watu wengi
• **Inapunguza tatizo la madampo** - Tanzania peke yake ina tatizo kubwa la taka

**Hatua kamili za kurecycle:**
1. **Tambua aina** - plastiki, karatasi, kioo, chuma, kikolojia, e-waste, nguo
2. **Tenganisha** - kila aina katika mfuko au chombo tofauti
3. **Safisha** - ondoa mabaki ya chakula, vinywaji, uchafu
4. **Hifadhi vizuri** - mahali pakavu, baridi, mbali na jua
5. **Tuma au peleka** kwa mnunuzi au kituo cha ukusanyaji

**Faida za kiuchumi:**
💰 Plastiki PET: TSh 200-500/kg
💰 Aluminium: TSh 800-1500/kg
💰 Shaba: TSh 2000-4000/kg
💰 Karatasi/Kadibodi: TSh 100-300/kg

🚫 **Usichome taka** - ni hatari na kupoteza thamani ya kiuchumi""",

'en': """## ♻️ Recycling - How and Why

**What is recycling?**
Recycling is the process of converting waste into new materials or products. It is the third step in the **3Rs principle: Reduce, Reuse, Recycle**.

**Why is recycling important?**
• **Saves natural resources** - trees, minerals, petroleum
• **Reduces pollution** - air, water, soil
• **Saves energy** - producing from waste requires much less energy
• **Creates jobs** - the recycling sector employs many people
• **Reduces landfill problems** - a major issue across Africa

**Complete recycling steps:**
1. **Identify the type** - plastic, paper, glass, metal, organic, e-waste, textile
2. **Separate** - each type in a different bag or container
3. **Clean** - remove food scraps, liquids, dirt
4. **Store properly** - dry, cool place, away from sunlight
5. **Send or take** to a buyer or collection point

**Economic benefits:**
💰 PET plastic: good market value
💰 Aluminium: very high value per kg
💰 Copper: highest value per kg
💰 Paper/Cardboard: moderate value

🚫 **Never burn waste** - dangerous and destroys economic value""",

'fr': """## ♻️ Recyclage - Comment et Pourquoi

**Qu'est-ce que le recyclage ?**
Le recyclage est le processus de conversion des dechets en nouveaux materiaux. C'est la troisieme etape du principe des **3R : Reduire, Reutiliser, Recycler**.

**Pourquoi le recyclage est-il important ?**
• **Economise les ressources naturelles** - arbres, mineraux, petrole
• **Reduit la pollution** - air, eau, sol
• **Economise l'energie** - produire a partir de dechets necessite beaucoup moins d'energie
• **Cree des emplois** - le secteur du recyclage emploie de nombreuses personnes
• **Reduit les problemes de decharges**

**Etapes completes de recyclage :**
1. **Identifier le type** - plastique, papier, verre, metal, organique, electronique, textile
2. **Separer** - chaque type dans un sac ou conteneur different
3. **Nettoyer** - retirer les restes alimentaires, liquides, saleté
4. **Bien conserver** - endroit sec et frais, a l'abri du soleil
5. **Envoyer ou apporter** a un acheteur ou point de collecte

🚫 **Ne jamais bruler les dechets** - dangereux et detruit la valeur economique"""
}

KB['hazardous'] = {
'sw': """## ☢️ Taka Hatari

**Ni zipi taka hatari?**
Taka hatari ni taka ambazo zinaweza kudhuru afya ya binadamu au mazingira ikiwa zitashughulikiwa vibaya.

**Mifano:**
• **Betri za aina zote** - betri za simu, gari, AA/AAA, betri za lithium
• **Sindano na vifaa vya matibabu** - sindano, lancets, vifaa vya upasuaji
• **Kemikali za kaya** - dawa za wadudu, rangi, sabuni kali, thinner
• **E-waste** - simu, kompyuta, TV chakavu (tazama sehemu ya e-waste)
• **Asbestos** - nyenzo za zamani za ujenzi (paa, mabomba ya zamani)
• **Betri za gari (acid batteries)** - asidi ya sulfuric ndani

**Sheria za usalama:**
1. **Usiguse** bila kinga za mkono na macho
2. **Usichome** - moshi wa sumu hatari angani
3. **Usitupe** kwenye taka za kawaida - unaweza kuumiza wengine
4. **Hifadhi** mbali na watoto, chakula, na maji ya kunywa
5. **Peleka** kituo kilichoidhinishwa cha taka hatari
6. **Kwa kiasi kikubwa**: Wasiliana na Wizara ya Mazingira au Halmashauri

**Dalili za kuathiriwa:**
• Asidi ya betri: inaweza kuchoma ngozi na macho - osha mara moja kwa maji mengi
• Kemikali za dawa za wadudu: kichefuchefu, maumivu ya kichwa - hewa safi haraka
• Moshi wa kemikali: matatizo ya kupumua - nenda nje mara moja

⚠️ Ikiwa umeguswa na kemikali hatari, wasiliana na Hospitali haraka""",

'en': """## ☢️ Hazardous Waste

**What is hazardous waste?**
Hazardous waste is waste that can harm human health or the environment if handled improperly.

**Examples:**
• **All types of batteries** - phone batteries, car batteries, AA/AAA, lithium
• **Needles and medical equipment** - syringes, lancets, surgical instruments
• **Household chemicals** - pesticides, paint, strong cleaning agents, thinner
• **E-waste** - old phones, computers, TVs (see e-waste section)
• **Asbestos** - old building materials (roofing, old pipes)
• **Car batteries (acid batteries)** - contain sulfuric acid inside

**Safety rules:**
1. **Do not touch** without hand and eye protection
2. **Do not burn** - releases toxic smoke
3. **Do not dump** with regular waste - can harm others
4. **Store** away from children, food, and drinking water
5. **Take** to a certified hazardous waste facility
6. **For large quantities**: Contact the Ministry of Environment or Municipal Council

**Signs of exposure:**
• Battery acid: can burn skin and eyes - rinse immediately with lots of water
• Pesticide chemicals: nausea, headache - get fresh air immediately
• Chemical smoke: breathing difficulties - go outside immediately

⚠️ If you have been exposed to hazardous chemicals, contact a hospital immediately""",

'fr': """## ☢️ Dechets Dangereux

**Qu'est-ce que les dechets dangereux ?**
Les dechets dangereux sont des dechets qui peuvent nuire a la sante humaine ou a l'environnement s'ils sont mal geres.

**Exemples :**
• **Toutes les piles** - piles de telephone, voiture, AA/AAA, lithium
• **Aiguilles et equipements medicaux** - seringues, lancettes
• **Produits chimiques menagers** - pesticides, peinture, detergents forts
• **Dechets electroniques** - vieux telephones, ordinateurs, televiseurs
• **Amiante** - anciens materiaux de construction
• **Batteries de voiture** - contiennent de l'acide sulfurique

**Regles de securite :**
1. **Ne pas toucher** sans protection des mains et des yeux
2. **Ne pas bruler** - libere de la fumee toxique
3. **Ne pas jeter** avec les ordures menageres
4. **Conserver** loin des enfants, des aliments et de l'eau potable
5. **Apporter** a un centre de dechets dangereux agree
6. **Pour les grandes quantites** : Contacter le Ministere de l'Environnement

⚠️ Si vous avez ete expose a des produits chimiques dangereux, contactez un hopital immediatement"""
}

KB['water'] = {
'sw': """## 💧 Uchafuzi wa Maji

**Jinsi taka zinavyoathiri maji:**
Taka zinazotupwa bila mpango huingia kwenye mito, maziwa, na bahari kupitia:
• Mvua inayoosha taka kutoka barabarani
• Kemikali za viwanda zinazomwagwa kwenye mito
• Plastiki inayovunjika na kuwa microplastics kwenye maji

**Athari:**
• **Viumbe vya majini** - samaki, kasa, ndege wa pwani wanakula plastiki au kufa
• **Maji ya kunywa** - kemikali zinaingia kwenye visima na mifereji ya maji
• **Afya ya binadamu** - kipindupindu, kuhara, typhoid kutoka kwa maji yaliyochafuliwa
• **Kilimo** - ardhi inayomwagiliwa kwa maji machafu inazalisha mazao yasio salama

**Tatizo la microplastics:**
Plastiki inagawanyika kuwa vipande vidogo sana (microplastics) ambazo:
• Zinapatikana kwenye mwili wa samaki
• Zinapatikana kwenye maji ya kunywa duniani kote
• Zinaweza kusababisha matatizo ya homoni na saratani

**Jinsi ya kusaidia:**
✅ Usitupe taka karibu na mto, ziwa, au pwani
✅ Ripoti uchafuzi wa maji kupitia TakaSmart
✅ Tumia mbolea ya asili (compost) badala ya kemikali
✅ Usimwage mafuta ya gari au kemikali kwenye ardhi au drani""",

'en': """## 💧 Water Pollution

**How waste affects water:**
Improperly disposed waste enters rivers, lakes, and oceans through:
• Rainwater washing waste off roads
• Industrial chemicals discharged into rivers
• Plastic breaking down into microplastics in water

**Effects:**
• **Marine life** - fish, turtles, seabirds eat plastic or die trapped in it
• **Drinking water** - chemicals contaminate wells and water pipes
• **Human health** - cholera, diarrhea, typhoid from contaminated water
• **Agriculture** - crops irrigated with polluted water are unsafe to eat

**The microplastics problem:**
Plastic breaks down into tiny pieces (microplastics) which:
• Are found inside the bodies of fish
• Are found in drinking water worldwide
• May cause hormonal problems and cancer

**How to help:**
✅ Never dump waste near rivers, lakes, or coastlines
✅ Report water pollution through TakaSmart
✅ Use natural fertiliser (compost) instead of chemicals
✅ Never pour motor oil or chemicals on the ground or drain""",

'fr': """## 💧 Pollution de l'Eau

**Comment les dechets affectent l'eau :**
Les dechets jetes sans gestion entrent dans les rivieres, lacs et oceans :
• Les pluies emportent les dechets des routes
• Les produits chimiques industriels deversés dans les rivieres
• Le plastique se degrade en microplastiques dans l'eau

**Effets :**
• **Faune marine** - poissons, tortues, oiseaux mangent du plastique ou meurent pieges
• **Eau potable** - les produits chimiques contaminent les puits et canalisations
• **Sante humaine** - cholera, diarrhee, typhoide de l'eau contaminee
• **Agriculture** - les cultures irriguees avec de l'eau polluee sont dangereuses

**Le probleme des microplastiques :**
Le plastique se degrade en minuscules particules (microplastiques) qui :
• Se trouvent dans le corps des poissons
• Se trouvent dans l'eau potable dans le monde entier
• Peuvent causer des problemes hormonaux et le cancer

**Comment aider :**
✅ Ne jamais jeter de dechets pres des rivieres, lacs ou cotes
✅ Signaler la pollution de l'eau via TakaSmart
✅ Utiliser de l'engrais naturel (compost) plutot que des produits chimiques"""
}

KB['air'] = {
'sw': """## 💨 Uchafuzi wa Hewa

**Jinsi taka zinavyochafua hewa:**
Uchafuzi wa hewa unaotokana na taka husababishwa hasa na:
• **Kuchoma taka wazi** - chanzo kikubwa cha uchafuzi
• **Madampo makubwa** - hutoa methane na gesi nyingine
• **Viwanda vya kemikali** - moshi na gesi kutoka kwa uzalishaji

**Kuchoma taka - hatari kubwa:**
Kuchoma plastiki, mpira, au e-waste hutoa:
• **Dioxins na Furans** - kemikali za hatari zinazosababisha saratani
• **Monoxide ya Kaboni** - gesi inayosababisha kifo haraka
• **Metali nzito** - risasi, zebaki ambazo zinaingia kwenye mapafu

**Athari za kiafya:**
• Matatizo ya kupumua (asthma, bronchitis)
• Maumivu ya kichwa na macho
• Saratani ya mapafu kwa muda mrefu
• Watoto wanaathirika zaidi kuliko watu wazima

**Madampo na tabianchi:**
• Madampo hutoa **methane** - gesi ya chafu yenye nguvu mara 25 zaidi ya CO2
• Compost inapunguza methane kwa kuoza taka kwa njia ya asili
• Recycling inapunguza haja ya viwanda kuzalisha bidhaa mpya - inapunguza uchafuzi

✅ Kamwe usichome taka - hata nyanjani au msituni
✅ Ripoti wachomaji wa taka waziwazi kupitia TakaSmart""",

'en': """## 💨 Air Pollution

**How waste pollutes air:**
Air pollution from waste is mainly caused by:
• **Open burning of waste** - a major source of air pollution
• **Large landfills** - release methane and other gases
• **Chemical factories** - smoke and gases from production

**Burning waste - a serious danger:**
Burning plastic, rubber, or e-waste releases:
• **Dioxins and Furans** - dangerous chemicals that cause cancer
• **Carbon Monoxide** - gas that can cause rapid death
• **Heavy metals** - lead, mercury that enter the lungs

**Health effects:**
• Breathing difficulties (asthma, bronchitis)
• Headaches and eye irritation
• Long-term lung cancer risk
• Children are more affected than adults

**Landfills and climate:**
• Landfills release **methane** - a greenhouse gas 25x more powerful than CO2
• Composting reduces methane by decomposing waste naturally
• Recycling reduces the need for factories to produce new goods - reduces pollution

✅ Never burn waste - even in fields or forests
✅ Report open burners of waste through TakaSmart""",

'fr': """## 💨 Pollution de l'Air

**Comment les dechets polluent l'air :**
La pollution de l'air par les dechets est principalement causee par :
• **Le brulage a ciel ouvert** - source majeure de pollution
• **Les grandes decharges** - liberent du methane et d'autres gaz
• **Les usines chimiques** - fumee et gaz de production

**Bruler des dechets - un danger grave :**
Bruler du plastique, du caoutchouc ou des dechets electroniques libere :
• **Dioxines et Furannes** - produits chimiques dangereux qui causent le cancer
• **Monoxyde de Carbone** - gaz qui peut causer la mort rapidement
• **Metaux lourds** - plomb, mercure qui penetrent dans les poumons

**Effets sur la sante :**
• Difficultés respiratoires (asthme, bronchite)
• Maux de tete et irritation des yeux
• Risque de cancer du poumon a long terme
• Les enfants sont plus touches que les adultes

✅ Ne jamais bruler de dechets - meme dans les champs ou les forets
✅ Signaler les bruleurs de dechets a ciel ouvert via TakaSmart"""
}

KB['climate'] = {
'sw': """## 🌡️ Mabadiliko ya Tabianchi na Taka

**Uhusiano wa taka na tabianchi:**
Usimamizi mbaya wa taka ni mchango mkubwa kwa mabadiliko ya tabianchi.

**Jinsi taka zinavyochangia:**
• **Madampo** - hutoa methane (CH4), gesi ya chafu yenye nguvu mara 25 zaidi ya CO2
• **Kuchoma taka** - hutoa CO2, dioxins, na gesi nyingine za chafu
• **Uzalishaji wa bidhaa** - kuzalisha plastiki mpya, chuma, karatasi kunahitaji nishati nyingi
• **Usafirishaji wa taka** - malori ya taka hutoa moshi wa diesel

**Nambari muhimu:**
• Sekta ya taka inachangia **5% ya uzalishaji wa gesi za chafu duniani**
• Madampo yanazalisha gesi ya methane inayochangia **11% ya uzalishaji wa methane duniani**
• Recycling karatasi inapunguza CO2 kwa tani 1 kwa kila tani 1 ya karatasi

**Jinsi TakaSmart inavyosaidia:**
✅ Recycling - inapunguza haja ya kuzalisha bidhaa mpya
✅ Compost - inapunguza methane kutoka kwa taka za kikolojia
✅ Ripoti ya uchafu - inasaidia kusafisha madampo haramu
✅ Kuunganisha wananunua - inahakikisha taka nyingi zinaenda kwa recycling

**Unachoweza kufanya wewe:**
• Punguza manunuzi ya vitu vya plastiki ya kutupa mara moja
• Tenganisha taka nyumbani kwa aina zao
• Tengeneza compost kwa taka za chakula
• Nunua bidhaa zilizofanywa kwa nyenzo ziliyorecyclewa""",

'en': """## 🌡️ Climate Change and Waste

**The link between waste and climate:**
Poor waste management is a major contributor to climate change.

**How waste contributes:**
• **Landfills** - release methane (CH4), a greenhouse gas 25x more powerful than CO2
• **Burning waste** - releases CO2, dioxins, and other greenhouse gases
• **Manufacturing new goods** - producing new plastic, metal, paper requires huge energy
• **Waste transportation** - collection trucks emit diesel fumes

**Key numbers:**
• The waste sector contributes **5% of global greenhouse gas emissions**
• Landfills produce methane accounting for **11% of global methane emissions**
• Recycling paper reduces CO2 by 1 tonne for every tonne of paper recycled

**How TakaSmart helps:**
✅ Recycling - reduces need to manufacture new goods
✅ Composting - reduces methane from organic waste
✅ Waste reporting - helps clear illegal dumpsites
✅ Connecting buyers - ensures more waste goes to recycling

**What you can do:**
• Reduce purchases of single-use plastic items
• Separate waste at home by type
• Compost food waste
• Buy products made from recycled materials""",

'fr': """## 🌡️ Changement Climatique et Dechets

**Le lien entre les dechets et le climat :**
La mauvaise gestion des dechets est un contributeur majeur au changement climatique.

**Comment les dechets contribuent :**
• **Decharges** - liberent du methane (CH4), un gaz a effet de serre 25x plus puissant que le CO2
• **Brulage de dechets** - libere du CO2, dioxines et autres gaz a effet de serre
• **Fabrication de nouveaux biens** - produire nouveau plastique, metal, papier necessite beaucoup d'energie
• **Transport des dechets** - les camions de collecte emettent des fumees diesel

**Chiffres cles :**
• Le secteur des dechets contribue a **5% des emissions mondiales de gaz a effet de serre**
• Les decharges produisent du methane representant **11% des emissions mondiales de methane**

**Comment TakaSmart aide :**
✅ Recyclage - reduit le besoin de fabriquer de nouveaux biens
✅ Compostage - reduit le methane des dechets organiques
✅ Signalement des dechets - aide a nettoyer les decharges illegales
✅ Mise en relation avec les acheteurs - assure que plus de dechets vont au recyclage"""
}

KB['health'] = {
'sw': """## 🏥 Athari za Taka kwa Afya

**Magonjwa yanayosababishwa na usimamizi mbaya wa taka:**

**1. Magonjwa ya maji yaliyochafuliwa:**
• **Kipindupindu (Cholera)** - inasababishwa na Vibrio cholerae kwenye maji machafu
• **Kuhara** - na magonjwa ya utumbo mwingine
• **Typhoid** - homa kali inayosababishwa na Salmonella kwenye maji machafu
• **Hepatitis A** - ugonjwa wa ini unaosambaa kwa maji machafu

**2. Magonjwa ya viumbe vya taka (vectors):**
• **Malaria** - mbu wanazaliana kwenye maji yaliyosimama kwenye taka
• **Dengue na Zika** - mbu wengine wanaozaliana kwenye maji yaliyosimama
• **Tauni (Plague)** - panya wanaoishi kwenye madampo wanaweza kubeba ugonjwa

**3. Athari za kemikali:**
• **Sumu ya risasi** - kutoka kwa rangi za zamani, betri, moshi wa e-waste
• **Sumu ya zebaki** - kutoka kwa thermometers, betri za zamani, e-waste
• **Saratani** - kutoka kwa dioxins za kuchoma plastiki, asbestos

**4. Majeraha ya kimwili:**
• Kioo kilichovunjika, chuma chenye kutu - majeraha ya kuchanjua

**Makundi yanayoathirika zaidi:**
• **Watoto** - wanaocheza karibu na taka, wanaoweza kumeza vitu vidogo
• **Wazee** - mfumo wa kinga dhaifu
• **Wajawazito** - kemikali zinaweza kuathiri mtoto tumboni

✅ Ripoti madampo karibu na makazi, shule, na hospitali kupitia TakaSmart""",

'en': """## 🏥 Health Effects of Waste

**Diseases caused by poor waste management:**

**1. Waterborne diseases:**
• **Cholera** - caused by Vibrio cholerae in contaminated water
• **Diarrhea** - and other intestinal diseases
• **Typhoid** - serious fever caused by Salmonella in contaminated water
• **Hepatitis A** - liver disease spread through contaminated water

**2. Vector-borne diseases:**
• **Malaria** - mosquitoes breed in stagnant water collecting in waste
• **Dengue and Zika** - other mosquitoes breed in stagnant water
• **Plague** - rats living in dumpsites can carry disease

**3. Chemical effects:**
• **Lead poisoning** - from old paint, batteries, e-waste smoke
• **Mercury poisoning** - from thermometers, old batteries, e-waste
• **Cancer** - from dioxins produced by burning plastic, asbestos

**4. Physical injuries:**
• Broken glass, rusty metal - cut and puncture injuries

**Most vulnerable groups:**
• **Children** - play near waste, may swallow small objects
• **Elderly** - weakened immune system
• **Pregnant women** - chemicals can affect the unborn child

✅ Report dumpsites near homes, schools, and hospitals through TakaSmart""",

'fr': """## 🏥 Effets des Dechets sur la Sante

**Maladies causees par une mauvaise gestion des dechets :**

**1. Maladies hydriques :**
• **Cholera** - cause par Vibrio cholerae dans l'eau contaminee
• **Diarrhee** - et autres maladies intestinales
• **Typhoide** - fievre grave causee par Salmonella dans l'eau contaminee
• **Hepatite A** - maladie du foie propagee par l'eau contaminee

**2. Maladies transmises par des vecteurs :**
• **Paludisme** - les moustiques se reproduisent dans les eaux stagnantes
• **Dengue et Zika** - autres moustiques dans les eaux stagnantes
• **Peste** - les rats vivant dans les decharges peuvent porter la maladie

**3. Effets chimiques :**
• **Intoxication au plomb** - vieille peinture, batteries, fumee electronique
• **Intoxication au mercure** - thermometres, vieilles batteries
• **Cancer** - dioxines produites par le brulage du plastique, amiante

**Groupes les plus vulnerables :**
• **Enfants** - jouent pres des dechets, peuvent avaler de petits objets
• **Personnes agees** - systeme immunitaire affaibli
• **Femmes enceintes** - les produits chimiques peuvent affecter l'enfant

✅ Signalez les decharges pres des habitations, ecoles et hopitaux via TakaSmart"""
}

KB['wildlife'] = {
'sw': """## 🦁 Wanyamapori na Plastiki

**Plastiki na wanyama - tatizo kubwa:**

**Baharini:**
• Tani milioni 8 za plastiki huingia baharini kila mwaka
• **Kasa wa baharini** (sea turtles) wanakula mifuko ya plastiki wakifikiri ni jellyfish
• **Nyangumi na dolphins** wanapatikana wamekufa na tumbo lililojaa plastiki
• **Ndege wa pwani** (seabirds) wanalisha watoto wao plastiki wakifikiri ni chakula
• **Samaki** wanakula microplastics - halafu sisi tunakula samaki hao

**Nchi kavu:**
• **Ng'ombe, mbuzi, kondoo** wanakula mifuko ya plastiki - inaziba njia ya utumbo na wanakufa
• **Ndege** wanakwama kwenye pete za plastiki za makopo ya bia
• **Wanyama wadogo** wanakwama kwenye vyombo vya plastiki vilivyoachwa wazi

**Takwimu za kutisha:**
• 90% ya ndege wa baharini wamekula plastiki
• 50% ya kasa wa baharini wamekula plastiki
• Ifikapo 2050, plastiki itakuwa zaidi ya samaki baharini kwa uzito

**Unachoweza kufanya:**
✅ Usitupe plastiki popote - hata mbali na bahari (mvua hupeleka plastiki baharini)
✅ Tumia mifuko ya kitambaa au kioo badala ya plastiki
✅ Anza kutumia bidhaa bila plastiki inapowezekana
✅ Ripoti madampo yanayozaliana karibu na vyanzo vya maji""",

'en': """## 🦁 Wildlife and Plastic

**Plastic and animals - a major problem:**

**In the ocean:**
• 8 million tonnes of plastic enter the ocean every year
• **Sea turtles** eat plastic bags thinking they are jellyfish
• **Whales and dolphins** are found dead with stomachs full of plastic
• **Seabirds** feed their chicks plastic thinking it is food
• **Fish** eat microplastics - then we eat those fish

**On land:**
• **Cattle, goats, sheep** eat plastic bags - they clog the digestive system and animals die
• **Birds** get trapped in plastic rings from beer cans
• **Small animals** get trapped in open plastic containers

**Shocking statistics:**
• 90% of seabirds have eaten plastic
• 50% of sea turtles have eaten plastic
• By 2050, there will be more plastic than fish in the ocean by weight

**What you can do:**
✅ Never litter plastic anywhere - even far from the sea (rain carries plastic to the ocean)
✅ Use cloth bags or glass containers instead of plastic
✅ Start choosing products without plastic where possible
✅ Report dumpsites near water sources""",

'fr': """## 🦁 Faune Sauvage et Plastique

**Le plastique et les animaux - un probleme majeur :**

**Dans l'ocean :**
• 8 millions de tonnes de plastique entrent dans l'ocean chaque annee
• **Les tortues marines** mangent des sacs plastique en les prenant pour des meduses
• **Les baleines et dauphins** sont trouves morts avec des estomacs pleins de plastique
• **Les oiseaux marins** nourrissent leurs petits avec du plastique
• **Les poissons** mangent des microplastiques - puis nous mangeons ces poissons

**Sur terre :**
• **Les bovins, chevres, moutons** mangent des sacs plastique - bouchent le systeme digestif et les animaux meurent
• **Les oiseaux** se coincent dans les anneaux plastique des canettes de biere
• **Les petits animaux** se coincent dans des contenants plastique ouverts

**Statistiques alarmantes :**
• 90% des oiseaux marins ont mange du plastique
• 50% des tortues marines ont mange du plastique
• D'ici 2050, il y aura plus de plastique que de poissons dans l'ocean en poids

**Ce que vous pouvez faire :**
✅ Ne jamais jeter de plastique nulle part
✅ Utiliser des sacs en tissu ou des contenants en verre
✅ Choisir des produits sans plastique quand c'est possible
✅ Signaler les decharges pres des sources d'eau"""
}

KB['soil'] = {
'sw': """## 🌱 Uchafuzi wa Udongo

**Jinsi taka zinavyoharibu udongo:**
Udongo ni msingi wa uzalishaji wa chakula. Taka zinazotupwa ovyo zinaharibu udongo kwa njia nyingi:

**Kemikali zinazoingia ardhini:**
• Plastiki inagawanyika polepole na kemikali zake (phthalates, BPA) zinaingia udongoni
• Betri zinaachilia asidi na metali nzito (risasi, cadmium) kwenye udongo
• Dawa za wadudu na kemikali nyingine zinapotumiwa kupita kiasi

**Athari kwa kilimo:**
• Udongo ulioathirika na kemikali unazalisha mazao machache
• Mimea inachukua kemikali kutoka udongoni - mazao yanakuwa si salama kula
• Vijidudu vya udongo vinavyofanya kazi nzuri ya kutengeneza udongo vizuri vinakufa

**Athari za muda mrefu:**
• Kemikali za udongo zinaingia kwenye maji ya chini ya ardhi (groundwater)
• Inaweza kuchukua **miaka 50-100** kusafisha udongo ulioathirika sana

**Jinsi ya kulinda udongo:**
1. Tenganisha taka - usitupe pamoja na ardhi inayolimwa
2. Tumia compost badala ya mbolea za kemikali
3. Epuka kutumia mifuko ya plastiki kwenye bustani - vipande vidogo hubaki udongoni
4. Ripoti madampo haramu karibu na mashamba kupitia TakaSmart
5. Osha vyombo vya plastiki kabla ya kutupa - kemikali za chakula hazitiririke ardhini""",

'en': """## 🌱 Soil Pollution

**How waste harms soil:**
Soil is the foundation of food production. Improperly disposed waste harms soil in multiple ways:

**Chemicals entering the ground:**
• Plastic slowly breaks down and its chemicals (phthalates, BPA) seep into soil
• Batteries leach acid and heavy metals (lead, cadmium) into soil
• Pesticides and other chemicals when used excessively

**Effects on farming:**
• Chemically damaged soil produces fewer crops
• Plants absorb chemicals from soil - crops become unsafe to eat
• Soil microorganisms that make soil fertile die off

**Long-term effects:**
• Soil chemicals enter groundwater
• It can take **50-100 years** to clean heavily contaminated soil

**How to protect soil:**
1. Separate waste - don't dump near agricultural land
2. Use compost instead of chemical fertilisers
3. Avoid using plastic bags in gardens - small pieces stay in soil
4. Report illegal dumpsites near farmland through TakaSmart
5. Rinse plastic containers before disposal - food chemicals don't leach into ground""",

'fr': """## 🌱 Pollution du Sol

**Comment les dechets endommagent le sol :**
Le sol est la base de la production alimentaire. Les dechets mal jetes endommagent le sol de multiples facons :

**Produits chimiques penetrant dans le sol :**
• Le plastique se degrade lentement et ses produits chimiques (phtalates, BPA) s'infiltrent dans le sol
• Les batteries libèrent de l'acide et des metaux lourds (plomb, cadmium) dans le sol
• Les pesticides et autres produits chimiques utilises en exces

**Effets sur l'agriculture :**
• Un sol chimiquement endommage produit moins de cultures
• Les plantes absorbent les produits chimiques du sol - les cultures deviennent dangereuses a manger
• Les micro-organismes du sol qui le fertilisent meurent

**Effets a long terme :**
• Les produits chimiques du sol penetrent dans les eaux souterraines
• Il peut falloir **50 a 100 ans** pour nettoyer un sol tres contamine

**Comment proteger le sol :**
1. Separer les dechets - ne pas jeter pres des terres agricoles
2. Utiliser le compost plutot que les engrais chimiques
3. Eviter les sacs plastique dans les jardins
4. Signaler les decharges illegales pres des terres agricoles via TakaSmart"""
}

KB['ocean'] = {
'sw': """## 🌊 Plastiki Baharini na Microplastics

**Hali ya sasa:**
Bahari ina zaidi ya **tani milioni 150 za plastiki** sasa hivi, na kila mwaka tani milioni 8 zinaongezeka.

**Great Pacific Garbage Patch:**
Kuna eneo kubwa la plastiki Bahari ya Pasifiki lenye ukubwa wa **mara 2 ya Texas** linaloundwa na mikondo ya maji iliyokusanya plastiki kutoka mataifa mengi.

**Microplastics:**
Plastiki inagawanyika lakini **haiozi kamwe** - inagawanyika kuwa vipande vidogo sana vinavyoitwa microplastics (chini ya mm 5):
• Zinapatikana kila mahali - bahari, mito, hewa, udongo
• Zinapatikana kwenye damu ya binadamu
• Zinapatikana kwenye maziwa ya mama
• Zinapatikana kwenye wanyama wote wa baharini

**Athari:**
• Samaki wanaokula microplastics wanapata matatizo ya ukuaji na uzazi
• Binadamu wanaokula samaki hao pia wanaathirika
• Kemikali za microplastics (BPA, phthalates) zinavuruga mfumo wa homoni

**Suluhisho:**
✅ Acha kutumia plastiki ya kutupa mara moja
✅ Usitupe taka popote isipokuwa kwenye pipa
✅ Tumia vichungi vya maji badala ya plastiki za maji
✅ Nunua nguo za asili (pamba, sufu) - nguo za synthetic zinatoa microplastics wakati wa kufuliwa""",
'en': """## 🌊 Ocean Plastic and Microplastics

**Current situation:**
The ocean contains over **150 million tonnes of plastic** right now, and 8 million more tonnes are added every year.

**The Great Pacific Garbage Patch:**
There is a massive area of plastic in the Pacific Ocean roughly **twice the size of Texas**, formed by ocean currents gathering plastic from many countries.

**Microplastics:**
Plastic breaks down but **never fully decomposes** - it breaks into tiny pieces called microplastics (smaller than 5mm):
• Found everywhere - oceans, rivers, air, soil
• Found in human blood
• Found in breast milk
• Found in all marine animals

**Effects:**
• Fish that eat microplastics develop growth and reproduction problems
• Humans who eat those fish are also affected
• Microplastic chemicals (BPA, phthalates) disrupt the hormonal system

**Solutions:**
✅ Stop using single-use plastic
✅ Never litter - only use waste bins
✅ Use water filters instead of plastic water bottles
✅ Buy natural fibre clothes (cotton, wool) - synthetic clothes shed microplastics when washed""",
'fr': """## 🌊 Plastique dans l'Ocean et Microplastiques

**Situation actuelle :**
L'ocean contient plus de **150 millions de tonnes de plastique** actuellement, et 8 millions de tonnes s'ajoutent chaque annee.

**Le Grand Vortex de Dechets du Pacifique :**
Il existe une immense zone de plastique dans l'ocean Pacifique d'environ **deux fois la taille du Texas**.

**Microplastiques :**
Le plastique se degrade mais **ne se decompose jamais vraiment** - il se fragmente en minuscules morceaux appeles microplastiques :
• Trouves partout - oceans, rivieres, air, sol
• Trouves dans le sang humain
• Trouves dans le lait maternel
• Trouves dans tous les animaux marins

**Effets :**
• Les poissons qui mangent des microplastiques developpent des problemes de croissance
• Les humains qui mangent ces poissons sont aussi affectes
• Les produits chimiques des microplastiques perturbent le systeme hormonal

**Solutions :**
✅ Arreter d'utiliser le plastique a usage unique
✅ Ne jamais jeter de dechets - utiliser les poubelles"""
}

KB['landfill'] = {
'sw': """## 🗑️ Madampo na Tatizo Lake

**Madampo ni nini?**
Madampo (landfill) ni maeneo yanayotumiwa kutupa taka. Ingawa yanaboresha ulinzi wa mazingira ikilinganishwa na kutupa ovyo, yana matatizo makubwa ya kimazingira.

**Matatizo ya madampo:**

**1. Gesi za chafu:**
• Taka za kikolojia zinaoza bila hewa (anaerobic decomposition) na kutoa **methane (CH4)**
• Methane ni gesi ya chafu yenye nguvu mara 25 zaidi ya CO2
• Madampo duniani yanachangia ~11% ya uzalishaji wa methane duniani

**2. Leachate (maji machafu ya madampo):**
• Mvua inapoingia kwenye madampo, inachukua kemikali kutoka kwa taka
• Kioevu hiki cha sumu (leachate) kinaweza kuingia kwenye maji ya chini ya ardhi
• Kinaweza kuchafua visima na mifereji ya maji

**3. Nafasi:**
• Madampo yanachukua ardhi nyingi
• Miji mingi ya Afrika inakabiliwa na upunguzi wa maeneo ya madampo

**Suluhisho:**
• **Reduce** - nunua kidogo, hasa plastiki ya kutupa mara moja
• **Reuse** - tumia tena vitu unavyoweza
• **Recycle** - taka nyingi zinaweza kugeuzwa bidhaa mpya
• **Compost** - taka za chakula zinaweza kuwa mbolea

💡 Nchi zilizoendelea zinalenga kupunguza taka kwenye madampo kwa zaidi ya 80% kupitia recycling na compost""",
'en': """## 🗑️ Landfills and Their Problems

**What is a landfill?**
Landfills are areas used for waste disposal. While better than open dumping, they have serious environmental problems.

**Landfill problems:**

**1. Greenhouse gases:**
• Organic waste decomposes without air (anaerobic decomposition) releasing **methane (CH4)**
• Methane is a greenhouse gas 25x more powerful than CO2
• Global landfills contribute ~11% of global methane emissions

**2. Leachate (landfill liquid):**
• Rain entering landfills picks up chemicals from waste
• This toxic liquid (leachate) can seep into groundwater
• Can contaminate wells and water pipes

**3. Space:**
• Landfills consume vast areas of land
• Many African cities face shortages of landfill space

**Solutions:**
• **Reduce** - buy less, especially single-use plastic
• **Reuse** - reuse items where possible
• **Recycle** - much waste can be turned into new products
• **Compost** - food waste can become fertiliser

💡 Developed nations aim to reduce landfill waste by over 80% through recycling and composting""",
'fr': """## 🗑️ Decharges et Leurs Problemes

**Qu'est-ce qu'une decharge ?**
Les decharges sont des zones utilisees pour eliminer les dechets. Bien que meilleures que le deversement sauvage, elles ont de graves problemes environnementaux.

**Problemes des decharges :**

**1. Gaz a effet de serre :**
• Les dechets organiques se decomposent sans air et liberent du **methane (CH4)**
• Le methane est un gaz a effet de serre 25x plus puissant que le CO2
• Les decharges mondiales contribuent a ~11% des emissions mondiales de methane

**2. Lixiviat (liquide de decharge) :**
• La pluie penetrant dans les decharges absorbe les produits chimiques des dechets
• Ce liquide toxique peut s'infiltrer dans les eaux souterraines

**3. Espace :**
• Les decharges consomment de vastes zones de terrain
• De nombreuses villes africaines manquent d'espace pour les decharges

**Solutions :**
• **Reduire** - acheter moins, surtout le plastique a usage unique
• **Reutiliser** - reutiliser les articles si possible
• **Recycler** - beaucoup de dechets peuvent devenir de nouveaux produits
• **Composter** - les dechets alimentaires peuvent devenir de l'engrais"""
}

KB['3rs'] = {
'sw': """## ♻️ 3R: Reduce, Reuse, Recycle

Kanuni ya **3R** ni msingi wa usimamizi bora wa taka. Mpangilio ni muhimu - **Reduce** iko kwanza kwa sababu ndiyo yenye athari kubwa zaidi.

## 1. Reduce (Punguza)
**Bora zaidi - zuia taka kabla hazijaundwa**
• Nunua bidhaa zinazodumu badala ya za kutupa mara moja
• Epuka vifungashio vya ziada - chagua bidhaa zenye ufungashaji mdogo
• Nunua kiasi unachohitaji tu - punguza upotevu wa chakula
• Fikiria kabla ya kununua - je, unahitaji kweli kweli?
• Chagua bidhaa zinazotengenezwa kwa nyenzo za asili

## 2. Reuse (Tumia Tena)
**Pili bora - tumia tena kabla ya kutupa**
• Tumia mifuko ya kitambaa badala ya plastiki kila wakati
• Tumia chupa za kioo au stainless steel kwa maji
• Rekebisha vitu vilivyovunjika badala ya kununua vipya
• Toa au uze vitu ambavyo havifai kwako tena
• Tumia kontena la chakula badala ya plastiki mpya kila wakati

## 3. Recycle (Recycle)
**Tatu - recycle taka ambazo haziwezi kupunguzwa wala kutumika tena**
• Tenganisha taka kwa aina
• Safisha kabla ya kupeleka
• Peleka kwa mnunuzi au kituo cha ukusanyaji

**Kanuni za ziada:**
• **Rot (Compost)** - taka za chakula kuwa mbolea
• **Refuse** - kataa kupokea vitu visivyo na haja (mifuko ya plastiki, vijisanduku vya plastiki)
• **Repair** - rekebisha badala ya kutupa

💡 Ikiwa kila mtu angetekeleza 3R, taka duniani zingeweza kupunguzwa kwa **70%**""",
'en': """## ♻️ The 3Rs: Reduce, Reuse, Recycle

The **3Rs principle** is the foundation of good waste management. The order matters - **Reduce** comes first because it has the biggest impact.

## 1. Reduce
**Best option - prevent waste before it is created**
• Buy durable products instead of single-use ones
• Avoid excess packaging - choose products with minimal packaging
• Buy only what you need - reduce food waste
• Think before buying - do you really need it?
• Choose products made from natural materials

## 2. Reuse
**Second best - use again before discarding**
• Use cloth bags instead of plastic every time
• Use glass or stainless steel bottles for water
• Repair broken items instead of buying new ones
• Donate or sell items you no longer need
• Use food containers instead of new plastic every time

## 3. Recycle
**Third - recycle waste that cannot be reduced or reused**
• Separate waste by type
• Clean before taking to a facility
• Take to a buyer or collection point

**Additional principles:**
• **Rot (Compost)** - food waste into fertiliser
• **Refuse** - refuse to receive unnecessary items (plastic bags, plastic containers)
• **Repair** - repair instead of discarding

💡 If everyone practised the 3Rs, global waste could be reduced by **70%**""",
'fr': """## ♻️ Les 3R : Reduire, Reutiliser, Recycler

Le **principe des 3R** est la base d'une bonne gestion des dechets. L'ordre est important - **Reduire** vient en premier car c'est l'option a plus grand impact.

## 1. Reduire
**Meilleure option - prevenir les dechets avant qu'ils ne soient crees**
• Acheter des produits durables plutot que jetables
• Eviter les emballages excessifs
• N'acheter que ce dont vous avez besoin - reduire le gaspillage alimentaire
• Reflechir avant d'acheter - en avez-vous vraiment besoin ?

## 2. Reutiliser
**Deuxieme meilleure option - reutiliser avant de jeter**
• Utiliser des sacs en tissu a chaque fois
• Utiliser des bouteilles en verre ou acier inoxydable
• Reparer les objets casses plutot qu'en acheter de nouveaux
• Donner ou vendre les articles dont vous n'avez plus besoin

## 3. Recycler
**Troisieme - recycler les dechets qui ne peuvent etre ni reduits ni reutilises**
• Separer les dechets par type
• Nettoyer avant d'apporter
• Apporter a un acheteur ou point de collecte

💡 Si tout le monde pratiquait les 3R, les dechets mondiaux pourraient etre reduits de **70%**"""
}

KB['zero_waste'] = {
'sw': """## 🌿 Maisha ya Zero Waste

**Zero Waste ni nini?**
Zero waste ni mtazamo wa maisha unaolenga kupunguza taka unazozalisha hadi karibu na sifuri iwezekanavyo. Si lazima iwe kamili - hata kupunguza kwa **50-80%** ni mafanikio makubwa.

**Kanuni ya 5R za Zero Waste:**
1. **Refuse** - Kataa vitu usivyohitaji (straw za plastiki, mifuko ya plastiki)
2. **Reduce** - Punguza kile unachonunua na kutumia
3. **Reuse** - Tumia tena - chupa, mifuko, vyombo
4. **Recycle** - Recycle taka ambazo haziwezi kupunguzwa au kutumika tena
5. **Rot** - Tengeneza compost kwa taka za chakula

**Mabadiliko rahisi ya kuanza:**
• Nunua mfuko wa kitambaa badala ya kutumia plastiki
• Tumia chupa ya maji inayoweza kujazwa tena
• Nunua chakula zaidi kwenye masoko badala ya vifungashio vya plastiki
• Tumia dawa ya meno katika kopo badala ya chupa ya plastiki
• Nunua mkaa wa msitu (bamboo toothbrush) badala ya plastiki
• Tumia sabuni ya mwili katika ubao badala ya chupa za plastiki

**Nyumbani:**
• Weka mikebe mitatu: kurecycle, compost, taka nyingine
• Pima taka unazozalisha kila wiki - utashangaa kiasi kitakachopungua

💡 Zero waste si perfectionism - ni maendeleo ya polepole. Kila hatua ndogo inasaidia!""",
'en': """## 🌿 Zero Waste Lifestyle

**What is Zero Waste?**
Zero waste is a lifestyle philosophy that aims to reduce the waste you generate to nearly nothing. It does not have to be perfect - even reducing by **50-80%** is a great achievement.

**The 5Rs of Zero Waste:**
1. **Refuse** - Refuse what you do not need (plastic straws, plastic bags)
2. **Reduce** - Reduce what you buy and use
3. **Reuse** - Reuse - bottles, bags, containers
4. **Recycle** - Recycle waste that cannot be reduced or reused
5. **Rot** - Compost food waste

**Easy changes to start:**
• Buy a cloth bag instead of using plastic
• Use a refillable water bottle
• Buy more food at markets instead of plastic packaging
• Use toothpaste in a jar instead of plastic tube
• Use a bamboo toothbrush instead of plastic
• Use bar soap instead of plastic bottles

**At home:**
• Have three bins: recycling, compost, other waste
• Weigh the waste you generate each week - you will be surprised how much decreases

💡 Zero waste is not perfectionism - it is gradual progress. Every small step helps!""",
'fr': """## 🌿 Mode de Vie Zero Dechet

**Qu'est-ce que le Zero Dechet ?**
Le zero dechet est une philosophie de vie visant a reduire les dechets generes a presque rien. Ce n'est pas obligatoirement parfait - meme une reduction de **50-80%** est un grand succes.

**Les 5R du Zero Dechet :**
1. **Refuser** - Refuser ce dont vous n'avez pas besoin (pailles plastique, sacs plastique)
2. **Reduire** - Reduire ce que vous achetez et utilisez
3. **Reutiliser** - Reutiliser - bouteilles, sacs, contenants
4. **Recycler** - Recycler les dechets qui ne peuvent etre reduits ou reutilises
5. **Composter** - Composter les dechets alimentaires

**Changements faciles pour commencer :**
• Acheter un sac en tissu
• Utiliser une bouteille d'eau rechargeable
• Acheter plus d'aliments sur les marches plutot qu'en emballage plastique
• Utiliser un cure-dent en bambou plutot qu'en plastique
• Utiliser du savon en pain plutot que des bouteilles plastique

💡 Le zero dechet n'est pas du perfectionnisme - c'est un progres graduel. Chaque petit pas aide !"""
}

KB['government'] = {
'sw': """## 🏛️ Sheria na Sera za Mazingira Tanzania

**Sheria Kuu:**

**1. Environmental Management Act (EMA) 2004**
• Sheria kuu ya usimamizi wa mazingira Tanzania
• Inazuia uchafuzi wa hewa, maji, na udongo
• Inaweka adhabu kwa ukiukwaji wa mazingira

**2. Solid Waste Management Regulations 2009**
• Inasimamia ukusanyaji, usafirishaji, na utupaji wa taka ngumu
• Inaweka viwango vya namna ya kushughulikia taka
• Halmashauri zinawajibika kwa ukusanyaji wa taka mijini

**3. Local Government Act**
• Halmashauri za miji (Municipal/District Councils) zinasimamia usafi wa miji
• Zina mamlaka ya kukusanya taka na kusimamia madampo

**Mamlaka zinazohusika:**
• **NEMC** (National Environment Management Council) - chombo kikuu cha mazingira Tanzania
• **Halmashauri za Manispaa** - ukusanyaji wa taka mijini
• **Wizara ya Nchi, Ofisi ya Makamu wa Rais (Mazingira)** - sera za mazingira
• **OSHA** - usalama wa kazi ikiwa ni pamoja na ushughulikiaji wa taka hatari

**Adhabu:**
• Kutupa taka ovyo - faini na/au kifungo
• Kuchoma taka - faini kubwa
• Kuchafua maji - adhabu kali

**Ripoti ukiukwaji:**
Tumia sehemu ya Ripoti kwenye TakaSmart au piga simu:
• NEMC: +255 22 245 1075
• Halmashauri yako ya eneo""",
'en': """## 🏛️ Environmental Laws and Policy in Tanzania

**Key Laws:**

**1. Environmental Management Act (EMA) 2004**
• The main environmental management law in Tanzania
• Prohibits pollution of air, water, and soil
• Sets penalties for environmental violations

**2. Solid Waste Management Regulations 2009**
• Governs the collection, transportation, and disposal of solid waste
• Sets standards for waste handling
• Municipal councils are responsible for urban waste collection

**3. Local Government Act**
• Municipal and District Councils manage urban cleanliness
• Have authority to collect waste and manage dumpsites

**Responsible authorities:**
• **NEMC** (National Environment Management Council) - Tanzania's main environmental body
• **Municipal Councils** - urban waste collection
• **Vice President's Office (Environment)** - environmental policy
• **OSHA** - workplace safety including hazardous waste handling

**Penalties:**
• Littering - fines and/or imprisonment
• Burning waste - heavy fines
• Water pollution - severe penalties

**Report violations:**
Use the Report section on TakaSmart or call:
• NEMC: +255 22 245 1075
• Your local Municipal Council""",
'fr': """## 🏛️ Lois et Politiques Environnementales en Tanzanie

**Lois principales :**

**1. Loi sur la gestion de l'environnement (EMA) 2004**
• La principale loi de gestion environnementale en Tanzanie
• Interdit la pollution de l'air, de l'eau et du sol
• Etablit des penalites pour les violations environnementales

**2. Reglementation sur la gestion des dechets solides 2009**
• Regit la collecte, le transport et l'elimination des dechets solides
• Fixe des normes de traitement des dechets
• Les conseils municipaux sont responsables de la collecte urbaine

**Autorites competentes :**
• **NEMC** - Conseil national de gestion de l'environnement de Tanzanie
• **Conseils municipaux** - collecte urbaine des dechets
• **Bureau du Vice-President (Environnement)** - politique environnementale

**Penalites :**
• Jonchage - amendes et/ou emprisonnement
• Brulage de dechets - amendes importantes
• Pollution de l'eau - penalites severes

**Signaler les violations :**
Utilisez la section Signalement sur TakaSmart ou appelez le NEMC : +255 22 245 1075"""
}

KB['report'] = {
'sw': """## 📋 Jinsi ya Kutuma Ripoti ya Uchafu

**Hatua kwa hatua:**

1. **Bonyeza 'Ripoti'** kwenye menyu ya juu ya TakaSmart

2. **Fungua Camera:**
   • Bonyeza 'Fungua Camera'
   • Ruhusu browser kutumia camera yako (bonyeza Allow)
   • Elekeza camera kwenye eneo lenye uchafu
   • Bonyeza 'Piga Picha'

3. **Jaza maelezo:**
   • Andika maelezo ya uchafu (aina, kiasi, hali)
   • Weka mahali (GPS au bonyeza ramani)

4. **Chagua mamlaka:**
   • 🏛️ **Halmashauri** - uchafu wa barabara, maeneo ya umma
   • 🏥 **Idara ya Afya** - taka karibu na hospitali, shule, vyanzo vya maji
   • 🌿 **Wizara ya Mazingira** - uchafuzi wa kemikali, mito
   • 🚛 **Shirika la Taka** - ukusanyaji usiofanyika

5. **Tuma:**
   • Bonyeza 'Tuma Ripoti'
   • Mamlaka itapokea ripoti yako mara moja

**Vidokezo:**
💡 Piga picha wakati wa mchana - mwanga mzuri unasaidia
💡 Thibitisha mahali kwenye ramani kwa usahihi
💡 Maelezo mazuri yanasaidia mamlaka kuchukua hatua haraka""",
'en': """## 📋 How to Submit a Waste Report

**Step by step:**

1. **Tap 'Report'** in the top menu of TakaSmart

2. **Open Camera:**
   • Tap 'Open Camera'
   • Allow the browser to use your camera (tap Allow)
   • Point the camera at the waste area
   • Tap 'Take Photo'

3. **Fill in details:**
   • Write a description of the waste (type, amount, condition)
   • Set location (GPS or tap the map)

4. **Choose an authority:**
   • 🏛️ **Municipality** - road waste, public spaces
   • 🏥 **Health Dept** - waste near hospitals, schools, water sources
   • 🌿 **Environment Ministry** - chemical pollution, rivers
   • 🚛 **Waste Services** - missed collections

5. **Submit:**
   • Tap 'Submit Report'
   • The authority will receive your report immediately

**Tips:**
💡 Take photos during the day - good lighting helps
💡 Confirm the map location accurately
💡 Good descriptions help authorities take action faster""",
'fr': """## 📋 Comment Soumettre un Signalement

**Etape par etape :**

1. **Appuyez sur 'Signaler'** dans le menu superieur de TakaSmart

2. **Ouvrir la camera :**
   • Appuyez sur 'Ouvrir la camera'
   • Autorisez l'acces a la camera (appuyez sur Autoriser)
   • Pointez la camera vers la zone de dechets
   • Appuyez sur 'Prendre une photo'

3. **Remplir les details :**
   • Decrire les dechets (type, quantite, etat)
   • Definir l'emplacement (GPS ou cliquer sur la carte)

4. **Choisir une autorite :**
   • 🏛️ **Mairie** - dechets sur routes, espaces publics
   • 🏥 **Sante** - dechets pres d'hopitaux, ecoles, sources d'eau
   • 🌿 **Environnement** - pollution chimique, rivieres
   • 🚛 **Service des dechets** - collectes manquees

5. **Envoyer :**
   • Appuyez sur 'Envoyer'
   • L'autorite recevra votre signalement immediatement"""
}

KB['buyer'] = {
'sw': """## 🏪 Jinsi ya Kupata Mnunuzi wa Taka

**Hatua kwa hatua:**

1. **Bonyeza 'Wananunua'** kwenye menyu ya juu
2. **Chagua aina ya taka** unayotaka kuuza kutoka kwenye orodha
3. **Tafuta** kwa jina la biashara au eneo (mji, mtaa)
4. **Angalia ramani** - wananunua wenye GPS wanaonekana kwenye ramani ya bluu
5. **Bonyeza 'Wasiliana'** - utaitwa moja kwa moja

**Vidokezo vya kupata bei nzuri:**
💡 Wasiliana na **wananunuzi 2-3** na linganisha bei kabla ya kuuza
💡 **Safisha taka** kabla ya kupeleka - taka safi ina bei nzuri zaidi
💡 **Tenganisha vizuri** - aina tofauti zina bei tofauti
💡 **Kiasi kikubwa** - kadri unavyopeleka nyingi ndivyo unavyopata bei nzuri zaidi
💡 **Piga picha** ya taka na uzito kabla ya kwenda - unaweza kulinganisha na mnunuzi

**Bei za kawaida (takriban):**
• Plastiki PET: TSh 200-500/kg
• Aluminium: TSh 800-1,500/kg
• Shaba: TSh 2,000-4,000/kg
• Karatasi/Kadibodi: TSh 100-300/kg
• Chuma cha kawaida: TSh 100-200/kg

⚠️ Bei hizi ni mwongozo tu - zinabadilika kulingana na soko""",
'en': """## 🏪 How to Find a Waste Buyer

**Step by step:**

1. **Tap 'Buyers'** in the top menu
2. **Select the waste type** you want to sell from the list
3. **Search** by business name or location (city, area)
4. **Check the map** - GPS-enabled buyers appear on the blue map
5. **Tap 'Contact'** - you will be called directly

**Tips for getting a good price:**
💡 Contact **2-3 buyers** and compare prices before selling
💡 **Clean the waste** before taking it - clean waste gets better prices
💡 **Sort properly** - different types have different prices
💡 **Larger quantities** - the more you bring, the better price you get
💡 **Take photos** of the waste and weigh it before going - you can compare with the buyer

**Approximate prices:**
• PET Plastic: moderate value per kg
• Aluminium: high value per kg
• Copper: very high value per kg
• Paper/Cardboard: lower value per kg
• Regular steel: low value per kg

⚠️ These are guidelines only - prices vary with market conditions""",
'fr': """## 🏪 Comment Trouver un Acheteur de Dechets

**Etape par etape :**

1. **Appuyez sur 'Acheteurs'** dans le menu superieur
2. **Selectionnez le type de dechet** que vous voulez vendre
3. **Recherchez** par nom d'entreprise ou lieu
4. **Consultez la carte** - les acheteurs avec GPS apparaissent sur la carte bleue
5. **Appuyez sur 'Contacter'** - vous serez appele directement

**Conseils pour obtenir un bon prix :**
💡 Contactez **2-3 acheteurs** et comparez les prix avant de vendre
💡 **Nettoyez les dechets** avant d'apporter - les dechets propres ont un meilleur prix
💡 **Triez correctement** - les differents types ont des prix differents
💡 **Grandes quantites** - plus vous apportez, meilleur est le prix

⚠️ Ces prix sont indicatifs - ils varient selon le marche"""
}

KB['camera'] = {
'sw': """## 📷 Jinsi ya Kutumia Camera kwenye TakaSmart

**Camera inafanya kazi kwenye:**
• Sehemu ya **Ripoti** - kupiga picha ya eneo lenye uchafu
• Sehemu ya **Tambua Taka** - kutambua aina ya taka

**Hatua:**
1. Bonyeza **'Fungua Camera'**
2. Browser itaomba ruhusa - bonyeza **'Allow' / 'Ruhusu'**
3. Camera itafunguka na kuonyesha kinachoonekana kwenye skrini
4. Elekeza camera kwenye taka au eneo
5. Bonyeza **'Piga Picha'** kurekodi picha
6. Picha itaonekana kwenye ukurasa

**Tatizo: Camera haifunguki?**
• Angalia mipangilio ya browser: klikia 🔒 au ⓘ kwenye URL bar → Camera → Allow
• Tumia **localhost:5000 au HTTPS** - camera haifanyi kazi kwenye HTTP ya kawaida
• Jaribu browser nyingine (Chrome, Firefox, Edge)
• Hakikisha camera yako ya simu au kompyuta haijazuiwa na programu nyingine

**Vidokezo vya picha nzuri:**
💡 Piga picha wakati wa mchana au mahali penye mwanga mzuri
💡 Karibia taka - zinajaza sehemu kubwa ya picha
💡 Epuka kivuli kinachofunika taka
💡 Piga picha ya taka moja kwa wakati mmoja kwa utambuzi bora

⚠️ Upakiaji wa picha kutoka gallery hautumiki - lazima utumie camera moja kwa moja""",
'en': """## 📷 How to Use the Camera on TakaSmart

**The camera works in:**
• The **Report** section - photographing a waste area
• The **Identify Waste** section - identifying waste type

**Steps:**
1. Tap **'Open Camera'**
2. The browser will ask for permission - tap **'Allow'**
3. The camera will open and show what it sees on screen
4. Point the camera at the waste or area
5. Tap **'Take Photo'** to capture
6. The photo will appear on the page

**Problem: Camera won't open?**
• Check browser settings: click 🔒 or ⓘ in the URL bar → Camera → Allow
• Use **localhost:5000 or HTTPS** - camera does not work on plain HTTP
• Try a different browser (Chrome, Firefox, Edge)
• Make sure your camera is not blocked by another application

**Tips for good photos:**
💡 Take photos in daylight or good lighting
💡 Get close to the waste - it should fill most of the frame
💡 Avoid shadows covering the waste
💡 Photograph one type of waste at a time for best identification

⚠️ Gallery uploads are not supported - you must use the camera directly""",
'fr': """## 📷 Comment Utiliser la Camera sur TakaSmart

**La camera fonctionne dans :**
• La section **Signalement** - photographier une zone de dechets
• La section **Identifier** - identifier le type de dechet

**Etapes :**
1. Appuyez sur **'Ouvrir la camera'**
2. Le navigateur demandera l'autorisation - appuyez sur **'Autoriser'**
3. La camera s'ouvre et montre ce qu'elle voit a l'ecran
4. Pointez la camera vers les dechets ou la zone
5. Appuyez sur **'Prendre une photo'** pour capturer
6. La photo apparaitra sur la page

**Probleme : La camera ne s'ouvre pas ?**
• Verifiez les parametres du navigateur : cliquez sur 🔒 ou ⓘ dans la barre d'URL → Camera → Autoriser
• Utilisez **localhost:5000 ou HTTPS**
• Essayez un navigateur different (Chrome, Firefox, Edge)

**Conseils pour de bonnes photos :**
💡 Prenez des photos en plein jour ou avec un bon eclairage
💡 Approchez-vous des dechets - ils doivent occuper la majorite du cadre
💡 Evitez les ombres couvrant les dechets

⚠️ Les importations depuis la galerie ne sont pas supportees"""
}

KB['register'] = {
'sw': """## 📝 Jinsi ya Kusajili Biashara yako kama Mnunuzi

**Unahitaji nini?**
• Jina la biashara
• Barua pepe halisi
• Namba ya simu
• Eneo lako (mtaa, mji)
• Aina za taka unazozinunua

**Hatua:**
1. **Bonyeza 'Jisajili'** kwenye menyu ya juu
2. **Jaza fomu:**
   • Jina la biashara
   • Barua pepe
   • Namba ya simu
   • Eneo (mtaa, mji)
   • Maelezo mafupi ya biashara
3. **Chagua aina za taka** unazozinunua (unaweza chagua zaidi ya moja)
4. **Ruhusu GPS** - biashara yako itaonekana kwenye ramani ya wananunua
5. **Bonyeza 'Jisajili Sasa'**

**Baada ya usajili:**
✅ Biashara yako itaonekana kwenye orodha ya wananunua
✅ Watu watatafuta biashara yako na kuwasiliana nawe
✅ GPS itasaidia wateja waliopo karibu nawe kukupata

**Vidokezo vya usajili mzuri:**
💡 Andika maelezo mazuri ya biashara - inawasaidia wateja kukuelewa
💡 Weka eneo sahihi - wateja wa karibu watakupata haraka
💡 Chagua aina zote za taka unazozinunua - utapata wateja wengi zaidi""",
'en': """## 📝 How to Register Your Business as a Buyer

**What you need:**
• Business name
• Valid email address
• Phone number
• Your location (street, city)
• Types of waste you buy

**Steps:**
1. **Tap 'Register'** in the top menu
2. **Fill in the form:**
   • Business name
   • Email address
   • Phone number
   • Location (street, city)
   • Short business description
3. **Select waste types** you buy (you can choose more than one)
4. **Allow GPS** - your business will appear on the buyers map
5. **Tap 'Register Now'**

**After registration:**
✅ Your business will appear in the buyers list
✅ People will search for your business and contact you
✅ GPS will help nearby customers find you

**Tips for a good listing:**
💡 Write a good business description - it helps customers understand you
💡 Enter an accurate location - nearby customers will find you faster
💡 Select all waste types you buy - you will get more customers""",
'fr': """## 📝 Comment Inscrire Votre Entreprise comme Acheteur

**Ce dont vous avez besoin :**
• Nom de l'entreprise
• Adresse e-mail valide
• Numero de telephone
• Votre emplacement (rue, ville)
• Types de dechets que vous achetez

**Etapes :**
1. **Appuyez sur 'S'inscrire'** dans le menu superieur
2. **Remplir le formulaire :**
   • Nom de l'entreprise
   • Adresse e-mail
   • Numero de telephone
   • Emplacement (rue, ville)
   • Courte description de l'entreprise
3. **Selectionnez les types de dechets** que vous achetez
4. **Activez le GPS** - votre entreprise apparaitra sur la carte
5. **Appuyez sur 'S'inscrire maintenant'**

**Apres l'inscription :**
✅ Votre entreprise apparaitra dans la liste des acheteurs
✅ Les gens rechercheront votre entreprise et vous contacteront"""
}

KB['safety'] = {
'sw': """## ⚠️ Usalama wa Kushughulikia Taka

**Sheria za msingi za usalama:**

🚫 **Usichome taka za aina yoyote** - plastiki, mpira, e-waste, taka hatari
• Moshi hutoa kemikali za sumu ambazo zinaathiri mapafu na zinaweza kusababisha saratani

🧤 **Vaa kinga inayofaa:**
• Glavu za mpira au ngozi kwa kioo kilichovunjika, chuma chenye ncha kali
• Barakoa ya vumbi ukifanya kazi karibu na madampo
• Viatu vya ngumi ukifanya kazi na taka nzito

👶 **Linda watoto:**
• Taka hatari (betri, sindano, kemikali) ziwekwe mbali na watoto kabisa
• Usiacha watoto kucheza karibu na madampo

🍽️ **Usalama wa chakula na maji:**
• Usihifadhi taka karibu na chakula au maji ya kunywa
• Osha mikono vizuri baada ya kushughulikia taka yoyote

🏠 **Hifadhi salama:**
• Hifadhi taka mahali penye hewa - usiifunge kwenye chumba bila hewa
• Taka za kikolojia zinaoza na kutoa gesi hatari ukifunga kabisa

**Kwa taka hatari:**
• Betri: Usiziache kwenye jua kali, usichomeke, usivunje
• Sindano: Weka kwenye chombo kigumu cha plastiki au chuma kabla ya kutupa
• Kemikali: Hifadhi kwenye chombo chake cha asili, usihifadhi pamoja na kemikali nyingine

💡 Dalili za hatari: kizunguzungu, maumivu ya kichwa, matatizo ya kupumua baada ya kushughulikia taka - toka nje na pumzika kwenye hewa safi, wasiliana na daktari""",
'en': """## ⚠️ Waste Handling Safety

**Basic safety rules:**

🚫 **Never burn any type of waste** - plastic, rubber, e-waste, hazardous materials
• Smoke releases toxic chemicals that affect the lungs and can cause cancer

🧤 **Wear appropriate protection:**
• Rubber or leather gloves for broken glass, sharp metal
• Dust mask when working near dumpsites
• Closed-toe shoes when handling heavy waste

👶 **Protect children:**
• Hazardous waste (batteries, needles, chemicals) must be completely out of reach of children
• Do not let children play near dumpsites

🍽️ **Food and water safety:**
• Never store waste near food or drinking water
• Wash hands thoroughly after handling any waste

🏠 **Safe storage:**
• Store waste in a ventilated area - do not seal it in a room without airflow
• Organic waste decomposes and releases hazardous gases if sealed completely

**For hazardous waste:**
• Batteries: Do not leave in direct sunlight, do not charge them, do not break them
• Needles: Place in a hard plastic or metal container before disposal
• Chemicals: Store in original container, do not store with other chemicals

💡 Warning signs: dizziness, headache, breathing difficulty after handling waste - go outside and rest in fresh air, contact a doctor""",
'fr': """## ⚠️ Securite lors de la Manipulation des Dechets

**Regles de securite de base :**

🚫 **Ne jamais bruler aucun type de dechet** - plastique, caoutchouc, electronique, matières dangereuses
• La fumee libere des produits chimiques toxiques qui affectent les poumons et peuvent causer le cancer

🧤 **Porter une protection appropriee :**
• Gants en caoutchouc ou cuir pour le verre brise, le metal tranchant
• Masque anti-poussiere pres des decharges
• Chaussures fermees pour les dechets lourds

👶 **Proteger les enfants :**
• Les dechets dangereux doivent etre completement hors de portee des enfants

🍽️ **Securite alimentaire et hydrique :**
• Ne jamais stocker de dechets pres des aliments ou de l'eau potable
• Se laver les mains apres avoir manipule des dechets

💡 Signes d'alerte : vertiges, maux de tete, difficultees respiratoires - sortez et reposez-vous a l'air frais, consultez un medecin"""
}

KB['not_understood'] = {
'sw': """Je, unaweza kuuliza tena kwa njia tofauti? Sijafaulu kuelewa swali lako vizuri.

Mimi ni **TakaSmart Assistant** na ninasaidia na maswali kuhusu:
• ♻️ Taka na recycling (plastiki, karatasi, kioo, chuma, kikolojia, e-waste, nguo)
• 🌍 Mazingira (uchafuzi wa maji, hewa, udongo)
• 🌡️ Mabadiliko ya tabianchi
• 🏥 Afya na usalama wa taka
• 🏛️ Sheria za mazingira
• 📱 Mfumo wa TakaSmart (ripoti, wananunua, usajili)

Niulize swali kuhusu mada hizi! 💬""",
'en': """Could you please rephrase your question? I was not able to understand it clearly.

I am **TakaSmart Assistant** and I help with questions about:
• ♻️ Waste and recycling (plastic, paper, glass, metal, organic, e-waste, textiles)
• 🌍 Environment (water, air, soil pollution)
• 🌡️ Climate change
• 🏥 Waste health and safety
• 🏛️ Environmental laws
• 📱 The TakaSmart platform (reports, buyers, registration)

Please ask a question about these topics! 💬""",
'fr': """Pourriez-vous reformuler votre question ? Je n'ai pas pu la comprendre clairement.

Je suis **TakaSmart Assistant** et j'aide avec les questions sur :
• ♻️ Dechets et recyclage (plastique, papier, verre, metal, organique, electronique, textile)
• 🌍 Environnement (pollution eau, air, sol)
• 🌡️ Changement climatique
• 🏥 Sante et securite des dechets
• 🏛️ Lois environnementales
• 📱 La plateforme TakaSmart

Posez une question sur ces sujets ! 💬"""
}

KB['off_topic'] = {
'sw': """Samahani, swali hilo halikuhusu taka wala mazingira.

Mimi ni **TakaSmart Assistant** - ninasaidia **tu** na maswali yanayohusiana na:
• Taka (plastiki, karatasi, kioo, chuma, kikolojia, e-waste, nguo)
• Mazingira (uchafuzi wa maji, hewa, udongo)
• Mabadiliko ya tabianchi
• Afya inayohusiana na taka
• Mfumo wa TakaSmart

Tafadhali niulize swali linalohusiana na mada hizi. 🙏""",
'en': """Sorry, that question is not related to waste or the environment.

I am **TakaSmart Assistant** - I can **only** help with questions related to:
• Waste (plastic, paper, glass, metal, organic, e-waste, textiles)
• Environment (water, air, soil pollution)
• Climate change
• Waste-related health topics
• The TakaSmart platform

Please ask me a question related to these topics. 🙏""",
'fr': """Desolee, cette question ne concerne pas les dechets ni l'environnement.

Je suis **TakaSmart Assistant** - je peux **seulement** aider avec des questions liees a :
• Dechets (plastique, papier, verre, metal, organique, electronique, textile)
• Environnement (pollution eau, air, sol)
• Changement climatique
• Sante liee aux dechets
• La plateforme TakaSmart

Veuillez me poser une question liee a ces sujets. 🙏"""
}

# =====================================================================
#  KEYWORDS — topic trigger words in all 3 languages
# =====================================================================
KEYWORDS = {
    "hello":       ["hello","hi","jambo","habari","bonjour","salut","hey","sasa","mambo","niaje"],
    "help":        ["help","msaada","aide","what can","naweza","commands","nini unaweza","unaeza","nikusaidia"],
    "plastic":     ["plastic","plastiki","plastique","pet","hdpe","pvc","ldpe","chupa","mfuko wa plastiki","bottle","polyethylene","polythene"],
    "paper":       ["paper","karatasi","papier","cardboard","carton","kadibodi","gazeti","newspaper","magazine","sanduku la karatasi"],
    "glass":       ["glass","kioo","verre","chupa ya kioo","dirisha","window glass","bottle glass"],
    "metal":       ["metal","chuma","aluminium","shaba","copper","steel","scrap","bati","ferraille","iron","zinc","metali"],
    "organic":     ["organic","kikolojia","compost","chakula","food waste","mabaki ya chakula","majani","matunda","organique","decompose","kuoza"],
    "ewaste":      ["ewaste","e-waste","electronic","electronique","betri","battery","simu chakavu","kompyuta","televisheni","charger","keyboard","laptop","monitor","printer"],
    "textile":     ["textile","nguo","clothes","clothing","vetement","fabrics","cotton","pamba","sufu","wool","shirt","pants","jeans","garment"],
    "recycle":     ["recycle","recycling","kurecycle","recyclage","reuse","tumia tena","3r","reduce","hatua za recycling"],
    "hazardous":   ["hazardous","hatari","dangerous","betri hatari","battery","sindano","needle","kemikali","chemical","asbestos","sumu","toxic","poison","risasi","lead","mercury","zebaki","cadmium"],
    "water":       ["water","maji","mto","river","bahari","ocean","ziwa","lake","uchafuzi wa maji","water pollution","contamination","pollution eau","drinking water","visima","groundwater"],
    "air":         ["air","hewa","uchafuzi wa hewa","air pollution","moshi","smoke","kuchoma","burning","dioxin","fumee","mapafu","lungs"],
    "climate":     ["climate","tabianchi","climate change","mabadiliko ya tabianchi","greenhouse","global warming","methane","co2","carbon","ongezeko la joto","gesi ya chafu"],
    "health":      ["health","afya","ugonjwa","malaria","dengue","cholera","typhoid","kipindupindu","disease","magonjwa","sante","cancer","saratani","sumu ya risasi","lead poisoning"],
    "wildlife":    ["wildlife","wanyama","animal","samaki","fish","ndege","bird","kasa","turtle","whale","nyangumi","dolphin","fauna","wanyamapori","nature"],
    "soil":        ["soil","udongo","ardhi","ground","uchafuzi wa udongo","soil pollution","kilimo","farming","shamba","agriculture","fertiliser","mbolea"],
    "ocean":       ["ocean","bahari","sea","bahari ya pwani","microplastic","microplastics","marine","garbage patch","pwani","coast"],
    "landfill":    ["landfill","dampo","dumping","madampo","dumpsite","methane","leachate","taka kwenye ardhi","disposal","utupaji"],
    "3rs":         ["3r","reduce reuse recycle","refuse","repair","rot","zero waste","kupunguza","punguza","reuse","reutiliser"],
    "zero_waste":  ["zero waste","zero dechet","maisha ya zero","zero waste lifestyle","beba mfuko","cloth bag","reusable","sustainable"],
    "government":  ["government","sheria","law","serikali","nemc","ema","regulation","kanuni","policy","halmashauri","municipal","wizara","ministry"],
    "report":      ["report","ripoti","tuma ripoti","submit report","signaler","jinsi ya kutuma","how to report","eneo la uchafu"],
    "camera":      ["camera","picha","photo","picture","kamera","jinsi ya kutumia camera","how to use camera","galerie","gallery","haifunguki"],
    "buyer":       ["buyer","buyers","mnunuzi","wananunua","acheteur","sell","uza","bei","price","thamani","kupata mnunuzi","find buyer"],
    "register":    ["register","jisajili","signup","inscription","biashara yangu","my business","usajili"],
    "safety":      ["safety","safe","usalama","danger","hatari","kinga","gloves","protection","securite","tahadhari"],
    "ocean":       ["ocean","bahari kubwa","sea","microplastic","pwani","coastal","marine pollution"],
    "compost":     ["compost","komposti","mbolea","fertiliser","fertilizer","kutengeneza mbolea","how to compost","organic waste"],
    "off_topic":   ["siasa","politics","football","soccer","recipe","cooking","kupika","pesa zangu","bank","benki","history","historia","math","science","muziki","music","filamu","movie","mchezo","sports","weather","hali ya hewa","translate","tafsiri","poem","joke","mzaha","funny","love","mpenzi"],
}

OFF_TOPIC_SIGNALS = re.compile(
    r"\b(siasa|politics|football|soccer|recipe|cooking|kupika|historia|history|"
    r"mathematics|math|hisabati|muziki|music|filamu|movie|mchezo wa|sports|"
    r"translate|tafsiri|poem|shairi|joke|mzaha|funny|blague|love|mpenzi|"
    r"send money|nipe pesa|benki|bank|stock market|soko la hisa)\b",
    re.IGNORECASE | re.UNICODE,
)

PRIORITY = [
    "off_topic","hazardous","ewaste","ocean","microplastic","landfill",
    "climate","health","water","air","soil","wildlife","3rs","zero_waste",
    "government","compost","register","camera","report","buyer",
]

# =====================================================================
#  ENGINE
# =====================================================================

def _norm(text):
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def _score(text, words):
    best = 0
    for w in words:
        if " " in w:
            if w in text:
                best = max(best, len(w))
        else:
            if re.search(r"\b" + re.escape(w) + r"\b", text):
                best = max(best, len(w))
    return best

def get_chat_reply(message: str, lang: str = "sw") -> str:
    lang = lang if lang in ("sw","en","fr") else "sw"
    raw  = (message or "").strip()
    text = _norm(raw)

    if not text:
        return KB["help"][lang]

    # Off-topic check
    if OFF_TOPIC_SIGNALS.search(raw):
        return KB["off_topic"][lang]

    # Score all topics
    scores = {}
    for topic, words in KEYWORDS.items():
        if topic == "off_topic":
            continue
        s = _score(text, words)
        if s:
            scores[topic] = s

    if not scores:
        return KB["not_understood"][lang]

    best_score = max(scores.values())

    # Priority pass
    for topic in PRIORITY:
        if topic in scores and scores[topic] >= best_score - 2:
            answer = KB.get(topic, {}).get(lang) or KB.get(topic, {}).get("sw")
            if answer:
                return answer

    # Best score
    best = max(scores, key=lambda k: scores[k])
    answer = KB.get(best, {}).get(lang) or KB.get(best, {}).get("sw")
    return answer or KB["not_understood"][lang]

# ── PATCH: missing entries ────────────────────────────────────────
KB["hello"] = {
"sw": "Jambo! Mimi ni **TakaSmart Assistant**.\n\nNinakusaidia kuhusu:\n- **Taka na recycling** - plastiki, karatasi, kioo, chuma, kikolojia, e-waste, nguo\n- **Mazingira** - uchafuzi wa maji, hewa, udongo, wanyamapori\n- **Afya** - athari za taka kwa binadamu\n- **Tabianchi** - jinsi taka zinavyoathiri hali ya hewa\n- **Mfumo wa TakaSmart** - ripoti, wananunua, usajili\n\nNiulize swali lolote kuhusu uchafu! 🌿",
"en": "Hello! I am **TakaSmart Assistant**.\n\nI can help with:\n- **Waste and recycling** - plastic, paper, glass, metal, organic, e-waste, textiles\n- **Environment** - water, air and soil pollution, wildlife\n- **Health** - health effects of poorly managed waste\n- **Climate** - how waste contributes to global warming\n- **TakaSmart platform** - reporting, buyers, registration\n\nAsk me anything about waste! 🌿",
"fr": "Bonjour ! Je suis **TakaSmart Assistant**.\n\nJe peux vous aider avec :\n- **Dechets et recyclage** - plastique, papier, verre, metal, organique, electronique, textile\n- **Environnement** - pollution eau, air, sol, faune\n- **Sante** - effets des dechets sur la sante\n- **Climat** - comment les dechets affectent le climat\n- **Plateforme TakaSmart** - signalements, acheteurs, inscription\n\nPosez n'importe quelle question sur les dechets ! 🌿",
}

KB["help"] = {
"sw": "## Ninachoweza kukusaidia:\n\n**Aina za taka na recycling**\n- Plastiki, karatasi, kioo, chuma, kikolojia, e-waste, nguo\n\n**Mazingira**\n- Uchafuzi wa maji, hewa, udongo\n- Wanyamapori\n- Mabadiliko ya tabianchi\n- Microplastics na bahari\n- Madampo\n\n**Afya na usalama**\n- Athari za taka kwa afya\n- Taka hatari\n\n**Mfumo wa TakaSmart**\n- Kutuma ripoti\n- Kutambua taka\n- Kupata wananunua\n- Usajili wa biashara\n\nNiulize swali lolote! 💬",
"en": "## What I can help with:\n\n**Waste types and recycling**\n- Plastic, paper, glass, metal, organic, e-waste, textiles\n\n**Environment**\n- Water, air and soil pollution\n- Wildlife\n- Climate change\n- Microplastics and the ocean\n- Landfills\n\n**Health and safety**\n- Health effects of waste\n- Hazardous waste\n\n**TakaSmart platform**\n- Submitting reports\n- Identifying waste\n- Finding buyers\n- Business registration\n\nAsk me anything! 💬",
"fr": "## Ce avec quoi je peux vous aider :\n\n**Types de dechets et recyclage**\n- Plastique, papier, verre, metal, organique, electronique, textile\n\n**Environnement**\n- Pollution eau, air, sol\n- Faune sauvage\n- Changement climatique\n- Microplastiques et ocean\n- Decharges\n\n**Sante et securite**\n- Effets des dechets sur la sante\n- Dechets dangereux\n\n**Plateforme TakaSmart**\n- Signalements, identification, acheteurs, inscription\n\nPosez n'importe quelle question ! 💬",
}

KB["compost"] = KB["organic"]  # alias

# ── PATCH: fix KEYWORDS ───────────────────────────────────────────
# Add hello + help triggers, fix glass to score higher for "recycle glass"
KEYWORDS["hello"]   = ["hello","hi","jambo","habari","bonjour","salut","hey","sasa","mambo","niaje","greetings","karibu"]
KEYWORDS["help"]    = ["help","msaada","aide","what can you","naweza kukuuliza","commands","nikusaidia","unaeza","about you"]
KEYWORDS["glass"]   = ["glass","kioo","verre","chupa ya kioo","dirisha","window glass","bottle glass","recycle glass","kioo recycling","glass recycling"]
KEYWORDS["soil"]    = ["soil","udongo","ardhi","ground","uchafuzi wa udongo","soil pollution","soil contamination","kilimo","farming","shamba","agriculture","fertiliser","mbolea","ground pollution","contaminated soil","soil damage"]
KEYWORDS["compost"] = ["compost","komposti","mbolea","fertiliser","fertilizer","kutengeneza mbolea","how to compost","organic fertilizer","organic waste","jinsi ya compost"]
KEYWORDS["organic"] = ["organic","kikolojia","food waste","mabaki ya chakula","majani","matunda","organique","decompose","kuoza","kitchen waste","garden waste"]

# Add hello+help to PRIORITY (at the start)
if "hello" not in PRIORITY:
    PRIORITY.insert(0, "hello")
if "help" not in PRIORITY:
    PRIORITY.insert(1, "help")
if "compost" not in PRIORITY:
    PRIORITY.insert(PRIORITY.index("government"), "compost")
if "glass" not in PRIORITY:
    PRIORITY.insert(PRIORITY.index("register"), "glass")

# ── PATCH 2: keyword fixes ────────────────────────────────────────
KEYWORDS["ocean"]      += ["microplastic","microplastics","micro plastic","ocean pollution","marine debris","sea pollution","garbage patch"]
KEYWORDS["hazardous"]  += ["betri za gari","car battery","acid battery","betri hatari","sindano","needle syringe","kemia","taka hatari","dispose battery","kutupa betri"]
# Make hazardous score higher than ewaste for battery disposal questions
# by adding longer phrases that distinguish them
KEYWORDS["ewaste"]      = [w for w in KEYWORDS["ewaste"] if w not in ("betri","battery")]
KEYWORDS["ewaste"]     += ["old phone","old computer","broken phone","simu ya zamani","kompyuta ya zamani","electronic recycling"]

# ── PATCH 3 ───────────────────────────────────────────────────────
KEYWORDS["3rs"] += ["what are the 3r","what are 3r","3 r","three r","reduce reuse","reduce and reuse","kanuni ya 3r","principes 3r","reduce recycle reuse","les 3r"]
KEYWORDS["zero_waste"] += ["zero rubbish","no waste","avoid waste","waste free","taka kidogo","punguza taka zote"]
KEYWORDS["compost"] += ["kutengeneza mbolea nyumbani","how to make fertilizer","organic fertilizer home","mbolea ya bustani"]
KEYWORDS["plastic"] += ["single use","single-use","disposable plastic","kupunguza plastiki","plastiki ya kutupa","reduce plastic","less plastic","no plastic bags"]
KEYWORDS["landfill"] += ["open dump","illegal dump","madampo haramu","dumping site","waste dump","tupa ovyo","kutupa ovyo"]
# Also add 3rs to PRIORITY list ahead of recycle
if "3rs" not in PRIORITY:
    idx = PRIORITY.index("compost") if "compost" in PRIORITY else len(PRIORITY)
    PRIORITY.insert(idx, "3rs")
