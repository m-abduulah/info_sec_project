from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_talisman import Talisman
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from kyber_py.kyber import Kyber512
import base64
import os

app = Flask(__name__)

security_policy = {
    'default-src': ['*'],
    'img-src': ['*'],
    'style-src': ['*'],
    'font-src': ['*'],
    'script-src': ['*']
}

Talisman(app, content_security_policy=security_policy)
CORS(app, origins="http://localhost:5000")

# In-memory store for demo usage
temp_store = {
    'pub': None,
    'priv': None,
    'shared_secret': None,
    'session_nonce': None,
    'original_text': None,
    'secured_data': None
}

@app.route('/init_keys', methods=['POST'])
def init_keys():
    public, private = Kyber512.keygen()
    temp_store['pub'] = public
    temp_store['priv'] = private

    shared_key, capsule = Kyber512.encaps(public)
    decrypted_key = Kyber512.decaps(private, capsule)

    assert shared_key == decrypted_key  # consistency check
    temp_store['shared_secret'] = shared_key

    return jsonify({
        'pub_key': base64.b64encode(public).decode(),
        'priv_key': base64.b64encode(private).decode()
    })

@app.route('/secure', methods=['POST'])
def secure():
    payload = request.get_json()
    raw_text = payload.get('text', '').encode()

    if temp_store['shared_secret'] is None:
        return jsonify({'error': 'Keypair not initialized'}), 400

    random_nonce = os.urandom(12)
    cipher = AESGCM(temp_store['shared_secret'])
    encrypted_data = cipher.encrypt(random_nonce, raw_text, None)

    temp_store.update({
        'session_nonce': random_nonce,
        'original_text': raw_text,
        'secured_data': encrypted_data
    })

    return jsonify({
        'cipher_text': base64.b64encode(encrypted_data).decode()
    })

@app.route('/unlock', methods=['POST'])
def unlock():
    if not all([temp_store.get(k) for k in ['shared_secret', 'session_nonce', 'secured_data']]):
        return jsonify({'error': 'Encryption phase required'}), 400

    try:
        decipher = AESGCM(temp_store['shared_secret'])
        output = decipher.decrypt(temp_store['session_nonce'], temp_store['secured_data'], None)
        return jsonify({'plain_text': output.decode()})
    except Exception as error:
        app.logger.error(f"Decryption error: {str(error)}")
        return jsonify({'error': 'Unable to decrypt'}), 400

@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False, ssl_context='adhoc')
