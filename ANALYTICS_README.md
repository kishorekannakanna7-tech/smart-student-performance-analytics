# 🎓 Smart Student Performance Analytics Platform

A visually stunning, AI-powered academic analytics system with advanced features including subject management, performance heatmaps, interactive charts, and an intelligent chatbot assistant.

## ✨ Key Features

### 🎯 Core Functionality

1. **Subject Management**
   - Create and manage multiple subjects (Mathematics, Data Structures, DBMS, etc.)
   - Each subject has dedicated analytics dashboard
   - Subject-wise student tracking

2. **Student Management**
   - Add students to specific subjects
   - Track attendance, internal marks, assignments, and previous performance
   - Automatic risk level prediction
   - Grade prediction with pass probability

3. **Subject Analytics Dashboard**
   - Real-time statistics (total students, average score, high-risk count)
   - Interactive animated charts (Bar, Pie, Line)
   - Top performers and weak students lists
   - Comprehensive student data table

4. **AI Performance Heatmap**
   - Visual grid showing student performance across all subjects
   - Color-coded cells:
     - 🟢 Green (80-100): Excellent
     - 🟡 Yellow (60-79): Average
     - 🟠 Orange (40-59): Weak
     - 🔴 Red (0-39): Critical
   - Instant identification of struggling students

5. **AI Insights Panel**
   - Automatically generated insights
   - Identifies subjects with low performance
   - Highlights attendance-related risks
   - Provides actionable recommendations

6. **Teacher Chatbot**
   - Bottom-right corner AI assistant
   - Answers queries like:
     - "Which students are high risk?"
     - "Which subject has lowest performance?"
     - "Who are the top performers?"
   - Real-time data-driven responses

### 🎨 Visual Design

- **Glassmorphism UI**: Frosted glass effect cards
- **Animated Gradients**: Dynamic background orbs
- **Smooth Animations**: Page transitions and hover effects
- **Modern Dashboard**: SaaS-style interface
- **Responsive Design**: Works on all devices
- **Interactive Charts**: Chart.js with animations

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install flask

# Run the application
python app_analytics.py
```

### Access

Open your browser and navigate to:
```
http://localhost:5000
```

### Login Credentials

```
Username: admin
Password: admin123
```

## 📊 How to Use

### Step 1: Create Subjects

1. Login to the dashboard
2. Click the "+" button in the sidebar
3. Enter subject name (e.g., "Data Structures")
4. Enter subject code (e.g., "CS201")
5. Click "Add Subject"

### Step 2: Add Students

1. Click on a subject from the sidebar or dashboard
2. Click "Add Student" button
3. Fill in student details:
   - Name
   - Register Number
   - Attendance %
   - Internal Marks
   - Assignment Marks
   - Previous Semester Marks
4. System automatically predicts risk level and grade

### Step 3: View Analytics

- **Subject Dashboard**: View charts and statistics
- **Heatmap**: Navigate to heatmap page to see cross-subject performance
- **AI Insights**: Check automated insights on dashboard

### Step 4: Use Chatbot

1. Click the chatbot in bottom-right corner
2. Ask questions about student performance
3. Get instant AI-powered responses

## 🤖 AI Prediction Logic

### Risk Level Classification

```python
if internal_marks < 40 OR attendance < 60:
    risk_level = "High Risk"
elif internal_marks < 55:
    risk_level = "Medium Risk"
else:
    risk_level = "Low Risk"
```

### Grade Prediction

- **A+**: Total Score ≥ 90
- **A**: Total Score ≥ 80
- **B+**: Total Score ≥ 70
- **B**: Total Score ≥ 60
- **C**: Total Score ≥ 50
- **F**: Total Score < 50

### Weighted Scoring

```
Total Score = (Attendance × 0.2) + 
              (Internal × 0.3) + 
              (Assignment × 0.2) + 
              (Previous × 0.3)
```

## 📁 Project Structure

```
analytics-platform/
│
├── app_analytics.py          # Flask backend
├── analytics.db              # SQLite database (auto-created)
│
├── templates/
│   ├── analytics_index.html      # Landing page
│   ├── analytics_login.html      # Login page
│   ├── analytics_dashboard.html  # Main dashboard
│   ├── subject_analytics.html    # Subject analytics
│   └── heatmap.html              # Performance heatmap
│
└── static/
    ├── css/
    │   └── analytics.css         # Complete styling
    └── js/
        └── analytics.js          # JavaScript utilities
