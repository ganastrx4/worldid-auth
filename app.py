from flask import Flask, redirect, request, render_template
import requests
import os

app = Flask(__name__)

CLIENT_ID = "app_7686f9027d3e3c0b53d987a3caf1e111"
CLIENT_SECRET = os.getenv("WORLD_ID_SECRET")
REDIRECT_URI = "https://worldid-auth.onrender.com/callback"

@app.route("/")
def index():
    # Enlace de inicio con World ID (nuevo flujo)
    auth_url = f"https://id.worldcoin.org/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=openid"
    return f'<a href="{auth_url}">✅ Sign in with World ID</a>'

@app.route("/callback")
def callback():
    code = request.args.get("code")

    if not code:
        return "❌ No se recibió ningún código."

    # Intercambiar el código por un token
    token_url = "https://id.worldcoin.org/token"
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(token_url, data=data)
    token_info = response.json()

    if "error" in token_info:
        return f"❌ Error: {token_info['error_description']}"

    id_token = token_info.get("id_token")
    return redirect(f"/billetera.html?token={id_token}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
