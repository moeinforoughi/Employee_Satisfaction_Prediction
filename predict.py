import pickle
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

# Load model
model_file = 'model.bin'

with open(model_file, 'rb') as f_in:
    dv, model = pickle.load(f_in)

# Emplyee Format
class Employee(BaseModel):
    employee_number: int
    employee_name: str
    employee_age: int
    maritial_status: int
    current_salary: float
    number_of_children: int
    years_experience: int
    past_projects: int
    current_projects: int
    divorced_earlier: str
    father_alive: str
    mother_alive: str
    performance_rating: int
    education_level: str
    department: str
    role: str
    work_life_balance: float
    is_outlier: Optional[int] = 0

# Initialize FastAPI
app = FastAPI()

# Prediction endpoint
@app.post('/predict')
async def predict_employee(employee: Employee):
    # Convert Pydantic model to dict
    emp_dict = employee.dict()
    
    # Transform with DictVectorizer
    X = dv.transform([emp_dict])
    
    # Predict job satisfaction (0-1 scale)
    y_pred_scaled = model.predict(X)
    
    # Convert to original scale (0-10)
    y_pred = float(y_pred_scaled[0] * 10)
    
    result = {
        'predicted_job_satisfaction': y_pred
    }
    
    return result