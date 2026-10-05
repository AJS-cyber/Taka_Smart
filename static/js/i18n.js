/**
 * TakaSmart i18n — mfumo mmoja wa lugha kwa paneli zote (sw / en / fr).
 * Hutoa: window.t(key), window.changeLang(lang), window.applyLocale(),
 *        window.currentLang, window.chatLang
 */
(function () {
  "use strict";

  /* ─────────────────────────────────────────────────────────────
   * CATALOG — maneno yote ya mfumo katika lugha tatu
   * ───────────────────────────────────────────────────────────── */
  const C = {
    sw: {
      /* ── Kichwa ── */
      page_title:        "TakaSmart - Usimamizi wa Taka",
      nav_home:          "Nyumbani",
      nav_report:        "Ripoti",
      nav_identify:      "Tambua",
      nav_buyers:        "Wananunua",
      nav_register:      "Jisajili",

      /* ── Hero ── */
      hero_title:        "🌍 TakaSmart – Usimamizi wa Taka kwa Ufasaha",
      hero_desc:         "Unganisha raia, mamlaka, na wananunua wa taka. Ripoti uchafu, tambua aina ya taka, na pata wananunua karibu nawe.",
      hero_report:       "Ripoti Uchafu",
      hero_identify:     "Tambua Taka",
      hero_buyers:       "Tafuta Wananunua",

      /* ── Takwimu ── */
      stat_reports:      "Ripoti Zilizowasilishwa",
      stat_resolved:     "Zimetatuliwa",
      stat_buyers:       "Wananunua Waliosajiliwa",
      stat_recycled:     "Taka Zilizorecycle",

      /* ── Ripoti ── */
      report_title:         "Ripoti Eneo Lenye Uchafu",
      report_desc:          "Piga picha eneo lenye uchafu na tuma ripoti kwa mamlaka husika.",
      report_photo_title:   "Piga Picha",
      report_upload_hint:   "Fungua kamera kupiga picha ya eneo",
      report_location_label:"📍 Mahali",
      report_desc_label:    "📝 Maelezo",
      report_authority_label:"🏛️ Mamlaka Husika",
      report_submit:        "Tuma Ripoti",
      report_map_title:     "Eneo kwenye Ramani",
      report_recent:        "Ripoti za Hivi Karibuni",
      report_placeholder:   "Eleza aina ya uchafu na hali ya eneo...",
      location_placeholder: "Dar es Salaam, Tanzania",

      /* ── Tambua ── */
      identify_title:        "Tambua Taka na Jinsi ya Kurecycle",
      identify_desc:         "Piga picha ya taka na mfumo utambue aina yake.",
      identify_photo_title:  "Piga Picha ya Taka",
      identify_upload_hint:  "Fungua kamera kupiga picha ya taka",
      identify_recycle_title:"Njia za Kurecycle",
      identify_recycle_hint: "Piga picha ya taka kwanza ili kupata mapendekezo",

      /* ── Wananunua ── */
      buyers_title:     "Tafuta Wananunua wa Taka",
      buyers_desc:      "Tafuta wananunua wa taka karibu nawe.",
      buyer_search:     "Tafuta kwa jina au eneo...",
      no_buyers:        "Hakuna wananunua waliopatikana",
      contact:          "Wasiliana",

      /* ── Jisajili ── */
      register_title:           "Jisajili kama Mnunuzi wa Taka",
      register_desc:            "Wewe ni mnunuzi wa taka? Jisajili hapa.",
      register_form_title:      "Fomu ya Usajili",
      business_name:            "👤 Jina la Biashara",
      email:                    "📧 Barua Pepe",
      phone:                    "📱 Simu",
      location:                 "📍 Eneo",
      waste_types:              "♻️ Aina za Taka Unazonunua",
      business_description:     "📝 Maelezo ya Biashara",
      business_placeholder:     "Eleza biashara yako...",
      reg_name_placeholder:     "Mfano: GreenRecycle Ltd",
      reg_location_placeholder: "Dar es Salaam, Kariakoo",
      register_now:             "Jisajili Sasa",
      registration_success:     "Usajili Umefanikiwa!",
      registration_success_desc:"Umefanikiwa kusajiliwa kama mnunuzi wa taka.",
      view_buyers:              "Tazama Wananunua",

      /* ── Aina za taka (filter + checkboxes) ── */
      all_types:   "Aina Zote",
      plastic:     "Plastiki",
      paper:       "Karatasi",
      glass:       "Kioo",
      metal:       "Chuma",
      organic:     "Kikolojia",
      ewaste:      "E-Waste",
      textile:     "Vazi/Nguo",

      /* ── Mamlaka options ── */
      choose_authority: "-- Chagua Mamlaka --",
      municipal:        "Halmashauri ya Manispaa",
      environment:      "Wizara ya Mazingira",
      health:           "Idara ya Afya",
      waste:            "Shirika la Taka",

      /* ── Camera ── */
      open_camera:     "Fungua Camera",
      take_photo:      "Piga Picha",
      close:           "Funga",

      /* ── Chat ── */
      chat_placeholder: "Andika swali lako...",

      /* ── Ripoti hali ── */
      status_pending:    "Inasubiri",
      status_progress:   "Inashughulikiwa",
      status_resolved:   "Imetatuliwa",
      not_set:           "Haijawekwa",
      no_reports:        "Hakuna ripoti bado.",
      confirm_delete_report: "Futa ripoti hii?",
      report_updated:    "✅ Ripoti imesasishwa",
      report_deleted:    "✅ Ripoti imefutwa",

      /* ── Report labels (authority panel) ── */
      report_content:   "Maudhui",
      report_location_lbl: "Mahali",
      report_status_lbl:   "Hali",
      photo_meaning:    "Maana ya picha",
      photo_missing:    "Picha haijaambatanishwa.",
      btn_handle:       "Shughulikia",
      btn_resolved:     "Tatuliwa",
      btn_delete:       "Futa",

      /* ── Toasts / ujumbe ── */
      saved_report:       "✅ Ripoti imehifadhiwa kwenye mfumo!",
      form_required:      "⚠️ Jaza fomu na chagua angalau aina moja ya taka.",
      registration_done:  "✅ Usajili umefanikiwa!",
      report_required:    "⚠️ Tafadhali jaza maelezo na chagua mamlaka",
      authority_required: "⚠️ Jaza taarifa zote za mamlaka",
      authority_saved:    "✅ Usajili wa mamlaka umetumwa",
      authority_logged_in:"✅ Umeingia kwenye portal ya mamlaka",
      camera_unavailable: "❌ Browser hii haiwezi kufungua camera. Tumia HTTPS au localhost.",
      camera_allow:       "❌ Ruhusu camera kwenye browser ili kupiga picha.",
      camera_not_ready:   "❌ Camera bado haijawa tayari.",
      chat_no_reply:      "Samahani, sijapata jibu. Jaribu tena.",
      chat_server_down:   "Samahani, server haipatikani. Hakikisha mfumo unafanya kazi kisha refresh.",

      /* ── Server error translations ── */
      server_error:          "Kuna tatizo. Tafadhali jaribu tena.",
      err_wrong_password:    "❌ Nywila au barua pepe si sahihi. Angalia na ujaribu tena.",
      err_wrong_credentials: "❌ Taarifa za kuingia si sahihi. Angalia na ujaribu tena.",
      err_login_required:    "❌ Tafadhali ingia kwanza ili kuendelea.",
      err_not_your_report:   "❌ Ripoti hii haipo chini ya mamlaka yako.",
      err_already_exists:    "❌ Jina hili au barua pepe tayari ipo. Tumia nyingine.",
      err_db:                "❌ Tatizo la database. Hakikisha database imeanzishwa.",

      /* ── Admin ── */
      admin_back:          "Rudi TakaSmart",
      admin_title:         "Portal ya Admin",
      admin_intro:         "Sehemu hii ni ya msimamizi wa mfumo pekee.",
      admin_login_btn:     "Ingia",
      admin_logged_in:     "✅ Admin dashboard imefunguka",
      admin_no_users:      "Hakuna watumiaji bado.",
      user_management:     "Usimamizi wa Watumiaji",
      admin_capabilities:  "Uwezo wa Admin",
      admin_logout:        "Toka",
      label_username:      "Jina la mtumiaji",
      label_password:      "Nenosiri",
      label_role:          "Wadhifa",
      label_permissions:   "Ruhusa (comma-separated)",
      btn_create_user:     "Unda Mtumiaji",
      user_created:        "✅ Mtumiaji ameundwa",
      user_updated:        "✅ Mtumiaji amesasishwa",
      user_deleted:        "✅ Mtumiaji amefutwa",
      confirm_delete_user: "Futa mtumiaji huyu?",
      stat_label_reports:  "Ripoti",
      stat_label_resolved: "Zimetatuliwa",
      stat_label_buyers:   "Wananunua",
      stat_label_auths:    "Mamlaka",
      /* ── User login ── */
      user_login_title:    "Ingia kama Mtumiaji",
      user_login_hint:     "Ingia kwa akaunti iliyoundwa na msimamizi.",
      user_login_label:    "Username au Email",
      user_logged_in:      "✅ Umeingia kwa mafanikio",
      user_logged_out:     "✅ Umetoka",
      user_dashboard_welcome: "Karibu kwenye TakaSmart",
      user_role_label:     "Wadhifa wako",
      user_panel_reports:  "Ripoti za Hivi Karibuni",
      user_panel_stats:    "Takwimu za Mfumo",

      /* ── Admin task cards (sw) ── */
      admin_tasks_title:       "Kazi za Msimamizi",
      task_manage_users:       "Simamia Watumiaji",
      task_manage_users_desc:  "Unda, hariri na futa akaunti za watumiaji. Weka wadhifu na ruhusa zinazofaa kwa kila mtu.",
      task_manage_reports:     "Simamia Ripoti",
      task_manage_reports_desc:"Pitia ripoti zote za uchafu zilizotumwa. Angalia picha, eneo na hali ya kila ripoti.",
      task_manage_buyers:      "Simamia Wananunua",
      task_manage_buyers_desc: "Angalia wananunua wote waliojisajili. Weza kuwasiliana nao au kuwaondoa ikiwa ni lazima.",
      task_manage_auths:       "Simamia Mamlaka",
      task_manage_auths_desc:  "Simamia mamlaka na idara zilizosajiliwa kwenye mfumo wa TakaSmart.",
      task_view_stats:         "Tazama Takwimu",
      task_view_stats_desc:    "Angalia idadi ya ripoti, zilizotatatuliwa, wananunua na mamlaka kwenye mfumo.",
      task_security:           "Usalama wa Mfumo",
      task_security_desc:      "Hakikisha usalama wa mfumo. Badilisha credentials za admin na uangalie shughuli za mfumo.",

      /* ── Authority portal ── */
      authority_portal:        "Portal ya Mamlaka",
      authority_intro:         "Halmashauri, wizara, idara na mashirika ya taka zinaweza kuingia na kusimamia ripoti zao hapa.",
      authority_signin_title:  "Ingia kwenye portal",
      authority_signup_title:  "Jisajili mamlaka",
      tab_signin:              "Ingia",
      tab_signup:              "Jisajili",
      label_authority_name:    "Jina la mamlaka/idara",
      label_authority_type:    "Aina",
      label_authority_email:   "Email ya kuingia",
      label_authority_phone:   "Simu",
      label_authority_location:"Eneo",
      label_description:       "Maelezo",
      btn_signin:              "Ingia",
      btn_create_account:      "Fungua akaunti",
      authority_dashboard_title:"Dashibodi ya Mamlaka",
      authority_dept_label:    "Idara:",
      authority_duties_title:  "Majukumu",
      authority_reports_title: "Ripoti za Mamlaka Hii",
      authority_pending_label: "Ripoti mpya zinazosubiri:",
      authority_no_reports:    "Hakuna ripoti bado.",
      auth_task_receive:       "📥 Pokea na chunguza ripoti zilizotumwa na wananchi.",
      auth_task_status:        "🔄 Weka hali ya utekelezaji (Inashughulikiwa / Imetatuliwa).",
      auth_task_feedback:      "📢 Tuma mrejesho kwa wananchi kuhusu hatua zilizochukuliwa.",
      auth_task_report:        "📊 Ripoti matokeo ya usafi na mafanikio kwa viongozi.",
    },

    en: {
      page_title:        "TakaSmart - Waste Management",
      nav_home:          "Home",
      nav_report:        "Report",
      nav_identify:      "Identify",
      nav_buyers:        "Buyers",
      nav_register:      "Register",

      hero_title:        "🌍 TakaSmart – Smart Waste Management",
      hero_desc:         "Connect citizens, authorities, and waste buyers. Report waste, identify waste types, and find buyers near you.",
      hero_report:       "Report Waste",
      hero_identify:     "Identify Waste",
      hero_buyers:       "Find Buyers",

      stat_reports:      "Reports Submitted",
      stat_resolved:     "Resolved",
      stat_buyers:       "Registered Buyers",
      stat_recycled:     "Waste Recycled",

      report_title:          "Report a Waste Area",
      report_desc:           "Take a photo of a waste area and send a report to the relevant authority.",
      report_photo_title:    "Take Photo",
      report_upload_hint:    "Open the camera to photograph the area",
      report_location_label: "📍 Location",
      report_desc_label:     "📝 Description",
      report_authority_label:"🏛️ Relevant Authority",
      report_submit:         "Submit Report",
      report_map_title:      "Location on Map",
      report_recent:         "Recent Reports",
      report_placeholder:    "Describe the waste and condition of the area...",
      location_placeholder:  "Dar es Salaam, Tanzania",

      identify_title:        "Identify Waste & How to Recycle",
      identify_desc:         "Take a photo and the system will identify the waste type.",
      identify_photo_title:  "Photograph Waste",
      identify_upload_hint:  "Open the camera to photograph waste",
      identify_recycle_title:"Recycling Methods",
      identify_recycle_hint: "Take a waste photo first to get recommendations",

      buyers_title:     "Find Waste Buyers",
      buyers_desc:      "Find waste buyers near you.",
      buyer_search:     "Search by name or location...",
      no_buyers:        "No buyers found",
      contact:          "Contact",

      register_title:           "Register as a Waste Buyer",
      register_desc:            "Are you a waste buyer? Register here.",
      register_form_title:      "Registration Form",
      business_name:            "👤 Business Name",
      email:                    "📧 Email",
      phone:                    "📱 Phone",
      location:                 "📍 Location",
      waste_types:              "♻️ Waste Types You Buy",
      business_description:     "📝 Business Description",
      business_placeholder:     "Describe your business...",
      reg_name_placeholder:     "e.g. GreenRecycle Ltd",
      reg_location_placeholder: "Dar es Salaam, Kariakoo",
      register_now:             "Register Now",
      registration_success:     "Registration Successful!",
      registration_success_desc:"You have successfully registered as a waste buyer.",
      view_buyers:              "View Buyers",

      all_types:   "All Types",
      plastic:     "Plastic",
      paper:       "Paper",
      glass:       "Glass",
      metal:       "Metal",
      organic:     "Organic",
      ewaste:      "E-Waste",
      textile:     "Textile",

      choose_authority: "-- Choose Authority --",
      municipal:        "Municipal Council",
      environment:      "Ministry of Environment",
      health:           "Health Department",
      waste:            "Waste Services",

      open_camera:     "Open Camera",
      take_photo:      "Take Photo",
      close:           "Close",

      chat_placeholder: "Type your question...",

      status_pending:    "Pending",
      status_progress:   "In Progress",
      status_resolved:   "Resolved",
      not_set:           "Not set",
      no_reports:        "No reports yet.",
      confirm_delete_report: "Delete this report?",
      report_updated:    "✅ Report updated",
      report_deleted:    "✅ Report deleted",

      report_content:      "Content",
      report_location_lbl: "Location",
      report_status_lbl:   "Status",
      photo_meaning:       "Photo meaning",
      photo_missing:       "No photo attached.",
      btn_handle:          "Process",
      btn_resolved:        "Resolved",
      btn_delete:          "Delete",

      saved_report:       "✅ Report saved to the system!",
      form_required:      "⚠️ Complete the form and choose at least one waste type.",
      registration_done:  "✅ Registration successful!",
      report_required:    "⚠️ Please enter a description and choose an authority",
      authority_required: "⚠️ Please fill in all authority details",
      authority_saved:    "✅ Authority registration submitted",
      authority_logged_in:"✅ Signed in to the authority portal",
      camera_unavailable: "❌ This browser cannot open the camera. Use HTTPS or localhost.",
      camera_allow:       "❌ Allow camera access in the browser to take a photo.",
      camera_not_ready:   "❌ Camera is not ready yet.",
      chat_no_reply:      "Sorry, no reply received. Please try again.",
      chat_server_down:   "Sorry, the server is unreachable. Make sure the system is running then refresh.",

      /* ── Server error translations ── */
      server_error:          "Something went wrong. Please try again.",
      err_wrong_password:    "❌ Incorrect email or password. Please check and try again.",
      err_wrong_credentials: "❌ Invalid login details. Please check and try again.",
      err_login_required:    "❌ Please sign in first to continue.",
      err_not_your_report:   "❌ This report does not belong to your authority.",
      err_already_exists:    "❌ This username or email already exists. Please use another.",
      err_db:                "❌ Database error. Make sure the database is set up.",

      admin_back:          "Back to TakaSmart",
      admin_title:         "Admin Portal",
      admin_intro:         "This area is for system administrators only.",
      admin_login_btn:     "Sign In",
      admin_logged_in:     "✅ Admin dashboard opened",
      admin_no_users:      "No users yet.",
      user_management:     "User Management",
      admin_capabilities:  "Admin Capabilities",
      admin_logout:        "Sign Out",
      label_username:      "Username",
      label_password:      "Password",
      label_role:          "Role",
      label_permissions:   "Permissions (comma-separated)",
      btn_create_user:     "Create User",
      user_created:        "✅ User created",
      user_updated:        "✅ User updated",
      user_deleted:        "✅ User deleted",
      confirm_delete_user: "Delete this user?",
      stat_label_reports:  "Reports",
      stat_label_resolved: "Resolved",
      stat_label_buyers:   "Buyers",
      stat_label_auths:    "Authorities",
      /* ── User login ── */
      user_login_title:    "Sign In as User",
      user_login_hint:     "Sign in with an account created by the administrator.",
      user_login_label:    "Username or Email",
      user_logged_in:      "✅ Signed in successfully",
      user_logged_out:     "✅ Signed out",
      user_dashboard_welcome: "Welcome to TakaSmart",
      user_role_label:     "Your Role",
      user_panel_reports:  "Recent Reports",
      user_panel_stats:    "System Statistics",

      /* ── Admin task cards (en) ── */
      admin_tasks_title:       "Administrator Responsibilities",
      task_manage_users:       "Manage Users",
      task_manage_users_desc:  "Create, edit and delete user accounts. Set the appropriate role for each user.",
      task_manage_reports:     "Manage Reports",
      task_manage_reports_desc:"Review all waste reports submitted. Check photos, location and status of each report.",
      task_manage_buyers:      "Manage Buyers",
      task_manage_buyers_desc: "View all registered buyers. Contact them or remove them if necessary.",
      task_manage_auths:       "Manage Authorities",
      task_manage_auths_desc:  "Manage authorities and departments registered in the TakaSmart system.",
      task_view_stats:         "View Statistics",
      task_view_stats_desc:    "See counts of reports, resolved cases, buyers and authorities in the system.",
      task_security:           "System Security",
      task_security_desc:      "Ensure system security. Change admin credentials and monitor system activity.",

      authority_portal:        "Authority Portal",
      authority_intro:         "Councils, ministries, departments and waste companies can sign in and manage their reports here.",
      authority_signin_title:  "Sign in to portal",
      authority_signup_title:  "Register authority",
      tab_signin:              "Sign In",
      tab_signup:              "Sign Up",
      label_authority_name:    "Authority/department name",
      label_authority_type:    "Type",
      label_authority_email:   "Login email",
      label_authority_phone:   "Phone",
      label_authority_location:"Location",
      label_description:       "Description",
      btn_signin:              "Sign In",
      btn_create_account:      "Create Account",
      authority_dashboard_title:"Authority Dashboard",
      authority_dept_label:    "Department:",
      authority_duties_title:  "Responsibilities",
      authority_reports_title: "This Authority's Reports",
      authority_pending_label: "New reports pending:",
      authority_no_reports:    "No reports yet.",
      auth_task_receive:       "📥 Receive and review reports submitted by citizens.",
      auth_task_status:        "🔄 Set the processing status (In Progress / Resolved).",
      auth_task_feedback:      "📢 Send feedback to citizens about actions taken.",
      auth_task_report:        "📊 Report cleanliness results and achievements to leaders.",
    },

    fr: {
      page_title:        "TakaSmart - Gestion des déchets",
      nav_home:          "Accueil",
      nav_report:        "Signaler",
      nav_identify:      "Identifier",
      nav_buyers:        "Acheteurs",
      nav_register:      "S'inscrire",

      hero_title:        "🌍 TakaSmart – Gestion Intelligente des Déchets",
      hero_desc:         "Connectez citoyens, autorités et acheteurs de déchets. Signalez, identifiez et trouvez des acheteurs près de vous.",
      hero_report:       "Signaler un déchet",
      hero_identify:     "Identifier",
      hero_buyers:       "Trouver des acheteurs",

      stat_reports:      "Signalements",
      stat_resolved:     "Résolus",
      stat_buyers:       "Acheteurs inscrits",
      stat_recycled:     "Déchets recyclés",

      report_title:          "Signaler une zone de déchets",
      report_desc:           "Photographiez une zone et envoyez le signalement à l'autorité.",
      report_photo_title:    "Prendre une photo",
      report_upload_hint:    "Ouvrir la caméra pour photographier la zone",
      report_location_label: "📍 Lieu",
      report_desc_label:     "📝 Description",
      report_authority_label:"🏛️ Autorité compétente",
      report_submit:         "Envoyer",
      report_map_title:      "Lieu sur la carte",
      report_recent:         "Signalements récents",
      report_placeholder:    "Décrivez le déchet et l'état de la zone...",
      location_placeholder:  "Dar es Salaam, Tanzanie",

      identify_title:        "Identifier les déchets & Recyclage",
      identify_desc:         "Prenez une photo et le système identifiera le type de déchet.",
      identify_photo_title:  "Photographier le déchet",
      identify_upload_hint:  "Ouvrir la caméra pour photographier le déchet",
      identify_recycle_title:"Méthodes de recyclage",
      identify_recycle_hint: "Prenez d'abord une photo du déchet",

      buyers_title:     "Trouver des acheteurs",
      buyers_desc:      "Trouvez des acheteurs de déchets près de vous.",
      buyer_search:     "Rechercher par nom ou lieu...",
      no_buyers:        "Aucun acheteur trouvé",
      contact:          "Contacter",

      register_title:           "S'inscrire comme acheteur",
      register_desc:            "Vous achetez des déchets ? Inscrivez-vous ici.",
      register_form_title:      "Formulaire d'inscription",
      business_name:            "👤 Nom de l'entreprise",
      email:                    "📧 E-mail",
      phone:                    "📱 Téléphone",
      location:                 "📍 Lieu",
      waste_types:              "♻️ Types de déchets achetés",
      business_description:     "📝 Description de l'activité",
      business_placeholder:     "Décrivez votre activité...",
      reg_name_placeholder:     "ex. GreenRecycle Sarl",
      reg_location_placeholder: "Dar es Salaam, Kariakoo",
      register_now:             "S'inscrire",
      registration_success:     "Inscription réussie !",
      registration_success_desc:"Vous êtes inscrit comme acheteur de déchets.",
      view_buyers:              "Voir les acheteurs",

      all_types:   "Tous les types",
      plastic:     "Plastique",
      paper:       "Papier",
      glass:       "Verre",
      metal:       "Métal",
      organic:     "Organique",
      ewaste:      "Déchets électroniques",
      textile:     "Textile",

      choose_authority: "-- Choisir une autorité --",
      municipal:        "Conseil municipal",
      environment:      "Ministère de l'environnement",
      health:           "Service de santé",
      waste:            "Service des déchets",

      open_camera:     "Ouvrir la caméra",
      take_photo:      "Prendre une photo",
      close:           "Fermer",

      chat_placeholder: "Écrivez votre question...",

      status_pending:    "En attente",
      status_progress:   "En cours",
      status_resolved:   "Résolu",
      not_set:           "Non défini",
      no_reports:        "Aucun signalement.",
      confirm_delete_report: "Supprimer ce signalement ?",
      report_updated:    "✅ Signalement mis à jour",
      report_deleted:    "✅ Signalement supprimé",

      report_content:      "Contenu",
      report_location_lbl: "Lieu",
      report_status_lbl:   "Statut",
      photo_meaning:       "Sens de la photo",
      photo_missing:       "Aucune photo jointe.",
      btn_handle:          "Traiter",
      btn_resolved:        "Résolu",
      btn_delete:          "Supprimer",

      saved_report:       "✅ Signalement enregistré !",
      form_required:      "⚠️ Remplissez le formulaire et choisissez au moins un type.",
      registration_done:  "✅ Inscription réussie !",
      report_required:    "⚠️ Saisissez une description et choisissez une autorité",
      authority_required: "⚠️ Veuillez remplir toutes les informations de l'autorité",
      authority_saved:    "✅ Inscription de l'autorité envoyée",
      authority_logged_in:"✅ Connecté au portail des autorités",
      camera_unavailable: "❌ Ce navigateur ne peut pas ouvrir la caméra. Utilisez HTTPS ou localhost.",
      camera_allow:       "❌ Autorisez la caméra dans le navigateur pour prendre une photo.",
      camera_not_ready:   "❌ La caméra n'est pas encore prête.",
      chat_no_reply:      "Désolé, pas de réponse. Réessayez.",
      chat_server_down:   "Désolé, le serveur est inaccessible. Assurez-vous que le système fonctionne puis actualisez.",

      /* ── Server error translations ── */
      server_error:          "Une erreur est survenue. Veuillez réessayer.",
      err_wrong_password:    "❌ E-mail ou mot de passe incorrect. Vérifiez et réessayez.",
      err_wrong_credentials: "❌ Identifiants invalides. Vérifiez et réessayez.",
      err_login_required:    "❌ Veuillez vous connecter d'abord pour continuer.",
      err_not_your_report:   "❌ Ce signalement n'appartient pas à votre autorité.",
      err_already_exists:    "❌ Ce nom ou e-mail existe déjà. Utilisez-en un autre.",
      err_db:                "❌ Erreur de base de données. Vérifiez que la base de données est configurée.",

      admin_back:          "Retour à TakaSmart",
      admin_title:         "Portail administrateur",
      admin_intro:         "Cette section est réservée aux administrateurs.",
      admin_login_btn:     "Connexion",
      admin_logged_in:     "✅ Tableau de bord ouvert",
      admin_no_users:      "Aucun utilisateur.",
      user_management:     "Gestion des utilisateurs",
      admin_capabilities:  "Fonctions administrateur",
      admin_logout:        "Déconnexion",
      label_username:      "Nom d'utilisateur",
      label_password:      "Mot de passe",
      label_role:          "Rôle",
      label_permissions:   "Autorisations (séparées par virgule)",
      btn_create_user:     "Créer un utilisateur",
      user_created:        "✅ Utilisateur créé",
      user_updated:        "✅ Utilisateur mis à jour",
      user_deleted:        "✅ Utilisateur supprimé",
      confirm_delete_user: "Supprimer cet utilisateur ?",
      stat_label_reports:  "Signalements",
      stat_label_resolved: "Résolus",
      stat_label_buyers:   "Acheteurs",
      stat_label_auths:    "Autorités",
      /* ── User login ── */
      user_login_title:    "Connexion Utilisateur",
      user_login_hint:     "Connectez-vous avec un compte créé par l'administrateur.",
      user_login_label:    "Nom d'utilisateur ou e-mail",
      user_logged_in:      "✅ Connexion réussie",
      user_logged_out:     "✅ Déconnecté",
      user_dashboard_welcome: "Bienvenue sur TakaSmart",
      user_role_label:     "Votre rôle",
      user_panel_reports:  "Signalements récents",
      user_panel_stats:    "Statistiques du système",

      /* ── Admin task cards (fr) ── */
      admin_tasks_title:       "Responsabilités de l'administrateur",
      task_manage_users:       "Gérer les utilisateurs",
      task_manage_users_desc:  "Créez, modifiez et supprimez des comptes utilisateurs. Définissez le rôle approprié pour chaque utilisateur.",
      task_manage_reports:     "Gérer les signalements",
      task_manage_reports_desc:"Consultez tous les signalements de déchets soumis. Vérifiez les photos, la localisation et le statut.",
      task_manage_buyers:      "Gérer les acheteurs",
      task_manage_buyers_desc: "Consultez tous les acheteurs inscrits. Contactez-les ou supprimez-les si nécessaire.",
      task_manage_auths:       "Gérer les autorités",
      task_manage_auths_desc:  "Gérez les autorités et services enregistrés dans le système TakaSmart.",
      task_view_stats:         "Voir les statistiques",
      task_view_stats_desc:    "Consultez le nombre de signalements, cas résolus, acheteurs et autorités.",
      task_security:           "Sécurité du système",
      task_security_desc:      "Assurez la sécurité du système. Modifiez les identifiants admin et surveillez l'activité.",

      authority_portal:        "Portail des autorités",
      authority_intro:         "Les conseils, ministères, services et entreprises de déchets peuvent se connecter ici.",
      authority_signin_title:  "Connexion au portail",
      authority_signup_title:  "Inscrire une autorité",
      tab_signin:              "Connexion",
      tab_signup:              "Inscription",
      label_authority_name:    "Nom de l'autorité/service",
      label_authority_type:    "Type",
      label_authority_email:   "E-mail de connexion",
      label_authority_phone:   "Téléphone",
      label_authority_location:"Lieu",
      label_description:       "Description",
      btn_signin:              "Connexion",
      btn_create_account:      "Créer un compte",
      authority_dashboard_title:"Tableau de bord",
      authority_dept_label:    "Service :",
      authority_duties_title:  "Responsabilités",
      authority_reports_title: "Signalements de cette autorité",
      authority_pending_label: "Nouveaux signalements en attente :",
      authority_no_reports:    "Aucun signalement.",
      auth_task_receive:       "📥 Recevoir et examiner les signalements soumis par les citoyens.",
      auth_task_status:        "🔄 Définir le statut de traitement (En cours / Résolu).",
      auth_task_feedback:      "📢 Envoyer des retours aux citoyens sur les mesures prises.",
      auth_task_report:        "📊 Rapporter les résultats de propreté et les réussites aux dirigeants.",
    },
  };

  /* ─────────────────────────────────────────────────────────────
   * INIT
   * ───────────────────────────────────────────────────────────── */
  var saved = localStorage.getItem("takasmart-language");
  window.currentLang = (saved && C[saved]) ? saved : "sw";
  window.chatLang    = window.currentLang;
  window.TakaI18n    = { catalog: C };

  /* ── Lookup helper ── */
  window.t = function (key) {
    return (C[window.currentLang] && C[window.currentLang][key]) ||
           C.sw[key] || key;
  };

  /* ─────────────────────────────────────────────────────────────
   * applyLocale — badilisha kila kitu kwenye ukurasa
   * ───────────────────────────────────────────────────────────── */
  window.applyLocale = function () {
    var lang = window.currentLang;

    /* html[lang] na title */
    document.documentElement.lang = lang;
    if (C[lang] && C[lang].page_title) document.title = C[lang].page_title;

    /* data-i18n → textContent */
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      el.textContent = window.t(el.dataset.i18n);
    });

    /* data-i18n-placeholder → placeholder */
    document.querySelectorAll("[data-i18n-placeholder]").forEach(function (el) {
      el.placeholder = window.t(el.dataset.i18nPlaceholder);
    });

    /* data-i18n-aria-label */
    document.querySelectorAll("[data-i18n-aria-label]").forEach(function (el) {
      el.setAttribute("aria-label", window.t(el.dataset.i18nAriaLabel));
    });

    /* data-i18n-title */
    document.querySelectorAll("[data-i18n-title]").forEach(function (el) {
      el.title = window.t(el.dataset.i18nTitle);
    });

    /* data-i18n-opt → <option> textContent (option ndani ya select yoyote) */
    document.querySelectorAll("[data-i18n-opt]").forEach(function (el) {
      var key = el.dataset.i18nOpt;
      var translated = window.t(key);
      /* Hifadhi emoji mwanzoni ikiweko (🧴, 📦, n.k.) */
      var current = el.textContent;
      var emoji = current.match(/^[\p{Emoji}\s]+/u);
      el.textContent = emoji ? emoji[0].trimEnd() + " " + translated : translated;
    });

    /* Sync .lang-select dropdowns kwenye ukurasa wowote */
    document.querySelectorAll(".lang-select").forEach(function (sel) {
      sel.value = lang;
    });

    /* Sync chat lang bar */
    document.querySelectorAll(".chat-lang-bar button").forEach(function (btn) {
      btn.classList.toggle("active", btn.dataset.lang === lang);
    });

    /* Hifadhi kwenye localStorage */
    localStorage.setItem("takasmart-language", lang);

    /* Rerender dynamic content ikiwa imewahi kupakiwa */
    if (typeof renderIdentifyResult === "function" && window.lastIdentifyResult) {
      renderIdentifyResult(window.lastIdentifyResult);
    }
    if (typeof loadRecentReports === "function" && document.getElementById("recentReports")) {
      loadRecentReports();
    }
    if (typeof loadBuyers === "function" && document.getElementById("buyersList")) {
      loadBuyers();
    }
    if (typeof refreshAdminDashboardLang === "function" && window.lastAdminData) {
      refreshAdminDashboardLang(window.lastAdminData);
    }
    if (typeof renderAdminUsers === "function" && window.lastAdminUsers) {
      renderAdminUsers(window.lastAdminUsers);
    }
    if (typeof refreshUserDashboardLang === "function" && window.lastUserData) {
      refreshUserDashboardLang();
    }
    if (typeof refreshAuthorityDashboardLang === "function" && window.lastAuthorityData) {
      refreshAuthorityDashboardLang(window.lastAuthorityData);
    }
    if (typeof renderAuthorityReports === "function" && window.lastAuthorityReports) {
      renderAuthorityReports(window.lastAuthorityReports);
    }
  };

  /* ─────────────────────────────────────────────────────────────
   * changeLang — kuitwa na navbar select au kitufe chochote
   * ───────────────────────────────────────────────────────────── */
  window.changeLang = function (lang) {
    if (!C[lang]) lang = "sw";
    window.currentLang = lang;
    window.chatLang    = lang;
    window.applyLocale();
    /* Sync chatbot — setChatLang is defined in app.js and handles the chat window */
    if (typeof setChatLang === "function") setChatLang(lang);
  };

  /* ─────────────────────────────────────────────────────────────
   * setChatLang — sycn chatbot peke yake (inaitwa pia na changeLang)
   * ───────────────────────────────────────────────────────────── */
  window.setChatLang = function (lang, button) {
    if (!C[lang]) lang = window.currentLang;
    window.chatLang = lang;
    document.querySelectorAll(".chat-lang-bar button").forEach(function (btn) {
      btn.classList.toggle("active", btn.dataset.lang === lang);
    });
    /* Rerender chatbot messages */
    if (typeof renderQQ === "function") {
      var messages = document.getElementById("chatMessages");
      if (messages) messages.innerHTML = "";
      if (typeof appendChatMessage === "function" && typeof WELCOME_MSG !== "undefined") {
        appendChatMessage(WELCOME_MSG[lang] || WELCOME_MSG.sw, "bot");
      }
      renderQQ();
    }
  };

  /* Tekeleza applyLocale baada ya DOM kupakia */
  document.addEventListener("DOMContentLoaded", window.applyLocale);

})();
