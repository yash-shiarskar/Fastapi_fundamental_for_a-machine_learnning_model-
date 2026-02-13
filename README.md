# Fastapi_fundamental_for_a-machine_learnning_model-
🏥 Patient Management API – FastAPI Basics Project
📌 Project Description

This project is a RESTful API built using FastAPI to manage patient records.
It demonstrates core backend concepts including:

Data validation using Pydantic

Request and response handling

Path and query parameters

Computed fields (BMI calculation)

CRUD operations

JSON file-based data storage

Proper HTTP status handling

Input validation with constraints

The API calculates BMI automatically using height and weight and generates a health verdict dynamically.

This project is designed to understand FastAPI fundamentals in a structured and practical way.

🧠 Concepts Covered
1️⃣ FastAPI Application Setup

Creating FastAPI instance

Running server using Uvicorn

Defining routes

2️⃣ Pydantic Models

Used for:

Data validation

Type enforcement

Field constraints

Auto documentation in Swagger UI

Example:

age: Annotated[int, Field(..., gt=0, lt=120)]

This ensures:

Age > 0

Age < 120

3️⃣ Computed Fields

Using:

@computed_field

Automatically calculates:

BMI

Health Verdict

No need to manually store BMI — it updates automatically when height/weight changes.

4️⃣ Path Parameters

Example:

@app.get("/patient/{patient_id}")

Used to fetch a specific patient.

5️⃣ Query Parameters

Example:

@app.get("/sort")

Supports:

sort_by

order

Example usage:

/sort?sort_by=weight&order=desc
6️⃣ CRUD Operations
Method	Route	Description
GET	/view	View all patients
GET	/patient/{id}	View single patient
PUT	/put/{id}	Update patient
DELETE	/delete/{id}	Delete patient
GET	/sort	Sort patients
7️⃣ Error Handling

Uses:

HTTPException

Examples:

404 → Patient not found

400 → Invalid query parameter

📘 API Documentation
🔹 Base URL
http://127.0.0.1:8000
🔹 1. Home Route
GET /

Returns welcome message.

🔹 2. View All Patients
GET /view

Returns all patient records.

🔹 3. View Single Patient
GET /patient/{patient_id}
Path Parameter:

patient_id → ID of the patient

Response:

Returns patient data including:

height

weight

bmi

verdict

🔹 4. Sort Patients
GET /sort
Query Parameters:
Parameter	Type	Required	Description
sort_by	string	Yes	height, weight, bmi
order	string	No	asc or desc

Example:

/sort?sort_by=bmi&order=desc
🔹 5. Update Patient
PUT /put/{patient_id}

Allows partial updates.

Only provided fields will be updated.

Example request body:

{
  "weight": 80,
  "height": 1.78
}

BMI will automatically update.

🔹 6. Delete Patient
DELETE /delete/{patient_id}

Deletes patient record permanently.

🧮 BMI Logic
BMI formula:

BMI = weight / (height²)

Verdict Rules:

BMI Range	Verdict
< 18.5	Underweight
18.5 - 24.9	Normal
≥ 25	Obese
🔐 Validation Features

Age must be between 1 and 119

Height must be > 0

Weight must be > 0

Gender must be:

male

female

others

📂 Data Storage

Data is stored in:

patients.json

Structure:

{
  "P001": {
    "name": "John",
    "city": "Delhi",
    "age": 30,
    "gender": "male",
    "height": 1.75,
    "weight": 75,
    "bmi": 24.49,
    "verdict": "Normal"
  }
}
🚀 How to Run
uvicorn main:app --reload

Open:

http://127.0.0.1:8000/docs

Swagger UI will automatically generate interactive API documentation.

🎯 Learning Outcome

After completing this project, you understand:

FastAPI routing

Pydantic validation

Computed fields

Partial updates

Query filtering & sorting

Exception handling

JSON persistence

API documentation
