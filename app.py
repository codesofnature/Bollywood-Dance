<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
  <meta name="theme-color" content="#07070f" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <title>BollyFusion Academy</title>

  <style>
    :root {
      --bg: #07070f;
      --text: #ffffff;
      --muted: rgba(255, 255, 255, .72);
      --line: rgba(255, 255, 255, .12);
      --panel: rgba(255, 255, 255, .08);
      --gold: #ffcf5f;
      --pink: #ff5fa2;
      --cyan: #55c6ff;
      --green: #43e97b;
    }

    * {
      box-sizing: border-box;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(255, 95, 162, .18), transparent 30%),
        radial-gradient(circle at top right, rgba(85, 198, 255, .16), transparent 25%),
        var(--bg);
      color: var(--text);
      line-height: 1.45;
    }

    .app {
      min-height: 100vh;
      padding:
        calc(18px + env(safe-area-inset-top))
        calc(16px + env(safe-area-inset-right))
        calc(98px + env(safe-area-inset-bottom))
        calc(16px + env(safe-area-inset-left));
    }

    .shell {
      max-width: 1100px;
      margin: 0 auto;
    }

    .screen {
      display: none;
    }

    .screen.active {
      display: block;
      animation: fade .25s ease;
    }

    @keyframes fade {
      from {
        opacity: 0;
        transform: translateY(8px);
      }
      to {
        opacity: 1;
        transform: none;
      }
    }

    .hero,
    .panel {
      border: 1px solid var(--line);
      background: var(--panel);
      box-shadow: 0 18px 60px rgba(0, 0, 0, .35);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
    }

    .hero {
      border-radius: 32px;
      padding: 28px 20px;
      background:
        linear-gradient(135deg, rgba(255, 95, 162, .18), rgba(85, 198, 255, .12), rgba(255, 207, 95, .14));
    }

    .panel {
      border-radius: 24px;
      padding: 20px;
      margin-top: 16px;
    }

    h1 {
      margin: 12px 0 8px;
      font-size: clamp(2rem, 5vw, 3.8rem);
      line-height: 1.03;
      letter-spacing: -.04em;
    }

    h2 {
      margin: 0 0 8px;
      font-size: 1.35rem;
    }

    h3 {
      margin: 0;
      font-size: 1.05rem;
    }

    .gradient {
      background: linear-gradient(90deg, var(--gold), var(--pink), var(--cyan));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
      color: transparent;
    }

    .muted {
      color: var(--muted);
    }

    .btn {
      width: 100%;
      min-height: 52px;
      border: 0;
      border-radius: 16px;
      padding: 14px 16px;
      font-size: 16px;
      font-weight: 800;
      font-family: inherit;
      cursor: pointer;
    }

    .btn.primary {
      background: linear-gradient(90deg, var(--gold), var(--pink));
      color: #171204;
    }

    .btn.secondary {
      background: rgba(255, 255, 255, .09);
      color: var(--text);
      border: 1px solid var(--line);
    }

    .btn:disabled {
      opacity: .35;
      cursor: not-allowed;
    }

    .row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-top: 16px;
    }

    .input {
      width: 100%;
      min-height: 52px;
      border-radius: 16px;
      border: 1px solid var(--line);
      background: rgba(255, 255, 255, .08);
      color: var(--text);
      padding: 14px;
      font-size: 16px;
      font-family: inherit;
      outline: none;
    }

    .input:focus {
      border-color: var(--cyan);
      box-shadow: 0 0 0 3px rgba(85, 198, 255, .14);
    }

    label {
      display: block;
      font-weight: 700;
      margin: 14px 0 8px;
    }

    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }

    .card {
      border: 1px solid var(--line);
      border-radius: 24px;
      overflow: hidden;
      background: rgba(255, 255, 255, .07);
    }

    .media {
      position: relative;
      aspect-ratio: 16 / 10;
      background: linear-gradient(135deg, rgba(255, 95, 162, .35), rgba(85, 198, 255, .28));
    }

    .media img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
    }

    .badge {
      position: absolute;
      top: 12px;
      left: 12px;
      padding: 7px 10px;
      border-radius: 999px;
      background: rgba(0, 0, 0, .35);
      border: 1px solid rgba(255, 255, 255, .14);
      font-size: 12px;
      font-weight: 800;
      backdrop-filter: blur(8px);
      -webkit-backdrop-filter: blur(8px);
    }

    .body {
      padding: 14px;
    }

    .chips {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 10px 0;
    }

    .chip {
      padding: 7px 9px;
      border-radius: 999px;
      background: rgba(255, 255, 255, .08);
      border: 1px solid rgba(255, 255, 255, .08);
      font-size: 12px;
      color: var(--muted);
    }

    .price {
      color: var(--green);
      font-weight: 900;
      font-size: 1.25rem;
    }

    .check {
      display: grid;
      grid-template-columns: auto 1fr;
      gap: 12px;
      padding: 14px;
      border-radius: 16px;
      background: rgba(255, 255, 255, .05);
      border: 1px solid rgba(255, 255, 255, .08);
      margin-bottom: 12px;
    }

    .check input {
      width: 22px;
      height: 22px;
      margin-top: 2px;
      accent-color: var(--pink);
    }

    .notice {
      padding: 14px;
      border-radius: 16px;
      background: rgba(85, 198, 255, .1);
      border: 1px solid rgba(85, 198, 255, .18);
      line-height: 1.5;
    }

    .error {
      background: rgba(255, 75, 75, .12);
      border-color: rgba(255, 75, 75, .25);
    }

    .success {
      background: rgba(67, 233, 123, .1);
      border-color: rgba(67, 233, 123, .2);
    }

    .qr {
      display: inline-block;
      background: #fff;
      padding: 12px;
      border-radius: 24px;
      margin: 18px 0;
      box-shadow: 0 18px 45px rgba(0, 0, 0, .28);
    }

    .qr img {
      display: block;
      width: min(260px, 70vw);
      height: auto;
      border-radius: 12px;
    }

    .table-wrap {
      overflow: auto;
      border-radius: 16px;
      border: 1px solid rgba(255, 255, 255, .08);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 650px;
    }

    th,
    td {
      padding: 12px 10px;
      border-bottom: 1px solid rgba(255, 255, 255, .08);
      text-align: left;
      font-size: .95rem;
    }

    th {
      color: var(--muted);
      font-size: .82rem;
      text-transform: uppercase;
      letter-spacing: .08em;
    }

    .nav {
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      display: grid;
      grid-template-columns: 1fr 1.2fr 1fr;
      gap: 10px;
      padding:
        12px
        calc(16px + env(safe-area-inset-right))
        calc(12px + env(safe-area-inset-bottom))
        calc(16px + env(safe-area-inset-left));
      background: rgba(7, 7, 15, .8);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border-top: 1px solid var(--line);
      z-index: 50;
    }

    .nav .btn {
      min-height: 48px;
      border-radius: 14px;
    }

    .empty {
      padding: 24px;
      text-align: center;
      color: var(--muted);
    }

    @media (max-width: 640px) {
      .row {
        grid-template-columns: 1fr;
      }

      .grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="app">
    <div class="shell">

      <!-- HOME -->
      <section id="screen-home" class="screen active">
        <div class="hero">
          <div class="muted">🎬 BollyFusion Academy</div>
          <h1>Cinematic dance, <span class="gradient">built for every stage</span></h1>
          <p class="muted">
            Register, choose a program, accept waivers, and receive a QR studio pass.
            Optimized for iPhone, Android, and desktop.
          </p>

          <div class="row">
            <button class="btn primary" onclick="go('register')">Register &amp; Enroll</button>
            <button class="btn secondary" onclick="goPrograms()">Browse Programs</button>
          </div>

          <div class="row">
            <button class="btn secondary" onclick="go('admin-login')">Admin Portal</button>
            <button class="btn secondary" onclick="go('home')">Home</button>
          </div>
        </div>

        <div class="panel">
          <h2>State-of-the-art enrollment</h2>
          <p class="muted">
            Mobile-first design, safe-area support for iPhone, large tap targets, digital waivers,
            QR student passes, and admin roster export.
          </p>
        </div>
      </section>

      <!-- REGISTER -->
      <section id="screen-register" class="screen">
        <div class="panel">
          <h2>Student Registration</h2>
          <p class="muted">Enter your details to browse available programs.</p>

          <label for="reg-name">Full Name</label>
          <input id="reg-name" class="input" type="text" autocomplete="name" placeholder="Jane Doe" oninput="syncRegistration()" />

          <label for="reg-email">Email</label>
          <input id="reg-email" class="input" type="email" inputmode="email" autocomplete="email" placeholder="jane@example.com" oninput="syncRegistration()" />

          <div class="row">
            <button class="btn secondary" onclick="go('home')">Back</button>
            <button id="register-next" class="btn primary" onclick="go('classes')" disabled>Continue</button>
          </div>
        </div>
      </section>

      <!-- CLASSES -->
      <section id="screen-classes" class="screen">
        <div class="panel">
          <h2>Choose a Program</h2>
          <p class="muted">Tap a program card to continue to secure checkout.</p>

          <input id="program-search" class="input" type="search" placeholder="Search programs..." oninput="renderPrograms()" />

          <div id="program-count" class="muted" style="margin-top:10px;"></div>
          <div id="program-grid" class="grid"></div>
          <div id="programs-empty" class="empty" style="display:none;">No programs match your search.</div>
        </div>
      </section>

      <!-- CHECKOUT -->
      <section id="screen-checkout" class="screen">
        <div class="panel">
          <h2>Secure Checkout</h2>
          <div id="checkout-summary" class="notice"></div>

          <div style="height:16px;"></div>

          <h3>Legal Agreements</h3>
          <p class="muted">Please review and accept all terms below to proceed with payment.</p>

          <label class="check">
            <input id="waiver1" type="checkbox" onchange="updatePayState()" />
            <span>
              <strong>Physical Activity &amp; Liability Waiver</strong>
              <div class="muted">
                I acknowledge that dance involves physical exertion and risk of injury. I assume all risks
                and release BollyFusion Academy, its instructors, and affiliates from liability.
              </div>
            </span>
          </label>

          <label class="check">
            <input id="waiver2" type="checkbox" onchange="updatePayState()" />
            <span>
              <strong>Media &amp; Photography Release</strong>
              <div class="muted">
                I grant BollyFusion Academy permission to use photographs and video recordings of me
                for promotional, educational, and studio-related purposes.
              </div>
            </span>
          </label>

          <label class="check">
            <input id="waiver3" type="checkbox" onchange="updatePayState()" />
            <span>
              <strong>Refund Policy</strong>
              <div class="muted">
                I understand and agree to the studio refund policy. A free refund is available after
                2 weeks of program commencement. No refunds or prorations outside this window.
              </div>
            </span>
          </label>

          <div class="row">
            <button class="btn secondary" onclick="go('classes')">Back</button>
            <button id="pay-btn" class="btn primary" onclick="processPayment()" disabled>Pay Securely</button>
          </div>
        </div>
      </section>

      <!-- SUCCESS -->
      <section id="screen-success" class="screen">
        <div class="panel" style="text-align:center;">
          <div class="notice success">Payment successful. Welcome to BollyFusion Academy.</div>

          <h2 id="success-name" style="margin-top:18px;"></h2>
          <div id="success-class" class="muted"></div>

          <div class="qr">
            <img id="success-qr" src="" alt="Student QR Code" />
          </div>

          <p class="muted">Save this QR code for front-desk check-in.</p>

          <div class="row">
            <button class="btn secondary" onclick="goPrograms()">Browse More</button>
            <button class="btn primary" onclick="finish()">Done</button>
          </div>
        </div>
      </section>

      <!-- ADMIN LOGIN -->
      <section id="screen-admin-login" class="screen">
        <div class="panel">
          <h2>🔒 Admin Login</h2>
          <p class="muted">Use the hardcoded portal credentials.</p>

          <label for="admin-user">Username</label>
          <input id="admin-user" class="input" type="text" autocomplete="username" placeholder="admin" />

          <label for="admin-pass">Password</label>
          <input id="admin-pass" class="input" type="password" autocomplete="current-password" placeholder="admin123" />

          <div id="admin-error" class="notice error" style="display:none; margin-top:12px;">
            Invalid credentials. Please use admin / admin123.
          </div>

          <div class="row">
            <button class="btn secondary" onclick="go('home')">Cancel</button>
            <button class="btn primary" onclick="adminLogin()">Login Securely</button>
          </div>
        </div>
      </section>

      <!-- ADMIN DASHBOARD -->
      <section id="screen-admin-dashboard" class="screen">
        <div class="panel">
          <h2>📊 Admin Portal</h2>
          <div id="admin-count" class="notice success"></div>

          <div class="table-wrap" style="margin-top:14px;">
            <table>
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Program #</th>
                  <th>Class</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody id="admin-tbody"></tbody>
            </table>
          </div>

          <div class="row">
            <button class="btn secondary" onclick="exportCsv()">Export CSV</button>
            <button class="btn secondary" onclick="clearRegistrations()">Clear Data</button>
          </div>

          <div class="row">
            <button class="btn primary" onclick="go('home')">Logout</button>
            <button class="btn secondary" onclick="renderAdmin()">Refresh</button>
          </div>
        </div>
      </section>

    </div>
  </div>

  <nav class="nav">
    <button class="btn secondary" onclick="go('home')">Home</button>
    <button class="btn primary" onclick="goPrograms()">Programs</button>
    <button class="btn secondary" onclick="go('admin-login')">Admin</button>
  </nav>

  <script>
    const PROGRAMS = [
  {
    "id": "1",
    "name": "Bolly Cardio 1",
    "hours": 0.5,
    "weeks": 20,
    "fee": 250.0,
    "poster": "https://images.unsplash.com/photo-1548690312-e3b507d8c110?auto=format&fit=crop&w=800&q=80",
    "desc": "High-energy entry-level fitness infused with cinematic Bollywood flair.",
    "song_count": "4-5 songs"
  },
  {
    "id": "2",
    "name": "Bolly Cardio II",
    "hours": 1.0,
    "weeks": 20,
    "fee": 500.0,
    "poster": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
    "desc": "Level up your stamina with complex beats and faster choreography.",
    "song_count": "4-5 songs"
  },
  {
    "id": "3",
    "name": "Couples to Event",
    "hours": 1.0,
    "weeks": 10,
    "fee": 1500.0,
    "poster": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80",
    "desc": "Perfect for weddings! Master partner choreography with elegance and grace.",
    "song_count": "2-3 songs"
  },
  {
    "id": "4",
    "name": "Group to Events",
    "hours": 1.0,
    "weeks": 10,
    "fee": 1000.0,
    "poster": "https://images.unsplash.com/photo-1532766324881-8b211bb1f2fc?auto=format&fit=crop&w=800&q=80",
    "desc": "Coordinate stunning group routines for your next big celebration.",
    "song_count": "2-3 songs"
  }
];
    const STORAGE_KEY = "bollyfusion_registrations_v1";

    const state = {
      user: {
        name: "",
        email: ""
      },
      selected: null,
      registrations: []
    };

    try {
      state.registrations = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    } catch (e) {
      state.registrations = [];
    }

    function go(name) {
      document.querySelectorAll(".screen").forEach(function(screen) {
        screen.classList.remove("active");
      });

      const el = document.getElementById("screen-" + name);
      if (el) {
        el.classList.add("active");
        window.scrollTo({ top: 0, behavior: "smooth" });
      }

      if (name === "classes") {
        renderPrograms();
      }

      if (name === "checkout") {
        updateCheckout();
      }

      if (name === "admin-dashboard") {
        renderAdmin();
      }
    }

    function goPrograms() {
      if (state.user.name.trim().length > 1 && state.user.email.trim().includes("@") && state.user.email.trim().includes(".")) {
        renderPrograms();
        go("classes");
      } else {
        go("register");
      }
    }

    function escapeHtml(value) {
      return String(value ?? "").replace(/[&<>"']/g, function(c) {
        return {
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;"
        }[c];
      });
    }

    function money(n) {
      return new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD"
      }).format(n || 0);
    }

    function syncRegistration() {
      state.user.name = document.getElementById("reg-name").value;
      state.user.email = document.getElementById("reg-email").value;

      const ok =
        state.user.name.trim().length > 1 &&
        state.user.email.trim().includes("@") &&
        state.user.email.trim().includes(".");

      document.getElementById("register-next").disabled = !ok;
    }

    function renderPrograms() {
      const grid = document.getElementById("program-grid");
      const empty = document.getElementById("programs-empty");
      const count = document.getElementById("program-count");
      const q = String(document.getElementById("program-search").value || "").toLowerCase();

      const items = PROGRAMS.filter(function(p) {
        return (
          !q ||
          String(p.name).toLowerCase().includes(q) ||
          String(p.desc).toLowerCase().includes(q)
        );
      });

      count.textContent = items.length + " program" + (items.length === 1 ? "" : "s") + " available";

      if (!items.length) {
        grid.innerHTML = "";
        empty.style.display = "block";
        return;
      }

      empty.style.display = "none";
      grid.innerHTML = items.map(cardHtml).join("");
    }

    function cardHtml(p) {
      const name = escapeHtml(p.name);
      const desc = escapeHtml(p.desc);
      const poster = escapeHtml(p.poster);
      const hours = escapeHtml(p.hours);
      const weeks = escapeHtml(p.weeks);
      const songs = escapeHtml(p.song_count);

      return `
        <article class="card">
          <div class="media">
            <span class="badge">${weeks} Weeks</span>
            <img
              src="${poster}"
              alt="${name} poster"
              loading="lazy"
              onerror="imageFallback(this)"
            />
          </div>

          <div class="body">
            <h3>${name}</h3>

            <div class="chips">
              <span class="chip">💃 ${hours} hrs/wk</span>
              <span class="chip">🗓 ${weeks} weeks</span>
              <span class="chip">🎵 ${songs}</span>
            </div>

            <p class="muted">${desc}</p>

            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
              <div class="price">${money(p.fee)}</div>
              <div class="muted">per program</div>
            </div>

            <button class="btn primary" style="margin-top:12px;" onclick="selectProgram('${escapeHtml(p.id)}')">
              Tap to Select
            </button>
          </div>
        </article>
      `;
    }

    function imageFallback(img) {
      img.onerror = null;
      img.style.display = "none";
    }

    function selectProgram(id) {
      state.selected = PROGRAMS.find(function(p) {
        return String(p.id) === String(id);
      }) || null;

      if (!state.selected) return;

      updateCheckout();
      go("checkout");
    }

    function updateCheckout() {
      const box = document.getElementById("checkout-summary");

      if (!state.selected) {
        box.textContent = "No program selected.";
        return;
      }

      box.innerHTML =
        "<strong>" + escapeHtml(state.selected.name) + "</strong><br>" +
        "Student: " + escapeHtml(state.user.name) + "<br>" +
        "Amount due: " + money(state.selected.fee);

      updatePayState();
    }

    function updatePayState() {
      const accepted = ["waiver1", "waiver2", "waiver3"].every(function(id) {
        return document.getElementById(id).checked;
      });

      document.getElementById("pay-btn").disabled = !accepted || !state.selected;
    }

    function processPayment() {
      if (!state.selected) return;

      const record = {
        name: state.user.name.trim(),
        email: state.user.email.trim(),
        program_id: state.selected.id,
        program: state.selected.name,
        status: "Paid",
        date: new Date().toISOString()
      };

      state.registrations.push(record);
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state.registrations));

      renderSuccess();
      go("success");
    }

    function renderSuccess() {
      if (!state.selected) return;

      document.getElementById("success-name").textContent = state.user.name.trim();
      document.getElementById("success-class").textContent = state.selected.name;

      const qrData = encodeURIComponent(
        "Student:" + state.user.name.trim() + "|Class:" + state.selected.name
      );

      document.getElementById("success-qr").src =
        "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=" + qrData;
    }

    function finish() {
      state.selected = null;

      ["waiver1", "waiver2", "waiver3"].forEach(function(id) {
        document.getElementById(id).checked = false;
      });

      go("home");
    }

    function adminLogin() {
      const user = document.getElementById("admin-user").value.trim();
      const pass = document.getElementById("admin-pass").value;
      const err = document.getElementById("admin-error");

      if (user === "admin" && pass === "admin123") {
        err.style.display = "none";
        document.getElementById("admin-pass").value = "";
        renderAdmin();
        go("admin-dashboard");
      } else {
        err.style.display = "block";
      }
    }

    function renderAdmin() {
      const tbody = document.getElementById("admin-tbody");
      const count = document.getElementById("admin-count");

      count.textContent =
        state.registrations.length +
        " registration" +
        (state.registrations.length === 1 ? "" : "s") +
        " stored";

      if (!state.registrations.length) {
        tbody.innerHTML = `
          <tr>
            <td colspan="6">No students have registered yet on this device/browser.</td>
          </tr>
        `;
        return;
      }

      tbody.innerHTML = state.registrations.map(function(r) {
        const when = r.date ? new Date(r.date).toLocaleString() : "";

        return `
          <tr>
            <td>${escapeHtml(r.name)}</td>
            <td>${escapeHtml(r.email)}</td>
            <td>${escapeHtml(r.program_id)}</td>
            <td>${escapeHtml(r.program)}</td>
            <td>${escapeHtml(r.status)}</td>
            <td>${escapeHtml(when)}</td>
          </tr>
        `;
      }).join("");
    }

    function exportCsv() {
      if (!state.registrations.length) {
        alert("No registrations to export.");
        return;
      }

      const rows = [["Name", "Email", "Program #", "Class", "Status", "Date"]];

      state.registrations.forEach(function(r) {
        rows.push([
          r.name,
          r.email,
          r.program_id,
          r.program,
          r.status,
          r.date
        ]);
      });

      const csv = rows
        .map(function(row) {
          return row
            .map(function(field) {
              return '"' + String(field ?? "").replace(/"/g, '""') + '"';
            })
            .join(",");
        })
        .join("\n");

      const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "bollyfusion-registrations.csv";
      a.click();
      URL.revokeObjectURL(url);
    }

    function clearRegistrations() {
      if (confirm("Clear all registrations stored in this browser?")) {
        state.registrations = [];
        localStorage.removeItem(STORAGE_KEY);
        renderAdmin();
      }
    }

    document.addEventListener("DOMContentLoaded", function() {
      renderPrograms();
      syncRegistration();
      updatePayState();
    });
  </script>
</body>
</html>
