import streamlit as st
import re
import google.generativeai as genai
from secret import API_KEY
from pdf_generator import create_pdf

# Configure Gemini
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# Page Config
st.set_page_config(
    page_title="AI Resume Studio // HUD",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk / Glassmorphic UI CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

/* Global Setup & Animated Gradient Background */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: radial-gradient(circle at 20% 20%, rgba(112, 0, 255, 0.15), transparent 40%),
                radial-gradient(circle at 80% 80%, rgba(0, 243, 255, 0.15), transparent 40%),
                radial-gradient(circle at 50% 50%, rgba(255, 0, 127, 0.08), transparent 50%),
                #030712 !important;
    color: #f3f4f6 !important;
}

/* Hide default headers/footers */
header[data-testid="stHeader"] { background: transparent !important; }
footer { visibility: hidden; }

/* Full-Screen Loader Overlay */
.fullscreen-loader-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(3, 7, 18, 0.92);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    z-index: 999999;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.loader-ring {
    position: relative;
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background: conic-gradient(from 0deg, transparent 0%, #00f3ff 50%, #7000ff 100%);
    animation: rotateRing 1.2s linear infinite;
    box-shadow: 0 0 35px rgba(0, 243, 255, 0.4);
}

.loader-ring::before {
    content: '';
    position: absolute;
    top: 6px;
    left: 6px;
    right: 6px;
    bottom: 6px;
    background: #030712;
    border-radius: 50%;
}

.loader-title {
    margin-top: 2rem;
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    background: linear-gradient(90deg, #00f3ff, #7000ff, #ff007f);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: pulseGlow 1.5s ease-in-out infinite alternate;
}

.loader-sub {
    color: #9ca3af;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    margin-top: 0.5rem;
}

@keyframes rotateRing {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

@keyframes pulseGlow {
    0% { opacity: 0.6; filter: drop-shadow(0 0 5px rgba(0,243,255,0.2)); }
    100% { opacity: 1; filter: drop-shadow(0 0 15px rgba(112,0,255,0.8)); }
}

/* Hero Header Styling */
.hero-wrapper {
    text-align: center;
    padding: 3rem 1.5rem 2rem;
    margin-bottom: 2rem;
    background: rgba(17, 24, 39, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 28px;
    backdrop-filter: blur(20px);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.hero-glow-title {
    font-size: 4rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #00f3ff 0%, #7000ff 50%, #ff007f 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px rgba(112, 0, 255, 0.3);
}

.hero-subtag {
    color: #9ca3af;
    font-size: 1.15rem;
    margin-top: 0.75rem;
    font-weight: 400;
}

/* Glass Cards / HUD Stats */
.hud-card {
    background: rgba(17, 24, 39, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 1.25rem;
    text-align: center;
    backdrop-filter: blur(16px);
    transition: all 0.3s ease;
}

.hud-card:hover {
    border-color: rgba(0, 243, 255, 0.4);
    box-shadow: 0 0 25px rgba(0, 243, 255, 0.15);
    transform: translateY(-3px);
}

.hud-val {
    font-size: 1.4rem;
    font-weight: 800;
    color: #00f3ff;
    font-family: 'JetBrains Mono', monospace;
}

.hud-lbl {
    font-size: 0.75rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 0.2rem;
}

/* Custom Form Inputs */
.stTextInput input, .stTextArea textarea {
    background: rgba(11, 15, 25, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 14px !important;
    color: #f3f4f6 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #00f3ff !important;
    box-shadow: 0 0 20px rgba(0, 243, 255, 0.25) !important;
}

/* Glowing Launch Button */
.stButton button {
    background: linear-gradient(135deg, #00f3ff 0%, #7000ff 50%, #ff007f 100%) !important;
    border: none !important;
    border-radius: 16px !important;
    color: #ffffff !important;
    font-weight: 800 !important;
    font-size: 1.2rem !important;
    height: 3.8rem !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    box-shadow: 0 10px 30px rgba(112, 0, 255, 0.4) !important;
    transition: all 0.3s ease !important;
}

.stButton button:hover {
    transform: translateY(-3px) scale(1.01) !important;
    box-shadow: 0 15px 40px rgba(255, 0, 127, 0.6) !important;
}

/* Output Display Cards */
.output-glass-box {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 2rem;
    backdrop-filter: blur(20px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: rgba(3, 7, 18, 0.85) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 ENGINE STATUS")
    st.caption("SYSTEM // GEMINI-2.5-FLASH")
    st.divider()

    st.markdown("#### ⚡ CAPABILITIES")
    st.markdown("🔹 **Neural Document Synthesis**")
    st.markdown("🔹 **ATS Keyword Matching**")
    st.markdown("🔹 **PDF Vector Export**")
    st.markdown("🔹 **Cover Letter Generation**")

    st.divider()
    st.caption("AI Resume Studio v3.0 // 2026 Edition")

# Hero Header Unit
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-glow-title">⚡ AI RESUME STUDIO</div>
    <div class="hero-subtag">Autonomous ATS Optimization & Career Asset Generation</div>
</div>
""", unsafe_allow_html=True)

# HUD Stats Bar
m1, m2, m3 = st.columns(3)
with m1:
    st.markdown("""
    <div class="hud-card">
        <div class="hud-val">GEMINI 2.5</div>
        <div class="hud-lbl">Core Model</div>
    </div>
    """, unsafe_allow_html=True)
with m2:
    st.markdown("""
    <div class="hud-card">
        <div class="hud-val">DUAL-GEN</div>
        <div class="hud-lbl">Resume + Cover</div>
    </div>
    """, unsafe_allow_html=True)
with m3:
    st.markdown("""
    <div class="hud-card">
        <div class="hud-val">REALTIME</div>
        <div class="hud-lbl">ATS Scanner</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Input Section
st.markdown("### 📋 CANDIDATE PROFILE")
col1, col2 = st.columns(2, gap="large")

with col1:
    name = st.text_input("👤 Full Name", placeholder="e.g. Alex Mercer")
    skills = st.text_area("🛠 Skills & Tech Stack", placeholder="e.g. React, Node.js, Python, AWS, Docker", height=130)
    education = st.text_area("🎓 Education & Credentials", placeholder="e.g. B.Tech in Computer Science", height=100)

with col2:
    experience = st.text_area("💼 Work History & Highlights", placeholder="e.g. Software Engineer at Tech Corp: Built microservices handling 1M+ req/day...", height=195)
    job_description = st.text_area("📄 Target Job Description (Optional for ATS Match)", placeholder="Paste target job post to trigger real-time ATS compatibility scoring...", height=100)

st.markdown("<br>", unsafe_allow_html=True)

# Initialize Session State Keys for Persistence
if "generated_text" not in st.session_state:
    st.session_state["generated_text"] = None
if "pdf_file" not in st.session_state:
    st.session_state["pdf_file"] = None
if "ats_analysis_text" not in st.session_state:
    st.session_state["ats_analysis_text"] = None
if "ats_score" not in st.session_state:
    st.session_state["ats_score"] = None
if "user_name" not in st.session_state:
    st.session_state["user_name"] = "Candidate"

# Main Generation Event
if st.button("🚀 INITIALIZE GENERATION PROCESS"):

    if not name or not skills or not education or not experience:
        st.warning("⚠️ Please fill in all required profile fields to continue.")
    else:
        try:
            loader_slot = st.empty()
            
            # Loader Screen
            loader_slot.markdown("""
            <div class="fullscreen-loader-overlay">
                <div class="loader-ring"></div>
                <div class="loader-title">Synthesizing Career Assets</div>
                <div class="loader-sub">[ Processing Gemini 2.5 Prompts & Formats ]</div>
            </div>
            """, unsafe_allow_html=True)

            prompt = f"""
            Generate a professional ATS-friendly Resume Summary and Cover Letter.

            Requirements:
            - Do NOT use placeholders such as [Your Address], [Company Name], [Phone Number].
            - Use only the information provided.
            - Make the cover letter ready to use.
            - Keep the resume summary concise and professional.

            Format:

            # RESUME SUMMARY

            <resume summary>

            # COVER LETTER

            <cover letter>

            Candidate Details:
            Name: {name}
            Skills: {skills}
            Education: {education}
            Experience: {experience}
            """

            response = model.generate_content(prompt)
            
            # Save into Session State to avoid wipe on button click
            st.session_state["generated_text"] = response.text
            st.session_state["user_name"] = name
            st.session_state["pdf_file"] = create_pdf(st.session_state["generated_text"], "resume_cover_letter.pdf")

            st.session_state["ats_analysis_text"] = None
            st.session_state["ats_score"] = None

            # Optional ATS Analysis
            if job_description:
                loader_slot.markdown("""
                <div class="fullscreen-loader-overlay">
                    <div class="loader-ring"></div>
                    <div class="loader-title">Scanning ATS Compatibility</div>
                    <div class="loader-sub">[ Calculating Keyword Match & Score Breakdown ]</div>
                </div>
                """, unsafe_allow_html=True)

                ats_prompt = f"""
                Analyze the candidate profile against the job description.

                Return ONLY in this format:

                ATS SCORE: XX

                # MISSING SKILLS
                - Skill 1
                - Skill 2

                # STRENGTHS
                - Strength 1
                - Strength 2

                # IMPROVEMENT SUGGESTIONS
                - Suggestion 1
                - Suggestion 2

                Candidate Details:
                Name: {name}
                Skills: {skills}
                Education: {education}
                Experience: {experience}

                Job Description:
                {job_description}
                """

                ats_response = model.generate_content(ats_prompt)
                st.session_state["ats_analysis_text"] = ats_response.text

                score_match = re.search(r"ATS SCORE[: ]+(\d+)", st.session_state["ats_analysis_text"], re.IGNORECASE)
                if score_match:
                    st.session_state["ats_score"] = int(score_match.group(1))

            # Clear Fullscreen Loader
            loader_slot.empty()
            st.balloons()
            st.success("⚡ Generation Complete!")

        except Exception as e:
            st.error("❌ Network or API error occurred.")
            st.error(str(e))

# Render Results persistent across session updates (like clicking download buttons)
if st.session_state["generated_text"] is not None:
    st.markdown("---")
    
    if st.session_state["ats_analysis_text"]:
        tab1, tab2 = st.tabs(["📄 Generated Assets", "🎯 ATS Intelligence Report"])
    else:
        tab1, tab2 = st.tabs(["📄 Generated Assets"], [None])

    with tab1:
        st.markdown('<div class="output-glass-box">', unsafe_allow_html=True)
        st.markdown(st.session_state["generated_text"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Safe File Read from Session PDF
        if st.session_state["pdf_file"]:
            with open(st.session_state["pdf_file"], "rb") as file:
                file_bytes = file.read()
                
            file_name_clean = st.session_state["user_name"].replace(" ", "_")
            st.download_button(
                label="📥 Download PDF Document",
                data=file_bytes,
                file_name=f"{file_name_clean}_Resume.pdf",
                mime="application/pdf"
            )

    if st.session_state["ats_analysis_text"]:
        with tab2:
            st.markdown('<div class="output-glass-box">', unsafe_allow_html=True)
            if st.session_state["ats_score"] is not None:
                st.markdown(f"### ATS Compatibility Index: **{st.session_state['ats_score']}%**")
                st.progress(st.session_state["ats_score"] / 100.0)
            
            st.markdown("---")
            st.markdown(st.session_state["ats_analysis_text"])
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button(
                label="📥 Download ATS Report (.txt)",
                data=st.session_state["ats_analysis_text"],
                file_name="ATS_Report.txt",
                mime="text/plain"
            )