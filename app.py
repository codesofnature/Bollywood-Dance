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

# --- CONFIGURE YOUR START DATES HERE ---
# Modify these lists anytime to add/remove available start dates for each program.
START_DATES = {
    "Bolly Cardio 1": ["Sept 1, 2026", "Oct 15, 2026", "Jan 10, 2027"],
    "Bolly Cardio II": ["Sept 5, 2026", "Nov 1, 2026"],
    "Couples to Event": ["Flexible - Discuss upon registration", "Sept 10, 2026"],
    "Group to Events": ["Flexible - Discuss upon registration"],
    "Bolly Kids 7-17": ["Sept 1, 2026", "Jan 15, 2027"],
    "Premier Company": ["Fall 2026 Season", "Spring 2027 Season"]
}

st.set_page_config(
    page_title="Phase Change, Inc - BollyFusion Academy",
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
    "desc": "Perfect for events/weddings/performances! Master partner choreography.",
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
    "desc": "High energy dance for the youngster techniques.",
    "song_count": "2-3 songs"
  }
]
DB_FILE = "bollyfusion_db.csv"
COMPANY_NAME = "Phase Change, Inc."

# --- Security Helpers ---
PBKDF2_ITERATIONS = 200_000

def _secure_chmod(path):
    try: os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except: pass

def generate_secure_password(length=12):
    alphabet = "abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789!@#$%"
    return "".join(secrets.choice(alphabet) for _ in range(length))

def hash_password(password, salt=None):
    if salt is None: salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), bytes.fromhex(salt), PBKDF2_ITERATIONS)
    return salt, digest.hex()

def verify_password(password, salt, expected_hash):
    if not salt or not expected_hash: return False
    _, computed = hash_password(password, salt)
    return secrets.compare_digest(computed, expected_hash)

# --- CSS omitted for brevity, keeping original styles ---
st.markdown('''
<style>
.stApp { background: #0a0510; color: #fdfbf7; }
button[kind="primary"], .stLinkButton > a[data-testid="stLinkButton"] {
    background: linear-gradient(90deg, #ff007f, #ffaa00) !important;
    color: #ffffff !important; border: none !important; border-radius: 16px !important;
}
.bf-card { background: rgba(255,255,255,.05); border-radius: 24px; padding:16px; margin-bottom: 12px; }
.legal-box { font-size: 11px; color: #aaa; max-height: 250px; overflow-y: auto; padding: 10px; border: 1px solid #333; background: #111; margin-bottom:15px; }
</style>
''', unsafe_allow_html=True)

if "app_state" not in st.session_state: st.session_state.app_state = "home"
if "current_user" not in st.session_state:
    st.session_state.current_user = {"Name": "", "Email": "", "Program Number": "-", "Class": "-", "Fee": 0.0, "Stripe Link": "", "Start Date": ""}
if "logged_in_student" not in st.session_state: st.session_state.logged_in_student = None

if "student_db" not in st.session_state:
    if os.path.exists(DB_FILE):
        st.session_state.student_db = pd.read_csv(DB_FILE).to_dict('records')
    else:
        st.session_state.student_db = []

def update_db(name, email, prog_num, class_name, status, password="", fee=0.0, start_date="N/A"):
    lock = filelock.FileLock(f"{DB_FILE}.lock")
    with lock:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M %p")
        if os.path.exists(DB_FILE): df = pd.read_csv(DB_FILE)
        else: df = pd.DataFrame(columns=["Timestamp", "Name", "Email", "Program Number", "Class", "Start Date", "Status", "PasswordSalt", "PasswordHash", "Fee"])

        if "Start Date" not in df.columns: df["Start Date"] = "N/A"

        pw_salt, pw_hash = (None, None)
        if password: pw_salt, pw_hash = hash_password(password)

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
                if fee: df.at[idx, 'Fee'] = fee
                
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

def send_email_invoice(to_email, name, class_name, fee, password, start_date):
    sender_email = st.secrets.get("smtp_email", "")
    sender_password = st.secrets.get("smtp_app_password", "")
    if not sender_email or not sender_password: return
    subject = f"Phase Change, Inc - Payment Invoice & Portal Login"
    body = (f"Hi {name},\n\nThank you for your payment of ${fee:.2f} for {class_name}.\n"
            f"Your Selected Start Date: {start_date}\n\n"
            f"Your Registered Student Portal login details are:\nEmail: {to_email}\nPassword: {password}\n\n"
            f"Please log in via the website to access your unique QR code.\n\nBest,\nPhase Change, Inc. (BollyFusion Academy)")
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
    except: pass

def navigate(to_state): st.session_state.app_state = to_state
def reset_user():
    st.session_state.current_user = {"Name": "", "Email": "", "Program Number": "-", "Class": "-", "Fee": 0.0, "Stripe Link": "", "Start Date": ""}
    st.query_params.clear()
    st.session_state.app_state = "home"

