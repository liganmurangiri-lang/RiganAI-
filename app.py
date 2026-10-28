python
from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <html>
    <head>
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
    body{background:#0f172a;color:white;font-family:sans-serif;text-align:center;padding:30px}
    h1{color:#2dd4bf}
    .box{background:#1e293b;padding:20px;border-radius:15px;margin-top:20px}
    </style>
    </head>
    <body>
    <h1>RIGAN MARINA V3</h1>
    <div class="box">
    <p>Poa sana Regan murangiri!</p>
    <p>Rigan AI iko ONLINE!</p>
    </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
