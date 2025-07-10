from fastapi import FastAPI, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi import Request
from .database import Base, engine, SessionLocal, User, Request as DelRequest
import json

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple auth placeholder

def authenticate(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and bcrypt.verify(password, user.hashed_password):
        return user
    return None

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register")
def register(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email exists")
    user = User(email=email, hashed_password=bcrypt.hash(password))
    db.add(user)
    db.commit()
    return {"message": "registered"}

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "logged_in", "admin": user.is_admin}

@app.post("/request")
def send_request(contact: str = Form(...), user_email: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    brokers = json.load(open("data_brokers.json"))
    req = DelRequest(user_id=user.id, contact=contact, status="sent")
    db.add(req)
    db.commit()
    # Placeholder for sending emails
    return {"brokers_notified": [b["name"] for b in brokers]}

@app.get("/admin", response_class=HTMLResponse)
def admin_panel(request: Request, email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate(db, email, password)
    if not user or not user.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    requests = db.query(DelRequest).all()
    users = db.query(User).all()
    return templates.TemplateResponse(
        "admin.html", {"request": request, "requests": requests, "users": users}
    )
