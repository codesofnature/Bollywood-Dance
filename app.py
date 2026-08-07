import streamlit as st
import urllib.parse
import pandas as pd
import re
import os
import datetime
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

st.markdown('''
<style>
/* Cinematic Bollywood Theme */
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
    padding-left: calc(1rem + env(safe-area-inset-left));
    padding-right: calc(1rem + env(safe-area-inset-right));
}

input, textarea, select {
    font-size: 16px !important;
}

button {
    min-height: 50px;
    border-radius: 16px !important;
    font-weight: 800 !important;
}

.stButton > button, .stLinkButton > a {
    width: 100%;
    padding: 14px 18px;
    font-size: 16px;
    text-align: center;
    border-radius: 16px !important;
    font-weight: 800 !important;
}

/* Primary Button Styling */
button[kind="primary"], .stLinkButton > a[data-testid="stLinkButton"] {
    background: linear-gradient(90deg, #ff007f, #ffaa00) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 4px 15px rgba(255, 0, 127, 0.3);
    transition: opacity 0.15s ease !important;
}

button[kind="primary"]:disabled,
button[kind="primary"][disabled] {
    background: linear-gradient(90deg, #ff007f, #ffaa00) !important;
    color: #ffffff !important;
    opacity: 0.45 !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
}
/* Secondary Button Styling (The 'Back' button) */
button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.05) !important;
    color: #fdfbf7 !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    box-shadow: none !important;
    transition: all 0.2s ease !important;
}

button[kind="secondary"]:hover,
button[kind="secondary"]:active,
button[kind="secondary"]:focus {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.4) !important;
    color: #ffffff !important;
}
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

.bf-hero {
    border-radius: 28px;
    padding: 32px 20px;
    border: 1px solid rgba(255, 255, 255, .12);
    background:
        linear-gradient(135deg, rgba(255, 0, 127, .2), rgba(255, 170, 0, .15), rgba(138, 43, 226, .15));
    text-align: center;
    margin-bottom: 18px;
}

.bf-pill {
    display: inline-block;
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(255, 255, 255, .08);
    border: 1px solid rgba(255, 255, 255, .12);
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 12px;
}

.bf-hero h1 {
    margin: 0 0 10px;
    font-size: clamp(2rem, 5vw, 3.3rem);
    line-height: 1.04;
    letter-spacing: -.04em;
}

.bf-gradient {
    background: linear-gradient(90deg, #ffaa00, #ff007f, #8a2be2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
}

.bf-muted { color: rgba(253, 251, 247, .7); }
.bf-section-title h2 { margin-bottom: 4px; }

.bf-card {
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, .15);
    background: rgba(255, 255, 255, .05);
    margin-bottom: 12px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}

.bf-media {
    position: relative;
    aspect-ratio: 16 / 10;
    background: linear-gradient(135deg, rgba(255, 0, 127, .35), rgba(255, 170, 0, .28));
}

.bf-media img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.bf-overlay {
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(10, 5, 16, .85), transparent 60%);
}

.bf-badge {
    position: absolute;
    top: 12px;
    left: 12px;
    padding: 7px 10px;
    border-radius: 999px;
    background: rgba(0, 0, 0, .45);
    border: 1px solid rgba(255, 255, 255, .25);
    font-size: 12px;
    font-weight: 800;
    color: white;
}

.bf-badge-bottom {
    top: auto;
    bottom: 12px;
    left: auto;
    right: 12px;
    background: rgba(255, 170, 0, .25);
}

.bf-body { padding: 16px; }
.bf-body h3 { margin: 0 0 10px; font-size: 1.05rem; }

.bf-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }
.bf-chip {
    padding: 7px 9px;
    border-radius: 999px;
    background: rgba(255, 255, 255, .08);
    border: 1px solid rgba(255, 255, 255, .08);
    font-size: 12px;
    color: rgba(253, 251, 247, .75);
}

.bf-price {
    font-size: 1.25rem;
    font-weight: 900;
    color: #00e676;
    margin-top: 8px;
}

.bf-summary {
    display: grid;
    gap: 12px;
    padding: 16px;
    border-radius: 20px;
    background: rgba(255, 255, 255, .05);
    border: 1px solid rgba(255, 255, 255, .1);
    margin-bottom: 18px;
}

.bf-summary div { display: flex; justify-content: space-between; gap: 12px; }

.bf-id {
    text-align: center;
    padding: 20px;
    border-radius: 24px;
    background:
        linear-gradient(135deg, rgba(255, 170, 0, .15), rgba(255, 0, 127, .15), rgba(138, 43, 226, .15));
    border: 1px solid rgba(255, 255, 255, .15);
    margin-bottom: 16px;
}

@media (max-width: 700px) {
    div[data-baseweb="row"] { flex-direction: column !important; }
    div[data-baseweb="col"] { width: 100% !important; min-width: 100% !important; }
    .block-container { padding-left: 12px; padding-right: 12px; }
}
</style>
''', unsafe_allow_html=True)