```

## 🎯 Database Schema

### Subjects Table
```sql
- id (PRIMARY KEY)
- name (TEXT, UNIQUE)
- code (TEXT, UNIQUE)
- created_at (TIMESTAMP)
```

### Students Table
```sql
- id (PRIMARY KEY)
- name (TEXT)
- register_number (TEXT)
- subject_id (FOREIGN KEY)
- attendance (REAL)
- internal_marks (REAL)
- assignment_marks (REAL)
- previous_marks (REAL)
- risk_level (TEXT)
- predicted_grade (TEXT)
- pass_probability (REAL)
- created_at (TIMESTAMP)
```

## 🎨 UI Components

### Landing Page
- Animated hero section
- Feature showcase cards
- Statistics counters
- Gradient background with floating orbs

### Dashboard
- Sidebar navigation with subject list
- AI insights panel
- Subject cards grid
- Add subject modal

### Subject Analytics
- Statistics cards (Total, Average, Risk)
- Bar chart (Student scores)
- Pie chart (Pass vs Fail)
- Top performers list
- Weak students list
- Complete student table

### Heatmap
- Color-coded performance grid
- Students vs Subjects matrix
- Legend for color interpretation
- Automated heatmap insights

### Chatbot
- Fixed bottom-right position
- Collapsible interface
- Message history
- Real-time responses

## 🔧 API Endpoints

### Subjects
- `GET /api/subjects` - Get all subjects
- `POST /api/subjects` - Create new subject

### Students
- `GET /api/subjects/<id>/students` - Get students for subject
- `POST /api/subjects/<id>/students` - Add student to subject

### Analytics
- `GET /api/subjects/<id>/analytics` - Get subject analytics
- `GET /api/heatmap-data` - Get heatmap data
- `GET /api/insights` - Get AI insights

### Chatbot
- `POST /api/chatbot` - Send query to chatbot

## 💡 Chatbot Queries

The chatbot understands:

- **High Risk Students**: "Which students are high risk?" or "Show at-risk students"
- **Subject Performance**: "Which subject has lowest performance?" or "Worst performing subject"
- **Top Performers**: "Who are the top students?" or "Show best performers"

## 🎓 Perfect For

- College project demonstrations
- Academic presentations
- Portfolio showcases
- Learning Flask and modern web design
- Data visualization projects
- AI/ML project demonstrations

## 🌟 What Makes It Special

### Professional Appearance
- Modern SaaS dashboard design
- Glassmorphism and gradient effects
- Smooth animations throughout
- Interactive data visualizations

### Advanced Features
- Multi-subject management
- Cross-subject performance heatmap
- AI-powered chatbot
- Automated insights generation
- Real-time analytics

### Beginner-Friendly
- Simple Flask backend
- SQLite database (no setup required)
- Clean code structure
- Well-documented
- Easy to extend

## 🚀 Future Enhancements

- Email notifications for at-risk students
- PDF report generation
- Export heatmap as image
- Advanced ML models (scikit-learn)
- Student login portal
- Parent access dashboard
- Attendance tracking system
- Assignment submission portal

## 📝 Technologies Used

### Backend
- Python 3.8+
- Flask 3.0
- SQLite

### Frontend
- HTML5
- CSS3 (Glassmorphism, Gradients)
- JavaScript (ES6+)
- Chart.js
- AOS (Animate On Scroll)
- Font Awesome

## 🎯 Key Differences from Basic Version

| Feature | Basic Version | Analytics Platform |
|---------|--------------|-------------------|
| Subject Management | ❌ | ✅ Multiple subjects |
| Heatmap | ❌ | ✅ Visual performance grid |
| Chatbot | ❌ | ✅ AI assistant |
| Subject Analytics | ❌ | ✅ Per-subject dashboards |
| Cross-subject View | ❌ | ✅ Heatmap comparison |
| Sidebar Navigation | ❌ | ✅ Dynamic subject list |

## 🐛 Troubleshooting

**Database errors?**
- Delete `analytics.db` and restart (auto-recreates)

**Port already in use?**
```bash
python app_analytics.py
# Or change port in code
```

**Charts not showing?**
- Check internet connection (Chart.js CDN)
- Ensure students are added to subjects

## 📧 Support

For issues or questions:
1. Check this documentation
2. Review code comments
3. Test with sample data

---

**Made with ❤️ for Academic Excellence**

*Transform your academic analytics with AI-powered insights!*
