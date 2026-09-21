from pypdf import PdfReader

# -----------------------------
# 1. Read Resume
# -----------------------------

reader = PdfReader("resume.pdf")

resume_text = ""

for page in reader.pages:
    resume_text += page.extract_text() or ""

resume_text = resume_text.lower()


# -----------------------------
# 2. Get Job Description
# -----------------------------

print("========== AI JOB MATCHING PORTAL ==========")

print("\nEnter Job Description.")
print("Type END on a new line when finished.\n")

job_description = ""

while True:
    line = input()

    if line.upper() == "END":
        break

    job_description += line + " "

job_description = job_description.lower()


# -----------------------------
# 3. Skills Database
# -----------------------------

skills = [
    "python",
    "java",
    "c",
    "c++",
    "machine learning",
    "deep learning",
    "sql",
    "mysql",
    "data science",
    "data analysis",
    "classification",
    "regression",
    "data preprocessing",
    "power bi",
    "excel",
    "github",
    "jupyter notebook",
    "html",
    "css",
    "javascript"
]


# -----------------------------
# 4. Extract Skills
# -----------------------------

resume_skills = [
    skill for skill in skills
    if skill in resume_text
]

job_skills = [
    skill for skill in skills
    if skill in job_description
]


# -----------------------------
# 5. Match Skills
# -----------------------------

matched_skills = set(resume_skills).intersection(set(job_skills))

if len(job_skills) > 0:
    match_percentage = (
        len(matched_skills) / len(job_skills)
    ) * 100
else:
    match_percentage = 0


# -----------------------------
# 6. Display Results
# -----------------------------

print("\n========== MATCHING RESULT ==========")

print("\nResume Skills:")
for skill in resume_skills:
    print("✓", skill)

print("\nJob Skills:")
for skill in job_skills:
    print("•", skill)

print("\nMatched Skills:")
for skill in matched_skills:
    print("✓", skill)

print("\nMissing Skills:")
for skill in set(job_skills) - matched_skills:
    print("✗", skill)

print("\nJob Match Percentage:",
      round(match_percentage, 2), "%")


if match_percentage >= 75:
    print("Result: Strong Match")
elif match_percentage >= 50:
    print("Result: Moderate Match")
else:
    print("Result: Low Match")