if "app_state" not in st.session_state:
    st.session_state.app_state = "home"

if "current_user" not in st.session_state:
    st.session_state.current_user = {
        "Name": "", "Email": "", "Program Number": "-", "Class": "-", "Fee": 0.0, "Stripe Link": ""
    }

if "logged_in_student" not in st.session_state:
    st.session_state.logged_in_student = None

# --- Persistent CSV Database Setup ---
if "student_db" not in st.session_state:
    if os.path.exists(DB_FILE):
        st.session_state.student_db = pd.read_csv(DB_FILE).to_dict('records')
    else:
        st.session_state.student_db = []

# Update DB Function that UPSERTS to prevent garbage rows
def update_db(name, email, prog_num, class_name, status, password="", fee=0.0):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
    df = pd.DataFrame(st.session_state.student_db)
    
    if not df.empty and email and email != "No Details Provided":
        if email in df['Email'].values:
            # Update existing user instead of adding garbage rows
            idx = df.index[df['Email'] == email].tolist()[0]
            df.at[idx, 'Timestamp'] = timestamp
            df.at[idx, 'Name'] = name
            df.at[idx, 'Program Number'] = prog_num
            df.at[idx, 'Class'] = class_name
            df.at[idx, 'Status'] = status
            if password:
                df.at[idx, 'Password'] = password
            if fee:
                df.at[idx, 'Fee'] = fee
                
            st.session_state.student_db = df.to_dict('records')
            df.to_csv(DB_FILE, index=False)
            return

    # Add new record
    record = {
        "Timestamp": timestamp,
        "Name": name,
        "Email": email,
        "Program Number": prog_num,
        "Class": class_name,
        "Status": status,
        "Password": password,
        "Fee": fee
    }
    st.session_state.student_db.append(record)
    pd.DataFrame(st.session_state.student_db).to_csv(DB_FILE, index=False)
# -------------------------------------

# Email function
def send_email_invoice(to_email, name, class_name, fee, password):
    # TO MAKE THIS WORK: Enter your real Gmail & App Password here.
    sender_email = "YOUR_GMAIL_HERE@gmail.com"
    sender_password = "YOUR_APP_PASSWORD_HERE"
    admin_email = "uday77@gmail.com"
    
    subject = "BollyFusion Academy - Payment Invoice & Portal Login"
    body = (
        f"Hi {name},\n\n"
        f"Thank you for your payment of ${fee:.2f} for {class_name}.\n\n"
        f"Your Registered Student Portal login details are:\n"
        f"Email: {to_email}\n"
        f"Password: {password}\n\n"
        f"Please log in via the website to access your unique QR code for class entry and view this invoice.\n\n"
        f"Best,\nBollyFusion Academy"
    )
    
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Bcc'] = admin_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        st.success(f"Invoice and Portal Password emailed successfully to {to_email} and {admin_email}.")
    except Exception as e:
        # Fails silently for the user so it doesn't crash the app if no SMTP config is present
        pass

def navigate(to_state):
    st.session_state.app_state = to_state

def reset_user():
    st.session_state.current_user = {
        "Name": "", "Email": "", "Program Number": "-", "Class": "-", "Fee": 0.0, "Stripe Link": ""
    }
    st.query_params.clear()
    st.session_state.app_state = "home"

# --- Client IP Detection ---
def get_client_ip():
    try:
        if hasattr(st, 'context') and hasattr(st.context, 'headers'):
            return st.context.headers.get("X-Forwarded-For", "Unknown IP").split(',')[0]
        from streamlit.web.server.websocket_headers import _get_websocket_headers
        headers = _get_websocket_headers()
        if headers and "X-Forwarded-For" in headers:
            return headers.get("X-Forwarded-For", "Unknown IP").split(',')[0]
    except Exception:
        pass
    return "IP Unavailable"

