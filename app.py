import streamlit as st
import json
import urllib.parse
import pandas as pd

st.set_page_config(page_title="BollyFusion Academy", layout="centered", initial_sidebar_state="collapsed")

# --- INITIAL DATA INJECTED FROM ADMIN DASHBOARD ---
AVAILABLE_PROGRAMS = [
    {
        "name": "Bolly Cardio 1",
        "prog_num": "1",
        "hours": 0.5,
        "weeks": 20,
        "fee": 250.0,
        "poster": "https://images.unsplash.com/photo-1548690312-e3b507d8c110?auto=format&fit=crop&w=800&q=80",
        "desc": "High-energy entry-level fitness infused with cinematic Bollywood flair.",
        "song_count": "4-5"
    },
    {
        "name": "Bolly Cardio II",
        "prog_num": "2",
        "hours": 1.0,
        "weeks": 20,
        "fee": 500.0,
        "poster": "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80",
        "desc": "Level up your stamina with complex beats and faster choreography.",
        "song_count": "4-5"
    },
    {
        "name": "Couples to Event",
        "prog_num": "3",
        "hours": 1.0,
        "weeks": 10,
        "fee": 1500.0,
        "poster": "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80",
        "desc": "Perfect for weddings! Master partner choreography with elegance and grace.",
        "song_count": "2-3"
    },
    {
        "name": "Group to Events",
        "prog_num": "4",
        "hours": 1.0,
        "weeks": 10,
        "fee": 1000.0,
        "poster": "https://images.unsplash.com/photo-1532766324881-8b211bb1f2fc?auto=format&fit=crop&w=800&q=80",
        "desc": "Coordinate stunning group routines for your next big celebration.",
        "song_count": "2-3"
    }
]

# --- SESSION STATE MANAGEMENT ---
if 'app_state' not in st.session_state:
    st.session_state.app_state = 'home'
if 'current_user' not in st.session_state:
    st.session_state.current_user = {"Name": "", "Email": "", "Program #": "", "Class": "", "Fee": 0}
if 'student_db' not in st.session_state:
    st.session_state.student_db = []

def navigate(to_state):
    st.session_state.app_state = to_state

