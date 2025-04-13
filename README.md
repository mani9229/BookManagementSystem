#   Intelligent Book Management System

##   1.   Introduction

The   Intelligent Book Management System is a RESTful API designed to manage books and reviews efficiently. It leverages a locally running Large Language Model (LLM) through Ollama to provide intelligent features like book summaries and recommendations. This   system is built using FastAPI, a modern, high-performance Python web framework, and PostgreSQL as its database. Docker   and Docker Compose are employed to simplify development and deployment, ensuring a consistent environment across different systems.

##   2.   Features

* **Book Management:**
    * Create, read, update, and delete book records.
    * Retrieve detailed information about individual books.
    * List all books available in the system.
* **Review Management:**
    * Add, read, update, and delete reviews for books.
    * Retrieve all reviews associated with a specific book.
    * User authentication is required to post or modify reviews.
* **LLM Integration:**
    * Generate summaries for books using a local LLM through Ollama.
    * Provide book recommendations based on the content of a given book.
* **User Authentication:**
    * Secure user registration and login using JSON Web Tokens (JWT).
    * Protected API endpoints require authentication.
* **API Documentation:**
    * Interactive API documentation using Swagger UI.
* **Containerization:**
    * Docker and Docker Compose for easy setup and deployment.
    * Consistent development and production environments.
* **Asynchronous Operations:**
    * Leverages FastAPI's asynchronous capabilities for improved performance.

##   3.   Technologies Used

* FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
* SQLAlchemy: The Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
* asyncpg: A fast PostgreSQL Database Client Library for Python/asyncio.
* python-dotenv: Reads key-value pairs from a `.env` file and can set them as environment variables.
* jose: A JavaScript Object Signing and Encryption (JOSE) for Python.
* llama.cpp: Library for Llama model integration.
* pytest: The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing.
* Docker: A tool that enables developers to package applications into containers—standardized executable components combining application source code with the operating system (OS) libraries and dependencies required to run that code in any environment.
* Docker Compose: A tool for defining and running multi-container Docker applications.
* Swagger UI: A collection of HTML, Javascript, and CSS assets that dynamically generate beautiful documentation from a Swagger-compliant API.
* PostgreSQL: A powerful, open source object-relational database system.
* Ollama: A library for running language models locally.

##   4.   API Endpoints

* `/auth/register/` (POST): Register a new user.
* `/auth/token` (POST): Authenticate and obtain a JWT.
* `/api/books/` (GET): Get all books.
* `/api/books/` (POST): Add a new book.
* `/api/books/{book_id}` (GET): Get a book by ID.
* `/api/books/{book_id}` (PUT): Update a book.
* `/api/books/{book_id}` (DELETE): Delete a book.
* `/api/books/{book_id}/reviews/` (GET): Get reviews for a book.
* `/api/books/{book_id}/reviews/` (POST): Add a review to a book.
* `/api/books/{book_id}/summary/` (GET): Generate a book summary.
* `/api/books/{book_id}/recommendations/` (GET): Get book recommendations.



##   5.   Setup

1.  **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <repository_name>
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure environment variables:**

    * Create a `.env` file in the root directory.
    * Copy the contents of `.env.example` into `.env` and fill in the values.

5.  **Run the application:**

    ```bash
    python run.py
    ```

6.  **Access the API documentation:**

    * Open your browser and navigate to `http://localhost:8000/docs`.

##   6.   Running with Docker

1.  **Build the Docker image:**

    ```bash
    docker build -t book-management-system .
    ```

2.  **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 book-management-system
    ```

    Or, use Docker Compose:

    ```bash
    docker-compose up --build
    ```

##   7.   Testing

* Run unit tests using pytest:

    ```bash
    pytest
    ```

    * Tests are located in the `tests/` directory.


##   8.   LLM Model Setup

* Download your chosen Llama 2 model and place it in the directory specified by `LLAMA_MODEL_PATH` in your `.env` file.
* If using Ollama, follow the Ollama installation instructions and pull/run the model.
* Ensure you have sufficient resources (RAM, GPU if possible) to run the model locally.
