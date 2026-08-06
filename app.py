import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import plotly.graph_objects as go
import plotly.express as px
import datetime
import json

# --- Configuration ---
st.set_page_config(page_title="BollyFusion Academy Dashboard", layout="wide")

st.title("BollyFusion Academy Financial Dashboard")
st.markdown("This model projects annual revenue, calculates Cost of Goods Sold (COGS), and generates an automated class timetable. **Toggle the 'Offer this program?' checkbox in each level to dynamically generate the public-facing student app code.**")

# --- Sidebar Inputs ---
st.sidebar.header("1. Studio Logistics")
hourly_rate = st.sidebar.number_input("Studio Rental Cost ($/hr)", min_value=0.0, value=20.0, step=5.0)
max_class_size = st.sidebar.number_input("Max Students per Class", min_value=5, value=20, step=1)

st.sidebar.divider()

st.sidebar.header("2. Program Enrollment & Economics")
st.sidebar.markdown("Specify students, program fees, duration, and event metrics per level.")

# Category 1
with st.sidebar.expander("**Category 1 (Bolly Cardio 1)**", expanded=False):
    offered_1 = st.checkbox("Offer this program?", value=True, key="off1")
    name_1 = st.text_input("Category Name", value="Bolly Cardio 1", key='n1')
    hrs_1 = st.number_input("Hours/Week", min_value=0.0, value=0.5, step=0.5, key='h1')
    weeks_1 = st.number_input("Program Weeks", min_value=1, value=20, step=1, key='wk1')
    st_sparks = st.number_input("Students", min_value=0, value=80, step=1, key='s1')
    term_sparks = st.number_input("Program Fee ($)", min_value=0.0, value=250.0, step=50.0, key='t1')
    ev_sparks = st.number_input("Events/Yr", min_value=0, value=0, step=1, key='e1')
    fee_sparks = st.number_input("Event Fee Charged/Student ($)", min_value=0.0, value=85.0, step=5.0, key='f1')
    vcogs_sparks = st.number_input("Event Cost/Student ($)", min_value=0.0, value=40.0, step=5.0, key='vc1')
    fcogs_sparks = st.number_input("Fixed Cost/Event ($)", min_value=0.0, value=250.0, step=50.0, key='fc1')

# Category 2
with st.sidebar.expander("**Category 2 (Bolly Cardio II)**", expanded=False):
    offered_2 = st.checkbox("Offer this program?", value=True, key="off2")
    name_2 = st.text_input("Category Name", value="Bolly Cardio II", key='n2')
    hrs_2 = st.number_input("Hours/Week", min_value=0.0, value=1.0, step=0.5, key='h2')
    weeks_2 = st.number_input("Program Weeks", min_value=1, value=20, step=1, key='wk2')
    st_roots = st.number_input("Students", min_value=0, value=50, step=1, key='s2')
    term_roots = st.number_input("Program Fee ($)", min_value=0.0, value=500.0, step=50.0, key='t2')
    ev_roots = st.number_input("Events/Yr", min_value=0, value=0, step=1, key='e2')
    fee_roots = st.number_input("Event Fee Charged/Student ($)", min_value=0.0, value=85.0, step=5.0, key='f2')
    vcogs_roots = st.number_input("Event Cost/Student ($)", min_value=0.0, value=40.0, step=5.0, key='vc2')
    fcogs_roots = st.number_input("Fixed Cost/Event ($)", min_value=0.0, value=250.0, step=50.0, key='fc2')

# Category 3
with st.sidebar.expander("**Category 3 (Couples to Event)**", expanded=False):
    offered_3 = st.checkbox("Offer this program?", value=True, key="off3")
    name_3 = st.text_input("Category Name", value="Couples to Event", key='n3')
    hrs_3 = st.number_input("Hours/Week", min_value=0.0, value=1.0, step=0.5, key='h3')
    weeks_3 = st.number_input("Program Weeks", min_value=1, value=10, step=1, key='wk3')
    st_stars = st.number_input("Students", min_value=0, value=4, step=1, key='s3')
    term_stars = st.number_input("Program Fee ($)", min_value=0.0, value=1500.0, step=50.0, key='t3')
    ev_stars = st.number_input("Events/Yr", min_value=0, value=0, step=1, key='e3')
    fee_stars = st.number_input("Event Fee Charged/Student ($)", min_value=0.0, value=100.0, step=5.0, key='f3')
    vcogs_stars = st.number_input("Event Cost/Student ($)", min_value=0.0, value=50.0, step=5.0, key='vc3')
    fcogs_stars = st.number_input("Fixed Cost/Event ($)", min_value=0.0, value=300.0, step=50.0, key='fc3')

