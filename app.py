import streamlit as st
import urllib.parse
import pandas as pd
import re
import os
import stat
import datetime
import secrets
import hashlib
import html
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import filelock

st.set_page_config(
    page_title="BollyFusion Academy",
    layout="centered",
    initial_sidebar_state="collapsed"
)

AVAILABLE_PROGRAMS = [
  {
    "id": "1",
    "name": "Bolly Cardio 1",
    "hours": 0.5,
    "weeks": 20,
    "fee": 250.0,
    "stripe_link": "https://buy.stripe.com/6oU00jgpm9IUfJLezI9R603",
    "poster": "https://github.com/codesofnature/Bollywood-Dance/blob/main/1.jpg?raw=true",
    "desc": "High-energy entry-level fitness infused with cinematic Bollywood flair.",
    "song_count": "4-5 songs",
    "start_dates": [
      "Sept 1 2026",
      "Oct 1 2026"
    ]
  },
  {
    "id": "2",
    "name": "Bolly Cardio II",
    "hours": 1.0,
    "weeks": 20,
    "fee": 500.0,
    "stripe_link": "https://buy.stripe.com/00waEX3CA8EQapr1MW9R604",
    "poster": "https://github.com/codesofnature/Bollywood-Dance/blob/main/2.jpg?raw=true",
    "desc": "Level up your stamina with complex beats and faster choreography.",
    "song_count": "4-5 songs",
    "start_dates": [
      "Sept 1 2026",
      "Oct 1 2026"
    ]
  },
  {
    "id": "3",
    "name": "Couples to Event",
    "hours": 1.0,
    "weeks": 10,
    "fee": 1500.0,
    "stripe_link": "https://buy.stripe.com/3cIbJ15KI08keFH9fo9R605",
    "poster": "https://github.com/codesofnature/Bollywood-Dance/blob/main/3.jpg?raw=true",
    "desc": "Perfect for events/weddings/performances! Master partner choreography with elegance and grace.",
    "song_count": "2-3 songs",
    "start_dates": [
      "Sept 15 2026",
      "Nov 1 2026"
    ]
  },
  {
    "id": "4",
    "name": "Group to Events",
    "hours": 1.0,
    "weeks": 10,
    "fee": 1000.0,
    "stripe_link": "https://buy.stripe.com/14A14n7SQ6wI8hj3V49R606",
    "poster": "https://github.com/codesofnature/Bollywood-Dance/blob/main/4.jpg?raw=true",
    "desc": "Coordinate stunning group routines for your next big celebration or event.",
    "song_count": "2-3 songs",
    "start_dates": [
      "Sept 15 2026",
      "Nov 1 2026"
    ]
  },
  {
    "id": "5",
    "name": "Bolly Kids 7-17",
    "hours": 1.0,
    "weeks": 12,
    "fee": 500.0,
    "stripe_link": "https://buy.stripe.com/aFa14n6OM4oA1SVfDM9R607",
    "poster": "https://github.com/codesofnature/Bollywood-Dance/blob/main/5.jpg?raw=true",
    "desc": "High energy dance for the youngster techniques for aspiring competitive performers.",
    "song_count": "2-3 songs",
    "start_dates": [
      "Sept 1 2026"
    ]
  }
]
DB_FILE = "bollyfusion_db.csv"
REQUIRED_COLUMNS = ["Timestamp", "Name", "Email", "Program Number", "Class", "Start Date", "Status", "PasswordSalt", "PasswordHash", "Fee"]

# --- Security Helpers ---
PBKDF2_ITERATIONS = 200_000

def _secure_chmod(path):
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        pass

def generate_secure_password(length=12):
    alphabet = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$%"
    return "".join(secrets.choice(alphabet) for _ in range(length))

def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), PBKDF2_ITERATIONS)
    return salt, digest.hex()

def verify_password(password, salt, expected_hash):
    if not salt or not expected_hash:
        return False
    _, computed = hash_password(password, salt)
    return secrets.compare_digest(computed, expected_hash)

