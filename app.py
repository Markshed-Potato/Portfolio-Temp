import io
import time
from pathlib import Path
import pandas as pd
import streamlit as st

NAME = "Wilmark S. Racho"
SECTION = "CS365"
PROGRAM = "BSCS-3"
EMAIL = "s.wilmarkracho@gmail.com"
CITY = "Zamboanga"
TAGLINE = "Be the all rounder"
GITHUB = "https://github.com/Markshed-Potato"
PHOTO_FILE = Path(__file__).parent / "Racho_Picture.jpg"

BIO = "I am an outgoing and adventurous person, even in tech."
BACKGROUND = "I grew up in Zamboanga City and entered university at CIT-U."
EDUCATION = ("I was a top student from kindergarten to Senior High School, "
             "then got humbled when I stepped into college.")
INTERESTS = "Anything that gives me energy."

SKILLS = {"SQL": 60, "SFX": 70, "Python": 80, "C#": 75}

MILESTONES = [
    (None, "Grew up in Zamboanga City"),
    (None, "Top of my class from kindergarten to SHS"),
    (None, "Entered CIT-U for BSCS"),
    (2025, "Built Lost and Found and AgriLink (solo)"),
    (2026, "Built Evacusafe (solo) and joined Game Jam 2026 as SFX/VFX"),
]

PROJECTS = [
    {"title": "Game Jam 2026", "role": "SFX / VFX", "year": 2026, "type": "Game", "team": "Team"},
    {"title": "Lost and Found", "role": "Solo project", "year": 2025, "type": "Solo", "team": "Solo"},
    {"title": "Evacusafe", "role": "Solo project", "year": 2026, "type": "Solo", "team": "Solo"},
    {"title": "AgriLink", "role": "Solo project", "year": 2025, "type": "Solo", "team": "Solo"},
]
# =========================================================

st.set_page_config(page_title=f"{NAME} | Portfolio", page_icon="🎮", layout="wide")
st.markdown("""
<style>
.hero{padding:1.6rem 2rem;border-radius:18px;background:linear-gradient(135deg,#6C5CE7,#00CEC9);color:white;margin-bottom:1rem}
.hero h1{margin:0;font-size:2.6rem}.hero p{margin:.3rem 0 0}
</style>""", unsafe_allow_html=True)

st.session_state.setdefault("likes", 0)
st.session_state.setdefault("messages", [])

def photo(**kw):
    if PHOTO_FILE.exists():
        st.image(str(PHOTO_FILE), caption=NAME, **kw)
    else:
        st.warning(f"Put {PHOTO_FILE.name} in the same folder as app.py")

skills_df = pd.DataFrame({"Skill": list(SKILLS), "Level": list(SKILLS.values())})

# ---------- Sidebar ----------
with st.sidebar:
    photo(width=160)
    st.header(NAME)
    st.caption(f"{PROGRAM} · {SECTION}\n\n📍 {CITY}")
    st.divider()
    st.subheader("Customize view")
    show_chart = st.checkbox("Show skills chart", True)
    chart_type = st.radio("Chart type", ["Bar", "Line", "Area"], horizontal=True)
    min_level = st.slider("Minimum skill level", 0, 100, 0, 5)
    st.divider()
    if st.button("👍 Like this portfolio"):
        st.session_state.likes += 1
        st.toast("Thanks!", icon="💜")
    st.metric("Likes", st.session_state.likes)
    st.link_button("GitHub", GITHUB)

