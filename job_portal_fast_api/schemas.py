
from typing import List, Optional

from pydantic import BaseModel


class JobBase(BaseModel):
    job_role : str
    location : str
    description : str
    experience : int
    salary : int
    


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    job_id : int

    class Config:
        orm_mode = True


class EmployerBase(BaseModel):
    email: str
    Company_name : str


class EmployerCreate(EmployerBase):
    password: str


class Employer(EmployerBase):
    id: int
    jobs_created : List[Job] = []

    class Config:
        orm_mode = True

class CandidateBase(BaseModel):
    email: str
    name : str
    Qualification : str


class CandidateCreate(CandidateBase):
    password: str


class Candidate(CandidateBase):
    id: int
    appliedjobs: List[Job] = []

    class Config:
        orm_mode = True