import re
import json

with open("skills_list.txt") as f:
    SKILLS_DB = [line.strip().lower() for line in f.readlines()]

def extract_skills(text):
    text = text.lower()
    return sorted(set(skill for skill in SKILLS_DB if skill in text))

def analyze_resume(text):
    skills = extract_skills(text)
    sections = ["education", "experience", "projects", "skills", "certification"]
    score = sum(1 for sec in sections if sec in text.lower()) * 10
    score += min(len(skills), 10) * 5  # up to 50 pts from skills
    return {
        "score": score,
        "skills": skills
    }
