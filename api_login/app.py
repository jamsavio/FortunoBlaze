from flask import Flask, request, jsonify
from datetime import datetime
import jwt
import mysql.connector

app = Flask(__name__)

@app.route('/login', methods=['GET'])
def login():
    # Configurações do MySQL
    config = {
        'user': 'jam',
        'password': '',
        'host': 'localhost',
        'database': 'assinaturas'
    }
    
    email = request.args.get('email')
    db = mysql.connector.connect(**config)
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()

    if user and user['assinatura_expiracao'] > datetime.now():
        token = jwt.encode({'email': user['email'], 'exp': user['assinatura_expiracao']}, '7e372c35c140e6d80b6f85dce25b56e64b8a858b0151e151d464c107865a7438e0b7a268b065d2beff57f8c8ebd7f24528f3e3c3c38337f74e6d01d6a1a1827c', algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Not found'}), 401

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000, debug=True)