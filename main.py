import logging
import os

import easyocr
# import PIL
# import numpy
import uvicorn

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db

from models import Employee as ModelEmployee
from schema import Employee as SchemaEmployee


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()
# ocr = easyocr.Reader(["en"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ocr")

app.add_middleware(DBSessionMiddleware, db_url=os.environ["DATABASE_URL"])


@app.post("/employee/", response_model=SchemaEmployee)
async def create(req_body: SchemaEmployee):
    db_user = ModelEmployee(
        first_name=req_body.first_name, last_name=req_body.last_name, 
        age=req_body.age, position=req_body.position, remote=req_body.remote
    )
    db.session.add(db_user)
    db.session.commit()
    return db_user


@app.get("/employee/")
async def get_all():
    # Retreive all employees from the db.
    employees = db.session.query(ModelEmployee)
    result = employees.all()

    data = {}
    res_data = []
    for employee in result:
        data = {
            "id": employee.id,
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "age": employee.age,
            "position": employee.position,
            "remote": employee.remote
        }
        res_data.append(data)

    return res_data


@app.get("/employee/{employee_id}", response_model=SchemaEmployee)
async def get_one(employee_id: int):
    if employee_id is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    # Retreive only one employee with the given id.
    employees = db.session.query(ModelEmployee)
    result = employees.filter(ModelEmployee.id==employee_id).one()

    res_data = {
        "first_name": result.first_name,
        "last_name": result.last_name,
        "age": result.age,
        "position": result.position,
        "remote": result.remote
    }
    return res_data


# @app.post("/upload-image-employee-id")
# async def do_ocr(request: Request, file: UploadFile = File(...)):
#     if file is None:
#         raise HTTPException(status_code=500, detail="missing file")
    
#     img_file = numpy.array(PIL.Image.open(file.file).convert("RGB"))
#     res = ocr.readtext(img_file)

#     # return array of strings
#     return [item[1] for item in res]


# @app.post("/employee-image")
# async def post_employee_image(req_body: Request, file: UploadFile = File(...)):
#     if file is None:
#         raise HTTPException(status_code=500, detail="missing file")
    
#     return "AAA"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
