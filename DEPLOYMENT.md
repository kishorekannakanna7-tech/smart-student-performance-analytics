# 🚀 Deployment Guide

## Local Development

### Windows
```bash
# Double-click run.bat
# OR
python app.py
```

### Mac/Linux
```bash
chmod +x run.sh
./run.sh
# OR
python app.py
```

## Production Deployment Options

### 1. PythonAnywhere (Free & Easy)

1. Create account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Upload project files
3. Create virtual environment:
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```
4. Configure WSGI file
5. Reload web app

### 2. Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn app:app
```
3. Add to requirements.txt:
```
gunicorn==21.2.0
```
4. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

### 3. Railway

1. Connect GitHub repository
2. Railway auto-detects Flask
3. Add environment variables
4. Deploy automatically

### 4. Render

1. Create new Web Service
2. Connect repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `python app.py`

### 5. DigitalOcean App Platform

1. Create new app
2. Connect GitHub
3. Configure build settings
4. Deploy

## Environment Variables

For production, set:

```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
```

Update `app.py`:
```python
import os
app.secret_key = os.environ.get('SECRET_KEY', 'fallback-secret-key')
```

## Database Migration

### For Production (PostgreSQL)

1. Install psycopg2:
```bash
pip install psycopg2-binary
```

2. Update database connection in `app.py`:
```python
import os
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')
```

## Security Checklist

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Add rate limiting
- [ ] Implement CSRF protection
- [ ] Validate all inputs
- [ ] Use environment variables
- [ ] Enable logging
- [ ] Regular backups

## Performance Optimization

### For Production

1. **Use Gunicorn**:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Enable Caching**:
```python
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
```

3. **Compress Assets**:
```python
from flask_compress import Compress
Compress(app)
```

4. **Use CDN** for static files

## Monitoring

### Add Logging

```python
import logging
logging.basicConfig(filename='app.log', level=logging.INFO)
```

### Error Tracking

Consider integrating:
- Sentry
- Rollbar
- New Relic

## Backup Strategy

### Database Backup

```bash
# SQLite
cp database.db database_backup_$(date +%Y%m%d).db

# PostgreSQL
pg_dump dbname > backup.sql
```

### Automated Backups

Set up cron job (Linux):
```bash
0 2 * * * /path/to/backup_script.sh
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer
- Multiple app instances
- Shared database
- Redis for sessions

### Vertical Scaling
- Increase server resources
- Optimize queries
- Add indexes
- Cache frequently accessed data

## Domain Setup

1. Purchase domain
2. Configure DNS:
   - A record pointing to server IP
   - CNAME for www subdomain
3. Enable SSL/TLS (Let's Encrypt)

## Maintenance

### Regular Tasks
- Update dependencies
- Monitor logs
- Check disk space
- Backup database
- Review security
- Update documentation

### Update Dependencies

```bash
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt
```

## Troubleshooting

### Common Issues

**Port in use**:
```bash
lsof -i :5000
kill -9 PID
```

**Permission denied**:
```bash
chmod +x run.sh
```

**Module not found**:
```bash
pip install -r requirements.txt --force-reinstall
```

**Database locked**:
- Close all connections
- Restart application
- Check file permissions

## Support

For deployment issues:
1. Check application logs
2. Verify environment variables
3. Test database connection
4. Review server configuration
5. Check firewall settings

---

Choose the deployment option that best fits your needs and budget! 🚀
