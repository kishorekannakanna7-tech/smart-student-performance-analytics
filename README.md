# 🎓 Smart Student Performance Predictor

A visually stunning AI-powered web application for predicting student performance with modern glassmorphism design, smooth animations, and interactive data visualizations.

## ✨ Features

- 🎨 **Modern UI/UX**: Glassmorphism design with gradient backgrounds and smooth animations
- 📊 **Interactive Dashboard**: Real-time statistics and animated charts using Chart.js
- 🤖 **AI Predictions**: Intelligent performance prediction based on multiple parameters
- 📈 **Visual Analytics**: Beautiful data visualization with risk level indicators
- 📤 **Data Upload**: Manual entry and CSV bulk upload support
- 💡 **Smart Insights**: Automated AI-generated insights and recommendations
- 📥 **Export Reports**: Download comprehensive analytics in CSV format
- 🔐 **Secure Login**: Session-based authentication system

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Run the Application**
```bash
python app.py
```

3. **Access the Application**
Open your browser and navigate to:
```
http://localhost:5000
```

### Default Login Credentials

- **Username**: admin
- **Password**: admin123

## 📁 Project Structure

```
project/
│
├── app.py                 # Flask backend application
├── database.db           # SQLite database (auto-created)
├── requirements.txt      # Python dependencies
│
├── templates/            # HTML templates
│   ├── index.html       # Landing page
│   ├── login.html       # Login page
│   ├── dashboard.html   # Main dashboard
│   ├── upload.html      # Data upload page
│   └── analytics.html   # Analytics table
│
└── static/              # Static assets
    ├── css/
    │   └── style.css    # Main stylesheet
    └── js/
        └── main.js      # JavaScript utilities
```

## 📊 CSV Upload Format

When uploading student data via CSV, use this format:

```csv
name,register_number,attendance,internal_marks,assignment_marks,previous_marks
John Doe,2024001,85,75,80,70
Jane Smith,2024002,90,85,88,82
```

**Required Columns:**
- name: Student full name
- register_number: Unique student ID
- attendance: Attendance percentage (0-100)
- internal_marks: Internal exam marks (0-100)
- assignment_marks: Assignment marks (0-100)
- previous_marks: Previous semester marks (0-100)

## 🎯 Prediction Logic

The system uses a weighted scoring algorithm:

- **Attendance**: 20% weight
- **Internal Marks**: 30% weight
- **Assignment Marks**: 20% weight
- **Previous Marks**: 30% weight

### Risk Levels

- **High Risk**: Attendance < 60% OR Internal Marks < 40
- **Medium Risk**: Attendance < 75% OR Internal Marks < 50
- **Low Risk**: All parameters above thresholds

### Grade Prediction

- A+: Total Score ≥ 90
- A: Total Score ≥ 80
- B+: Total Score ≥ 70
- B: Total Score ≥ 60
- C: Total Score ≥ 50
- F: Total Score < 50

## 🎨 Design Features

- **Glassmorphism Cards**: Frosted glass effect with backdrop blur
- **Gradient Backgrounds**: Animated gradient orbs
- **Smooth Animations**: AOS library for scroll animations
- **Interactive Charts**: Chart.js with custom animations
- **Responsive Design**: Mobile-friendly layout
- **Hover Effects**: Interactive UI elements
- **Loading States**: Smooth transitions and loaders

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3 (Glassmorphism, Gradients, Animations)
- JavaScript (ES6+)
- Chart.js (Data Visualization)
- AOS (Animate On Scroll)
- Font Awesome (Icons)

### Backend
- Python Flask
- SQLite Database
- Session-based Authentication

## 📱 Pages Overview

### 1. Landing Page
- Animated hero section
- Feature showcase
- Statistics counters
- Call-to-action buttons

### 2. Login Page
- Floating label inputs
- Smooth form animations
- Error handling
- Demo credentials display

### 3. Dashboard
- Statistics cards
- Interactive charts (Bar, Pie, Line)
- AI-generated insights
- Sidebar navigation

### 4. Upload Data
- Manual form entry
- CSV drag-and-drop upload
- Sample CSV download
- Success animations

### 5. Analytics
- Searchable data table
- Risk level filtering
- Color-coded risk indicators
- CSV export functionality

## 🔧 Customization

### Change Color Scheme
Edit CSS variables in `static/css/style.css`:

```css
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    /* Add your custom colors */
}
```

### Modify Prediction Logic
Edit the `predict_performance()` function in `app.py`

### Add New Features
- Extend database schema in `init_db()`
- Add new routes in `app.py`
- Create corresponding templates

## 🎓 Perfect for

- College Projects
- Academic Demonstrations
- Portfolio Showcases
- Learning Flask & Web Development
- UI/UX Practice

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and use this project for your needs!

## 📧 Support

For issues or questions, please create an issue in the repository.

---

**Made with ❤️ for Students and Educators**