st.markdown('''
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(255, 0, 127, .18), transparent 35%),
        radial-gradient(circle at top right, rgba(255, 170, 0, .15), transparent 30%),
        radial-gradient(circle at bottom, rgba(138, 43, 226, .12), transparent 45%),
        #0a0510;
    color: #fdfbf7;
}

.block-container {
    max-width: 760px;
    padding-top: calc(5rem + env(safe-area-inset-top));
    padding-bottom: calc(2rem + env(safe-area-inset-bottom));
}

input, textarea, select { font-size: 16px !important; }

button { min-height: 50px; border-radius: 16px !important; font-weight: 800 !important; }

.stButton > button, .stLinkButton > a {
    width: 100%; padding: 14px 18px; font-size: 16px; text-align: center;
    border-radius: 16px !important; font-weight: 800 !important;
    height: auto !important; 
}

button[kind="primary"], .stLinkButton > a[data-testid="stLinkButton"] {
    background: linear-gradient(90deg, #ff007f, #ffaa00) !important;
    color: #ffffff !important; border: none !important;
    box-shadow: 0 4px 15px rgba(255, 0, 127, 0.3);
}

button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.05) !important; color: #fdfbf7 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
}

.bf-hero {
    position: relative; border-radius: 28px; padding: 0; overflow: hidden;
    border: 1px solid rgba(255, 255, 255, .12);
    box-shadow: 0 20px 50px rgba(0,0,0,0.45);
    text-align: center; margin-bottom: 18px;
}

.bf-hero-inner {
    position: relative; z-index: 2;
    padding: 40px 20px 24px;
    background: linear-gradient(180deg, rgba(10,5,16,.55) 0%, rgba(10,5,16,.55) 55%, rgba(10,5,16,.95) 100%);
}

.bf-hero h1 {
    margin: 0 0 10px; font-size: clamp(2rem, 6vw, 3.4rem); line-height: 1.05; letter-spacing: -.04em;
    text-shadow: 0 4px 24px rgba(0,0,0,.5);
}

.bf-gradient {
    background: linear-gradient(90deg, #ffaa00, #ff007f, #8a2be2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

.bf-hero p.bf-sub { font-size: 1.02rem; margin: 0 0 4px; }

.media-grid {
    position: relative; 
    height: 300px; 
    width: 100%; 
    overflow: hidden; 
    padding: 0; 
    margin: 0;
}

.media-grid > .bf-hero-media {
    position: absolute; 
    top: 0; 
    left: 0; 
    width: 100%; 
    height: 100%; 
    opacity: 0; 
    animation: bf-fade 15s infinite; 
}

.media-grid > .bf-hero-media:nth-child(1) { animation-delay: 0s; }
.media-grid > .bf-hero-media:nth-child(2) { animation-delay: 2s; }
.media-grid > .bf-hero-media:nth-child(3) { animation-delay: 4s; }
.media-grid > .bf-hero-media:nth-child(4) { animation-delay: 6s; }
.media-grid > .bf-hero-media:nth-child(5) { animation-delay: 8s; }

.media-grid > .bf-hero-media img {
    width: 100%; height: 100%; object-fit: cover; display: block;
    animation: bf-kenburns 14s ease-in-out infinite alternate;
}
.media-grid > .bf-hero-media:nth-child(even) img { 
    animation-direction: alternate-reverse; 
    animation-duration: 18s; 
}

@keyframes bf-fade {
    0%   { opacity: 0; }
    8%   { opacity: 1; }
    20%  { opacity: 1; }
    28%  { opacity: 0; }
    100% { opacity: 0; }
}

@keyframes bf-kenburns {
    0%   { transform: scale(1) translate(0,0); }
    100% { transform: scale(1.18) translate(-2%, -2%); }
}

@media (prefers-reduced-motion: reduce) {
    .media-grid > .bf-hero-media img,
    .media-grid > .bf-hero-media { animation: none; opacity: 1; position: relative; display: none; }
    .media-grid > .bf-hero-media:first-child { display: block; }
}

.bf-muted { color: rgba(253, 251, 247, .7); }

.bf-card {
    border-radius: 24px; overflow: hidden; border: 1px solid rgba(255, 255, 255, .15);
    background: rgba(255, 255, 255, .05); margin-bottom: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.4);
    transition: transform .15s ease, box-shadow .15s ease;
}
.bf-media { position: relative; aspect-ratio: 16 / 10; }
.bf-media img { width: 100%; height: 100%; object-fit: cover; display: block; }
.bf-overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(10, 5, 16, .9), transparent 60%); }
.bf-badge {
    position: absolute; top: 10px; right: 10px; padding: 5px 10px; border-radius: 999px;
    background: rgba(10,5,16,.6); border: 1px solid rgba(255,255,255,.2);
    font-size: 11px; font-weight: 800; backdrop-filter: blur(4px);
}
.bf-body { padding: 16px; }
.bf-body h3 { margin: 0 0 2px; font-size: 1.05rem; }
.bf-price { font-size: 1.25rem; font-weight: 900; color: #00e676; margin-top: 8px; }

/* --- Floating chat launcher + popup panel --- */
div.st-key-bf_fab { position: fixed; right: 20px; bottom: 20px; z-index: 999998; width: 60px; }
div.st-key-bf_fab button {
    width: 60px !important; height: 60px !important; min-height: 60px !important;
    border-radius: 50% !important; font-size: 26px !important; padding: 0 !important;
    background: linear-gradient(135deg, #ff007f, #ffaa00) !important; color: #fff !important;
    border: none !important; box-shadow: 0 8px 24px rgba(255,0,127,.5) !important;
}

div.st-key-bf_chat_panel {
    position: fixed !important; right: 20px !important; bottom: 92px !important; z-index: 999999 !important;
    width: min(360px, calc(100vw - 40px)) !important; max-height: 70vh !important;
    background: #140a20 !important; border: 1px solid rgba(255,255,255,.25) !important; border-radius: 20px !important;
    box-shadow: 0 20px 60px rgba(0,0,0,.8) !important; padding: 16px !important;
    overflow-y: auto !important;
}

.bf-chat-row { display: flex; width: 100%; margin-bottom: 12px; }
.bf-chat-row.user { justify-content: flex-end; }
.bf-chat-row.bot { justify-content: flex-start; }
.bf-chat-bubble { padding: 10px 14px; border-radius: 18px; max-width: 85%; font-size: 15px; line-height: 1.4; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
.bf-chat-row.user .bf-chat-bubble { background-color: #007AFF !important; border-bottom-right-radius: 4px; }
.bf-chat-row.bot .bf-chat-bubble { background-color: #34C759 !important; border-bottom-left-radius: 4px; }
.bf-chat-bubble p, .bf-chat-bubble * { margin: 0 !important; color: #fdfbf7 !important; }
div.st-key-bf_chat_panel div[data-testid="stChatInput"] { background-color: #140a20 !important; }
div.st-key-bf_chat_panel div[data-testid="stChatInput"] textarea { background-color: rgba(255, 255, 255, 0.08) !important; color: #fdfbf7 !important; -webkit-text-fill-color: #fdfbf7 !important; }

</style>
''', unsafe_allow_html=True)

