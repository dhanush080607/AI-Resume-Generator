# ⚡ AI Resume Studio

An AI-powered Resume and Cover Letter Generator built with **Python, Streamlit, and Google Gemini AI**.

AI Resume Studio helps users create professional, ATS-friendly resume summaries and cover letters from their personal information. It also provides an optional ATS compatibility analysis by comparing the candidate's profile with a target job description.

🌐 **Live Demo:** https://ai-resume-generator-project.streamlit.app/

---

## 🚀 Features

### 📄 AI Resume Summary Generation

Generate a concise and professional resume summary using your:

* Name
* Skills
* Education
* Work experience

### ✉️ AI Cover Letter Generation

Automatically generate a professional, ready-to-use cover letter based on the candidate information provided.

### 🎯 ATS Compatibility Analysis

Paste a target job description to receive an AI-powered analysis containing:

* ATS Compatibility Score
* Missing Skills
* Candidate Strengths
* Improvement Suggestions

### 📥 PDF Resume Export

Download your generated resume and cover letter as a PDF document.

### 📊 ATS Report Download

Download your ATS analysis as a `.txt` file for future reference.

### 🎨 Modern Cyberpunk UI

The application features a modern glassmorphism and cyberpunk-inspired interface with:

* Animated loading screen
* Gradient UI elements
* Glass-style cards
* Responsive Streamlit layout
* Dark futuristic design

---

## 🛠️ Tech Stack

| Technology          | Purpose                                |
| ------------------- | -------------------------------------- |
| Python              | Application development                |
| Streamlit           | Web application framework              |
| Google Gemini AI    | Resume, cover letter, and ATS analysis |
| ReportLab           | PDF document generation                |
| Regular Expressions | ATS score extraction                   |
| HTML & CSS          | Custom user interface                  |

---

## 📂 Project Structure

```text
AI-Resume-Generator/
│
├── app.py
├── pdf_generator.py
├── requirements.txt
├── .gitignore
└── README.md
```

### File Description

* `app.py` — Main Streamlit application and AI generation logic
* `pdf_generator.py` — Generates downloadable PDF documents
* `requirements.txt` — Contains required Python dependencies
* `.gitignore` — Prevents sensitive and unnecessary files from being uploaded
* `README.md` — Project documentation

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Resume-Generator.git
```

### 2. Navigate to the Project

```bash
cd AI-Resume-Generator
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Configuration

This project uses the **Google Gemini API**.

For local development, configure your Gemini API key using your preferred secure method.

For Streamlit Community Cloud deployment, add your API key to Streamlit Secrets:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
```

⚠️ **Never commit your API key to GitHub.**

Make sure sensitive files such as `secret.py` and `.streamlit/secrets.toml` are included in `.gitignore`.

---

## ▶️ Run Locally

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🧑‍💻 How to Use

1. Open the AI Resume Studio application.
2. Enter your full name.
3. Add your skills and technical stack.
4. Enter your education and credentials.
5. Add your work experience and highlights.
6. Optionally paste a target job description.
7. Click **Initialize Generation Process**.
8. Wait for Gemini AI to generate your resume summary and cover letter.
9. Download your generated PDF.
10. If a job description was provided, review your ATS compatibility report.
11. Download the ATS report if required.

---

## 🎯 ATS Analysis

When a job description is provided, the application analyzes the candidate profile against the target role.

The ATS analysis provides:

```text
ATS SCORE

MISSING SKILLS

STRENGTHS

IMPROVEMENT SUGGESTIONS
```

The ATS score is extracted from the AI-generated response and displayed as a percentage inside the application.

---

## ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

🌐 **Live Application:**

https://ai-resume-generator-project.streamlit.app/

To deploy your own version:

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select `app.py` as the main file.
5. Add `GEMINI_API_KEY` under Streamlit Secrets.
6. Deploy the application.

---

## 🔐 Security

The Gemini API key is a private credential.

Do not:

* Commit API keys to GitHub
* Share API keys publicly
* Add API keys directly to `app.py`
* Upload `secret.py` if it contains your API key

Use environment variables or Streamlit Secrets to manage sensitive credentials.

---

## 🔮 Future Improvements

Planned improvements may include:

* Full AI-generated resume sections
* Multiple professional resume templates
* Custom resume themes
* Job-specific resume optimization
* LinkedIn profile optimization
* Resume keyword recommendations
* Resume scoring improvements
* DOCX export
* Resume history and saved profiles
* User authentication
* Database integration
* Improved ATS keyword matching

---

## 👨‍💻 Author

**Dhanush**

Computer Science & Engineering — Data Science

Interested in:

* Artificial Intelligence
* Machine Learning
* Data Science
* Full-Stack Development
* AI-Powered Applications

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---

## 📜 License

This project is created for educational and portfolio purposes.
