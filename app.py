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
    page_title="AI Resume & Cover Letter Generator",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

/* Animated Background */
.stApp {
    background: linear-gradient(-45deg,#0f172a,#1e293b,#312e81,#0f172a);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

@keyframes gradientBG {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

/* Hero */
.hero-title{
    text-align:center;
    font-size:4rem;
    font-weight:900;
    background:linear-gradient(90deg,#00e5ff,#8b5cf6,#ff4ecd);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.hero-sub{
    text-align:center;
    color:#d1d5db;
    font-size:1.2rem;
    margin-bottom:30px;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#0b1120;
}

/* Inputs */
.stTextInput input,
.stTextArea textarea{
    border-radius:15px !important;
    border:2px solid #38bdf8 !important;
}

/* Button */
.stButton button{
    width:100%;
    height:60px;
    border-radius:18px;
    font-size:18px;
    font-weight:bold;
    border:none;
    color:white;
    background:linear-gradient(
        90deg,
        #00e5ff,
        #8b5cf6,
        #ff4ecd
    );
}

.stButton button:hover{
    transform:scale(1.03);
    transition:.3s;
}

/* Result */
.result-box{
    background:rgba(255,255,255,.08);
    backdrop-filter:blur(20px);
    border-radius:20px;
    padding:25px;
    border-left:5px solid #00e5ff;
    margin-top:20px;
}

</style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.header("🚀 Features")

    st.success("Resume Generator")
    st.success("Cover Letter Generator")
    st.success("ATS Score Checker")
    st.success("PDF Download")

    st.markdown("---")

    st.info("Powered by Gemini AI")

# Main Title
st.markdown("""
<h1 class="hero-title">
🤖 AI Resume Studio
</h1>

<p class="hero-sub">
Create ATS-Friendly Resumes, Cover Letters & Career Insights with AI
</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("⚡ AI Model", "Gemini")

with col2:
    st.metric("📄 Documents", "Resume + Cover")

with col3:
    st.metric("🎯 ATS Analysis", "Enabled")

st.markdown("---")
st.markdown("<br>", unsafe_allow_html=True)
# User Inputs
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("👤 Full Name")
    skills = st.text_area("🛠 Skills")
    education = st.text_area("🎓 Education")

with col2:
    experience = st.text_area("💼 Experience")
    job_description = st.text_area("📄 Job Description (Optional)")
# Generate Button
if st.button("🚀 Generate"):

    if not name or not skills or not education or not experience:
        st.warning("⚠️ Please fill all required fields.")
    else:
        try:

            with st.spinner("Generating Resume and Cover Letter..."):

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

                generated_text = response.text

            # Display Output
            st.subheader("📄 Generated Resume & Cover Letter")
            st.markdown(generated_text)
            
            # PDF Creation
            pdf_file = create_pdf(
                generated_text,
                "resume_cover_letter.pdf"
            )

            # Download Button
            with open(pdf_file, "rb") as file:
                st.download_button(
                    label="📥 Download PDF",
                    data=file,
                    file_name="resume_cover_letter.pdf",
                    mime="application/pdf"
                )
            st.balloons()
            st.success("✅ Resume and Cover Letter generated successfully!")

            # ATS Analysis
            if job_description:

                with st.spinner("Analyzing ATS Compatibility..."):

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

                    ats_response = model.generate_content(
                        ats_prompt
                    )

                    # ATS Score Progress Bar
                    score_match = re.search(
                        r"ATS SCORE[: ]+(\d+)",
                        ats_response.text,
                        re.IGNORECASE
                    )

                    if score_match:
                        score = int(score_match.group(1))

                        st.subheader("🎯 ATS Score")
                        st.progress(score)
                        st.metric("ATS Score", f"{score}/100")

                    st.subheader("📊 ATS Analysis")
                    st.markdown(ats_response.text)

                st.download_button(
                    label="📥 Download ATS Report",
                    data=ats_response.text,
                    file_name="ats_report.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(
                "❌ API limit reached or an error occurred. Please wait and try again."
            )
            st.error(str(e))