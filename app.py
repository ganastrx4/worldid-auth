from flask import Flask, render_template, request, redirect, jsonify
import os

app = Flask(__name__)

# Página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para la verificación con World ID
@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    print("Datos recibidos de World ID:", data)
    
    # Aquí iría tu lógica para verificar el proof si lo deseas validar realmente
    if data and data.get("proof"):
        wallet = data.get("wallet", "0x0000000000000000000000000000000000000000")
        return jsonify({"status": "success", "redirect": f"/billetera.html?wallet={wallet}"})
    else:
        return jsonify({"status": "error", "message": "Invalid proof"})

# Página de la billetera
@app.route('/billetera.html')
def billetera():
    wallet = request.args.get('wallet', 'desconocida')
    return render_template('billetera.html', wallet=wallet)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
