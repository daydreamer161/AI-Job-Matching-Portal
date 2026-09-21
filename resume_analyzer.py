import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer, util
import re

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="AI Job Matching Portal",
    page_icon="🤖",
    layout="wide"
)

# =========================================================
# CUSTOM CSS — UI ONLY
# =========================================================
st.markdown("""
<style>

.stApp {
    background: #f6f7fb;
}

/* Remove extra top space */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* =====================================================
   HERO
   ===================================================== */
.hero {
    background: linear-gradient(135deg, #5b5ce2 0%, #7b4bb7 55%, #9333a8 100%);
    padding: 42px 35px;
    border-radius: 26px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 15px 35px rgba(91,92,226,0.22);
}

.hero h1 {
    font-size: 42px;
    margin: 0;
    font-weight: 850;
    letter-spacing: -1px;
}

.hero p {
    font-size: 17px;
    margin-top: 10px;
    opacity: 0.92;
}

/* =====================================================
   SECTION TITLES
   ===================================================== */
.section-title {
    font-size: 26px;
    font-weight: 800;
    color: #202124;
    margin-top: 32px;
    margin-bottom: 17px;
}

/* =====================================================
   INPUT AREA
   ===================================================== */
.input-card {
    background: white;
    padding: 22px;
    border-radius: 20px;
    border: 1px solid #e8e8f0;
    box-shadow: 0 7px 22px rgba(0,0,0,0.05);
}

/* =====================================================
   SCORE CARDS
   ===================================================== */
.score-card {
    background: white;
    padding: 27px 20px;
    border-radius: 22px;
    text-align: center;
    border: 1px solid #e8e8f0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.06);
    transition: transform 0.2s ease;
}

.score-card:hover {
    transform: translateY(-3px);
}

.score-number {
    font-size: 40px;
    font-weight: 850;
    background: linear-gradient(135deg, #5b5ce2, #9333a8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.score-label {
    color: #6b7280;
    font-size: 14px;
    font-weight: 650;
    margin-top: 6px;
}

/* =====================================================
   RESULT BANNER
   ===================================================== */
.result-banner {
    margin-top: 18px;
    padding: 17px 22px;
    background: white;
    border-radius: 18px;
    border: 1px solid #e8e8f0;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    text-align: center;
    font-size: 17px;
    font-weight: 750;
    color: #343434;
}

/* =====================================================
   SKILL SECTION CONTAINER
   ===================================================== */
.skill-box {
    background: white;
    padding: 27px;
    border-radius: 24px;
    min-height: 285px;
    border: 1px solid #e8e8f0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.055);
}

.skill-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}

.skill-header h2 {
    margin: 0;
    font-size: 21px;
    font-weight: 800;
}

.skill-description {
    color: #737780;
    font-size: 14px;
    margin-bottom: 20px;
}

/* =====================================================
   SKILL COUNT
   ===================================================== */
.skill-count {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 750;
    margin-left: auto;
}

.match-count {
    background: #e7f8ee;
    color: #138a4b;
}

.gap-count {
    background: #fff0f1;
    color: #d73545;
}

/* =====================================================
   SKILL CHIPS
   ===================================================== */
.match-chip {
    display: inline-block;
    background: linear-gradient(135deg, #e9faef, #dff6e8);
    color: #147a43;
    padding: 10px 15px;
    margin: 5px 4px;
    border-radius: 13px;
    font-size: 13px;
    font-weight: 700;
    border: 1px solid #c9ebd5;
    box-shadow: 0 3px 8px rgba(25,135,84,0.07);
}

.gap-chip {
    display: inline-block;
    background: linear-gradient(135deg, #fff3f3, #ffe9eb);
    color: #c92f40;
    padding: 10px 15px;
    margin: 5px 4px;
    border-radius: 13px;
    font-size: 13px;
    font-weight: 700;
    border: 1px solid #f3ced2;
    box-shadow: 0 3px 8px rgba(220,53,69,0.07);
}

/* =====================================================
   AI INSIGHTS
   ===================================================== */
.insight-card {
    background: white;
    padding: 26px;
    border-radius: 22px;
    border: 1px solid #e8e8f0;
    box-shadow: 0 8px 25px rgba(0,0,0,0.055);
    min-height: 190px;
}

.insight-icon {
    font-size: 30px;
    margin-bottom: 7px;
}

.insight-title {
    font-size: 18px;
    font-weight: 800;
    color: #242424;
    margin-bottom: 8px;
}

.insight-score {
    font-size: 30px;
    font-weight: 850;
    color: #6257d9;
    margin-top: 12px;
}

.insight-text {
    color: #6b7280;
    line-height: 1.55;
    font-size: 14px;
}

/* =====================================================
   AI GAP ANALYSIS
   ===================================================== */
.ai-intro {
    background: linear-gradient(135deg, #f1efff, #faf9ff);
    padding: 19px 22px;
    border-radius: 18px;
    border: 1px solid #e3defc;
    color: #5b5875;
    margin-bottom: 18px;
}

.ai-card {
    background: linear-gradient(135deg, #ffffff, #faf9ff);
    padding: 22px;
    border-radius: 18px;
    border-left: 5px solid #6759d8;
    box-shadow: 0 6px 18px rgba(0,0,0,0.055);
    margin: 8px 0;
}

.ai-card h4 {
    margin-top: 0;
    color: #292929;
    font-size: 17px;
}

.ai-card p {
    color: #666b75;
    line-height: 1.65;
}

.practice-box {
    background: #f0edff;
    padding: 12px 15px;
    border-radius: 12px;
    margin-top: 14px;
    color: #5c54a5;
    font-size: 13px;
}

/* =====================================================
   ROADMAP
   ===================================================== */
.roadmap-intro {
    background: linear-gradient(135deg, #f8f7ff, #ffffff);
    padding: 19px 22px;
    border-radius: 18px;
    border: 1px solid #e5e1fb;
    color: #666;
    margin-bottom: 18px;
}

.roadmap-card {
    background: white;
    padding: 21px;
    border-radius: 19px;
    margin-bottom: 13px;
    border: 1px solid #e8e8f0;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
}

.step-circle {
    min-width: 47px;
    height: 47px;
    border-radius: 50%;
    background: linear-gradient(135deg, #5b5ce2, #8c4fc0);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 850;
    font-size: 17px;
    box-shadow: 0 6px 15px rgba(91,92,226,0.20);
}

.roadmap-title {
    font-size: 17px;
    font-weight: 800;
    color: #292929;
    margin-bottom: 5px;
}

.roadmap-text {
    color: #6b7280;
    font-size: 14px;
    line-height: 1.55;
}

.roadmap-action {
    margin-top: 11px;
    color: #6257d9;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.2px;
}

/* =====================================================
   SUCCESS BOX
   ===================================================== */
.success-box {
    background: linear-gradient(135deg, #ecfaf1, #ffffff);
    padding: 22px;
    border-radius: 19px;
    text-align: center;
    border: 1px solid #d1ecd9;
    margin-top: 20px;
    color: #187443;
    font-weight: 650;
}

/* =====================================================
   STREAMLIT EXPANDER
   ===================================================== */
[data-testid="stExpander"] {
    border: none !important;
    background: transparent !important;
}

/* =====================================================
   INFO MESSAGE
   ===================================================== */
.stAlert {
    border-radius: 15px;
}

/* =====================================================
   TEXT AREA
   ===================================================== */
textarea {
    border-radius: 12px !important;
}

/* =====================================================
   FOOTER
   ===================================================== */
.footer {
    margin-top: 45px;
    text-align: center;
    color: #9a9aa2;
    font-size: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <h1>🤖 AI Job Matching Portal</h1>
    <p>AI-powered Resume & Job Compatibility Analysis</p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# SKILLS DATABASE
# =========================================================
SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "MySQL",
    "Oracle",
    "PostgreSQL",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Generative AI",
    "Data Science",
    "Data Analysis",
    "Statistics",
    "Classification",
    "Regression",
    "Data Preprocessing",
    "Model Evaluation",
    "Power BI",
    "Excel",
    "Git",
    "GitHub",
    "Jupyter Notebook",
    "AWS",
    "Amazon Rekognition",
    "Amazon S3",
    "HTML",
    "CSS",
    "JavaScript",
    "Prompt Engineering",
    "LLM",
    "Computer Vision",
    "Natural Language Processing",
    "TensorFlow",
    "PyTorch"
]


# =========================================================
# ALIASES
# =========================================================
ALIASES = {
    "sql": [
        "sql",
        "mysql",
        "oracle",
        "postgresql"
    ],

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


# =========================================================
# LEARNING MAP
# =========================================================
learning_map = {

    "Python":
        "Practice Python programming, functions, OOP, NumPy and Pandas.",

    "SQL":
        "Learn SELECT, JOIN, GROUP BY, subqueries and database queries.",

    "Machine Learning":
        "Study supervised and unsupervised learning, model training and evaluation.",

    "Data Science":
        "Learn data preprocessing, EDA, visualization and machine learning.",

    "Data Analysis":
        "Practice Pandas, NumPy, data cleaning, EDA and visualization.",

    "Statistics":
        "Learn probability, distributions, hypothesis testing and statistical analysis.",

    "Power BI":
        "Practice dashboards, Power Query, DAX and interactive visualizations.",

    "Deep Learning":
        "Learn neural networks, CNNs, RNNs and deep learning frameworks.",

    "AWS":
        "Learn AWS cloud basics including S3, EC2, IAM and deployment.",

    "Git":
        "Practice repositories, commits, branches and version control.",

    "GitHub":
        "Practice repositories, pull requests, collaboration and project management.",

    "Jupyter Notebook":
        "Practice data analysis and machine learning experiments using Jupyter Notebook.",

    "Computer Vision":
        "Learn image processing, OpenCV, object detection and computer vision fundamentals.",

    "Natural Language Processing":
        "Learn text processing, tokenization, embeddings and NLP models.",

    "TensorFlow":
        "Practice building and training neural network models using TensorFlow.",

    "PyTorch":
        "Learn tensors, neural networks, model training and deep learning using PyTorch.",

    "Java":
        "Practice OOP, collections, exception handling and Java development.",

    "C++":
        "Practice OOP, STL, data structures and algorithms.",

    "HTML":
        "Learn HTML5 structure, forms, tables and semantic elements.",

    "CSS":
        "Practice responsive layouts, Flexbox, Grid and modern CSS.",

    "JavaScript":
        "Learn JavaScript fundamentals, DOM manipulation and web interactions.",

    "Excel":
        "Practice formulas, pivot tables, charts and data analysis.",

    "Generative AI":
        "Learn LLM concepts, prompt engineering, embeddings and GenAI applications.",

    "Prompt Engineering":
        "Practice effective prompts, structured outputs and prompt optimization.",

    "LLM":
        "Learn transformer models, embeddings and LLM applications.",

    "Artificial Intelligence":
        "Study AI fundamentals, intelligent systems, machine learning and deep learning.",

    "Classification":
        "Practice Logistic Regression, Decision Trees, Random Forest and evaluation metrics.",

    "Regression":
        "Learn linear regression, polynomial regression and regression evaluation.",

    "Data Preprocessing":
        "Practice missing values, encoding, scaling, outlier treatment and feature preparation.",

    "Model Evaluation":
        "Learn accuracy, precision, recall, F1-score and cross-validation."
}


# =========================================================
# FUNCTIONS
# =========================================================
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

    text = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


def contains_skill(text, skill):

    text = normalize_text(text)

    skill = normalize_text(skill)

    pattern = (
        r"(?<![a-z0-9])"
        + re.escape(skill)
        + r"(?![a-z0-9])"
    )

    return bool(
        re.search(pattern, text)
    )


def extract_skills(text):

    detected = []

    for skill in SKILLS:

        if contains_skill(text, skill):
            detected.append(skill)

    return sorted(
        set(detected)
    )


def skill_matches(
    resume_text,
    job_text,
    skill
):

    resume_normalized = normalize_text(
        resume_text
    )

    job_normalized = normalize_text(
        job_text
    )

    skill_key = skill.lower()

    # Direct matching
    if (
        contains_skill(resume_text, skill)
        and
        contains_skill(job_text, skill)
    ):
        return True

    # Alias matching
    if skill_key in ALIASES:

        for alias in ALIASES[skill_key]:

            alias_pattern = (
                r"(?<![a-z0-9])"
                + re.escape(
                    normalize_text(alias)
                )
                + r"(?![a-z0-9])"
            )

            if re.search(
                alias_pattern,
                resume_normalized
            ):

                for job_alias in ALIASES[skill_key]:

                    job_pattern = (
                        r"(?<![a-z0-9])"
                        + re.escape(
                            normalize_text(job_alias)
                        )
                        + r"(?![a-z0-9])"
                    )

                    if re.search(
                        job_pattern,
                        job_normalized
                    ):
                        return True

    return False


def calculate_skill_match(
    resume_text,
    job_text
):

    # IMPORTANT:
    # Only skills detected in the JOB DESCRIPTION
    # are used for the matching result.

    job_skills = extract_skills(
        job_text
    )

    matched = []
    missing = []

    for skill in job_skills:

        if skill_matches(
            resume_text,
            job_text,
            skill
        ):
            matched.append(skill)

        else:
            missing.append(skill)

    if len(job_skills) == 0:

        return (
            0,
            matched,
            missing,
            job_skills
        )

    score = (
        len(matched)
        /
        len(job_skills)
    ) * 100

    return (
        score,
        matched,
        missing,
        job_skills
    )


# =========================================================
# LOAD AI MODEL
# =========================================================
@st.cache_resource
def load_model():

    return SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


# =========================================================
# INPUT SECTION
# =========================================================
st.markdown(
    '<div class="section-title">📥 Resume & Job Details</div>',
    unsafe_allow_html=True
)

input_col1, input_col2 = st.columns(2)

with input_col1:

    uploaded_file = st.file_uploader(
        "📄 Upload Resume PDF",
        type=["pdf"]
    )

with input_col2:

    job_description = st.text_area(
        "💼 Paste Complete Job Description",
        height=230,
        placeholder="Paste the complete job description here..."
    )


# =========================================================
# ANALYSIS
# =========================================================
if (
    uploaded_file
    and
    job_description.strip()
):

    with st.spinner(
        "🔍 Analyzing resume and job requirements..."
    ):

        # Resume text
        resume_text = extract_text_from_pdf(
            uploaded_file
        )

        # Resume skills
        resume_skills = extract_skills(
            resume_text
        )

        # Job-specific skill matching
        (
            skill_score,
            matched_skills,
            missing_skills,
            job_skills
        ) = calculate_skill_match(
            resume_text,
            job_description
        )

        # AI semantic model
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
            min(
                100,
                semantic_score
            )
        )

        # Final score
        final_score = (
            skill_score * 0.70
            +
            semantic_score * 0.30
        )


    # =====================================================
    # MATCH RESULT
    # =====================================================
    if final_score >= 75:

        result_text = "Strong Match"
        result_icon = "🟢"

    elif final_score >= 50:

        result_text = "Moderate Match"
        result_icon = "🟡"

    else:

        result_text = "Needs Improvement"
        result_icon = "🔴"


    # =====================================================
    # DASHBOARD
    # =====================================================
    st.markdown(
        '<div class="section-title">📊 Job Match Dashboard</div>',
        unsafe_allow_html=True
    )

    score1, score2, score3 = st.columns(3)

    with score1:

        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-number">
                    {final_score:.1f}%
                </div>
                <div class="score-label">
                    🎯 Overall Match
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with score2:

        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-number">
                    {skill_score:.1f}%
                </div>
                <div class="score-label">
                    🛠️ Job Skill Match
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with score3:

        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-number">
                    {semantic_score:.1f}%
                </div>
                <div class="score-label">
                    🧠 AI Semantic Match
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.progress(
        int(final_score)
    )

    st.markdown(
        f"""
        <div class="result-banner">
            {result_icon} &nbsp; {result_text}
            &nbsp;&nbsp;•&nbsp;&nbsp;
            AI-based compatibility analysis completed
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # MATCHED + GAPS
    # =====================================================
    st.markdown(
        '<div class="section-title">🎯 Job Skill Compatibility</div>',
        unsafe_allow_html=True
    )

    skill_col1, skill_col2 = st.columns(2)

    # ---------------- MATCHED SKILLS ----------------
    with skill_col1:

        st.markdown(
            f"""
            <div class="skill-box">

                <div class="skill-header">

                    <span style="font-size:28px;">✅</span>

                    <h2>Matched Skills</h2>

                    <span class="skill-count match-count">
                        {len(matched_skills)} MATCHED
                    </span>

                </div>

                <div class="skill-description">
                    Skills from your resume that match
                    the selected job requirements.
                </div>
            """,
            unsafe_allow_html=True
        )

        if matched_skills:

            for skill in matched_skills:

                st.markdown(
                    f"""
                    <span class="match-chip">
                        ✓ &nbsp;{skill}
                    </span>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                """
                <div style="
                    padding:20px;
                    text-align:center;
                    color:#777;
                ">
                    No matching skills detected.
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # ---------------- SKILL GAPS ----------------
    with skill_col2:

        st.markdown(
            f"""
            <div class="skill-box">

                <div class="skill-header">

                    <span style="font-size:28px;">🚀</span>

                    <h2>Skill Gaps</h2>

                    <span class="skill-count gap-count">
                        {len(missing_skills)} GAPS
                    </span>

                </div>

                <div class="skill-description">
                    Job-required skills that are currently
                    missing from your resume.
                </div>
            """,
            unsafe_allow_html=True
        )

        if missing_skills:

            for skill in missing_skills:

                st.markdown(
                    f"""
                    <span class="gap-chip">
                        + &nbsp;{skill}
                    </span>
                    """,
                    unsafe_allow_html=True
                )

        else:

            st.markdown(
                """
                <div style="
                    padding:20px;
                    text-align:center;
                    color:#198754;
                    font-weight:700;
                ">
                    🎉 No major skill gaps detected!
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # AI MATCHING INSIGHTS
    # =====================================================
    st.markdown(
        '<div class="section-title">🧠 AI Matching Insights</div>',
        unsafe_allow_html=True
    )

    insight1, insight2 = st.columns(2)

    with insight1:

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-icon">🛠️</div>

                <div class="insight-title">
                    Skill-Based Analysis
                </div>

                <div class="insight-text">
                    The system identified
                    <b>{len(matched_skills)}</b>
                    matching skills out of
                    <b>{len(job_skills)}</b>
                    detected job skills.
                </div>

                <div class="insight-score">
                    {skill_score:.1f}%
                </div>

                <div class="insight-text">
                    Skill-based compatibility
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with insight2:

        st.markdown(
            f"""
            <div class="insight-card">

                <div class="insight-icon">🤖</div>

                <div class="insight-title">
                    Semantic AI Analysis
                </div>

                <div class="insight-text">
                    AI compares the overall meaning
                    and context of the resume and
                    job description.
                </div>

                <div class="insight-score">
                    {semantic_score:.1f}%
                </div>

                <div class="insight-text">
                    Semantic similarity
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # =====================================================
    # AI SKILL GAP ANALYSIS
    # =====================================================
    st.markdown(
        '<div class="section-title">🧠 AI Skill Gap Analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="ai-intro">
            💡 <b>Personalized Learning Guidance</b><br>
