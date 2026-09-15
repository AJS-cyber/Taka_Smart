"""Multilingual domain assistant for TakaSmart."""

ANSWERS = {
    "sw": {
        "hello": "Jambo! Naweza kusaidia kuhusu camera, GPS, ripoti, aina za taka, recycling, wanunuzi, usajili, faragha na usalama.",
        "report": "Fungua Ripoti, ruhusu camera, piga picha ya eneo, jaza maelezo na mamlaka, thibitisha location kwenye ramani, kisha bonyeza Tuma Ripoti.",
        "camera": "Bonyeza Fungua Camera, ruhusu camera, elekeza kwenye taka, kisha bonyeza Piga Picha. Gallery uploads hazitumiki.",
        "location": "Ruhusu GPS ili location iambatane na picha. Unaweza pia kubofya sehemu sahihi kwenye ramani kuweka coordinates.",
        "types": "Aina ni plastiki, karatasi, kioo, chuma, taka za kikolojia, e-waste na nguo/textile.",
        "plastic": "Safisha plastiki, tenga PET/HDPE/PVC, bana, usichome, kisha ipeleke kituo cha ukusanyaji au kwa mnunuzi.",
        "recycle": "Kurecycle plastiki: 1. Tenganisha plastiki na taka nyingine. 2. Safisha chupa/vifungashio na ondoa mabaki. 3. Tenganisha PET, HDPE na PVC. 4. Bana ili kupunguza nafasi. 5. Peleka kwenye kituo cha recycling au wasiliana na mnunuzi. Usichome plastiki.",
        "paper": "Tenga karatasi, ondoa zenye mafuta/kemikali, zihifadhi kavu, kisha peleka kwa recycler au mnunuzi.",
        "glass": "Vaa kinga unaposhughulikia kioo, kitenganishe, kisha peleka kwenye kituo cha kioo.",
        "metal": "Tenga aluminium, shaba na chuma, ondoa sehemu zisizo za chuma, kisha wasiliana na mnunuzi wa scrap metal.",
        "organic": "Tenganisha taka za kikolojia na tengeneza compost kwa majani makavu. Usichanganye na plastiki au kemikali.",
        "ewaste": "Usichome e-waste wala kuvunja betri. Hifadhi sehemu kavu na peleka kituo kilichoidhinishwa.",
        "textile": "Tenga nguo zinazoweza kutumika kwa kutoa au kuuza; peleka zilizochakaa kwenye textile recycling.",
        "buyer": "Fungua Wananunua, chagua aina ya taka, tafuta kwa jina/eneo, kisha bonyeza Wasiliana. Wanunuzi wenye GPS huonekana kwenye ramani.",
        "register": "Fungua Jisajili, jaza biashara, email, simu, eneo na aina za taka unazonunua. Ruhusu GPS ili biashara ionekane kwenye ramani.",
        "safety": "Usichome plastiki/e-waste, shika kioo kwa kinga, na weka taka hatari mbali na watoto, chakula na maji.",
        "privacy": "Camera hutumika baada ya ruhusa yako. Picha hutumwa unapobonyeza Tuma Ripoti au kuomba utambuzi.",
        "another_photo": "Baada ya majibu kuonekana, bonyeza Piga Picha Nyingine. Mfumo utaondoa jibu la awali na kufungua camera tena.",
        "accuracy": "Utambuzi wa picha wa sasa ni wa demo na hauwezi kuthibitisha aina ya taka kwa 100%. Angalia picha na jibu, kisha muulize mtaalamu ikiwa taka ni hatari.",
        "price": "TakaSmart haiweki bei ya kudumu. Bei hutegemea aina, usafi, uzito, kiasi na mnunuzi; wasiliana na wanunuzi kadhaa kwenye sehemu ya Wananunua.",
        "error": "Kama camera haifunguki, ruhusu camera kwenye browser na tumia localhost/HTTPS. Kama upload inakataa, hakikisha ni picha ya JPG, PNG, GIF au WEBP chini ya 8 MB.",
        "authority": "Kwa ripoti, chagua mamlaka kulingana na tatizo: Halmashauri kwa uchafu wa eneo, Afya kwa hatari za kiafya, Mazingira kwa uchafuzi, au Shirika la Taka kwa ukusanyaji.",
        "compost": "Kwa compost, tumia mabaki ya matunda/mboga na majani. Epuka plastiki, kioo, metali, kemikali, nyama nyingi na taka za binadamu.",
        "hazardous": "Usiguse taka hatari bila kinga. Betri, sindano, kemikali, asbestos na e-waste viweke mbali na watoto, chakula na maji, kisha wasiliana na mamlaka iliyopo.",
        "help": "Naweza kusaidia kuhusu camera, picha nyingine, GPS, ripoti, mamlaka, aina za taka, recycling, compost, bei, wanunuzi, usajili, faragha na usalama.",
    },
    "en": {
        "hello": "Hello! I can help with camera, GPS, reports, waste types, recycling, buyers, registration, and safety.",
        "report": "Open Report, allow the camera, take a photo, add details and authority, confirm the map location, then submit.",
        "camera": "Press Open Camera, grant permission, point at the waste, then press Take Photo. Gallery uploads are not used.",
        "location": "Allow GPS to attach the photo location. You can also click the exact point on the map to save coordinates.",
        "types": "Categories are plastic, paper, glass, metal, organic waste, e-waste, and textiles.",
        "plastic": "Clean plastic, separate PET/HDPE/PVC, compress it, never burn it, then take it to a collection point or buyer.",
        "recycle": "To recycle plastic: 1. Separate it from other waste. 2. Clean bottles and packaging. 3. Sort PET, HDPE, and PVC. 4. Compress it to save space. 5. Take it to a recycling point or contact a buyer. Never burn plastic.",
        "paper": "Separate paper, remove oily or chemical paper, keep it dry, then take it to a recycler or buyer.",
        "glass": "Use protection when handling glass, keep it separate, then take it to a glass collection point.",
        "metal": "Separate aluminium, copper, and steel, remove non-metal parts, then contact a scrap-metal buyer.",
        "organic": "Separate organic waste and compost it with dry leaves. Keep it away from plastic and chemicals.",
        "ewaste": "Never burn e-waste or break batteries. Keep it dry and take it to an approved facility.",
        "textile": "Donate or sell reusable clothes and take worn textiles to textile recycling.",
        "buyer": "Open Buyers, choose a waste type, search by name or area, then press Contact. GPS-enabled buyers appear on the map.",
        "register": "Open Register, add business details, location, and waste types purchased. Allow GPS to appear on the map.",
        "safety": "Do not burn plastic or e-waste. Handle glass with protection and keep hazardous waste away from children, food, and water.",
        "privacy": "The camera is used after permission. Photos are sent only when you submit a report or request identification.",
        "another_photo": "After the result appears, press Take Another Photo. The previous result is cleared and the camera opens again.",
        "accuracy": "The current image identification is a demo and cannot guarantee 100% accuracy. Review the result and ask a qualified professional about hazardous waste.",
        "price": "TakaSmart does not set fixed prices. Price depends on type, cleanliness, weight, volume, and buyer; contact several buyers in Buyers.",
        "error": "If the camera does not open, allow browser camera access and use localhost/HTTPS. Accepted images are JPG, PNG, GIF, or WEBP under 8 MB.",
        "authority": "For reports, choose the authority that matches the issue: municipality for public waste, health for health risks, environment for pollution, or waste services for collection.",
        "compost": "For compost, use fruit and vegetable scraps with dry leaves. Keep out plastic, glass, metal, chemicals, large amounts of meat, and human waste.",
        "hazardous": "Do not handle hazardous waste without protection. Keep batteries, needles, chemicals, asbestos, and e-waste away from children, food, and water, then contact the relevant authority.",
        "help": "I can help with camera, taking another photo, GPS, reports, authorities, waste types, recycling, compost, prices, buyers, registration, privacy, and safety.",
    },
    "fr": {
        "hello": "Bonjour ! Je peux aider avec la caméra, le GPS, les signalements, les déchets, le recyclage et les acheteurs.",
        "report": "Ouvrez Signaler, autorisez la caméra, prenez une photo, ajoutez les détails et l'autorité, confirmez la carte, puis envoyez.",
        "camera": "Appuyez sur Ouvrir la caméra, autorisez-la et appuyez sur Prendre la photo. La galerie n'est pas utilisée.",
        "location": "Autorisez le GPS pour joindre la position. Vous pouvez aussi cliquer sur la carte pour enregistrer les coordonnées.",
        "types": "Les catégories sont plastique, papier, verre, métal, organique, électronique et textile.",
        "plastic": "Nettoyez le plastique, séparez PET/HDPE/PVC, compactez-le, ne le brûlez jamais et apportez-le à un point de collecte.",
        "recycle": "Pour recycler le plastique : 1. Séparez-le des autres déchets. 2. Nettoyez les bouteilles et emballages. 3. Triez PET, HDPE et PVC. 4. Compactez-les. 5. Apportez-les à un point de recyclage ou contactez un acheteur. Ne brûlez jamais le plastique.",
        "paper": "Séparez le papier, retirez le papier gras ou chimique, gardez-le sec et apportez-le à un recycleur.",
        "glass": "Utilisez une protection, gardez le verre séparé et apportez-le à un point de collecte.",
        "metal": "Séparez aluminium, cuivre et acier, retirez les parties non métalliques et contactez un acheteur.",
        "organic": "Séparez les déchets organiques et faites du compost avec des feuilles sèches.",
        "ewaste": "Ne brûlez pas les déchets électroniques et ne cassez pas les batteries. Apportez-les à un centre agréé.",
        "textile": "Donnez ou vendez les vêtements réutilisables et recyclez les textiles usés.",
        "buyer": "Ouvrez Acheteurs, choisissez le type, recherchez une zone et appuyez sur Contacter. Les acheteurs géolocalisés apparaissent sur la carte.",
        "register": "Ouvrez Inscription et ajoutez votre entreprise, votre zone et les types achetés. Autorisez le GPS pour la carte.",
        "safety": "Ne brûlez pas le plastique ou l'électronique et manipulez le verre avec protection.",
        "privacy": "La caméra est utilisée après autorisation. La photo est envoyée seulement après votre action.",
        "another_photo": "Après le résultat, appuyez sur Prendre une autre photo. Le résultat précédent est effacé et la caméra se rouvre.",
        "accuracy": "L'identification actuelle est une démonstration et ne garantit pas une précision de 100 %. Vérifiez le résultat et demandez conseil pour les déchets dangereux.",
        "price": "TakaSmart ne fixe pas les prix. Le prix dépend du type, de la propreté, du poids, du volume et de l'acheteur.",
        "error": "Si la caméra ne s'ouvre pas, autorisez-la dans le navigateur et utilisez localhost/HTTPS. Les images acceptées sont JPG, PNG, GIF ou WEBP sous 8 Mo.",
        "authority": "Choisissez la mairie pour les déchets publics, la santé pour les risques sanitaires, l'environnement pour la pollution et le service des déchets pour la collecte.",
        "compost": "Pour le compost, utilisez les restes de fruits/légumes et des feuilles sèches. Évitez plastique, verre, métal, produits chimiques et déchets humains.",
        "hazardous": "Ne manipulez pas les déchets dangereux sans protection. Éloignez batteries, aiguilles, produits chimiques, amiante et déchets électroniques des enfants, aliments et eau.",
        "help": "Je peux aider avec la caméra, une autre photo, le GPS, les signalements, les autorités, les catégories, le recyclage, le compost, les prix, les acheteurs, l'inscription et la sécurité.",
    },
}

