from dotenv import load_dotenv
import os

load_dotenv()
print("running check_secret")
print("PWD:", os.getcwd())
print("SECRET_KEY =", os.getenv("SECRET_KEY"))