
from sqlalchemy.orm import Session

import models, schemas

def get_user_employer(db: Session, email: str):
    return db.query(models.Employer).filter(models.Employer.email == email).first()

def get_user_employer_by_id(db: Session, id: int):
    return db.query(models.Employer).filter(models.Employer.id == id).first()

def create_employer(db: Session, emp: schemas.EmployerCreate):
    fake_hashed_password = emp.password + "notreallyhashed"
    db_emp = models.Employer(email=emp.email, hashed_password=fake_hashed_password,Company_name = emp.Company_name)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return 
    
def get_user_Candidate(db: Session, email: str):
    return db.query(models.Candidate).filter(models.Candidate.email == email).first()

def get_user_Candidate_by_id(db: Session, id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == id).first()


def create_Candidate(db: Session, cand: schemas.CandidateCreate):
    fake_hashed_password = cand.password + "notreallyhashed"
    db_cand = models.Candidate(email=cand.email, hashed_password=fake_hashed_password,name = cand.name,Qualification = cand.Qualification)
    db.add(db_cand)
    db.commit()
    db.refresh(db_cand)
    return db_cand

def get_job_by_role(db: Session, job_role: str):
    return db.query(models.job_list).filter(models.job_list.job_role == job_role).all()


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.job_list).offset(skip).limit(limit).all()


def create_jobs_by_employer(db: Session, job: schemas.JobCreate, j_id: int):
    db_job = models.job_list(**job.dict(), job_id=j_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job