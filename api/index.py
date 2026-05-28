from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/start', methods=['GET'])
def start():
    return jsonify({"status": "active", "price": 2350.0})
    
