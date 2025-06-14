# Teacher Attendance App

## Overview
The Teacher Attendance App is a web application designed to manage teacher attendance, course management, semester management, scheduling, and teacher assignments. This application is built using Python with a Flask backend and a simple frontend.

## Features
1. **Course Management**: Add, edit, and delete courses with details such as course ID, name, and department.
2. **Semester Management**: Manage semesters, including adding, editing, and deleting semesters, and associating courses with semesters.
3. **Schedule Management**: Create and manage class schedules.
4. **Teacher Assignment**: Assign teachers to courses and manage teacher information, including qualifications and department.
5. **Statistics**: Generate reports and statistics related to courses, semesters, and teacher assignments.

## Project Structure
```
teacher-attendance-app
├── backend
│   ├── app.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── subject.py
│   │   ├── semester.py
│   │   ├── schedule.py
│   │   ├── teacher.py
│   │   └── assignment.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── subjects.py
│   │   ├── semesters.py
│   │   ├── schedules.py
│   │   ├── teachers.py
│   │   └── assignments.py
│   ├── database.py
│   └── config.py
├── frontend
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── main.js
│   └── templates
│       ├── base.html
│       ├── index.html
│       ├── subjects.html
│       ├── semesters.html
│       ├── schedules.html
│       ├── teachers.html
│       └── assignments.html
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/teacher-attendance-app.git
   ```
2. Navigate to the project directory:
   ```
   cd teacher-attendance-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Start the backend server:
   ```
   python backend/app.py
   ```
2. Open your web browser and go to `http://localhost:5000` to access the application.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
