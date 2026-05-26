from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path

from app.services import initiate_payment, confirm_payment
from app.database import init_db, get_db
from app.database import Payment as PaymentModel
from sqlalchemy.orm import Session

class PaymentRequest(BaseModel):
    amount: float

app = FastAPI()

# Mount uploads directory for static files
app.mount("/uploads", StaticFiles(directory=Path(__file__).parent.parent / "uploads"), name="uploads")

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

templates = Jinja2Templates(directory=Path(__file__).parent.parent / "templates")


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# HOME
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# CREATE ORDER
@app.post("/create-payment")
def create_payment(request: PaymentRequest):
    return initiate_payment(request.amount)


# SUCCESS PAGE
@app.get("/success", response_class=HTMLResponse)
def success(request: Request, token: str, amount: str = "10.00"):
    return templates.TemplateResponse(
        "success.html",
        {"request": request, "token": token, "amount": amount}
    )


# CANCEL PAGE
@app.get("/cancel", response_class=HTMLResponse)
def cancel(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})


# CAPTURE PAYMENT
@app.post("/capture/{order_id}")
def capture(order_id: str, amount: str = "10.00", db: Session = Depends(get_db)):
    result = confirm_payment(order_id)
    
    # Store payment in database if successful
    if result["status"] in ["COMPLETED", "APPROVED"]:
        payment = PaymentModel(
            payment_id=result["order_id"],
            payer_id="",
            payer_name="",
            payer_email="",
            item_id="",
            item_name="Course Purchase",
            currency="USD",
            amount=amount,
            status=result["status"]
        )
        db.add(payment)
        db.commit()
        db.refresh(payment)
        
        result["db_id"] = payment.id
    
    return result