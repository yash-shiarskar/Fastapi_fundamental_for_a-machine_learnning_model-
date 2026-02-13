from fastapi import FastAPI, Path, HTTPException, Query
from pydantic import BaseModel, Field, ValidationError, computed_field
from typing import Literal, Annotated, Optional
from fastapi.responses import JSONResponse
import json

app = FastAPI()

# ==============================
#           MODEL
# ==============================

class Patient(BaseModel):

    id: Annotated[str, Field(..., description="ID of the patient", examples=["P001"])]
    name: Annotated[str, Field(..., description="Name of the patient")]
    city: Annotated[str, Field(..., description="City where the patient is living")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender of the patient")]
    height: Annotated[float, Field(..., gt=0, description="Height of the patient in mtrs")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the patient in kgs")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)

    # verdict taking help OF a bmi feild which is agaien this is comuputed field,
    # that is now verdict going to trigger bmi() this function too.
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        else:
            return 'Obese'


class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


# ==============================
#        UILITY FUNCTIONS
# ==============================

def load_data():
    try:
        with open("patients.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data


def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)


# ==============================
#            ROUTES
# ==============================

@app.get("/")
def home():
    return {"message": "Welcome to Patient API"}


@app.get("/view")
def get_patients():
    return load_data()


@app.get("/patient/{patient_id}")
def view_patient(
    patient_id: str = Path(..., description="Enter the patient ID")
):
    data = load_data()

    if patient_id in data:
        return data[patient_id]

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(..., description="Sort by height, weight or bmi"),
    order: str = Query("asc", description="Sort in asc or desc order")
):
    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field. Choose from {valid_fields}"
        )

    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid order. Choose 'asc' or 'desc'"
        )

    data = load_data()

    sorted_data = sorted(
        data.values(),
        key=lambda x: x.get(sort_by, 0),
        reverse=True if order == "desc" else False
    )

    return sorted_data


# ==============================
#        UPDATE ROUTE
# ==============================

@app.put('/put/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate): # this means is that "patient_update" should be validate fron this "PatientUpdate "pydantic 
    #  patient_update throgh this varible request body that client send that new information to update this feild 
    # patient_update this is object of this PatientUpdate
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient is Not Found')
    
    existing_pateint_info = data[patient_id]  # # this will extract existing information of pateints.

    #  patient_update (is object sai ) yaha sai hame naye field ki value nikalni hai.

    # patient_update this is pydantic object we have to convert this to  dictionary 
    updated_patient_info = patient_update.model_dump(exclude_unset=True)  # exclude_unse none item will be excluded t=True
    # updated_patient_info this will have only new feild given by client.

    for key, value in updated_patient_info.items():
        existing_pateint_info[key] = value  # we run a loop on a updated_patient_info
        # and updated in a existing_pateint_info 
        # now if we change a weight and height then bmi also going to change so also verdict too
        # this is where tricky part start let's go 

    # existing_pateint_info[(updated dictionary ) -> pydantic object ->updated bmi+verdict ->now will convert this pydantic objct to a dictionary 

    existing_pateint_info['id'] = patient_id  # we have to add this id back beacause it giving us error while crating a pydantic object
    
    # now we can crate a  pydantic object
    patients_pydantic_object = Patient(**existing_pateint_info)

    existing_pateint_info = patients_pydantic_object.model_dump(exclude='id')
    data[patient_id] = existing_pateint_info

    save_data(data)
    return JSONResponse(status_code=202, content={'message': 'patient updated'})
@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    # load data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'patient deleted'})

# ==============================
#       TESTING FUNCTIONS
# ==============================

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted")


def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("updated")


# ==============================
#      SAFE TEST BLOCK
# ==============================

if __name__ == "__main__":

    patient_info = {
        "id": "P100",
        "name": "nitish",
        "city": "Delhi",
        "age": 30,
        "gender": "male",
        "height": 1.75,
        "weight": 75.2
    }

    try:
        patient1 = Patient(**patient_info)

        insert_patient_data(patient1)
        update_patient_data(patient1)

    except ValidationError as e:
        print("Validation Error:")
        print(e)
