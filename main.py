import datetime 
import os
from flask import Flask, request, jsonify
import google_drive_service

app = Flask(__name__)
application = app
app.config['UPLOAD_FOLDER'] = 'uploads'
dir_actual = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def index():
    return "Hello World!"

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    now = datetime.datetime.now()
    filename = f"{now.strftime('%Y-%m-%d %H-%M-%S')}-{file.filename}"
    file.save(os.path.join(dir_actual, filename))

    try:
        response = google_drive_service.upload_file_drive(os.path.join(dir_actual, filename), filename)
        os.remove(os.path.join(dir_actual, filename))
        return jsonify({'status': response['id']})
    except Exception as e:
        print(f"Error uploading image to Google Drive: {e}")
        return jsonify({'error': 'Error uploading image to Google Drive'}), 500

if __name__ == '__main__':
    app.run(host="localhost", port=8005, debug=True)