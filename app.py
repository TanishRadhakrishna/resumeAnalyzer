import streamlit as st
import pandas as pd
import base64
import io
import matplotlib.pyplot as plt
from matplotlib import style
from PyPDF2 import PdfReader
from collections import Counter
import re

# Use a more aesthetic style for matplotlib
style.use('ggplot')

# ---- Helper Functions ----
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def analyze_resume(text):
    keywords = ['python', 'java', 'sql', 'machine learning', 'data analysis']

    # Extract skill mentions from projects (more relevant than general text)
    project_keywords = '|'.join(keywords)
    project_mentions = re.findall(fr'(?i)\b({project_keywords})\b', text)
    skill_distribution = dict(Counter([kw.lower() for kw in project_mentions]))

    found_skills = list(skill_distribution.keys())
    missing_skills = list(set(keywords) - set(found_skills))

    # Improved Skill Score: considers both presence and frequency of skills
    total_possible = len(keywords)
    presence_score = len(found_skills) / total_possible
    freq_score = sum(skill_distribution.values()) / total_possible
    skill_score = int((0.5 * presence_score + 0.5 * min(freq_score, 1)) * 100)

    # Job roles and courses mapped to each skill
    job_role_map = {
        'python': ['Python Developer', 'ML Engineer'],
        'sql': ['Data Analyst', 'BI Analyst'],
        'java': ['Java Developer'],
        'machine learning': ['ML Engineer'],
        'data analysis': ['Data Scientist']
    }

    course_map = {
        'python': ['Python for Everybody (Coursera)'],
        'sql': ['SQL for Data Science (Udemy)'],
        'java': ['Java Programming Masterclass (Udemy)'],
        'machine learning': ['Intro to ML (Kaggle)', 'ML Specialization (Coursera)'],
        'data analysis': ['Data Analytics with Excel (Coursera)']
    }

    job_suggestions = set()
    course_suggestions = set()
    for skill in found_skills:
        job_suggestions.update(job_role_map.get(skill, []))
        course_suggestions.update(course_map.get(skill, []))

    return {
        'found_skills': found_skills,
        'missing_skills': missing_skills,
        'skill_score': skill_score,
        'skill_distribution': skill_distribution,
        'suggested_jobs': list(job_suggestions) or ['Explore internships to gain experience'],
        'courses': list(course_suggestions) or ['Consider introductory courses on Coursera/Udemy']
    }

# ---- Streamlit UI ----
st.set_page_config(page_title="Resume Analyzer", layout="centered")
st.title("📄 Resume Analyzer")
st.write("Upload your resume (PDF) to receive a detailed analysis of your skills, matching jobs, and suggestions to improve.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    result = analyze_resume(text)

    st.subheader("✅ Resume Analysis Summary")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Skill Match %", f"{result['skill_score']}%")
        st.success("✔️ Found Skills")
        st.write(", ".join(result['found_skills']) or "None")

    with col2:
        st.warning("⚠️ Missing Skills")
        st.write(", ".join(result['missing_skills']) or "None")

    # --- Skill Relevance Pie Chart ---
    st.subheader("📊 Skill Relevance from Projects")

    skill_labels = list(result['skill_distribution'].keys())
    skill_sizes = list(result['skill_distribution'].values())

    if skill_sizes:
        fig, ax = plt.subplots(figsize=(6, 6))
        wedges, texts, autotexts = ax.pie(
            skill_sizes,
            labels=skill_labels,
            autopct='%1.1f%%',
            startangle=140,
            colors=plt.cm.Paired.colors,
            textprops={'fontsize': 12, 'color': 'black'}
        )
        ax.axis('equal')
        ax.set_title("Skill Distribution in Projects", fontsize=16, fontweight='bold')
        st.pyplot(fig)
    else:
        st.info("No relevant skills mentioned in project descriptions.")

    # --- Job Suggestions ---
    st.subheader("💼 Recommended Job Roles")
    st.write("Based on your skills, you may apply for:")
    for job in result['suggested_jobs']:
        st.markdown(f"- {job}")

    # --- Course Suggestions ---
    st.subheader("🎓 Suggested Courses to Improve Your Resume")
    for course in result['courses']:
        st.markdown(f"- {course}")

else:
    st.info("⬆️ Please upload your resume to get started.")
