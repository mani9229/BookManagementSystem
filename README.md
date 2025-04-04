#   Intelligent Book Management System

This system provides a RESTful API for managing books and reviews, leveraging a local Llama 2 generative AI model for book summaries and recommendations. It uses Flask, PostgreSQL, and Docker for efficient development and deployment.

##   Table of Contents

1.  Dependencies
    * 1.1. Python Dependencies
    * 1.2. System Dependencies
    * 1.3. Ollama Setup 
    * 1.4. PostgreSQL Setup 
2.  Setup
    * 2.1. Cloning the Repository
    * 2.2. Environment Configuration 
    * 2.3. Database Migration 
    * 2.4. Running the Application 
3.  API Endpoints 
4.  Testing 


##   1. Dependencies

###   1.1. Python Dependencies

The project uses Python and requires the following packages. It is strongly recommended to use a virtual environment to isolate these dependencies and avoid conflicts with system-level packages.


**Installation Instructions:**

1.  **Create a Virtual Environment:**



    * **On Windows:**

        ```bash
        python3 -m venv venv  #  Create a directory named 'venv'
        venv\Scripts\activate  #  Activate the environment
        ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt  #  Install all packages listed in requirements.txt
    ```


###   1.2. System Dependencies

These dependencies are required at the operating system level for certain Python packages to function correctly.


###   1.3. Ollama Setup 

Ollama is essential for generating book summaries and recommendations. Proper setup is critical.

1.  **Install Ollama:**

    * This Application setup is done assuming there is a local instance of ollama is downloaded and ready to run if not please download the model as mentioned in the next step.

2.  **Download the Language Model:**

    * Ollama needs a language model to perform its tasks. Download the model . 

        ```bash
        ollama run Llama-2-7b-chat-GGUF  
        ```

###   1.4. PostgreSQL Setup 

PostgreSQL is used to store book and review data.

1.  **Install PostgreSQL:**
     * For this i have used the free version of neondb postgeSQL
    
2.  **Create the Database and User:**

    * These steps assume you have basic PostgreSQL command-line access.

        ```bash
        sudo -u postgres psql  #  Access the PostgreSQL prompt as the 'postgres' user
        ```

    * **Inside the PostgreSQL prompt:**

        ```sql
        CREATE DATABASE your_db_name;  #  Create the database
        CREATE USER your_db_user WITH PASSWORD 'your_db_password';  #  Create a user
        GRANT ALL PRIVILEGES ON DATABASE your_db_name TO your_db_user;  #  Grant privileges
        \q  
        ```

 
##   2. Setup

###   2.1. Cloning the Repository

1.  **Clone the Repository:**

    ```bash
    git clone <repository_url>  
    cd <repository_name>  
    ```


###   2.2. Environment Configuration 

Environment variables are used to configure the application without hardcoding sensitive information in the code.

1.  **Copy the `.env.example` File:**

    ```bash
    cp .env.example .env  #  Copy the template to create the actual .env file
    ```

 
2.  **Edit the `.env` File:**

    * Open the `.env` file in a text editor and replace the placeholder values with your actual configuration.

    ```
    SECRET_KEY=your_strong_secret_key  
    DATABASE_URL=postgresql://your_db_user:your_db_password@your_host:your_port/your_db_name  #  PostgreSQL connection string
    FLASK_ENV=development 
    OLLAMA_MODEL=Llama-2-7b-chat-GGUF  #  Ollama model name 
    ```

###   2.3. Database Migration 

Database migrations are used to create and update the database schema.

1.  **Initialize the Migration Repository:**

    ```bash
    flask db init  #  Creates the 'migrations' directory
    ```


2.  **Run the Migration:**

    ```bash
    flask db upgrade  #  Applies the migrations to the database
    ```


###   2.4. Running the Application 

1.  **Run the Flask Application:**

    ```bash
    flask run --host=0.0.0.0 --port=8000
    ```

##   3. API Endpoints 

This section details all the available API endpoints.

**Endpoint Details:**

