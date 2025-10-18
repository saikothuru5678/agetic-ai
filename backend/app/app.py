from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
from .config import get_settings
from .schemas import FeedbackCreate, FeedbackOut
from .db.database import Base, engine, get_db
from .db import models
from .ai.agent import analyze_feedback
import json, os

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

# Mount static frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

def _seed_if_empty(db: Session):
    empty = db.query(models.Feedback).count() == 0
    if not empty or not settings.load_sample_on_boot:
        return
    sample_path = os.path.join(FRONTEND_DIR, "sample_data.json")
    if os.path.exists(sample_path):
        with open(sample_path, "r") as f:
            items = json.load(f)
        for it in items:
            analysis = analyze_feedback(it["text"])
            row = models.Feedback(
                parent_name=it.get("parent_name"),
                parent_email=it.get("parent_email"),
                text=it["text"],
                sentiment=analysis["sentiment"],
                category=analysis["category"],
                department=analysis["department"],
            )
            db.add(row)
        db.commit()

@app.on_event("startup")
def on_startup():
    db = next(get_db())
    _seed_if_empty(db)

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/feedback", response_model=FeedbackOut)
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Feedback text cannot be empty.")
    analysis = analyze_feedback(payload.text)
    row = models.Feedback(
        parent_name=payload.parent_name,
        parent_email=payload.parent_email,
        text=payload.text,
        sentiment=analysis["sentiment"],
        category=analysis["category"],
        department=analysis["department"],
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row

@app.get("/api/feedback", response_model=List[FeedbackOut])
def list_feedback(
    sentiment: Optional[str] = Query(None, pattern="^(positive|negative|neutral)$"),
    department: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Feedback)
    if sentiment:
        q = q.filter(models.Feedback.sentiment == sentiment)
    if department:
        q = q.filter(models.Feedback.department == department)
    q = q.order_by(models.Feedback.id.desc())
    return q.all()

from fastapi.responses import HTMLResponse
def _read_file(name: str) -> str:
    path = os.path.join(FRONTEND_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

@app.get("/", response_class=HTMLResponse)
def index_page():
    return _read_file("index.html")

@app.get("/admin", response_class=HTMLResponse)
def admin_page():
    return _read_file("admin.html")