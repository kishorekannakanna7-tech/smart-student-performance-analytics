# 🚀 Quick Start Guide

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Run the Application

```bash
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

## Step 3: Open in Browser

Navigate to: **http://localhost:5000**

## Step 4: Login

Click "Teacher Login" and use:
- Username: `admin`
- Password: `admin123`

## Step 5: Upload Sample Data

1. Go to "Upload Data" from sidebar
2. Click "Download Sample CSV" 
3. Upload the downloaded CSV file
4. Or use the provided `sample_students.csv` file

## Step 6: Explore Features

- **Dashboard**: View statistics and charts
- **Analytics**: See detailed student table
- **Export**: Download CSV reports

## 🎨 What Makes This Special?

✨ **Glassmorphism Design** - Modern frosted glass effects
🎭 **Smooth Animations** - Professional transitions
📊 **Interactive Charts** - Animated data visualizations
🎯 **AI Predictions** - Smart performance analysis
📱 **Responsive** - Works on all devices

## 🎓 Perfect For

- College project demonstrations
- Portfolio showcases
- Learning Flask and modern web design
- Academic presentations

## 💡 Tips

1. The database is created automatically on first run
2. All data is stored locally in `database.db`
3. You can modify prediction logic in `app.py`
4. Customize colors in `static/css/style.css`

## 🐛 Troubleshooting

**Port already in use?**
```bash
python app.py
# Or specify a different port
flask run --port 5001
```

**Module not found?**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Database errors?**
Delete `database.db` and restart the app (it will recreate)

---

Enjoy your stunning student performance predictor! 🎉
