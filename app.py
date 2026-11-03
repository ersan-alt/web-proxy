from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="tr">
    <head>
        <meta charset="UTF-8">
        <title>MEB Erişim Geçidi</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 50px; background-color: #f4f4f9; color: #333; }
            .container { background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); max-width: 500px; }
            input[type="text"] { width: 100%; padding: 10px; margin-top: 10px; margin-bottom: 15px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
            button { background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
            button:hover { background-color: #0056b3; }
            #status-box { margin-top: 20px; padding: 15px; border-radius: 4px; background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>MEB Erişim Geçidi</h2>
            
            <div id="status-box">
                ⏳ Sunucu uyandırılıyor... Lütfen <span id="countdown">60</span> saniye bekleyin.
            </div>

            <form id="proxy-form" action="/proxy" method="get" style="margin-top: 20px;">
                <label for="url">Gitmek İstediğiniz Adres:</label>
                <input type="text" id="url" name="url" placeholder="https://www.ornek.com" required>
                <button type="submit" id="submit-btn" disabled style="opacity: 0.6; cursor: not-allowed;">Git</button>
            </form>
        </div>

        <script>
            let timeLeft = 60;
            const countdownEl = document.getElementById('countdown');
            const statusBox = document.getElementById('status-box');
            const submitBtn = document.getElementById('submit-btn');

            const timer = setInterval(() => {
                timeLeft--;
                countdownEl.textContent = timeLeft;

                ...

                if (timeLeft <= 0) {
                    clearInterval(timer);
                    statusBox.style.backgroundColor = "#d4edda";
                    statusBox.style.color = "#155724";
                    statusBox.style.borderColor = "#c3e6cb";
                    statusBox.innerHTML = "✅ Sunucu aktif! Artık dilediğiniz siteye girebilirsiniz.";
                    submitBtn.disabled = false;
                    submitBtn.style.opacity = "1";
                    submitBtn.style.cursor = "pointer";
                }
            }, 1000);
        </script>
    </body>
    </html>
    '''

@app.route('/proxy')
def proxy():
    url = request.args.get('url')
    if not url:
        return "Lütfen bir URL belirtin.", 400
    
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': url
    }
    
    try:
        # İçeriği hiç kurcalamadan, doğrudan en hızlı şekilde iletiyoruz
        resp = requests.get(url, headers=headers, timeout=10)
        
        # Sıkıştırma veya transfer çakışmalarını önlemek için başlıkları filtreliyoruz
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers_list = [(name, value) for name, value in resp.headers.items() if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, headers_list)
            
    except Exception as e:
        return f"Bağlantı hatası oluştu: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)