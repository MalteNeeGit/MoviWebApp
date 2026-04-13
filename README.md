[README.md](https://github.com/user-attachments/files/26646334/README.md)
# 🎬 MoviWeb

> Deine persönliche Filmsammlung – minimalistisch, schnell, stylish.

![Python](https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.1-black?style=flat-square&logo=flask)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## 📖 Über das Projekt

MoviWeb ist eine Web-App mit der du deine Lieblingsfilme verwalten kannst. Nutzer können sich registrieren, Filme über die **OMDb API** suchen und ihrer persönlichen Sammlung hinzufügen.

Das Design ist inspiriert von modernen Streaming-Plattformen – dunkel, clean und cineastisch.

---

## ✨ Features

- 👤 Mehrere Nutzerprofile mit Avatar
- 🎥 Filme per Titel suchen (OMDb API)
- 🖼️ Automatisches Poster, Regisseur & Jahr
- ✏️ Filmtitel bearbeiten
- 🗑️ Filme und Nutzer löschen
- ⚡ Flash-Nachrichten bei Fehlern
- 📱 Responsives Layout

---

## 🛠️ Tech Stack

| Technologie | Verwendung |
|---|---|
| Python 3.10 | Backend |
| Flask | Web Framework |
| SQLAlchemy | ORM / Datenbank |
| SQLite | Datenbank |
| Jinja2 | Templating |
| OMDb API | Filmdaten |
| HTML / CSS | Frontend |

---

## 🚀 Installation

```bash
# Repository klonen
git clone https://github.com/MalteNeeGit/MoviWebApp
cd MoviWebApp

# Virtuelle Umgebung erstellen
python3 -m venv .venv
source .venv/bin/activate

# Abhängigkeiten installieren
pip install -r requirements.txt
```

### Umgebungsvariablen

Erstelle eine `.env` Datei im Projektordner:

```
OMDB_API_KEY=dein_api_key
SECRET_KEY=dein_secret_key
```

Einen kostenlosen OMDb API Key gibt es unter [omdbapi.com](https://www.omdbapi.com/apikey.aspx).

### App starten

```bash
python app.py
```

Die App läuft dann unter `http://127.0.0.1:5000`

---

## 📁 Projektstruktur

```
MoviWebApp/
├── app.py               # Flask Routen & Logik
├── data_manager.py      # Datenbankoperationen
├── models.py            # SQLAlchemy Models
├── requirements.txt
├── .env                 # API Keys (nicht in Git!)
├── data/
│   └── movies.db        # SQLite Datenbank
├── static/
│   ├── style.css
│   └── logo.png
└── templates/
    ├── base.html
    ├── index.html
    ├── movies.html
    ├── update_movie.html
    ├── 404.html
    └── 500.html
```

---

## 🌐 Deployment

Die App ist deployed auf **PythonAnywhere**:

🔗 [MalteMasterschoolProject.pythonanywhere.com](https://MalteMasterschoolProject.pythonanywhere.com)

---