# --- Dynamic Processing Logic ---
def process_registration(is_valid):
    if not is_valid:
        ip_addr = get_client_ip()
        update_db(f"Guest ({ip_addr})", "No Details Provided", "-", "Browsing Programs...", "Just Browsing")
    else:
        update_db(st.session_state.current_user["Name"], 
                  st.session_state.current_user["Email"], 
                  "-", "Browsing Programs...", "Entered Details")
    navigate("classes")

# --- Stripe Success Listener ---
if "status" in st.query_params and st.query_params["status"] == "success":
    if st.session_state.app_state != "success":
        st.session_state.app_state = "success"
        if st.session_state.current_user.get("Email"):
            # Generate random 6 character password
            gen_pw = "".join(random.choices(string.ascii_letters + string.digits, k=6))
            
            update_db(
                st.session_state.current_user["Name"],
                st.session_state.current_user["Email"],
                st.session_state.current_user["Program Number"],
                st.session_state.current_user["Class"],
                "Paid ✅",
                password=gen_pw,
                fee=st.session_state.current_user.get("Fee", 0.0)
            )
            # Trigger Email
            send_email_invoice(
                st.session_state.current_user["Email"],
                st.session_state.current_user["Name"],
                st.session_state.current_user["Class"],
                st.session_state.current_user.get("Fee", 0.0),
                gen_pw
            )
# -------------------------------


