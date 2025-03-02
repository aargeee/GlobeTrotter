# GlobeTrotter Game

![globe-trotter-rose vercel app_](https://github.com/user-attachments/assets/738b026d-c3fc-4532-8d4b-f63cbaa61e59)

## Overview

This application is a Tourist Destination Quiz Game, providing users with an engaging way to test their knowledge about various tourist destinations around the world. The backend service provides endpoints for managing quizzes, questions, user profiles, and scores.

## Features

- User authentication and authorization
- Profile management (create/update profile, view scores)
- Browse and take quizzes on various tourist destinations
- Social sharing of scores and achievements
- Leaderboards to track top players
- Admin panel for managing quizzes and questions

## Tech Stack

- **Frontend:** Vite, React, JavaScript, CSS
- **Backend:** Django, Python
- **Database:** Sqlite3

### Frontend Details

The frontend is built using Vite, a fast and lightweight build tool that provides a great developer experience. React is used for building the user interface, with JavaScript and CSS for functionality and styling.

### Backend Details

The backend is built using Django, a high-level Python web framework that encourages rapid development and clean, pragmatic design. It provides a robust set of features for building web applications, including an ORM, templating engine, and more. The backend is also unit tested, with a coverage of approximately 80%.

## Deployment

- **Backend:** The Django backend is hosted on PythonAnywhere.
- **Frontend:** The Vite frontend is hosted on Vercel.

## Installation

### Frontend Installation

1. Navigate to the project directory:
    ```sh
    cd project
    ```
2. Install dependencies:
    ```sh
    npm install
    ```
3. Start the development server:
    ```sh
    npm run dev
    ```

### Backend Installation

1. Navigate to the service directory:
    ```sh
    cd service
    ```
2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Set up environment variables:
    ```sh
    cp .env.example .env
    ```
    Update the `.env` file with your MongoDB URI and other necessary configurations.
4. Start the server:
    ```sh
    python manage.py runserver
    ```

## API Endpoints

- **POST /api/token/**: Obtain an unregistered user token
- **POST /api/token/refresh/**: Refresh an unregistered user token
- **POST /api/signup/**: Register a new user
- **GET /api/profile/**: Get user profile information
- **POST /api/game/**: Start a new game
- **GET /api/game/<str:game_id>/questions/**: Get questions for a specific game
- **POST /api/game/<str:game_id>/response/**: Submit a game response
- **GET /api/game/<str:game_id>/score/**: Get the score for a specific game
- **POST /api/destination/**: Add a new destination (admin only)
- **POST /api/admin/token/**: Obtain an admin token
- **GET /api/cities/**: List available cities
- **GET /api/game/high_score/**: Get the high score for all users
- **GET /api/game/high_score/<str:username>/**: Get the high score for a specific user
- **POST /api/destination/generate/**: Generate a new destination

## Contact

For any questions or feedback, please contact at dev.rahulgoel@gmail.com
