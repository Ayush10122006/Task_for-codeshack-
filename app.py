import os
import re
import PyPDF2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "supersecretkey"


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


SKILLS = [
    "Python", "C++", "Java", "Machine Learning", "LEADERSHIP", "AI DEVELOPMENT",
    "SQL", "HTML", "CSS", "JavaScript", "PRODUCT DEVELOPMENT", "ROBOTICS", "INNOVATION"
]
EDUCATION = ["Bachelor's in Electrical Engineering","Master's in Electrical Engineering","Masters in Electrical Engineering", "B.E", "B.Tech", "M.Tech", "PhD", "College", "University"]
EXPERIENCE = ["Internship","CEO", "Lead Engineer", "Developer", "Research", "Team Lead" , "Manager"]


def extract_text_from_pdf(filepath):
    """Extract all text from a PDF file."""
    text = ""
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += "\n" + page_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def extract_personal_info(text):
    """Extract Name, Email, and Phone Number using regex and heuristics."""

    email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    email = email_match.group(0) if email_match else "Not Found"


    phone_match = re.search(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{4}", text)
    phone = phone_match.group(0) if phone_match else "Not Found"

    # Guess name: usually the first non-empty line that doesn’t contain certain keywords
    lines = text.strip().split("\n")
    name = "Not Found"
    for line in lines:
        if (len(line.strip().split()) <= 4 and
            not any(word.lower() in line.lower() for word in 
                    ["email", "phone", "@", "resume", "curriculum", "vitae", 
                     "address", "linkedin", "github"])):
            name = line.strip().title()
            break

    return {"name": name, "email": email, "phone": phone}


def analyze_resume(text):
    """Detects skills, education, and experience keywords in resume text."""
    found_skills = [skill for skill in SKILLS if skill.lower() in text.lower()]
    found_education = [edu for edu in EDUCATION if edu.lower() in text.lower()]
    found_experience = [exp for exp in EXPERIENCE if exp.lower() in text.lower()]

    return {
        "skills": found_skills or ["None"],
        "education": found_education or ["None"],
        "experience": found_experience or ["None"],
    }


def score_resume(personal_info, analysis):
    """Give a score out of 10 based on resume completeness."""
    score = 0


    if personal_info["name"] != "Not Found":
        score += 1
    if personal_info["email"] != "Not Found":
        score += 1
    if personal_info["phone"] != "Not Found":
        score += 1


    if len(analysis["skills"]) >= 3 and "None" not in analysis["skills"]:
        score += 3
    if "None" not in analysis["education"]:
        score += 2
    if "None" not in analysis["experience"]:
        score += 2

    return score


@app.route("/")
def index():
    """Render the upload page."""
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload_resume():
    """Handles PDF upload and redirects to result page after analysis."""
    if "file" not in request.files:
        flash("⚠️ No file part in request.")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("⚠️ Please choose a file to upload.")
        return redirect(url_for("index"))

    if not file.filename.lower().endswith(".pdf"):
        flash("❌ Only PDF files are allowed.")
        return redirect(url_for("index"))

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)
    text = extract_text_from_pdf(filepath)
    personal_info = extract_personal_info(text)
    analysis = analyze_resume(text)
    score = score_resume(personal_info, analysis)


    return render_template(
        "result.html",
        filename=file.filename,
        name=personal_info["name"],
        email=personal_info["email"],
        phone=personal_info["phone"],
        skills=analysis["skills"],
        education=analysis["education"],
        experience=analysis["experience"],
        score=score
    )



if __name__ == "__main__":
    app.run(debug=True, port=8000)
