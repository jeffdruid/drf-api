# Trigger Warning ⚠️

Content Warning: This documentation discusses sensitive topics, including mentions of self-harm, suicide, and other potentially triggering material related to content moderation. The backend functionality described in this project includes detection of language associated with these topics to ensure user safety.

# Backend Overview

The backend for this project is built with Django and Django REST Framework (DRF). It handles content moderation, including flagging and checking content for specific trigger words that may indicate self-harm or other concerning behaviors. The main components are the FlaggedContent model, serializer, and viewset.
![Moderation Page](README/images/main.png)

## Table of Contents

Key Features
Technology Stack
Models
Serializers
Views and Endpoints
Trigger Words Detection
Installation and Setup
Admin Interface

## Key Features

- Content Flagging and Moderation: Detects and flags content containing specific trigger words.
- Admin Review System: Allows admins to approve or delete flagged content.
- Custom Action for Real-Time Moderation: Provides an endpoint to check for sensitive content without persisting it.
- Firebase Integration: Syncs with Firebase for user and post management.

## Technology Stack

- Django: Web framework for backend development.
- Django REST Framework (DRF): Extends - Django to build RESTful APIs.
- Firebase Admin SDK: Integrates Firebase services for user management and data synchronization.

## Models

FlaggedContent Model
The FlaggedContent model stores information about content flagged for potential issues, such as trigger words related to self-harm or harmful behaviors.

```python
from django.db import models

class FlaggedContent(models.Model):
    post_id = models.CharField(max_length=100)  # Firebase post ID
    content = models.TextField()
    reason = models.CharField(max_length=255)
    user = models.CharField(max_length=255)  # Firebase user UID
    flagged_at = models.DateTimeField(auto_now_add=True)
    reviewed = models.BooleanField(default=False)
    is_visible = models.BooleanField(default=False)  # New field to control post visibility

    def __str__(self):
        return f"Flagged by {self.user} for {self.reason}"
```

### Fields:

- post_id: A CharField that stores the ID of the post in Firebase.
- content: A TextField that holds the actual content that was flagged.
- reason: A CharField that provides the reason for flagging (e.g., detected trigger words).
- user: A CharField storing the user ID of the person who posted the flagged content.
- flagged_at: A DateTimeField set to the time the content was flagged.
  reviewed: A BooleanField indicating if the flagged content has been reviewed by an admin.
- is_visible: A BooleanField to control the visibility of flagged content on the platform (default is False).

## Serializers

FlaggedContentSerializer
The FlaggedContentSerializer is responsible for converting FlaggedContent model instances to JSON and vice versa. It exposes the following fields:

```python
from rest_framework import serializers
from .models import FlaggedContent

class FlaggedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlaggedContent
        fields = ['user', 'post_id', 'reason', 'flagged_at', 'reviewed']
```

- user: ID of the user who created the flagged content.
- post_id: Firebase post ID.
- reason: Reason for flagging the content.
- flagged_at: Timestamp of when the content was flagged.
- reviewed: Status of whether the content has been reviewed.

This serializer enables efficient data transfer between the Django backend and frontend or external applications.

### Views

#### FlaggedContentViewSet

The FlaggedContentViewSet is a DRF viewset that manages CRUD operations for flagged content, allowing for creation, retrieval, updating, and deletion.

#### Main Endpoints:

- create: Handles creation of flagged content. Before saving, it validates the presence of all required fields (post_id, content, reason, and user).

```python
def create(self, request, *args, **kwargs):
        try:
            # Log the incoming request data
            print(request.data)

            # Validate required fields
            required_fields = ['post_id', 'content', 'reason', 'user']
            for field in required_fields:
                if field not in request.data:
                    raise ValueError(f"'{field}' is a required field.")

            flagged_content = FlaggedContent.objects.create(
                post_id=request.data.get('post_id'),
                content=request.data['content'],
                reason=request.data['reason'],
                user=request.data['user'],  # Ensure this matches the 'user' field
            )
            return Response({"success": True}, status=status.HTTP_201_CREATED)
```

- check_content: A custom action that checks if content contains trigger words without saving it to the database. This helps in real-time moderation of content as users post.

