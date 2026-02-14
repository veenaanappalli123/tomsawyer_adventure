import requests
from django.shortcuts import render
from .models import Play
from django.db.models import Count


def home(request):
    response = requests.get("http://127.0.0.1:5000/api/stories")
    all_stories = response.json()

    # Only show published stories
    stories = [s for s in all_stories if s["status"] == "published"]

    return render(request, "home.html", {"stories": stories})


def play_story(request, story_id):
    story_response = requests.get("http://127.0.0.1:5000/api/stories")
    stories = story_response.json()

    story = next((s for s in stories if s["id"] == story_id), None)

    if not story:
        return render(request, "error.html", {"message": "Story not found"})

    page_id = request.GET.get("page_id")

    if page_id:
        page_response = requests.get(f"http://127.0.0.1:5000/api/pages/{page_id}")
    else:
        start_page_id = story["start_page_id"]
        page_response = requests.get(f"http://127.0.0.1:5000/api/pages/{start_page_id}")

    page = page_response.json()

    # If this page is an ending, store Play record
    if page.get("is_ending"):
        Play.objects.create(
            story_id=story_id,
            ending_page_id=page["id"]
        )

    return render(request, "page.html", {"page": page})

def stats(request):
    from collections import defaultdict

    # Total plays per story
    story_stats = (
        Play.objects.values("story_id")
        .annotate(total_plays=Count("id"))
    )

    # Ending distribution
    ending_raw = (
        Play.objects.values("story_id", "ending_page_id")
        .annotate(count=Count("id"))
    )

    # Convert to percentage per story
    story_totals = {s["story_id"]: s["total_plays"] for s in story_stats}

    ending_stats = []

    for ending in ending_raw:
        total = story_totals.get(ending["story_id"], 1)
        percentage = round((ending["count"] / total) * 100, 2)

        ending_stats.append({
            "story_id": ending["story_id"],
            "ending_page_id": ending["ending_page_id"],
            "count": ending["count"],
            "percentage": percentage
        })

    context = {
        "story_stats": story_stats,
        "ending_stats": ending_stats,
    }

    return render(request, "stats.html", context)

