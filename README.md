# PayPal Integration with FastAPI

A professional PayPal payment integration built with FastAPI, featuring a modern Bootstrap UI, database storage, and dynamic amount input.

## Features

- **Dynamic Amount Input**: Users can enter any payment amount
- **Professional UI**: Bootstrap 5 styled pages with PayPal branding
- **Database Storage**: SQLite database for payment records
- **Auto-capture**: Automatic payment capture on success page
- **Error Handling**: Comprehensive error handling for PayPal API responses
- **Static File Serving**: Course images served via FastAPI

## Project Structure

```
paypal/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application and routes
│   ├── config.py            # PayPal credentials configuration
│   ├── paypal.py            # PayPal API integration
│   ├── services.py          # Business logic for payments
│   └── database.py          # SQLAlchemy database setup
├── templates/
│   ├── index.html           # Payment page with amount input
│   ├── success.html         # Success page with payment details
│   └── cancel.html          # Cancellation page
├── uploads/                 # Static course images
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd paypal
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure PayPal credentials**
   
   Edit `app/config.py` with your PayPal Sandbox credentials:
   ```python
   PAYPAL_CLIENT_ID = "your-client-id"
   PAYPAL_SECRET = "your-secret"
   PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"
   ```

   To get PayPal Sandbox credentials:
   - Go to [PayPal Developer Dashboard](https://developer.paypal.com/dashboard/)
   - Create a Sandbox account
   - Create an App and get your Client ID and Secret

## Running the Application

Start the FastAPI server with auto-reload:
```bash
uvicorn app.main:app --reload
```

The application will be available at: `http://127.0.0.1:8000`

## Usage

1. **Access the home page**: Navigate to `http://127.0.0.1:8000`
2. **Enter amount**: Input the desired payment amount in USD
3. **Pay with PayPal**: Click the PayPal button to proceed
4. **Complete payment**: Log in to PayPal and approve the payment
5. **View success**: See payment details on the success page

## API Endpoints

### `POST /create-payment`
Creates a PayPal order with the specified amount.

**Request Body:**
```json
{
  "amount": 10.00
}
```

**Response:**
```json
{
  "order_id": "ORDER_ID",
  "approve_link": "PAYPAL_APPROVE_URL",
  "amount": "10.00"
}
```

### `GET /success`
Success page after PayPal approval.

**Query Parameters:**
- `token`: PayPal order ID
- `amount`: Payment amount

### `GET /cancel`
Cancellation page when payment is cancelled.

### `POST /capture/{order_id}`
Captures the PayPal payment and stores it in the database.

**Query Parameters:**
- `amount`: Payment amount

**Response:**
```json
{
  "status": "COMPLETED",
  "order_id": "ORDER_ID",
  "amount": "10.00",
  "db_id": 1
}
```

## Database

The application uses SQLite for payment storage. The database file (`paypal.db`) is created automatically on first run.

### Payment Table Structure

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| payment_id | String | PayPal payment ID |
| payer_id | String | PayPal payer ID |
| payer_name | String | Payer name |
| payer_email | String | Payer email |
| item_id | String | Item ID |
| item_name | String | Item name |
| currency | String | Currency code (USD) |
| amount | String | Payment amount |
| status | String | Payment status |
| created_at | DateTime | Creation timestamp |

## Environment Variables

You can optionally use a `.env` file for configuration:

```env
PAYPAL_CLIENT_ID=your-client-id
PAYPAL_SECRET=your-secret
PAYPAL_BASE_URL=https://api-m.sandbox.paypal.com
```

## Error Handling

The application handles various error scenarios:

- **Invalid Amount**: Validates user input before creating order
- **PayPal API Errors**: Catches and displays PayPal API errors
- **Already Captured**: Handles duplicate capture attempts gracefully
- **Network Errors**: Displays user-friendly error messages

## Production Deployment

For production deployment:

1. **Use PayPal Live API**: Change `PAYPAL_BASE_URL` to `https://api-m.paypal.com`
2. **Use Production Credentials**: Replace sandbox credentials with live credentials
3. **Use Production Database**: Consider using PostgreSQL or MySQL instead of SQLite
4. **Add HTTPS**: Ensure your application uses HTTPS
5. **Environment Variables**: Use environment variables for sensitive data
6. **Static File Serving**: Use a CDN or proper static file server for uploads

## Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `requests` - HTTP client for PayPal API
- `jinja2==3.1.2` - Template engine
- `starlette==0.27.0` - ASGI toolkit
- `sqlalchemy` - Database ORM
- `python-dotenv` - Environment variable management

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please refer to:
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [PayPal API Documentation](https://developer.paypal.com/docs/api/)
