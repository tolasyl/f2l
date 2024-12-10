from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    public_link = f"https://f2l-m0l0.onrender.com/uploads/{file.filename}"
    return jsonify({'link': public_link}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
