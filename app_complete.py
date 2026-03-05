"""
Smart Student Performance Predictor
A Flask web application for predicting student academic performance
with AI-powered analytics and beautiful visualizations
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import sqlite3
import csv
import io
from datetime import datetime
from functools import wraps
import os

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'smart_student_predictor_secret_key_2024'

# Database configuration
DATABASE = 'database.db'

# ============================================================================
# DATABASE FUNCTIONS
# ============================================================================

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            register_number TEXT UNIQUE NOT NULL,
            attendance REAL NOT NULL,
            internal_marks REAL NOT NULL,
            assignment_marks REAL NOT NULL,
            previous_marks REAL NOT NULL,
            risk_level TEXT NOT NULL,
            predicted_grade TEXT NOT NULL,
            pass_probability REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Initialize database on startup
init_db()

# ============================================================================
# AUTHENTICATION DECORATOR
# ============================================================================

def login_required(f):
    """Decorator to require login for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# AI PREDICTION LOGIC
# ============================================================================

def predict_performance(attendance, internal_marks, assignment_marks, previous_marks):
    """
    AI-powered prediction algorithm for student performance
    
    Parameters:
    - attendance: Attendance percentage (0-100)
    - internal_marks: Internal exam marks (0-100)
    - assignment_marks: Assignment marks (0-100)
    - previous_marks: Previous semester marks (0-100)
    
    Returns:
    - risk_level: High Risk, Medium Risk, or Low Risk
    - predicted_grade: A+, A, B+, B, C, or F
    - pass_probability: Probability of passing (0-100)
    """
    
    # Weighted scoring algorithm
    # Attendance: 20%, Internal: 30%, Assignment: 20%, Previous: 30%
    total_score = (
        (attendance * 0.2) + 
        (internal_marks * 0.3) + 
        (assignment_marks * 0.2) + 
        (previous_marks * 0.3)
    )
    
    # Risk level classification
    if attendance < 60 or internal_marks < 40:
        risk_level = "High Risk"
    elif attendance < 75 or internal_marks < 50:
        risk_level = "Medium Risk"
    else:
        risk_level = "Low Risk"
    
    # Pass probability calculation
    if total_score >= 75:
        pass_probability = 95
    elif total_score >= 60:
        pass_probability = 80
    elif total_score >= 50:
        pass_probability = 60
    elif total_score >= 40:
        pass_probability = 40
    else:
        pass_probability = 20
    
    # Grade prediction
    if total_score >= 90:
        predicted_grade = "A+"
    elif total_score >= 80:
        predicted_grade = "A"
    elif total_score >= 70:
        predicted_grade = "B+"
    elif total_score >= 60:
        predicted_grade = "B"
    elif total_score >= 50:
        predicted_grade = "C"
    else:
        predicted_grade = "F"
    
    return risk_level, predicted_grade, pass_probability

# ============================================================================
# ROUTES - PUBLIC PAGES
# ============================================================================

