from pypdf import PdfReader

# -----------------------------
# 1. Read Resume PDF
# -----------------------------

pdf_path = "resume.pdf"

reader = PdfReader(pdf_path)

resume_text = ""

for page in reader.pages:
    resume_text += page.extract_text() or ""

resume_text = resume_text.lower()


# -----------------------------
# 2. Skills Database
# -----------------------------

skills = [
    "python",
    "java",
    "machine learning",
    "sql",
    "mysql",
    "data science",
    "classification",
    "regression",
    "data preprocessing",
    "power bi",
    "github",
    "jupyter notebook"
]


# -----------------------------
# 3. Extract Resume Skills
# -----------------------------

resume_skills = []

for skill in skills:
    if skill in resume_text:
        resume_skills.append(skill)


# -----------------------------
# 4. Job Required Skills
# -----------------------------

job_skills = [
    "python",
    "machine learning",
    "sql",
    "data science"
]


# -----------------------------
# 5. Find Matching Skills
# -----------------------------

matched_skills = set(resume_skills).intersection(set(job_skills))

match_percentage = (
    len(matched_skills) / len(job_skills)
) * 100


# -----------------------------
# 6. Display Result
# -----------------------------

print("========== AI JOB MATCHING PORTAL ==========")

print("\nResume Skills:")
for skill in resume_skills:
    print("✓", skill)

print("\nJob Required Skills:")
for skill in job_skills:
    print("•", skill)

print("\nMatched Skills:")
for skill in matched_skills:
    print("✓", skill)

print("\nJob Match Percentage:", round(match_percentage, 2), "%")


if match_percentage >= 75:
    print("Result: Strong Match")
elif match_percentage >= 50:
    print("Result: Moderate Match")
else:
    print("Result: Low Match")