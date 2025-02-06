# Number Classification API

## Overview
This API that takes a number and returns interesting mathematical properties about it, along with a fun fact. It's an exercise from Stage 1 of the HNG Internship for back-end developers.

## Project Requirements
- Programming Language/Framework: Use any of the following: See Sharp (C#), PHP, Python, Go, Java, JavaScript/TypeScript.
- Deployment: The API must be deployed to a publicly accessible endpoint.
- CORS Handling: Ensure the API handles Cross-Origin Resource Sharing (CORS) appropriately.
- Response Format: All responses must be in JSON format.
- Endpoint: `GET** <your-domain.com>/api/classify-number?number=371`
- The required JSON Response Format (200 OK).
```JSON
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,  // sum of its digits
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371" //gotten from the numbers API
}
```
- The required JSON Response Format (400 Bad Request). See it below.
```JSON
{
    "number": "alphabet",
    "error": true
}
```
- The API must accept GET requests and return the required JSON response.
- It provides appropriate HTTP status code.

## Technologies Used
- Programming Language: Python
- Framework: FastAPI
- CORS Handling: using FastAPI CORS Middleware `fastapi.middleware.cors`
- Caching: using FastAPI Caching for improved performance
- Deployment: Railway

## API Documentation

### API Endpoint
`GET <your-domain.com>/api/classify-number?number=371`

### Public API Endpoint
`https://basic-numbers-api.up.railway.app/api/classify-number?number=371`

### Sample Usage
Here's the proper request format:
`curl -X GET https://basic-numbers-api.up.railway.app/api/classify-number?number=371`

- Response Format (200 OK):
```JSON
{
    "number": 371,
    "is_prime": false,
    "is_perfect": false,
    "properties": ["armstrong", "odd"],
    "digit_sum": 11,  // sum of its digits
    "fun_fact": "371 is an Armstrong number because 3^3 + 7^3 + 1^3 = 371" //gotten from the numbers API
}
```

Here's an improper request:
`curl -X GET https://basic-numbers-api.up.railway.app/api/classify-number?number=alphabet`

- Response Format (400 Bad Request):
```JSON
{
    "number": "alphabet",
    "error": true
}
```

## Deployment
Again, this API is publicly accessible at:
`https://basic-numbers-api.up.railway.app/api/classify-number?number=371`

## How To Run this API Locally
Ensure you have:
- Python 3 installed.
- `pip` package manager.

```Bash
# Clone the repository
git clone https://github.com/dahunsi-dami/basic-numbers-api.git
cd basic-numbers-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API locally
uvicorn main:app --reload

# Test the API
`curl -X GET https://basic-numbers-api.up.railway.app/api/classify-number?number=371`
```

## Deploying This API on Railway
```Bash
# Push code to GitHub
git add .
git commit -m "Initial commit"
git push origin main

# Deploy on Railway
# 1. Go to Railway (https://railway.app/)
# 2. Create a new project
# 3. Link your GitHub repository
# 4. Deploy 🚀
# 6. Go to Settings and Generate Domain under Network to get your publicly accessible API URL.
```
