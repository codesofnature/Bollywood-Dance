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
    "song_count": "4-5 songs"
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
    "song_count": "4-5 songs"
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
    "song_count": "2-3 songs"
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
    "song_count": "2-3 songs"
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
    "song_count": "2-3 songs"
  }
]
DB_FILE = "bollyfusion_db.csv"

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
    /* Reduced to 15 seconds total */
    animation: bf-fade 15s infinite; 
}

/* Staggered by 3 seconds instead of 5 */
.media-grid > .bf-hero-media:nth-child(1) { animation-delay: 0s; }
.media-grid > .bf-hero-media:nth-child(2) { animation-delay: 2s; }
.media-grid > .bf-hero-media:nth-child(3) { animation-delay: 4s; }
.media-grid > .bf-hero-media:nth-child(4) { animation-delay: 6s; }
.media-grid > .bf-hero-media:nth-child(5) { animation-delay: 8s; }

.media-grid > .bf-hero-media img {
    width: 100%; height: 100%; object-fit: cover; display: block;
    /* Keeps the slow zoom effect you already have */
    animation: bf-kenburns 14s ease-in-out infinite alternate;
}
.media-grid > .bf-hero-media:nth-child(even) img { 
    animation-direction: alternate-reverse; 
    animation-duration: 18s; 
}

/* The math: 5 images = each gets 20% of the timeline to shine */
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