# ---------- Hero ----------
st.markdown(f"""<div class="hero"><h1>👋 {NAME}</h1>
<p>{TAGLINE}</p><p><b>{PROGRAM} · {SECTION}</b></p></div>""", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Projects", len(PROJECTS))
c2.metric("Solo projects", sum(p["team"] == "Solo" for p in PROJECTS))
c3.metric("Skills", len(SKILLS))

tabs = st.tabs(["🙋 About", "📖 Autobiography", "🛠️ Skills", "💼 Projects", "✉️ Contact"])

# ---------- About ----------
with tabs[0]:
    a, b = st.columns([1, 2], gap="large")
    with a:
        photo(use_container_width=True)
    with b:
        st.header("About me")
        st.write(BIO)
        st.markdown(f"- 🎓 {PROGRAM}, CIT-U\n- 📍 {CITY}\n- 🎯 {TAGLINE}")
        with st.expander("Interests"):
            st.write(INTERESTS)
        st.info("Open to collaborations!")

# ---------- Autobiography ----------
with tabs[1]:
    st.header("My story")
    l, r = st.columns(2, gap="large")
    with l:
        st.subheader("Background")
        st.write(BACKGROUND)
        st.subheader("Education")
        st.write(EDUCATION)
    with r:
        st.subheader("Interests")
        st.write(INTERESTS)
    st.subheader("Milestones")
    ms = pd.DataFrame(MILESTONES, columns=["Year", "Milestone"]).fillna("—")
    ms["Year"] = ms["Year"].astype(str).str.replace(".0", "", regex=False)
    st.dataframe(ms, hide_index=True, use_container_width=True)
    pick = st.select_slider("Scrub through my story", options=list(range(len(MILESTONES))),
                            format_func=lambda i: f"Step {i+1}")
    st.success(MILESTONES[pick][1])

# ---------- Skills ----------
with tabs[2]:
    st.header("Skills")
    f = skills_df[skills_df.Level >= min_level]
    s1, s2 = st.columns([1, 1.4], gap="large")
    with s1:
        st.write("My main tools: " + ", ".join(SKILLS) + ".")
        st.dataframe(f, hide_index=True, use_container_width=True,
                     column_config={"Level": st.column_config.ProgressColumn("Level", min_value=0, max_value=100, format="%d%%")})
    with s2:
        if f.empty:
            st.warning("No skills match the filter.")
        elif show_chart:
            {"Bar": st.bar_chart, "Line": st.line_chart, "Area": st.area_chart}[chart_type](f.set_index("Skill")["Level"])

# ---------- Projects ----------
with tabs[3]:
    st.header("Projects")
    p1, p2 = st.columns([2, 1])
    kind = p1.selectbox("Filter", ["All", "Solo", "Game"])
    newest = p2.toggle("Newest first", True)
    shown = sorted([p for p in PROJECTS if kind == "All" or p["type"] == kind],
                   key=lambda p: p["year"], reverse=newest)
    cols = st.columns(2, gap="large")
    for i, p in enumerate(shown):
        with cols[i % 2].container(border=True):
            st.subheader(p["title"])
            st.caption(f"{p['year']} · {p['type']}")
            st.write(f"**Role:** {p['role']}")
            st.link_button("See my GitHub", GITHUB, key=f"gh{i}")
    st.subheader("Rate my work")
    st.feedback("stars")

# ---------- Contact ----------
with tabs[4]:
    st.header("Get in touch")
    x, y = st.columns([1.3, 1], gap="large")
    with x:
        with st.form("contact", clear_on_submit=True):
            n = st.text_input("Your name")
            e = st.text_input("Your email")
            topic = st.selectbox("Topic", ["Feedback", "Collaboration", "Just saying hi"])
            msg = st.text_area("Message", height=120)
            mood = st.radio("How was the site?", ["😍 Loved it", "🙂 Good", "😐 Okay"], horizontal=True)
            ok = st.checkbox("I agree to be contacted back")
            sent = st.form_submit_button("Send", type="primary")
        if sent:
            if not (n and e and msg):
                st.error("Fill in name, email, and message.")
            else:
                with st.spinner("Sending..."):
                    time.sleep(1)
                st.session_state.messages.append({"name": n, "topic": topic, "mood": mood})
                st.success(f"Thanks, {n}!")
                st.balloons()
    with y:
        st.markdown(f"**📧** {EMAIL}\n\n**📍** {CITY}")
        st.map(pd.DataFrame({"lat": [6.9214], "lon": [122.0790]}), zoom=10)
        if st.session_state.messages:
            st.caption(f"Messages this session: {len(st.session_state.messages)}")

st.divider()
buf = io.StringIO(); skills_df.to_csv(buf, index=False)
f1, f2 = st.columns([3, 1])
f1.caption(f"© 2026 {NAME} · {SECTION} · Built with Streamlit")
f2.download_button("⬇️ Skills CSV", buf.getvalue(), "skills.csv", "text/csv")