# --- 1. HOME SCREEN ---
if st.session_state.app_state == 'home':
    st.image("https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    st.markdown("<h1 style='text-align: center; color: #fbbf24; font-size: 3em;'>BollyFusion Academy</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; letter-spacing: 2px; font-weight: bold;'>CINEMATIC DANCE EXPERIENCE</p>", unsafe_allow_html=True)
    st.divider()
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.button("Register & Enroll ➔", use_container_width=True, type="primary", on_click=navigate, args=('register',))
        st.button("Admin Portal", use_container_width=True, on_click=navigate, args=('admin_login',))

# --- 2. REGISTRATION SCREEN ---
elif st.session_state.app_state == 'register':
    st.title("Student Registration")
    st.markdown("Please enter your details to browse available programs.")
    
    st.session_state.current_user["Name"] = st.text_input("Full Name", value=st.session_state.current_user.get("Name", ""), placeholder="Jane Doe")
    st.session_state.current_user["Email"] = st.text_input("Email", value=st.session_state.current_user.get("Email", ""), placeholder="jane@example.com")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", use_container_width=True, on_click=navigate, args=('home',))
    with col2:
        if st.session_state.current_user["Name"] and st.session_state.current_user["Email"]:
            st.button("Next ➔", use_container_width=True, type="primary", on_click=navigate, args=('classes',))
        else:
            st.button("Next ➔", use_container_width=True, disabled=True)

# --- 3. CLASS SELECTION SCREEN (2 COLUMN SCROLL GRID) ---
elif st.session_state.app_state == 'classes':
    st.title("Choose a Program")
    st.markdown("Browse our offerings. **Tap the select button right under the image** to enroll.")
    
    st.markdown("""
    <style>
    .program-card { border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 20px; background: white; }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container(height=650, border=False):
        cols = st.columns(2)
        for idx, prog in enumerate(AVAILABLE_PROGRAMS):
            with cols[idx % 2]:
                # NOTE: Indentation removed inside HTML string to prevent Streamlit Markdown escaping
                st.markdown(f"""
<div class='program-card'>
<div style='position: relative; cursor: pointer;'>
<img src='{prog["poster"]}' style='width:100%; border-radius:8px;'>
<div style='position:absolute; top:50%; left:50%; transform: translate(-50%, -50%); background:rgba(255,255,255,0.9); border-radius:50%; width:50px; height:50px; display:flex; justify-content:center; align-items:center; box-shadow:0 4px 15px rgba(0,0,0,0.6); font-size:24px; border: 2px solid #fbbf24;'>👆</div>
</div>
<h4 style='margin-top:10px; margin-bottom:5px; font-size: 16px;'>{prog['name']}</h4>
<p style='font-size: 12px; color: gray; margin-bottom: 5px;'>{prog['weeks']} Weeks | {prog['hours']} hrs/wk</p>
<p style='font-size: 12px; margin-bottom: 10px;'>{prog['desc']}</p>
<p style='font-size: 14px; font-weight: bold; color: #10b981;'>${prog['fee']:,.2f}</p>
</div>
""", unsafe_allow_html=True)
                
                if st.button(f"👆 Tap to Select {prog['name']}", key=f"enroll_{prog['prog_num']}", use_container_width=True, type="primary"):
                    st.session_state.current_user["Class"] = prog["name"]
                    st.session_state.current_user["Program #"] = prog["prog_num"]
                    st.session_state.current_user["Fee"] = prog["fee"]
                    navigate('checkout')
                
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("Back", on_click=navigate, args=('register',))

# --- 4. SECURE CHECKOUT SCREEN (LEGAL WAIVERS) ---
elif st.session_state.app_state == 'checkout':
    st.title("Secure Checkout")
    c_class = st.session_state.current_user["Class"]
    c_fee = st.session_state.current_user["Fee"]
    
    st.info(f"**Selected Program:** {c_class}\n\n**Amount Due:** ${c_fee:,.2f}")
    
    st.markdown("### Legal Agreements")
    st.markdown("Please review and accept all terms below to proceed with payment.")
    
    waiver_text = "I hereby acknowledge that dance involves physical exertion and risk of injury. I expressly assume all risks associated with participating in BollyFusion Academy programs. I release the studio, its instructors, and affiliates from any and all liability, claims, or demands arising from injury or harm."
    media_text = "I grant BollyFusion Academy the irrevocable right and permission to use photographs and/or video recordings of me on studio and other websites and in publications, promotional flyers, educational materials, derivative works, or for any other similar purpose without compensation."
    refund_text = "I understand and agree to the studio's refund policy: A free refund is given after 2 weeks of the program commencement. No refunds or prorations will be provided outside of this designated window."
    
    cb1 = st.checkbox("I agree to the Physical Activity & Liability Waiver", help=waiver_text)
    st.caption(waiver_text)
    
    cb2 = st.checkbox("I agree to the Media & Photography Release", help=media_text)
    st.caption(media_text)
    
    cb3 = st.checkbox("I agree to the Refund Policy", help=refund_text)
    st.caption(refund_text)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Back", use_container_width=True, on_click=navigate, args=('classes',))
    with col2:
        if cb1 and cb2 and cb3:
            def process_payment():
                st.session_state.student_db.append({
                    "Name": st.session_state.current_user["Name"],
                    "Email": st.session_state.current_user["Email"],
                    "Program #": st.session_state.current_user["Program #"],
                    "Class": st.session_state.current_user["Class"],
                    "Status": "Paid"
                })
                navigate('success')
                
            st.button(" Pay", use_container_width=True, type="primary", on_click=process_payment)
        else:
            st.button(" Pay (Accept all terms to enable)", use_container_width=True, disabled=True)

# --- 5. DIGITAL ID SCREEN ---
elif st.session_state.app_state == 'success':
    st.success("Payment Successful! Welcome to the Academy.")
    st.markdown("Please save this digital Studio ID for check-in at the front desk.")
    
    u_name = st.session_state.current_user["Name"]
    u_class = st.session_state.current_user["Class"]
    
    qr_data = urllib.parse.quote(f"Student:{u_name}|Class:{u_class}")
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={qr_data}"
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(qr_url, use_container_width=True)
        st.markdown(f"<h3 style='text-align: center;'>{u_name}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: gray;'>{u_class}</p>", unsafe_allow_html=True)
    
    def reset():
        st.session_state.current_user = {"Name": "", "Email": "", "Program #": "", "Class": "", "Fee": 0}
        navigate('home')
        
    st.divider()
    st.button("Done (Back to Home)", type="primary", use_container_width=True, on_click=reset)

# --- 6. ADMIN LOGIN SCREEN ---
elif st.session_state.app_state == 'admin_login':
    st.title("🔒 Admin Login")
    st.markdown("Hardcoded secure portal access.")
    
    a_user = st.text_input("Username")
    a_pass = st.text_input("Password", type="password")
    
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.button("Cancel", use_container_width=True, on_click=navigate, args=('home',))
    with col2:
        if st.button("Login Securely", use_container_width=True, type="primary"):
            if a_user == "admin" and a_pass == "admin123":
                navigate('admin_dashboard')
            else:
                st.error("Invalid credentials. Please use admin / admin123")

# --- 7. ADMIN DASHBOARD ---
elif st.session_state.app_state == 'admin_dashboard':
    st.title("📊 Admin Portal")
    st.markdown("Live Student Registration Roster:")
    
    if len(st.session_state.student_db) > 0:
        df_students = pd.DataFrame(st.session_state.student_db)
        df_students = df_students[['Name', 'Email', 'Program #', 'Class', 'Status']]
        st.dataframe(df_students, use_container_width=True, hide_index=True)
    else:
        st.info("No students have registered yet during this session.")
        
    st.divider()
    st.button("Logout", use_container_width=True, on_click=navigate, args=('home',))
