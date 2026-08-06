import streamlit as st
import urllib.parse
import pandas as pd
import re

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
        "Name": "", "Email": "", "Program Number": "", "Class": "", "Fee": 0.0, "Stripe Link": ""
    }

if "student_db" not in st.session_state:
    st.session_state.student_db = []


def navigate(to_state):
    st.session_state.app_state = to_state

def reset_user():
    st.session_state.current_user = {
        "Name": "", "Email": "", "Program Number": "", "Class": "", "Fee": 0.0, "Stripe Link": ""
    }
    st.session_state.app_state = "home"


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
        st.button("Admin Portal", use_container_width=True, on_click=navigate, args=("admin_login",))


elif st.session_state.app_state == "register":
    st.markdown(
        '<div class="bf-section-title"><h2>Student Registration</h2>'
        '<p class="bf-muted">Enter your details to browse available programs.</p></div>',
        unsafe_allow_html=True
    )

    st.session_state.current_user["Name"] = st.text_input("Full Name", value=st.session_state.current_user.get("Name", ""), placeholder="Jane Doe")
    st.session_state.current_user["Email"] = st.text_input("Email", value=st.session_state.current_user.get("Email", ""), placeholder="jane@example.com")

    st.write("")

    # --- NEW REGEX EMAIL VALIDATION ---
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    is_valid_email = bool(re.match(email_pattern, st.session_state.current_user["Email"]))
    
    valid = (st.session_state.current_user["Name"].strip() != "" and is_valid_email)
    # ----------------------------------

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", use_container_width=True, on_click=navigate, args=("home",))
    with col2:
        st.button("Continue", use_container_width=True, type="primary", disabled=not valid, on_click=navigate, args=("classes",))


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
                    
                    # --- NEW LOGGING LOGIC ---
                    # Logs the user to the admin database regardless of payment completion
                    st.session_state.student_db.append({
                        "Name": st.session_state.current_user.get("Name", "Unknown"),
                        "Email": st.session_state.current_user.get("Email", "Unknown"),
                        "Program Number": prog["id"],
                        "Class": prog["name"],
                        "Status": "Pending Payment"
                    })
                    # -------------------------

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

    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", use_container_width=True, on_click=navigate, args=("classes",))

    with col2:
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


elif st.session_state.app_state == "success":
    st.markdown(
        '<div class="bf-section-title"><h2>Digital Studio ID</h2>'
        '<p class="bf-muted">Save this QR code for front-desk check-in.</p></div>',
        unsafe_allow_html=True
    )

    u_name = st.session_state.current_user.get("Name", "")
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
                st.error("Invalid credentials. Use admin / admin123.")


elif st.session_state.app_state == "admin_dashboard":
    st.markdown(
        '<div class="bf-section-title"><h2>📊 Admin Portal</h2>'
        '<p class="bf-muted">Live registration roster for this session.</p></div>',
        unsafe_allow_html=True
    )

    if st.session_state.student_db:
        df = pd.DataFrame(st.session_state.student_db)
        df = df[["Name", "Email", "Program Number", "Class", "Status"]]
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button("Download CSV", data=csv, file_name="bollyfusion-registrations.csv", mime="text/csv", key="download_roster_csv")
    else:
        st.info("No students have registered yet during this session.")

    st.write("")
    st.button("Logout", use_container_width=True, on_click=navigate, args=("home",))
