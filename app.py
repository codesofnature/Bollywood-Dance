import streamlit as st
import urllib.parse
import pandas as pd
import sqlite3
import secrets
import string
import json
from pathlib import Path
from datetime import datetime

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
    "stripe_link": "https://buy.stripe.com/test_group_event_1000",
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
    "stripe_link": "https://buy.stripe.com/test_elite_fusion_2500",
    "poster": "https://github.com/codesofnature/Bollywood-Dance/blob/main/5.jpg?raw=true",
    "desc": "High energy dance for the youngster techniques for aspiring competitive performers.",
    "song_count": "2-3 songs"
  }
]

# =========================================================
# Persistent Storage (SQLite)
# ---------------------------------------------------------
# Stored next to this script so it survives Streamlit reruns
# and server restarts (as long as the host disk persists).
# On Streamlit Community Cloud the disk is reset on redeploy,
# so for a permanent production database, swap this file for
# a hosted database (e.g. Supabase/Postgres) using the same
# function signatures below.
# =========================================================
DB_PATH = Path(__file__).resolve().parent / "bollyfusion_students.db"
KEY_ALPHABET = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"  # no 0/O/1/I/L - easy to read aloud


def get_conn():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS students (
                email TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                program_number TEXT,
                class_name TEXT,
                fee REAL DEFAULT 0,
                status TEXT DEFAULT 'Pending',
                access_key TEXT UNIQUE,
                created_at TEXT,
                paid_at TEXT
            )
        ''')
        conn.commit()


def generate_access_key(length=12):
    return "".join(secrets.choice(KEY_ALPHABET) for _ in range(length))


def format_key(key):
    if not key:
        return ""
    return "-".join([key[i:i + 4] for i in range(0, len(key), 4)])


def register_student(email, name):
    '''Create the student's record on first registration, or refresh
    their name if they registered before. The access key is generated
    once and never changes, so it can double as a login credential.'''
    email = email.strip().lower()
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
        if row is None:
            access_key = generate_access_key()
            conn.execute('''
                INSERT INTO students (email, name, status, access_key, created_at)
                VALUES (?, ?, 'Pending', ?, ?)
            ''', (email, name.strip(), access_key, datetime.now().isoformat()))
            conn.commit()
            return access_key
        else:
            conn.execute("UPDATE students SET name = ? WHERE email = ?", (name.strip(), email))
            conn.commit()
            return row["access_key"]


def update_program(email, program_number, class_name, fee):
    email = email.strip().lower()
    with get_conn() as conn:
        conn.execute('''
            UPDATE students SET program_number = ?, class_name = ?, fee = ?
            WHERE email = ?
        ''', (program_number, class_name, fee, email))
        conn.commit()


def mark_status(email, status):
    email = email.strip().lower()
    with get_conn() as conn:
        if status == "Paid":
            conn.execute('''
                UPDATE students SET status = ?, paid_at = ? WHERE email = ?
            ''', (status, datetime.now().isoformat(), email))
        else:
            conn.execute("UPDATE students SET status = ? WHERE email = ?", (status, email))
        conn.commit()


def get_student(email):
    email = email.strip().lower()
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None


def get_student_by_credentials(email, access_key):
    email = email.strip().lower()
    access_key = access_key.strip().upper().replace("-", "").replace(" ", "")
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM students WHERE email = ? AND access_key = ?",
            (email, access_key)
        ).fetchone()
        return dict(row) if row else None


def get_all_students():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM students ORDER BY created_at DESC").fetchall()
        return [dict(r) for r in rows]


def delete_student(email):
    email = email.strip().lower()
    with get_conn() as conn:
        conn.execute("DELETE FROM students WHERE email = ?", (email,))
        conn.commit()


def qr_url_for(access_key, size=300):
    data = urllib.parse.quote(access_key)
    return f"https://api.qrserver.com/v1/create-qr-code/?size={size}x{size}&data={data}"


def export_backup_json():
    '''Full, restorable export of every field for every student -
    use this to back up the roster off of Streamlit's disk, since
    Streamlit Community Cloud wipes local files on every redeploy.'''
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM students ORDER BY created_at").fetchall()
        return json.dumps([dict(r) for r in rows], indent=2)


def restore_backup_json(json_text):
    '''Upserts every record from a JSON backup into the database.
    Existing students (matched by email) are overwritten with the
    backup's values; new students are inserted. Returns the number
    of records processed.'''
    records = json.loads(json_text)
    if not isinstance(records, list):
        raise ValueError("Backup file must contain a list of student records.")
    with get_conn() as conn:
        for rec in records:
            conn.execute('''
                INSERT INTO students (email, name, program_number, class_name, fee, status, access_key, created_at, paid_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(email) DO UPDATE SET
                    name=excluded.name,
                    program_number=excluded.program_number,
                    class_name=excluded.class_name,
                    fee=excluded.fee,
                    status=excluded.status,
                    access_key=excluded.access_key,
                    created_at=excluded.created_at,
                    paid_at=excluded.paid_at
            ''', (
                rec["email"].strip().lower(), rec["name"], rec.get("program_number"),
                rec.get("class_name"), rec.get("fee", 0), rec.get("status", "Pending"),
                rec["access_key"], rec.get("created_at"), rec.get("paid_at")
            ))
        conn.commit()
    return len(records)


init_db()

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

.bf-pill-paid {
    background: rgba(0, 230, 118, .18);
    border-color: rgba(0, 230, 118, .4);
    color: #00e676;
}

.bf-pill-pending {
    background: rgba(255, 170, 0, .18);
    border-color: rgba(255, 170, 0, .4);
    color: #ffaa00;
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

.bf-key-box {
    text-align: center;
    padding: 16px;
    border-radius: 18px;
    background: rgba(0, 0, 0, .35);
    border: 1px dashed rgba(255, 255, 255, .35);
    margin: 14px 0;
}

.bf-key {
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: .12em;
    color: #ffaa00;
    word-break: break-all;
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
        "Name": "", "Email": "", "Program Number": "", "Class": "", "Fee": 0.0,
        "Stripe Link": "", "Access Key": "", "Status": "Pending"
    }

if "login_error" not in st.session_state:
    st.session_state.login_error = ""


def navigate(to_state):
    st.session_state.app_state = to_state


def reset_user():
    st.session_state.current_user = {
        "Name": "", "Email": "", "Program Number": "", "Class": "", "Fee": 0.0,
        "Stripe Link": "", "Access Key": "", "Status": "Pending"
    }
    st.session_state.login_error = ""
    st.session_state.app_state = "home"


def load_user_from_record(record):
    st.session_state.current_user = {
        "Name": record["name"],
        "Email": record["email"],
        "Program Number": record["program_number"] or "",
        "Class": record["class_name"] or "",
        "Fee": record["fee"] or 0.0,
        "Stripe Link": next(
            (p["stripe_link"] for p in AVAILABLE_PROGRAMS if p["id"] == record["program_number"]),
            ""
        ),
        "Access Key": record["access_key"],
        "Status": record["status"],
    }


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

    col1, col2 = st.columns(2)
    with col1:
        st.button("Register & Enroll", use_container_width=True, type="primary", on_click=navigate, args=("register",))
    with col2:
        st.button("🔑 My QR Code / Login", use_container_width=True, on_click=navigate, args=("login",))

    st.write("")
    st.button("Admin Portal", use_container_width=True, on_click=navigate, args=("admin_login",))


elif st.session_state.app_state == "login":
    st.markdown(
        '<div class="bf-section-title"><h2>Returning Student Login</h2>'
        '<p class="bf-muted">Enter the email and access key you were given after registering to view your QR code and program.</p></div>',
        unsafe_allow_html=True
    )

    login_email = st.text_input("Email", placeholder="jane@example.com", key="login_email_input")
    login_key = st.text_input("Access Key", placeholder="XXXX-XXXX-XXXX", key="login_key_input")

    if st.session_state.login_error:
        st.error(st.session_state.login_error)

    st.write("")
    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", use_container_width=True, on_click=navigate, args=("home",))
    with col2:
        if st.button("Login", use_container_width=True, type="primary"):
            record = get_student_by_credentials(login_email, login_key)
            if record:
                load_user_from_record(record)
                st.session_state.login_error = ""
                navigate("success")
                st.rerun()
            else:
                st.session_state.login_error = "We couldn't find a match. Double-check your email and access key."
                st.rerun()


elif st.session_state.app_state == "register":
    st.markdown(
        '<div class="bf-section-title"><h2>Student Registration</h2>'
        '<p class="bf-muted">Enter your details to browse available programs.</p></div>',
        unsafe_allow_html=True
    )

    st.session_state.current_user["Name"] = st.text_input("Full Name", value=st.session_state.current_user.get("Name", ""), placeholder="Jane Doe")
    st.session_state.current_user["Email"] = st.text_input("Email", value=st.session_state.current_user.get("Email", ""), placeholder="jane@example.com")

    st.write("")

    valid = (st.session_state.current_user["Name"].strip() != "" and "@" in st.session_state.current_user["Email"] and "." in st.session_state.current_user["Email"])

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", use_container_width=True, on_click=navigate, args=("home",))
    with col2:
        if st.button("Continue", use_container_width=True, type="primary", disabled=not valid):
            access_key = register_student(
                st.session_state.current_user["Email"],
                st.session_state.current_user["Name"]
            )
            st.session_state.current_user["Access Key"] = access_key
            navigate("classes")
            st.rerun()


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
                    update_program(
                        st.session_state.current_user["Email"],
                        prog["id"], prog["name"], prog["fee"]
                    )
                    navigate("checkout")
                    st.rerun()

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

    st.markdown(f'''
    <div class="bf-summary">
        <div>
            <span class="bf-muted">Program</span>
            <strong>{selected_class}</strong>
        </div>
        <div>
            <span class="bf-muted">Student</span>
            <strong>{st.session_state.current_user.get("Name", "")}</strong>
        </div>
        <div>
            <span class="bf-muted">Amount Due</span>
            <strong class="bf-price">${selected_fee:,.2f}</strong>
        </div>
    </div>
    ''', unsafe_allow_html=True)

    st.markdown("### Legal Agreements")

    cb1 = st.checkbox("I agree to the Physical Activity & Liability Waiver")
    st.caption("I acknowledge that dance involves physical exertion and risk of injury. I assume all risks and release BollyFusion Academy from liability.")

    cb2 = st.checkbox("I agree to the Media & Photography Release")
    st.caption("I grant BollyFusion Academy permission to use photographs and video recordings of me for studio-related promotional purposes.")

    cb3 = st.checkbox("I agree to the Refund Policy")
    st.caption("A free refund is available after 2 weeks of program commencement. No refunds or prorations outside this window.")

    st.write("")

    can_pay = cb1 and cb2 and cb3

    if can_pay:
        st.link_button(
            f"💳 Pay ${selected_fee:,.2f} via Stripe",
            url=stripe_link,
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

    st.caption("After completing payment in the Stripe tab, come back here and confirm below.")

    if st.button("✅ I've Completed Payment", use_container_width=True, disabled=not can_pay):
        mark_status(st.session_state.current_user["Email"], "Paid")
        st.session_state.current_user["Status"] = "Paid"
        navigate("success")
        st.rerun()

    st.write("")
    st.button("Back", use_container_width=True, on_click=navigate, args=("classes",))


elif st.session_state.app_state == "success":
    record = get_student(st.session_state.current_user.get("Email", ""))
    if record:
        load_user_from_record(record)

    u_name = st.session_state.current_user.get("Name", "")
    u_class = st.session_state.current_user.get("Class", "")
    u_status = st.session_state.current_user.get("Status", "Pending")
    u_key = st.session_state.current_user.get("Access Key", "")

    st.markdown(
        '<div class="bf-section-title"><h2>Digital Studio ID</h2>'
        '<p class="bf-muted">Show this screen at check-in. If a QR scanner isn\'t handy, your instructor can compare the key below instead.</p></div>',
        unsafe_allow_html=True
    )

    status_class = "bf-pill-paid" if u_status == "Paid" else "bf-pill-pending"
    status_label = "✅ Payment Confirmed" if u_status == "Paid" else "⏳ Payment Pending"

    st.markdown(f'''
    <div class="bf-id">
        <div class="bf-pill {status_class}">{status_label}</div>
        <h2>{u_name}</h2>
        <p class="bf-muted">{u_class if u_class else "No program selected yet"}</p>
    </div>
    ''', unsafe_allow_html=True)

    if u_status == "Paid" and u_key:
        st.image(qr_url_for(u_key), use_container_width=True)
        st.markdown(f'''
        <div class="bf-key-box">
            <div class="bf-muted" style="font-size:12px; margin-bottom:6px;">VISUAL ACCESS KEY (backup if scanner unavailable)</div>
            <div class="bf-key">{format_key(u_key)}</div>
        </div>
        ''', unsafe_allow_html=True)
        st.caption("Save your email and access key — you'll use them to log in and view this ID again anytime.")
    elif u_status == "Pending" and u_class:
        st.warning("Your program is selected but payment hasn't been confirmed yet.")
        if st.button("Resume Checkout", use_container_width=True, type="primary"):
            navigate("checkout")
            st.rerun()
    else:
        st.info("No enrollment found yet. Register and choose a program to get your Digital Studio ID.")

    st.write("")
    st.button("Done (Back to Home)", use_container_width=True, type="primary", on_click=reset_user)


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
            if a_user == "admin" and a_pass == "admin123":
                navigate("admin_dashboard")
            else:
                st.error("Invalid credentials. Use admin / admin123.")


elif st.session_state.app_state == "admin_dashboard":
    st.markdown(
        '<div class="bf-section-title"><h2>📊 Admin Portal</h2>'
        '<p class="bf-muted">Full enrollment roster, payment status, and check-in QR codes.</p></div>',
        unsafe_allow_html=True
    )

    all_students = get_all_students()

    if all_students:
        df = pd.DataFrame(all_students)
        df["Access Key"] = df["access_key"].apply(format_key)
        df["QR"] = df["access_key"].apply(lambda k: qr_url_for(k, size=120) if k else "")
        df_display = df.rename(columns={
            "name": "Name", "email": "Email", "program_number": "Program #",
            "class_name": "Class", "fee": "Fee", "status": "Status"
        })[["Name", "Email", "Program #", "Class", "Fee", "Status", "Access Key", "QR"]]

        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True,
            column_config={
                "QR": st.column_config.ImageColumn("QR Code"),
                "Fee": st.column_config.NumberColumn("Fee", format="$%.2f"),
            }
        )

        csv = df_display.drop(columns=["QR"]).to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", data=csv, file_name="bollyfusion-registrations.csv", mime="text/csv", key="download_roster_csv")

        st.divider()
        st.markdown("### Manage a Student")
        st.caption("Manually confirm cash payments, correct a status, or remove a record. Compare the Access Key here against the student's phone if you can't scan their QR.")

        emails = [s["email"] for s in all_students]
        labels = [f'{s["name"]} <{s["email"]}> — {s["status"]}' for s in all_students]
        pick = st.selectbox("Student", options=range(len(emails)), format_func=lambda i: labels[i])
        picked_email = emails[pick]
        picked_record = next(s for s in all_students if s["email"] == picked_email)

        st.markdown(f'''
        <div class="bf-key-box">
            <div class="bf-muted" style="font-size:12px; margin-bottom:6px;">ACCESS KEY FOR {picked_record["name"]}</div>
            <div class="bf-key">{format_key(picked_record["access_key"])}</div>
        </div>
        ''', unsafe_allow_html=True)

        mcol1, mcol2, mcol3 = st.columns(3)
        with mcol1:
            if st.button("✅ Mark Paid", use_container_width=True, type="primary"):
                mark_status(picked_email, "Paid")
                st.rerun()
        with mcol2:
            if st.button("⏳ Mark Pending", use_container_width=True):
                mark_status(picked_email, "Pending")
                st.rerun()
        with mcol3:
            if st.button("🗑️ Delete Record", use_container_width=True):
                delete_student(picked_email)
                st.rerun()
    else:
        st.info("No students have registered yet.")

    st.divider()
    st.markdown("### 💾 Backup & Restore")
    st.caption(
        "Streamlit Community Cloud wipes local files on every redeploy, so this database "
        "does not survive one on its own. Download a backup regularly, then restore it here "
        "right after any redeploy to bring every student, payment status, and access key back."
    )

    bcol1, bcol2 = st.columns(2)
    with bcol1:
        if all_students:
            backup_json = export_backup_json()
            st.download_button(
                "⬇️ Download Full Backup (JSON)",
                data=backup_json,
                file_name=f"bollyfusion-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
                key="download_backup_json"
            )
        else:
            st.button("⬇️ Download Full Backup (JSON)", use_container_width=True, disabled=True)
    with bcol2:
        if DB_PATH.exists():
            st.download_button(
                "⬇️ Download Raw Database File",
                data=DB_PATH.read_bytes(),
                file_name="bollyfusion_students.db",
                mime="application/octet-stream",
                use_container_width=True,
                key="download_raw_db"
            )
        else:
            st.button("⬇️ Download Raw Database File", use_container_width=True, disabled=True)

    st.write("")
    restore_file = st.file_uploader("Restore from a JSON backup", type=["json"], key="restore_upload")
    if restore_file is not None:
        if st.button("Restore Backup Now", type="primary", use_container_width=True):
            try:
                count = restore_backup_json(restore_file.read().decode("utf-8"))
                st.success(f"Restored {count} student record(s).")
                st.rerun()
            except Exception as e:
                st.error(f"Restore failed: {e}")

    st.write("")
    st.button("Logout", use_container_width=True, on_click=navigate, args=("home",))
