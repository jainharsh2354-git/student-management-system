# 🎓 Student Management System

## Description
A full-stack web application to **add, search, update and delete** student records (CRUD).
The frontend (HTML/CSS/JavaScript) talks to a **Python Flask** REST API using the Fetch API and JSON.
Data is stored persistently in **SQLite**. The list and search results update dynamically without reloading the page.

## Features
- Add, view, edit and delete students (Name, Roll No, Class, Marks, Contact)
- Live search by name or roll number
- Validation on both client and server (required fields, marks 0–100, 10-digit contact, **unique roll number**)
- Proper error handling (duplicate roll no, non-existent student, empty search results)

## Technologies Used
- **Frontend:** HTML5, CSS3, JavaScript (Fetch API); Node.js/npm for tooling scripts
- **Backend:** Python 3, Flask
- **Database:** SQLite

## Project Structure
```
student-management-system/
├── app.py              # Flask backend + REST API
├── requirements.txt
├── package.json        # Node.js tooling scripts
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md
```

## How to Run
1. Clone the repository
   ```bash
   git clone <your-repo-url>
   cd student-management-system
   ```
2. (Optional) Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Start the server
   ```bash
   python app.py        # or: npm start
   ```
5. Open **http://127.0.0.1:5000** in your browser.

The SQLite database (`students.db`) is created automatically on first run.

## API Endpoints
| Method | Endpoint              | Description                          |
|--------|-----------------------|--------------------------------------|
| GET    | `/api/students`       | List all students (`?q=` to search)  |
| POST   | `/api/students`       | Add a new student                    |
| PUT    | `/api/students/<id>`  | Update a student                     |
| DELETE | `/api/students/<id>`  | Delete a student                     |

## Testing
Verified: add/update/delete, search by name & roll no, duplicate roll number (409), invalid marks/contact (400),
updating/deleting non-existent student (404), searching a non-existent student (empty list).

## Author
<Your Name>
