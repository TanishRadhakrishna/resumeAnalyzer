import json

with open("job_titles.json") as f:
    JOB_DB = json.load(f)

with open("courses.json") as f:
    COURSE_DB = json.load(f)

def recommend_roles(skills):
    matches = []
    for job, keywords in JOB_DB.items():
        if any(skill in keywords for skill in skills):
            matches.append(job)
    return matches[:5]

def recommend_skills_and_courses(user_skills):
    suggestions = {}
    for course in COURSE_DB:
        if course['skill'] not in user_skills:
            suggestions[course['skill']] = {
                "title": course["title"],
                "link": course["link"]
            }
        if len(suggestions) == 5:
            break
    return suggestions