/* Custom Flexbox Chat Bubbles (Left/Right Layout) */
.bf-chat-row {
    display: flex;
    width: 100%;
    margin-bottom: 12px;
}
.bf-chat-row.user {
    justify-content: flex-end; /* Pushes user messages to the right */
}
.bf-chat-row.bot {
    justify-content: flex-start; /* Pushes bot messages to the left */
}
.bf-chat-bubble {
    padding: 10px 14px;
    border-radius: 18px;
    max-width: 85%;
    font-size: 15px;
    line-height: 1.4;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
.bf-chat-row.user .bf-chat-bubble {
    background-color: #007AFF !important; /* Blue user bubble */
    border-bottom-right-radius: 4px;
}
.bf-chat-row.bot .bf-chat-bubble {
    background-color: #34C759 !important; /* Green bot bubble */
    border-bottom-left-radius: 4px;
}
/* Force all text inside the bubbles to be crisp white */
.bf-chat-bubble p, .bf-chat-bubble * {
    margin: 0 !important;
    color: #fdfbf7 !important;
}

/* Fix the white background on the chat input container */
div.st-key-bf_chat_panel div[data-testid="stChatInput"] {
    background-color: #140a20 !important; 
}

/* Fix the actual typing area and send button to match the dark theme */
div.st-key-bf_chat_panel div[data-testid="stChatInput"] textarea {
    background-color: rgba(255, 255, 255, 0.08) !important;
    color: #fdfbf7 !important;
    -webkit-text-fill-color: #fdfbf7 !important; /* Critical for overriding iOS defaults */
}

</style>
''', unsafe_allow_html=True)

if "app_state" not in st.session_state:
    st.session_state.app_state = "home"
if "current_user" not in st.session_state:
    st.session_state.current_user = {"Name": "", "Email": "", "Program Number": "-", "Class": "-", "Fee": 0.0, "Stripe Link": ""}
if "logged_in_student" not in st.session_state:
    st.session_state.logged_in_student = None

if "student_db" not in st.session_state:
    if os.path.exists(DB_FILE):
        st.session_state.student_db = pd.read_csv(DB_FILE).to_dict('records')
        _secure_chmod(DB_FILE)
    else:
        st.session_state.student_db = []

# Using FileLock for thread-safety and to prevent race conditions during DB updates
def update_db(name, email, prog_num, class_name, status, password="", fee=0.0):
    lock = filelock.FileLock(f"{DB_FILE}.lock")
    with lock:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        
        # Fresh read inside lock
        if os.path.exists(DB_FILE):
            df = pd.read_csv(DB_FILE)
        else:
            df = pd.DataFrame(columns=["Timestamp", "Name", "Email", "Program Number", "Class", "Status", "PasswordSalt", "PasswordHash", "Fee"])

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
            "Class": class_name, "Status": status, "PasswordSalt": pw_salt, "PasswordHash": pw_hash, "Fee": fee
        }
        df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)
        st.session_state.student_db = df.to_dict('records')
        df.to_csv(DB_FILE, index=False)
        _secure_chmod(DB_FILE)

# One-time demo seed: gives the teacher 3 already-paid students to look at
# the very first time the app runs. Runs only while DB_FILE doesn't exist yet,
# so it never re-adds students on later reruns/restarts.
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
        update_db(
            s["name"], s["email"], prog["id"], prog["name"],
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
            f"Please log in via the website to access your unique QR code for class entry and view this invoice.\n\nBest,\nBollyFusion Academy")
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
    st.session_state.current_user = {"Name": "", "Email": "", "Program Number": "-", "Class": "-", "Fee": 0.0, "Stripe Link": ""}
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
        update_db(f"Guest ({ip_addr})", "No Details Provided", "-", "Browsing Programs...", "Just Browsing")
    else:
        update_db(st.session_state.current_user["Name"], st.session_state.current_user["Email"], "-", "Browsing Programs...", "Entered Details")
    navigate("classes")

if "status" in st.query_params and st.query_params["status"] == "success":
    if st.session_state.app_state != "success":
        st.session_state.app_state = "success"
        if st.session_state.current_user.get("Email"):
            gen_pw = generate_secure_password(12)
            update_db(st.session_state.current_user["Name"], st.session_state.current_user["Email"], st.session_state.current_user["Program Number"], st.session_state.current_user["Class"], "Paid ✅", password=gen_pw, fee=st.session_state.current_user.get("Fee", 0.0))
            send_email_invoice(st.session_state.current_user["Email"], st.session_state.current_user["Name"], st.session_state.current_user["Class"], st.session_state.current_user.get("Fee", 0.0), gen_pw)


if st.session_state.app_state == "home":
    # Splash UI: curated, real Bollywood-dance photography with a slow Ken Burns
    # drift (no broken/irrelevant placeholder video files).
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

    # --- Studio gallery media links -- kept here as code only (not rendered on
    # the page). Swap these for your own studio photos/clips any time, then
    # wire GALLERY_IMAGES / GALLERY_VIDEOS into a section wherever you'd like
    # them displayed.
    GALLERY_VIDEOS = [
        "https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    ]
    GALLERY_IMAGES = [
        "https://images.unsplash.com/photo-1547106510-6aec13ee41ff?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1563775957285-5860ffa885c0?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1712192682756-ae5b3a8e7508?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1598975762861-28118e88154e?auto=format&fit=crop&w=600&q=80",
        "https://images.unsplash.com/photo-1652111132299-ff1056c87b35?auto=format&fit=crop&w=600&q=80",
    ]

    # --- FAQ knowledge base: fully aware of the studio's actual offered programs ---
    def _fmt_money(v):
        return f"\\${v:,.0f}" if float(v) == int(v) else f"\\${v:,.2f}"

    def _program_names():
        return [p["name"] for p in AVAILABLE_PROGRAMS] if AVAILABLE_PROGRAMS else []

    def _fee_range():
        if not AVAILABLE_PROGRAMS: return "please check Browse Program Options"
        fees = [p["fee"] for p in AVAILABLE_PROGRAMS]
        return f"{_fmt_money(min(fees))} to {_fmt_money(max(fees))}" if min(fees) != max(fees) else _fmt_money(fees[0])

    def _kids_program():
        return next((p for p in AVAILABLE_PROGRAMS if "kid" in p["name"].lower()), None)

    def _event_programs():
        return [p for p in AVAILABLE_PROGRAMS if any(k in p["name"].lower() for k in ["event", "couple"])]

    def _company_program():
        return next((p for p in AVAILABLE_PROGRAMS if any(k in p["name"].lower() for k in ["premier", "company"])), None)

    def _cardio_programs():
        return [p for p in AVAILABLE_PROGRAMS if "cardio" in p["name"].lower()]

    names = _program_names()
    names_str = ", ".join(names) if names else "our current programs (see Browse Program Options)"
    kids_p = _kids_program()
    company_p = _company_program()
    event_ps = _event_programs()
    cardio_ps = _cardio_programs()

    FAQS = [
        {"q": "What programs / levels do you offer?",
         "kw": ["program", "level", "class", "offer", "options", "types"],
         "a": f"We currently offer: **{names_str}**. Each is designed for a different stage — from first-timers to performance-ready dancers. Tap 'Browse Program Options' to see full details."},
        {"q": "How much do classes cost?",
         "kw": ["price", "cost", "fee", "how much", "expensive", "pricing"],
         "a": f"Program fees range from **{_fee_range()}** for the full term, depending on the level and number of weeks. Tap 'Browse Program Options' for exact pricing per class."},
        {"q": "What ages do you teach?",
         "kw": ["age", "kid", "child", "children", "young", "adult", "teen"],
         "a": (f"We welcome adults in most programs, plus a dedicated **{kids_p['name']}** class for younger dancers." if kids_p
               else "Our programs are primarily designed for teens and adults — check Browse Program Options for the age focus of each level.")},
        {"q": "Do I need prior dance experience?",
         "kw": ["experience", "beginner", "never danced", "background", "new to dance", "first time"],
         "a": "Not at all! Our entry-level cardio classes are built for total beginners — no dance background needed. As you progress, later levels add more technical choreography."},
        {"q": "What should I wear to class?",
         "kw": ["wear", "outfit", "clothes", "attire", "shoes", "dress code"],
         "a": "Comfortable, breathable workout clothes and supportive sneakers or dance sneakers work best. Avoid anything restrictive — you'll be moving a lot!"},
        {"q": "How long is each program / how many weeks?",
         "kw": ["weeks", "duration", "long", "term", "how many classes"],
         "a": "Program length varies by level, generally 10-20 weeks per term. Exact duration for each program is shown on the 'Browse Program Options' page."},
        {"q": "Is there a trial or drop-in class?",
         "kw": ["trial", "drop in", "try", "sample", "first class free"],
         "a": "We don't run a separate free trial — registration secures your spot for the full program term. If you're unsure which level fits you, message us here and we'll point you in the right direction."},
        {"q": "How do I sign up / register?",
         "kw": ["sign up", "register", "enroll", "join", "how do i start"],
         "a": "Tap 'Browse Program Options', enter your name and email, choose your program, and complete secure checkout. You'll get portal login details by email right after payment."},
        {"q": "What payment methods do you accept?",
         "kw": ["payment", "pay", "stripe", "credit card", "card", "venmo"],
         "a": "We accept all major credit/debit cards through secure Stripe checkout — no cash or manual payment needed to register."},
        {"q": "What is Bollywood dance / cardio style like?",
         "kw": ["what is bollywood", "style", "what kind of dance", "genre"],
         "a": "Bollywood dance blends high-energy cinematic choreography from Indian films with elements of hip-hop, folk, and classical Indian movement — it's fun, expressive, and a great workout."},
        {"q": "Do you host performances or showcase events?",
         "kw": ["event", "performance", "showcase", "recital", "perform"],
         "a": "Yes! Several programs include live events and showcases through the year — details and any event fees are listed per program on the pricing page."},
        {"q": "What's the difference between Cardio I and Cardio II?",
         "kw": ["cardio 1", "cardio i", "cardio 2", "cardio ii", "difference between", "which cardio"],
         "a": (f"**{cardio_ps[0]['name']}** is the entry-level class focused on fundamentals and fitness. **{cardio_ps[1]['name']}** builds on that with faster combinations and more complex choreography." if len(cardio_ps) >= 2
               else "Our cardio levels progress from fundamentals to faster, more complex choreography as you move up.")},
        {"q": "Do you offer wedding or couples choreography?",
         "kw": ["wedding", "couple", "sangeet", "first dance", "engagement"],
         "a": (f"Yes — our **{event_ps[0]['name']}** program is built exactly for that: personalized partner choreography for weddings, sangeets, and special events." if event_ps
               else "We offer small-group and couples choreography for weddings and events — see Browse Program Options for current availability.")},
        {"q": "Do you offer private lessons or group event choreography?",
         "kw": ["private lesson", "group choreography", "custom routine", "book a routine"],
         "a": (f"Our **{event_ps[-1]['name']}** program covers custom group routines for celebrations and events. For fully private 1-on-1 lessons, message us here and we'll follow up directly." if event_ps
               else "For custom group or private choreography requests, please message us here and our team will follow up directly.")},
        {"q": "Where is the studio located?",
         "kw": ["location", "where", "address", "studio", "directions"],
         "a": "We're at our Main Studio location. Exact address and entry details are sent automatically to registered students after checkout for security."},
        {"q": "What is your cancellation / refund policy?",
         "kw": ["refund", "cancel", "cancellation", "reschedule", "policy"],
         "a": "Program fees cover the full term once classes begin. For cancellations before a term starts, or any special circumstances, please contact the studio directly and we'll help sort it out."},
        {"q": "How many songs will we learn?",
         "kw": ["songs", "how many routines", "choreography count", "music"],
         "a": ("Shorter terms typically cover 2-3 songs, while full 20-week terms cover 4-5 full routines" + (f" — for example, **{AVAILABLE_PROGRAMS[0]['name']}** covers {AVAILABLE_PROGRAMS[0]['song_count']}." if AVAILABLE_PROGRAMS else "."))},
        {"q": "Is Bollywood dance a good workout?",
         "kw": ["workout", "fitness", "cardio workout", "calories", "exercise", "burn"],
         "a": "Definitely — it's a full-body cardio workout disguised as fun. Expect an elevated heart rate, improved coordination, and serious stamina gains over a term."},
        {"q": "Do I get an online student portal after registering?",
         "kw": ["portal", "login", "account", "dashboard", "qr code"],
         "a": "Yes — once you complete checkout, we email you a secure portal login (with a generated password) where you can view your class details and entry QR code."},
        {"q": "Is there a company / advanced performance team?",
         "kw": ["company", "advanced team", "competitive", "premier"],
         "a": (f"Yes — **{company_p['name']}** is our flagship, audition-caliber team for stage-ready, competitive-level dancers." if company_p
               else "Yes — our top level is reserved for advanced, performance-ready dancers. Check Browse Program Options for current availability.")},
        {"q": "How can I contact the studio for more help?",
         "kw": ["contact", "phone", "email", "call", "support", "help", "talk to someone"],
         "a": "Happy to help directly — please call our support line at **2341239239**, or leave your question here and we'll follow up."},
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

    # Floating chat launcher icon (fixed bottom-right, pops the panel open/closed)
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

elif st.session_state.app_state == "admin_dashboard":
    st.markdown('<div class="bf-section-title"><h2>Registered Students</h2><p class="bf-muted">Full profile for every student who has registered or paid.</p></div>', unsafe_allow_html=True)

    if not st.session_state.student_db:
        st.info("No students yet. They'll appear here as soon as someone registers or pays.")
    else:
        df_students = pd.DataFrame(st.session_state.student_db)
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
                with st.expander(f"{badge} {row.get('Name', 'Unknown')} — {row.get('Class', '-')}"):
                    pc1, pc2 = st.columns(2)
                    with pc1:
                        st.markdown(f"**Name:** {row.get('Name', '-')}")
                        st.markdown(f"**Email:** {row.get('Email', '-')}")
                        st.markdown(f"**Program:** {row.get('Class', '-')} (#{row.get('Program Number', '-')})")
                        st.markdown(f"**Status:** {status}")
                    with pc2:
                        st.markdown(f"**Fee:** {fee_display}")
                        st.markdown(f"**Registered:** {row.get('Timestamp', '-')}")
                        st.markdown(f"**Portal Login Set:** {'Yes' if row.get('PasswordHash') else 'No'}")
        else:
            st.dataframe(
                df_students.drop(columns=["PasswordSalt", "PasswordHash"], errors="ignore"),
                use_container_width=True
            )
            st.caption("Passwords are hashed and hidden here for security. Use the CSV export below if you need the full raw record.")
            
            st.download_button(
                "⬇️ Export students CSV",
                data=df_students.to_csv(index=False).encode("utf-8"),
                file_name="bollyfusion_students_export.csv",
                mime="text/csv"
            )

    st.divider()
    
    # --- NEW: Database Restore Feature ---
    st.subheader("Database Management")
    st.markdown("If the Streamlit Cloud server restarts and clears the local database, you can upload your most recent CSV backup here to restore it.")
    
    with st.expander("Upload CSV Backup"):
        uploaded_file = st.file_uploader("Upload bollyfusion_students_export.csv", type=["csv"])
        if uploaded_file is not None:
            try:
                restored_df = pd.read_csv(uploaded_file)
                # Quick validation to ensure it's the right file format
                if "Email" in restored_df.columns and "Name" in restored_df.columns:
                    if st.button("Confirm & Restore Database", type="primary"):
                        lock = filelock.FileLock(f"{DB_FILE}.lock")
                        with lock:
                            # Save the uploaded file as the active database
                            restored_df.to_csv(DB_FILE, index=False)
                            # Update session state so the UI reflects the changes instantly
                            st.session_state.student_db = restored_df.to_dict('records')
                            _secure_chmod(DB_FILE)
                        st.success("Database restored successfully!")
                        st.rerun()
                else:
                    st.error("Invalid CSV format. Please upload a valid BollyFusion student export.")
            except Exception as e:
                st.error(f"Error reading CSV: {e}")

    st.write("")
    if st.button("Logout", use_container_width=True, on_click=navigate, args=("home",)): pass
