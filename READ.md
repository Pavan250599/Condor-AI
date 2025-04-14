## Setup Instructions

### Local Development

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/stock-prediction-api.git
   cd stock-prediction-api

2. Install dependencies

   pip install -r requirements.txt

3. Set environment variables

   # Edit .env with your API key

 4. Run application
   
   uvicorn app.main:app --reload

##Docker Deployment

1. Build image

   docker build -t stock-predictor .

2. Run container

   docker run -d --name stock-api -p 8000:8000 --env-file .env stock-predictor

API Documentation
Interactive documentation available at:

http://localhost:8000/docs (Swagger UI)

http://localhost:8000/redoc (ReDoc)


