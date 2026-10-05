/**
 * TakaSmart app.js — v20261001
 * Maneno yote yanabadilishwa kwa window.t(key) kutoka i18n.js.
 * Hakuna hardcoded text — lugha inafuata currentLang kila wakati.
 */

/* ─── globals ─────────────────────────────────────────────────── */
var reportMap = null, buyerMap = null, reportMarker = null, buyerMarkers = [];

/* i18n.js owns window.currentLang and window.chatLang.
   We just read them; never redefine with Object.defineProperty. */
var currentLang = window.currentLang || "sw";
var chatLang    = window.chatLang    || "sw";

/* ─── helpers ─────────────────────────────────────────────────── */
function escapeHtml(v) {
  return String(v ?? "").replace(/[&<>"']/g, function (c) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;" }[c];
  });
}
function escapeJs(v) {
  return String(v ?? "").replace(/\\/g, "\\\\").replace(/'/g, "\\'");
}
function showToast(msg, type) {
  var el = document.getElementById("toast");
  if (!el) return;
  el.className = "toast show toast-" + (type || "info");
  el.innerHTML = msg;
  setTimeout(function () { el.classList.remove("show"); }, 4000);
}

/* ─── section navigation ─────────────────────────────────────── */
function showSection(name) {
  var home = document.getElementById("section-home");
  if (home) home.style.display = name === "home" ? "" : "none";
  document.querySelectorAll(".section").forEach(function (s) { s.classList.remove("active"); });
  var sec = document.getElementById("section-" + name);
  if (sec) sec.classList.add("active");
  document.querySelectorAll(".nav-links button").forEach(function (b) { b.classList.remove("active"); });
  var nb = document.getElementById("nav-" + name);
  if (nb) nb.classList.add("active");
  if (name === "report" && !reportMap) setTimeout(initReportMap, 200);
  if (name === "buyers" && !buyerMap) setTimeout(initBuyerMap, 200);
  if (name === "buyers" && document.getElementById("buyersList")) setTimeout(loadBuyers, 400);
  if (document.body) window.scrollTo({ top: name === "home" ? 0 : 200, behavior: "smooth" });
}

/* ─── API ─────────────────────────────────────────────────────── */
var API = { reports: "/api/reports", buyers: "/api/buyers", identify: "/api/identify", chat: "/api/chat" };

/* Server error messages → i18n keys.
   Keys must exist in every language in i18n.js catalog. */
var SERVER_ERR_MAP = [
  [/password.*si sahihi|password.*incorrect|invalid.*password|mot de passe.*incorrect/i, "err_wrong_password"],
  [/si sahihi|incorrect credentials|identifiants incorrects/i,                          "err_wrong_credentials"],
  [/inahitajika|required|requis/i,                                                       "err_login_required"],
  [/si ya idara yako|not your report|pas votre signalement/i,                            "err_not_your_report"],
  [/tayari imetumika|already exists|déjà utilisé/i,                                      "err_already_exists"],
  [/database|db|connexion/i,                                                             "err_db"],
];

function translateServerError(msg) {
  if (!msg) return window.t("server_error");
  for (var i = 0; i < SERVER_ERR_MAP.length; i++) {
    if (SERVER_ERR_MAP[i][0].test(msg)) return window.t(SERVER_ERR_MAP[i][1]);
  }
  return msg; /* keep original if no mapping found */
}

async function apiJSON(url, options) {
  options = options || {};
  var response = await fetch(url, Object.assign({ cache: "no-store" }, options));
  var data = await response.json().catch(function () { return {}; });
  if (!response.ok) throw new Error(translateServerError(data.error) || window.t("server_error"));
  return data;
}

/* ─── Stats / Recent Reports ─────────────────────────────────── */
async function loadStats() {
  try {
    var s = await apiJSON("/api/stats");
    document.getElementById("statReports").textContent = Number(s.reports).toLocaleString();
    document.getElementById("statResolved").textContent = Number(s.resolved).toLocaleString();
    document.getElementById("statBuyers").textContent = Number(s.buyers).toLocaleString();
  } catch (_) {}
}

async function loadRecentReports() {
  try {
    var data = await apiJSON(API.reports);
    var d = document.getElementById("recentReports");
    if (!d) return;
    d.innerHTML = "";
    (data.reports || []).slice(0, 10).forEach(function (r) {
      var statusKey = r.status === "resolved" ? "status_resolved"
                    : r.status === "in_progress" ? "status_progress"
                    : "status_pending";
      var statusClass = r.status === "resolved" ? "resolved"
                      : r.status === "in_progress" ? "progress"
                      : "pending";
      var locText = escapeHtml(r.location || window.t("not_set"));
      d.innerHTML +=
        '<div class="report-item">' +
          '<div class="report-img">' +
            (r.photo ? '<img src="' + r.photo + '" alt="report">' : '<i class="fas fa-camera"></i>') +
          '</div>' +
          '<div class="report-details">' +
            '<h4>' + escapeHtml(r.description) + '</h4>' +
            '<p>📍 ' + locText + '</p>' +
          '</div>' +
          '<span class="report-status status-' + statusClass + '">' + window.t(statusKey) + '</span>' +
        '</div>';
    });
    if (!d.innerHTML) d.innerHTML = '<p style="color:var(--text-light);padding:16px">' + window.t("no_reports") + '</p>';
  } catch (_) {}
}

/* ─── Report submission ──────────────────────────────────────── */
var capturedPhotos = {};
var cameraStreams  = {};

async function submitReport() {
  var desc = document.getElementById("reportDesc").value.trim();
  var auth = document.getElementById("reportAuthority").value;
  var loc  = document.getElementById("reportLocation").value.trim();
  var lat  = document.getElementById("reportLat").value;
  var lng  = document.getElementById("reportLng").value;
  if (!desc || !auth || !capturedPhotos.report) {
    showToast(window.t("report_required"), "warning");
    return;
  }
  try {
    var fd = new FormData();
    fd.append("photo", capturedPhotos.report, "camera-report.jpg");
    [["description", desc], ["authority", auth], ["location", loc || window.t("not_set")], ["lat", lat], ["lng", lng]]
      .forEach(function (kv) { fd.append(kv[0], kv[1]); });
    await apiJSON(API.reports, { method: "POST", body: fd });
    showToast(window.t("saved_report"), "success");
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
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

/* ─── Registration ───────────────────────────────────────────── */
async function submitRegistration() {
  var name     = document.getElementById("regName").value.trim();
  var email    = document.getElementById("regEmail").value.trim();
  var phone    = document.getElementById("regPhone").value.trim();
  var location = document.getElementById("regLocation").value.trim();
  var lat      = document.getElementById("regLat").value;
  var lng      = document.getElementById("regLng").value;
  var description = document.getElementById("regDesc").value.trim();
  var types    = Array.from(document.querySelectorAll('#regFormCard input[type="checkbox"]:checked'))
                      .map(function (x) { return x.value; });
  if (!name || !email || !phone || !location || !types.length) {
    showToast(window.t("form_required"), "warning");
    return;
  }
  try {
    await apiJSON(API.buyers, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name: name, email: email, phone: phone, location: location,
                             description: description, types: types, lat: lat, lng: lng })
    });
    document.getElementById("regFormCard").style.display = "none";
    document.getElementById("regSuccess").classList.add("show");
    showToast(window.t("registration_done"), "success");
    loadStats();
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

/* ─── Identify Waste ─────────────────────────────────────────── */
async function identifyCapturedPhoto(blob) {
  var preview = document.getElementById("identifyPreview");
  preview.src = URL.createObjectURL(blob);
  preview.classList.add("show");
  document.getElementById("identifyUploadArea").style.display = "none";
  try {
    var fd = new FormData();
    fd.append("photo", blob, "camera-identify.jpg");
    var result = await apiJSON(API.identify, { method: "POST", body: fd });
    renderIdentifyResult(result);
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

function renderIdentifyResult(result) {
  window.lastIdentifyResult = result;
  var lang = window.currentLang || "sw";

  /* ── REJECTED ── */
  if (!result.accepted) {
    var msg = lang === "en" ? (result.reasonEn || "Image not identified.")
            : lang === "fr" ? (result.reason   || "Image non identifiée.")
            :                  (result.reason   || "Picha haikutambuliwa.");

    var titleText  = lang === "en" ? "Image Not Identified"
                   : lang === "fr" ? "Image non identifiée"
                   : "Picha Haikutambuliwa";
    var tipsLabel  = lang === "en" ? "Tips for a better photo:"
                   : lang === "fr" ? "Conseils pour une meilleure photo :"
                   : "Vidokezo vya picha bora:";
    var tips = lang === "en"
      ? ["Get closer to the waste item", "Waste should fill most of the frame", "Use good lighting, avoid shadows", "Photograph one waste type at a time"]
      : lang === "fr"
      ? ["Rapprochez-vous du déchet", "Le déchet doit occuper la majorité du cadre", "Bon éclairage, évitez les ombres", "Photographiez un seul type à la fois"]
      : ["Karibia zaidi na taka", "Taka ijaze sehemu kubwa ya picha", "Tumia mwanga mzuri, epuka kivuli", "Piga picha ya aina moja kwa wakati mmoja"];
    var tipsHTML   = tips.map(function (tip) { return '<li style="margin:4px 0">' + tip + '</li>'; }).join("");
    var retryLabel = window.t("open_camera");

    document.getElementById("aiResult").innerHTML =
      '<div style="background:#fff3e0;border-left:4px solid #FF8F00;border-radius:8px;padding:16px;margin-top:8px">' +
        '<h4 style="color:#E65100;margin:0 0 10px"><i class="fas fa-exclamation-triangle"></i> ' + titleText + '</h4>' +
        '<p style="white-space:pre-line;margin-bottom:12px">' + escapeHtml(msg) + '</p>' +
        '<strong>' + tipsLabel + '</strong>' +
        '<ul style="margin:8px 0 0 16px">' + tipsHTML + '</ul>' +
      '</div>' +
      '<button class="btn btn-primary" style="margin-top:16px;width:100%" onclick="takeAnotherIdentifyPhoto()">' +
        '<i class="fas fa-camera-rotate"></i> ' + retryLabel +
      '</button>';
    document.getElementById("aiResult").classList.add("show");
    document.getElementById("recycleGuide").style.display = "none";
    document.getElementById("recycleGuidePlaceholder").style.display = "";
    return;
  }

  /* ── ACCEPTED ── */
  var w  = result.waste;
  var tn = lang === "en" ? w.typeEn : lang === "fr" ? w.typeFr : w.type;
  var ds = (w.desc           && (w.desc[lang]           || w.desc.sw))           || "";
  var sf = (w.safety         && (w.safety[lang]         || w.safety.sw))         || "";
  var rc = (w.recommendation && (w.recommendation[lang] || w.recommendation.sw)) || "";
  var st = (w.steps          && (w.steps[lang]          || w.steps.sw))          || [];
  var mv = (w.market_value   && (w.market_value[lang]   || w.market_value.sw))   || "";
  var ei = (w.env_impact     && (w.env_impact[lang]     || w.env_impact.sw))     || "";

  var conf     = Math.round((result.confidence || w.confidence || 0) * 100);
  var confCol  = conf >= 65 ? "#2E7D32" : conf >= 40 ? "#F57F17" : "#C62828";
  var confBar  = '<div style="background:#e0e0e0;border-radius:4px;height:8px;margin:4px 0 12px">' +
                   '<div style="background:' + confCol + ';width:' + conf + '%;height:8px;border-radius:4px"></div>' +
                 '</div>';

  var reviewNote = result.needs_review
    ? '<div style="background:#fff8e1;border-left:3px solid #FFC107;padding:8px 12px;border-radius:4px;margin:10px 0;font-size:.88rem">' +
        '<i class="fas fa-exclamation-circle" style="color:#F57F17"></i> ' +
        (lang === "en" ? "Lower confidence — verify the result visually before acting."
         : lang === "fr" ? "Confiance plus faible — vérifiez visuellement avant d'agir."
         : "Uhakika ni mdogo — thibitisha matokeo kwa macho kabla ya kutenda.") +
      '</div>'
    : "";

  var demoNote = result.demo
    ? '<div style="background:#e3f2fd;border-left:3px solid #1565C0;padding:8px 12px;border-radius:4px;margin:8px 0;font-size:.85rem">' +
        '<i class="fas fa-info-circle" style="color:#1565C0"></i> ' +
        (lang === "en" ? "Identified by visual analysis (no exact YOLO match). Take a closer photo for better accuracy."
         : lang === "fr" ? "Identifié par analyse visuelle. Prenez une photo plus proche pour plus de précision."
         : "Imetambuliwa kwa uchambuzi wa rangi/sura. Piga picha karibu zaidi kwa usahihi zaidi.") +
      '</div>'
    : "";

  var stepsLabel  = lang === "en" ? "Recycling Steps"       : lang === "fr" ? "Etapes de recyclage" : "Hatua za Kurecycle";
  var safetyLabel = lang === "en" ? "Safety"                : lang === "fr" ? "Securite"            : "Usalama";
  var recLabel    = lang === "en" ? "Recommendation"        : lang === "fr" ? "Recommandation"      : "Ushauri";
  var mvLabel     = lang === "en" ? "Market Value"          : lang === "fr" ? "Valeur marchande"    : "Thamani Sokoni";
  var eiLabel     = lang === "en" ? "Environmental Impact"  : lang === "fr" ? "Impact environnemental": "Athari kwa Mazingira";
  var findLabel   = lang === "en" ? "Find Buyers for This Waste": lang === "fr" ? "Trouver des acheteurs": "Tafuta Wananunua wa Taka Hii";
  var anotherLbl  = lang === "en" ? "Take Another Photo"   : lang === "fr" ? "Prendre une autre photo": "Piga Picha Nyingine";
  var confLabel   = lang === "en" ? "Confidence"           : lang === "fr" ? "Confiance"            : "Uhakika";

  var stepsHTML = st.map(function (s, i) {
    return '<div class="step"><div class="step-num">' + (i + 1) + '</div><div class="step-text">' + escapeHtml(s) + '</div></div>';
  }).join("");

  var infoRow = (mv || ei) ? (
    '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px">' +
      (mv ? '<div style="flex:1;min-width:140px;background:#fff8e1;border-radius:8px;padding:10px 12px">' +
              '<div style="font-size:.78rem;color:#888;margin-bottom:2px"><i class="fas fa-coins" style="color:#F57F17"></i> ' + mvLabel + '</div>' +
              '<div style="font-size:.88rem;font-weight:600">' + escapeHtml(mv) + '</div>' +
            '</div>' : '') +
      (ei ? '<div style="flex:1;min-width:140px;background:#e8f5e9;border-radius:8px;padding:10px 12px">' +
              '<div style="font-size:.78rem;color:#888;margin-bottom:2px"><i class="fas fa-leaf" style="color:#2E7D32"></i> ' + eiLabel + '</div>' +
              '<div style="font-size:.88rem;font-weight:600">' + escapeHtml(ei) + '</div>' +
            '</div>' : '') +
    '</div>'
  ) : "";

  document.getElementById("aiResult").innerHTML =
    '<div style="background:#f1f8e9;border-left:4px solid #2E7D32;border-radius:8px;padding:14px;margin-bottom:14px">' +
      '<div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">' +
        '<span class="waste-type-badge ' + w.badge + '" style="font-size:1.1rem;padding:6px 18px">' + w.icon + ' ' + escapeHtml(tn) + '</span>' +
        '<span style="font-size:.85rem;color:#555">' + confLabel + ': <strong style="color:' + confCol + '">' + conf + '%</strong></span>' +
      '</div>' +
      confBar +
      '<p style="margin:0 0 6px;line-height:1.5">' + escapeHtml(ds) + '</p>' +
      reviewNote + demoNote +
    '</div>' +
    infoRow +
    '<div class="recycle-steps" style="margin-bottom:14px">' +
      '<h4 style="color:var(--primary-dark);margin-bottom:10px"><i class="fas fa-recycle"></i> ' + stepsLabel + ':</h4>' +
      stepsHTML +
    '</div>' +
    '<div style="background:#fce4ec;border-left:4px solid #C62828;border-radius:8px;padding:12px;margin-bottom:14px">' +
      '<h4 style="color:#C62828;margin:0 0 6px"><i class="fas fa-shield-alt"></i> ' + safetyLabel + '</h4>' +
      '<p style="margin:0;line-height:1.5">' + escapeHtml(sf) + '</p>' +
    '</div>' +
    '<div style="background:#e8f5e9;border-left:4px solid #43A047;border-radius:8px;padding:12px;margin-bottom:16px">' +
      '<h4 style="color:#2E7D32;margin:0 0 6px"><i class="fas fa-lightbulb"></i> ' + recLabel + '</h4>' +
      '<p style="margin:0;line-height:1.5">' + escapeHtml(rc) + '</p>' +
    '</div>' +
    '<div style="display:flex;gap:10px;flex-wrap:wrap">' +
      '<button class="btn btn-primary" style="flex:1" onclick="showSection(\'buyers\')">' +
        '<i class="fas fa-store"></i> ' + escapeHtml(findLabel) +
      '</button>' +
      '<button class="btn btn-secondary" style="flex:1" onclick="takeAnotherIdentifyPhoto()">' +
        '<i class="fas fa-camera-rotate"></i> ' + escapeHtml(anotherLbl) +
      '</button>' +
    '</div>';
  document.getElementById("aiResult").classList.add("show");

  document.getElementById("recycleGuide").innerHTML =
    '<div style="margin-bottom:14px">' +
      '<span class="waste-type-badge ' + w.badge + '" style="font-size:1rem;padding:8px 20px">' + w.icon + ' ' + escapeHtml(tn) + '</span>' +
    '</div>' +
    stepsHTML +
    '<div style="background:#fce4ec;border-left:3px solid #C62828;border-radius:6px;padding:10px;margin-top:14px">' +
      '<strong style="color:#C62828"><i class="fas fa-shield-alt"></i> ' + safetyLabel + ':</strong>' +
      '<p style="margin:4px 0 0;font-size:.9rem">' + escapeHtml(sf) + '</p>' +
    '</div>' +
    '<div style="background:#e8f5e9;border-left:3px solid #43A047;border-radius:6px;padding:10px;margin-top:10px">' +
      '<strong style="color:#2E7D32"><i class="fas fa-lightbulb"></i> ' + recLabel + ':</strong>' +
      '<p style="margin:4px 0 0;font-size:.9rem">' + escapeHtml(rc) + '</p>' +
    '</div>' +
    (mv ? '<div style="background:#fff8e1;border-left:3px solid #F57F17;border-radius:6px;padding:10px;margin-top:10px">' +
            '<strong style="color:#E65100"><i class="fas fa-coins"></i> ' + mvLabel + ':</strong>' +
            '<p style="margin:4px 0 0;font-size:.9rem">' + escapeHtml(mv) + '</p>' +
          '</div>' : '') +
    (ei ? '<div style="background:#e8f5e9;border-left:3px solid #388E3C;border-radius:6px;padding:10px;margin-top:10px">' +
            '<strong style="color:#1B5E20"><i class="fas fa-leaf"></i> ' + eiLabel + ':</strong>' +
            '<p style="margin:4px 0 0;font-size:.9rem">' + escapeHtml(ei) + '</p>' +
          '</div>' : '');
  document.getElementById("recycleGuide").style.display = "block";
  document.getElementById("recycleGuidePlaceholder").style.display = "none";

  var toastMsg = lang === "en" ? "Identified: " + tn
               : lang === "fr" ? "Identifie : " + tn
               : "Imetambuliwa: " + tn;
  showToast(toastMsg, "success");
}
function takeAnotherIdentifyPhoto() {
  stopCamera("identify");
  capturedPhotos.identify = null;
  var preview = document.getElementById("identifyPreview");
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

function closeAnalysisModal() {
  var modal = document.getElementById("analysisModal");
  if (!modal) return;
  modal.classList.remove("open");
  modal.setAttribute("aria-hidden", "true");
}

/* ─── Buyers ────────────────────────────────────────────────── */
async function loadBuyers() {
  var tf = document.getElementById("buyerTypeFilter").value;
  var sf = (document.getElementById("buyerSearch").value || "").trim();
  var params = new URLSearchParams();
  if (tf && tf !== "all") params.set("type", tf);
  if (sf) params.set("search", sf);
  try {
    var data = await apiJSON(API.buyers + "?" + params.toString());
    renderBuyersFromAPI(data.buyers || []);
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

function renderBuyersFromAPI(f) {
  if (!buyerMap) initBuyerMap();
  buyerMarkers.forEach(function (m) { buyerMap.removeLayer(m); });
  buyerMarkers = [];
  var list = document.getElementById("buyersList");
  if (!list) return;
  list.innerHTML = "";

  if (!f.length) {
    list.innerHTML =
      '<div style="text-align:center;padding:40px;color:var(--text-light)">' +
        '<i class="fas fa-search" style="font-size:2rem;margin-bottom:10px;display:block"></i>' +
        '<p>' + window.t("no_buyers") + '</p>' +
      '</div>';
    return;
  }

  var cl = window.t("contact");
  f.forEach(function (b) {
    if (b.lat != null && b.lng != null) {
      var mk = L.marker([b.lat, b.lng]).addTo(buyerMap)
        .bindPopup("<b>" + escapeHtml(b.name) + "</b><br>" + escapeHtml(b.location));
      buyerMarkers.push(mk);
    }
    var ts = (b.types || []).map(function (type) {
      return '<span>' + window.t(type) + '</span>';
    }).join("");
    list.innerHTML +=
      '<div class="buyer-card">' +
        '<div class="buyer-avatar"><i class="fas fa-store"></i></div>' +
        '<div class="buyer-info">' +
          '<h4>' + escapeHtml(b.name) + '</h4>' +
          '<p>📍 ' + escapeHtml(b.location) + ' &bull; 📞 ' + escapeHtml(b.phone) + '</p>' +
          '<div class="buyer-types">' + ts + '</div>' +
        '</div>' +
        '<button class="buyer-contact-btn" onclick="contactBuyer(\'' + escapeJs(b.phone) + '\')">' +
          '<i class="fas fa-phone"></i> ' + cl +
        '</button>' +
      '</div>';
  });
}

function filterBuyers() { loadBuyers(); }

function contactBuyer(phone) {
  window.location.href = "tel:" + phone;
}

/* ─── Authority portal ───────────────────────────────────────── */
async function submitAuthority() {
  var data = {
    name:           document.getElementById("authorityName").value.trim(),
    authority_type: document.getElementById("authorityType").value,
    email:          document.getElementById("authorityEmail").value.trim(),
    phone:          document.getElementById("authorityPhone").value.trim(),
    location:       document.getElementById("authorityLocation").value.trim(),
    description:    document.getElementById("authorityDescription").value.trim(),
    password:       document.getElementById("authorityPassword").value
  };
  if (!data.name || !data.email || !data.phone || !data.location) {
    showToast(window.t("authority_required"), "warning");
    return;
  }
  try {
    await apiJSON("/api/authorities", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
    showToast(window.t("authority_saved"), "success");
    document.getElementById("authorityLoginUsername").value = data.email;
    showAuthorityAuth("signin");
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

function showAuthorityAuth(mode) {
  var signIn    = mode === "signin";
  var signInForm = document.getElementById("authoritySignInForm");
  var signUpForm = document.getElementById("authoritySignUpForm");
  if (!signInForm || !signUpForm) return;
  signInForm.classList.toggle("active", signIn);
  signUpForm.classList.toggle("active", !signIn);
  document.getElementById("authoritySignInTab").classList.toggle("active", signIn);
  document.getElementById("authoritySignUpTab").classList.toggle("active", !signIn);
}

async function authorityLogin() {
  try {
    var result = await apiJSON("/api/authority/login", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: document.getElementById("authorityLoginUsername").value.trim(),
        password: document.getElementById("authorityLoginPassword").value
      })
    });
    var data = await apiJSON("/api/authority/dashboard");

    ["authoritySignInForm", "authoritySignUpForm"].forEach(function (id) {
      var el = document.getElementById(id); if (el) el.style.display = "none";
    });
    var tabs = document.querySelector(".portal-tabs");
    if (tabs) tabs.style.display = "none";
    document.getElementById("authorityPanel").style.display = "block";

    window.lastAuthorityData    = data;
    window.lastAuthorityReports = data.reports || [];
    refreshAuthorityDashboardLang(data);
    showToast(window.t("authority_logged_in"), "success");
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

/**
 * Rebuilds all dynamic content inside the authority dashboard in the
 * currently selected language.  Called from authorityLogin AND from
 * applyLocale() every time the user switches language.
 */
function refreshAuthorityDashboardLang(data) {
  data = data || window.lastAuthorityData || {};

  /* Dashboard heading — authority name (server-provided, no translation needed) */
  var nameEl = document.getElementById("authorityDisplayName");
  var typeEl = document.getElementById("authorityDisplayType");
  if (nameEl && data.authority_name) nameEl.textContent = data.authority_name;
  if (typeEl && data.authority_type) typeEl.textContent = data.authority_type;

  /* Pending count */
  var pc = document.getElementById("authorityPendingCount");
  if (pc) pc.textContent = data.pending_count || 0;

  /* Tasks list — server now returns i18n keys, translate them */
  var tasksEl = document.getElementById("authorityTasks");
  if (tasksEl) {
    tasksEl.innerHTML = (data.tasks || []).map(function (key) {
      /* t(key) looks up the key; if not found it returns the key itself as fallback */
      return '<p style="padding:8px 0;border-bottom:1px solid #eee;line-height:1.5">' +
               escapeHtml(window.t(key)) +
             '</p>';
    }).join("") || '<p style="color:var(--text-light)">—</p>';
  }

  /* Reports table */
  renderAuthorityReports(window.lastAuthorityReports || data.reports || []);
}

async function refreshAuthorityReports() {
  try {
    var data = await apiJSON("/api/authority/dashboard");
    window.lastAuthorityData    = data;
    window.lastAuthorityReports = data.reports || [];
    refreshAuthorityDashboardLang(data);
  } catch (_) {}
}

function renderAuthorityReports(reports) {
  var target = document.getElementById("authorityReports");
  if (!target) return;
  window.lastAuthorityReports = reports;

  if (!reports || !reports.length) {
    target.innerHTML = '<p style="color:var(--text-light);padding:16px">' + window.t("authority_no_reports") + '</p>';
    return;
  }

  target.innerHTML = reports.map(function (report) {
    var coordinates = (report.lat != null && report.lng != null)
      ? '<a href="https://www.google.com/maps?q=' + report.lat + ',' + report.lng + '" target="_blank" rel="noopener">' +
          escapeHtml(report.location || (report.lat + ", " + report.lng)) + '</a>'
      : escapeHtml(report.location || window.t("not_set"));

    var photo = report.photo
      ? '<img src="' + escapeHtml(report.photo) + '" alt="' + window.t("report_photo_title") + '" style="width:100%;max-height:260px;object-fit:cover;border-radius:10px;margin-top:10px">'
      : '<p><small>' + window.t("photo_missing") + '</small></p>';

    var meaning = escapeHtml(report.photo_meaning || window.t("photo_missing"));

    var statusKey = report.status === "resolved" ? "status_resolved"
                  : report.status === "in_progress" ? "status_progress"
                  : "status_pending";

    return '<div class="authority-report" style="padding:14px 0;border-bottom:1px solid #eee">' +
      '<strong>' + window.t("report_content") + ':</strong> ' + escapeHtml(report.description) + '<br>' +
      '<strong>' + window.t("report_location_lbl") + ':</strong> ' + coordinates + '<br>' +
      '<strong>' + window.t("report_status_lbl") + ':</strong> ' + window.t(statusKey) +
      photo +
      '<p style="margin-top:10px"><strong>' + window.t("photo_meaning") + ':</strong> ' + meaning + '</p>' +
      '<div style="margin-top:8px;display:flex;gap:8px;flex-wrap:wrap">' +
        '<button class="btn btn-secondary" style="padding:6px 10px" onclick="updateAuthorityReport(' + report.id + ',\'in_progress\')">' +
          '<i class="fas fa-play"></i> ' + window.t("btn_handle") +
        '</button>' +
        '<button class="btn btn-primary" style="padding:6px 10px" onclick="updateAuthorityReport(' + report.id + ',\'resolved\')">' +
          '<i class="fas fa-check"></i> ' + window.t("btn_resolved") +
        '</button>' +
        '<button class="btn btn-secondary" style="padding:6px 10px" onclick="deleteAuthorityReport(' + report.id + ')">' +
          '<i class="fas fa-trash"></i> ' + window.t("btn_delete") +
        '</button>' +
      '</div></div>';
  }).join("");
}

async function updateAuthorityReport(reportId, status) {
  try {
    await apiJSON("/api/authority/reports/" + reportId, {
      method: "PUT", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: status })
    });
    await refreshAuthorityReports();
    showToast(window.t("report_updated"), "success");
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

async function deleteAuthorityReport(reportId) {
  if (!window.confirm(window.t("confirm_delete_report"))) return;
  try {
    await apiJSON("/api/authority/reports/" + reportId, { method: "DELETE" });
    await refreshAuthorityReports();
    showToast(window.t("report_deleted"), "success");
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

/* ─── Admin portal ───────────────────────────────────────────── */
async function adminLogin() {
  try {
    await apiJSON("/api/admin/login", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: document.getElementById("adminUsername").value.trim(),
        password: document.getElementById("adminPassword").value
      })
    });
    var data = await apiJSON("/api/admin/dashboard");
    document.getElementById("loginSection").style.display = "none";
    document.getElementById("adminPanel").style.display = "block";

    window.lastAdminData  = data;
    window.lastAdminUsers = data.users || [];
    refreshAdminDashboardLang(data);
    showToast(window.t("admin_logged_in"), "success");
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

/* Rebuild all dynamic admin content in the current language.
   Called from adminLogin AND from applyLocale on every language switch. */
function refreshAdminDashboardLang(data) {
  data = data || window.lastAdminData || {};
  var stats = data.stats || {};

  /* ── Stats bar ── */
  var statsEl = document.getElementById("adminStats");
  if (statsEl) {
    statsEl.innerHTML = [
      [window.t("stat_label_reports"),  stats.reports    || 0, "fas fa-file-alt",     "#1565C0"],
      [window.t("stat_label_resolved"), stats.resolved   || 0, "fas fa-check-circle", "#2E7D32"],
      [window.t("stat_label_buyers"),   stats.buyers     || 0, "fas fa-store",        "#E65100"],
      [window.t("stat_label_auths"),    (data.authorities || []).length, "fas fa-landmark", "#6A1B9A"]
    ].map(function (item) {
      return '<div class="stat-card">' +
        '<i class="' + item[2] + '" style="font-size:1.6rem;color:' + item[3] + ';margin-bottom:4px"></i>' +
        '<div class="stat-number" style="color:' + item[3] + '">' + item[1] + '</div>' +
        '<div class="stat-label">' + item[0] + '</div>' +
      '</div>';
    }).join("");
  }

  /* ── Task cards title ── */
  var titleEl = document.getElementById("adminTasksTitle");
  if (titleEl) titleEl.textContent = window.t("admin_tasks_title");

  /* ── Task cards ── */
  var cardsEl = document.getElementById("adminTaskCards");
  if (cardsEl) {
    var TASKS = [
      { key: "task_manage_users",   icon: "👥", color: "blue",   desc_key: "task_manage_users_desc"   },
      { key: "task_manage_reports", icon: "📋", color: "green",  desc_key: "task_manage_reports_desc" },
      { key: "task_manage_buyers",  icon: "🏪", color: "orange", desc_key: "task_manage_buyers_desc"  },
      { key: "task_manage_auths",   icon: "🏛️", color: "teal",   desc_key: "task_manage_auths_desc"   },
      { key: "task_view_stats",     icon: "📊", color: "purple", desc_key: "task_view_stats_desc"     },
      { key: "task_security",       icon: "🔒", color: "red",    desc_key: "task_security_desc"       },
    ];
    cardsEl.innerHTML = TASKS.map(function (task) {
      return '<div class="admin-task-card ' + task.color + '">' +
        '<div class="task-icon">' + task.icon + '</div>' +
        '<h4>' + window.t(task.key) + '</h4>' +
        '<p>' + window.t(task.desc_key) + '</p>' +
      '</div>';
    }).join("");
  }

  /* ── User table ── */
  renderAdminUsers(data.users || window.lastAdminUsers || []);

  /* ── Edit modal labels (update if open) ── */
  var editModal = document.getElementById("editUserModal");
  if (editModal && editModal.classList.contains("open")) {
    var lang = window.currentLang || "sw";
    var titleMEl = document.getElementById("editModalTitle");
    var saveMEl  = document.getElementById("editSaveLabel");
    var cancelMEl= document.getElementById("editCancelLabel");
    var pwdLEl   = document.getElementById("editPwdLabel");
    if (titleMEl)  titleMEl.textContent  = lang === "en" ? "Edit User" : lang === "fr" ? "Modifier l'utilisateur" : "Hariri Mtumiaji";
    if (saveMEl)   saveMEl.textContent   = lang === "en" ? "Save"   : lang === "fr" ? "Enregistrer" : "Hifadhi";
    if (cancelMEl) cancelMEl.textContent = lang === "en" ? "Cancel" : lang === "fr" ? "Annuler"     : "Ghairi";
    if (pwdLEl)    pwdLEl.textContent    = lang === "en" ? "New Password (leave blank to keep current)"
                                         : lang === "fr" ? "Nouveau mot de passe (laisser vide)"
                                         : "Nenosiri Jipya (acha wazi kubaki sawa)";
  }
}

async function adminLogout() {
  await apiJSON("/api/admin/logout", { method: "POST" });
  window.lastAdminData  = null;
  window.lastAdminUsers = null;
  document.getElementById("loginSection").style.display = "block";
  document.getElementById("adminPanel").style.display = "none";
  switchLoginTab("admin");
}

/* ═══════════════════════════════════════════════════════════
   TAB SWITCHER — Admin Login / User Login
═══════════════════════════════════════════════════════════ */
function switchLoginTab(tab) {
  var isAdmin = tab === "admin";
  document.getElementById("tabAdmin").classList.toggle("active", isAdmin);
  document.getElementById("tabUser").classList.toggle("active", !isAdmin);
  document.getElementById("adminLoginForm").classList.toggle("active", isAdmin);
  document.getElementById("userLoginForm").classList.toggle("active", !isAdmin);
}

/* ═══════════════════════════════════════════════════════════
   USER LOGIN  (users created via admin panel)
═══════════════════════════════════════════════════════════ */
async function userLogin() {
  var identifier = document.getElementById("userLoginUsername").value.trim();
  var password   = document.getElementById("userLoginPassword").value;

  if (!identifier || !password) {
    showToast(window.t("form_required"), "warning");
    return;
  }

  try {
    var result = await apiJSON("/api/user/login", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ username: identifier, password: password })
    });

    /* If the user has the admin role, give them the full admin dashboard */
    if (result.role === "admin") {
      var data = await apiJSON("/api/user/dashboard");
      document.getElementById("loginSection").style.display = "none";
      document.getElementById("adminPanel").style.display = "block";
      window.lastAdminData  = data;
      window.lastAdminUsers = data.users || [];
      refreshAdminDashboardLang(data);
      showToast(window.t("admin_logged_in"), "success");
      return;
    }

    /* All other roles → user panel */
    document.getElementById("loginSection").style.display = "none";
    document.getElementById("userPanel").style.display = "block";
    window.lastUserData = result;
    renderUserDashboard(result);
    showToast(window.t("user_logged_in"), "success");

  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

async function userLogout() {
  try { await apiJSON("/api/user/logout", { method: "POST" }); } catch (_) {}
  window.lastUserData = null;
  document.getElementById("loginSection").style.display = "block";
  document.getElementById("userPanel").style.display = "none";
  document.getElementById("userLoginUsername").value = "";
  document.getElementById("userLoginPassword").value = "";
  switchLoginTab("user");
  showToast(window.t("user_logged_out"), "info");
}

/* ═══════════════════════════════════════════════════════════
   USER DASHBOARD  — shown for non-admin roles
═══════════════════════════════════════════════════════════ */
var ROLE_LABELS = {
  admin:     { sw: "Msimamizi",     en: "Administrator",   fr: "Administrateur" },
  reporter:  { sw: "Mripoti",       en: "Reporter",        fr: "Rapporteur" },
  buyer:     { sw: "Mnunuzi",       en: "Buyer",           fr: "Acheteur" },
  authority: { sw: "Mamlaka",       en: "Authority",       fr: "Autorité" },
  support:   { sw: "Msaidizi",      en: "Support",         fr: "Support" },
};

function renderUserDashboard(user) {
  user = user || window.lastUserData || {};
  var lang   = window.currentLang || "sw";
  var role   = user.role || "reporter";
  var rlObj  = ROLE_LABELS[role] || ROLE_LABELS.reporter;
  var rlText = rlObj[lang] || rlObj.sw;

  /* Welcome card */
  var nameEl = document.getElementById("userWelcomeName");
  var roleEl = document.getElementById("userWelcomeRole");
  if (nameEl) nameEl.textContent = window.t("user_dashboard_welcome") + ", " + escapeHtml(user.username || "—") + "!";
  if (roleEl) roleEl.textContent = window.t("user_role_label") + ": " + rlText;

  /* Stats */
  var stats   = user.stats || {};
  var gridEl  = document.getElementById("userInfoGrid");
  if (gridEl) {
    var items = [
      { icon: "📋", val: stats.reports  || 0, lbl: window.t("stat_label_reports")  },
      { icon: "✅", val: stats.resolved || 0, lbl: window.t("stat_label_resolved") },
      { icon: "🏪", val: stats.buyers   || 0, lbl: window.t("stat_label_buyers")   },
    ];
    gridEl.innerHTML = items.map(function (item) {
      return '<div class="user-info-card">' +
        '<div class="ui-icon">' + item.icon + '</div>' +
        '<div class="ui-val">' + item.val + '</div>' +
        '<div class="ui-lbl">' + escapeHtml(item.lbl) + '</div>' +
      '</div>';
    }).join("");
  }

  /* Role-specific content */
  var contentEl = document.getElementById("userRoleContent");
  if (!contentEl) return;

  var reports = user.reports || [];

  /* Reporter / Support / Authority / Buyer — show recent reports */
  var recentTitle = window.t("user_panel_reports");
  var reportRows  = reports.slice(0, 10).map(function (r) {
    var statusKey   = r.status === "resolved" ? "status_resolved"
                    : r.status === "in_progress" ? "status_progress" : "status_pending";
    var statusClass = r.status === "resolved" ? "resolved"
                    : r.status === "in_progress" ? "progress" : "pending";
    return '<div class="report-item">' +
      '<div class="report-img">' +
        (r.photo ? '<img src="' + r.photo + '" alt="report">' : '<i class="fas fa-camera"></i>') +
      '</div>' +
      '<div class="report-details">' +
        '<h4>' + escapeHtml(r.description) + '</h4>' +
        '<p>📍 ' + escapeHtml(r.location || window.t("not_set")) + '</p>' +
      '</div>' +
      '<span class="report-status status-' + statusClass + '">' + window.t(statusKey) + '</span>' +
    '</div>';
  }).join("") || '<p style="color:var(--text-light);padding:12px 0">' + window.t("no_reports") + '</p>';

  contentEl.innerHTML =
    '<div class="card">' +
      '<div class="card-header" style="background:linear-gradient(135deg,#2E7D32,#1B5E20)">' +
        '<i class="fas fa-list-check"></i>' +
        '<h3>' + escapeHtml(recentTitle) + '</h3>' +
      '</div>' +
      '<div class="card-body">' + reportRows + '</div>' +
    '</div>';
}

/* Re-render user panel on language change */
function refreshUserDashboardLang() {
  if (window.lastUserData) renderUserDashboard(window.lastUserData);
}

function renderAdminUsers(users) {
  window.lastAdminUsers = users;
  var box = document.getElementById("adminUsers");
  if (!box) return;

  if (!users || !users.length) {
    box.innerHTML = '<p style="color:var(--text-light);padding:12px 0">' + window.t("admin_no_users") + '</p>';
    return;
  }

  /* Role → badge class mapping */
  var roleClass = { admin:"role-admin", reporter:"role-reporter", buyer:"role-buyer", authority:"role-authority", support:"role-support" };

  var rows = users.map(function (user) {
    var badge = '<span class="role-badge ' + (roleClass[user.role] || "role-support") + '">' + escapeHtml(user.role) + '</span>';
    return '<tr>' +
      '<td><strong>' + escapeHtml(user.username) + '</strong></td>' +
      '<td>' + escapeHtml(user.email) + '</td>' +
      '<td>' + badge + '</td>' +
      '<td>' +
        '<button class="btn btn-secondary" style="padding:4px 10px;margin-right:6px" title="' + window.t("user_management") + '" ' +
          'onclick="openEditModal(' + user.id + ',\'' + escapeJs(user.username) + '\',\'' + escapeJs(user.email) + '\',\'' + escapeJs(user.role) + '\')">' +
          '<i class="fas fa-pen"></i>' +
        '</button>' +
        '<button class="btn btn-secondary" style="padding:4px 10px" title="' + window.t("btn_delete") + '" onclick="deleteAdminUser(' + user.id + ')">' +
          '<i class="fas fa-trash"></i>' +
        '</button>' +
      '</td>' +
    '</tr>';
  }).join("");

  box.innerHTML =
    '<table class="user-table">' +
      '<thead><tr>' +
        '<th>' + window.t("label_username") + '</th>' +
        '<th>' + window.t("email") + '</th>' +
        '<th>' + window.t("label_role") + '</th>' +
        '<th style="width:100px">' + window.t("user_management") + '</th>' +
      '</tr></thead>' +
      '<tbody>' + rows + '</tbody>' +
    '</table>';
}

/* ── Edit modal helpers ── */
function openEditModal(userId, username, email, role) {
  document.getElementById("editUserId").value     = userId;
  document.getElementById("editUsername").value   = username;
  document.getElementById("editEmail").value      = email;
  document.getElementById("editRole").value       = role;
  document.getElementById("editPassword").value   = "";

  var lang = window.currentLang || "sw";
  document.getElementById("editModalTitle").textContent =
    lang === "en" ? "Edit User" : lang === "fr" ? "Modifier l'utilisateur" : "Hariri Mtumiaji";
  document.getElementById("editSaveLabel").textContent =
    lang === "en" ? "Save" : lang === "fr" ? "Enregistrer" : "Hifadhi";
  document.getElementById("editCancelLabel").textContent =
    lang === "en" ? "Cancel" : lang === "fr" ? "Annuler" : "Ghairi";
  document.getElementById("editPwdLabel").textContent =
    lang === "en" ? "New Password (leave blank to keep current)"
    : lang === "fr" ? "Nouveau mot de passe (laisser vide pour conserver)"
    : "Nenosiri Jipya (acha wazi kubaki sawa)";

  document.getElementById("editUserModal").classList.add("open");
}

function closeEditModal() {
  document.getElementById("editUserModal").classList.remove("open");
}

async function saveEditUser() {
  var userId   = document.getElementById("editUserId").value;
  var username = document.getElementById("editUsername").value.trim();
  var email    = document.getElementById("editEmail").value.trim();
  var role     = document.getElementById("editRole").value;
  var password = document.getElementById("editPassword").value;

  if (!username || !email) {
    showToast(window.t("form_required"), "warning");
    return;
  }
  try {
    await apiJSON("/api/admin/users/" + userId, {
      method: "PUT", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, email: email, role: role,
                             permissions: [], password: password })
    });
    closeEditModal();
    var data = await apiJSON("/api/admin/dashboard");
    window.lastAdminData  = data;
    window.lastAdminUsers = data.users || [];
    renderAdminUsers(window.lastAdminUsers);
    showToast(window.t("user_updated"), "success");
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

async function createAdminUser() {
  var username = document.getElementById("userUsername").value.trim();
  var email    = document.getElementById("userEmail").value.trim();
  var password = document.getElementById("userPassword").value;
  var role     = document.getElementById("userRole").value;

  if (!username || !email || !password) {
    showToast(window.t("form_required"), "warning");
    return;
  }
  try {
    await apiJSON("/api/admin/users", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: username, email: email,
                             password: password, role: role, permissions: [] })
    });
    /* Clear form */
    document.getElementById("userUsername").value = "";
    document.getElementById("userEmail").value    = "";
    document.getElementById("userPassword").value = "";
    document.getElementById("userRole").value     = "admin";
    showToast(window.t("user_created"), "success");
    var data = await apiJSON("/api/admin/dashboard");
    window.lastAdminData  = data;
    window.lastAdminUsers = data.users || [];
    renderAdminUsers(window.lastAdminUsers);
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

async function deleteAdminUser(userId) {
  if (!window.confirm(window.t("confirm_delete_user"))) return;
  try {
    await apiJSON("/api/admin/users/" + userId, { method: "DELETE" });
    var data = await apiJSON("/api/admin/dashboard");
    window.lastAdminData  = data;
    window.lastAdminUsers = data.users || [];
    renderAdminUsers(window.lastAdminUsers);
    showToast(window.t("user_deleted"), "success");
  } catch (err) { showToast("❌ " + err.message, "warning"); }
}

/* editAdminUser — replaced by openEditModal / saveEditUser (modal in admin.html) */

/* ─── Camera ─────────────────────────────────────────────────── */
async function startCamera(kind) {
  var panel = document.getElementById(kind + "CameraPanel");
  var video = document.getElementById(kind + "Camera");
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    showToast(window.t("camera_unavailable"), "warning");
    return;
  }
  try {
    cameraStreams[kind] = await navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: "environment" } }, audio: false });
    video.srcObject = cameraStreams[kind];
    panel.classList.add("open");
  } catch (err) {
    showToast(window.t("camera_allow"), "warning");
  }
}

function stopCamera(kind) {
  if (cameraStreams[kind]) {
    cameraStreams[kind].getTracks().forEach(function (track) { track.stop(); });
    cameraStreams[kind] = null;
  }
  var panel = document.getElementById(kind + "CameraPanel");
  if (panel) panel.classList.remove("open");
}

function captureCameraPhoto(kind) {
  var video  = document.getElementById(kind + "Camera");
  var canvas = document.getElementById(kind + "Canvas");
  if (!video.videoWidth || !video.videoHeight) {
    showToast(window.t("camera_not_ready"), "warning");
    return;
  }
  canvas.width  = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
  canvas.toBlob(function (blob) {
    capturedPhotos[kind] = blob;
    var preview = document.getElementById(kind + "Preview");
    preview.src = URL.createObjectURL(blob);
    preview.classList.add("show");
    document.getElementById(kind + "UploadArea").style.display = "none";
    stopCamera(kind);
    if (kind === "report" && navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function (pos) {
        markReportLocation(pos.coords.latitude, pos.coords.longitude);
      });
    }
    if (kind === "identify") identifyCapturedPhoto(blob);
  }, "image/jpeg", 0.9);
}

/* ─── Map helpers ────────────────────────────────────────────── */
function setReportCoordinates(lat, lng) {
  document.getElementById("reportLat").value     = Number(lat).toFixed(7);
  document.getElementById("reportLng").value     = Number(lng).toFixed(7);
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
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "&copy; OpenStreetMap" }).addTo(reportMap);
  reportMap.on("click", function (e) { markReportLocation(e.latlng.lat, e.latlng.lng); });
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (p) {
      markReportLocation(p.coords.latitude, p.coords.longitude);
    });
  }
  setTimeout(function () { reportMap.invalidateSize(); }, 300);
}

