
import streamlit as st
import pandas as pd
import io
import random
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

# =====================================
# STUDYSYNC
# =====================================

st.set_page_config(
    page_title="StudySync",
    page_icon="🍊",
    layout="wide"
)

# ---------- SESSION STATE ----------

defaults = {
    "subjects": [
        "Mathematics", "Physics", "Chemistry",
        "Computer Science", "English", "Biology",
        "Economics", "Accountancy", "History"
    ],
    "selected_subjects": [],
    "weak_subjects": [],
    "schedule": None,
    "name": "",
    "student_class": "Class 12",
    "study_hours": 4,
    "study_start": datetime.strptime("16:00", "%H:%M").time(),
    "session_length": 50,
    "break_length": 10
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- COLOURS ----------

orange = "#FF985F"
blue = "#A8C9FF"
pink = "#F6B7CF"
purple = "#C9B5F4"
green = "#A9DEC9"
yellow = "#F5D58C"

# ---------- CSS DESIGN ----------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at 90% 5%, #ffe8d9 0%, transparent 30%),
        radial-gradient(ellipse at 5% 95%, #e8eaff 0%, transparent 30%),
        #f5f5f7;
    color: #20232b;
    font-family: 'DM Sans', sans-serif;
}

.block-container {
    max-width: 1450px;
    padding: 2rem 2.5rem 4rem 2.5rem;
}

h1, h2, h3 {
    color: #20232b;
    letter-spacing: -0.7px;
}

p, label {
    color: #69717e;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.62);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.85);
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 8px 28px rgba(40,50,70,0.045);
}

[data-testid="stTabs"] [role="tablist"] {
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(255,255,255,0.9);
    padding: 7px;
    border-radius: 18px;
    gap: 8px;
}

[data-testid="stTabs"] button[role="tab"] {
    border-radius: 13px;
    color: #69717e;
}

[data-testid="stTabs"] button[aria-selected="true"] {
    background: white;
    color: #f18448;
    box-shadow: 0 3px 12px rgba(40,50,70,0.08);
}

.stButton > button,
.stDownloadButton > button {
    border-radius: 13px;
    border: 1px solid rgba(255,255,255,0.9);
    background: linear-gradient(135deg, #ffad7e, #ff8e56);
    color: white;
    font-weight: 600;
    min-height: 43px;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #ff985f;
    color: white;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: rgba(255,255,255,0.75);
    border-radius: 12px;
}

.glass-card {
    background: rgba(255,255,255,0.62);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.9);
    border-radius: 22px;
    padding: 23px;
    box-shadow: 0 10px 35px rgba(50,60,80,0.055);
    margin-bottom: 14px;
}

.small-label {
    color: #89909d;
    font-size: 12px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.big-number {
    font-size: 27px;
    font-weight: 600;
    color: #242936;
}

.mono {
    font-family: 'DM Mono', monospace;
    font-size: 12px;
    color: #89909d;
}

.ring {
    width: 155px;
    height: 155px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: auto;
    position: relative;
}

.ring-inner {
    width: 119px;
    height: 119px;
    background: #f9f9fb;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    box-shadow: inset 0 2px 8px rgba(0,0,0,0.04);
}

.ring-number {
    font-size: 28px;
    font-weight: 600;
    color: #222936;
}

.ring-caption {
    font-size: 12px;
    color: #9299a5;
}

.orange-dot {
    display: inline-block;
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #ff985f;
    margin-right: 7px;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------

st.markdown("""
<div style="display:flex;align-items:center;gap:13px;margin-bottom:5px">
    <div style="width:43px;height:43px;border-radius:14px;
    background:linear-gradient(140deg,#ffc49f,#ff8b50);
    display:flex;align-items:center;justify-content:center;
    color:white;font-size:24px;font-weight:bold">S</div>
    <div>
        <div style="font-size:25px;font-weight:700;color:#20232b">
            StudySync
        </div>
        <div class="mono">PLAN. STUDY. GROW.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------- PROFILE ----------

st.markdown(
    f"<div class='small-label'>YOUR PERSONAL STUDY SPACE</div>",
    unsafe_allow_html=True
)

st.title(
    "Good day, " +
    (st.session_state.name.strip() if st.session_state.name.strip() else "Student") +
    "!"
)

st.caption("Small steps. Big progress.")

with st.expander("⚙️ Student settings", expanded=False):

    c1, c2 = st.columns(2)

    with c1:
        st.session_state.name = st.text_input(
            "Your name",
            value=st.session_state.name
        )

        st.session_state.student_class = st.selectbox(
            "Your class",
            ["Class 9", "Class 10", "Class 11", "Class 12", "College"],
            index=["Class 9", "Class 10", "Class 11", "Class 12", "College"].index(
                st.session_state.student_class
            )
        )

    with c2:
        st.session_state.study_hours = st.slider(
            "Daily study hours",
            1, 12,
            st.session_state.study_hours
        )

        st.session_state.study_start = st.time_input(
            "Study start time",
            value=st.session_state.study_start
        )

        st.session_state.session_length = st.selectbox(
            "Session duration",
            [25, 40, 50, 60, 90],
            index=[25, 40, 50, 60, 90].index(
                st.session_state.session_length
            )
        )

        st.session_state.break_length = st.selectbox(
            "Break duration",
            [5, 10, 15, 20],
            index=[5, 10, 15, 20].index(
                st.session_state.break_length
            )
        )

# ---------- SUBJECT DATA ----------

st.markdown("### Your subjects")

c1, c2 = st.columns([3, 1])

with c1:
    st.multiselect(
        "Select your subjects",
        options=st.session_state.subjects,
        key="selected_subjects",
        placeholder="Choose your subjects"
    )

with c2:
    with st.popover("＋ Add subject"):
        with st.form("add_subject"):
            custom = st.text_input("New subject")
            submitted = st.form_submit_button("Add")

            if submitted:
                clean = custom.strip()

                if not clean:
                    st.warning("Enter a subject name.")
                elif any(
                    clean.lower() == s.lower()
                    for s in st.session_state.subjects
                ):
                    st.warning("Subject already exists.")
                else:
                    st.session_state.subjects.append(clean)
                    st.session_state.selected_subjects.append(clean)
                    st.success("Subject added!")

if st.session_state.selected_subjects:
    st.multiselect(
        "Subjects needing extra attention",
        options=st.session_state.selected_subjects,
        key="weak_subjects",
        placeholder="Choose weaker subjects"
    )

st.divider()

# ---------- GENERATE TIMETABLE ----------

st.markdown("### Your study plan")

if st.button("Generate weekly timetable", use_container_width=True):

    selected = st.session_state.selected_subjects
    weak = st.session_state.weak_subjects

    if not st.session_state.name.strip():
        st.warning("Please enter your name in Student settings.")

    elif not selected:
        st.warning("Please select at least one subject.")

    else:
        weighted = []

        for subject in selected:
            weighted.append(subject)

            if subject in weak:
                weighted.append(subject)

        minutes = st.session_state.study_hours * 60
        session_length = st.session_state.session_length
        break_length = st.session_state.break_length

        count = max(
            1,
            (minutes + break_length) // (session_length + break_length)
        )

        rows = []
        index = 0

        for day in range(7):

            date = datetime.today().date() + timedelta(days=day)

            current = datetime.combine(
                date,
                st.session_state.study_start
            )

            for session in range(count):

                subject = weighted[index % len(weighted)]

                end = current + timedelta(minutes=session_length)

                rows.append({
                    "Day": date.strftime("%A"),
                    "Date": date.strftime("%d %b"),
                    "Start": current.strftime("%I:%M %p"),
                    "End": end.strftime("%I:%M %p"),
                    "Subject": subject,
                    "Completed": False
                })

                index += 1
                current = end + timedelta(minutes=break_length)

        st.session_state.schedule = pd.DataFrame(rows)
        st.success("Your timetable is ready!")

# ---------- DASHBOARD ----------

schedule = st.session_state.schedule

if schedule is not None:

    st.divider()

    completed = int(schedule["Completed"].sum())
    total = len(schedule)
    percent = completed / total if total else 0

    st.markdown("### Overview")

    c1, c2, c3 = st.columns([1, 1, 1])

    with c1:
        st.markdown(
            f"""
            <div class="glass-card" style="text-align:center">
                <div class="small-label">WEEKLY PROGRESS</div>
                <div class="ring" style="
                background:conic-gradient(
                #ffad7e 0% {percent*100}%,
                #e9e9ed {percent*100}% 100%);
                ">
                    <div class="ring-inner">
                        <div class="ring-number">{percent*100:.0f}%</div>
                        <div class="ring-caption">completed</div>
                    </div>
                </div>
                <div style="color:#858c98;font-size:13px">
                    {completed} of {total} sessions
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="small-label">DAILY STUDY GOAL</div>
                <div class="big-number">{st.session_state.study_hours} hrs</div>
                <div style="color:#ff985f;font-size:13px">
                    Your planned study time
                </div>
                <div style="margin-top:25px;font-size:13px;color:#89909d">
                    Session length
                </div>
                <div class="big-number">
                    {st.session_state.session_length} min
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="small-label">SUBJECTS</div>
                <div class="big-number">
                    {len(st.session_state.selected_subjects)}
                </div>
                <div style="color:#89909d;font-size:13px">
                    Subjects selected
                </div>
                <div style="margin-top:25px;font-size:13px;color:#89909d">
                    Priority subjects
                </div>
                <div class="big-number">
                    {len(st.session_state.weak_subjects)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ---------- TABS ----------

    home_tab, timetable_tab, subjects_tab, progress_tab = st.tabs([
        "⌂  Home",
        "▦  Timetable",
        "◉  Subjects",
        "◌  Progress"
    ])

    with home_tab:

        st.subheader("Today's schedule")

        today_name = datetime.today().strftime("%A")

        today_rows = schedule[schedule["Day"] == today_name]

        if today_rows.empty:
            st.info("No sessions scheduled today.")
        else:
            for _, row in today_rows.iterrows():

                symbol = "✓" if row["Completed"] else "○"

                st.markdown(
                    f"""
                    <div class="glass-card"
                    style="padding:15px 20px;margin-bottom:9px">
                        <div style="display:flex;justify-content:space-between">
                            <div>
                                <div class="mono">
                                    {row['Start']} — {row['End']}
                                </div>
                                <div style="font-weight:600;margin-top:5px">
                                    {row['Subject']}
                                </div>
                            </div>
                            <div style="color:#ff985f;font-size:20px">
                                {symbol}
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    with timetable_tab:

        st.subheader("Weekly timetable")

        edited = st.data_editor(
            schedule,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            key="schedule_editor",
            column_config={
                "Completed": st.column_config.CheckboxColumn(
                    "Completed"
                )
            }
        )

        st.session_state.schedule = edited

        st.subheader("Daily view")

        days = edited["Day"].drop_duplicates().tolist()

        day_choice = st.selectbox("Select day", days)

        st.dataframe(
            edited[edited["Day"] == day_choice],
            use_container_width=True,
            hide_index=True
        )

    with subjects_tab:

        st.subheader("Subject overview")

        for i, subject in enumerate(st.session_state.selected_subjects):

            colours = [orange, blue, purple, green, pink, yellow]
            colour = colours[i % len(colours)]

            priority = (
                "Needs improvement"
                if subject in st.session_state.weak_subjects
                else "Regular priority"
            )

            st.markdown(
                f"""
                <div class="glass-card"
                style="display:flex;justify-content:space-between;
                align-items:center;padding:16px 22px">
                    <div>
                        <div style="font-weight:600">{subject}</div>
                        <div class="mono">{priority}</div>
                    </div>
                    <div style="width:12px;height:12px;
                    border-radius:50%;background:{colour}"></div>
                </div>
                """,
                unsafe_allow_html=True
            )

    with progress_tab:

        st.subheader("Your progress")

        completed = int(st.session_state.schedule["Completed"].sum())
        total = len(st.session_state.schedule)

        st.metric("Completed sessions", completed)
        st.metric("Remaining sessions", total - completed)

        st.progress(completed / total if total else 0)

        st.caption("Tick completed sessions in the Timetable tab.")

    # ---------- PDF DOWNLOAD ----------

    st.divider()
    st.markdown("### Export your timetable")

    def make_pdf(data):

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4)
        )

        styles = getSampleStyleSheet()
        elements = []

        elements.append(
            Paragraph("StudySync — Weekly Timetable", styles["Title"])
        )

        elements.append(Spacer(1, 15))

        elements.append(
            Paragraph(
                f"Student: {st.session_state.name} | "
                f"Class: {st.session_state.student_class}",
                styles["Normal"]
            )
        )

        elements.append(Spacer(1, 20))

        table_data = [[
            "Day", "Date", "Start", "End", "Subject", "Completed"
        ]]

        for _, row in data.iterrows():
            table_data.append([
                str(row["Day"]),
                str(row["Date"]),
                str(row["Start"]),
                str(row["End"]),
                str(row["Subject"]),
                "Yes" if row["Completed"] else "No"
            ])

        table = Table(table_data, repeatRows=1)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FF985F")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.lightgrey),
            ("PADDING", (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#FFF5EF")])
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return buffer.getvalue()

    pdf = make_pdf(st.session_state.schedule)

    st.download_button(
        "↓  Download PDF",
        data=pdf,
        file_name="StudySync_Timetable.pdf",
        mime="application/pdf"
    )

else:

    st.markdown("""
    <div class="glass-card" style="text-align:center;padding:45px">
        <div style="font-size:36px;color:#ff985f">◌</div>
        <h3>Your study space is ready.</h3>
        <p>Select your subjects and generate your first timetable.</p>
    </div>
    """, unsafe_allow_html=True)

# ---------- FOOTER ----------

st.divider()

st.markdown(
    "<div style='text-align:center;color:#a0a5af;"
    "font-size:12px;font-family:DM Mono'>"
    "STUDYSYNC · PLAN. STUDY. GROW.</div>",
    unsafe_allow_html=True
)
