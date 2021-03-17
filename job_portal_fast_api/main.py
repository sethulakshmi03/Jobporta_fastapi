
from typing import List

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.get("/home/")
def home(request:Request):
    return templates.TemplateResponse("test.html",{"request":request})


# Dependency
def get_db(request: Request):
    return request.state.db

## for Employer
@app.post("/employer/", response_model=schemas.Employer)
def create_employer(emp: schemas.EmployerCreate, db: Session = Depends(get_db)):
    db_emp = crud.get_user_employer(db, email=emp.email)
    if db_emp:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_employer(db=db, emp=emp)


@app.get("/employer/{emp_id}", response_model=schemas.Employer)
def read_employer(emp_id: int, db: Session = Depends(get_db)):
    db_emp = crud.get_user_employer_by_id(db, id=emp_id)
    if db_emp is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_emp

## for candidates
@app.post("/candidate/", response_model=schemas.Candidate)
def create_candidate(cand: schemas.CandidateCreate, db: Session = Depends(get_db)):
    db_cand = crud.get_user_Candidate(db, email=cand.email)
    if db_cand:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_Candidate(db=db, cand=cand)


@app.get("/candidate/{cand_id}", response_model=schemas.Candidate)
def read_candidate(cand_id: int, db: Session = Depends(get_db)):
    db_cand = crud.get_user_Candidate_by_id(db, id=cand_id)
    if db_cand is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_cand

## For Jobs
@app.post("/employer/{id}/jobs/", response_model=schemas.Job)
def create_job_for_employer(
    j_id: int, job: schemas.JobCreate, db: Session = Depends(get_db)
):
    return crud.create_jobs_by_employer(db=db, job=job, j_id=j_id)

#read jobs based on designation
@app.get("/jobs/{job_role}", response_model=List[schemas.Job])
def read_jobs_by_role(job_role: str, db: Session = Depends(get_db)):
    db_job = crud.get_job_by_role(db, job_role=job_role)
    if db_job is None:
        raise HTTPException(status_code=404, detail="search not found")
    return db_job

@app.get("/jobs/", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs

#delete job
"""
def crud_delete_job(db: Session, job_id: int) -> bool:
    # records = db.query(models.Category).all()

    stm = models.job_list.delete().where(models.job_list.job_id == job_id)
    results = db.execute(stm)
    db.commit()
    return True


@app.delete("/category/{job_id}", tags=["category"])
def read_item(job_id: int, db: Session = Depends(get_db)):
    deleted = crud_delete_job(db, job_id)
    return {"job_deleted": deleted}"""