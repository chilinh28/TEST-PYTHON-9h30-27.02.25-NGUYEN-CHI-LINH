# Sales Data Analysis API

## Setup Instructions

### 1. Clone the Repository
git clone https://github.com/chilinh28/TEST-PYTHON-9h30-27.02.25-NGUYEN-CHI-LINH.git

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Apply Migrations & Start Server
python manage.py migrate
python manage.py runserver

## API Endpoints

### Upload CSV File
POST /api/upload/
Upload a CSV file containing sales data.
curl -X POST -F "file=@sales_data.csv" http://127.0.0.1:8000/api/upload/

### Get Filtered Sales Data
GET /api/sales/?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&region=RegionName
curl -X GET "http://127.0.0.1:8000/api/sales/?start_date=2024-01-01&end_date=2024-02-01&region=USA"

