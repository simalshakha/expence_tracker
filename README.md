# Expense Tracker API

A backend API built with Django and Django REST Framework to manage personal expenses. The API supports secure JWT authentication and provides features for user registration, login, and full CRUD operations on expense and income records.

---

## Project Overview

### Features
- User registration and login with JWT authentication
- CRUD operations for expense and income records
- Automatic tax calculation (flat amount or percentage)
- Pagination support on list endpoints
- Role-based access control (regular users vs superusers)
- Detailed timestamps for records

---

## Technologies Used
- Python
- Django
- Django REST Framework
- Simple JWT (JWT token authentication)
- SQLite (local development)

---

## How to Run the Project Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/simalshakha/expence_tracker.git
   cd expense_tracker


2. Create a virtual environment and activate it:
   For Windows:
   python -m venv venv
   venv\Scripts\activate

   For macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

3. Install all required Python packages:
   pip install -r requirements.txt

4. Apply database migrations:
   python manage.py makemigrations
   python manage.py migrate

5. Create a superuser account to access the admin panel and also for login:
   python manage.py createsuperuser

6. Start the Django development server:
   python manage.py runserver

Now your project is running at:
http://127.0.0.1:8000/

## API Endpoints  

Authentication Endpoints
| Method | Endpoint              | Description                     |
| ------ | --------------------- | ------------------------------- |
| POST   | `/api/auth/register/` | User registration               |
| POST   | `/api/auth/login/`    | User login (returns JWT tokens) |
| POST   | `/api/auth/refresh/`  | Refresh JWT token               |

Expense/Income Endpoints
Method	Endpoint	Description
| Method | Endpoint              | Description                                    |
| ------ | --------------------- | ---------------------------------------------- |
| GET    | `/api/expenses/`      | List user's expense/income records (paginated) |
| POST   | `/api/expenses/`      | Create a new record                            |
| GET    | `/api/expenses/{id}/` | Retrieve a specific record                     |
| PUT    | `/api/expenses/{id}/` | Update a record                                |
| DELETE | `/api/expenses/{id}/` | Delete a record                                |

## Sample API Call: POST /api/expenses/

In Headers:
  Authorization: Bearer <access_token>
  Content-Type: application/json

Body:
{
  "title": "Percentage Tax Test",
  "description": "Test percentage tax calculation",
  "amount": 100.00,
  "transaction_type": "debit",
  "tax": 10.00,
  "tax_type": "percentage"
}

## Notes

- All endpoints are protected and require authentication.
- Use the access token in the headers like this:
  Authorization: Bearer your_access_token_here
- SQLite is used for local development.

## Additional Notes

- Token Expiry:  
  Access tokens are valid for **30 minutes**. After that, use the refresh token at `/api/token/refresh/` to get a new one.

- Date Format:  
  All dates must be in the format `YYYY-MM-DD`.  
  Example: `2025-06-30`



- Authentication Header:
  All API endpoints require authentication using a JWT access token.  
  In Postman (or any API testing tool), include this in the Headers tab:
  Key: Authorization
  Value: Bearer <your_access_token>

- Recommended Tool for Testing:  
  Use **Postman** to test API endpoints. Make sure to:
  1. First, obtain your access and refresh token by calling `/api/auth/login/`.
  2. Then, add the access token to the `Authorization` header as shown above.
 
-Contact
 For any questions or feedback, feel free to open an issue or contact me at sshakha350@gmail.com.