@app.route('/')
def index():
    """Landing page with animated hero section"""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page with authentication"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple authentication (can be extended with database)
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            session['username'] = username
            session['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('index'))

# ============================================================================
# ROUTES - DASHBOARD
# ============================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard with statistics and charts"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get total students count
    cursor.execute('SELECT COUNT(*) as count FROM students')
    total_students = cursor.fetchone()['count']
    
    # Get average score
    cursor.execute('SELECT AVG(internal_marks) as avg_score FROM students')
    result = cursor.fetchone()
    avg_score = round(result['avg_score'], 2) if result['avg_score'] else 0
    
    # Get high risk students count
    cursor.execute('SELECT COUNT(*) as count FROM students WHERE risk_level = ?', ('High Risk',))
    high_risk = cursor.fetchone()['count']
    
    # Get top performers count (A+ and A grades)
    cursor.execute('SELECT COUNT(*) as count FROM students WHERE predicted_grade IN (?, ?)', ('A+', 'A'))
    top_performers = cursor.fetchone()['count']
    
    conn.close()
    
    return render_template('dashboard.html',
                         total_students=total_students,
                         avg_score=avg_score,
                         high_risk=high_risk,
                         top_performers=top_performers)

# ============================================================================
# ROUTES - DATA UPLOAD
# ============================================================================

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """Upload student data - manual entry or CSV file"""
    if request.method == 'POST':
        try:
            # Check if CSV file upload
            if 'csv_file' in request.files:
                file = request.files['csv_file']
                
                if file.filename == '':
                    return jsonify({'success': False, 'message': 'No file selected'})
                
                if not file.filename.endswith('.csv'):
                    return jsonify({'success': False, 'message': 'Please upload a CSV file'})
                
                # Read CSV file
                stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
                csv_reader = csv.DictReader(stream)
                
                conn = get_db_connection()
                cursor = conn.cursor()
                
                uploaded_count = 0
                
                for row in csv_reader:
                    try:
                        # Extract data from CSV
                        name = row['name']
                        register_number = row['register_number']
                        attendance = float(row['attendance'])
                        internal_marks = float(row['internal_marks'])
                        assignment_marks = float(row['assignment_marks'])
                        previous_marks = float(row['previous_marks'])
                        
                        # Predict performance
                        risk_level, predicted_grade, pass_probability = predict_performance(
                            attendance, internal_marks, assignment_marks, previous_marks
                        )
                        
                        # Insert or replace student data
                        cursor.execute('''
                            INSERT OR REPLACE INTO students 
                            (name, register_number, attendance, internal_marks, 
                            assignment_marks, previous_marks, risk_level, 
                            predicted_grade, pass_probability, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (name, register_number, attendance, internal_marks,
                              assignment_marks, previous_marks, risk_level,
                              predicted_grade, pass_probability, datetime.now()))
                        
                        uploaded_count += 1
                    except Exception as e:
                        print(f"Error processing row: {e}")
                        continue
                
                conn.commit()
                conn.close()
                
                return jsonify({
                    'success': True, 
                    'message': f'Successfully uploaded {uploaded_count} students'
                })
            
            # Manual entry
            else:
                name = request.form.get('name')
                register_number = request.form.get('register_number')
                attendance = float(request.form.get('attendance'))
                internal_marks = float(request.form.get('internal_marks'))
                assignment_marks = float(request.form.get('assignment_marks'))
                previous_marks = float(request.form.get('previous_marks'))
                
                # Validate input
                if not all([name, register_number]):
                    return jsonify({'success': False, 'message': 'All fields are required'})
                
                if not (0 <= attendance <= 100 and 0 <= internal_marks <= 100 and 
                       0 <= assignment_marks <= 100 and 0 <= previous_marks <= 100):
                    return jsonify({'success': False, 'message': 'Marks must be between 0 and 100'})
                
                # Predict performance
                risk_level, predicted_grade, pass_probability = predict_performance(
                    attendance, internal_marks, assignment_marks, previous_marks
                )
                
                # Insert into database
                conn = get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO students 
                    (name, register_number, attendance, internal_marks, 
                    assignment_marks, previous_marks, risk_level, 
                    predicted_grade, pass_probability, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, register_number, attendance, internal_marks,
                      assignment_marks, previous_marks, risk_level,
                      predicted_grade, pass_probability, datetime.now()))
                
                conn.commit()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'message': 'Student data added successfully',
                    'prediction': {
                        'risk_level': risk_level,
                        'grade': predicted_grade,
                        'pass_probability': pass_probability
                    }
                })
        
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error: {str(e)}'})
    
    return render_template('upload.html')

# ============================================================================
# ROUTES - ANALYTICS
# ============================================================================

@app.route('/analytics')
@login_required
def analytics():
    """Analytics page with student data table"""
    # Get filter parameters
    risk_filter = request.args.get('risk', 'all')
    search_query = request.args.get('search', '')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Build query with filters
    query = 'SELECT * FROM students WHERE 1=1'
    params = []
    
    # Apply risk filter
    if risk_filter != 'all':
        query += ' AND risk_level = ?'
        params.append(risk_filter)
    
    # Apply search filter
    if search_query:
        query += ' AND (name LIKE ? OR register_number LIKE ?)'
        params.extend([f'%{search_query}%', f'%{search_query}%'])
    
    # Order by risk level (High Risk first)
    query += ' ORDER BY CASE risk_level WHEN "High Risk" THEN 1 WHEN "Medium Risk" THEN 2 ELSE 3 END, name'
    
    cursor.execute(query, params)
    students = cursor.fetchall()
    
    conn.close()
    
    return render_template('analytics.html', students=students)

# ============================================================================
# API ROUTES - CHART DATA
# ============================================================================

@app.route('/api/chart-data')
@login_required
def chart_data():
    """API endpoint for dashboard chart data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Subject scores (average marks)
    cursor.execute('''
        SELECT 
            AVG(internal_marks) as avg_internal,
            AVG(assignment_marks) as avg_assignment,
            AVG(previous_marks) as avg_previous
        FROM students
    ''')
    scores = cursor.fetchone()
    
    # Pass vs Fail counts
    cursor.execute('SELECT COUNT(*) as count FROM students WHERE pass_probability >= 60')
    pass_count = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM students WHERE pass_probability < 60')
    fail_count = cursor.fetchone()['count']
    
    # Risk distribution
    cursor.execute('''
        SELECT risk_level, COUNT(*) as count 
        FROM students 
        GROUP BY risk_level
    ''')
    risk_data = cursor.fetchall()
    
    conn.close()
    
    # Prepare response data
    response = {
        'subject_scores': {
            'labels': ['Internal Marks', 'Assignment Marks', 'Previous Marks'],
            'data': [
                round(scores['avg_internal'] or 0, 2),
                round(scores['avg_assignment'] or 0, 2),
                round(scores['avg_previous'] or 0, 2)
            ]
        },
        'pass_fail': {
            'labels': ['Pass', 'Fail'],
            'data': [pass_count, fail_count]
        },
        'risk_distribution': {
            'labels': [row['risk_level'] for row in risk_data],
            'data': [row['count'] for row in risk_data]
        }
    }
    
    return jsonify(response)

# ============================================================================
# API ROUTES - AI INSIGHTS
# ============================================================================

@app.route('/api/insights')
@login_required
def insights():
    """API endpoint for AI-generated insights"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insights_list = []
    
    # Total students
    cursor.execute('SELECT COUNT(*) as count FROM students')
    total_students = cursor.fetchone()['count']
    
    if total_students == 0:
        insights_list.append("No student data available. Upload data to see insights.")
        return jsonify({'insights': insights_list})
    
    # Insight 1: Low attendance students
    cursor.execute('SELECT COUNT(*) as count FROM students WHERE attendance < 65')
    low_attendance = cursor.fetchone()['count']
    if low_attendance > 0:
        percentage = round((low_attendance / total_students) * 100, 1)
        insights_list.append(
            f"{low_attendance} students ({percentage}%) have attendance below 65% - High failure risk detected!"
        )
    
    # Insight 2: Weak internal marks
    cursor.execute('SELECT COUNT(*) as count FROM students WHERE internal_marks < 50')
    weak_internal = cursor.fetchone()['count']
    if weak_internal > 0:
        percentage = round((weak_internal / total_students) * 100, 1)
        insights_list.append(
            f"{weak_internal} students ({percentage}%) are weak in internal marks - Immediate attention required!"
        )
    
    # Insight 3: High performers
    cursor.execute('SELECT COUNT(*) as count FROM students WHERE predicted_grade IN ("A+", "A")')
    top_students = cursor.fetchone()['count']
    if top_students > 0:
        percentage = round((top_students / total_students) * 100, 1)
        insights_list.append(
            f"{top_students} students ({percentage}%) are predicted to score A+ or A grade - Excellent performance!"
        )
    
    # Insight 4: High risk analysis
    cursor.execute('SELECT COUNT(*) as count FROM students WHERE risk_level = "High Risk"')
    high_risk = cursor.fetchone()['count']
    if high_risk > 0:
        risk_percent = round((high_risk / total_students) * 100, 1)
        insights_list.append(
            f"{risk_percent}% of students are in high-risk category - Intervention programs recommended"
        )
    
    # Insight 5: Pass probability analysis
    cursor.execute('SELECT AVG(pass_probability) as avg_prob FROM students')
    avg_pass_prob = cursor.fetchone()['avg_prob']
    if avg_pass_prob:
        insights_list.append(
            f"Average pass probability is {round(avg_pass_prob, 1)}% across all students"
        )
    
    # Insight 6: Assignment performance
    cursor.execute('SELECT AVG(assignment_marks) as avg_marks FROM students')
    avg_assignment = cursor.fetchone()['avg_marks']
    if avg_assignment and avg_assignment < 60:
        insights_list.append(
            f"Average assignment marks are {round(avg_assignment, 1)}% - Consider additional assignment support"
        )
    
    # Insight 7: Correlation insight
    cursor.execute('''
        SELECT COUNT(*) as count 
        FROM students 
        WHERE attendance >= 75 AND pass_probability >= 80
    ''')
    good_attendance_pass = cursor.fetchone()['count']
    if good_attendance_pass > 0:
        insights_list.append(
            f"Students with 75%+ attendance show significantly higher pass rates - Attendance is key!"
        )
    
    conn.close()
    
    return jsonify({'insights': insights_list})

# ============================================================================
# EXPORT FUNCTIONALITY
# ============================================================================

@app.route('/export-csv')
@login_required
def export_csv():
    """Export all student data as CSV file"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students ORDER BY name')
    students = cursor.fetchall()
    
    conn.close()
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'ID', 'Name', 'Register Number', 'Attendance (%)', 
        'Internal Marks', 'Assignment Marks', 'Previous Marks',
        'Risk Level', 'Predicted Grade', 'Pass Probability (%)',
        'Created At', 'Updated At'
    ])
    
    # Write data rows
    for student in students:
        writer.writerow([
            student['id'],
            student['name'],
            student['register_number'],
            student['attendance'],
            student['internal_marks'],
            student['assignment_marks'],
            student['previous_marks'],
            student['risk_level'],
            student['predicted_grade'],
            student['pass_probability'],
            student['created_at'],
            student['updated_at']
        ])
    
    # Prepare file for download
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'student_analytics_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    )

# ============================================================================
# API ROUTES - STUDENT DETAILS
# ============================================================================

@app.route('/api/student/<int:student_id>')
@login_required
def get_student(student_id):
    """Get individual student details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
    student = cursor.fetchone()
    
    conn.close()
    
    if student:
        return jsonify({
            'success': True,
            'student': dict(student)
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Student not found'
        })

@app.route('/api/delete-student/<int:student_id>', methods=['DELETE'])
@login_required
def delete_student(student_id):
    """Delete a student record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
    conn.commit()
    
    deleted = cursor.rowcount > 0
    conn.close()
    
    if deleted:
        return jsonify({'success': True, 'message': 'Student deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Student not found'})

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# MAIN APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Smart Student Performance Predictor")
    print("=" * 60)
    print("\nStarting application...")
    print("\nAccess the application at: http://localhost:5000")
    print("\nDefault Login Credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\n" + "=" * 60)
    
    # Run the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)