if "app_state" not in st.session_state:
    st.session_state.app_state = "home"
if "current_user" not in st.session_state:
    st.session_state.current_user = {"Name": "", "Email": "", "Program Number": "-", "Class": "-", "Start Date": "-", "Fee": 0.0, "Stripe Link": ""}
if "logged_in_student" not in st.session_state:
    st.session_state.logged_in_student = None

if "student_db" not in st.session_state:
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_csv(DB_FILE)
            # Ensure new columns exist for legacy databases
            for col in REQUIRED_COLUMNS:
                if col not in df.columns:
                    df[col] = "-" if col != "Fee" else 0.0
            st.session_state.student_db = df.to_dict('records')
        except Exception:
            st.session_state.student_db = []
    else:
        st.session_state.student_db = []

def update_db(name, email, prog_num, class_name, start_date, status, password="", fee=0.0):
    lock = filelock.FileLock(f"{DB_FILE}.lock")
    with lock:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        
        if os.path.exists(DB_FILE):
            df = pd.read_csv(DB_FILE)
            for col in REQUIRED_COLUMNS:
                if col not in df.columns:
                    df[col] = "-" if col != "Fee" else 0.0
        else:
            df = pd.DataFrame(columns=REQUIRED_COLUMNS)

        pw_salt, pw_hash = (None, None)
        if password:
            pw_salt, pw_hash = hash_password(password)

        if not df.empty and email and email != "No Details Provided":
            if email in df['Email'].values:
                idx = df.index[df['Email'] == email].tolist()[0]
                df.at[idx, 'Timestamp'] = timestamp
                df.at[idx, 'Name'] = name
                df.at[idx, 'Program Number'] = prog_num
                df.at[idx, 'Class'] = class_name
                df.at[idx, 'Start Date'] = start_date
                df.at[idx, 'Status'] = status
                if pw_hash:
                    df.at[idx, 'PasswordSalt'] = pw_salt
                    df.at[idx, 'PasswordHash'] = pw_hash
                if fee:
                    df.at[idx, 'Fee'] = fee
                
                st.session_state.student_db = df.to_dict('records')
                df.to_csv(DB_FILE, index=False)
                _secure_chmod(DB_FILE)
                return

        record = {
            "Timestamp": timestamp, "Name": name, "Email": email, "Program Number": prog_num,
            "Class": class_name, "Start Date": start_date, "Status": status, "PasswordSalt": pw_salt, "PasswordHash": pw_hash, "Fee": fee
        }
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        st.session_state.student_db = df.to_dict('records')
        df.to_csv(DB_FILE, index=False)
        _secure_chmod(DB_FILE)

