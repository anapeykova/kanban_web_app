# Kanban Web App

A simple web app to help users stay on top of work by keeping track of tasks. Responsive design, minimalist style, intuitive layout.

## Stack

<ul>
<li>Python
<li>Flask
<li>html
<li>CSS
<li>Boostrap 5
</ul>

## Features

### <a href="https://www.loom.com/share/b74b0c4d132544edaf81602d76b8ddce">Watch the demo </a>

### Task Management

- Users can create tasks.
- Tasks can be marked high priority, displayed with a yellow badge for better visibility.
- Tasks can have different status - to-do, doing & done - and are displayed accordingly in 3 columns.
- Tasks are sorted by date modified, in ascending order (oldest tasks appear on top).
- Users can edit, change status and delete tasks.

### User Authentication

- Access to the task board is managed through user authentication with unique username and password.
- Users only have access to their own task board.
- Passwords are stored hashed for security.

## Getting Started

### Clone the repository

```bash
git clone
```

### Installing

Once you have the repository on your computer, open Terminal, navigate to the main directory (kanban_web_app) and run the following:
**macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

**Windows:**

```bash
python -m venv venv
venv/Scripts/activate.bat
pip3 install -r requirements.txt
python app.py
```

## Testing

To run existing tests run the following from the main directory:

```bash
python -m unittest discover
```

To get report on coverage, run the following:

```bash
pip install coverage
coverage run -m unittest discover
coverage report
```
