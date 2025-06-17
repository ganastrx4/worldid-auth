import os
import requests
from flask import Flask, request, redirect, jsonify

app = Flask(__name__)

@app.route("/callback", methods=["GET"])
def handle_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"success": False, "error": "Falta el parámetro 'code'"}), 400

    CLIENT_ID = os.environ.get("WORLD_ID_APP_ID")
    CLIENT_SECRET = os.environ.get("WORLD_ID_API_KEY")
    REDIRECT_URI = "https://ganastrx4.github.io/chc-flask-app/dados.html"

    token_url = "https://id.worldcoin.org/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    token_res = requests.post(token_url, data=data)
    if token_res.status_code != 200:
        return jsonify({
            "success": False,
            "error": "No se pudo obtener token",
            "detalle": token_res.text
        }), 500

    tokens = token_res.json()
    access_token = tokens.get("access_token")

    userinfo_res = requests.get(
        "https://id.worldcoin.org/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    if userinfo_res.status_code != 200:
        return jsonify({
            "success": False,
            "error": "Error al obtener perfil",
            "detalle": userinfo_res.text
        }), 500

    userinfo = userinfo_res.json()
    wallet = userinfo.get("wallet")

    # ✅ Redirigir con wallet al frontend
    return redirect(f"https://ganastrx4.github.io/chc-flask-app/billetera.html?wallet={wallet}")

