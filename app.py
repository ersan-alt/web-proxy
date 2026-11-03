import os
from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h2>MEB Erişim Geçidi</h2>
    <form action="/proxy" method="get">
        <input type="text" name="url" placeholder="https://example.com" style="width:300px; pading:8px;">
        <button type="submit">Git</button>
    </form>
    '''

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "Lütfen bir URL girin.", 400
    if not target_url.startswith('http'):
        target_url = 'https://' + target_url
    
    try:
        resp = requests.get(target_url)
        return Response(resp.content, content_type=resp.headers.get('Content-Type', 'text/html'))
    except Exception as e:
        return f"Hata oluştu: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)