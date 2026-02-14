# Customers and Orders API

A robust **Django REST API** designed to manage customers and their orders. The system is secured with **OpenID Connect (OIDC)** and **JWT-based authentication** and includes automated **SMS notifications** upon order creation.
This is the api url
https://customers-and-orders-api.onrender.com/

---

## Table of Contents

1. [Features](#features)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Environment Variables](#environment-variables)
4. [API Endpoints](#api-endpoints)
5. [Running Tests](#running-tests)
6. [Docker Deployment](#docker-deployment)
7. [CI/CD Pipeline](#cicd-pipeline)

---

## Features

- 🔒 **Secure Authentication:** User authentication is handled via **OpenID Connect (OIDC)** and secured with **JWTs**.
- ⚙️ **Core Functionality:** Full **CRUD** operations for **Customers** and **Orders**.
- 📞 **SMS Notifications:** Customers receive an SMS notification automatically when a new order is created.
- 🧪 **Quality Assurance:** Comprehensive API testing using **`pytest`** with detailed **coverage** reports.
- 📦 **Containerization:** **Dockerized** for consistent development and easy deployment.
- 🚀 **CI/CD:** Continuous Integration and Deployment automated with **GitHub Actions** and **Render**.

---

## Getting Started

### Prerequisites

To run this project, you will need the following installed;:

- **Python 3.13**
- **pip**
- **Docker** (for containerization)
- **OIDC Credentials** (from your identity provider)
- **Africa’s Talking Account** (optional, required for SMS functionality)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone (https://github.com/PatrickBett/Customers-and-Orders-API.git)
    cd Customers-and-Orders-API
    ```

2.  **Navigate and Create a virtual environment:**

    ```bash
    cd marketplace
    python -m venv venv
    source venv/bin/activate   # Mac/Linux
    venv\Scripts\activate      # Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API is now running and accessible at `http://127.0.0.1:8000/`.

---

## Environment Variables

The following variables must be set in a local **`.env`** file (located in the `marketplace/` directory) or configured as **GitHub Secrets** for CI/CD.

````ini
# Django Settings
SECRET_KEY=your_django_secret_key

# OpenID Connect (OIDC) Configuration
OIDC_RP_CLIENT_ID=your_oidc_client_id
OIDC_RP_CLIENT_SECRET=your_oidc_client_secret
OIDC_OP_ISSUER=your_oidc_issuer_url
OIDC_OP_AUTHORIZATION_ENDPOINT=...
OIDC_OP_TOKEN_ENDPOINT=...
OIDC_OP_USER_ENDPOINT=...
OIDC_OP_JWKS_ENDPOINT=...
OIDC_RP_SIGN_ALGO=RS256

# Africa's Talking SMS Configuration (Optional)
AFRICASTALKING_USERNAME=your_username
AFRICASTALKING_API_KEY=your_api_key

## API Endpoints
This is the api url
https://customers-and-orders-api.onrender.com/


| Endpoint               | Method           | Description                                     | Authentication |
| :--------------------- | :--------------- | :---------------------------------------------- | :------------- |
| `/api/customers/`      | `GET`            | List all customers.                             | **Required**   |
| `/api/customers/`      | `POST`           | Create a new customer.                          | **Required**   |
| `/api/orders/`         | `GET`            | List all orders.                                | **Required**   |
| `/api/orders/`         | `POST`           | Create a new order (triggers SMS notification). | **Required**   |
| `/oidc/authenticate/`         | `POST`           | Exchange OIDC code for JWT token.               | None           |

---

## Running Tests

Navigate to the root directory (`Customers-and-Orders-API/`) and execute `pytest` to run the test suite and generate a coverage report.

```bash
# Ensure you are in the root directory (where manage.py is located)
pytest --cov=. --cov-report=term-missing
````

## Example Payloads

#### API Status Response (GET /):

{
"message": "Customer Orders API"
}

#### Create Customer (POST /api/customers/):

{
"name": "Patrick",
"code": "CUST1",
"phone_number": "+254791474737"
}

#### Create Order (POST /api/orders/):

{
"customer": "uuid-of-customer",
"item": "Laptop",
"amount": 1500.00
}

## Docker Deployment

Build the Docker image:

```bash
docker build -t my-django-app -f Dockerfile .
```

Run the Docker container:

#### Note: Ensure you have your .env file configured for variables

```bash
docker run -p 8000:8000 --env-file .env my-django-app
```

## CI/CD Pipeline

The Continuous Integration/Continuous Deployment process is defined in .github/workflows/ci-cd.yml and runs automatically on every push to the main branch.

The GitHub Action workflow performs the following steps:

1. Checkout code.

2. Set up Python environment.

3. Install dependencies.

4. Run tests with coverage.

5. Build Docker image.

6. Trigger Render deployment using the built image.
