[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square&logo=mit&logoColor=white)](https://opensource.org/licenses/MIT)&nbsp;
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)&nbsp;
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)&nbsp;
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-FF0000?style=flat-square&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)

[![MySQL](https://img.shields.io/badge/MySQL-00758F?style=flat-square&logo=mysql&logoColor=white)](https://www.mysql.com/)&nbsp;
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://www.sqlite.org/)&nbsp;
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)&nbsp;
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)&nbsp;
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)&nbsp;
![Bootstrap](https://img.shields.io/badge/Bootstrap-563D7C?style=flat-square&logo=bootstrap&logoColor=white)
[![Figma](https://img.shields.io/badge/Figma-F24E1E.svg?style=flat-square&logo=figma&logoColor=white)](https://www.figma.com/)


[![VS Code](https://img.shields.io/badge/Editor-VS%20Code-blue?style=flat-square&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)
---

# 🧠 Student Mental Health Forum (SIH 2025)
A web based platform where students can share experiences, seek support, and access mental health resources.
Built for **Smart India Hackathon 2025**
---
## 🕹️ Features (MVP)
▶ Anonymous discussion forum for students
                                  
▶ Peer-to-Peer support with moderation
                        
▶ Resource Hub (Articles, Audio, Video)
                                
▶ Admin Dashboard for reports and trends

▶Guided Self-Help Page – “How are you feeling today?” → Quick tips (video, article, helpline, motivation).

▶Mood Tracker + Diary – Daily check-ins with simple graphs + journaling.

▶Peer Support Forum – Anonymous, moderated student discussions (like Quora).

▶SOS & NGO Connect – One-tap helpline, local NGO links, hidden emergency button.

▶Gamified Wellness – Daily challenges, earn points, grow a digital pet and become healthy according to the mood.

▶Personalized Resources – Stories, tips, and positive quotes based on Indian student life so that student can relate.

▶Screen Break Reminders – Gentle nudges to reduce burnout.

▶Workshops & Counsellor Booking – Online/offline sessions + secure booking.

▶Anonymous Polls – To show “you’re not alone” in facing issues.
                          
---
## 📂 Project Structure
- Frontend/ → UI (HTML, CSS, JS)
                                      
- Backend/  → Flask backend (apps, configs, etc.)

- Database/ → Scripts for MySQL (schema.sql,seed.sql)
                                                    
- Docs/     → Documentation, PPT, and other details
                                                  
- .gitignore → Files to ignore (like cache, .env)
                              
- README.md  → Project overview (This file)

**Tree Structure**
```
SIH-project-mental-health-forum/
│
├── app.py                 # Main Flask app
├── config.py              # DB configurations secret keys
├── models.py              # DB models/quierie 
│
├── templates/             # HTML (frontend)
│   ├── index.html
│   ├── registration.html
│   ├── login.html
│   ├── registration.html
│   └── register.html
│
├── static/                # Static assets
│   ├── css/
│   │   ├── style.css
│   │   └── style2.css
│   ├── js/
│   │   └── script.js
│   └── img/
│       └── logo.jpeg
│
├── database/              # MySQL scripts
│   ├── schema.sql
│   └── seed.sql
│    
│
├── requirements.txt       # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```
---
## 🛠️ Tech Stack (Skills)
- **Version Control** : Git CLI and Github

- **Backend** : Python (Flask, Django, APIs)
                                
- **Database** : MySQL / SQLite + SQLAlchemy / PostgreSQL
                                          
- **Frontend** : HTML5, CSS3, JavaScript, React.js or Jinja2
                                          
- **Deployment** : PythonAnywhere / Render / Vercel
                      
----
## 👥 Team Members
| Name | Role | Focus |
|------|------|-------|
| Jasmine Kaur | Back-end | Database , APIs , Servers , Scaling , Authentication |
| Saiyam Gupta | Back-end | Database , APIs , Servers , Scaling , Authentication |
| Siddhi Mishra | Front-end | UI design , HTML/CSS webpages , Responsive design |
| Pari | Front-end | UI design , HTML/CSS webpages , Responsive design |
| Aadi Jain | Debugging | Front-end debugging , Deployment |
| Naman Jaria | Database | Database , Deployment |

---

## 🚀 Git Workflow Guide  

This guide will explain how our team will use Git.  
Follow these steps to avoid merging conflicts and keep our repo clean.  

---

## 🔹 Branches  
- **main** → stable release (always clean)  
- **dev** → integration branch (all features merge here)  
- **feature branches** → per teammate (one feature = one branch)  

Example branches:  
- `backend-auth`, `backend-api`  
- `frontend-ui`, `frontend-design`  
- `db-schema`  
- `deploy-debug`  

---

## 🔹 First-time setup (once per teammate)  
```bash
# Go in the folder you will keep project files, and Clone the repo
cd <Address of folder>
git clone https://github.com/<username>/<repo>.git
cd <repo>

# Get all branches from GitHub
git fetch origin

# Switch to dev (team base branch)
git checkout dev
```

---

### 🔹 Daily workflow

Before coding (sync with team):
```bash
git checkout dev
git pull origin dev
git checkout <your-branch>
git merge dev   # bring in the latest work
```
---

### 🔹 While coding:
```bash
# Stage and commit your changes
git add .
git commit -m "feat: add login API"

# Push your branch to GitHub
git push origin <your-branch>
```
---

When your feature is ready:

- Open a Pull Request (PR) from <your-branch> → dev on GitHub.

- Another teammate reviews and merges.

---

### 🔹 Deployment workflow

When dev is stable & tested:
```bash
git checkout main
git pull origin main
git merge dev
git push origin main

```

### 🔹 Guidelines

✅ Never code directly on main or dev.  
✅ Pull dev every morning before coding.    
✅ One feature = one branch.    
✅ Write clear commit messages: 

feat: → new feature

fix: → bug fix  
etc

---

## 📜 License

**This project is licensed under MIT License.**            
This means anyone can use, modify, and share this project and its contributions, as long as credit is given.

