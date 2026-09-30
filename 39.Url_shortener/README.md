# URL Shortener Backend

A simple URL shortener REST API built with Flask.

## Installation

```bash
pip install flask
```

## Running the Server

```bash
cd c:\Users\babur\Desktop\python\projects\url_shortener
python app.py
```

Server will start at: http://127.0.0.1:5000

## API Endpoints

### 1. Shorten a URL
**POST** `/shorten`

Request body:
```json
{
  "url": "https://www.example.com/very/long/url"
}
```

With custom code:
```json
{
  "url": "https://www.example.com",
  "custom_code": "mylink"
}
```

Response:
```json
{
  "short_url": "http://127.0.0.1:5000/abc123",
  "short_code": "abc123",
  "long_url": "https://www.example.com/very/long/url"
}
```

### 2. Redirect to Original URL
**GET** `/<short_code>`

Example: http://127.0.0.1:5000/abc123

Redirects to the original URL.

### 3. Get URL Statistics
**GET** `/stats/<short_code>`

Response:
```json
{
  "short_code": "abc123",
  "long_url": "https://www.example.com",
  "created_at": "2024-01-15 10:30:00",
  "clicks": 42,
  "last_accessed": "2024-01-15 15:45:30"
}
```

### 4. List All URLs
**GET** `/list`

Response:
```json
{
  "total": 3,
  "urls": [
    {
      "short_code": "abc123",
      "long_url": "https://www.example.com",
      "clicks": 42,
      "created_at": "2024-01-15 10:30:00"
    }
  ]
}
```

### 5. Delete a Short URL
**DELETE** `/delete/<short_code>`

Response:
```json
{
  "message": "Short URL abc123 deleted successfully"
}
```

## Testing with cURL

### Shorten a URL:
```bash
curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d "{\"url\":\"https://www.google.com\"}"
```

### With custom code:
```bash
curl -X POST http://127.0.0.1:5000/shorten -H "Content-Type: application/json" -d "{\"url\":\"https://www.github.com\",\"custom_code\":\"gh\"}"
```

### Get stats:
```bash
curl http://127.0.0.1:5000/stats/abc123
```

### List all URLs:
```bash
curl http://127.0.0.1:5000/list
```

### Delete URL:
```bash
curl -X DELETE http://127.0.0.1:5000/delete/abc123
```

## Testing with Python

```python
import requests

# Shorten URL
response = requests.post('http://127.0.0.1:5000/shorten', 
                        json={'url': 'https://www.example.com'})
print(response.json())

# Get stats
response = requests.get('http://127.0.0.1:5000/stats/abc123')
print(response.json())

# List all
response = requests.get('http://127.0.0.1:5000/list')
print(response.json())
```

## Features

- ✅ Generate random short codes (6 characters)
- ✅ Custom short codes
- ✅ Click tracking
- ✅ URL statistics (creation date, clicks, last accessed)
- ✅ List all shortened URLs
- ✅ Delete URLs
- ✅ Persistent storage (JSON file)
- ✅ RESTful API design