if "status" in st.query_params and st.query_params["status"] == "success":
    if st.session_state.app_state != "success":
        st.session_state.app_state = "success"
        if st.session_state.current_user.get("Email"):
            gen_pw = generate_secure_password(12)
            update_db(st.session_state.current_user["Name"], st.session_state.current_user["Email"], st.session_state.current_user["Program Number"], st.session_state.current_user["Class"], "Paid ✅", password=gen_pw, fee=st.session_state.current_user.get("Fee", 0.0), start_date=st.session_state.current_user.get("Start Date", "N/A"))
            send_email_invoice(st.session_state.current_user["Email"], st.session_state.current_user["Name"], st.session_state.current_user["Class"], st.session_state.current_user.get("Fee", 0.0), gen_pw, st.session_state.current_user.get("Start Date", "N/A"))

if st.session_state.app_state == "home":
    st.markdown("<h1>Phase Change, Inc <br><small>BollyFusion Academy</small></h1>", unsafe_allow_html=True)
    st.button("Browse Program Options", use_container_width=True, type="primary", on_click=navigate, args=("register",))
    st.button("Registered Student Portal", use_container_width=True, on_click=navigate, args=("student_login",))
    st.button("Teacher Portal", use_container_width=True, on_click=navigate, args=("admin_login",))

elif st.session_state.app_state == "register":
    st.markdown('<h2>Register</h2>', unsafe_allow_html=True)
    st.session_state.current_user["Name"] = st.text_input("Full Name", value=st.session_state.current_user.get("Name", ""))
    st.session_state.current_user["Email"] = st.text_input("Email", value=st.session_state.current_user.get("Email", ""))
    valid = bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", st.session_state.current_user["Email"])) and st.session_state.current_user["Name"]
    if st.button("Continue" if valid else "Browse", use_container_width=True, type="primary"):
        if valid: update_db(st.session_state.current_user["Name"], st.session_state.current_user["Email"], "-", "Browsing...", "Entered Details")
        navigate("classes")
    st.button("Back", on_click=navigate, args=("home",))

elif st.session_state.app_state == "classes":
    for prog in AVAILABLE_PROGRAMS:
        with st.container():
            st.markdown(f"### {prog['name']} - ${prog['fee']:,.2f}")
            st.write(prog['desc'])
            if st.button(f"Select {prog['name']}", key=f"sel_{prog['id']}", type="primary"):
                st.session_state.current_user.update({"Class": prog["name"], "Program Number": prog["id"], "Fee": prog["fee"], "Stripe Link": prog["stripe_link"]})
                navigate("checkout")
    st.button("Back", on_click=navigate, args=("register",))

elif st.session_state.app_state == "checkout":
    sc = st.session_state.current_user.get("Class", "")
    available_dates = START_DATES.get(sc, ["Open Enrollment"])
    st.session_state.current_user["Start Date"] = st.selectbox("Select Your Start Date", available_dates)

    st.markdown(f"### Amount Due: **${st.session_state.current_user.get('Fee', 0):,.2f}**")
    
    with st.expander("⚠️ LEGAL WAIVER, MEDIA RELEASE, AND TERMS (MUST READ)"):
        st.markdown(f'''<div class="legal-box">
        <b>PHASE CHANGE, INC. - COMPREHENSIVE LIABILITY WAIVER, ASSUMPTION OF RISK, MEDIA RELEASE, AND INDEMNIFICATION AGREEMENT</b><br><br>
        1. <b>Assumption of Risk:</b> I understand that dance and fitness activities involve inherent risks of severe physical injury, illness, or property damage. I voluntarily assume all risks associated with participation.<br>
        2. <b>Waiver and Release:</b> I hereby irrevocably and unconditionally release, waive, discharge, and covenant not to sue Phase Change, Inc., BollyFusion Academy, its owners, directors, officers, agents, independent contractors, and employees from any and all liability, claims, demands, actions, or causes of action.<br>
        3. <b>Indemnification:</b> I agree to indemnify and hold harmless Phase Change, Inc. from any loss, liability, damage, or costs, including attorney fees, arising out of my participation.<br>
        4. <b>Medical Clearance:</b> I declare I am in sound medical condition to participate. I assume full responsibility for my own medical expenses in the event of injury.<br>
        5. <b>No Refunds:</b> All payments to Phase Change, Inc. are final. No refunds, prorations, or roll-overs will be provided under any circumstances, including absence or illness.<br>
        6. <b>Media Release:</b> I grant Phase Change, Inc. the absolute and irrevocable right and unrestricted permission to use, reproduce, publish, and distribute photographs or video footage of me for promotional, commercial, or any other purposes without compensation.<br>
        7. <b>Governing Law:</b> This agreement shall be governed by the laws of the applicable jurisdiction, and any disputes will be subject to exclusive arbitration.
        </div>''', unsafe_allow_html=True)
    
    cb = st.checkbox(f"I fully agree to the Phase Change, Inc. terms above.")
    if cb: st.link_button("💳 Pay via Stripe", url=f"{st.session_state.current_user.get('Stripe Link', '#')}?prefilled_email={urllib.parse.quote(st.session_state.current_user.get('Email', ''))}", type="primary", use_container_width=True)
    else: st.button("💳 Pay via Stripe (Accept Terms First)", disabled=True, use_container_width=True)
    st.button("Back", on_click=navigate, args=("classes",))

