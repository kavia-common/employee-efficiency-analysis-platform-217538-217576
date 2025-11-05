# employee-efficiency-analysis-platform-217538-217576

## Environment configuration

Backend (FastAPI) expects:
- DATABASE_URL: SQLAlchemy URL. Defaults to postgresql+psycopg2://postgres:postgres@localhost:5001/employee_efficiency
- DATA_DIR: path to store uploaded CSV files (optional; defaults to employee_efficiency_backend/data)
- CORS_ALLOW_ORIGINS: comma-separated origins allowed by CORS (optional; defaults to http://localhost:3000,http://127.0.0.1:3000)

Frontend (React) should call backend at:
- default http://localhost:3001 (configurable via environment variable in frontend using REACT_APP_API_BASE_URL or VITE_API_BASE_URL)

Database (PostgreSQL):
- Should be exposed on port 5001.
- Ensure the database "employee_efficiency" exists and credentials match DATABASE_URL.

### Useful endpoints
- GET / -> service health
- GET /health/db -> database connectivity health
- GET /report/pdf?dataset_id=ID -> generate report metadata
- GET /report/pdf/download?dataset_id=ID -> download report PDF

### Generate OpenAPI
From the backend root:
```
python -m src.api.generate_openapi
```
This will update interfaces/openapi.json.

### Quick start
1) Ensure Postgres is running on port 5001 and database is created.
2) Create employee_efficiency_backend/.env based on .env.example.
3) Install backend requirements and start FastAPI (e.g., uvicorn src.api.main:app --port 3001).
4) Start the frontend; it will use http://localhost:3001 by default.
