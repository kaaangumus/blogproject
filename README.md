# Blog Project

A legacy Flask and MySQL blog application built as a learning project.

## Status

Beta / legacy project. This repository is kept for learning history and should be reviewed before any real deployment.

## Features

- Flask-based web application
- MySQL database usage
- Blog post pages
- Admin panel routes
- Basic user/profile-related forms
- Image upload handling for posts

## Project Files

```text
main.py          Flask application
veritabanı.sql   Database schema / SQL dump
templates/       HTML templates
static/          Static assets
js/              Frontend JavaScript assets
```

## Local Setup

Install the likely Python dependencies:

```bash
pip install flask flask-mysqldb flask-wtf wtforms passlib
```

Import the database schema from `veritabanı.sql`, then update the MySQL settings in `main.py` for your local environment.

Run the app:

```bash
python main.py
```

## Security Notes

This is an old learning project. Before using it beyond a local lab, review and improve:

- Secret key handling
- Database credentials
- Authentication and session security
- Input validation
- File upload restrictions
- Dependency management
- Encoding issues in Turkish text

## License

See [LICENSE](LICENSE).
