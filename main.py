import os
import tempfile
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from sambanova_client import SambanovaClient
from file_processor import (
    allowed_file, extract_zip, process_file_content, 
    check_for_direct_answer
)

# Load environment variables
load_dotenv()

# Initialize Flask app
from flask import Flask

app = Flask(__name__)  # Use double underscores around name

@app.route('/')
def home():
    return "Hello, Flask!"

if __name__ == '__main__':
    app.run(debug=True)

# Initialize SambaNova client
sambanova_client = SambanovaClient()

# Configure upload settings
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def query_sambanova(question, file_contents=None):
    """Query the SambaNova API with the question and optional file contents."""
    
    try:
        # Use the SambanovaClient to generate an answer
        return sambanova_client.generate_answer(question, file_contents)
    except Exception as e:
        return f"Error generating answer: {str(e)}"

@app.route('/api/', methods=['POST'])
def process_question():
    """Process TDS assignment questions and return answers."""
    
    # Check if question is provided
    if 'question' not in request.form:
        return jsonify({"error": "No question provided"}), 400
    
    question = request.form['question']
    file_contents = None
    direct_answer = None
    
    # Process file if uploaded
    if 'file' in request.files:
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process file based on type
            if filename.lower().endswith('.zip'):
                extracted_files = extract_zip(file_path)
                
                # Process each extracted file
                for ext_file in extracted_files:
                    # Check if the file contains a direct answer
                    direct_answer = check_for_direct_answer(ext_file, question)
                    if direct_answer:
                        return jsonify({"answer": direct_answer})
                    
                    # Process file contents for LLM
                    file_contents = process_file_content(ext_file)
                    # For now, just use the first file's contents
                    break
            else:
                # Check if the file contains a direct answer
                direct_answer = check_for_direct_answer(file_path, question)
                if direct_answer:
                    return jsonify({"answer": direct_answer})
                
                # Process file for LLM
                file_contents = process_file_content(file_path)
    
    # If we found a direct answer, return it
    if direct_answer:
        return jsonify({"answer": direct_answer})
    
    # Query SambaNova API
    answer = query_sambanova(question, file_contents)
    
    return jsonify({"answer": answer})

@app.route('/', methods=['GET'])
def index():
    """Return a simple index page."""
    return jsonify({
        "name": "TDS Solver API",
        "description": "An API for automatically answering IIT Madras' TDS graded assignments",
        "usage": "Send POST requests to /api/ with 'question' and optional 'file'"
    })

if __name__ == '_main_':
    # Run the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)