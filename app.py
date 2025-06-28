from dotenv import load_dotenv
load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, send_file, session
import os
from utils.resume_parser import parse_resume
from utils.olama_api import generate_career_roadmap
from utils.feedback_gen import generate_feedback
from utils.pdf_generator import create_pdf

app = Flask(__name__)
app.secret_key = 'skillivy_secret'  # session use karne ke liye zaroori hai

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['GENERATED_FOLDER'] = 'static/generated'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return "❌ No file uploaded.", 400
    
    file = request.files['resume']

    if file.filename == '':
        return "❌ No file selected.", 400
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Extract text
        parsed_data = parse_resume(filepath)

        # Get feedback & roadmap
        feedback = generate_feedback(parsed_data)
        roadmap = generate_career_roadmap(parsed_data)

        # Save in session for reuse
        session['roadmap'] = roadmap
        session['feedback'] = feedback

        # ✅ Generate feedback PDF
        os.makedirs(app.config['GENERATED_FOLDER'], exist_ok=True)
        pdf_path = create_pdf(parsed_data, feedback, roadmap)

        return render_template('result.html', feedback=feedback, roadmap=roadmap, pdf_path=pdf_path)

    return "❌ Invalid file type.", 400

@app.route('/result')
def result_page():
    return render_template('result.html')

@app.route('/roadmap')
def roadmap_page():
    roadmap = session.get('roadmap', '❌ No roadmap found.')
    return render_template('roadmap.html', roadmap=roadmap)

@app.route('/payment')
def payment_page():
    return render_template('payment.html')

@app.route('/download/<filename>')
def download_file(filename):
    path = os.path.join('static', 'generated', filename)
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
