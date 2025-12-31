# Fittrack - Gym Management System

A comprehensive gym management system built with Flask (backend) and modern web technologies.

## Project Structure

```
fittrack/
├── backend/              # Flask backend application
│   ├── app/
│   │   ├── api/         # REST API endpoints
│   │   ├── services/    # Business logic
│   │   ├── repositories/# Data access layer
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic validation schemas
│   │   ├── exceptions/  # Custom exceptions
│   │   ├── utils/       # Utility functions
│   │   └── db/          # Database configuration
│   ├── tests/           # Unit tests
│   └── scripts/         # Utility scripts
└── frontend/            # Frontend application (to be implemented)
```

## Prerequisites

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)

## Quick Start

### 1. Setup (First Time Only)

```bash
# Make scripts executable
chmod +x setup.sh init_db.sh run.sh

# Run setup
./setup.sh
```

### 2. Configure Database

Edit `backend/config.ini` with your MySQL credentials:

```ini
[mysql]
host = localhost
user = your_mysql_user
password = your_mysql_password
```

### 3. Initialize Database

```bash
./init_db.sh
```

### 4. Run the Application

```bash
./run.sh
```

The server will start at `http://127.0.0.1:5000`

## API Endpoints

### Users
- `GET /` - List all users
- `POST /` - Create new user
- `GET /<id>` - Get user by ID
- `PUT /<id>` - Update user
- `DELETE /<id>` - Delete user

### Plans
- `GET /plans/` - List all plans
- `POST /plans/` - Create new plan
- `GET /plans/<id>` - Get plan by ID
- `PUT /plans/<id>` - Update plan
- `DELETE /plans/<id>` - Delete plan

### Subscriptions
- `GET /subscriptions/` - List all subscriptions
- `POST /subscriptions/` - Create new subscription
- `GET /subscriptions/<id>` - Get subscription by ID
- `GET /subscriptions/member/<member_id>` - Get member's subscriptions
- `PUT /subscriptions/<id>/freeze` - Freeze subscription
- `PUT /subscriptions/<id>/unfreeze` - Unfreeze subscription
- `PUT /subscriptions/<id>/renew` - Renew subscription

### Classes
- `GET /classes/` - List all classes
- `POST /classes/` - Create new class
- `GET /classes/<id>` - Get class by ID
- `PUT /classes/<id>` - Update class
- `DELETE /classes/<id>` - Delete class

### Enrollments
- `GET /enrollments/` - List all enrollments
- `POST /enrollments/` - Create new enrollment
- `GET /enrollments/class/<class_id>` - Get enrollments by class
- `GET /enrollments/member/<member_id>` - Get enrollments by member
- `DELETE /enrollments/<id>` - Cancel enrollment

### Check-ins
- `GET /checkins/` - List all check-ins
- `POST /checkins/` - Create new check-in
- `GET /checkins/member/<member_id>` - Get member's check-in history

### Payments
- `GET /payments/` - List all payments
- `POST /payments/` - Create new payment
- `GET /payments/<id>` - Get payment by ID
- `GET /payments/member/<member_id>` - Get member's payments
- `DELETE /payments/<id>` - Cancel payment

### Workout Plans
- `GET /workout-plans/` - List all workout plans
- `POST /workout-plans/` - Create new workout plan
- `GET /workout-plans/<id>` - Get workout plan by ID
- `GET /workout-plans/member/<member_id>` - Get member's workout plans
- `PUT /workout-plans/<id>` - Update workout plan
- `DELETE /workout-plans/<id>` - Delete workout plan
- `GET /workout-plans/<id>/exercises` - Get exercises for a plan

### Workout Items
- `GET /workout-items/` - List all workout items
- `POST /workout-items/` - Create new workout item
- `GET /workout-items/<id>` - Get workout item by ID
- `GET /workout-items/plan/<plan_id>` - Get items by plan
- `PUT /workout-items/<id>` - Update workout item
- `DELETE /workout-items/<id>` - Delete workout item

## Manual Installation

If you prefer to set up manually:

```bash
# 1. Create virtual environment
cd backend
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure database (edit backend/config.ini)

# 5. Initialize database
cd ..
PYTHONPATH=. python -m backend.scripts.init_db

# 6. Run application
PYTHONPATH=. python -m backend.app
```

## Development

### Running Tests
```bash
source backend/venv/bin/activate
pytest backend/tests/
```

### Code Structure
- **API Layer** (`backend/app/api/`): HTTP endpoints and request/response handling
- **Service Layer** (`backend/app/services/`): Business logic
- **Repository Layer** (`backend/app/repositories/`): Database operations (to be implemented)
- **Models** (`backend/app/models/`): SQLAlchemy table definitions
- **Schemas** (`backend/app/schemas/`): Pydantic validation models

## Troubleshooting

### "No module named 'backend'"
Make sure you're running from the project root directory and using `PYTHONPATH=.`

### Database connection errors
- Verify MySQL is running
- Check credentials in `backend/config.ini`
- Ensure the fittrack database exists (run `./init_db.sh`)

### Port 5000 already in use
- Stop other applications using port 5000 (like AirPlay on macOS)
- Or modify the port in `backend/app/__main__.py`

## License

[Your License Here]

## Contributors

[Your Name]