function initBuyerMap() {
  if (buyerMap) return;
  buyerMap = L.map("buyerMap").setView([-6.7924, 39.2083], 12);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", { attribution: "&copy; OpenStreetMap" }).addTo(buyerMap);
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (p) {
      buyerMap.setView([p.coords.latitude, p.coords.longitude], 13);
      var latEl = document.getElementById("regLat");
      var lngEl = document.getElementById("regLng");
      if (latEl) latEl.value = p.coords.latitude.toFixed(7);
      if (lngEl) lngEl.value = p.coords.longitude.toFixed(7);
    });
  }
  setTimeout(function () { buyerMap.invalidateSize(); }, 300);
}

/* ─── Chatbot ─────────────────────────────────────────────────── */
var QUICK_QUESTIONS = {
  sw: ["Jinsi ya kurecycle plastiki?", "Aina za taka ni zipi?", "Ninapataje mnunuzi?", "Bei ya taka ni ngapi?", "Jinsi ya kutuma ripoti?", "Compost ni nini?"],
  en: ["How do I recycle plastic?", "What are the waste types?", "How do I find a buyer?", "What is the price of waste?", "How do I submit a report?", "What is composting?"],
  fr: ["Comment recycler le plastique ?", "Quels sont les types de déchets ?", "Comment trouver un acheteur ?", "Quel est le prix des déchets ?", "Comment envoyer un signalement ?", "Qu'est-ce que le compost ?"]
};

