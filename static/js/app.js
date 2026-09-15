var currentLang='sw',chatLang='sw',reportMap=null,buyerMap=null,reportMarker=null,buyerMarkers=[];
var T={sw:{nav_home:'Nyumbani',nav_report:'Ripoti',nav_identify:'Tambua',nav_buyers:'Wananunua',nav_register:'Jisajili',hero_title:'🌍 TakaSmart – Usimamizi wa Taka kwa Ufasaha',hero_desc:'Connect raia, mamlaka, na wananunua wa taka. Ripoti uchafu, tambua aina ya taka, na pata wananunua karibu nawe.',hero_report:'Ripoti Uchafu',hero_identify:'Tambua Taka',hero_buyers:'Tafuta Wananunua',stat_reports:'Ripoti Zilizowasilishwa',stat_resolved:'Zimeitatuliwa',stat_buyers:'Wananunua Waliosajiliwa',stat_recycled:'Taka Zilizorecycle',report_title:'Ripoti Eneo Lenye Uchafu',report_desc:'Piga picha eneo lenye uchafu na tuma ripoti kwa mamlaka husika.',report_photo_title:'Piga Picha',report_upload_hint:'Bofya hapa kuchukua picha',report_location_label:'📍 Mahali',report_desc_label:'📝 Maelezo',report_authority_label:'🏛️ Mamlaka Husika',report_submit:'Tuma Ripoti',report_map_title:'Eneo kwenye Map',report_recent:'Ripoti za Hivi Karibuni',identify_title:'Tambua Taka na Jinsi ya Kurecycle',identify_desc:'Piga picha ya taka na mfumo utambue aina yake.',identify_photo_title:'Piga Picha ya Taka',identify_upload_hint:'Bofya hapa kupiga picha ya taka',identify_recycle_title:'Njia za Kurecycle',identify_recycle_hint:'Piga picha ya taka kwanza',buyers_title:'Tafuta Wananunua wa Taka',buyers_desc:'Tafuta wananunua wa taka karibu nawe.',register_title:'Jisajili kama Mnunuzi wa Taka',register_desc:'Wewe ni mnunuzi wa taka? Jisajili hapa.',register_form_title:'Fomu ya Usajili'},en:{nav_home:'Home',nav_report:'Report',nav_identify:'Identify',nav_buyers:'Buyers',nav_register:'Register',hero_title:'🌍 TakaSmart – Smart Waste Management',hero_desc:'Connect citizens, authorities, and waste buyers. Report waste, identify waste type, and find buyers near you.',hero_report:'Report Waste',hero_identify:'Identify Waste',hero_buyers:'Find Buyers',stat_reports:'Reports Submitted',stat_resolved:'Resolved',stat_buyers:'Registered Buyers',stat_recycled:'Waste Recycled',report_title:'Report a Waste Area',report_desc:'Take a photo of a waste area and submit to the relevant authority.',report_photo_title:'Take Photo',report_upload_hint:'Click here to take a photo',report_location_label:'📍 Location',report_desc_label:'📝 Description',report_authority_label:'🏛️ Relevant Authority',report_submit:'Submit Report',report_map_title:'Location on Map',report_recent:'Recent Reports',identify_title:'Identify Waste & How to Recycle',identify_desc:'Take a photo of waste and the system will identify its type.',identify_photo_title:'Take Photo of Waste',identify_upload_hint:'Click here to take a photo of waste',identify_recycle_title:'Recycling Methods',identify_recycle_hint:'Take a photo of waste first',buyers_title:'Find Waste Buyers',buyers_desc:'Find waste buyers near you.',register_title:'Register as a Waste Buyer',register_desc:'Are you a waste buyer? Register here.',register_form_title:'Registration Form'},fr:{nav_home:'Accueil',nav_report:'Signaler',nav_identify:'Identifier',nav_buyers:'Acheteurs',nav_register:"S'inscrire",hero_title:'🌍 TakaSmart – Gestion Intelligente des Déchets',hero_desc:'Connectez citoyens, autorités et acheteurs de déchets.',hero_report:'Signaler',hero_identify:'Identifier',hero_buyers:'Acheteurs',stat_reports:'Signalements',stat_resolved:'Résolus',stat_buyers:'Acheteurs Inscrits',stat_recycled:'Déchets Recyclés',report_title:'Signaler une Zone de Déchets',report_desc:"Prenez une photo d'une zone de déchets.",report_photo_title:'Prendre Photo',report_upload_hint:'Cliquez ici pour prendre une photo',report_location_label:'📍 Emplacement',report_desc_label:'📝 Description',report_authority_label:'🏛️ Autorité',report_submit:'Envoyer',report_map_title:'Carte',report_recent:'Signalements Récents',identify_title:'Identifier les Déchets & Recyclage',identify_desc:"Prenez une photo et le système identifiera le type.",identify_photo_title:'Photo des Déchets',identify_upload_hint:'Cliquez ici pour photographier',identify_recycle_title:'Méthodes de Recyclage',identify_recycle_hint:"Prenez d'abord une photo",buyers_title:'Trouver des Acheteurs',buyers_desc:'Trouvez des acheteurs près de chez vous.',register_title:"S'inscrire comme Acheteur",register_desc:"Inscrivez-vous ici.",register_form_title:"Formulaire d'Inscription"}};
function t(k){return(T[currentLang]&&T[currentLang][k])||T.sw[k]||k}
function changeLang(l){currentLang=l;document.querySelectorAll('[data-i18n]').forEach(function(e){e.textContent=t(e.getAttribute('data-i18n'))})}
function showSection(n){document.getElementById('section-home').style.display=n==='home'?'':'none';document.querySelectorAll('.section').forEach(function(s){s.classList.remove('active')});var sec=document.getElementById('section-'+n);if(sec)sec.classList.add('active');document.querySelectorAll('.nav-links button').forEach(function(b){b.classList.remove('active')});var nb=document.getElementById('nav-'+n);if(nb)nb.classList.add('active');if(n==='report'&&!reportMap)setTimeout(initReportMap,200);if(n==='buyers'&&!buyerMap)setTimeout(initBuyerMap,200);if(n==='buyers')setTimeout(renderBuyers,400);window.scrollTo({top:n==='home'?0:200,behavior:'smooth'});}
function initReportMap(){reportMap=L.map('reportMap').setView([-6.7924,39.2083],12);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'&copy; OSM'}).addTo(reportMap);reportMap.on('click',function(e){if(reportMarker)reportMap.removeLayer(reportMarker);reportMarker=L.marker(e.latlng,{icon:L.divIcon({className:'',html:'<div style="font-size:2rem;color:#C62828"><i class="fas fa-map-marker-alt"></i></div>',iconSize:[30,30],iconAnchor:[15,30]})}).addTo(reportMap);document.getElementById('reportLocation').value=e.latlng.lat.toFixed(4)+', '+e.latlng.lng.toFixed(4);document.getElementById('reportLocInfo').classList.add('show');document.getElementById('reportLocText').textContent='Lat: '+e.latlng.lat.toFixed(4)+', Lng: '+e.latlng.lng.toFixed(4);});if(navigator.geolocation)navigator.geolocation.getCurrentPosition(function(p){reportMap.setView([p.coords.latitude,p.coords.longitude],14)});setTimeout(function(){reportMap.invalidateSize()},500);}
function initBuyerMap(){buyerMap=L.map('buyerMap').setView([-6.7924,39.2083],12);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'&copy; OSM'}).addTo(buyerMap);if(navigator.geolocation)navigator.geolocation.getCurrentPosition(function(p){buyerMap.setView([p.coords.latitude,p.coords.longitude],13)});setTimeout(function(){buyerMap.invalidateSize()},500);}
function handleReportPhoto(input){if(input.files&&input.files[0]){var r=new FileReader();r.onload=function(e){document.getElementById('reportPreview').src=e.target.result;document.getElementById('reportPreview').classList.add('show');document.getElementById('reportUploadArea').style.display='none';if(navigator.geolocation)navigator.geolocation.getCurrentPosition(function(p){if(reportMap){reportMap.setView([p.coords.latitude,p.coords.longitude],15);if(reportMarker)reportMap.removeLayer(reportMarker);reportMarker=L.marker([p.coords.latitude,p.coords.longitude],{icon:L.divIcon({className:'',html:'<div style="font-size:2rem;color:#C62828"><i class="fas fa-map-marker-alt"></i></div>',iconSize:[30,30],iconAnchor:[15,30]})}).addTo(reportMap);document.getElementById('reportLocation').value=p.coords.latitude.toFixed(4)+', '+p.coords.longitude.toFixed(4);document.getElementById('reportLocInfo').classList.add('show');document.getElementById('reportLocText').textContent='Lat: '+p.coords.latitude.toFixed(4)+', Lng: '+p.coords.longitude.toFixed(4);}});};r.readAsDataURL(input.files[0]);}}
function submitReport(){var desc=document.getElementById('reportDesc').value;var auth=document.getElementById('reportAuthority').value;var loc=document.getElementById('reportLocation').value;if(!desc||!auth){showToast('⚠️ Tafadhali jaza maelezo na chagua mamlaka','warning');return}showToast('✅ Ripoti imetumwa kwa mamlaka husika!','success');var d=document.getElementById('recentReports');var now=new Date();var st=currentLang==='en'?'Pending':currentLang==='fr'?'En attente':'Inasubiri';d.insertAdjacentHTML('afterbegin','<div class="report-item"><div class="report-img"><i class="fas fa-camera"></i></div><div class="report-details"><h4>'+desc.substring(0,50)+'</h4><p>📍 '+loc+'</p></div><span class="report-status status-pending">'+st+'</span></div>');var s=document.getElementById('statReports');s.textContent=(parseInt(s.textContent.replace(/,/g,''))+1).toLocaleString();document.getElementById('reportDesc').value='';document.getElementById('reportAuthority').value='';document.getElementById('reportPreview').classList.remove('show');document.getElementById('reportUploadArea').style.display='';}
var wasteDB=[{type:'Plastiki',typeEn:'Plastic',typeFr:'Plastique',badge:'badge-plastic',icon:'🧴',desc:{sw:'Hii ni taka ya plastiki. Plastiki inaweza kuchukua miaka 100+ kuoza.',en:'This is plastic waste. Plastic can take 100+ years to decompose.',fr:'Ceci est un déchet plastique.'},steps:{sw:['Safisha chupa - ondoa mabaki ya chakula','Tenganisha kwa aina: PET, HDPE, PVC','Bana/kunja ili kupunguza ukubwa','Peleka kwenye kituo cha kukusanya plastiki','Au uuze kwa wananunua kwenye platform'],en:['Clean bottles - remove food residue','Separate by type: PET, HDPE, PVC','Crush to reduce size','Take to a plastic collection center','Or sell to plastic buyers on the platform'],fr:['Nettoyez les bouteilles','Séparez par type: PET, HDPE, PVC','Écrasez pour réduire la taille','Apportez à un centre de collecte','Ou vendez aux acheteurs']}},{type:'Karatasi',typeEn:'Paper',typeFr:'Papier',badge:'badge-paper',icon:'📦',desc:{sw:'Hii ni taka ya karatasi. Karatasi inaweza kurecyclewa hadi mara 5-7.',en:'This is paper waste. Paper can be recycled 5-7 times.',fr:'Ceci est un déchet papier.'},steps:{sw:['Tenganisha karatasi kutoka kwa taka nyingine','Ondoa karatasi zenye mafuta/chemikali','Bana karatasi ili kurahisisha usafirishaji','Pekeleke kwenye kituo cha kukusanya karatasi','Karatasi nzito na kadibodi zina thamani zaidi'],en:['Separate paper from other waste','Remove oily/chemical paper','Flatten paper for easy transport','Take to paper collection center','Heavy paper and cardboard have more value'],fr:['Séparez le papier','Retirez le papier huileux','Aplatissez le papier','Apportez à un centre de collecte','Le papier épais a plus de valeur']}},{type:'Kioo',typeEn:'Glass',typeFr:'Verre',badge:'badge-glass',icon:'🍶',desc:{sw:'Hii ni taka ya kioo. Kioo kinaweza kurecyclewa bila kupoteza ubora.',en:'This is glass waste. Glass can be recycled without losing quality.',fr:'Ceci est un déchet de verre.'},steps:{sw:['Kaa kwa usalama - kioo kinaweza kukatiza','Tenganisha kwa rangi','Ondoa matope na mabaki','Usichanganye kioo na aina nyingine za taka','Pekeleke kwenye kituo cha kukusanya kioo'],en:['Handle safely - glass can cut','Separate by color','Remove dirt and residue','Do not mix glass with other waste','Take to glass collection center'],fr:['Manipulez avec précaution','Séparez par couleur','Retirez la saleté','Ne mélangez pas','Apportez à un centre de collecte']}},{type:'Chuma',typeEn:'Metal',typeFr:'Métal',badge:'badge-metal',icon:'🔩',desc:{sw:'Hii ni taka ya chuma. Chuma cha aluminium kinaweza kurecyclewa ndani ya wiki 2.',en:'This is metal waste. Aluminium can be recycled within 2 weeks.',fr:'Ceci est un déchet métallique.'},steps:{sw:['Tenganisha chuma tofauti: felesi, aluminium, shaba','Ondoa vifaa visivyo cha chuma','Safisha chuma cha kutu','Bana/kunja chuma ili kupunguza ukubwa','Uza kwa wananunua wa chuma - ina thamani kubwa'],en:['Separate different metals','Remove non-metal parts','Clean rusty metal','Crush to reduce size','Sell to metal buyers - high value'],fr:['Séparez les métaux','Retirez les parties non métalliques','Nettoyez le métal rouillé','Écrasez','Vendez aux acheteurs']}},{type:'Kikolojia',typeEn:'Organic',typeFr:'Organique',badge:'badge-organic',icon:'🍂',desc:{sw:'Hii ni taka ya kikolojia. Inaweza kutumika kutengeneza mbolea ya komposti.',en:'This is organic waste. It can be used to make compost.',fr:'Ceci est un déchet organique.'},steps:{sw:['Tenganisha taka za kikolojia kutoka kwa taka nyingine','Tia kwenye mashimo ya komposti','Changanya na majani na udongo','Geuza mara kwa mara kwa hewa','Baada ya miezi 2-3 utapata mbolea nzuri'],en:['Separate organic waste','Put in compost pit','Mix with leaves and soil','Turn regularly','After 2-3 months you get good fertilizer'],fr:['Séparez les déchets organiques','Mettez dans une fosse à compost','Mélangez avec des feuilles','Retournez régulièrement','Après 2-3 mois: bon engrais']}},{type:'E-Waste',typeEn:'E-Waste',typeFr:'Déchets électroniques',badge:'badge-ewaste',icon:'💻',desc:{sw:'Hii ni taka ya elektroniki. E-waste ina metali zenye thamani lakini ni hatari.',en:'This is electronic waste. Contains valuable metals but is hazardous.',fr:'Ceci est un déchet électronique.'},steps:{sw:['Usituachie e-waste kwenye mazingira - ni hatari!','Toa bateri na vifaa vya hatari kwa usalama','Tenganisha vifaa kwa aina','Peleke kwenye kituo cha e-waste kilichoidhinishwa','Au uuze kwa wananunua wa e-waste waliosajiliwa'],en:['Do not dump e-waste - hazardous!','Remove batteries safely','Separate devices by type','Take to certified e-waste center','Sell to registered e-waste buyers'],fr:['Ne jetez pas!','Retirez les batteries','Séparez par type','Apportez à un centre certifié','Vendez aux acheteurs certifiés']}},{type:'Vazi/Nguo',typeEn:'Textile',typeFr:'Textile',badge:'badge-textile',icon:'👕',desc:{sw:'Hii ni taka ya nguo. Nguo za zamani zinaweza kutumika tena au kurecyclewa.',en:'This is textile waste. Old clothes can be reused or recycled.',fr:'Ceci est un déchet textile.'},steps:{sw:['Tenganisha nguo zenye kufaa na zilizochakaa','Zile zenye kufaa: zawadi kwa misada au uze','Zilizochakaa: weka kwa vitengo vya uchakavu','Baadhi ya nguo zinaweza kutumika kama mbolea','Nguo za pamba ni rahisi kurecyclewa zaidi'],en:['Separate wearable and worn-out clothes','Wearable: donate or sell','Worn-out: textile recycling','Some fabrics can be composted','Cotton is easiest to recycle'],fr:['Séparez les vêtements portables et usés','Portables: donnez ou vendez','Usés: recyclage textile','Certains tissus: compost','Le coton est le plus facile à recycler']}}];
function handleIdentifyPhoto(input){if(input.files&&input.files[0]){var r=new FileReader();r.onload=function(e){document.getElementById('identifyPreview').src=e.target.result;document.getElementById('identifyPreview').classList.add('show');document.getElementById('identifyUploadArea').style.display='none';simulateIdentify();};r.readAsDataURL(input.files[0]);}}
function simulateIdentify(){var lang=currentLang;var w=wasteDB[Math.floor(Math.random()*wasteDB.length)];var tn=lang==='en'?w.typeEn:lang==='fr'?w.typeFr:w.type;var ds=w.desc[lang]||w.desc.sw;var st=w.steps[lang]||w.steps.sw;var rl=lang==='en'?'Recycling Steps':lang==='fr'?'Étapes de Recyclage':'Hatua za Kurecycle';var fl=lang==='en'?'Find Buyers for This Waste':lang==='fr'?'Trouver des Acheteurs':'Tafuta Wananunua wa Taka Hii';var stepsHTML=st.map(function(s,i){return '<div class="step"><div class="step-num">'+(i+1)+'</div><div class="step-text">'+s+'</div></div>'}).join('');document.getElementById('aiResult').innerHTML='<h4><i class="fas fa-robot"></i> AI Imetambua:</h4><p style="margin-bottom:12px">'+ds+'</p><div style="margin-bottom:12px"><span class="waste-type-badge '+w.badge+'">'+w.icon+' '+tn+'</span></div><div class="recycle-steps"><h4 style="color:var(--primary-dark);margin-bottom:10px"><i class="fas fa-recycle"></i> '+rl+':</h4>'+stepsHTML+'</div><button class="btn btn-primary" style="margin-top:16px;width:100%" onclick="showSection(\'buyers\')"><i class="fas fa-store"></i> '+fl+'</button>';document.getElementById('aiResult').classList.add('show');document.getElementById('recycleGuide').innerHTML='<div style="margin-bottom:16px"><span class="waste-type-badge '+w.badge+'" style="font-size:1rem;padding:8px 20px">'+w.icon+' '+tn+'</span></div>'+stepsHTML;document.getElementById('recycleGuide').style.display='block';document.getElementById('recycleGuidePlaceholder').style.display='none';showToast('🔍 Aina ya taka imetambuliwa!','info');}
var buyersData=[{name:'GreenRecycle Ltd',location:'Dar es Salaam, Kariakoo',types:['plastic','paper'],lat:-6.828,lng:39.280,phone:'+255 712 345 678'},{name:'MetalWorks TZ',location:'Dar es Salaam, Ubungo',types:['metal','ewaste'],lat:-6.780,lng:39.265,phone:'+255 713 456 789'},{name:'EcoGlass Tanzania',location:'Dar es Salaam, Kinondoni',types:['glass'],lat:-6.800,lng:39.240,phone:'+255 714 567 890'},{name:'OrganicPlus',location:'Dar es Salaam, Temeke',types:['organic'],lat:-6.850,lng:39.290,phone:'+255 715 678 901'},{name:'TakaBora',location:'Dar es Salaam, Ilala',types:['plastic','metal','paper'],lat:-6.815,lng:39.270,phone:'+255 716 789 012'},{name:'TextileRevive',location:'Dar es Salaam, Mwananyamala',types:['textile'],lat:-6.790,lng:39.255,phone:'+255 717 890 123'},{name:'E-Waste Solutions',location:'Dar es Salaam, Mikocheni',types:['ewaste'],lat:-6.770,lng:39.245,phone:'+255 718 901 234'},{name:'PlastiKwanza',location:'Dar es Salaam, Mbagala',types:['plastic'],lat:-6.860,lng:39.270,phone:'+255 719 012 345'},{name:'PaperTrail TZ',location:'Dar es Salaam, Upanga',types:['paper','textile'],lat:-6.810,lng:39.260,phone:'+255 720 123 456'},{name:'ScrapMasters',location:'Dar es Salaam, Buguruni',types:['metal'],lat:-6.840,lng:39.275,phone:'+255 721 234 567'}];
function renderBuyers(){var tf=document.getElementById('buyerTypeFilter').value;var sf=(document.getElementById('buyerSearch').value||'').toLowerCase();var f=buyersData;if(tf!=='all')f=f.filter(function(b){return b.types.indexOf(tf)!==-1});if(sf)f=f.filter(function(b){return b.name.toLowerCase().indexOf(sf)!==-1||b.location.toLowerCase().indexOf(sf)!==-1});buyerMarkers.forEach(function(m){if(buyerMap)buyerMap.removeLayer(m)});buyerMarkers=[];var list=document.getElementById('buyersList');list.innerHTML='';if(!f.length){list.innerHTML='<div style="text-align:center;padding:40px;color:var(--text-light)"><i class="fas fa-search" style="font-size:2rem;margin-bottom:10px;display:block"></i><p>Hakuna wananunua walioapatikana</p></div>';return}var tl={plastic:{sw:'Plastiki',en:'Plastic',fr:'Plastique'},paper:{sw:'Karatasi',en:'Paper',fr:'Papier'},glass:{sw:'Kioo',en:'Glass',fr:'Verre'},metal:{sw:'Chuma',en:'Metal',fr:'Métal'},organic:{sw:'Kikolojia',en:'Organic',fr:'Organique'},ewaste:{sw:'E-Waste',en:'E-Waste',fr:'Électronique'},textile:{sw:'Vazi/Nguo',en:'Textile',fr:'Textile'}};var cl=currentLang==='en'?'Contact':currentLang==='fr'?'Contacter':'Wasiliana';f.forEach(function(b){if(buyerMap){var mk=L.marker([b.lat,b.lng],{icon:L.divIcon({className:'',html:'<div style="background:#2E7D32;color:#fff;border-radius:50%;width:32px;height:32px;display:flex;align-items:center;justify-content:center;font-size:.8rem;font-weight:800;box-shadow:0 2px 8px rgba(0,0,0,.3);border:2px solid #fff"><i class="fas fa-store"></i></div>',iconSize:[32,32],iconAnchor:[16,16]})}).addTo(buyerMap).bindPopup('<b>'+b.name+'</b><br>'+b.location);buyerMarkers.push(mk);}var ts=b.types.map(function(t){return '<span>'+(tl[t]&&tl[t][currentLang]||tl[t]&&tl[t].sw||t)+'</span>'}).join('');list.innerHTML+='<div class="buyer-card"><div class="buyer-avatar"><i class="fas fa-store"></i></div><div class="buyer-info"><h4>'+b.name+'</h4><p>📍 '+b.location+' &bull; 📞 '+b.phone+'</p><div class="buyer-types">'+ts+'</div></div><button class="buyer-contact-btn" onclick="contactBuyer(\''+b.name+'\')"><i class="fas fa-phone"></i> '+cl+'</button></div>';});}
function filterBuyers(){if(!buyerMap){initBuyerMap();setTimeout(renderBuyers,500);return}renderBuyers()}
function contactBuyer(n){showToast('📞 Unawasiliana na '+n+'...','info')}
function submitRegistration(){var n=document.getElementById('regName').value;var e=document.getElementById('regEmail').value;var p=document.getElementById('regPhone').value;if(!n||!e||!p){showToast('⚠️ Tafadhali jaza fomu kikamilifu','warning');return}document.getElementById('regFormCard').style.display='none';document.getElementById('regSuccess').classList.add('show');showToast('✅ Usajili umefanikiwa!','success');var s=document.getElementById('statBuyers');s.textContent=parseInt(s.textContent)+1;}
var CR={sw:{welcome:'Jambo! 👋 Mimi ni TakaSmart Assistant. Niko hapa kukusaidia kuhusu usimamizi wa taka. 🌿',qs:['Jinsi ya kurecycle plastiki?','Aina za taka ni zipi?','Ninapataje mnunuzi?','Jinsi ya kutumia platform?'],r:{plastik:'🧴 <b>Kuhusu Plastiki:</b><br><br>1. <b>Tenganisha</b> plastiki kwa aina: PET, HDPE, PVC<br>2. <b>Safisha</b> kabla ya kurecycle<br>3. <b>Bana</b> chupa ili kupunguza ukubwa<br>4. <b>Pekeleke</b> kwenye kituo cha kukusanya plastiki<br>5. <b>Uze</b> kwa wananunua kwenye "Wananunua"<br><br>💡 PET ina thamani zaidi!',recycle:'♻️ <b>Jinsi ya Kurecycle:</b><br><br>1. <b>Tambua</b> aina ya taka<br>2. <b>Tenganisha</b> taka kwa aina zao<br>3. <b>Safisha</b> taka kabla ya kurecycle<br>4. <b>Pata mnunuzi</b> kwenye "Wananunua"<br>5. <b>Au peleke</b> kwenye kituo cha kukusanya taka<br><br>🌍 Kila mtu anaweza kuchangia!',aina:'📋 <b>Aina za Taka:</b><br><br>1. 🧴 <b>Plastiki</b> - Chupa, mifuko, vyungu<br>2. 📦 <b>Karatasi</b> - Sanduku, gazeti<br>3. 🍶 <b>Kioo</b> - Chupa, dirisha<br>4. 🔩 <b>Chuma</b> - Felesi, aluminium, shaba<br>5. 🍂 <b>Kikolojia</b> - Mabaki ya chakula<br>6. 💻 <b>E-Waste</b> - Simu, kompyuta, TV<br>7. 👕 <b>Vazi/Nguo</b> - Nguo za zamani',mnunuzi:'🏪 <b>Kupata Mnunuzi:</b><br><br>1. Nenda kwenye <b>"Wananunua"</b><br>2. <b>Chagua</b> aina ya taka unayotaka kuuza<br>3. <b>Tafuta</b> wananunua karibu na eneo lako<br>4. <b>Wasiliana</b> na mnunuzi moja kwa moja<br>5. <b>Kubaliana</b> kwenye bei na usafirishaji',platform:'📱 <b>Jinsi ya Kutumia Platform:</b><br><br>🔧 <b>Ripoti Uchafu</b> - Piga picha na tuma kwa mamlaka<br>🔍 <b>Tambua Taka</b> - Piga picha na jua aina ya taka<br>🏪 <b>Wananunua</b> - Tafuta na uwasiliane na wananunua<br>📝 <b>Jisajili</b> - Jiunge kama mnunuzi<br>💬 <b>Chat</b> - Niulize maswali yoyete!<br><br>🌍 TakaSmart inaunganisha raia, mamlaka, na wananunua!',uchafu:'🚯 <b>Kuhusu Uchafu:</b><br><br>1. <b>Ripoti</b> eneo lenye uchafu<br>2. <b>Tambua</b> aina ya uchafu<br>3. <b>Pata wananunua</b> wa taka hiyo<br>4. <b>Shiriki</b> na jirani zako',mazingira:'🌍 <b>Kuhusu Mazingira:</b><br><br>- Plastiki inachukua miaka 100+ kuoza<br>- Kioo kinaweza kurecyclewa bila kikomo<br>- Aluminium kinaweza kurecyclewa ndani ya wiki 2<br>- Taka za kikolojia zinaweza kuwa mbolea',komposti:'🍂 <b>Kuhusu Komposti:</b><br><br>1. Kusanya mabaki ya chakula na majani<br>2. Tia kwenye shimoni au chombo<br>3. Changanya na majani kavu na udongo<br>4. Geuza mara kwa mara<br>5. Baada ya miezi 2-3 utapata mbolea!',default:'🤔 Asante kwa swali lako! Jaribu kuuliza kuhusu: plastiki, recycle, aina za taka, mnunuzi, au jinsi ya kutumia platform.'}},en:{welcome:'Hello! 👋 I am TakaSmart Assistant. I can help you with waste management. 🌿',qs:['How to recycle plastic?','What are the waste types?','How to find a buyer?','How to use the platform?'],r:{plast:'🧴 <b>About Plastic:</b><br><br>1. <b>Separate</b> by type: PET, HDPE, PVC<br>2. <b>Clean</b> before recycling<br>3. <b>Crush</b> bottles to reduce size<br>4. <b>Take</b> to a collection center<br>5. <b>Sell</b> to buyers on the platform<br><br>💡 PET has the most recycling value!',recycle:'♻️ <b>How to Recycle:</b><br><br>1. <b>Identify</b> waste type<br>2. <b>Separate</b> waste by type<br>3. <b>Clean</b> waste before recycling<br>4. <b>Find buyers</b> in "Buyers" section<br>5. <b>Or take</b> to a collection center',type:'📋 <b>Waste Types:</b><br><br>1. 🧴 <b>Plastic</b> - Bottles, bags<br>2. 📦 <b>Paper</b> - Boxes, cardboard<br>3. 🍶 <b>Glass</b> - Bottles, windows<br>4. 🔩 <b>Metal</b> - Iron, aluminium, copper<br>5. 🍂 <b>Organic</b> - Food scraps, leaves<br>6. 💻 <b>E-Waste</b> - Phones, computers, TVs<br>7. 👕 <b>Textile</b> - Old clothes',buyer:'🏪 <b>Finding a Buyer:</b><br><br>1. Go to <b>"Buyers"</b> section<br>2. <b>Select</b> waste type<br>3. <b>Search</b> for buyers near you<br>4. <b>Contact</b> the buyer directly<br>5. <b>Agree</b> on price and pickup',platform:'📱 <b>How to Use the Platform:</b><br><br>🔧 <b>Report Waste</b> - Photo and send to authorities<br>🔍 <b>Identify Waste</b> - Photo and learn waste type<br>🏪 <b>Buyers</b> - Find and contact waste buyers<br>📝 <b>Register</b> - Join as a waste buyer<br>💬 <b>Chat</b> - Ask me any questions!',waste:'🚯 <b>About Waste:</b><br><br>1. <b>Report</b> waste areas<br>2. <b>Identify</b> waste type<br>3. <b>Find buyers</b> for that waste<br>4. <b>Share</b> with neighbors',compost:'🍂 <b>About Composting:</b><br><br>1. Collect food scraps and leaves<br>2. Put in a compost bin<br>3. Mix with dry leaves and soil<br>4. Turn regularly<br>5. After 2-3 months: natural fertilizer!',default:'🤔 Thanks for your question! Try asking about: plastic, recycling, waste types, buyers, or how to use the platform.'}},fr:{welcome:"Bonjour! 👋 Je suis l'assistant TakaSmart. 🌿",qs:['Comment recycler le plastique?','Types de déchets?','Comment trouver un acheteur?','Comment utiliser la plateforme?'],r:{plast:"🧴 <b>Plastique:</b><br><br>1. <b>Séparez</b> par type: PET, HDPE, PVC<br>2. <b>Nettoyez</b> avant recyclage<br>3. <b>Écrasez</b> les bouteilles<br>4. <b>Apportez</b> à un centre de collecte<br>5. <b>Vendez</b> aux acheteurs",recycl:"♻️ <b>Comment Recycler:</b><br><br>1. <b>Identifiez</b> le type de déchets<br>2. <b>Séparez</b> par type<br>3. <b>Nettoyez</b> avant recyclage<br>4. <b>Trouvez</b> des acheteurs<br>5. <b>Ou apportez</b> à un centre de collecte",type:"📋 <b>Types de Déchets:</b><br><br>1. 🧴 <b>Plastique</b><br>2. 📦 <b>Papier</b><br>3. 🍶 <b>Verre</b><br>4. 🔩 <b>Métal</b><br>5. 🍂 <b>Organique</b><br>6. 💻 <b>Électronique</b><br>7. 👕 <b>Textile</b>",acheteur:"🏪 <b>Trouver un Acheteur:</b><br><br>1. Allez à <b>\"Acheteurs\"</b><br>2. <b>Sélectionnez</b> le type de déchets<br>3. <b>Recherchez</b> des acheteurs proches<br>4. <b>Contactez</b> l'acheteur<br>5. <b>Convenez</b> du prix",plateforme:"📱 <b>Utiliser la Plateforme:</b><br><br>🔧 <b>Signaler</b> - Photo et envoyez<br>🔍 <b>Identifier</b> - Photo des déchets<br>🏪 <b>Acheteurs</b> - Trouvez des acheteurs<br>📝 <b>S'inscrire</b> - Devenez acheteur<br>💬 <b>Chat</b> - Posez des questions!",default:"🤔 Merci! Essayez de demander sur: plastique, recyclage, types de déchets, acheteurs."}}};
function setChatLang(l,btn){chatLang=l;document.querySelectorAll('.chat-lang-bar button').forEach(function(b){b.classList.remove('active')});if(btn)btn.classList.add('active');document.getElementById('chatMessages').innerHTML='';addBotMsg(CR[chatLang].welcome);renderQQ();}
function toggleChat(){var w=document.getElementById('chatWindow');w.classList.toggle('open');var b=document.getElementById('chatToggle');var bd=b.querySelector('.badge');if(bd)bd.remove();if(w.classList.contains('open')&&!document.getElementById('chatMessages').children.length){addBotMsg(CR[chatLang].welcome);renderQQ();}}
function renderQQ(){var qs=CR[chatLang].qs||[];var c=document.getElementById('quickQuestions');c.innerHTML=qs.map(function(q){return '<button onclick="sendQQ(\''+q.replace(/'/g,"\\'")+'\')">'+q+'</button>'}).join('');}
function addBotMsg(txt){var m=document.getElementById('chatMessages');var d=document.createElement('div');d.className='msg msg-bot';d.innerHTML='<div class="bot-icon"><i class="fas fa-robot"></i> TakaSmart</div><div>'+txt+'</div>';m.appendChild(d);m.scrollTop=m.scrollHeight;}
function addUserMsg(txt){var m=document.getElementById('chatMessages');var d=document.createElement('div');d.className='msg msg-user';d.textContent=txt;m.appendChild(d);m.scrollTop=m.scrollHeight;}
function processChat(input){var txt=input.toLowerCase();var rs=CR[chatLang].r;var matched=false;for(var k in rs){if(k!=='default'&&txt.indexOf(k)!==-1){addBotMsg(rs[k]);matched=true;break;}}if(!matched)addBotMsg(rs.default||'🤔...');}
function sendChat(){var inp=document.getElementById('chatInput');var txt=inp.value.trim();if(!txt)return;addUserMsg(txt);inp.value='';var m=document.getElementById('chatMessages');var tp=document.createElement('div');tp.className='msg msg-bot';tp.id='typing';tp.innerHTML='<div class="bot-icon"><i class="fas fa-robot"></i> TakaSmart</div><div style="opacity:.6"><i class="fas fa-circle" style="font-size:.4rem;animation:blink 1s infinite"></i> <i class="fas fa-circle" style="font-size:.4rem;animation:blink 1s infinite .2s"></i> <i class="fas fa-circle" style="font-size:.4rem;animation:blink 1s infinite .4s"></i></div>';m.appendChild(tp);m.scrollTop=m.scrollHeight;setTimeout(function(){tp.remove();processChat(txt)},800);}
function sendQQ(q){document.getElementById('chatInput').value=q;sendChat();}
function showToast(msg,type){var t=document.getElementById('toast');t.className='toast show toast-'+type;t.innerHTML=msg;setTimeout(function(){t.classList.remove('show')},4000);}
document.addEventListener('DOMContentLoaded',function(){showSection('home')});

/* TakaSmart - Flask API integration */
const API = {
  reports: "/api/reports",
  buyers: "/api/buyers",
  identify: "/api/identify",
  chat: "/api/chat"
};

const cameraStreams = {};
const capturedPhotos = {};

async function apiJSON(url, options={}) {
  const response = await fetch(url, {...options, cache:"no-store"});
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(data.error || "Server error");
  return data;
}

function fileToFormData(input, extra={}) {
  const fd = new FormData();
  if (input && input.files && input.files[0]) fd.append("photo", input.files[0]);
  Object.entries(extra).forEach(([k,v]) => fd.append(k, v));
  return fd;
}

/* Submit a report to Flask/MySQL */
async function submitReport() {
  const desc = document.getElementById("reportDesc").value.trim();
  const auth = document.getElementById("reportAuthority").value;
  const loc = document.getElementById("reportLocation").value.trim();
  const lat = document.getElementById("reportLat").value;
  const lng = document.getElementById("reportLng").value;
  if (!desc || !auth || !capturedPhotos.report) {
    showToast("⚠️ Tafadhali jaza maelezo na chagua mamlaka", "warning");
    return;
  }

  try {
    const fd = new FormData();
    fd.append("photo", capturedPhotos.report, "camera-report.jpg");
    Object.entries({
      description: desc,
      authority: auth,
      location: loc || "Haijawekwa",
      lat,
      lng
    }).forEach(([key, value]) => fd.append(key, value));
    const result = await apiJSON(API.reports, {method:"POST", body:fd});
    showToast("✅ Ripoti imehifadhiwa kwenye mfumo!", "success");
    document.getElementById("reportDesc").value = "";
    document.getElementById("reportAuthority").value = "";
    document.getElementById("reportLocation").value = "";
    document.getElementById("reportLat").value = "";
    document.getElementById("reportLng").value = "";
    capturedPhotos.report = null;
    document.getElementById("reportPreview").classList.remove("show");
    document.getElementById("reportUploadArea").style.display = "";
    loadStats();
    loadRecentReports();
  } catch (err) {
    showToast("❌ " + err.message, "warning");
  }
}

/* Register buyer in MySQL */
async function submitRegistration() {
  const name = document.getElementById("regName").value.trim();
  const email = document.getElementById("regEmail").value.trim();
  const phone = document.getElementById("regPhone").value.trim();
  const location = document.getElementById("regLocation").value.trim();
  const lat = document.getElementById("regLat").value;
  const lng = document.getElementById("regLng").value;
  const description = document.getElementById("regDesc").value.trim();
  const types = [...document.querySelectorAll('#regFormCard input[type="checkbox"]:checked')]
    .map(x => x.value);

  if (!name || !email || !phone || !location || !types.length) {
    showToast("⚠️ Jaza fomu na chagua angalau aina moja ya taka.", "warning");
    return;
  }

  try {
    await apiJSON(API.buyers, {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({name,email,phone,location,description,types,lat,lng})
    });
    document.getElementById("regFormCard").style.display = "none";
    document.getElementById("regSuccess").classList.add("show");
    showToast("✅ Usajili umefanikiwa!", "success");
    loadStats();
  } catch (err) {
    showToast("❌ " + err.message, "warning");
  }
}

/* Real server-side waste classification endpoint.
   The starter backend uses safe demo classification; replace the classifier
   function later with a trained ML model if desired. */
async function identifyCapturedPhoto(blob) {
  const preview = document.getElementById("identifyPreview");
  preview.src = URL.createObjectURL(blob);
  preview.classList.add("show");
  document.getElementById("identifyUploadArea").style.display = "none";

  try {
    const fd = new FormData();
    fd.append("photo", blob, "camera-identify.jpg");
    const result = await apiJSON(API.identify, {method:"POST", body:fd});
    renderIdentifyResult(result);
  } catch (err) {
    showToast("❌ " + err.message, "warning");
  }
}

function renderIdentifyResult(result) {
  const w = result.waste;
  const lang = currentLang || "sw";
  const tn = lang === "en" ? w.typeEn : lang === "fr" ? w.typeFr : w.type;
  const ds = w.desc[lang] || w.desc.sw;
  const st = w.steps[lang] || w.steps.sw;
  const rl = lang === "en" ? "Recycling Steps" : lang === "fr" ? "Étapes de Recyclage" : "Hatua za Kurecycle";
  const fl = lang === "en" ? "Find Buyers for This Waste" : lang === "fr" ? "Trouver des Acheteurs" : "Tafuta Wananunua wa Taka Hii";
  const stepsHTML = st.map((s,i)=>`<div class="step"><div class="step-num">${i+1}</div><div class="step-text">${s}</div></div>`).join("");

  document.getElementById("aiResult").innerHTML =
    `<h4><i class="fas fa-robot"></i> ${result.demo ? "Mfumo Umetambua:" : "AI Imetambua:"}</h4>
     <p style="margin-bottom:12px">${ds}</p>
     <div style="margin-bottom:12px"><span class="waste-type-badge ${w.badge}">${w.icon} ${tn}</span></div>
     <div class="recycle-steps"><h4 style="color:var(--primary-dark);margin-bottom:10px"><i class="fas fa-recycle"></i> ${rl}:</h4>${stepsHTML}</div>
     <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px">
       <button class="btn btn-primary" style="flex:1" onclick="showSection('buyers')">
         <i class="fas fa-store"></i> ${fl}
       </button>
       <button class="btn btn-secondary" style="flex:1" onclick="takeAnotherIdentifyPhoto()">
         <i class="fas fa-camera-rotate"></i> ${currentLang === "en" ? "Take Another Photo" : currentLang === "fr" ? "Prendre une autre photo" : "Piga Picha Nyingine"}
       </button>
     </div>`;
  document.getElementById("aiResult").classList.add("show");

  document.getElementById("recycleGuide").innerHTML =
    `<div style="margin-bottom:16px"><span class="waste-type-badge ${w.badge}" style="font-size:1rem;padding:8px 20px">${w.icon} ${tn}</span></div>${stepsHTML}`;
  document.getElementById("recycleGuide").style.display = "block";
  document.getElementById("recycleGuidePlaceholder").style.display = "none";
  showToast("🔍 Aina ya taka imetambuliwa!", "info");
}

function takeAnotherIdentifyPhoto() {
  stopCamera("identify");
  capturedPhotos.identify = null;
  const preview = document.getElementById("identifyPreview");
  preview.removeAttribute("src");
  preview.classList.remove("show");
  document.getElementById("identifyUploadArea").style.display = "";
  document.getElementById("aiResult").innerHTML = "";
  document.getElementById("aiResult").classList.remove("show");
  document.getElementById("recycleGuide").innerHTML = "";
  document.getElementById("recycleGuide").style.display = "none";
  document.getElementById("recycleGuidePlaceholder").style.display = "";
  startCamera("identify");
}

/* Buyers */
async function loadBuyers() {
  const tf = document.getElementById("buyerTypeFilter").value;
  const sf = (document.getElementById("buyerSearch").value || "").trim();
  const params = new URLSearchParams();
  if (tf && tf !== "all") params.set("type", tf);
  if (sf) params.set("search", sf);

  try {
    const data = await apiJSON(API.buyers + "?" + params.toString());
    renderBuyersFromAPI(data.buyers || []);
  } catch (err) {
    showToast("❌ " + err.message, "warning");
  }
}

function renderBuyersFromAPI(f) {
  if (!buyerMap) initBuyerMap();
  buyerMarkers.forEach(m => buyerMap.removeLayer(m));
  buyerMarkers = [];
  const list = document.getElementById("buyersList");
  list.innerHTML = "";

  if (!f.length) {
    list.innerHTML = '<div style="text-align:center;padding:40px;color:var(--text-light)"><i class="fas fa-search" style="font-size:2rem;margin-bottom:10px;display:block"></i><p>Hakuna wananunua walioapatikana</p></div>';
    return;
  }

  const tl = {
    plastic:{sw:"Plastiki",en:"Plastic",fr:"Plastique"},
    paper:{sw:"Karatasi",en:"Paper",fr:"Papier"},
    glass:{sw:"Kioo",en:"Glass",fr:"Verre"},
    metal:{sw:"Chuma",en:"Metal",fr:"Métal"},
    organic:{sw:"Kikolojia",en:"Organic",fr:"Organique"},
    ewaste:{sw:"E-Waste",en:"E-Waste",fr:"Électronique"},
    textile:{sw:"Vazi/Nguo",en:"Textile",fr:"Textile"}
  };
  const cl = currentLang === "en" ? "Contact" : currentLang === "fr" ? "Contacter" : "Wasiliana";

  f.forEach(b => {
    if (b.lat != null && b.lng != null) {
      const mk = L.marker([b.lat,b.lng]).addTo(buyerMap)
        .bindPopup("<b>"+escapeHtml(b.name)+"</b><br>"+escapeHtml(b.location));
      buyerMarkers.push(mk);
    }
    const ts = (b.types || []).map(t => `<span>${(tl[t] && tl[t][currentLang]) || t}</span>`).join("");
    list.innerHTML += `
      <div class="buyer-card">
        <div class="buyer-avatar"><i class="fas fa-store"></i></div>
        <div class="buyer-info">
          <h4>${escapeHtml(b.name)}</h4>
          <p>📍 ${escapeHtml(b.location)} &bull; 📞 ${escapeHtml(b.phone)}</p>
          <div class="buyer-types">${ts}</div>
        </div>
        <button class="buyer-contact-btn" onclick="contactBuyer('${escapeJs(b.phone)}')">
          <i class="fas fa-phone"></i> ${cl}
        </button>
      </div>`;
  });
}

function filterBuyers() { loadBuyers(); }

function contactBuyer(phone) {
  window.location.href = "tel:" + phone;
}

function escapeHtml(v) {
  return String(v ?? "").replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
function escapeJs(v) {
  return String(v ?? "").replace(/\\/g,"\\\\").replace(/'/g,"\\'");
}

/* Dashboard stats/reports */
async function loadStats() {
  try {
    const s = await apiJSON("/api/stats");
    document.getElementById("statReports").textContent = Number(s.reports).toLocaleString();
    document.getElementById("statResolved").textContent = Number(s.resolved).toLocaleString();
    document.getElementById("statBuyers").textContent = Number(s.buyers).toLocaleString();
  } catch (_) {}
}

async function loadRecentReports() {
  try {
    const data = await apiJSON(API.reports);
    const d = document.getElementById("recentReports");
    d.innerHTML = "";
    (data.reports || []).slice(0,10).forEach(r => {
      d.innerHTML += `
      <div class="report-item">
        <div class="report-img">${r.photo ? `<img src="${r.photo}" alt="report">` : '<i class="fas fa-camera"></i>'}</div>
        <div class="report-details">
          <h4>${escapeHtml(r.description)}</h4>
          <p>📍 ${escapeHtml(r.location || "Haijawekwa")}</p>
        </div>
        <span class="report-status status-${r.status === "resolved" ? "resolved" : r.status === "in_progress" ? "progress" : "pending"}">
          ${r.status === "resolved" ? "Imetatuliwa" : r.status === "in_progress" ? "Inashughulikiwa" : "Inasubiri"}
        </span>
      </div>`;
    });
  } catch (_) {}
}

/* Chatbot */
async function sendChat() {
  const input = document.getElementById("chatInput");
  const message = input.value.trim();
  if (!message) return;
  appendChatMessage(message, "user");
  input.value = "";
  const request = {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({message, lang: chatLang})
  };
  try {
    const result = await apiJSON(API.chat, request);
    appendChatMessage(result.reply || "Samahani, sijapata jibu kwa swali hilo.", "bot");
  } catch (firstError) {
    try {
      const result = await apiJSON(API.chat + "?retry=1", request);
      appendChatMessage(result.reply || "Samahani, sijapata jibu kwa swali hilo.", "bot");
    } catch (secondError) {
      console.error("Chatbot request failed", secondError);
      appendChatMessage("Samahani, server haipatikani kwa sasa. Hakikisha umefungua mfumo kupitia http://127.0.0.1:5000/ kisha refresh ukurasa.", "bot");
    }
  }
}

function appendChatMessage(message, who) {
  const box = document.getElementById("chatMessages");
  const div = document.createElement("div");
  div.className = "msg " + (who === "user" ? "msg-user" : "msg-bot");
  if (who === "bot") div.innerHTML = `<div class="bot-icon"><i class="fas fa-robot"></i> TakaSmart</div>${message}`;
  else div.textContent = message;
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

/* Preserve the original UI helpers */
document.addEventListener("DOMContentLoaded", () => {
  loadStats();
  loadRecentReports();
  if (typeof setChatLang === "function") setChatLang("sw", document.querySelector(".chat-lang-bar button"));
  if (typeof showSection === "function") showSection("home");
});

async function startCamera(kind) {
  const panel = document.getElementById(kind + "CameraPanel");
  const video = document.getElementById(kind + "Camera");
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showToast("❌ Browser hii haiwezi kufungua camera. Tumia HTTPS au localhost.", "warning");
    return;
  }
  try {
    cameraStreams[kind] = await navigator.mediaDevices.getUserMedia({video:{facingMode:{ideal:"environment"}}, audio:false});
    video.srcObject = cameraStreams[kind];
    panel.classList.add("open");
  } catch (error) {
    showToast("❌ Ruhusu camera kwenye browser ili kupiga picha.", "warning");
  }
}

function stopCamera(kind) {
  if (cameraStreams[kind]) {
    cameraStreams[kind].getTracks().forEach(track => track.stop());
    cameraStreams[kind] = null;
  }
  const panel = document.getElementById(kind + "CameraPanel");
  if (panel) panel.classList.remove("open");
}

function captureCameraPhoto(kind) {
  const video = document.getElementById(kind + "Camera");
  const canvas = document.getElementById(kind + "Canvas");
  if (!video.videoWidth || !video.videoHeight) {
    showToast("❌ Camera bado haijawa tayari.", "warning");
    return;
  }
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(blob => {
    capturedPhotos[kind] = blob;
    const preview = document.getElementById(kind + "Preview");
    preview.src = URL.createObjectURL(blob);
    preview.classList.add("show");
    document.getElementById(kind + "UploadArea").style.display = "none";
    stopCamera(kind);
    if (kind === "report" && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(position => markReportLocation(position.coords.latitude, position.coords.longitude));
    }
    if (kind === "identify") identifyCapturedPhoto(blob);
  }, "image/jpeg", 0.9);
}

function setReportCoordinates(lat, lng) {
  document.getElementById("reportLat").value = Number(lat).toFixed(7);
  document.getElementById("reportLng").value = Number(lng).toFixed(7);
  document.getElementById("reportLocation").value = Number(lat).toFixed(4) + ", " + Number(lng).toFixed(4);
  document.getElementById("reportLocInfo").classList.add("show");
  document.getElementById("reportLocText").textContent = "Lat: " + Number(lat).toFixed(4) + ", Lng: " + Number(lng).toFixed(4);
}

function markReportLocation(lat, lng) {
  if (!reportMap) return;
  if (reportMarker) reportMap.removeLayer(reportMarker);
  reportMarker = L.marker([lat, lng]).addTo(reportMap);
  reportMap.setView([lat, lng], 15);
  setReportCoordinates(lat, lng);
}

function initReportMap() {
  if (reportMap) return;
  reportMap = L.map("reportMap").setView([-6.7924, 39.2083], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {attribution: "&copy; OpenStreetMap"}).addTo(reportMap);
  reportMap.on("click", event => markReportLocation(event.latlng.lat, event.latlng.lng));
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => markReportLocation(position.coords.latitude, position.coords.longitude));
  }
  setTimeout(() => reportMap.invalidateSize(), 300);
}

function initBuyerMap() {
  if (buyerMap) return;
  buyerMap = L.map("buyerMap").setView([-6.7924, 39.2083], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {attribution: "&copy; OpenStreetMap"}).addTo(buyerMap);
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      buyerMap.setView([position.coords.latitude, position.coords.longitude], 13);
      document.getElementById("regLat").value = position.coords.latitude.toFixed(7);
      document.getElementById("regLng").value = position.coords.longitude.toFixed(7);
    });
  }
  setTimeout(() => buyerMap.invalidateSize(), 300);
}

function handleReportPhoto(input) {
  if (!input.files || !input.files[0]) return;
  const preview = document.getElementById("reportPreview");
  preview.src = URL.createObjectURL(input.files[0]);
  preview.classList.add("show");
  document.getElementById("reportUploadArea").style.display = "none";
  initReportMap();
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => markReportLocation(position.coords.latitude, position.coords.longitude));
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      document.getElementById("regLat").value = position.coords.latitude.toFixed(7);
      document.getElementById("regLng").value = position.coords.longitude.toFixed(7);
    });
  }
});