* **User Authentication**

    * **`POST /auth/register`**: Register a new user.
        * Request Body:

            ```json
            {
                "username": "newuser",
                "password": "strongpassword"
            }
            ```

        * Response (201 Created):

            ```json
            {
                "id": 1,
                "username": "newuser"
            }
            ```

        * Error Responses: 400 (Bad Request) if username already exists or validation fails.

    * **`POST /auth/login`**: Authenticate a user and obtain an access token.
        * Request Body:

            ```json
            {
                "username": "existinguser",
                "password": "userpassword"
            }
            ```

        * Response (200 OK):

            ```json
            {
                "access_token": "your.jwt.access.token"
            }
            ```

        * Error Responses: 401 (Unauthorized) if credentials are invalid.

* **Books**

    * **`GET /api/books`**: Get all books.
        * Response (200 OK):

            ```json
            [
                {
                    "id": 1,
                    "title": "Book Title 1",
                    "author": "Author 1",
                    "genre": "Genre 1",
                    "year_published": 2023,
                    "summary": "Summary 1"
                },
                {
                    "id": 2,
                    "title": "Book Title 2",
                    "author": "Author 2",
                    "genre": "Genre 2",
                    "year_published": 2022,
                    "summary": "Summary 2"
                }
            ]
            ```

    * **`GET /api/books/{book_id}`**: Get a specific book by ID.
        * Path Parameters:
            * `book_id` (integer): The ID of the book to retrieve.
        * Response (200 OK):

            ```json
            {
                "id": 1,
                "title": "Book Title 1",
                "author": "Author 1",
                "genre": "Genre 1",
                "year_published": 2023,
                "summary": "Summary 1"
            }
            ```

        * Error Responses: 404 (Not Found) if the book with the given ID does not exist.

    * **`POST /api/books`**: Add a new book.
        * Request Body:

            ```json
            {
                "title": "New Book Title",
                "author": "New Author",
                "genre": "New Genre",
                "year_published": 2024,
                "summary": "Optional Summary"
            }
            ```

        * Response (201 Created):

            ```json
            {
                "id": 3,
                "title": "New Book Title",
                "author": "New Author",
                "genre": "New Genre",
                "year_published": 2024,
                "summary": "Optional Summary"
            }
            ```

        * Error Responses: 400 (Bad Request) if validation fails (e.g., missing required fields).

    * **`PUT /api/books/{book_id}`**: Update an existing book.
        * Path Parameters:
            * `book_id` (integer): The ID of the book to update.
        * Request Body:

            ```json
            {
                "title": "Updated Title",
                "author": "Updated Author",
                "genre": "Updated Genre",
                "year_published": 2025,
                "summary": "Updated Summary"
            }
            ```

            * Note: You only need to provide the fields you want to update.

        * Response (200 OK):

            ```json
            {
                "id": 3,
                "title": "Updated Title",
                "author": "Updated Author",
                "genre": "Updated Genre",
                "year_published": 2025,
                "summary": "Updated Summary"
            }
            ```

        * Error Responses: 400 (Bad Request) if validation fails, 404 (Not Found) if the book with the given ID does not exist.

    * **`DELETE /api/books/{book_id}`**: Delete a book.
        * Path Parameters:
            * `book_id` (integer): The ID of the book to delete.
        * Response (204 No Content):
            * (Empty response body)
        * Error Responses: 404 (Not Found) if the book with the given ID does not exist.

