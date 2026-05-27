# PayPal Integration with FastAPI

A professional PayPal payment integration built with FastAPI, featuring a modern Bootstrap UI, database storage, and dynamic amount input.

## Features

- Dynamic Amount Input
- Professional Bootstrap UI
- SQLite Database Storage
- Auto-capture payments
- PayPal Sandbox integration
- Error handling

## Project Structure

paypal/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── paypal.py
│   ├── services.py
│   └── database.py
├── templates/
│   ├── index.html
│   ├── success.html
│   └── cancel.html
├── uploads/
├── requirements.txt
└── README.md

## Setup

pip install -r requirements.txt

## Run

uvicorn app.main:app --reload

App runs at:
http://127.0.0.1:8000

## API

POST /create-payment  
GET /success  
POST /capture/{order_id}