def _seed_demo_students():
    if os.path.exists(DB_FILE) or not AVAILABLE_PROGRAMS:
        return
    demo_students = [
        {"name": "Priya Sharma",  "email": "priya.sharma@example.com"},
        {"name": "Arjun Mehta",   "email": "arjun.mehta@example.com"},
        {"name": "Simone Clarke", "email": "simone.clarke@example.com"},
    ]
    for i, s in enumerate(demo_students):
        prog = AVAILABLE_PROGRAMS[i % len(AVAILABLE_PROGRAMS)]
        demo_password = generate_secure_password(12)
        demo_date = prog.get("start_dates", ["Anytime"])[0]
        update_db(
            s["name"], s["email"], prog["id"], prog["name"], demo_date,
            "Paid ✅", password=demo_password, fee=prog["fee"]
        )

_seed_demo_students()

def send_email_invoice(to_email, name, class_name, fee, password):
    sender_email = st.secrets.get("smtp_email", "")
    sender_password = st.secrets.get("smtp_app_password", "")
    admin_email = st.secrets.get("admin_notify_email", "")

    if not sender_email or not sender_password: return
    subject = "BollyFusion Academy - Payment Invoice & Portal Login"
    body = (f"Hi {name},\n\nThank you for your payment of ${fee:.2f} for {class_name}.\n\n"
            f"Your Registered Student Portal login details are:\nEmail: {to_email}\nPassword: {password}\n\n"
            f"Please log in via the website to access your unique QR code for class entry and view this invoice.\n\nBest,\nBollyFusion Academy\nBilling Provider: Phase Change, Inc")
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        if admin_email: msg['Bcc'] = admin_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        st.success("Invoice and portal password emailed successfully.")
    except Exception:
        st.warning("Payment was recorded, but the confirmation email could not be sent. Please contact the studio.")

def navigate(to_state): st.session_state.app_state = to_state
def reset_user():
    st.session_state.current_user = {"Name": "", "Email": "", "Program Number": "-", "Class": "-", "Start Date": "-", "Fee": 0.0, "Stripe Link": ""}
    st.query_params.clear()
    st.session_state.app_state = "home"

def get_client_ip():
    try:
        if hasattr(st, 'context') and hasattr(st.context, 'headers'):
            return st.context.headers.get("X-Forwarded-For", "Unknown IP").split(',')[0]
    except Exception: pass
    return "IP Unavailable"

def process_registration(is_valid):
    if not is_valid:
        ip_addr = get_client_ip()
        update_db(f"Guest ({ip_addr})", "No Details Provided", "-", "Browsing Programs...", "-", "Just Browsing")
    else:
        update_db(st.session_state.current_user["Name"], st.session_state.current_user["Email"], "-", "Browsing Programs...", "-", "Entered Details")
    navigate("classes")

if "status" in st.query_params and st.query_params["status"] == "success":
    if st.session_state.app_state != "success":
        st.session_state.app_state = "success"
        if st.session_state.current_user.get("Email"):
            gen_pw = generate_secure_password(12)
            update_db(st.session_state.current_user["Name"], st.session_state.current_user["Email"], st.session_state.current_user["Program Number"], st.session_state.current_user["Class"], st.session_state.current_user.get("Start Date", "-"), "Paid ✅", password=gen_pw, fee=st.session_state.current_user.get("Fee", 0.0))
            send_email_invoice(st.session_state.current_user["Email"], st.session_state.current_user["Name"], st.session_state.current_user["Class"], st.session_state.current_user.get("Fee", 0.0), gen_pw)

