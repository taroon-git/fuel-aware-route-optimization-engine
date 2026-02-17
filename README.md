
# Fuel-Aware Route Optimization Engine

## Project Overview

This project is a Django-based web application designed to optimize vehicle routes based on fuel prices and availability. It leverages real-time and historical fuel price data to help users plan cost-effective routes, minimizing fuel expenses and maximizing efficiency. The application is suitable for logistics companies, fleet managers, and individual users seeking smarter route planning.

## Features

- Route optimization based on fuel prices
- Integration with fuel price datasets
- REST API for route queries
- User-friendly web interface
- Modular and extensible architecture

## Project Structure

- `fuel_route_project/`: Django project settings and configuration
- `fuel-aware-route-optimization-engine/route_api/`: Main app with models, views, serializers, services, and utilities
- `static/` and `templates/`: Frontend assets and HTML templates
- `db.sqlite3`: Default SQLite database
- `fuel-prices-for-be-assessment.csv`: Fuel price dataset

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/taroon-git/fuel-aware-route-optimization-engine.git
cd fuel-aware-route-optimization-engine
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root for any sensitive settings (e.g., API keys, database credentials).

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

### 7. Access the Application

Open your browser and go to `http://127.0.0.1:8000/` to use the web interface.

## API Usage

The project exposes REST endpoints for route optimization. See `route_api/urls.py` for available endpoints.

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes
4. Push to your branch and create a pull request

## License

This project is licensed under the MIT License.