if st.session_state.app_state == "home":
    st.markdown('''
    <div class="bf-hero">
        <div class="bf-pill">🎬 Bollywood Dance Studio</div>
        <h1>Master Cinematic Dance on Any Stage, <span class="bf-gradient">built for every stage</span></h1>
        <p class="bf-muted">
            Choose, Register, Pay            
        </p>
    </div>
    ''', unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Browse Program Options", use_container_width=True, type="primary", on_click=navigate, args=("register",))
    with col2:
        st.button("Registered Student Portal", use_container_width=True, on_click=navigate, args=("student_login",))
    with col3:
        st.button("Teacher Portal", use_container_width=True, on_click=navigate, args=("admin_login",))


elif st.session_state.app_state == "register":
    st.markdown(
        '<div class="bf-section-title"><h2>BROWSE PROGRAM OPTIONS AND PRICES</h2>'
        '<p class="bf-muted">Enter your details, or simply browse.</p></div>',
        unsafe_allow_html=True
    )

    st.session_state.current_user["Name"] = st.text_input("Full Name", value=st.session_state.current_user.get("Name", ""), placeholder="What do we call you?")
    st.session_state.current_user["Email"] = st.text_input("Email", value=st.session_state.current_user.get("Email and / or Phone", ""), placeholder=".com .edu email ID")

    st.write("")

    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    is_valid_email = bool(re.match(email_pattern, st.session_state.current_user["Email"]))
    
    valid = (st.session_state.current_user["Name"].strip() != "" and is_valid_email)

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", use_container_width=True, on_click=navigate, args=("home",))
    with col2:
        btn_label = "Continue" if valid else "I'll just browse"
        st.button(btn_label, use_container_width=True, type="primary", on_click=process_registration, args=(valid,))


elif st.session_state.app_state == "classes":
    st.markdown(
        '<div class="bf-section-title"><h2>Choose a Program</h2>'
        '<p class="bf-muted">Tap a program to continue to secure checkout.</p></div>',
        unsafe_allow_html=True
    )

    if not AVAILABLE_PROGRAMS:
        st.info("No programs are currently available.")
    else:
        cols = st.columns(2)
        for idx, prog in enumerate(AVAILABLE_PROGRAMS):
            with cols[idx % 2]:
                st.markdown(f'''
                <div class="bf-card">
                    <div class="bf-media">
                        <img src="{prog['poster']}" alt="{prog['name']}" onerror="this.style.display='none'">
                        <div class="bf-overlay"></div>
                        <div class="bf-badge">{prog['weeks']} Weeks</div>
                        <div class="bf-badge bf-badge-bottom">{prog['song_count']}</div>
                    </div>
                    <div class="bf-body">
                        <h3>{prog['name']}</h3>
                        <div class="bf-chips">
                            <span class="bf-chip">💃 {prog['hours']} hrs/wk</span>
                            <span class="bf-chip">🗓 {prog['weeks']} weeks</span>
                            <span class="bf-chip">🎵 {prog['song_count']}</span>
                        </div>
                        <p class="bf-muted">{prog['desc']}</p>
                        <div class="bf-price">${prog['fee']:,.2f}</div>
                    </div>
                </div>
                ''', unsafe_allow_html=True)

                if st.button(f"Select {prog['name']}", key=f"select_{prog['id']}", use_container_width=True, type="primary"):
                    st.session_state.current_user["Class"] = prog["name"]
                    st.session_state.current_user["Program Number"] = prog["id"]
                    st.session_state.current_user["Fee"] = prog["fee"]
                    st.session_state.current_user["Stripe Link"] = prog["stripe_link"]
                    
                    update_db(st.session_state.current_user.get("Name", "Guest"), 
                              st.session_state.current_user.get("Email", "None"), 
                              prog["id"], prog["name"], "Pending Payment")

                    navigate("checkout")

    st.write("")
    st.button("Back", use_container_width=True, on_click=navigate, args=("register",))


elif st.session_state.app_state == "checkout":
    st.markdown(
        '<div class="bf-section-title"><h2>Secure Checkout</h2>'
        '<p class="bf-muted">Review your program and accept all legal terms.</p></div>',
        unsafe_allow_html=True
    )

    selected_class = st.session_state.current_user.get("Class", "")
    selected_fee = st.session_state.current_user.get("Fee", 0)
    
    stripe_link = st.session_state.current_user.get("Stripe Link", "#")
    checkout_url = f"{stripe_link}?prefilled_email={urllib.parse.quote(st.session_state.current_user.get('Email', ''))}"

    st.markdown(f'''
    <div class="bf-summary">
        <div>
            <span class="bf-muted">Program</span>
            <strong>{selected_class}</strong>
        </div>
        <div>
            <span class="bf-muted">Student</span>
            <strong>{st.session_state.current_user.get("Name", "Guest")}</strong>
        </div>
        <div>
            <span class="bf-muted">Amount Due</span>
            <strong class="bf-price">${selected_fee:,.2f}</strong>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("### Legal Agreements")

    cb1 = st.checkbox("I agree to the Physical Activity & Liability Waiver")
    cb2 = st.checkbox("I agree to the Media & Photography Release")

    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", use_container_width=True, on_click=navigate, args=("classes",))

    with col2:
        can_pay = cb1 and cb2

        if can_pay:
            st.link_button(
                f"💳 Pay ${selected_fee:,.2f} via Stripe",
                url=checkout_url,
                use_container_width=True,
                type="primary"
            )
        else:
            st.button(
                f"💳 Pay ${selected_fee:,.2f} via Stripe",
                use_container_width=True,
                type="primary",
                disabled=True
            )


elif st.session_state.app_state == "success":
    st.markdown(
        '<div class="bf-section-title"><h2>Digital Studio ID & Registration Confirmed</h2>'
        '<p class="bf-muted">Your invoice and portal password have been emailed to you.</p></div>',
        unsafe_allow_html=True
    )

    u_name = st.session_state.current_user.get("Name", "Guest")
    u_class = st.session_state.current_user.get("Class", "")

    qr_data = urllib.parse.quote(f"Student:{u_name}|Class:{u_class}")
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qr_data}"

    st.markdown(f'''
    <div class="bf-id">
        <div class="bf-pill">✅ Payment Successful</div>
        <h2>{u_name}</h2>
        <p class="bf-muted">{u_class}</p>
    </div>
    ''', unsafe_allow_html=True)

    st.image(qr_url, use_container_width=True)

    st.write("")
    st.button("Done (Back to Home)", use_container_width=True, type="primary", on_click=reset_user)

# --- NEW: Student Login & Dashboard ---
elif st.session_state.app_state == "student_login":
    st.markdown(
        '<div class="bf-section-title"><h2>🎓 Registered Student Portal</h2>'
        '<p class="bf-muted">Login using the email and password sent in your payment invoice.</p></div>',
        unsafe_allow_html=True
    )

    s_email = st.text_input("Registered Email")
    s_pass = st.text_input("Password", type="password")

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Cancel", use_container_width=True, on_click=navigate, args=("home",))
    with col2:
        if st.button("Login", use_container_width=True, type="primary"):
            df = pd.DataFrame(st.session_state.student_db)
            if not df.empty and s_email in df['Email'].values:
                # Get user row
                user_row = df[df['Email'] == s_email].iloc[0]
                if str(user_row.get('Password', '')) == s_pass and s_pass != "":
                    st.session_state.logged_in_student = user_row.to_dict()
                    navigate("student_dashboard")
                else:
                    st.error("Invalid password.")
            else:
                st.error("Email not found in our records.")

elif st.session_state.app_state == "student_dashboard":
    u_data = st.session_state.logged_in_student
    st.markdown(
        f'<div class="bf-section-title"><h2>Welcome back, {u_data.get("Name", "Student")}!</h2>'
        '<p class="bf-muted">Here are your class details and invoice.</p></div>',
        unsafe_allow_html=True
    )

    tab1, tab2 = st.tabs(["QR Code Entry ID", "My Invoice"])
    
    with tab1:
        st.markdown("### Class Entry QR Code")
        st.info(f"Show this to the instructor for **{u_data.get('Class', 'Dance Class')}**.")
        qr_data = urllib.parse.quote(f"Student:{u_data.get('Name')}|Class:{u_data.get('Class')}")
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={qr_data}"
        st.image(qr_url)
        
    with tab2:
        st.markdown("### Payment Invoice")
        st.markdown(f'''
        <div class="bf-summary">
            <div><span class="bf-muted">Date</span><strong>{u_data.get("Timestamp", "N/A")}</strong></div>
            <div><span class="bf-muted">Student Name</span><strong>{u_data.get("Name", "N/A")}</strong></div>
            <div><span class="bf-muted">Email</span><strong>{u_data.get("Email", "N/A")}</strong></div>
            <div><span class="bf-muted">Service/Class</span><strong>{u_data.get("Class", "N/A")}</strong></div>
            <div><span class="bf-muted">Status</span><strong>{u_data.get("Status", "N/A")}</strong></div>
            <div><span class="bf-muted">Total Paid</span><strong class="bf-price">${float(u_data.get("Fee", 0)):,.2f}</strong></div>
        </div>
        ''', unsafe_allow_html=True)
        
    st.write("")
    if st.button("Logout", use_container_width=True):
        st.session_state.logged_in_student = None
        navigate("home")

# --- MODIFIED: Admin Login & Dashboard ---
elif st.session_state.app_state == "admin_login":
    st.markdown(
        '<div class="bf-section-title"><h2>🔒 Admin Login</h2>'
        '<p class="bf-muted">Use admin / admin123.</p></div>',
        unsafe_allow_html=True
    )

    a_user = st.text_input("Username")
    a_pass = st.text_input("Password", type="password")

    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Cancel", use_container_width=True, on_click=navigate, args=("home",))
    with col2:
        if st.button("Login", use_container_width=True, type="primary"):
            if a_user == "manasidharmadhikari" and a_pass == "bestofbollywood7925":
                navigate("admin_dashboard")
            else:
                st.error("Invalid credentials.")


elif st.session_state.app_state == "admin_dashboard":
    st.markdown(
        '<div class="bf-section-title"><h2>📊 Teacher Admin Portal</h2>'
        '<p class="bf-muted">Select rows and hit delete (or use the trash icon) to remove garbage entries. Hit save to lock changes.</p></div>',
        unsafe_allow_html=True
    )

    if os.path.exists(DB_FILE) and st.session_state.student_db:
        df = pd.DataFrame(st.session_state.student_db)
        
        # Add dynamic QR Link and Invoice String for Admin View
        if 'Name' in df.columns and 'Class' in df.columns:
            df['Admin_QR_Link'] = df.apply(
                lambda row: f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=Student:{urllib.parse.quote(str(row['Name']))}|Class:{urllib.parse.quote(str(row['Class']))}", 
                axis=1
            )
        
        # Editable dataframe that allows row deletion
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True, hide_index=True)
        
        if st.button("💾 Save Database Changes", type="primary"):
            st.session_state.student_db = edited_df.to_dict('records')
            edited_df.to_csv(DB_FILE, index=False)
            st.success("Database changes saved successfully!")

        csv = edited_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="bollyfusion-registrations.csv", mime="text/csv", key="download_roster_csv")
    else:
        st.info("No students have registered yet during this session.")

    st.write("")
    st.button("Logout", use_container_width=True, on_click=navigate, args=("home",))
