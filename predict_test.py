import requests

url = 'http://127.0.0.1:8000/predict'

employee = {
    "employee_number": 10001,
    "employee_name": "Karen Anderson",
    "employee_age": 36,
    "maritial_status": 1,
    "current_salary": 116138,
    "number_of_children": 2,
    "years_experience": 12,
    "past_projects": 6,
    "current_projects": 1,
    "divorced_earlier": "No",
    "father_alive": "Yes",
    "mother_alive": "Yes",
    "performance_rating": 3,
    "education_level": "bachelor's",
    "department": "R&D",
    "role": "Researcher",
    "work_life_balance": 1.936454,
    "is_outlier": 0
}


response = requests.post(url, json=employee)

print(response.json())