# Category 4
with st.sidebar.expander("**Category 4 (Group to Events)**", expanded=False):
    offered_4 = st.checkbox("Offer this program?", value=True, key="off4")
    name_4 = st.text_input("Category Name", value="Group to Events", key='n4')
    hrs_4 = st.number_input("Hours/Week", min_value=0.0, value=1.0, step=0.5, key='h4')
    weeks_4 = st.number_input("Program Weeks", min_value=1, value=10, step=1, key='wk4')
    st_beats = st.number_input("Students", min_value=0, value=4, step=1, key='s4')
    term_beats = st.number_input("Program Fee ($)", min_value=0.0, value=1000.0, step=50.0, key='t4')
    ev_beats = st.number_input("Events/Yr", min_value=0, value=0, step=1, key='e4')
    fee_beats = st.number_input("Event Fee Charged/Student ($)", min_value=0.0, value=50.0, step=5.0, key='f4')
    vcogs_beats = st.number_input("Event Cost/Student ($)", min_value=0.0, value=20.0, step=5.0, key='vc4')
    fcogs_beats = st.number_input("Fixed Cost/Event ($)", min_value=0.0, value=150.0, step=50.0, key='fc4')

# Category 5
with st.sidebar.expander("**Category 5 (Elite Fusion Troupe)**", expanded=False):
    offered_5 = st.checkbox("Offer this program?", value=True, key="off5")
    name_5 = st.text_input("Category Name", value="Elite Fusion Troupe", key='n5')
    hrs_5 = st.number_input("Hours/Week", min_value=0.0, value=11.0, step=0.5, key='h5')
    weeks_5 = st.number_input("Program Weeks", min_value=1, value=20, step=1, key='wk5')
    st_elite = st.number_input("Students", min_value=0, value=0, step=1, key='s5')
    term_elite = st.number_input("Program Fee ($)", min_value=0.0, value=2500.0, step=50.0, key='t5')
    ev_elite = st.number_input("Events/Yr", min_value=0, value=0, step=1, key='e5')
    fee_elite = st.number_input("Event Fee Charged/Student ($)", min_value=0.0, value=150.0, step=5.0, key='f5')
    vcogs_elite = st.number_input("Event Cost/Student ($)", min_value=0.0, value=75.0, step=5.0, key='vc5')
    fcogs_elite = st.number_input("Fixed Cost/Event ($)", min_value=0.0, value=500.0, step=50.0, key='fc5')

# Category 6
with st.sidebar.expander("**Category 6 (Premier Company)**", expanded=False):
    offered_6 = st.checkbox("Offer this program?", value=True, key="off6")
    name_6 = st.text_input("Category Name", value="Premier Company", key='n6')
    hrs_6 = st.number_input("Hours/Week", min_value=0.0, value=13.0, step=0.5, key='h6')
    weeks_6 = st.number_input("Program Weeks", min_value=1, value=20, step=1, key='wk6')
    st_premier = st.number_input("Students", min_value=0, value=0, step=1, key='s6')
    term_premier = st.number_input("Program Fee ($)", min_value=0.0, value=3000.0, step=50.0, key='t6')
    ev_premier = st.number_input("Events/Yr", min_value=0, value=0, step=1, key='e6')
    fee_premier = st.number_input("Event Fee Charged/Student ($)", min_value=0.0, value=150.0, step=5.0, key='f6')
    vcogs_premier = st.number_input("Event Cost/Student ($)", min_value=0.0, value=75.0, step=5.0, key='vc6')
    fcogs_premier = st.number_input("Fixed Cost/Event ($)", min_value=0.0, value=500.0, step=50.0, key='fc6')

