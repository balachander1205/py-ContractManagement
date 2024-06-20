from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flasgger import Swagger
import os
from utils import read_pdf_file, supplier_agreement_llm_call
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
CORS(app)

# Set the folder to save uploaded files
UPLOAD_FOLDER = 'static/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# swagger config
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name' : 'customer review sentiment analysis Application'
    }
)
app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix = SWAGGER_URL)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['POST', 'GET'])
@cross_origin()
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print("PATH=",path)
        file.save(path)
        extracted_text = read_pdf_file(path)
        # openai to process the extracted data
        # openai_data = supplier_agreement_llm_call(extracted_text)
        # return jsonify({"message": "File uploaded successfully", "filename": filename, "data":extracted_text, "openai_data":"openai_data"}), 200
        return jsonify({"message": "File uploaded successfully", "filename": filename, "data":extracted_text}), 200
    else:
        return jsonify({"error": "Invalid file format. Only PDFs are allowed."}), 400

@app.route('/uploads/<filename>')
@cross_origin()
def uploaded_file(filename):
    """
    Retrieve an uploaded file
    ---
    parameters:
      - in: path
        name: filename
        type: string
        required: true
        description: Name of the file to retrieve
    responses:
      200:
        description: File retrieved successfully
      404:
        description: File not found
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
