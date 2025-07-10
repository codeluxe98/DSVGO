from fastapi import FastAPI, Depends, Form, HTTPException

from fastapi.responses import HTMLResponse, FileResponse

from fastapi.responses import HTMLResponse

from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi import Request

from .database import (
    Base,
    engine,
    SessionLocal,
    User,
    Request as DelRequest,
    Broker,
    Log,
)
import json
import os
from fpdf import FPDF
from .database import Base, engine, SessionLocal, User, Request as DelRequest
import json


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def load_brokers():
    db = SessionLocal()
    if db.query(Broker).count() == 0:
        brokers = json.load(open("data_brokers.json"))
        for b in brokers:
            db.add(Broker(name=b["name"], email=b["email"]))
        db.commit()
    db.close()

# simple email and pdf helpers

def send_email(to_email: str, subject: str, body: str):
    """Placeholder for sending email."""
    print(f"Sending email to {to_email}: {subject}\n{body}")


def generate_pdf(request_id: int, brokers: list[str]) -> str:
    os.makedirs("pdfs", exist_ok=True)
    path = f"pdfs/request_{request_id}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, txt="Brokers notified:", ln=1)
    for b in brokers:
        pdf.cell(0, 10, txt=b, ln=1)
    pdf.output(path)
    return path

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

    db.add(Log(user_id=user.id, action="register"))
    db.commit()
    send_email(user.email, "Registration", "Welcome to the DSGVO tool")

    return {"message": "registered"}

@app.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    db.add(Log(user_id=user.id, action="login"))
    db.commit()

    return {"message": "logged_in", "admin": user.is_admin}

@app.post("/request")
def send_request(contact: str = Form(...), user_email: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    brokers = db.query(Broker).all()
    req = DelRequest(user_id=user.id, contact=contact, status="sent")
    db.add(req)
    db.commit()
    broker_names = []
    for b in brokers:
        send_email(b.email, "Delete data", f"Please delete data for {contact}")
        broker_names.append(b.name)
    pdf_path = generate_pdf(req.id, broker_names)
    req.pdf_path = pdf_path
    db.add(Log(user_id=user.id, request_id=req.id, action="delete_request"))
    db.commit()
    send_email(user.email, "Deletion request sent", "Your request has been sent to brokers.")
    return {"brokers_notified": broker_names, "request_id": req.id}


@app.get("/request/{req_id}/pdf")
def request_pdf(req_id: int, db: Session = Depends(get_db)):
    req = db.query(DelRequest).filter(DelRequest.id == req_id).first()
    if not req or not req.pdf_path:
        raise HTTPException(status_code=404, detail="Request not found")
    return FileResponse(req.pdf_path, media_type="application/pdf")
=======
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



@app.post("/admin/user/{user_id}/make_admin")
def make_admin(user_id: int, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin = authenticate(db, email, password)
    if not admin or not admin.is_admin:
        raise HTTPException(status_code=403, detail="Forbidden")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = True
    db.add(Log(user_id=admin.id, action=f"made {user.email} admin"))
    db.commit()
    return {"status": "ok"}


