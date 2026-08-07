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
    padding-top: calc(1.8rem + env(safe-area-inset-top));
    padding-bottom: calc(2rem + env(safe-area-inset-bottom));
}

input, textarea, select { font-size: 16px !important; }

button { min-height: 50px; border-radius: 16px !important; font-weight: 800 !important; }

.stButton > button, .stLinkButton > a {
    width: 100%; padding: 14px 18px; font-size: 16px; text-align: center;
    border-radius: 16px !important; font-weight: 800 !important;
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
    border-radius: 28px; padding: 32px 20px;
    border: 1px solid rgba(255, 255, 255, .12);
    background: linear-gradient(135deg, rgba(255, 0, 127, .2), rgba(255, 170, 0, .15), rgba(138, 43, 226, .15));
    text-align: center; margin-bottom: 18px;
}

.bf-pill {
    display: inline-block; padding: 8px 12px; border-radius: 999px;
    background: rgba(255, 255, 255, .08); border: 1px solid rgba(255, 255, 255, .12);
    font-size: 13px; font-weight: 800; margin-bottom: 12px;
}

.bf-hero h1 { margin: 0 0 10px; font-size: clamp(2rem, 5vw, 3.3rem); line-height: 1.04; letter-spacing: -.04em; }

.bf-gradient {
    background: linear-gradient(90deg, #ffaa00, #ff007f, #8a2be2);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}

.media-grid { 
    display: flex; gap: 10px; overflow-x: auto; padding: 10px 0; margin-top: 15px; 
    scroll-snap-type: x mandatory;
}
.media-grid::-webkit-scrollbar { display: none; }
.media-grid > * {
    flex: 0 0 auto; width: 240px; height: 140px; border-radius: 12px; 
    object-fit: cover; border: 1px solid rgba(255,255,255,0.2); scroll-snap-align: center;
}

.bf-muted { color: rgba(253, 251, 247, .7); }
.bf-card {
    border-radius: 24px; overflow: hidden; border: 1px solid rgba(255, 255, 255, .15);
    background: rgba(255, 255, 255, .05); margin-bottom: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}
.bf-media { position: relative; aspect-ratio: 16 / 10; }
.bf-media img { width: 100%; height: 100%; object-fit: cover; display: block; }
.bf-overlay { position: absolute; inset: 0; background: linear-gradient(to top, rgba(10, 5, 16, .85), transparent 60%); }
.bf-body { padding: 16px; }
.bf-price { font-size: 1.25rem; font-weight: 900; color: #00e676; margin-top: 8px; }

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
    # Splash UI containing 5 placeholder components (3 Imgs, 2 Vids) 
    st.markdown('''
    <div class="bf-hero">
        <div class="bf-pill">🎬 Bollywood Dance Studio</div>
        <h1>Master Cinematic Dance on Any Stage, <span class="bf-gradient">built for every stage</span></h1>
        <p class="bf-muted">Choose, Register, Pay</p>
        <div class="media-grid">
            <img src="https://images.unsplash.com/photo-1543857778-c4a1a3e0b2eb?auto=format&fit=crop&w=400&q=80" alt="Image 1"/>
            <video autoplay loop muted playsinline src="https://www.w3schools.com/html/mov_bbb.mp4"></video>
            <img src="https://images.unsplash.com/photo-1516450360452-9312f5e86fc7?auto=format&fit=crop&w=400&q=80" alt="Image 2"/>
            <video autoplay loop muted playsinline src="https://www.w3schools.com/html/mov_bbb.mp4"></video>
            <img src="https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=400&q=80" alt="Image 3"/>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1: st.button("Browse Program Options", use_container_width=True, type="primary", on_click=navigate, args=("register",))
    with col2: st.button("Registered Student Portal", use_container_width=True, on_click=navigate, args=("student_login",))
    with col3: st.button("Teacher Portal", use_container_width=True, on_click=navigate, args=("admin_login",))
    
    st.divider()
    
    # Splash Screen Chatbot logic
    st.markdown("### 💬 Chat with us")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Hi! Do you have any questions about our programs, schedules, or pricing?"}]
    if "chat_failed_attempts" not in st.session_state:
        st.session_state.chat_failed_attempts = 0

    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).write(msg["content"])

    prompt = st.chat_input("Ask a question...")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        prompt_lower = prompt.lower()
        
        # Prepopulated logic
        if any(word in prompt_lower for word in ["price", "cost", "fee", "how much"]):
            answer = "Our classes range based on the level and duration. Tap 'Browse Program Options' above for full pricing details!"
        elif any(word in prompt_lower for word in ["schedule", "time", "when", "days"]):
            answer = "Schedules vary by program. Please browse our program options to see specific class dates and hours."
        elif any(word in prompt_lower for word in ["location", "where", "studio"]):
            answer = "We are located at the Main Studio. Registered students receive exact access/entry details upon checkout."
        else:
            st.session_state.chat_failed_attempts += 1
            if st.session_state.chat_failed_attempts >= 3:
                answer = "I'm sorry, I couldn't find a good answer to your recent questions. **Please contact our support at 2341239239** for immediate assistance."
            else:
                answer = "I'm not quite sure about that. Could you ask something else regarding prices, schedule, or location?"
                
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
                    update_db(st.session_state.current_user.get("Name", "Guest"), st.session_state.current_user.get("Email", "None"), prog["id"], prog["name"], "Pending Payment")
                    navigate("checkout")
    st.write("")
    st.button("Back", use_container_width=True, on_click=navigate, args=("register",))

elif st.session_state.app_state == "checkout":
    selected_class, selected_fee = st.session_state.current_user.get("Class", ""), st.session_state.current_user.get("Fee", 0)
    checkout_url = f"{st.session_state.current_user.get('Stripe Link', '#')}?prefilled_email={urllib.parse.quote(st.session_state.current_user.get('Email', ''))}"
    st.markdown(f"### Amount Due: **${selected_fee:,.2f}**")
    cb1 = st.checkbox("I agree to the Liability Waiver")
    cb2 = st.checkbox("I agree to the Media Release")
    st.write("")
    col1, col2 = st.columns(2)
    with col1: st.button("Back", use_container_width=True, on_click=navigate, args=("classes",))
    with col2:
        if cb1 and cb2: st.link_button(f"💳 Pay via Stripe", url=checkout_url, use_container_width=True, type="primary")
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
            else: st.error("Invalid credentials.")

elif st.session_state.app_state == "admin_dashboard":
    if st.session_state.student_db:
        st.data_editor(pd.DataFrame(st.session_state.student_db))
    if st.button("Logout", use_container_width=True, on_click=navigate, args=("home",)): pass
