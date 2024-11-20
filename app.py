from flask import Flask, request, render_template, redirect, url_for
import os
import pdfplumber

app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Welcome page
    return render_template('index.html')

@app.route('/convert', methods=['GET', 'POST'])
def convert():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'pdf_file' not in request.files:
            return "No file part"
        file = request.files['pdf_file']
        if file.filename == '':
            return "No selected file"
        
        # Save the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        # Extract text from the PDF
        extracted_text = extract_text_from_pdf(filepath)
        return render_template('result.html', text=extracted_text)
    
    # Display the file upload form
    return render_template('convert.html')

def extract_text_from_pdf(filepath):
    text = ""
    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

if __name__ == '__main__':
    app.run(debug=True)