st.sidebar.divider()

# --- Insurance Costs ---
st.sidebar.header("3. Insurance Costs")
st.sidebar.markdown("Set liability/insurance costs per student and per studio hour.")
ins_per_student = st.sidebar.number_input("Cost per Student ($/yr)", min_value=0.0, value=15.0, step=5.0)
ins_per_hour = st.sidebar.number_input("Cost per Studio Hour ($/hr)", min_value=0.0, value=1.0, step=0.5)

st.sidebar.divider()

# --- Music Rights Costs ---
st.sidebar.header("4. Music Licensing & Rights")
st.sidebar.markdown("Set music performance rights costs per studio teaching hour.")
music_per_hour = st.sidebar.number_input("Music Rights Cost ($/hr)", min_value=0.0, value=0.50, step=0.10)

# --- Data Logic ---
programs = [name_1, name_2, name_3, name_4, name_5, name_6]
program_weeks = [weeks_1, weeks_2, weeks_3, weeks_4, weeks_5, weeks_6]
base_weekly_hours = [hrs_1, hrs_2, hrs_3, hrs_4, hrs_5, hrs_6]

students = [
    st_sparks if offered_1 else 0, 
    st_roots if offered_2 else 0, 
    st_stars if offered_3 else 0, 
    st_beats if offered_4 else 0, 
    st_elite if offered_5 else 0, 
    st_premier if offered_6 else 0
]

term_fees = [term_sparks, term_roots, term_stars, term_beats, term_elite, term_premier]
events = [ev_sparks, ev_roots, ev_stars, ev_beats, ev_elite, ev_premier]
event_fees = [fee_sparks, fee_roots, fee_stars, fee_beats, fee_elite, fee_premier]
event_v_cogs = [vcogs_sparks, vcogs_roots, vcogs_stars, vcogs_beats, vcogs_elite, vcogs_premier]
event_f_cogs = [fcogs_sparks, fcogs_roots, fcogs_stars, fcogs_beats, fcogs_elite, fcogs_premier]

posters = [
    "https://images.unsplash.com/photo-1548690312-e3b507d8c110?auto=format&fit=crop&w=800&q=80", 
    "https://images.unsplash.com/photo-1518611012118-696072aa579a?auto=format&fit=crop&w=800&q=80", 
    "https://images.unsplash.com/photo-1519741497674-611481863552?auto=format&fit=crop&w=800&q=80", 
    "https://images.unsplash.com/photo-1532766324881-8b211bb1f2fc?auto=format&fit=crop&w=800&q=80", 
    "https://images.unsplash.com/photo-1547153760-18fc86324498?auto=format&fit=crop&w=800&q=80", 
    "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&w=800&q=80"  
]

descriptions = [
    "High-energy entry-level fitness infused with cinematic Bollywood flair.",
    "Level up your stamina with complex beats and faster choreography.",
    "Perfect for weddings! Master partner choreography with elegance and grace.",
    "Coordinate stunning group routines for your next big celebration.",
    "Advanced fusion techniques for aspiring competitive performers.",
    "Our flagship professional company. Stage-ready cinematic perfection."
]

offered_flags = [offered_1, offered_2, offered_3, offered_4, offered_5, offered_6]
generated_programs = []

for i in range(len(programs)):
    if offered_flags[i]:
        generated_programs.append({
            "name": programs[i],
            "prog_num": str(i + 1),
            "hours": base_weekly_hours[i],
            "weeks": program_weeks[i],
            "fee": term_fees[i],
            "poster": posters[i],
            "desc": descriptions[i],
            "song_count": "4-5" if program_weeks[i] >= 20 else "2-3"
        })