KEYWORDS = {
    "hello": ["hello", "hi", "jambo", "habari", "bonjour", "salut"],
    "camera": ["camera", "kamera", "picha", "photo", "gallery", "galeri"],
    "location": ["gps", "location", "eneo", "mahali", "map", "ramani", "position"],
    "report": ["report", "ripoti", "uchafu", "authority", "mamlaka", "signaler"],
    "types": ["aina", "type", "types", "category", "categories", "déchets"],
    "plastic": ["plastic", "plastiki", "plastique", "bottle", "chupa"],
    "paper": ["paper", "karatasi", "papier", "cardboard", "carton"],
    "glass": ["glass", "kioo", "verre"],
    "metal": ["metal", "chuma", "scrap", "aluminium", "shaba", "métal"],
    "organic": ["organic", "kikolojia", "chakula", "food", "compost", "organique"],
    "ewaste": ["e-waste", "ewaste", "electronic", "electronics", "battery", "betri"],
    "textile": ["textile", "nguo", "cloth", "clothes", "vêtement"],
    "buyer": ["buyer", "buyers", "mnunuzi", "wananunua", "acheteur", "sell", "uza"],
    "register": ["register", "jisajili", "signup", "inscription", "business", "biashara"],
    "safety": ["safe", "safety", "usalama", "hatari", "danger", "sécurité"],
    "privacy": ["privacy", "faragha", "permission", "ruhusa", "confidentialité"],
    "another_photo": ["another photo", "take another", "picha nyingine", "piga tena", "autre photo", "nouvelle photo"],
    "accuracy": ["accurate", "accuracy", "100%", "uhakika", "sahihi", "précision", "fiable"],
    "price": ["price", "bei", "gharama", "cost", "sell for", "prix", "coût"],
    "error": ["error", "haifunguki", "imekataa", "fail", "failed", "cannot", "tatizo", "erreur", "ne marche"],
    "authority": ["authority", "mamlaka", "municipal", "halmashauri", "health department", "environnement"],
    "compost": ["compost", "komposti", "mbolea", "composter"],
    "hazardous": ["hazard", "hatari", "dangerous", "chemical", "kemikali", "needle", "sindano", "asbestos", "dangereux"],
    "recycle": ["recycle", "recycling", "recycl", "kurecycle", "recyclage"],
    "help": ["help", "msaada", "what can you", "naweza", "aide", "comment"],
}


def get_chat_reply(message, lang="sw"):
    language = lang if lang in ANSWERS else "sw"
    text = " ".join((message or "").lower().split())
    if not text:
        return ANSWERS[language]["help"]
    priority_intents = (
        "another_photo", "accuracy", "price", "error", "authority",
        "compost", "hazardous",
    )
    for intent in priority_intents:
        if any(word in text for word in KEYWORDS[intent]):
            return ANSWERS[language][intent]
    matches = []
    for intent, words in KEYWORDS.items():
        score = max((len(word) for word in words if word in text), default=0)
        if score:
            matches.append((score, intent))
    if matches:
        for _, intent in sorted(matches, reverse=True):
            return ANSWERS[language][intent]
    extra = {
        "sw": "Tafadhali uliza swali moja kwa moja ili nikusaidie vizuri.",
        "en": "Please ask one specific question so I can help accurately.",
        "fr": "Posez une question précise pour que je puisse aider correctement.",
    }
    return ANSWERS[language]["help"] + " " + extra[language]
