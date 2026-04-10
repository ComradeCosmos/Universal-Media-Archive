# Universal Media Archive 📚🎬🎵

A metadata-rich media discovery and aggregation platform inspired by the Internet Archive. Centralize, search, and explore all forms of human media — movies, books, music, games, comics, podcasts, and more — through a unified system that links to external sources without hosting copyrighted content.

## Project Structure
The main application is housed within the `universal-media-archive` subfolder:
```text
universal-media-archive/
├── backend/            # Flask REST API (Python)
├── frontend/           # Vanilla HTML/CSS/JS web dashboard
├── scripts/            # Database seeding and utilities
└── data/               # Source data
```

## Quick Start

### 1. Database Setup
You will need an instance of MongoDB running locally or remotely on port `27017`.
```bash
# Verify it's running:
mongosh --eval "db.adminCommand('ping')"
```

### 2. Backend API
The backend exposes all search and analytics endpoints on `http://localhost:5000`.

```bash
cd universal-media-archive/backend
pip install -r requirements.txt
python app.py
```
*Note: A Virtual Environment (`venv`) should ideally be used for installing dependencies.*

### 3. Database Seeding (Optional)
To populate the database with some starting media, run the seed script:
```bash
cd universal-media-archive/scripts
python seed.py
```

### 4. Frontend Web App
The frontend is a vanilla single-page application. You can view it by simply launching an HTTP server in the `frontend` directory:
```bash
cd universal-media-archive/frontend
python -m http.server 3000
```
Then visit **http://localhost:3000** in your web browser.

---

*This GitHub repository serves as the complete backup of the application including the customized local virtual environment (`venv`). Please consult the inner `universal-media-archive/README.md` for a complete breakdown of the MongoDB Schemas, API Endpoints, and extensive architectural documentation.*
