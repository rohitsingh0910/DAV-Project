import requests
import os

# Use your YouTube API Key
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "YOUR_YOUTUBE_API_KEY_HERE")

def fetch_youtube_videos(skill):
    """
    Fetches top YouTube videos related to a skill using the YouTube Data API.
    """
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{skill} tutorial",
        "key": 'AIzaSyDLz4g3KRIU9ktGg3-HC4gpRZeYDa_hfOk',
        "maxResults": 3,
        "type": "video"
    }

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        videos = response.json().get("items", [])
        return [
            {"title": video["snippet"]["title"], "videoId": video["id"]["videoId"]}
            for video in videos
        ]
    else:
        print("Error fetching videos:", response.text)
        return []

    response = requests.get(search_url, params=params)
    if response.status_code == 200:
        videos = response.json().get("items", [])
        return [
            {"title": video["snippet"]["title"], "videoId": video["id"]["videoId"]}
            for video in videos
        ]
    else:
        print("Error fetching videos:", response.text)
        return []

def get_missing_skills(job_skills, resume_skills):
    """
    Compares job skills with resume skills and returns missing skills.
    """
    resume_skills_lower = {skill.lower() for skill in resume_skills}
    job_skills_lower = {skill.lower() for skill in job_skills}

    missing_skills = job_skills_lower - resume_skills_lower
    return list(missing_skills)

def recommend_courses(job_skills, resume_skills):
    """
    Recommends courses for missing skills by fetching YouTube videos.
    """
    missing_skills = get_missing_skills(job_skills, resume_skills)
    recommendations = {}

    for skill in missing_skills:
        recommendations[skill] = fetch_youtube_videos(skill)

    return recommendations