var WELCOME_MSG = {
  sw: "Jambo! 👋 Mimi ni TakaSmart Assistant. Uliza swali lolote kuhusu taka, recycling, wananunua au mfumo. 🌿",
  en: "Hello! 👋 I'm TakaSmart Assistant. Ask me anything about waste, recycling, buyers, or the platform. 🌿",
  fr: "Bonjour ! 👋 Je suis l'assistant TakaSmart. Posez n'importe quelle question sur les déchets, le recyclage ou la plateforme. 🌿"
};

function setChatLang(lang, btn) {
  /* Sync local chatLang var and window.chatLang */
  window.chatLang = lang;
  chatLang = lang;
  /* Sync chat lang bar active state */
  document.querySelectorAll(".chat-lang-bar button").forEach(function (b) { b.classList.remove("active"); });
  if (btn) {
    btn.classList.add("active");
  } else {
    document.querySelectorAll(".chat-lang-bar button").forEach(function (b) {
      if (b.dataset.lang === lang) b.classList.add("active");
    });
  }
  /* Reset and re-render chatbot in the new language */
  var messages = document.getElementById("chatMessages");
  if (!messages) return;
  messages.innerHTML = "";
  appendChatMessage(WELCOME_MSG[lang] || WELCOME_MSG.sw, "bot");
  renderQQ();
}