if st.session_state.app_state == "home":
    st.markdown('''
    <div class="bf-hero">
        <div class="media-grid">
            <div class="bf-hero-media"><img src="https://github.com/codesofnature/Bollywood-Dance/blob/4dcb2186d5a9907998e63d390443477be4ce7bae/s1.jpg?raw=true" alt="Dancers performing a traditional Bollywood routine"/></div>
            <div class="bf-hero-media"><img src="https://github.com/codesofnature/Bollywood-Dance/blob/4dcb2186d5a9907998e63d390443477be4ce7bae/s2.jpg?raw=true" alt="Group dancing on stage in colorful costume"/></div>
            <div class="bf-hero-media"><img src="https://github.com/codesofnature/Bollywood-Dance/blob/4dcb2186d5a9907998e63d390443477be4ce7bae/s3.jpg?raw=true" alt="High-energy Bollywood performance"/></div>
            <div class="bf-hero-media"><img src="https://github.com/codesofnature/Bollywood-Dance/blob/4dcb2186d5a9907998e63d390443477be4ce7bae/s4.jpg?raw=true alt="Dancers in traditional festive dress"/></div>
            <div class="bf-hero-media"><img src="https://github.com/codesofnature/Bollywood-Dance/blob/4dcb2186d5a9907998e63d390443477be4ce7bae/s5.jpg?raw=true" alt="Dancer in traditional Indian attire mid-performance"/></div>
        </div>
        <div class="bf-hero-inner">
            <h1>Master Cinematic Dance on Any Stage, <span class="bf-gradient">built for every stage</span></h1>
            <p class="bf-sub bf-muted">Choose a program, register, and pay securely — all in a couple of minutes.</p>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1: st.button("Browse Program Options", use_container_width=True, type="primary", on_click=navigate, args=("register",))
    with col2: st.button("Registered Student Portal", use_container_width=True, on_click=navigate, args=("student_login",))
    with col3: st.button("Teacher Portal", use_container_width=True, on_click=navigate, args=("admin_login",))

    st.write("")

    FAQS = [
        {"q": "What programs / levels do you offer?", "kw": ["program", "level", "class", "offer", "options", "types"], "a": "We offer a variety of cinematic dance programs for all levels. Tap 'Browse Program Options' to see full details."},
    ]

    def _match_faq(user_text):
        text = user_text.lower()
        best, best_score = None, 0
        for item in FAQS:
            score = sum(1 for kw in item["kw"] if kw in text)
            if score > best_score:
                best, best_score = item, score
        return best if best_score > 0 else None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Hi! 👋 Ask me about our programs, pricing, schedules, attire, or anything else about the studio."}]
    if "chat_failed_attempts" not in st.session_state:
        st.session_state.chat_failed_attempts = 0
    if "chat_open" not in st.session_state:
        st.session_state.chat_open = False

    def _toggle_chat():
        st.session_state.chat_open = not st.session_state.chat_open

    with st.container(key="bf_fab"):
        st.button("💬" if not st.session_state.chat_open else "✖️", key="bf_fab_btn", on_click=_toggle_chat)

    if st.session_state.chat_open:
        with st.container(key="bf_chat_panel"):
            st.markdown("**💬 Chat with BollyFusion**")
            for msg in st.session_state.chat_history:
                align_class = "user" if msg["role"] == "user" else "bot"
                st.markdown(f'''
                    <div class="bf-chat-row {align_class}">
                        <div class="bf-chat-bubble">{msg["content"]}</div>
                    </div>
                ''', unsafe_allow_html=True)

            prompt = st.chat_input("Ask about programs, pricing, schedule...")
            if prompt:
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                match = _match_faq(prompt)
                if match:
                    answer = match["a"]
                    st.session_state.chat_failed_attempts = 0
                else:
                    st.session_state.chat_failed_attempts += 1
                    if st.session_state.chat_failed_attempts >= 3:
                        answer = "I'm sorry, I couldn't find a good answer to your recent questions. **Please call our support at 2341239239** for immediate assistance."
                    else:
                        answer = "I'm not quite sure about that. Try asking about programs, pricing, age groups, attire, schedule, or events!"
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.rerun()

elif st.session_state.app_state == "register":
    st.markdown('<div class="bf-section-title"><h2>BROWSE PROGRAM OPTIONS AND PRICES</h2><p class="bf-muted">Enter your details, or simply browse.</p></div>', unsafe_allow_html=True)
    st.session_state.current_user["Name"] = st.text_input("Full Name", value=st.session_state.current_user.get("Name", ""), placeholder="What do we call you?")
    st.session_state.current_user["Email"] = st.text_input("Email", value=st.session_state.current_user.get("Email", ""), placeholder=".com .edu email ID")
    st.write("")
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    is_valid_email = bool(re.match(email_pattern, st.session_state.current_user["Email"]))
    valid = (st.session_state.current_user["Name"].strip() != "" and is_valid_email)

    col1, col2 = st.columns(2)
    with col1: st.button("Back", use_container_width=True, on_click=navigate, args=("home",))
    with col2:
        btn_label = "Continue" if valid else "I'll just browse"
        st.button(btn_label, use_container_width=True, type="primary", on_click=process_registration, args=(valid,))

elif st.session_state.app_state == "classes":
    st.markdown('<div class="bf-section-title"><h2>Choose a Program</h2><p class="bf-muted">Tap a program to continue to secure checkout.</p></div>', unsafe_allow_html=True)
    if not AVAILABLE_PROGRAMS:
        st.info("No programs are currently available.")
    else:
        cols = st.columns(2)
        for idx, prog in enumerate(AVAILABLE_PROGRAMS):
            with cols[idx % 2]:
                st.markdown(f'''
                <div class="bf-card">
                    <div class="bf-media">
                        <img src="{prog['poster']}" alt="{prog['name']}">
                        <div class="bf-overlay"></div>
                        <div class="bf-badge">{prog['weeks']} Weeks</div>
                    </div>
                    <div class="bf-body">
                        <h3>{prog['name']}</h3>
                        <div class="bf-price">${prog['fee']:,.2f}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)
                if st.button(f"Select {prog['name']}", key=f"select_{prog['id']}", use_container_width=True, type="primary"):
                    st.session_state.current_user["Class"] = prog["name"]
                    st.session_state.current_user["Program Number"] = prog["id"]
                    st.session_state.current_user["Fee"] = prog["fee"]
                    st.session_state.current_user["Stripe Link"] = prog["stripe_link"]
                    update_db(st.session_state.current_user.get("Name", "Guest"), st.session_state.current_user.get("Email", "None"), prog["id"], prog["name"], "-", "Pending Payment")
                    navigate("checkout")
    st.write("")
    st.button("Back", use_container_width=True, on_click=navigate, args=("register",))

