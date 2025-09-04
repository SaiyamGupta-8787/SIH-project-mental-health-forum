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
                          
---
## 📂 Project Structure
- Frontend/ → UI (HTML, CSS, JS)
                                      
- Backend/  → Flask backend (Python + DB)
                                                    
- Docs/     → Documentation, PPT, and other details
                                                  
- .gitignore → Files to ignore (like cache, .env)
                              
- README.md  → Project overview (This file)

**Tree Structure**
```
SIH-project-mental-health-forum/
├── Frontend/         # UI files (HTML, CSS, JS)
├── Backend/          # Flask backend (Python, APIs, Database)
├── Docs/             # Documentation, reports, PPTs
├── .gitignore        # Ignore unnecessary files
├── README.md         # Project overview
└── LICENSE           # License details
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

## 📌 Git/Github Workflow

### 1) Main Branches
- **main** : The Main source file of the project, the final working version of the project, keep it clean, and **Do not modify unless changes are finalized and confirmed.**

- **dev** : Development Branch, we will work here
### 2) Feature Branches

- **feature** : What feature or task **you** are working on

### 3)Workflow
- **feature branch** → **dev** → **main**

---

## 💻 Running The Project Locally
**1) Cloning The Repo**

only first time
### In your Git bash 
First, go to your local folder/directory, the one where you will store the project files, using the command :
```bash
cd ~/<Folder-name>

```
Now clone the project files into your directory

``` bash
git clone https://github.com/SaiyamGupta-8787/SIH-project-mental-health-forum
```
**2) Feature branch**
when you start a new work, make new branch from **dev**
```bash
git checkout dev
git pull origin dev #get latest updates
git checkout -b <feature>/<short/sub-feature name>
```
**3) Working on project**

Work/add features, after doing a small work, commit your changes
```bash
git add -A
git commit -m"Commit Message"
```
#### note : use short forms like 
- feat : for features,
- fix : for fixing bugs,
- docs : for any change in documents, etc.

in your commit messages

**4) Pushing your branch**

Push your changes to Github

```bash
git push origin <feature>/<feature name>
```
**4) Creating Pull Request**
- Repo -> Pull request -> new pull request
- base branch : dev, compare branch : feature/featurename
- write description of what you did
- create the pr
---
**5) Merging**
#### 🔴 Always discuss with the team member/ role partner before merging

- Merge PR -> it goes in dev
- After all feature are tested and finalized, and after discussing with all team members/role partners, team leader will merge dev into main

## 📑 Guidelines
### For our Team
- Always work on a feature branch, never directly on main
- Use simple, clear and conscise commit messages
- Update README and Docs/ when adding new feature/work
- Always talk to all team members / role partner before merging your feature branch into main

---

## 📜 License

**This project is licensed under MIT License.**            
This means anyone can use, modify, and share this project and its contributions, as long as credit is given.
