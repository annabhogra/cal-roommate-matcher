# Cal Roommate Matcher

Roommate matching platform for Berkeley students. Sign up with your @berkeley.edu email, fill out your living preferences, and get matched with compatible students based on sleep schedule, cleanliness, noise tolerance, budget, and neighborhood.


## Stack

- Python / Flask
- SQLAlchemy + SQLite (dev) / PostgreSQL (prod)
- Bootstrap 5
- Deployed on AWS EC2

## Running locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

App runs at `http://localhost:5000`.

## Environment variables

Copy `.env.example` to `.env` and fill in:

```
SECRET_KEY=...
DATABASE_URL=...   # optional, defaults to SQLite
```

## Matching algorithm

Scores each pair of users across weighted features — sleep schedule (3×), cleanliness (2×), noise tolerance (2×), guest/smoking compatibility, neighborhood, and budget overlap. Returns a 0–100% compatibility score.