elif st.session_state.app_state == "checkout":
    selected_class = st.session_state.current_user.get("Class", "")
    selected_fee = st.session_state.current_user.get("Fee", 0)
    checkout_url = f"{st.session_state.current_user.get('Stripe Link', '#')}?prefilled_email={urllib.parse.quote(st.session_state.current_user.get('Email', ''))}"
    
    st.markdown(f"### Checkout: {selected_class}")
    
    # Select Start Date Logic
    active_program = next((p for p in AVAILABLE_PROGRAMS if p['id'] == st.session_state.current_user["Program Number"]), None)
    available_dates = active_program.get("start_dates", ["Anytime"]) if active_program else ["Anytime"]
    chosen_date = st.selectbox("Select Program Start Date", available_dates)
    st.session_state.current_user["Start Date"] = chosen_date
    
    st.markdown(f"### Amount Due: **${selected_fee:,.2f}**")
    
    legal_disclaimer = '''BINDING AGREEMENT, WAIVER AND RELEASE OF LIABILITY, ASSUMPTION OF RISK, AND INDEMNITY AGREEMENT.

By completing this transaction and participating in any programs, events, or classes, you (the "Participant") agree to all terms and conditions set forth herein. 

1. BILLING ENTITY: The Participant understands and agrees that all financial transactions, billing, invoicing, and payment processing are managed exclusively by Phase Change, Inc. Any references to payment, refunds, or financial liability shall be directed to and governed by Phase Change, Inc.

2. ASSUMPTION OF RISK: The Participant acknowledges that dance and fitness programs involve physical exertion and movement, which carry inherent risks of injury, illness, or property damage. The Participant voluntarily assumes all risks associated with participation.

3. WAIVER AND RELEASE: In consideration for being permitted to participate, the Participant hereby releases, waives, discharges, and covenants not to sue the studio, its owners, instructors, affiliates, or Phase Change, Inc. from any and all liability, claims, demands, or causes of action arising out of or related to any loss, damage, or injury.

4. MEDICAL CLEARANCE: The Participant certifies that they are physically fit and have no medical conditions that would prevent their full participation. The Participant agrees to bear all costs for any medical care required as a result of participation.

5. MEDIA RELEASE: The Participant grants full permission to the studio and Phase Change, Inc. to use any photographs, motion pictures, recordings, or any other record of the programs for any legitimate purpose, including commercial advertising, without further compensation.

6. REFUND POLICY: All sales are final. Phase Change, Inc. reserves the right to refuse refunds, exchanges, or transfers once a transaction is processed.

THIS DOCUMENT IS A LEGALLY BINDING CONTRACT. BY CHECKING THE BOX BELOW, YOU AFFIRM THAT YOU HAVE READ, UNDERSTOOD, AND AGREED TO ALL TERMS STATED ABOVE IN FULL.
'''
    st.text_area("Legal Terms & Conditions", value=legal_disclaimer, height=250, disabled=True)
    cb_legal = st.checkbox("I have read, understood, and accept the Binding Agreement and Waiver of Liability, acknowledging Phase Change, Inc as the sole billing entity.")

    st.write("")
    col1, col2 = st.columns(2)
    with col1: st.button("Back", use_container_width=True, on_click=navigate, args=("classes",))
    with col2:
        if cb_legal: st.link_button(f"💳 Pay via Stripe", url=checkout_url, use_container_width=True, type="primary")
        else: st.button(f"💳 Pay via Stripe", use_container_width=True, type="primary", disabled=True)

