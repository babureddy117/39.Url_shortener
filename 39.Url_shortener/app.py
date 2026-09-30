from flask import Flask, request, jsonify, redirect
import json
import string
import random
from datetime import datetime
import os

app = Flask(__name__)

class URLShortener:
    def __init__(self, storage_file='urls.json'):
        self.storage_file = storage_file
        self.urls = {}
        self.load_urls()

    def load_urls(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                self.urls = json.load(f)
        else:
            self.save_urls()

    def save_urls(self):
        with open(self.storage_file, 'w') as f:
            json.dump(self.urls, f, indent=2)

    def generate_short_code(self, length=6):
        chars = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choice(chars) for _ in range(length))
            if code not in self.urls:
                return code

    def shorten_url(self, long_url, custom_code=None):
        if custom_code:
            if custom_code in self.urls:
                return None, "Custom code already exists"
            short_code = custom_code
        else:
            short_code = self.generate_short_code()

        self.urls[short_code] = {
            'long_url': long_url,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'clicks': 0,
            'last_accessed': None
        }
        self.save_urls()
        return short_code, None

    def get_long_url(self, short_code):
        if short_code in self.urls:
            self.urls[short_code]['clicks'] += 1
            self.urls[short_code]['last_accessed'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.save_urls()
            return self.urls[short_code]['long_url']
        return None

    def get_stats(self, short_code):
        return self.urls.get(short_code)

    def delete_url(self, short_code):
        if short_code in self.urls:
            del self.urls[short_code]
            self.save_urls()
            return True
        return False

    def list_all(self):
        return self.urls

shortener = URLShortener()

@app.route('/')
def home():
    return jsonify({
        'message': 'URL Shortener API',
        'endpoints': {
            'POST /shorten': 'Shorten a URL',
            'GET /<short_code>': 'Redirect to original URL',
            'GET /stats/<short_code>': 'Get URL statistics',
            'GET /list': 'List all URLs',
            'DELETE /delete/<short_code>': 'Delete a short URL'
        }
    })

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400
    
    long_url = data['url']
    custom_code = data.get('custom_code')
    
    if not long_url.startswith(('http://', 'https://')):
        long_url = 'http://' + long_url
    
    short_code, error = shortener.shorten_url(long_url, custom_code)
    
    if error:
        return jsonify({'error': error}), 400
    
    short_url = request.host_url + short_code
    
    return jsonify({
        'short_url': short_url,
        'short_code': short_code,
        'long_url': long_url
    }), 201

@app.route('/<short_code>')
def redirect_url(short_code):
    long_url = shortener.get_long_url(short_code)
    
    if long_url:
        return redirect(long_url)
    
    return jsonify({'error': 'Short URL not found'}), 404

@app.route('/stats/<short_code>')
def get_stats(short_code):
    stats = shortener.get_stats(short_code)
    
    if stats:
        return jsonify({
            'short_code': short_code,
            'long_url': stats['long_url'],
            'created_at': stats['created_at'],
            'clicks': stats['clicks'],
            'last_accessed': stats['last_accessed']
        })
    
    return jsonify({'error': 'Short URL not found'}), 404

@app.route('/list')
def list_urls():
    urls = shortener.list_all()
    
    result = []
    for code, data in urls.items():
        result.append({
            'short_code': code,
            'long_url': data['long_url'],
            'clicks': data['clicks'],
            'created_at': data['created_at']
        })
    
    return jsonify({
        'total': len(result),
        'urls': result
    })

@app.route('/delete/<short_code>', methods=['DELETE'])
def delete_url(short_code):
    if shortener.delete_url(short_code):
        return jsonify({'message': f'Short URL {short_code} deleted successfully'})
    
    return jsonify({'error': 'Short URL not found'}), 404

if __name__ == '__main__':
    print("=" * 50)
    print("URL Shortener Backend")
    print("=" * 50)
    print("\nAPI Endpoints:")
    print("  POST   http://127.0.0.1:5000/shorten")
    print("  GET    http://127.0.0.1:5000/<short_code>")
    print("  GET    http://127.0.0.1:5000/stats/<short_code>")
    print("  GET    http://127.0.0.1:5000/list")
    print("  DELETE http://127.0.0.1:5000/delete/<short_code>")
    print("\nStarting server...\n")
    app.run(debug=True, port=5000)
