# TakaSmart — Full Flask + MySQL Project

TakaSmart is a waste-management web application based on the uploaded TakaSmart HTML design.

## Included
- Responsive TakaSmart frontend
- Waste-area reporting with photo upload
- Leaflet map for selecting report location
- Waste identification/recycling guidance
- Waste-buyer search
- Buyer registration
- Multilingual UI: Kiswahili, English, French
- Waste-management chatbot
- Flask REST API
- MySQL persistence
- Uploaded report photos saved under `static/uploads/`
- `/health` endpoint for testing

## Folder structure

TakaSmart_Project/
├── app.py
├── database.py
├── classifier.py
├── chatbot.py
├── requirements.txt
├── .env.example
├── README.md
├── database/
│   └── schema.sql
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   └── style.css
    ├── js/
    │   └── app.js
    └── uploads/

## Windows + VS Code setup

1. Install Python 3.11+.
2. Install MySQL Server and make sure MySQL is running.
3. Open this folder in VS Code.
4. Open Terminal and run:

   python -m venv venv

5. Activate it:

   PowerShell:
   .\venv\Scripts\Activate.ps1

   Command Prompt:
   venv\Scripts\activate

6. Install packages:

   pip install -r requirements.txt

7. Copy `.env.example` to `.env`.

8. Put your MySQL password in `.env`:

   DB_USER=root
   DB_PASSWORD=YOUR_MYSQL_PASSWORD

9. Start the app:

   python app.py

10. Open:

   http://127.0.0.1:5000

The app automatically creates the `taka_smart` database and its tables when `app.py` starts.

## If automatic database creation fails

Open MySQL Workbench or the MySQL command line and run:

    source database/schema.sql

Then run:

    python app.py

## Important note about image AI

The included `classifier.py` is a clearly marked demo classifier. It does not pretend to be a real computer-vision model. It uses the uploaded filename as a simple demonstration signal and defaults to plastic.

To make the "Tambua Taka" feature a real AI image classifier, replace `classify_waste()` with a trained TensorFlow, PyTorch, YOLO, or external vision API model. The Flask API route is already prepared for that replacement.

## API endpoints

GET  /api/stats
GET  /api/reports
POST /api/reports
GET  /api/buyers
POST /api/buyers
POST /api/identify
POST /api/chat
GET  /health

## Common problems

### `ModuleNotFoundError: No module named 'flask'`
Activate the virtual environment and run:

    pip install -r requirements.txt

### MySQL connection error
Check:
- MySQL service is running
- DB_HOST is correct
- DB_PORT is correct
- DB_USER is correct
- DB_PASSWORD is correct

### Port already in use
Change `PORT=5001` in `.env`, then restart.

### Map is blank
Internet access is needed because Leaflet and OpenStreetMap tiles are loaded from CDNs.

## Source design

The original uploaded `TakaSmart.html` design was separated into:
- `templates/index.html`
- `static/css/style.css`
- `static/js/app.js`

The original visual structure, colors, sections, maps, chatbot UI, buyer cards and waste categories are retained.
