# Smart Quizzer - AI-Powered Quiz Application

A modern, full-stack quiz application with AI-generated questions powered by Groq. Built with Flask, SQLite, and vanilla JavaScript for a fast, responsive experience.

## Features

- **User Authentication**: Secure login and registration system
- **AI-Generated Quizzes**: Dynamic quiz generation using Groq API
- **15+ Topics**: Wide variety of programming and tech topics
- **Flexible Question Count**: Choose 5-50 questions per quiz
- **Instant Feedback**: See correct/incorrect answers with explanations
- **Score Tracking**: Complete results with grade and percentage
- **Quiz History**: Track all your past quiz attempts
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Clean, vibrant interface with smooth animations

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **AI**: Groq API (Mixtral model)
- **Authentication**: Flask sessions with password hashing

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Groq API key (get one at https://console.groq.com)

## Installation & Setup

### Step-by-Step Setup Guide

Follow these steps carefully to get the application running:

#### Step 1: Install Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

#### Step 2: Create .env File

**Option A: Copy from example (Recommended)**
\`\`\`bash
# On Mac/Linux:
cp .env.example .env

# On Windows (Command Prompt):
copy .env.example .env

# On Windows (PowerShell):
Copy-Item .env.example .env
\`\`\`

**Option B: Create manually**
1. Create a new file named `.env` (with the dot at the start)
2. Add these two lines:
\`\`\`env
SECRET_KEY=your-secret-key-here-change-this-in-production
GROQ_API_KEY=your-groq-api-key-here
\`\`\`

#### Step 3: Get Your Groq API Key

1. Visit https://console.groq.com
2. Sign up or log in
3. Click on "API Keys" in the sidebar
4. Click "Create API Key"
5. Copy the key (it starts with `gsk_`)

#### Step 4: Add API Key to .env File

1. Open the `.env` file in a text editor (Notepad, VS Code, etc.)
2. Find the line: `GROQ_API_KEY=your-groq-api-key-here`
3. Replace `your-groq-api-key-here` with your actual API key
4. Save the file

Your `.env` should look like this:
\`\`\`env
SECRET_KEY=any-random-string-here
GROQ_API_KEY=gsk_abc123xyz789...
\`\`\`

#### Step 5: Verify Setup (Recommended)

Run the verification script to check everything is configured correctly:

\`\`\`bash
python verify_setup.py
\`\`\`

This will:
- Check if .env file exists
- Verify API key is set correctly
- Test connection to Groq API
- Show helpful error messages if something is wrong

#### Step 6: Run the Application

\`\`\`bash
python app.py
\`\`\`

If everything is configured correctly, you'll see:
\`\`\`
============================================================
Smart Quizzer - Starting Application
============================================================

✓ GROQ_API_KEY configured: gsk_...xyz
✓ Database initialized
✓ Starting server on http://localhost:5000
============================================================
\`\`\`

#### Step 7: Access the Application

Open your browser and go to:
\`\`\`
http://localhost:5000
\`\`\`

## How to Use

### First Time Setup

1. **Register**: Click "Register here" on the login page
2. **Create Account**: Enter username, email, and password
3. **Login**: Use your credentials to log in

### Taking a Quiz

1. **Select Topic**: Choose from 15+ available topics
2. **Set Question Count**: Choose between 5-50 questions
3. **Generate Quiz**: Click "Generate Quiz" (AI will create questions)
4. **Answer Questions**: 
   - Click on your answer choice (A, B, C, or D)
   - Click "Submit Answer" to check if you're correct
   - See instant feedback with explanations
5. **Navigate**: Use "Previous" and "Next" buttons
6. **View Results**: See your final score, grade, and statistics

### Quiz History

Your quiz history is automatically saved and displayed on the dashboard, showing:
- Topic name
- Score (correct/total)
- Percentage
- Date and time

## Project Structure

\`\`\`
smart-quizzer/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .env.example           # Environment template
├── quiz.db                # SQLite database (auto-created)
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── index.html        # Dashboard
│   └── quiz.html         # Quiz interface
└── static/               # Static files
    ├── css/
    │   └── style.css     # Main stylesheet
    └── js/
        ├── main.js       # Utility functions
        └── quiz.js       # Quiz logic
\`\`\`

## Available Topics

- JavaScript Programming
- Python Programming
- Web Development
- Data Structures and Algorithms
- Database Management
- Machine Learning
- Cybersecurity
- Cloud Computing
- React Framework
- Node.js
- DevOps
- Mobile Development
- Software Engineering
- Artificial Intelligence
- Computer Networks

## Troubleshooting

### "Failed to generate quiz" Error

If you see this error in the browser, follow these steps:

**Step 1: Check if .env file exists**
\`\`\`bash
# On Mac/Linux:
ls -la .env

# On Windows:
dir .env
\`\`\`

If the file doesn't exist, create it:
\`\`\`bash
cp .env.example .env
\`\`\`

**Step 2: Verify API key is set**

Open `.env` file and check:
- The file contains: `GROQ_API_KEY=gsk_...`
- The key starts with `gsk_`
- There are no quotes around the key
- There are no spaces around the `=` sign

**Step 3: Run verification script**
\`\`\`bash
python verify_setup.py
\`\`\`

This will tell you exactly what's wrong and how to fix it.

**Step 4: Restart the application**

After fixing the .env file:
1. Stop the app (Ctrl+C)
2. Run `python app.py` again

### Common Setup Errors

**Error: `TypeError: Client.__init__() got an unexpected keyword argument 'proxies'`**

This means you have an outdated version of the Groq library. Fix it by:

\`\`\`bash
pip install --upgrade groq
\`\`\`

Or reinstall all dependencies:

\`\`\`bash
pip uninstall groq
pip install -r requirements.txt
\`\`\`

**Error: `groq.GroqError: The api_key client option must be set`**

This means your `.env` file is missing or the API key is not set correctly. Fix it by:

1. Make sure `.env` file exists in the root directory (same folder as `app.py`)
2. Copy from the example: `cp .env.example .env` (or manually create it)
3. Open `.env` and replace `your-groq-api-key-here` with your actual API key
4. Your `.env` should look like:
   \`\`\`env
   SECRET_KEY=any-random-string-here
   GROQ_API_KEY=gsk_your_actual_api_key_here
   \`\`\`
5. Restart the application: `python app.py`

**Error: Application exits immediately with API key error**

The app now checks your API key on startup. If you see an error message:
1. Read the error message carefully - it tells you exactly what to do
2. Run `python verify_setup.py` for detailed diagnostics
3. Fix the issue mentioned in the error
4. Run `python app.py` again

**How to verify your .env file is correct:**
- The file must be named exactly `.env` (with the dot at the start)
- It should be in the same directory as `app.py`
- The API key should start with `gsk_`
- There should be no quotes around the values
- There should be no spaces around the `=` sign

**Windows users - Can't see .env file:**

Windows hides files starting with a dot by default. To see it:
1. Open File Explorer
2. Click "View" tab
3. Check "Hidden items"
4. Check "File name extensions"

Or use Command Prompt to verify:
\`\`\`cmd
dir .env
type .env
\`\`\`

### Port Already in Use

If port 5000 is already in use, change it in `app.py`:

\`\`\`python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change to any available port
\`\`\`

### Groq API Errors

**Error: "Invalid API key"**
- Check that your `GROQ_API_KEY` in `.env` is correct
- Make sure there are no extra spaces or quotes
- Verify the key starts with `gsk_`
- Try generating a new API key from https://console.groq.com

**Error: "Rate limit exceeded"**
- Groq has rate limits on free tier
- Wait a few minutes and try again
- Consider upgrading your Groq plan

**Error: "API key not configured"**
- This means the `.env` file is not being loaded
- Make sure the file is named `.env` (not `.env.txt` or `env`)
- Restart the application after creating/editing `.env`

### Database Issues

**Reset Database:**
\`\`\`bash
rm quiz.db
python app.py  # Will create fresh database
\`\`\`

### Module Not Found Errors

Make sure all dependencies are installed:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

If you still get errors, try:
\`\`\`bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
\`\`\`

### .env File Not Loading

- Make sure `.env` file is in the root directory (same folder as `app.py`)
- Check that `python-dotenv` is installed: `pip install python-dotenv`
- Verify there are no syntax errors in `.env`
- File must be named exactly `.env` (not `.env.txt`)
- On Windows, make sure file extensions are visible to verify the name

**Windows users:** To see file extensions:
1. Open File Explorer
2. Click "View" tab
3. Check "File name extensions"

## Security Notes

**Important for Production:**

1. **Change SECRET_KEY**: Generate a strong random key
   \`\`\`python
   import secrets
   print(secrets.token_hex(32))
   \`\`\`

2. **Disable Debug Mode**: In `app.py`, change:
   \`\`\`python
   app.run(debug=False)
   \`\`\`

3. **Use HTTPS**: Deploy with SSL/TLS certificates

4. **Secure Database**: Use PostgreSQL or MySQL for production

5. **Environment Variables**: Never commit `.env` to version control

## Customization

### Adding More Topics

Edit the topic dropdown in `templates/index.html`:

\`\`\`html
<option value="Your New Topic">Your New Topic</option>
\`\`\`

### Changing AI Model

In `app.py`, modify the model parameter:

\`\`\`python
response = groq_client.chat.completions.create(
    model="llama-3.1-70b-versatile",  # Change model here
    # ... rest of config
)
\`\`\`

Available Groq models:
- `mixtral-8x7b-32768` (default, balanced)
- `llama-3.1-70b-versatile` (more capable)
- `gemma2-9b-it` (faster, lighter)

### Styling

Modify colors in `static/css/style.css` by changing CSS variables:

\`\`\`css
:root {
  --primary: #6366f1;
  --secondary: #8b5cf6;
  /* ... other colors */
}
\`\`\`

## Development

### Running in Development Mode

\`\`\`bash
python app.py
\`\`\`

The app runs with debug mode enabled, which provides:
- Auto-reload on code changes
- Detailed error messages
- Interactive debugger

### Database Schema

**Users Table:**
- id (Primary Key)
- username (Unique)
- email (Unique)
- password (Hashed)
- created_at

**QuizAttempts Table:**
- id (Primary Key)
- user_id (Foreign Key)
- topic
- score
- total_questions
- completed_at

## API Endpoints

- `GET /` - Dashboard (requires login)
- `GET /login` - Login page
- `POST /login` - Login submission
- `GET /register` - Registration page
- `POST /register` - Registration submission
- `GET /logout` - Logout
- `GET /quiz` - Quiz interface
- `POST /api/generate-quiz` - Generate AI quiz
- `POST /api/save-score` - Save quiz results
- `GET /api/history` - Get quiz history

## License

This project is open source and available for educational purposes.

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review the Groq API documentation
3. Check Flask documentation for backend issues

## Credits

- **AI**: Powered by Groq
- **Framework**: Flask
- **Database**: SQLite

---

**Happy Learning! 🎓**