```python
 # Custom action for checking content without saving flagged content
    @action(detail=False, methods=['post'], url_path='check')
    def check_content(self, request):
        content = request.data.get('content', '')

        # Simple trigger word example
        trigger_words = [
            ...  # Trigger words here
        ]
        flagged = any(word in content.lower() for word in trigger_words)

        if flagged:
            return Response({"flagged": True, "message": "Content contains trigger words."})

        return Response({"flagged": False}, status=status.HTTP_200_OK)
```

#### Custom Action (check_content):

This action uses a list of trigger words to check if the submitted content includes any concerning terms related to self-harm or other harmful behaviors.
If any trigger word is detected, the content is flagged, and a response indicating the presence of trigger words is returned.

##### Trigger Words Example:

The list includes terms like "suicide," "self-harm," "cutting," and similar terms that may indicate self-harm or suicidal ideation.

##### Example Response from check_content:

If flagged:

```json
{"flagged": True, "message": "Content contains trigger words."}
```

If safe:

```json
{"flagged": False}
```

create Method Error Handling:

In case of missing fields or other issues during creation, the method logs the error and returns an appropriate message with HTTP status 500 (Internal Server Error).

```python
  except Exception as e:
            print(e)  # Check the exact error in the console
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

### Admin Review Interface

The admin interface allows administrators to review, approve, or delete flagged posts. Flagged content is displayed with the reason for flagging, the user who posted it, and the flagged date.
![Flagged Post](/README/images/flagged-post.png)

#### Admin Actions

- Approve: Admins can mark content as reviewed and make it visible if deemed safe.
- Delete: Admins can permanently remove flagged content from the database.

# Tests

add tests here

## Deployment

This section provides detailed instructions for deploying the backend of the project. You can either set up the backend locally or deploy it to Heroku for remote hosting.

### Prerequisites

- Python 3.x and pip installed
- Django and Django REST Framework installed
- Firebase Admin SDK (if Firebase integration is required)
- Git for version control
- Heroku CLI (if deploying on Heroku)

### Local Deployment

To deploy the backend locally, follow these steps:

Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```

Install Required Packages

```bash
pip install -r requirements.txt
```

Set Up Environment Variables

- Create a .env file in the project root.

Add the required environment variables:

```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
# Firebase Configurations if using Firebase
FIREBASE_CREDENTIALS=path/to/firebase/credentials.json
```

Run Migrations

```bash
python manage.py migrate
```

Start the Development Server

```bash
python manage.py runserver
```

Access the Application

- Open your browser and navigate to http://127.0.0.1:8000 to access the backend.

### Deployment on Heroku

To deploy the backend on Heroku, follow these steps:

Log in to Heroku CLI

```bash
heroku login
```

Create a New Heroku App

```bash
heroku create <app_name>
```

### Add Heroku PostgreSQL Database

Set up a PostgreSQL database on Heroku:

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

Set Environment Variables on Heroku

- Go to your Heroku dashboard, navigate to your app, and set the required environment variables in the Settings tab under Config Vars.

- Alternatively, you can set them via the Heroku CLI:

```bash
heroku config:set SECRET_KEY=your_secret_key
heroku config:set DEBUG=False
heroku config:set FIREBASE_CREDENTIALS=$(<path/to/firebase/credentials.json)
```

Prepare the Application for Deployment

Install gunicorn to act as the web server:

```bash
pip install gunicorn
```

Add gunicorn to your requirements.txt file:

```bash
pip freeze > requirements.txt
```

Create a Procfile in the root directory with the following line:

```plaintext
web: gunicorn your_project_name.wsgi
```

### Deploy to Heroku

Add, commit, and push your code to Heroku:

```bash
git add .
git commit -m "Deploying to Heroku"
git push heroku main
```

Run Migrations on Heroku

```bash
heroku run python manage.py migrate
```

Access Your Deployed Application

Open your browser and navigate to the URL provided by Heroku (https://<app_name>.herokuapp.com) to access the backend.

### Additional Notes

- Static Files: For production, set up static files handling using Django's collectstatic and an appropriate storage solution like AWS S3 or Heroku's built-in storage.

- Firebase Integration: If Firebase Admin SDK is used, ensure the Firebase credentials JSON file is added securely and referenced correctly in your Heroku environment variables.

- SSL/TLS: Heroku provides HTTPS automatically on all applications under the herokuapp.com domain.