elif st.session_state.app_state == "success":
    st.markdown("### Payment Successful!")
    st.button("Done (Back to Home)", use_container_width=True, type="primary", on_click=reset_user)

elif st.session_state.app_state == "student_login":
    s_email = st.text_input("Registered Email")
    s_pass = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    with col1: st.button("Cancel", use_container_width=True, on_click=navigate, args=("home",))
    with col2:
        if st.button("Login", use_container_width=True, type="primary"):
            df = pd.DataFrame(st.session_state.student_db)
            if not df.empty and s_email in df['Email'].values:
                user_row = df[df['Email'] == s_email].iloc[0]
                if verify_password(s_pass, user_row.get('PasswordSalt', ''), user_row.get('PasswordHash', '')):
                    st.session_state.logged_in_student = user_row.to_dict()
                    navigate("student_dashboard")
                    st.rerun()
                else: st.error("Invalid credentials.")
            else: st.error("Invalid credentials.")

elif st.session_state.app_state == "student_dashboard":
    st.write("Welcome to your dashboard!")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in_student = None
        navigate("home")

elif st.session_state.app_state == "admin_login":
    a_user = st.text_input("Username")
    a_pass = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    with col1: st.button("Cancel", use_container_width=True, on_click=navigate, args=("home",))
    with col2:
        if st.button("Login", use_container_width=True, type="primary"):
            if secrets.compare_digest(a_user, st.secrets.get("admin_username", "")) and secrets.compare_digest(a_pass, st.secrets.get("admin_password", "")):
                navigate("admin_dashboard")
                st.rerun()
            else: st.error("Invalid credentials.")

