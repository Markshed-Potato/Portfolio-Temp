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
TAGLINE = "Striving to be an all-rounder"
GITHUB = "https://github.com/Markshed-Potato"
PHOTO_FILE = Path(__file__).parent / "Racho_Picture.jpg"

ICONS = {
    "person": '<circle cx="12" cy="8" r="3.5"/><path d="M5 21v-2a7 7 0 0 1 14 0v2"/>',
    "location": '<path d="M20 10c0 5-8 12-8 12S4 15 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/>',
    "education": '<path d="m2 9 10-5 10 5-10 5L2 9Z"/><path d="M6 11v5c3.5 2.7 8.5 2.7 12 0v-5M22 9v6"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
}

BIO = "I am outgoing and adventurous, even in the world of technology."
BACKGROUND = "I grew up in Zamboanga City and later enrolled at CIT-U."
EDUCATION = ("I was a top student from kindergarten through senior high school, "
             "but college soon humbled me.")
INTERESTS = "I enjoy anything that gives me energy."

SKILLS = {"SQL": 60, "SFX": 70, "Python": 80, "C#": 75}

MILESTONES = [
    (None, "Grew up in Zamboanga City"),
    (None, "Ranked at the top of my class from kindergarten through senior high school"),
    (None, "Enrolled in the BSCS program at CIT-U"),
    (2025, "Built Lost and Found and AgriLink as solo projects"),
    (2026, "Built Evacusafe as a solo project and joined Game Jam 2026 as an SFX/VFX artist"),
]

PROJECTS = [
    {"title": "Game Jam 2026", "role": "SFX / VFX", "year": 2026, "type": "Game", "team": "Team"},
    {"title": "Lost and Found", "role": "Solo project", "year": 2025, "type": "Solo", "team": "Solo"},
    {"title": "Evacusafe", "role": "Solo project", "year": 2026, "type": "Solo", "team": "Solo"},
    {"title": "AgriLink", "role": "Solo project", "year": 2025, "type": "Solo", "team": "Solo"},
]

def icon(name, size=18):
    return (f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{ICONS[name]}</svg>')

# =========================================================

st.set_page_config(page_title=f"{NAME} | Portfolio", page_icon=str(PHOTO_FILE), layout="wide")
st.markdown("""
<style>
.hero{padding:1.6rem 2rem;border-radius:18px;background:linear-gradient(135deg,#6C5CE7,#00CEC9);color:white;margin-bottom:1rem}
.hero h1{display:flex;align-items:center;gap:.65rem;margin:0;font-size:2.6rem}.hero p{margin:.3rem 0 0}
.icon-label{display:flex;align-items:center;gap:.55rem;margin:.5rem 0}
.icon{flex:none}
</style>""", unsafe_allow_html=True)

st.session_state.setdefault("likes", 0)
st.session_state.setdefault("messages", [])

def photo(**kw):
    if PHOTO_FILE.exists():
        st.image(str(PHOTO_FILE), caption=NAME, **kw)
    else:
        st.warning(f"Place {PHOTO_FILE.name} in the same folder as app.py.")

skills_df = pd.DataFrame({"Skill": list(SKILLS), "Level": list(SKILLS.values())})

# ---------- Sidebar ----------
with st.sidebar:
    photo(width=160)
    st.header(NAME)
    st.caption(f"{PROGRAM} · {SECTION}")
    st.markdown(f'<div class="icon-label">{icon("location")}<span>{CITY}</span></div>',
                unsafe_allow_html=True)
    st.divider()
    st.subheader("Customize your view")
    show_chart = st.checkbox("Show skills chart", True)
    chart_type = st.radio("Chart type", ["Bar", "Line", "Area"], horizontal=True)
    min_level = st.slider("Minimum skill level", 0, 100, 0, 5)
    st.divider()
    if st.button("Like this portfolio", icon=":material/favorite:"):
        st.session_state.likes += 1
        st.toast("Thank you!", icon=":material/favorite:")
    st.metric("Likes", st.session_state.likes)
    st.link_button("GitHub", GITHUB)

# ---------- Hero ----------
st.markdown(f"""<div class="hero"><h1>{icon("person", 32)} {NAME}</h1>
<p>{TAGLINE}</p><p><b>{PROGRAM} · {SECTION}</b></p></div>""", unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
c1.metric("Projects", len(PROJECTS))
c2.metric("Solo projects", sum(p["team"] == "Solo" for p in PROJECTS))
c3.metric("Skills", len(SKILLS))

tabs = st.tabs(["About", "Autobiography", "Skills", "Projects", "Contact"])

# ---------- About ----------
with tabs[0]:
    a, b = st.columns([1, 2], gap="large")
    with a:
        photo(use_container_width=True)
    with b:
        st.header("About me")
        st.write(BIO)
        st.markdown(
            f'<div class="icon-label">{icon("education")}<span>{PROGRAM}, CIT-U</span></div>'
            f'<div class="icon-label">{icon("location")}<span>{CITY}</span></div>'
            f'<div class="icon-label">{icon("target")}<span>{TAGLINE}</span></div>',
            unsafe_allow_html=True,
        )
        with st.expander("Interests"):
            st.write(INTERESTS)
        st.info("I'm open to collaboration!")

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
    pick = st.select_slider("Explore my story", options=list(range(len(MILESTONES))),
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
            st.warning("No skills match your selected filter.")
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
            st.link_button("View on GitHub", GITHUB, key=f"gh{i}")
    st.subheader("Rate my projects")
    st.feedback("stars")

# ---------- Contact ----------
with tabs[4]:
    st.header("Get in touch")
    x, y = st.columns([1.3, 1], gap="large")
    with x:
        with st.form("contact", clear_on_submit=True):
            n = st.text_input("Your name")
            e = st.text_input("Your email")
            topic = st.selectbox("Topic", ["Feedback", "Collaboration", "Just saying hello"])
            msg = st.text_area("Message", height=120)
            mood = st.radio("How was the site?", ["Loved it", "Good", "Okay"], horizontal=True)
            ok = st.checkbox("I agree to be contacted.")
            sent = st.form_submit_button("Send", type="primary")
        if sent:
            if not (n and e and msg):
                st.error("Please enter your name, email address, and message.")
            else:
                with st.spinner("Sending..."):
                    time.sleep(1)
                st.session_state.messages.append({"name": n, "topic": topic, "mood": mood})
                st.success(f"Thanks, {n}!")
                st.balloons()
    with y:
        st.markdown(
            f'<div class="icon-label">{icon("mail")}<span>{EMAIL}</span></div>'
            f'<div class="icon-label">{icon("location")}<span>{CITY}</span></div>',
            unsafe_allow_html=True,
        )
        st.map(pd.DataFrame({"lat": [6.9214], "lon": [122.0790]}), zoom=10)
        if st.session_state.messages:
            st.caption(f"Messages this session: {len(st.session_state.messages)}")

st.divider()
buf = io.StringIO(); skills_df.to_csv(buf, index=False)
f1, f2 = st.columns([3, 1])
f1.caption(f"© 2026 {NAME} · {SECTION} · Created with Streamlit")
f2.download_button("Skills CSV", buf.getvalue(), "skills.csv", "text/csv",
                   icon=":material/download:")
