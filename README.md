# tomsawyer_adventure
# NAHB – Not Another Hero's Book

A web application inspired by TOM SAWYER ,really he doesnt have any conncetion with it , i just used his name, books.

This project was built as a final assignment using:

- Flask (REST API for story content)
- Django (Web application + gameplay engine)

---

## Architecture Overview

This project contains two separate applications:

### 1️ Flask API (Story Content Service)
- Stores stories, pages, and choices
- Provides REST JSON endpoints
- Uses SQLite database
- No HTML rendering

### 2️ Django Web App (Game Engine)
- Renders HTML templates
- Handles gameplay logic
- Stores play statistics
- Consumes Flask API
- Uses its own separate SQLite database

Story content is stored **only in Flask**.  
Gameplay tracking is stored **only in Django**.

---

## Features Implemented (Level 13)

### Core Features
- Create and manage interactive stories
- Multi-branch narrative tree
- Multiple endings with labels
- Story navigation through choices
- Published story filtering
- Play tracking (anonymous)
- Statistics page

### Statistics
- Total plays per story
- Ending distribution
- Percentage breakdown per ending

### UI Improvements
- Clean layout
- Navigation bar
- Styled buttons
- Ending highlight box

---

##  Example Story

Included story:

**"Lost After Storm"**

Branches include:
- Hide from the wolf
- Run and get caught
- Discover a cave
- Dream ending twist

Demonstrates:
- Multi-path branching
- Multiple endings
- Proper navigation flow

---

## Installation & Run Instructions

### Clone Repository
git clone https://github.com/veenaanappalli123/tomsawyer_adventure.git
cd tomsawyer_adventure



##RUN FLASK API##
cd flask-api
python -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
python app.py

##FLASK runs on 
http://127.0.0.1:5000


##RUN DJANGO APP##
cd django-web
python -m venv venv
source venv/Scripts/activate
pip install django requests
python manage.py migrate
python manage.py runserver


##DJANGO runs in
http://127.0.0.1:8000



API Endpoints (Flask)

Reading
GET /api/stories
GET /api/stories/<id>
GET /api/pages/<id>

Writing
POST /api/stories
POST /api/stories/<id>/pages
POST /api/pages/<id>/choices
DELETE /api/choices/<id>



##Data Models##
Flask Models

Story
 id
 title
 description
 status
 start_page_id
Page
 id
 story_id
 text
 is_ending
 ending_label
Choice
 id
 page_id
 text
 next_page_id

Django Model
 Play
 story_id
 ending_page_id
 created_at

#######thankyou######