elif st.session_state.app_state == "admin_dashboard":
    st.markdown('<div class="bf-section-title"><h2>Registered Students</h2><p class="bf-muted">Full profile for every student who has registered or paid.</p></div>', unsafe_allow_html=True)

    if not st.session_state.student_db:
        st.info("No students yet. They'll appear here as soon as someone registers or pays.")
    else:
        df_students = pd.DataFrame(st.session_state.student_db)
        # Ensure all columns exist
        for col in REQUIRED_COLUMNS:
            if col not in df_students.columns:
                df_students[col] = "-"
                
        paid_count = int((df_students.get("Status", pd.Series(dtype=str)) == "Paid ✅").sum())
        m1, m2 = st.columns(2)
        m1.metric("Total Students", len(df_students))
        m2.metric("Paid", paid_count)

        st.write("")
        view_mode = st.radio("View", ["Profile Cards", "Raw Table"], horizontal=True, label_visibility="collapsed")

        if view_mode == "Profile Cards":
            for _, row in df_students.iloc[::-1].iterrows():
                status = row.get("Status", "-")
                fee_val = row.get("Fee", 0)
                try:
                    fee_display = f"${float(fee_val):,.2f}"
                except (TypeError, ValueError):
                    fee_display = "-"
                badge = "✅" if status == "Paid ✅" else "⏳"
                with st.expander(f"{badge} {row.get('Name', 'Unknown')} — {row.get('Class', '-')} ({row.get('Start Date', '-')})"):
                    pc1, pc2 = st.columns(2)
                    with pc1:
                        st.markdown(f"**Name:** {row.get('Name', '-')}")
                        st.markdown(f"**Email:** {row.get('Email', '-')}")
                        st.markdown(f"**Program:** {row.get('Class', '-')} (#{row.get('Program Number', '-')})")
                        st.markdown(f"**Start Date:** {row.get('Start Date', '-')}")
                        st.markdown(f"**Status:** {status}")
                    with pc2:
                        st.markdown(f"**Fee:** {fee_display}")
                        st.markdown(f"**Registered:** {row.get('Timestamp', '-')}")
                        st.markdown(f"**Portal Login Set:** {'Yes' if row.get('PasswordHash') else 'No'}")
                        
                        st.write("") 
                        # Hardened Delete Record Button
                        delete_key = f"del_{row.get('Email', 'unk')}_{row.get('Timestamp', 't')}"
                        if st.button("🗑️ Delete Record", key=delete_key):
                            target_email = row.get("Email")
                            target_time = row.get("Timestamp")
                            if target_email:
                                lock = filelock.FileLock(f"{DB_FILE}.lock")
                                with lock:
                                    if os.path.exists(DB_FILE):
                                        df_current = pd.read_csv(DB_FILE)
                                        # Strict matching to avoid deleting multiple entries if emails duplicate
                                        df_current = df_current[~((df_current['Email'] == target_email) & (df_current['Timestamp'] == target_time))]
                                        df_current.to_csv(DB_FILE, index=False)
                                        _secure_chmod(DB_FILE)
                                        st.session_state.student_db = df_current.to_dict('records')
                                
                                st.success(f"Record for {target_email} deleted.")
                                st.rerun()
        else:
            # Download full current DB as CSV including everything but hashed passwords for security view
            st.dataframe(
                df_students.drop(columns=["PasswordSalt", "PasswordHash"], errors="ignore"),
                use_container_width=True
            )
            
            # Full DB Export
            st.download_button(
                "⬇️ Export Full Students CSV (Backup)",
                data=df_students.to_csv(index=False).encode("utf-8"),
                file_name="bollyfusion_students_export.csv",
                mime="text/csv"
            )

    st.divider()
    
    # Hardened Restore Database Section
    st.markdown('<div class="bf-section-title"><h2>Restore / Upload Database</h2><p class="bf-muted">Upload a previously exported CSV to safely restore student records.</p></div>', unsafe_allow_html=True)
    uploaded_csv = st.file_uploader("Upload bollyfusion_students_export.csv", type=["csv"])
    
    if uploaded_csv is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_csv)
            # Validate essential columns
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in df_uploaded.columns]
            if missing_cols:
                st.error(f"Upload Failed: CSV is missing required columns: {', '.join(missing_cols)}")
            else:
                st.success("CSV format verified. Ready to restore.")
                if st.button("⚠️ Confirm Restore (Overwrites Current Data)", type="primary"):
                    lock = filelock.FileLock(f"{DB_FILE}.lock")
                    with lock:
                        df_uploaded.to_csv(DB_FILE, index=False)
                        _secure_chmod(DB_FILE)
                    
                    st.session_state.student_db = df_uploaded.to_dict('records')
                    st.success("✅ Database restored successfully!")
                    st.rerun()
        except Exception as e:
            st.error(f"Failed to read CSV: {e}")
                
    st.write("")
    if st.button("Logout", use_container_width=True, on_click=navigate, args=("home",)): pass
