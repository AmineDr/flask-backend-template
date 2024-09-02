# Flask Backend Template with JWT Authentication

This repository is a Flask backend template designed to kickstart your web application development. It includes essential boilerplate code for setting up a robust authentication system using JWT (JSON Web Tokens). The template features a user model with login and registration endpoints, complete with input validation to ensure data integrity. The project is structured to follow best practices, making it easy to extend and customize according to your needs.

## Key Features:
- JWT-based authentication
- User model with login and registration boilerplate
- Validators for each action to ensure secure and reliable operations
- Environment configuration through `.env` file
- MySQL database integration

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.x
- MySQL
- Git (optional)

## Getting Started

Follow the steps below to set up and run the Flask backend.

### 1. Clone the Repository

Clone this repository to your local machine
using `git clone --depth 1 git@github.com:AmineDr/flask-backend-template.git` or download it as a zip file.

### 2. Create a Python Virtual Environment

A virtual environment helps to isolate the dependencies required by your project. To create a virtual environment, navigate to your project directory and run:

    python3 -m venv venv

This will create a directory named `venv` in your project folder.

### 3. Activate the Virtual Environment

Before installing any dependencies, activate the virtual environment. The activation command differs based on your operating system:

- **For Windows:**

    ```bash
    venv\Scripts\activate
    ```

- **For macOS/Linux:**

    ```bash
    source venv/bin/activate
    ```

Once activated, your terminal will show the name of the environment in the prompt.

### 4. Install Requirements

With the virtual environment activated, install the required dependencies using `pip`. These dependencies are listed in the `requirements.txt` file. Run the following command:

    pip install -r requirements.txt

This command will install all the necessary Python packages needed to run the Flask backend.

### 5. Setup MySQL User

Next, set up a MySQL user and database that the Flask application will use. Follow these steps:

1. Log in to MySQL as the root user:

    ```bash
    mysql -u root -p
    ```

2. Create a new database:

    ```sql
    CREATE DATABASE fbt_app_db;
    ```

3. Create a new user and grant them privileges on the database:

    ```sql
    CREATE USER 'fbt_user'@'localhost' IDENTIFIED BY 'fbt_pass';
    GRANT ALL PRIVILEGES ON fbt_app_db.* TO 'fbt_user'@'localhost';
    FLUSH PRIVILEGES;
    ```

4. Exit the MySQL shell:

    ```sql
    EXIT;
    ```

### 6. Create `.env` File

The application uses environment variables for configuration, which are stored in a `.env` file. To set up your environment variables:

1. Copy the `.env.example` file to `.env`:

    ```bash
    cp .env.example .env
    ```

2. Open the `.env` file in a text editor and modify the variables to suit your setup, especially the database credentials:

    ```plaintext
    DB_NAME=fbt_app_db
    DB_USER=fbt_user
    DB_PASSWORD=fbt_pass
    DB_HOST=localhost
    DB_PORT=3306
    ```

### 7. Run the Application

With everything set up, you can now run the Flask application. Use the following command:

    python main.py

The application should now be running on `http://127.0.0.1:5000/`.
And you're done! You can now start developing your web application.

* Note: The application will automatically create the database tables if they don't exist.

## Additional Notes

- Ensure your MySQL server is running before starting the Flask application.
- If you need to install additional packages, add them to `requirements.txt` and run `pip install -r requirements.txt` again.
- You can deactivate the virtual environment at any time by running `deactivate` in the terminal.