function toggleChat() {
  var w = document.getElementById("chatWindow");
  if (!w) return;
  w.classList.toggle("open");
  var badge = document.querySelector("#chatToggle .badge");
  if (badge) badge.remove();
  var messages = document.getElementById("chatMessages");
  if (w.classList.contains("open") && messages && !messages.children.length) {
    appendChatMessage(WELCOME_MSG[window.chatLang] || WELCOME_MSG.sw, "bot");
    renderQQ();
  }
}

function renderQQ() { /* quick questions disabled */ }
function sendQQ(q) { /* quick questions disabled */ }

async function sendChat() {
  var input   = document.getElementById("chatInput");
  var message = input.value.trim();
  if (!message) return;
  appendChatMessage(message, "user");
  input.value = "";
  var req = { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: message, lang: window.chatLang }) };
  try {
    var result = await apiJSON(API.chat, req);
    appendChatMessage(result.reply || window.t("chat_no_reply"), "bot");
  } catch (firstErr) {
    try {
      var result2 = await apiJSON(API.chat + "?retry=1", req);
      appendChatMessage(result2.reply || window.t("chat_no_reply"), "bot");
    } catch (secondErr) {
      appendChatMessage(window.t("chat_server_down"), "bot");
    }
  }
}

function formatBotMessage(text) {
  /* Convert plain-text markdown-style formatting to HTML */
  var html = text
    /* escape HTML first */
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    /* bold: **text** */
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    /* headers: ### text  or  ## text */
    .replace(/^###\s+(.+)$/gm, '<p class="cb-h3">$1</p>')
    .replace(/^##\s+(.+)$/gm,  '<p class="cb-h2">$1</p>')
    /* numbered list: lines starting with 1️⃣ … or 1. */
    .replace(/^(\d+[️⃣]?\.?\s)/gm, '<span class="cb-num">$1</span>')
    /* bullet: lines starting with •, -, ✅, 🚫, ⚠️, 💡, 📌, ➡️ emoji */
    .replace(/^([•\-])\s/gm, '<span class="cb-bullet">•</span> ')
    /* emoji-led lines — keep as-is, just wrap */
    /* horizontal rule: --- */
    .replace(/^---$/gm, '<hr class="cb-hr">')
    /* newlines → <br> */
    .replace(/\n/g, "<br>");
  return html;
}

function appendChatMessage(message, who) {
  var box = document.getElementById("chatMessages");
  var div = document.createElement("div");
  div.className = "msg " + (who === "user" ? "msg-user" : "msg-bot");
  if (who === "bot") {
    var formatted = formatBotMessage(String(message || ""));
    div.innerHTML =
      '<div class="bot-icon"><i class="fas fa-robot"></i> TakaSmart</div>' +
      '<div class="cb-body">' + formatted + '</div>';
  } else {
    div.textContent = message;
  }
  box.appendChild(div);
  box.scrollTop = box.scrollHeight;
}

/* ─── DOMContentLoaded ─────────────────────────────────────── */
document.addEventListener("DOMContentLoaded", function () {
  /* Sync local vars from i18n globals (i18n.js loads before app.js) */
  currentLang = window.currentLang || "sw";
  chatLang    = window.chatLang    || "sw";

  /* GPS kwa fomu ya usajili */
  if (document.getElementById("regLat") && navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (p) {
      document.getElementById("regLat").value = p.coords.latitude.toFixed(7);
      document.getElementById("regLng").value = p.coords.longitude.toFixed(7);
    });
  }

  /* Ukurasa mkuu */
  if (document.getElementById("section-home")) {
    loadStats();
    loadRecentReports();
    showSection("home");
    /* Sync chat lang bar na chatbot welcome */
    setChatLang(window.currentLang || "sw");
  }
});