# --- Financial Calculations ---
sections_needed = [math.ceil(s / max_class_size) if s > 0 else 0 for s in students]
annual_hours = [sec * hrs * 52 for sec, hrs in zip(sections_needed, base_weekly_hours)]
tuition_revenue = [s * rate * (52 / wks) if wks > 0 else 0 for s, rate, wks in zip(students, term_fees, program_weeks)]
event_revenue = [s * e * fee for s, e, fee in zip(students, events, event_fees)]
total_gross_revenue = [t + e for t, e in zip(tuition_revenue, event_revenue)]
cogs_studio = [hours * hourly_rate for hours in annual_hours]
cogs_events = [(s * e * v_cogs) + (e * f_cogs if s > 0 else 0) for s, e, v_cogs, f_cogs in zip(students, events, event_v_cogs, event_f_cogs)]
cogs_insurance = [(s * ins_per_student) + (hours * ins_per_hour) for s, hours in zip(students, annual_hours)]
cogs_music = [hours * music_per_hour for hours in annual_hours]
total_cogs = [s_cogs + e_cogs + i_cogs + m_cogs for s_cogs, e_cogs, i_cogs, m_cogs in zip(cogs_studio, cogs_events, cogs_insurance, cogs_music)]
gross_profit = [rev - cost for rev, cost in zip(total_gross_revenue, total_cogs)]

g_students = sum(students)
g_revenue = sum(total_gross_revenue)
g_cogs = sum(total_cogs)
g_profit = sum(gross_profit)

df = pd.DataFrame({
    "Program Level": programs,
    "Offered": ["Yes" if flag else "No" for flag in offered_flags],
    "Enrolled": students,
    "Hours/Week": base_weekly_hours,
    "Program Weeks": program_weeks,
    "Cycles/Year": [f"{52/wks:.1f}" if wks > 0 else "0.0" for wks in program_weeks],
    "Fee per Cycle": [f"${fee:,.2f}" for fee in term_fees],
    "Gross Revenue": [f"${rev:,.2f}" for rev in total_gross_revenue],
    "Studio COGS": [f"${cost:,.2f}" for cost in cogs_studio],
    "Event COGS": [f"${cost:,.2f}" for cost in cogs_events],
    "Total COGS": [f"${cost:,.2f}" for cost in total_cogs],
    "Gross Profit": [f"${profit:,.2f}" for profit in gross_profit]
})

# --- Dashboard Layout ---
col_met1, col_met2, col_met3, col_met4 = st.columns(4)
col_met1.metric(label="Total Enrolled", value=g_students)
col_met2.metric(label="Total Gross Revenue", value=f"${g_revenue:,.0f}")
col_met3.metric(label="Total COGS", value=f"${g_cogs:,.0f}")
col_met4.metric(label="Total Gross Profit", value=f"${g_profit:,.0f}", delta=f"{(g_profit/g_revenue)*100:.1f}% Margin" if g_revenue > 0 else "0%")

st.divider()

if g_students > 0:
    col1, col2 = st.columns([1, 1.5])
    with col1:
        st.subheader("Revenue Breakdown (COGS vs. Profit)")
        labels = ["Total Gross Revenue"]
        parents = [""]
        values = [sum(total_gross_revenue)]
        node_colors = ["#e2e8f0"]
        for i, p in enumerate(programs):
            rev = total_gross_revenue[i]
            prof = gross_profit[i]
            c_total = total_cogs[i]
            if rev > 0:
                labels.append(p)
                parents.append("Total Gross Revenue")
                values.append(rev)
                node_colors.append("#3b82f6")
                v_prof = prof if prof > 0 else 0
                v_cogs = rev - v_prof
                if v_prof > 0:
                    labels.append(f"Profit<br>({p})")
                    parents.append(p)
                    values.append(v_prof)
                    node_colors.append("#00e676")
                if v_cogs > 0:
                    cogs_label = f"COGS<br>({p})"
                    labels.append(cogs_label)
                    parents.append(p)
                    values.append(v_cogs)
                    node_colors.append("#ff0000")
        if sum(total_gross_revenue) > 0:
            fig1 = go.Figure(go.Sunburst(
                labels=labels, parents=parents, values=values,
                branchvalues="total", texttemplate="%{label}<br>$%{value:,.0f}", 
                marker=dict(colors=node_colors)
            ))
            fig1.update_layout(margin=dict(t=10, l=0, r=0, b=0))
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Revenue vs. COGS vs. Gross Profit")
        fig2, ax2 = plt.subplots(figsize=(10, 6))
        x = np.arange(len(programs))
        width = 0.25
        ax2.bar(x - width, total_gross_revenue, width, label='Total Gross Revenue', color='#2ca02c', edgecolor='black')
        ax2.bar(x, total_cogs, width, label='Total COGS', color='#d62728', edgecolor='black')
        ax2.bar(x + width, gross_profit, width, label='Gross Profit', color='#1f77b4', edgecolor='black')
        ax2.set_ylabel('USD ($)')
        ax2.set_xticks(x)
        chart_labels = [p.replace(" ", "\n") for p in programs]
        ax2.set_xticklabels(chart_labels, rotation=0, fontsize=9)
        ax2.legend()
        plt.tight_layout()
        st.pyplot(fig2)

