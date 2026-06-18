from flask import Flask, render_template, request
import pdfplumber
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

skills_list = [
    "python", "sql", "machine learning", "html",
    "css", "javascript", "react", "flask",
    "power bi", "excel", "data analysis",
    "communication", "teamwork", "problem solving"
]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    if 'resume' not in request.files:
        return "No file uploaded"

    file = request.files['resume']

    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

    file.save(filepath)

    resume_text = ""

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text = page.extract_text()

            if text:
                resume_text += text.lower()

    detected_skills = []

    for skill in skills_list:
        if skill in resume_text:
            detected_skills.append(skill.title())

    ats_score = min(len(detected_skills) * 10, 100)

    recommended_skills = []

    for skill in skills_list:
        if skill.title() not in detected_skills:
            recommended_skills.append(skill.title())

    career_role = "General"

    if "machine learning" in resume_text or "python" in resume_text:
        career_role = "Machine Learning Engineer"

    elif "html" in resume_text or "css" in resume_text:
        career_role = "Frontend Developer"

    elif "sql" in resume_text or "excel" in resume_text:
        career_role = "Data Analyst"

    return render_template(
        'result.html',
        ats_score=ats_score,
        detected_skills=', '.join(detected_skills),
        recommended_skills=', '.join(recommended_skills[:5]),
        career_role=career_role
    )


if __name__ == '__main__':
    app.run(debug=True)
