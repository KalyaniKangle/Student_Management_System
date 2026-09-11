from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv
import os


# --------------------------------------------------
# Load variables from .env
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# Create FastAPI application
# --------------------------------------------------

app = FastAPI()


# --------------------------------------------------
# Find frontend folder
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"


# --------------------------------------------------
# CORS configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Serve frontend files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


# --------------------------------------------------
# Open index.html when visiting /
# --------------------------------------------------

@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


# --------------------------------------------------
# Get Supabase credentials
# --------------------------------------------------

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


# --------------------------------------------------
# Connect Python to Supabase
# --------------------------------------------------

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# --------------------------------------------------
# TEST SUPABASE CONNECTION
# --------------------------------------------------

@app.get("/test-supabase")
def test_supabase():
    try:
        response = (
            supabase
            .table("students")
            .select("*")
            .limit(1)
            .execute()
        )

        return {
            "message": "Supabase connected successfully!",
            "data": response.data
        }

    except Exception as e:
        return {
            "message": "Supabase connection failed",
            "error": str(e)
        }


# --------------------------------------------------
# CREATE STUDENT
# --------------------------------------------------

@app.post("/students")
def create_student(name: str, course: str, marks: int):

    # Data to be inserted into Supabase
    student = {
        "name": name,
        "course": course,
        "marks": marks
    }

    # Insert student into Supabase
    response = (
        supabase
        .table("students")
        .insert(student)
        .execute()
    )

    # Return database response
    return {
        "message": "Student created successfully",
        "data": response.data
    }


# --------------------------------------------------
# READ — Get all students
# --------------------------------------------------

@app.get("/students")
def get_students():

    # Read all records from students table
    response = (
        supabase
        .table("students")
        .select("*")
        .execute()
    )

    # Send database records as API response
    return {
        "message": "Students fetched successfully",
        "data": response.data
    }


# --------------------------------------------------
# READ ONE — Get student by ID
# --------------------------------------------------

@app.get("/students/{student_id}")
def get_student(student_id: int):

    response = (
        supabase
        .table("students")
        .select("*")
        .eq("id", student_id)
        .execute()
    )

    return {
        "message": "Student fetched successfully",
        "data": response.data
    }


# --------------------------------------------------
# UPDATE STUDENT
# --------------------------------------------------

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    name: str,
    course: str,
    marks: int
):

    # Data to be updated in Supabase
    student = {
        "name": name,
        "course": course,
        "marks": marks
    }

    # Update student in Supabase
    response = (
        supabase
        .table("students")
        .update(student)
        .eq("id", student_id)
        .execute()
    )

    # Return database response
    return {
        "message": "Student updated successfully",
        "data": response.data
    }


# --------------------------------------------------
# DELETE STUDENT
# --------------------------------------------------

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    # Delete student from Supabase
    response = (
        supabase
        .table("students")
        .delete()
        .eq("id", student_id)
        .execute()
    )

    # Return database response
    return {
        "message": "Student deleted successfully",
        "data": response.data
    }