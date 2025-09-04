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

tree form
```
Mental-Health-Forum/
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

- **Backend** : Python (Flask,Django, APIs)
                                
- **Database** : MySQL / SQLite + SQLAlchemy / PostgreSQL
                                          
- **Frontend** : HTML5, CSS3, JavaScript, React.js / Jinja2
                                          
- **Deployment** : PythonAnywhere / Render / Vercel
                      
----
## 👥 Team Members
| Name | Role | Focus |
|------|------|-------|
| Jasmine Kaur | Backend | Database , APIs , Servers , Scaling , Authentication |
| Saiyam Gupta | Backend | Database , APIs , Servers , Scaling , Authentication |
| Siddhi Mishra | Frontend | UI design , HTML/CSS webpages , Responsive design |
| Pari | Frontend | UI design , HTML/CSS webpages , Responsive design |
| Aadi Jain | Debugging | Front end debugging , Deployment |
| Naman Jaria| Database | Deployment |

---

## 📌 Git/Github Workflow

### 1) Main Branches
- **main** : The Main source file of the project, the final working version of the project, keep it clean, and **Do Not Touch Unless Completely Sure and Final**

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
when you start a new work, amke new branch from **dev**
```bash
git checkout dev
git pull origin dev updates #get latest
git checkout -b <feature>/< short/sub-feature name >
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

push your changes on github

```bash
git push origin <feature>/<feautre name>
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
- After all feature are teseted and finalised, and after discussing with all team members/role partners, team leader will merge dev into main

## 📑 Guidelines
### For our Team
- Always work on a feature branch, never directly on main
- Use simple, clear and conscise commit messages
- Update README and Docs/ when adding new feature/work
- Always talk to all team members / role partner before merging your feature branch in main

---

## 📜 License

**This project is licensed under MIT License.**            
This means that anyone can use, modify and share this project or any contributions in it as long as credit is given
