# Book Management System with Python Flask and MySQL

## Project Overview

This project implements a book management system using Python Flask for the backend and MySQL for database storage. The system allows users to perform basic CRUD operations (Create, Read, Update, Delete) on books stored in the database. It also includes user authentication to secure access to the system.

## Features

- **CRUD Operations**: Allows users to add new books, view existing books, update book details, and delete books from the database.
- **User Authentication**: Secure access to the system with user login and session management.
- **Persistence**: Stores book information securely in a MySQL database.
- **Scalability**: Designed to handle a growing library of books efficiently.

## Technologies Used

- Python 3
- Flask
- MySQL

## Installation and Setup

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```

2. **Setup virtual environment (optional but recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**

**1. Install MySQL and create a new database.**
**2. Update the database configuration in `config.py` or `db_service.py` with your MySQL credentials.**

5. **Run the application**

   ```bash
   python app.py
   ```

## Future Enhancements

### Filtering Options

**Enhance the system with filtering capabilities to allow users to search and sort books based on various attributes**

**These features are planned enhancements for the project to improve security and usability, providing more control and flexibility in managing book data.**
