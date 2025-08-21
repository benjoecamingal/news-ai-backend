
# News AI Backend

This is the backend for a news application that fetches the latest news articles, generates AI-powered summaries, and provides a RESTful API to access the data.

## Features

*   Fetches latest news from the [newsdata.io](https://newsdata.io) API.
*   Generates article summaries in both English and Tagalog using AI.
*   Provides a REST API to list and retrieve news articles.
*   Allows filtering of news articles by category.

## Technologies Used

*   Python
*   Django
*   Django REST Framework
*   requests
*   python-dotenv

## Setup and Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd backend
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv env
    source env/bin/activate  # On Windows, use `env\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Create a `.env` file:**

    Create a `.env` file in the `backend` directory and add your newsdata.io API key:

    ```
    NEWS_API_KEY=your_api_key_here
    ```

4.  **Run database migrations:**

    ```bash
    python manage.py migrate
    ```

## Running the Application

1.  **Fetch the latest news:**

    ```bash
    python manage.py fetch_news
    ```

2.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

*   **List News Articles:**

    *   `GET /api/news/`
    *   **Filter by category:** `GET /api/news/?category=<category_name>`

*   **Get Article Summary:**

    *   `GET /api/news/<article_id>/summarize/`
    *   **Specify language (en/tl):** `GET /api/news/<article_id>/summarize/?lang=<language_code>`