* **Reviews**

    * **`GET /api/books/{book_id}/reviews`**: Get all reviews for a specific book.
        * Path Parameters:
            * `book_id` (integer): The ID of the book to get reviews for.
        * Response (200 OK):

            ```json
            [
                {
                    "id": 1,
                    "book_id": 1,
                    "user_id": 1,
                    "review_text": "Great book!",
                    "rating": 5
                },
                {
                    "id": 2,
                    "book_id": 1,
                    "user_id": 2,
                    "review_text": "Enjoyable read.",
                    "rating": 4
                }
            ]
            ```

        * Error Responses: 404 (Not Found) if the book with the given ID does not exist.

    * **`POST /api/books/{book_id}/reviews`**: Add a new review for a book.
        * Path Parameters:
            * `book_id` (integer): The ID of the book to add the review to.
        * Request Body:

            ```json
            {
                "review_text": "My review...",
                "rating": 4
            }
            ```

        * Response (201 Created):

            ```json
            {
                "id": 3,
                "book_id": 1,
                "user_id": 1, 
                "review_text": "My review...",
                "rating": 4
            }
            ```

        * Error Responses: 400 (Bad Request) if validation fails (e.g., missing fields, invalid rating), 404 (Not Found) if the book with the given ID does not exist.

    * **`GET /api/reviews/{review_id}`**: Get a specific review by ID.
        * Path Parameters:
            * `review_id` (integer): The ID of the review to retrieve.
        * Response (200 OK):

            ```json
            {
                "id": 3,
                "book_id": 1,
                "user_id": 1,
                "review_text": "My review...",
                "rating": 4
            }
            ```

        * Error Responses: 404 (Not Found) if the review with the given ID does not exist.

    * **`PUT /api/reviews/{review_id}`**: Update a review.
        * Path Parameters:
            * `review_id` (integer): The ID of the review to update.
        * Request Body:

            ```json
            {
                "review_text": "Updated review text",
                "rating": 5
            }
            ```

        * Response (200 OK):

            ```json
            {
                "id": 3,
                "book_id": 1,
                "user_id": 1,
                "review_text": "Updated review text",
                "rating": 5
            }
            ```

        * Error Responses: 400 (Bad Request) if validation fails, 404 (Not Found) if the review with the given ID does not exist.

    * **`DELETE /api/reviews/{review_id}`**: Delete a review.
        * Path Parameters:
            * `review_id` (integer): The ID of the review to delete.
        * Response (204 No Content):
            * (Empty response body)
        * Error Responses: 404 (Not Found) if the review with the given ID does not exist.

* **LLM Endpoints**

    * **`POST /api/books/{book_id}/summary`**: Generate a summary for a book using the local LLM.
        * Path Parameters:
            * `book_id` (integer): The ID of the book to generate a summary for.
        * Response (200 OK):

            ```json
            {
                "summary": "This is a generated summary of the book..."
            }
            ```

        * Error Responses: 404 (Not Found) if the book with the given ID does not exist, 500 (Internal Server Error) if there is an error communicating with the LLM.

    * **`GET /api/books/{book_id}/recommendations`**: Get book recommendations based on the book's content.
        * Path Parameters:
            * `book_id` (integer): The ID of the book to get recommendations for.
        * Response (200 OK):

            ```json
            {
                "recommendations": [
                    "Recommended Book Title 1",
                    "Recommended Book Title 2",
                    "Recommended Book Title 3"
                ]
            }
            ```

        * Error Responses: 404 (Not Found) if the book with the given ID does not exist, 500 (Internal Server Error) if there is an error communicating with the LLM.

##   4. Testing 

This project includes unit tests to ensure the reliability of the API.

1.  **Ensure Pytest is Installed:**

    ```bash
    pip install pytest  #  If you haven't already installed it
    ```

2.  **Running Tests:**

    ```bash
    pytest  #  Runs all tests in the 'tests' directory
    ```

    * **Test Organization:**
        * Tests are located in the `tests/` directory.
        * Test files are typically named `test_*.py` (e.g., `test_api.py`, `test_auth.py`).
        * Test functions are typically named `test_*` (e.g., `test_get_all_books`, `test_create_user`).
    * **Test Fixtures:**
        * Pytest fixtures are used to set up test data and resources.
        * The `test_client` fixture creates a Flask test client that allows you to simulate API requests.
        * The `init_database` fixture populates the test database with sample data before each test.
    * **Test Coverage:**
        * Aim for high test coverage. This means testing as much of your code as possible.
        * Test both successful scenarios (happy paths) and error scenarios (e.g., invalid input, authentication failures, database errors).
    * **Running Specific Tests:**
        * You can run a specific test file: `pytest tests/test_api.py`
        * You can run a specific test function: `pytest tests/test_api.py::test_get_all_books`
    * **Test Output:**
        * Pytest provides detailed output indicating which tests passed, failed, or were skipped.
        * Use the output to identify and fix any issues in your code.

