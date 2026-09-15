
from pathlib import Path

WASTE_DB = {
    "plastic": {
        "type":"Plastiki","typeEn":"Plastic","typeFr":"Plastique","badge":"badge-plastic","icon":"🧴",
        "desc":{"sw":"Hii ni taka ya plastiki. Tenganisha na taka nyingine na ipeleke kwenye kituo cha ukusanyaji.","en":"This is plastic waste. Separate it and take it to a collection/recycling point.","fr":"Ceci est un déchet plastique. Séparez-le et apportez-le à un point de collecte."},
        "steps":{"sw":["Safisha na ondoa mabaki","Tenganisha PET, HDPE, PVC","Bana ili kupunguza ukubwa","Peleka kwenye kituo cha plastiki","Au uuze kwa mnunuzi wa plastiki"],
                 "en":["Clean it","Separate PET, HDPE and PVC","Compress to reduce volume","Take it to a plastic collection point","Or sell to a registered buyer"],
                 "fr":["Nettoyez","Séparez PET, HDPE et PVC","Compactez","Apportez à un point de collecte","Ou vendez à un acheteur"]}},
    "paper": {
        "type":"Karatasi","typeEn":"Paper","typeFr":"Papier","badge":"badge-paper","icon":"📦",
        "desc":{"sw":"Hii ni taka ya karatasi na inaweza kukusanywa kwa ajili ya recycling.","en":"This is paper waste and can be collected for recycling.","fr":"Ceci est un déchet papier recyclable."},
        "steps":{"sw":["Tenganisha karatasi","Ondoa zilizojaa mafuta/kemikali","Zikunje au zibane","Peleka kituo cha karatasi","Uza kwa mnunuzi"],
                 "en":["Separate paper","Remove oily/chemical paper","Flatten it","Take it to a paper collection point","Sell to a buyer"],
                 "fr":["Séparez le papier","Retirez le papier huileux","Aplatissez-le","Apportez-le à un centre","Vendez-le"]}},
    "glass": {
        "type":"Kioo","typeEn":"Glass","typeFr":"Verre","badge":"badge-glass","icon":"🍶",
        "desc":{"sw":"Hii ni taka ya kioo. Ishughulikie kwa uangalifu kwa sababu inaweza kukata.","en":"This is glass waste. Handle carefully because it can cut.","fr":"Ceci est un déchet de verre. Manipulez-le avec précaution."},
        "steps":{"sw":["Vaa kinga inapowezekana","Tenganisha kwa rangi","Ondoa uchafu","Usichanganye na taka nyingine","Peleka kituo cha kioo"],
                 "en":["Use protection when possible","Separate by color","Remove dirt","Do not mix with other waste","Take to a glass collection point"],
                 "fr":["Utilisez une protection","Séparez par couleur","Retirez la saleté","Ne mélangez pas","Apportez à un centre"]}},
    "metal": {
        "type":"Chuma","typeEn":"Metal","typeFr":"Métal","badge":"badge-metal","icon":"🔩",
        "desc":{"sw":"Hii ni taka ya chuma kama aluminium, shaba au chuma chakavu.","en":"This is metal waste such as aluminium, copper or scrap steel.","fr":"Ceci est un déchet métallique."},
        "steps":{"sw":["Tenganisha aina za metali","Ondoa sehemu zisizo za chuma","Safisha","Punguza ukubwa inapowezekana","Uza kwa mnunuzi wa chuma"],
                 "en":["Separate metal types","Remove non-metal parts","Clean it","Reduce volume when possible","Sell to a metal buyer"],
                 "fr":["Séparez les métaux","Retirez les parties non métalliques","Nettoyez","Réduisez le volume","Vendez à un acheteur"]}},
    "organic": {
        "type":"Kikolojia","typeEn":"Organic","typeFr":"Organique","badge":"badge-organic","icon":"🍂",
        "desc":{"sw":"Hii ni taka ya kikolojia inayoweza kutumika kutengeneza komposti.","en":"This is organic waste that can be composted.","fr":"Ceci est un déchet organique qui peut être composté."},
        "steps":{"sw":["Tenganisha taka za kikolojia","Weka kwenye komposti","Changanya na majani","Geuza mara kwa mara","Tumia mbolea iliyotengenezwa"],
                 "en":["Separate organic waste","Put it in compost","Mix with dry leaves","Turn regularly","Use the finished compost"],
                 "fr":["Séparez les déchets organiques","Mettez-les au compost","Ajoutez des feuilles","Retournez régulièrement","Utilisez le compost"]}},
    "ewaste": {
        "type":"E-Waste","typeEn":"E-Waste","typeFr":"Déchets électroniques","badge":"badge-ewaste","icon":"💻",
        "desc":{"sw":"Hii ni taka ya elektroniki. Ipeleke kwenye kituo kilichoidhinishwa; usiichome au kuitupa ovyo.","en":"This is electronic waste. Take it to an approved e-waste facility; do not burn or dump it.","fr":"Ceci est un déchet électronique. Apportez-le à un centre agréé."},
        "steps":{"sw":["Usichome e-waste","Tenganisha betri kwa usalama","Hifadhi sehemu kavu","Peleka kituo kilichoidhinishwa","Au wasiliana na mnunuzi wa e-waste"],
                 "en":["Do not burn e-waste","Handle batteries safely","Store it dry","Take it to an approved facility","Contact an e-waste buyer"],
                 "fr":["Ne brûlez pas","Manipulez les batteries avec soin","Conservez au sec","Apportez à un centre agréé","Contactez un acheteur"]}},
    "textile": {
        "type":"Vazi/Nguo","typeEn":"Textile","typeFr":"Textile","badge":"badge-textile","icon":"👕",
        "desc":{"sw":"Hii ni taka ya nguo. Nguo nzuri inaweza kutumika tena au kutolewa.","en":"This is textile waste. Usable clothes can be reused or donated.","fr":"Ceci est un déchet textile. Les vêtements utilisables peuvent être réemployés."},
        "steps":{"sw":["Tenganisha nguo nzuri","Toa au uza zinazofaa","Tenganisha zilizochakaa","Peleka kwenye recycling ya nguo","Hifadhi kwa usafi"],
                 "en":["Separate usable clothes","Donate or sell usable items","Separate worn textiles","Take them to textile recycling","Keep them clean"],
                 "fr":["Séparez les vêtements utilisables","Donnez ou vendez","Séparez les textiles usés","Apportez-les au recyclage","Gardez-les propres"]}}
}

def classify_waste(file_storage):
    """
    Starter classifier. It is intentionally transparent: it uses the filename
    as a demo signal. For true image AI, replace this function with a trained
    TensorFlow/PyTorch/YOLO model.
    """
    name = Path(file_storage.filename or "").stem.lower()
    aliases = {
        "plastic":["plastic","plastiki","bottle","chupa","polybag"],
        "paper":["paper","karatasi","cardboard","carton","gazeti"],
        "glass":["glass","kioo","bottle_glass"],
        "metal":["metal","chuma","aluminium","aluminum","copper","scrap"],
        "organic":["organic","chakula","food","leaf","majani","compost"],
        "ewaste":["ewaste","e-waste","phone","computer","laptop","tv","electronic"],
        "textile":["textile","cloth","nguo","shirt","shoe"]
    }
    selected = None
    for key, words in aliases.items():
        if any(w in name for w in words):
            selected = key
            break
    selected = selected or "plastic"
    return {"waste": WASTE_DB[selected], "demo": True}
