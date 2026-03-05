"""
Smart Student Performance Analytics Platform
Advanced AI-powered academic analytics system with subject management
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import sqlite3
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'analytics_platform_secret_2024'

DATABASE = 'analytics.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Subjects table
    c.execute('''CREATE TABLE IF NOT EXISTS subjects
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT UNIQUE NOT NULL,
                  code TEXT UNIQUE NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Students table with subject relationship
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  register_number TEXT NOT NULL,
                  subject_id INTEGER NOT NULL,
                  attendance REAL NOT NULL,
                  internal_marks REAL NOT NULL,
                  assignment_marks REAL NOT NULL,
                  previous_marks REAL NOT NULL,
                  risk_level TEXT NOT NULL,
                  predicted_grade TEXT NOT NULL,
                  pass_probability REAL NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (subject_id) REFERENCES subjects(id),
                  UNIQUE(register_number, subject_id))''')
    
    conn.commit()
    conn.close()

init_db()

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def predict_performance(attendance, internal, assignment, previous):
    total = (attendance * 0.2) + (internal * 0.3) + (assignment * 0.2) + (previous * 0.3)
    
    if internal < 40 or attendance < 60:
        risk = "High Risk"
    elif internal < 55:
        risk = "Medium Risk"
    else:
        risk = "Low Risk"
    
    if total >= 75:
        prob = 95
    elif total >= 60:
        prob = 80
    elif total >= 50:
        prob = 60
    else:
        prob = 30
    
    if total >= 90:
        grade = "A+"
    elif total >= 80:
        grade = "A"
    elif total >= 70:
        grade = "B+"
    elif total >= 60:
        grade = "B"
    elif total >= 50:
        grade = "C"
    else:
        grade = "F"
    
    return risk, grade, prob

@app.route('/')
def index():
    return render_template('analytics_index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'success': True})
        return jsonify({'success': False, 'message': 'Invalid credentials'})
    return render_template('analytics_login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    subjects = conn.execute('SELECT * FROM subjects ORDER BY name').fetchall()
    conn.close()
    return render_template('analytics_dashboard.html', subjects=subjects)

@app.route('/api/subjects', methods=['GET', 'POST'])
@login_required
def manage_subjects():
    conn = get_db()
    if request.method == 'POST':
        data = request.json
        try:
            conn.execute('INSERT INTO subjects (name, code) VALUES (?, ?)',
                        (data['name'], data['code']))
            conn.commit()
            return jsonify({'success': True})
        except:
            return jsonify({'success': False, 'message': 'Subject already exists'})
        finally:
            conn.close()
    else:
        subjects = conn.execute('SELECT * FROM subjects ORDER BY name').fetchall()
        conn.close()
        return jsonify([dict(s) for s in subjects])

@app.route('/api/subjects/<int:subject_id>/students', methods=['GET', 'POST'])
@login_required
def manage_students(subject_id):
    conn = get_db()
    if request.method == 'POST':
        data = request.json
        risk, grade, prob = predict_performance(
            float(data['attendance']),
            float(data['internal_marks']),
            float(data['assignment_marks']),
            float(data['previous_marks'])
        )
        try:
            conn.execute('''INSERT INTO students 
                           (name, register_number, subject_id, attendance, internal_marks,
                            assignment_marks, previous_marks, risk_level, predicted_grade, pass_probability)
                           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                        (data['name'], data['register_number'], subject_id,
                         data['attendance'], data['internal_marks'], data['assignment_marks'],
                         data['previous_marks'], risk, grade, prob))
            conn.commit()
            return jsonify({'success': True})
        except:
            return jsonify({'success': False, 'message': 'Student already exists in this subject'})
        finally:
            conn.close()
    else:
        students = conn.execute('SELECT * FROM students WHERE subject_id = ?', (subject_id,)).fetchall()
        conn.close()
        return jsonify([dict(s) for s in students])

@app.route('/subject/<int:subject_id>')
@login_required
def subject_analytics(subject_id):
    conn = get_db()
    subject = conn.execute('SELECT * FROM subjects WHERE id = ?', (subject_id,)).fetchone()
    conn.close()
    return render_template('subject_analytics.html', subject=subject)

@app.route('/api/subjects/<int:subject_id>/analytics')
@login_required
def get_subject_analytics(subject_id):
    conn = get_db()
    students = conn.execute('SELECT * FROM students WHERE subject_id = ?', (subject_id,)).fetchall()
    
    if not students:
        conn.close()
        return jsonify({'students': [], 'stats': {}, 'charts': {}})
    
    total = len(students)
    avg_score = sum(s['internal_marks'] for s in students) / total
    high_risk = sum(1 for s in students if s['risk_level'] == 'High Risk')
    pass_count = sum(1 for s in students if s['pass_probability'] >= 60)
    fail_count = total - pass_count
    
    top_students = sorted(students, key=lambda x: x['internal_marks'], reverse=True)[:3]
    weak_students = sorted(students, key=lambda x: x['internal_marks'])[:3]
    
    conn.close()
    
    return jsonify({
        'stats': {
            'total': total,
            'avg_score': round(avg_score, 2),
            'high_risk': high_risk,
            'risk_percentage': round((high_risk/total)*100, 1)
        },
        'top_students': [dict(s) for s in top_students],
        'weak_students': [dict(s) for s in weak_students],
        'charts': {
            'scores': [s['internal_marks'] for s in students],
            'names': [s['name'] for s in students],
            'pass_fail': [pass_count, fail_count]
        }
    })

@app.route('/heatmap')
@login_required
def heatmap():
    return render_template('heatmap.html')

@app.route('/api/heatmap-data')
@login_required
def heatmap_data():
    conn = get_db()
    subjects = conn.execute('SELECT * FROM subjects ORDER BY name').fetchall()
    
    students_dict = {}
    for subject in subjects:
        students = conn.execute('SELECT * FROM students WHERE subject_id = ?', (subject['id'],)).fetchall()
        for student in students:
            if student['register_number'] not in students_dict:
                students_dict[student['register_number']] = {
                    'name': student['name'],
                    'register_number': student['register_number'],
                    'subjects': {}
                }
            students_dict[student['register_number']]['subjects'][subject['name']] = student['internal_marks']
    
    conn.close()
    
    return jsonify({
        'subjects': [s['name'] for s in subjects],
        'students': list(students_dict.values())
    })

@app.route('/api/insights')
@login_required
def get_insights():
    conn = get_db()
    insights = []
    
    subjects = conn.execute('SELECT * FROM subjects').fetchall()
    
    for subject in subjects:
        students = conn.execute('SELECT * FROM students WHERE subject_id = ?', (subject['id'],)).fetchall()
        if students:
            avg = sum(s['internal_marks'] for s in students) / len(students)
            if avg < 50:
                insights.append(f"{subject['name']} has the lowest class average ({avg:.1f}%)")
    
    all_students = conn.execute('SELECT * FROM students').fetchall()
    if all_students:
        low_att = [s for s in all_students if s['attendance'] < 65]
        if low_att:
            insights.append(f"Students with attendance below 65% have 3x higher failure risk")
        
        high_risk = sum(1 for s in all_students if s['risk_level'] == 'High Risk')
        if high_risk > 0:
            insights.append(f"{high_risk} students are at high risk across all subjects")
    
    conn.close()
    return jsonify({'insights': insights})

@app.route('/api/chatbot', methods=['POST'])
@login_required
def chatbot():
    query = request.json.get('query', '').lower()
    conn = get_db()
    
    response = "I'm not sure how to answer that. Try asking about high-risk students or subject performance."
    
    if 'high risk' in query or 'at risk' in query:
        students = conn.execute('SELECT DISTINCT name, register_number FROM students WHERE risk_level = "High Risk"').fetchall()
        if students:
            names = ', '.join([s['name'] for s in students[:5]])
            response = f"High-risk students: {names}"
        else:
            response = "No high-risk students found."
    
    elif 'lowest' in query or 'worst' in query:
        subjects = conn.execute('SELECT * FROM subjects').fetchall()
        lowest = None
        lowest_avg = 100
        for subject in subjects:
            students = conn.execute('SELECT AVG(internal_marks) as avg FROM students WHERE subject_id = ?', (subject['id'],)).fetchone()
            if students['avg'] and students['avg'] < lowest_avg:
                lowest_avg = students['avg']
                lowest = subject['name']
        if lowest:
            response = f"{lowest} has the lowest performance with {lowest_avg:.1f}% average."
    
    elif 'top' in query or 'best' in query:
        students = conn.execute('SELECT name, internal_marks FROM students ORDER BY internal_marks DESC LIMIT 3').fetchall()
        if students:
            names = ', '.join([f"{s['name']} ({s['internal_marks']}%)" for s in students])
            response = f"Top performers: {names}"
    
    conn.close()
    return jsonify({'response': response})

if __name__ == '__main__':
    print("Smart Student Performance Analytics Platform")
    print("Access at: http://localhost:5000")
    print("Login: admin / admin123")
    app.run(debug=True, host='0.0.0.0', port=5000)
