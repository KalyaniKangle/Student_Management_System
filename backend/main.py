
from fastapi import FastAPI
from supabase import create_client
from dotenv import load_dotenv
import os

# Load variables from .env
load_dotenv()

# Create FastAPI application
app = FastAPI()

# Get Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Connect Python to Supabase
supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# TEST SUPABASE CONNECTION
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


# CREATE STUDENT
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

#STEP 6
#1. READ — Get all students
#Add this below your CREATE endpoint in main.py:


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

# -------------------------
# READ ONE
# -------------------------

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



@app.put("/students/{student_id}")
def update_students(student_id: int, name: str, course: str, marks: int):

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