st.divider()

# --- Data Table ---
st.subheader("Detailed Financial Breakdown by Program Level")
st.dataframe(df, use_container_width=True)

st.divider()

# --- Tabs: Timetable, Roadmap, Website Generator ---
tab1, tab2, tab3 = st.tabs(["Staggered Weekly Class Timetable", "60-Week High-Level Roadmap", "💻 Generate Student Site Code"])

with tab1:
    st.markdown("Auto-scheduler distributing classes across the week based on capacity logic. (Only generates slots for programs with > 0 enrolled students).")
    daily_capacity = {d: {'start': 16.0, 'end': 21.0, 'current': 16.0} for d in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']}
    daily_capacity.update({d: {'start': 9.0, 'end': 15.0, 'current': 9.0} for d in ['Saturday', 'Sunday']})
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dummy_date = datetime.date(2026, 1, 1)
    
    def float_to_time(h):
        hours, minutes = int(h), int(round((h - int(h)) * 60))
        if minutes == 60: hours, minutes = hours + 1, 0
        return datetime.time(hours, minutes)

    schedule_data = []
    for i, program in enumerate(programs):
        if students[i] > 0 and offered_flags[i]:
            for sec in range(sections_needed[i]):
                hours_to_schedule = base_weekly_hours[i]
                target_days = ['Saturday'] if i==0 else ['Sunday'] if i==1 else ['Monday', 'Wednesday', 'Friday', 'Tuesday', 'Thursday'] if i==2 else days_of_week
                max_chunk = 1.0 if i in [0,2] else 1.5 if i==1 else 2.5
                
                for day in target_days:
                    if hours_to_schedule <= 0: break
                    available_hours = daily_capacity[day]['end'] - daily_capacity[day]['current']
                    if available_hours > 0:
                        chunk = min(hours_to_schedule, available_hours, max_chunk)
                        start_time = float_to_time(daily_capacity[day]['current'])
                        end_time = float_to_time(daily_capacity[day]['current'] + chunk)
                        schedule_data.append({
                            "Program": program, "Section": f"Sec {sec+1}", "Day": day,
                            "Start Time": datetime.datetime.combine(dummy_date, start_time),
                            "End Time": datetime.datetime.combine(dummy_date, end_time),
                            "Display": f"{program} ({chunk}h)"
                        })
                        daily_capacity[day]['current'] += chunk
                        hours_to_schedule -= chunk

    if schedule_data:
        df_week = pd.DataFrame(schedule_data)
        base_colors = ['#ff4b4b', '#ffa421', '#ffc533', '#00d4b2', '#00a3e0', '#b9529f']
        level_colors = {programs[idx]: base_colors[idx] for idx in range(len(programs))}
        fig_week = px.timeline(
            df_week, x_start="Start Time", x_end="End Time", y="Day", color="Program",
            color_discrete_map=level_colors, text="Display", title="Weekly Studio Allocation"
        )
        fig_week.update_yaxes(categoryorder='array', categoryarray=days_of_week[::-1])
        fig_week.update_layout(xaxis=dict(tickformat="%I:%M %p", title="Time of Day"))
        st.plotly_chart(fig_week, use_container_width=True)
    else:
        st.info("No schedule generated. Add students to offered programs.")

with tab2:
    st.markdown("Timeline maps a macro 60-week sequence.")
    start_date = datetime.date(2026, 9, 1)
    macro_schedule = [
        {"Phase": "Fall Registration", "Start": start_date - datetime.timedelta(days=30), "End": start_date, "Type": "Admin"},
        {"Phase": "Term 1 (Fall/Winter)", "Start": start_date, "End": start_date + datetime.timedelta(weeks=20), "Type": "Classes"},
        {"Phase": "Winter Showcase", "Start": start_date + datetime.timedelta(weeks=18), "End": start_date + datetime.timedelta(weeks=19), "Type": "Event"},
        {"Phase": "Winter Break", "Start": start_date + datetime.timedelta(weeks=20), "End": start_date + datetime.timedelta(weeks=22), "Type": "Break"},
        {"Phase": "Term 2 (Spring)", "Start": start_date + datetime.timedelta(weeks=22), "End": start_date + datetime.timedelta(weeks=42), "Type": "Classes"}
    ]
    df_macro = pd.DataFrame(macro_schedule)
    fig_macro = px.timeline(df_macro, x_start="Start", x_end="End", y="Phase", color="Type", color_discrete_map={"Classes": "#3b82f6", "Event": "#ff0000", "Break": "#00e676", "Admin": "#ffa421"})
    fig_macro.update_yaxes(autorange="reversed")
    fig_macro.update_layout(xaxis_title="Date", yaxis_title="")
    st.plotly_chart(fig_macro, use_container_width=True)

with tab3:
    st.markdown("### 💻 Export Student App for Streamlit Cloud")
    st.markdown(
        "Generates a Python Streamlit app for GitHub + Streamlit Community Cloud. "
        "Download `student_app.py`, `requirements.txt`, and `config.toml`, then push them to GitHub."
    )

    try:
        site_programs = []

        for i in range(len(programs)):
            if offered_flags[i]:
                poster = str(posters[i]).strip().replace(" &", "&").replace("&amp;", "&")

                site_programs.append({
                    "id": str(i + 1),
                    "name": str(programs[i]).strip(),
                    "hours": float(base_weekly_hours[i]),
                    "weeks": int(program_weeks[i]),
                    "fee": float(term_fees[i]),
                    "poster": poster,
                    "desc": str(descriptions[i]).strip(),
                    "song_count": "4-5 songs" if program_weeks[i] >= 20 else "2-3 songs",
                })

        if not site_programs:
            st.warning("⚠️ No programs are currently marked as 'Offered'. Toggle at least one category.")
        else:
            programs_json = json.dumps(site_programs, indent=2).replace("</", "<\\/")

            student_app_template = r"""import streamlit as st
import urllib.parse
import pandas as pd

st.set_page_config(
    page_title="BollyFusion Academy",
    layout="centered",
    initial_sidebar_state="collapsed"
)

AVAILABLE_PROGRAMS = __PROGRAMS_JSON__

st.markdown('''
<style>
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(255, 95, 162, .16), transparent 30%),
        radial-gradient(circle at top right, rgba(85, 198, 255, .14), transparent 25%),
        #07070f;
    color: #f9fafb;
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

.stButton > button {
    width: 100%;
    padding: 14px 18px;
    font-size: 16px;
}

button[kind="primary"] {
    background: linear-gradient(90deg, #ffcf5f, #ff5fa2) !important;
    color: #171204 !important;
    border: none !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.bf-hero {
    border-radius: 28px;
    padding: 32px 20px;
    border: 1px solid rgba(255, 255, 255, .12);
    background:
        linear-gradient(135deg, rgba(255, 95, 162, .18), rgba(85, 198, 255, .12), rgba(255, 207, 95, .14));
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
    background: linear-gradient(90deg, #ffcf5f, #ff5fa2, #55c6ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
}

.bf-muted {
    color: rgba(249, 250, 251, .68);
}

.bf-section-title h2 {
    margin-bottom: 4px;
}

.bf-card {
    border-radius: 24px;
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, .12);
    background: rgba(255, 255, 255, .05);
    margin-bottom: 12px;
}

.bf-media {
    position: relative;
    aspect-ratio: 16 / 10;
    background: linear-gradient(135deg, rgba(255, 95, 162, .35), rgba(85, 198, 255, .28));
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
    background: linear-gradient(to top, rgba(3, 7, 18, .65), transparent 45%);
}

.bf-badge {
    position: absolute;
    top: 12px;
    left: 12px;
    padding: 7px 10px;
    border-radius: 999px;
    background: rgba(0, 0, 0, .35);
    border: 1px solid rgba(255, 255, 255, .15);
    font-size: 12px;
    font-weight: 800;
    color: white;
}

.bf-badge-bottom {
    top: auto;
    bottom: 12px;
    left: auto;
    right: 12px;
    background: rgba(255, 207, 95, .18);
}

.bf-body {
    padding: 16px;
}

.bf-body h3 {
    margin: 0 0 10px;
    font-size: 1.05rem;
}

.bf-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 10px;
}

.bf-chip {
    padding: 7px 9px;
    border-radius: 999px;
    background: rgba(255, 255, 255, .08);
    border: 1px solid rgba(255, 255, 255, .08);
    font-size: 12px;
    color: rgba(249, 250, 251, .72);
}

.bf-price {
    font-size: 1.25rem;
    font-weight: 900;
    color: #43e97b;
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

.bf-summary div {
    display: flex;
    justify-content: space-between;
    gap: 12px;
}

.bf-id {
    text-align: center;
    padding: 20px;
    border-radius: 24px;
    background:
        linear-gradient(135deg, rgba(255, 207, 95, .12), rgba(255, 95, 162, .12), rgba(85, 198, 255, .12));
    border: 1px solid rgba(255, 255, 255, .12);
    margin-bottom: 16px;
}

@media (max-width: 700px) {
    div[data-baseweb="row"] {
        flex-direction: column !important;
    }

    div[data-baseweb="col"] {
        width: 100% !important;
        min-width: 100% !important;
    }

    .block-container {
        padding-left: 12px;
        padding-right: 12px;
    }
}
</style>
''', unsafe_allow_html=True)

if "app_state" not in st.session_state:
    st.session_state.app_state = "home"

if "current_user" not in st.session_state:
    st.session_state.current_user = {
        "Name": "",
        "Email": "",
        "Program Number": "",
        "Class": "",
        "Fee": 0.0
    }

if "student_db" not in st.session_state:
    st.session_state.student_db = []


def navigate(to_state):
    st.session_state.app_state = to_state


def reset_user():
    st.session_state.current_user = {
        "Name": "",
        "Email": "",
        "Program Number": "",
        "Class": "",
        "Fee": 0.0
    }
    st.session_state.app_state = "home"


if st.session_state.app_state == "home":
    st.markdown('''
    <div class="bf-hero">
        <div class="bf-pill">🎬 BollyFusion Academy</div>
        <h1>Cinematic dance, <span class="bf-gradient">built for every stage</span></h1>
        <p class="bf-muted">
            Register, choose a program, accept waivers, and receive a QR studio pass.
            Optimized for iPhone, Android, and desktop.
        </p>
    </div>
    ''', unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "Register & Enroll",
            use_container_width=True,
            type="primary",
            on_click=navigate,
            args=("register",)
        )

    with col2:
        st.button(
            "Admin Portal",
            use_container_width=True,
            on_click=navigate,
            args=("admin_login",)
        )


elif st.session_state.app_state == "register":
    st.markdown(
        '<div class="bf-section-title"><h2>Student Registration</h2>'
        '<p class="bf-muted">Enter your details to browse available programs.</p></div>',
        unsafe_allow_html=True
    )

    st.session_state.current_user["Name"] = st.text_input(
        "Full Name",
        value=st.session_state.current_user.get("Name", ""),
        placeholder="Jane Doe"
    )

    st.session_state.current_user["Email"] = st.text_input(
        "Email",
        value=st.session_state.current_user.get("Email", ""),
        placeholder="jane@example.com"
    )

    st.write("")

    valid = (
        st.session_state.current_user["Name"].strip() != ""
        and "@" in st.session_state.current_user["Email"]
        and "." in st.session_state.current_user["Email"]
    )

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "Back",
            use_container_width=True,
            on_click=navigate,
            args=("home",)
        )

    with col2:
        st.button(
            "Continue",
            use_container_width=True,
            type="primary",
            disabled=not valid,
            on_click=navigate,
            args=("classes",)
        )


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

                if st.button(
                    f"Select {prog['name']}",
                    key=f"select_{prog['id']}",
                    use_container_width=True,
                    type="primary"
                ):
                    st.session_state.current_user["Class"] = prog["name"]
                    st.session_state.current_user["Program Number"] = prog["id"]
                    st.session_state.current_user["Fee"] = prog["fee"]
                    navigate("checkout")

    st.write("")

    st.button(
        "Back",
        use_container_width=True,
        on_click=navigate,
        args=("register",)
    )


elif st.session_state.app_state == "checkout":
    st.markdown(
        '<div class="bf-section-title"><h2>Secure Checkout</h2>'
        '<p class="bf-muted">Review your program and accept all legal terms.</p></div>',
        unsafe_allow_html=True
    )

    selected_class = st.session_state.current_user.get("Class", "")
    selected_fee = st.session_state.current_user.get("Fee", 0)

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
    st.caption(
        "I acknowledge that dance involves physical exertion and risk of injury. "
        "I assume all risks and release BollyFusion Academy from liability."
    )

    cb2 = st.checkbox("I agree to the Media & Photography Release")
    st.caption(
        "I grant BollyFusion Academy permission to use photographs and video recordings of me "
        "for studio-related promotional purposes."
    )

    cb3 = st.checkbox("I agree to the Refund Policy")
    st.caption(
        "A free refund is available after 2 weeks of program commencement. "
        "No refunds or prorations outside this window."
    )

    st.write("")

    col1, col2 = st.columns(2)

    with col1:
        st.button(
            "Back",
            use_container_width=True,
            on_click=navigate,
            args=("classes",)
        )

    with col2:
        can_pay = cb1 and cb2 and cb3

        def process_payment():
            st.session_state.student_db.append({
                "Name": st.session_state.current_user.get("Name", ""),
                "Email": st.session_state.current_user.get("Email", ""),
                "Program Number": st.session_state.current_user.get("Program Number", ""),
                "Class": st.session_state.current_user.get("Class", ""),
                "Status": "Paid"
            })
            st.session_state.app_state = "success"

        st.button(
            "Pay Securely",
            use_container_width=True,
            type="primary",
            disabled=not can_pay,
            on_click=process_payment
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

    st.button(
        "Done (Back to Home)",
        use_container_width=True,
        type="primary",
        on_click=reset_user
    )


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
        st.button(
            "Cancel",
            use_container_width=True,
            on_click=navigate,
            args=("home",)
        )

    with col2:
        if st.button(
            "Login",
            use_container_width=True,
            type="primary"
        ):
            if a_user == "admin" and a_pass == "admin123":
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

        st.download_button(
            "Download CSV",
            data=csv,
            file_name="bollyfusion-registrations.csv",
            mime="text/csv",
            key="download_roster_csv"
        )
    else:
        st.info("No students have registered yet during this session.")

    st.write("")

    st.button(
        "Logout",
        use_container_width=True,
        on_click=navigate,
        args=("home",)
    )
"""

            student_app_code = student_app_template.replace("__PROGRAMS_JSON__", programs_json)

            requirements_code = """streamlit>=1.36.0
pandas>=2.0.0
"""

            config_code = """[theme]
base="dark"
primaryColor="#ffcf5f"
backgroundColor="#07070f"
secondaryBackgroundColor="#111827"
textColor="#f9fafb"
"""

            st.success(f"✅ Generated Streamlit student app for {len(site_programs)} offered programs.")

            st.download_button(
                "⬇️ Download student_app.py",
                data=student_app_code.encode("utf-8"),
                file_name="student_app.py",
                mime="text/x-python",
                key="download_student_app"
            )

            st.download_button(
                "⬇️ Download requirements.txt",
                data=requirements_code.encode("utf-8"),
                file_name="requirements.txt",
                mime="text/plain",
                key="download_requirements"
            )

            st.download_button(
                "⬇️ Download config.toml",
                data=config_code.encode("utf-8"),
                file_name="config.toml",
                mime="text/plain",
                key="download_config_toml"
            )

            with st.expander("Show student_app.py code"):
                st.code(student_app_code, language="python")

    except Exception as e:
        st.error(f"Generator error: {e}")
