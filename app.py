import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util
import re

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Job Matching Portal",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------
st.markdown("""
<style>

.main {
    background-color: #f7f8fc;
}

.hero {
    padding: 30px;
    border-radius: 18px;
    margin-bottom: 25px;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    text-align: center;
}

.hero h1 {
    font-size: 38px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 17px;
    margin-top: 0;
}

.section-title {
    font-size: 25px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 15px;
}

.score-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    border: 1px solid #eeeeee;
}

.score-number {
    font-size: 34px;
    font-weight: 800;
    color: #667eea;
}

.score-label {
    font-size: 14px;
    color: #666;
    margin-top: 5px;
}

.small-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}

.small-number {
    font-size: 28px;
    font-weight: 700;
    color: #764ba2;
}

.skill-chip {
    display: inline-block;
    padding: 8px 14px;
    margin: 5px;
    border-radius: 20px;
    background: #e8f5e9;
    color: #237a35;
    font-weight: 600;
    font-size: 14px;
}

.missing-chip {
    display: inline-block;
    padding: 8px 14px;
    margin: 5px;
    border-radius: 20px;
    background: #fff0f0;
    color: #d63333;
    font-weight: 600;
    font-size: 14px;
}

.gap-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 12px;
    border-left: 5px solid #667eea;
    box-shadow: 0 3px 10px rgba(0,0,0,0.06);
}

.roadmap-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 12px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}

.roadmap-number {
    font-size: 24px;
    font-weight: 800;
    color: #667eea;
}

.summary-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown("""
<div class="hero">
    <h1>🤖 AI Job Matching Portal</h1>
    <p>AI-powered Resume & Job Compatibility Analysis</p>
</div>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# SKILLS DATABASE
# ---------------------------------------------------------
SKILLS = [
    "Python", "Java", "C++", "SQL", "MySQL", "Oracle", "PostgreSQL",
    "Machine Learning", "Deep Learning", "Artificial Intelligence",
    "Generative AI", "Data Science", "Data Analysis", "Statistics",
    "Classification", "Regression", "Data Preprocessing",
    "Model Evaluation", "Power BI", "Excel", "Git", "GitHub",
    "Jupyter Notebook", "AWS", "Amazon Rekognition", "Amazon S3",
    "HTML", "CSS", "JavaScript", "Prompt Engineering", "LLM",
    "Computer Vision", "Natural Language Processing", "TensorFlow",
    "PyTorch"
]


# ---------------------------------------------------------
# ALIASES
# ---------------------------------------------------------
ALIASES = {
    "sql": ["sql", "mysql", "oracle", "postgresql"],

    "machine learning": [
        "machine learning",
        "classification",
        "regression",
        "data preprocessing",
        "model evaluation"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai",
        "machine learning",
        "deep learning"
    ],

    "data science": [
        "data science",
        "data analysis",
        "statistics",
        "machine learning"
    ],

    "generative ai": [
        "generative ai",
        "prompt engineering",
        "llm"
    ],

    "cloud": [
        "aws",
        "amazon s3",
        "amazon rekognition"
    ]
}


# ---------------------------------------------------------
# LEARNING MAP
# ---------------------------------------------------------
learning_map = {

    "Python": (
        "Practice Python programming, functions, OOP, file handling "
        "and libraries such as NumPy and Pandas."
    ),

    "SQL": (
        "Learn SELECT, JOIN, GROUP BY, subqueries, aggregate functions "
        "and database queries."
    ),

    "Machine Learning": (
        "Study supervised and unsupervised learning, model training, "
        "evaluation and basic ML algorithms."
    ),

    "Data Science": (
        "Learn data collection, preprocessing, exploratory data analysis, "
        "visualization and machine learning."
    ),

    "Data Analysis": (
        "Practice Pandas, NumPy, data cleaning, EDA and visualization."
    ),

    "Statistics": (
        "Learn probability, distributions, hypothesis testing, "
        "mean, variance and statistical interpretation."
    ),

    "Power BI": (
        "Practice dashboards, data modeling, Power Query, DAX and "
        "interactive visualizations."
    ),

    "Deep Learning": (
        "Learn neural networks, CNNs, RNNs and deep learning workflows."
    ),

    "AWS": (
        "Learn basic AWS services such as EC2, S3, IAM and cloud deployment."
    ),

    "GitHub": (
        "Practice repositories, commits, branches, pull requests and "
        "collaborative development."
    ),

    "Jupyter Notebook": (
        "Practice Python-based data analysis and machine learning "
        "experiments using Jupyter Notebook."
    ),

    "Computer Vision": (
        "Learn image processing, OpenCV, object detection and "
        "computer vision fundamentals."
    ),

    "Natural Language Processing": (
        "Learn text preprocessing, tokenization, embeddings, NLP models "
        "and text classification."
    ),

    "TensorFlow": (
        "Practice building and training neural network models using TensorFlow."
    ),

    "PyTorch": (
        "Learn tensors, neural networks, model training and deep learning "
        "using PyTorch."
    ),

    "Java": (
        "Practice OOP, collections, exception handling and Java application development."
    ),

    "C++": (
        "Practice OOP, STL, data structures and algorithm implementation."
    ),

    "HTML": (
        "Learn HTML5 structure, forms, tables and semantic elements."
    ),

    "CSS": (
        "Practice responsive layouts, Flexbox, Grid and modern CSS styling."
    ),

    "JavaScript": (
        "Learn JavaScript fundamentals, DOM manipulation and web interactions."
    ),

    "Excel": (
        "Practice formulas, pivot tables, charts and data analysis."
    ),

    "Generative AI": (
        "Learn LLM concepts, prompt engineering, embeddings and generative AI applications."
    ),

    "Prompt Engineering": (
        "Practice writing effective prompts, role prompting, structured outputs "
        "and prompt optimization."
    ),

    "LLM": (
        "Learn transformer-based language models, embeddings and LLM applications."
    ),

    "Artificial Intelligence": (
        "Study AI fundamentals, intelligent systems, machine learning "
        "and deep learning."
    ),

    "Classification": (
        "Practice classification algorithms such as Logistic Regression, "
        "Decision Trees, Random Forest and evaluation metrics."
    ),

    "Regression": (
        "Learn linear regression, polynomial regression and regression evaluation metrics."
    ),

    "Data Preprocessing": (
        "Practice handling missing values, encoding, scaling, outlier treatment "
        "and feature preparation."
    ),

    "Model Evaluation": (
        "Learn accuracy, precision, recall, F1-score, confusion matrix "
        "and cross-validation."
    )
}


# ---------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------
def extract_text_from_pdf(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def normalize_text(text):

    text = text.lower()

    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text


def contains_skill(text, skill):

    text = normalize_text(text)

    skill = normalize_text(skill)

    pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"

    return bool(re.search(pattern, text))


def extract_skills(text):

    detected = []

    for skill in SKILLS:

        if contains_skill(text, skill):
            detected.append(skill)

    return sorted(set(detected))


def skill_matches(resume_text, job_text, skill):

    resume_normalized = normalize_text(resume_text)
    job_normalized = normalize_text(job_text)

    skill_key = skill.lower()

    # Direct matching
    if contains_skill(resume_text, skill) and contains_skill(job_text, skill):
        return True

    # Alias matching
    if skill_key in ALIASES:

        for alias in ALIASES[skill_key]:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(normalize_text(alias))
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, resume_normalized):

                for job_alias in ALIASES[skill_key]:

                    job_pattern = (
                        r"(?<![a-z0-9])"
                        + re.escape(normalize_text(job_alias))
                        + r"(?![a-z0-9])"
                    )

                    if re.search(job_pattern, job_normalized):
                        return True

    return False


def get_job_relevant_skills(job_text):

    return extract_skills(job_text)


def calculate_skill_match(resume_text, job_text):

    job_skills = get_job_relevant_skills(job_text)

    matched = []
    missing = []

    for skill in job_skills:

        if skill_matches(resume_text, job_text, skill):
            matched.append(skill)
        else:
            missing.append(skill)

    if len(job_skills) == 0:
        return 0, matched, missing, job_skills

    score = (len(matched) / len(job_skills)) * 100

    return score, matched, missing, job_skills


# ---------------------------------------------------------
# MODEL
# ---------------------------------------------------------
@st.cache_resource
def load_model():

    return SentenceTransformer("all-MiniLM-L6-v2")


# ---------------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------------
st.markdown(
    '<div class="section-title">📥 Resume & Job Details</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    uploaded_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"]
    )

with col2:

    job_description = st.text_area(
        "Paste Complete Job Description",
        height=230,
        placeholder="Paste the complete job description here..."
    )


# ---------------------------------------------------------
# ANALYSIS
# ---------------------------------------------------------
if uploaded_file and job_description.strip():

    with st.spinner("🔍 Analyzing resume and job description..."):

        # Extract resume
        resume_text = extract_text_from_pdf(uploaded_file)

        # Resume skills
        resume_skills = extract_skills(resume_text)

        # Job skill matching
        skill_score, matched_skills, missing_skills, job_skills = (
            calculate_skill_match(
                resume_text,
                job_description
            )
        )

        # Semantic AI similarity
        model = load_model()

        resume_embedding = model.encode(
            resume_text,
            convert_to_tensor=True
        )

        job_embedding = model.encode(
            job_description,
            convert_to_tensor=True
        )

        semantic_score = float(
            util.cos_sim(
                resume_embedding,
                job_embedding
            )[0][0]
        ) * 100

        semantic_score = max(
            0,
            min(100, semantic_score)
        )

        # Final score
        final_score = (
            skill_score * 0.70
            + semantic_score * 0.30
        )

    # -----------------------------------------------------
    # RESULT CATEGORY
    # -----------------------------------------------------
    if final_score >= 75:
        result_text = "Strong Match"
        result_icon = "🟢"

    elif final_score >= 50:
        result_text = "Moderate Match"
        result_icon = "🟡"

    else:
        result_text = "Needs Improvement"
        result_icon = "🔴"


    # -----------------------------------------------------
    # DASHBOARD
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">📊 Job Match Dashboard</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{final_score:.1f}%</div>
            <div class="score-label">Overall Match</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{skill_score:.1f}%</div>
            <div class="score-label">Job Skill Match</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{semantic_score:.1f}%</div>
            <div class="score-label">AI Semantic Match</div>
        </div>
        """, unsafe_allow_html=True)


    st.progress(
        int(final_score),
        text=f"{result_icon} {result_text}"
    )


    # -----------------------------------------------------
    # QUICK ANALYSIS
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">⚡ Quick Analysis</div>',
        unsafe_allow_html=True
    )

    q1, q2, q3 = st.columns(3)

    with q1:
        st.markdown(f"""
        <div class="small-card">
            <div class="small-number">{len(matched_skills)}</div>
            <div>✅ Matched Skills</div>
        </div>
        """, unsafe_allow_html=True)

    with q2:
        st.markdown(f"""
        <div class="small-card">
            <div class="small-number">{len(missing_skills)}</div>
            <div>🚀 Skills to Learn</div>
        </div>
        """, unsafe_allow_html=True)

    with q3:
        st.markdown(f"""
        <div class="small-card">
            <div class="small-number">{len(job_skills)}</div>
            <div>🎯 Job Required Skills</div>
        </div>
        """, unsafe_allow_html=True)


    # -----------------------------------------------------
    # MATCHED SKILLS
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">✅ Your Matching Skills</div>',
        unsafe_allow_html=True
    )

    if matched_skills:

        matched_html = ""

        for skill in matched_skills:

            matched_html += (
                f'<span class="skill-chip">✓ {skill}</span>'
            )

        st.markdown(
            matched_html,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No matching job skills were found in the resume."
        )


    # -----------------------------------------------------
    # MISSING SKILLS
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">🚀 Skills Required for This Job</div>',
        unsafe_allow_html=True
    )

    if missing_skills:

        missing_html = ""

        for skill in missing_skills:

            missing_html += (
                f'<span class="missing-chip">+ {skill}</span>'
            )

        st.markdown(
            missing_html,
            unsafe_allow_html=True
        )

    else:

        st.success(
            "🎉 Your resume contains all the detected job-required skills!"
        )


    # -----------------------------------------------------
    # DETAILED SKILL DETECTION
    # -----------------------------------------------------
    with st.expander("📋 View Detailed Skill Detection"):

        st.write(
            "**Skills detected from Resume:**"
        )

        st.write(
            ", ".join(resume_skills)
            if resume_skills
            else "No skills detected"
        )

        st.write(
            "**Skills detected from Job Description:**"
        )

        st.write(
            ", ".join(job_skills)
            if job_skills
            else "No job skills detected"
        )


    # -----------------------------------------------------
    # AI MATCHING INSIGHTS
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">🧠 AI Matching Insights</div>',
        unsafe_allow_html=True
    )

    i1, i2 = st.columns(2)

    with i1:

        st.info(
            f"""
            **Skill-Based Analysis**

            The resume matches **{len(matched_skills)}**
            out of **{len(job_skills)}** detected job skills.

            Skill Match: **{skill_score:.1f}%**
            """
        )

    with i2:

        st.info(
            f"""
            **Semantic AI Analysis**

            The AI model compares the overall meaning and
            context of the resume and job description.

            Semantic Match: **{semantic_score:.1f}%**
            """
        )


    # -----------------------------------------------------
    # AI SKILL GAP ANALYSIS
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">🧠 AI Skill Gap Analysis</div>',
        unsafe_allow_html=True
    )

    if missing_skills:

        for skill in missing_skills:

            recommendation = learning_map.get(
                skill,
                f"Learn the fundamentals of {skill} and practice it through a small project."
            )

            with st.expander(
                f"📘 {skill} — Recommended Learning"
            ):

                st.markdown(
                    f"""
                    <div class="gap-card">
                        <h4>How to improve</h4>
                        <p>{recommendation}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    else:

        st.success(
            "No major skill gaps detected for this job description."
        )


    # -----------------------------------------------------
    # CAREER ROADMAP
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">🎯 Career Preparation Roadmap</div>',
        unsafe_allow_html=True
    )

    if missing_skills:

        for index, skill in enumerate(
            missing_skills,
            start=1
        ):

            recommendation = learning_map.get(
                skill,
                f"Study {skill} and complete a practical project."
            )

            st.markdown(
                f"""
                <div class="roadmap-card">
                    <span class="roadmap-number">
                        Step {index}
                    </span>

                    <h3>Learn {skill}</h3>

                    <p>{recommendation}</p>

                    <b>🎯 Goal:</b>
                    Build practical knowledge and add a project
                    demonstrating this skill.
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.success(
            "🎉 You already match all detected job-required skills. "
            "Focus on projects, interview preparation and practical experience."
        )


    # -----------------------------------------------------
    # RESUME SUMMARY
    # -----------------------------------------------------
    st.markdown(
        '<div class="section-title">📄 Resume Analysis Summary</div>',
        unsafe_allow_html=True
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        st.markdown(f"""
        <div class="summary-card">
            <h2>{len(resume_skills)}</h2>
            <p>Resume Skills</p>
        </div>
        """, unsafe_allow_html=True)

    with s2:

        st.markdown(f"""
        <div class="summary-card">
            <h2>{len(job_skills)}</h2>
            <p>Job Skills</p>
        </div>
        """, unsafe_allow_html=True)

    with s3:

        st.markdown(f"""
        <div class="summary-card">
            <h2>{len(matched_skills)}</h2>
            <p>Skills Matched</p>
        </div>
        """, unsafe_allow_html=True)

    with s4:

        st.markdown(f"""
        <div class="summary-card">
            <h2>{len(missing_skills)}</h2>
            <p>Skills to Improve</p>
        </div>
        """, unsafe_allow_html=True)


# ---------------------------------------------------------
# WAITING MESSAGE
# ---------------------------------------------------------
elif uploaded_file is None:

    st.info(
        "👆 Upload your resume PDF to start the analysis."
    )

elif not job_description.strip():

    st.info(
        "📝 Paste the complete job description to compare your resume."
    )