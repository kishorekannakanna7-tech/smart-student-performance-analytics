from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import sqlite3
import csv
import io
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'smart_student_predictor_2024'

# Database initialization
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  register_number TEXT UNIQUE NOT NULL,
                  attendance REAL,
                  internal_marks REAL,
                  assignment_marks REAL,
                  previous_marks REAL,
                  risk_level TEXT,
                  predicted_grade TEXT,
                  pass_probability REAL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Prediction logic
def predict_performance(attendance, internal_marks, assignment_marks, previous_marks):
    # Calculate weighted score
    total_score = (attendance * 0.2) + (internal_marks * 0.3) + (assignment_marks * 0.2) + (previous_marks * 0.3)
    
    # Risk level calculation
    if attendance < 60 or internal_marks < 40:
        risk_level = "High Risk"
    elif attendance < 75 or internal_marks < 50:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"
    
    # Pass probability
    if total_score >= 75:
        pass_probability = 95
    elif total_score >= 60:
        pass_probability = 80
    elif total_score >= 50:
        pass_probability = 60
    else:
        pass_probability = 30
    
    # Predicted grade
    if total_score >= 90:
        grade = "A+"
    elif total_score >= 80:
        grade = "A"
    elif total_score >= 70:
        grade = "B+"
    elif total_score >= 60:
        grade = "B"
    elif total_score >= 50:
        grade = "C"
    else:
        grade = "F"
    
    return risk_level, grade, pass_probability

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Get statistics
    c.execute('SELECT COUNT(*) FROM students')
    total_students = c.fetchone()[0]
    
    c.execute('SELECT AVG(internal_marks) FROM students')
    avg_score = c.fetchone()[0] or 0
    
    c.execute('SELECT COUNT(*) FROM students WHERE risk_level = "High Risk"')
    high_risk = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM students WHERE predicted_grade IN ("A+", "A")')
    top_performers = c.fetchone()[0]
    
    conn.close()
    
    return render_template('dashboard.html', 
                         total_students=total_students,
                         avg_score=round(avg_score, 2),
                         high_risk=high_risk,
                         top_performers=top_performers)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'csv_file' in request.files:
            file = request.files['csv_file']
            if file.filename != '':
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_reader = csv.DictReader(stream)
                
                conn = sqlite3.connect('database.db')
                c = conn.cursor()
                
                for row in csv_reader:
                    risk, grade, prob = predict_performance(
                        float(row['attendance']),
                        float(row['internal_marks']),
                        float(row['assignment_marks']),
                        float(row['previous_marks'])
                    )
                    
                    c.execute('''INSERT OR REPLACE INTO students 
                                (name, register_number, attendance, internal_marks, 
                                assignment_marks, previous_marks, risk_level, 
                                predicted_grade, pass_probability)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                             (row['name'], row['register_number'], 
                              float(row['attendance']), float(row['internal_marks']),
                              float(row['assignment_marks']), float(row['previous_marks']),
                              risk, grade, prob))
                
                conn.commit()
                conn.close()
                return jsonify({'success': True})
        else:
            # Manual entry
            name = request.form.get('name')
            register_number = request.form.get('register_number')
            attendance = float(request.form.get('attendance'))
            internal_marks = float(request.form.get('internal_marks'))
            assignment_marks = float(request.form.get('assignment_marks'))
            previous_marks = float(request.form.get('previous_marks'))
            
            risk, grade, prob = predict_performance(attendance, internal_marks, 
                                                   assignment_marks, previous_marks)
            
            conn = sqlite3.connect('database.db')
            c = conn.cursor()
            c.execute('''INSERT OR REPLACE INTO students 
                        (name, register_number, attendance, internal_marks, 
                        assignment_marks, previous_marks, risk_level, 
                        predicted_grade, pass_probability)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (name, register_number, attendance, internal_marks,
                      assignment_marks, previous_marks, risk, grade, prob))
            conn.commit()
            conn.close()
            
            return jsonify({'success': True})
    
    return render_template('upload.html')

@app.route('/analytics')
@login_required
def analytics():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    risk_filter = request.args.get('risk', 'all')
    search = request.args.get('search', '')
    
    query = 'SELECT * FROM students WHERE 1=1'
    params = []
    
    if risk_filter != 'all':
        query += ' AND risk_level = ?'
        params.append(risk_filter)
    
    if search:
        query += ' AND (name LIKE ? OR register_number LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    c.execute(query, params)
    students = c.fetchall()
    conn.close()
    
    return render_template('analytics.html', students=students)

@app.route('/api/chart-data')
@login_required
def chart_data():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    # Subject scores (simulated)
    c.execute('SELECT AVG(internal_marks), AVG(assignment_marks), AVG(previous_marks) FROM students')
    scores = c.fetchone()
    
    # Pass vs Fail
    c.execute('SELECT COUNT(*) FROM students WHERE pass_probability >= 60')
    pass_count = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM students WHERE pass_probability < 60')
    fail_count = c.fetchone()[0]
    
    # Risk distribution
    c.execute('SELECT risk_level, COUNT(*) FROM students GROUP BY risk_level')
    risk_data = c.fetchall()
    
    conn.close()
    
    return jsonify({
        'subject_scores': {
            'labels': ['Internal Marks', 'Assignment Marks', 'Previous Marks'],
            'data': [scores[0] or 0, scores[1] or 0, scores[2] or 0]
        },
        'pass_fail': {
            'labels': ['Pass', 'Fail'],
            'data': [pass_count, fail_count]
        },
        'risk_distribution': {
            'labels': [r[0] for r in risk_data],
            'data': [r[1] for r in risk_data]
        }
    })

@app.route('/api/insights')
@login_required
def insights():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    
    insights = []
    
    # Attendance insight
    c.execute('SELECT COUNT(*) FROM students WHERE attendance < 65')
    low_attendance = c.fetchone()[0]
    if low_attendance > 0:
        insights.append(f"{low_attendance} students have attendance below 65% - High failure risk!")
    
    # Internal marks insight
    c.execute('SELECT COUNT(*) FROM students WHERE internal_marks < 50')
    weak_internal = c.fetchone()[0]
    if weak_internal > 0:
        insights.append(f"{weak_internal} students are weak in internal marks - Need attention!")
    
    # High performers
    c.execute('SELECT COUNT(*) FROM students WHERE predicted_grade IN ("A+", "A")')
    top_students = c.fetchone()[0]
    insights.append(f"{top_students} students are predicted to score A+ or A grade!")
    
    # Risk analysis
    c.execute('SELECT COUNT(*) FROM students WHERE risk_level = "High Risk"')
    high_risk = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM students')
    total = c.fetchone()[0]
    if total > 0:
        risk_percent = (high_risk / total) * 100
        insights.append(f"{risk_percent:.1f}% of students are in high-risk category")
    
    conn.close()
    
    return jsonify({'insights': insights})

@app.route('/export-csv')
@login_required
def export_csv():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM students')
    students = c.fetchall()
    conn.close()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Register Number', 'Attendance', 'Internal Marks', 
                    'Assignment Marks', 'Previous Marks', 'Risk Level', 
                    'Predicted Grade', 'Pass Probability'])
    writer.writerows(students)
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='student_analytics.csv'
    )

if __name__ == '__main__':
    app.run(debug=True)
