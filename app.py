from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv
import json
from groq import Groq

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def get_groq_client():
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key or api_key == 'your-groq-api-key-here':
        raise ValueError("GROQ_API_KEY not set. Please create a .env file with your Groq API key.")
    return Groq(api_key=api_key)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy=True)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    topic = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'success': True, 'message': 'Login successful'})
        
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'success': False, 'message': 'Username already exists'}), 400
        
        hashed_password = generate_password_hash(data['password'])
        new_user = User(username=data['username'], email=data['email'], password=hashed_password)
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/quiz')
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('quiz.html')

@app.route('/api/test-groq')
def test_groq():
    """Test endpoint to verify Groq API is configured correctly"""
    try:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            return jsonify({
                'success': False,
                'message': 'GROQ_API_KEY not found in environment variables',
                'help': 'Create a .env file with GROQ_API_KEY=your-actual-key'
            }), 500
        
        if api_key == 'your-groq-api-key-here':
            return jsonify({
                'success': False,
                'message': 'GROQ_API_KEY is still set to placeholder value',
                'help': 'Replace the placeholder in .env with your actual Groq API key'
            }), 500
        
        groq_client = Groq(api_key=api_key)
        
        # Test with a simple request
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,   # give it room for ~15–20 questions
            temperature=0.7    # optional: add some variation
        )


        
        return jsonify({
            'success': True,
            'message': 'Groq API is configured correctly!',
            'test_response': response.choices[0].message.content
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Groq API test failed: {str(e)}',
            'error_type': type(e).__name__
        }), 500

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    topic = data.get('topic', 'General Knowledge')
    num_questions = data.get('num_questions', 15)
    
    # Limit to reasonable number
    num_questions = min(max(num_questions, 5), 50)
    
    try:
        # Check API key
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key or api_key == 'your-groq-api-key-here':
            print("[ERROR] GROQ_API_KEY not configured properly")
            return jsonify({
                'success': False, 
                'message': 'API key not configured. Please check your .env file and ensure GROQ_API_KEY is set to your actual key.'
            }), 500
        
        print(f"[INFO] Generating quiz: topic={topic}, questions={num_questions}")
        groq_client = Groq(api_key=api_key)
        
        prompt = f"""Generate {num_questions} multiple choice quiz questions about {topic}.
        
        Return ONLY a valid JSON array with this exact structure:
        [
          {{
            "question": "Question text here?",
            "options": ["Option A text", "Option B text", "Option C text", "Option D text"],
            "correct_answer": 0,
            "explanation": "Brief explanation of the correct answer"
          }}
        ]
        
        Rules:
        - Each question must have exactly 4 options
        - correct_answer is the index (0-3) of the correct option
        - Make questions educational and accurate
        - Vary difficulty levels
        - Return ONLY the JSON array, no other text"""
        
        print("[INFO] Sending request to Groq API...")
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.7
        )


        
        print("[INFO] Received response from Groq API")
        response_content = response.choices[0].message.content
        print(f"[DEBUG] Response content (first 200 chars): {response_content[:200]}")
        
        try:
            quiz_data = json.loads(response_content)
        except json.JSONDecodeError as je:
            print(f"[ERROR] JSON parsing failed: {je}")
            print(f"[DEBUG] Full response: {response_content}")
            return jsonify({
                'success': False,
                'message': 'Failed to parse quiz data. The AI response was not in valid JSON format. Please try again.'
            }), 500
        
        if not isinstance(quiz_data, list) or len(quiz_data) == 0:
            print(f"[ERROR] Invalid quiz data structure: {type(quiz_data)}")
            return jsonify({
                'success': False,
                'message': 'Invalid quiz data received. Please try again.'
            }), 500
        
        print(f"[SUCCESS] Generated {len(quiz_data)} questions successfully")
        
        return jsonify({
            'success': True,
            'quiz': quiz_data,
            'topic': topic
        })
    
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"[ERROR] {error_type}: {error_msg}")
        
        if 'api_key' in error_msg.lower():
            user_message = 'API key error. Please verify your GROQ_API_KEY in the .env file.'
        elif 'rate' in error_msg.lower() or 'limit' in error_msg.lower():
            user_message = 'Rate limit exceeded. Please wait a moment and try again.'
        elif 'network' in error_msg.lower() or 'connection' in error_msg.lower():
            user_message = 'Network error. Please check your internet connection and try again.'
        else:
            user_message = f'Failed to generate quiz: {error_msg}'
        
        return jsonify({
            'success': False, 
            'message': user_message,
            'error_type': error_type
        }), 500

@app.route('/api/save-score', methods=['POST'])
def save_score():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    attempt = QuizAttempt(
        user_id=session['user_id'],
        topic=data['topic'],
        score=data['score'],
        total_questions=data['total_questions']
    )
    
    db.session.add(attempt)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Score saved'})

@app.route('/api/history')
def get_history():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    attempts = QuizAttempt.query.filter_by(user_id=session['user_id']).order_by(QuizAttempt.completed_at.desc()).limit(10).all()
    
    history = [{
        'topic': attempt.topic,
        'score': attempt.score,
        'total': attempt.total_questions,
        'percentage': round((attempt.score / attempt.total_questions) * 100, 1),
        'date': attempt.completed_at.strftime('%Y-%m-%d %H:%M')
    } for attempt in attempts]
    
    return jsonify({'success': True, 'history': history})

if __name__ == '__main__':
    # Startup verification to check API key before running
    print("\n" + "="*60)
    print("Smart Quizzer - Starting Application")
    print("="*60)
    
    # Verify API key is configured
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("\n❌ ERROR: GROQ_API_KEY not found!")
        print("\nTo fix this:")
        print("1. Create a .env file: cp .env.example .env")
        print("2. Add your Groq API key to the .env file")
        print("3. Get your key from: https://console.groq.com/keys")
        print("\nOr run the verification script: python verify_setup.py")
        print("="*60 + "\n")
        exit(1)
    
    if api_key == 'your-groq-api-key-here':
        print("\n❌ ERROR: GROQ_API_KEY is still set to placeholder!")
        print("\nTo fix this:")
        print("1. Open .env file")
        print("2. Replace 'your-groq-api-key-here' with your actual API key")
        print("3. Get your key from: https://console.groq.com/keys")
        print("\nOr run the verification script: python verify_setup.py")
        print("="*60 + "\n")
        exit(1)
    
    # Show masked API key for verification
    masked_key = f"{api_key[:4]}...{api_key[-4:]}"
    print(f"\n✓ GROQ_API_KEY configured: {masked_key}")
    print("✓ Database initialized")
    print(f"✓ Starting server on http://localhost:5000")
    print("\nRun 'python verify_setup.py' to test your Groq API connection")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
