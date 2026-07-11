from flask import Flask, render_template_string, request, redirect, session, url_for, flash
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Database Config - Un password irundha inga podu
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'todo_db'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('exam'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        if not conn:
            flash('Database connection failed', 'error')
            return render_template_string(LOGIN_TEMPLATE)

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Testing ku plain password check. Production la hash use pannu
        if user and user['password'] == password:
            session['user_id'] = user['id']
            session['username'] = username
            return redirect(url_for('exam'))
        else:
            flash('Invalid username or password', 'error')

    return render_template_string(LOGIN_TEMPLATE)

@app.route('/exam')
def exam():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions ORDER BY id")
    questions = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template_string(EXAM_TEMPLATE, questions=questions, username=session['username'])

@app.route('/submit', methods=['POST'])
def submit():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Pazhaya answers ah delete pannu
    cursor.execute("DELETE FROM user_answers WHERE user_id = %s", (user_id,))

    # Correct answers ah eduthuko
    cursor.execute("SELECT id, correct_answer FROM questions")
    correct_answers = {q['id']: q['correct_answer'] for q in cursor.fetchall()}

    score = 0
    for key, selected in request.form.items():
        if key.startswith('question_'):
            q_id = int(key.split('_')[1])
            is_correct = 1 if selected == correct_answers.get(q_id) else 0
            if is_correct:
                score += 1
            cursor.execute(
                "INSERT INTO user_answers (user_id, question_id, selected_answer, is_correct) VALUES (%s, %s, %s, %s)",
                (user_id, q_id, selected, is_correct)
            )

    conn.commit()
    cursor.close()
    conn.close()

    session['last_score'] = score
    session['total_questions'] = len(correct_answers)
    return redirect(url_for('result'))

@app.route('/result')
def result():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    score = session.get('last_score', 0)
    total = session.get('total_questions', 0)
    percentage = (score / total * 100) if total > 0 else 0

    return render_template_string(RESULT_TEMPLATE, score=score, total=total,
                                percentage=round(percentage, 2), username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# HTML Templates
LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Exam Portal</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-4">
                <div class="card shadow">
                    <div class="card-header text-center"><h4>Exam Portal Login</h4></div>
                    <div class="card-body">
                        {% with messages = get_flashed_messages(with_categories=true) %}
                            {% if messages %}{% for category, message in messages %}
                                <div class="alert alert-{{ 'danger' if category == 'error' else 'success' }}">{{ message }}</div>
                            {% endfor %}{% endif %}
                        {% endwith %}
                        <form method="POST">
                            <div class="mb-3">
                                <label>Username</label>
                                <input type="text" name="username" class="form-control" required>
                            </div>
                            <div class="mb-3">
                                <label>Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Login</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

EXAM_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Exam</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <span class="navbar-brand">Welcome, {{ username }}</span>
            <a href="/logout" class="btn btn-outline-light btn-sm">Logout</a>
        </div>
    </nav>
    <div class="container mt-4">
        <div class="card shadow">
            <div class="card-header"><h4>Technical Assessment</h4></div>
            <div class="card-body">
                <form method="POST" action="/submit">
                    {% for q in questions %}
                    <div class="mb-4 p-3 border rounded">
                        <p><strong>Q{{ loop.index }}: {{ q.question_text }}</strong></p>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="question_{{ q.id }}" value="{{ q.option_a }}" required>
                            <label class="form-check-label">{{ q.option_a }}</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="question_{{ q.id }}" value="{{ q.option_b }}">
                            <label class="form-check-label">{{ q.option_b }}</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="question_{{ q.id }}" value="{{ q.option_c }}">
                            <label class="form-check-label">{{ q.option_c }}</label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="question_{{ q.id }}" value="{{ q.option_d }}">
                            <label class="form-check-label">{{ q.option_d }}</label>
                        </div>
                    </div>
                    {% endfor %}
                    <button type="submit" class="btn btn-success w-100">Submit Answers</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
'''

RESULT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Result</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
    <nav class="navbar navbar-dark bg-dark">
        <div class="container">
            <span class="navbar-brand">Welcome, {{ username }}</span>
            <a href="/logout" class="btn btn-outline-light btn-sm">Logout</a>
        </div>
    </nav>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card shadow text-center">
                    <div class="card-header"><h4>Assessment Result</h4></div>
                    <div class="card-body">
                        <h2 class="display-4">{{ score }}/{{ total }}</h2>
                        <p class="lead">You scored {{ percentage }}%</p>
                        {% if percentage >= 80 %}
                            <div class="alert alert-success">Excellent Performance!</div>
                        {% elif percentage >= 60 %}
                            <div class="alert alert-warning">Good Job!</div>
                        {% else %}
                            <div class="alert alert-danger">Need Improvement</div>
                        {% endif %}
                        <a href="/exam" class="btn btn-primary">Retake Exam</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, port=5000)
