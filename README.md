# E‑Commerce Backend

This repository contains a fully‑featured e‑commerce backend built with
**Django**. It is designed to illustrate best practices for developing
scalable, secure and maintainable web applications. The codebase
demonstrates a wide range of technologies—including asynchronous task
processing, caching, containerization and payment integration—to
simulate a real‑world production environment.

## Features

The project implements the following functionality:

1. **User Management** – Registration, JWT‑based authentication and profile
   management. Each user has an associated profile storing phone and
   address details. Signals automatically create profiles and send
   welcome emails via Celery.

2. **Product Catalog** – CRUD APIs for categories, products and
   product variations. Categories support hierarchical nesting. Products
   include additional attributes such as SKU and brand. Variations
   capture differences like color or size and maintain their own
   price and stock levels.

3. **Filtering, Sorting and Pagination** – Powerful search endpoints
   supporting category filters, price ranges, text search, ordering
   options and paginated responses for large datasets. Products may be
   annotated on the fly with discounted prices and inventory value.

4. **Shopping Cart** – Each authenticated user can maintain an active
   cart. Items may be added, updated and removed. Carts record a
   snapshot of prices at the time of addition so that subsequent
   price changes do not affect the cart total.

5. **Orders and Shipments** – When a cart is checked out it is
   converted into an order. Order items record the purchased product,
   variation, quantity and price. A shipment record is created for
   each order and can be updated by administrators with tracking
   details. Signals dispatch order confirmation emails and initialize
   shipments.

6. **Payments with MPesa** – Payments may be associated with orders or
   created independently. The MPesa integration demonstrates how to
   initiate an STK push via Safaricom's Daraja API. Celery tasks
   perform the network calls asynchronously and update payment status
   based on responses. Additional payment methods can be added
   easily.

7. **Advanced ORM Techniques** – Custom querysets demonstrate complex
   annotations such as discounted prices and stock value calculations
   using `F` expressions and `Coalesce`. Nested relations are
   efficiently fetched using `select_related`.

8. **Middleware and Context Managers** – A custom middleware measures
   request processing times and exposes metrics via response headers.
   Context managers centralize database atomic operations and
   temporary environment overrides.

9. **Celery & Background Tasks** – Asynchronous tasks handle long
   running operations like sending emails, updating stock quantities and
   executing periodic maintenance jobs. Celery Beat schedules
   cron‑like tasks such as automatically disabling out of stock
   products. Order and payment processing also run in the background.

10. **Redis Caching** – High performance caching layer (via
    `django‑redis`) speeds up database queries and maintains session
    data.

11. **Message Brokering** – Ready to work with either RabbitMQ or
    Redis as a Celery broker, configurable via environment variables.

12. **MPesa Payment Integration** – Demonstrates how to integrate with
    the Safaricom MPesa Daraja API for initiating STK push payments.

13. **Containerization** – Dockerfile and docker‑compose definitions
    orchestrate the application, PostgreSQL, Redis and RabbitMQ into
    disposable services suitable for local development and deployment.

14. **Kubernetes (Basics)** – Example manifests illustrate how to run
    the web server and Celery workers in a Kubernetes cluster using
    deployments, services and config maps.

15. **CI/CD Pipeline** – A GitHub Actions workflow installs
    dependencies, runs migrations and executes the test suite on each
    push to the main branch.

## Project Structure

```
ecommerce_backend/
├── ecommerce/                  # Django project configuration
│   ├── settings.py             # Environment‑driven configuration
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI entry point
│   ├── asgi.py                 # ASGI entry point
│   ├── celery.py               # Celery application definition
│   └── __init__.py
├── core/                      # Shared utilities
│   ├── middleware.py          # Request timing middleware
│   ├── context_managers.py    # Database and environment context managers
│   ├── tasks.py               # Periodic maintenance tasks
│   └── __init__.py
├── users/                     # User registration and authentication
│   ├── models.py              # UserProfile model
│   ├── serializers.py         # Registration & profile serializers
│   ├── views.py               # API views for users
│   ├── tasks.py               # Async tasks (e.g. welcome emails)
│   ├── signals.py             # Signal handlers for profiles
│   ├── permissions.py         # Custom permission classes
│   ├── apps.py                # App configuration
│   └── urls.py               # User endpoints
├── catalog/                   # Product and category management
│   ├── models.py              # Category, Product & ProductVariation models
│   ├── serializers.py         # Serializers including computed fields
│   ├── views.py               # ViewSets with filtering & annotations
│   ├── filters.py             # Advanced filtering definitions
│   ├── tasks.py               # Async stock update tasks
│   ├── apps.py                # App configuration
│   └── urls.py               # Catalog endpoints
├── orders/                    # Cart, order and shipment management
│   ├── models.py              # Cart, Order, OrderItem & Shipment models
│   ├── serializers.py         # Serializers for carts and orders
│   ├── views.py               # API views for carts, items, orders & shipments
│   ├── tasks.py               # Order‑related asynchronous tasks
│   ├── signals.py             # Signal handlers for orders
│   ├── apps.py                # App configuration
│   └── urls.py               # Order endpoints
├── payments/                  # Payment processing
│   ├── models.py              # Payment record model with order linkage
│   ├── mpesa.py               # Low‑level MPesa API integration
│   ├── tasks.py               # Celery tasks for STK push
│   ├── serializers.py         # Payment creation and read serializers
│   ├── views.py               # API views to initiate and list payments
│   ├── apps.py                # App configuration
│   └── urls.py               # Payment endpoints
├── Dockerfile                # Build instructions for the web service
├── docker-compose.yml        # Compose services: web, db, redis, rabbitmq, celery
├── k8s/                      # Example Kubernetes manifests
│   └── deployment.yaml
├── .github/workflows/ci.yml  # Continuous integration pipeline
├── .env.example              # Sample environment configuration
├── manage.py                 # Django management entry point
└── requirements.txt          # Python dependencies
```