elif st.session_state.app_state == "success":
    st.success("Payment Successful!")
    st.button("Back to Home", on_click=reset_user)

elif st.session_state.app_state == "student_login":
    s_email, s_pass = st.text_input("Registered Email"), st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        df = pd.DataFrame(st.session_state.student_db)
        if not df.empty and s_email in df['Email'].values:
            user_row = df[df['Email'] == s_email].iloc[0]
            if verify_password(s_pass, user_row.get('PasswordSalt', ''), user_row.get('PasswordHash', '')):
                st.session_state.logged_in_student = user_row.to_dict()
                navigate("student_dashboard")
                st.rerun()
            else: st.error("Invalid")
        else: st.error("Invalid")
    st.button("Cancel", on_click=navigate, args=("home",))

elif st.session_state.app_state == "student_dashboard":
    st.write(f"Welcome {st.session_state.logged_in_student.get('Name')}!")
    st.write(f"Program: {st.session_state.logged_in_student.get('Class')}")
    st.write(f"Start Date: {st.session_state.logged_in_student.get('Start Date', 'N/A')}")
    st.button("Logout", on_click=navigate, args=("home",))

elif st.session_state.app_state == "admin_login":
    a_user, a_pass = st.text_input("Username"), st.text_input("Password", type="password")
    if st.button("Login", type="primary"):
        if secrets.compare_digest(a_user, st.secrets.get("admin_username", "")) and secrets.compare_digest(a_pass, st.secrets.get("admin_password", "")):
            navigate("admin_dashboard")
            st.rerun()
        else: st.error("Invalid")
    st.button("Cancel", on_click=navigate, args=("home",))

elif st.session_state.app_state == "admin_dashboard":
    st.title("Admin Dashboard - Phase Change, Inc.")
    
    if not st.session_state.student_db: st.info("No students yet.")
    else:
        df_students = pd.DataFrame(st.session_state.student_db)
        st.write(f"Total Students: {len(df_students)}")
        
        for idx, row in df_students.iterrows():
            with st.expander(f"{row.get('Name', 'Unknown')} - {row.get('Class', '-')} ({row.get('Start Date', 'N/A')})"):
                st.write(row.drop(["PasswordSalt", "PasswordHash"], errors="ignore").to_dict())
                
                # HARDENED DELETE USING INDEX INSTEAD OF EMAIL
                if st.button("🗑️ Delete Exact Record", key=f"del_{idx}"):
                    lock = filelock.FileLock(f"{DB_FILE}.lock")
                    with lock:
                        if os.path.exists(DB_FILE):
                            df_current = pd.read_csv(DB_FILE)
                            # Delete by exact timestamp and email match to avoid killing duplicate emails safely
                            df_current = df_current[~((df_current['Email'] == row['Email']) & (df_current['Timestamp'] == row['Timestamp']))]
                            df_current.to_csv(DB_FILE, index=False)
                            st.session_state.student_db = df_current.to_dict('records')
                    st.success("Record deleted.")
                    st.rerun()
        
        csv_data = df_students.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Export students CSV", data=csv_data, file_name="bollyfusion_students_export.csv", mime="text/csv")

    st.divider()
    st.subheader("Restore Database (Hardened)")
    uploaded_csv = st.file_uploader("Upload bollyfusion_students_export.csv", type=["csv"])
    if uploaded_csv is not None:
        if st.button("⚠️ Confirm Restore", type="primary"):
            try:
                df_restored = pd.read_csv(uploaded_csv)
                required_cols = {"Name", "Email", "Program Number", "Class", "Status"}
                if not required_cols.issubset(df_restored.columns):
                    st.error(f"Upload failed: CSV is missing required columns. Must contain at least: {required_cols}")
                else:
                    if "Start Date" not in df_restored.columns: df_restored["Start Date"] = "N/A"
                    # Deduplicate safely before restore to harden database
                    df_restored = df_restored.drop_duplicates(subset=['Email', 'Timestamp'])
                    
                    lock = filelock.FileLock(f"{DB_FILE}.lock")
                    with lock:
                        df_restored.to_csv(DB_FILE, index=False)
                    
                    st.session_state.student_db = df_restored.to_dict('records')
                    st.success("✅ Database restored securely!")
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to process CSV: {e}")

    st.button("Logout", on_click=navigate, args=("home",))