## Getting Started

### Prerequisites

Ensure you have **Python 3.11**, **Docker** and **docker‑compose** installed on
your machine for the simplest development setup. Alternatively you can
run the project directly using `venv` and a locally installed
PostgreSQL and Redis instance.

### Local Development (without Docker)

1. **Clone the repository** and navigate into it:

   ```bash
   git clone <your-repo-url>
   cd ecommerce_backend
   ```

2. **Create a virtual environment** and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use venv\Scripts\activate
   ```

3. **Install dependencies**:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure your environment**. Copy `.env.example` to `.env` and
   update the values to match your local PostgreSQL, Redis and RabbitMQ
   configuration. If you do not have these services installed, set
   `DB_ENGINE=django.db.backends.sqlite3` and leave other DB variables
   empty to fall back to SQLite.

5. **Run database migrations** and create a superuser:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Start the Celery worker and beat scheduler** (each in a separate
   terminal session):

   ```bash
   celery -A ecommerce worker --loglevel=info
   celery -A ecommerce beat --loglevel=info --scheduler django_celery_beat.schedulers:DatabaseScheduler
   ```

7. **Run the development server**:

   ```bash
   python manage.py runserver
   ```

8. **Access the API documentation** at `http://localhost:8000/api/docs/`.

### Running with Docker

The `docker-compose.yml` file defines services for PostgreSQL, Redis,
RabbitMQ, the Django application and the Celery workers. To build and
start the entire stack run:

```bash
docker-compose up --build
```

The web server will be available at `http://localhost:8000/`. Celery
workers will automatically process background jobs and periodic tasks.

### Deploying on Kubernetes (Basic Example)

The `k8s/deployment.yaml` provides a minimal set of manifests to run
the web server and Celery workers in a Kubernetes cluster. Before
applying these manifests you must build your Docker image and push it
to a container registry, then update `image:` fields accordingly. You
also need to provision PostgreSQL, Redis and RabbitMQ (or use managed
services) and create corresponding Kubernetes `Service` and
`StatefulSet` objects. Apply the configuration with:

```bash
kubectl apply -f k8s/deployment.yaml
```

Further customization, such as horizontal pod autoscaling, ingress
configuration, secret management and persistent storage, are beyond the
scope of this example but are natural next steps for production.

## MPesa Integration

The `payments/mpesa.py` module demonstrates how to integrate with the
Safaricom MPesa Daraja API by obtaining an OAuth token and initiating
an STK push. For security reasons you **must** supply your own
credentials via environment variables. The asynchronous task
`process_mpesa_payment` handles the network call to the API and
persists the resulting `CheckoutRequestID` in the database. You can
add webhook endpoints to receive payment confirmations and update
payment statuses accordingly.

## API Overview

The following table summarizes the key API endpoints exposed by the
application. All routes are prefixed with `/api/` and require JWT
authentication unless otherwise stated.

| Resource           | Method | Endpoint                                 | Description |
|--------------------|--------|------------------------------------------|-------------|
| Users              | POST   | `/api/users/register/`                  | Register a new user |
|                    | POST   | `/api/users/token/`                     | Obtain JWT token |
|                    | GET/PUT/DELETE | `/api/users/me/`             | Retrieve/update/delete current user profile |
| Categories         | GET    | `/api/catalog/categories/`               | List categories |
|                    | POST   | `/api/catalog/categories/`               | Create category (admin only) |
| Products           | GET    | `/api/catalog/products/`                 | List products with filtering & sorting |
|                    | POST   | `/api/catalog/products/`                 | Create product (admin only) |
| Variations         | GET    | `/api/catalog/variations/`               | List product variations |
|                    | POST   | `/api/catalog/variations/`               | Create variation (admin only) |
| Cart               | GET    | `/api/orders/carts/`                     | List user carts |
| Cart Items         | POST   | `/api/orders/cart-items/`                | Add item to current cart |
|                    | PATCH  | `/api/orders/cart-items/<id>/`           | Update cart item quantity |
|                    | DELETE | `/api/orders/cart-items/<id>/`           | Remove item from cart |
| Orders             | POST   | `/api/orders/orders/`                    | Checkout cart and create order |
|                    | GET    | `/api/orders/orders/`                    | List user orders |
|                    | GET    | `/api/orders/orders/<id>/`               | Retrieve order details |
| Shipments          | GET    | `/api/orders/shipments/`                 | List shipment statuses |
| Payments           | POST   | `/api/payments/initiate/`               | Initiate a payment (MPesa STK push) |
|                    | GET    | `/api/payments/records/`                | List payment records |
|                    | GET    | `/api/payments/records/<id>/`           | Retrieve payment details |

## Contributing

Pull requests, issues and feature suggestions are welcome. You can also
fork and extend the project—for example, adding a product search,
reviews, wishlists or integration with additional payment gateways.

## License

This project is developed for educational purposes as part of the ALX
Backend Engineering program. It is provided for learning and personal
use without warranty.