from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.orm import relationship

from database import Base


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, index=True)
    Company_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    job_lists = relationship("job_list", back_populates="employer")

# for jobs created by employer
class job_list(Base):
    __tablename__ = "job_lists"

    id = Column(Integer, primary_key=True, index=True)
    job_role = Column(String, index=True)
    location = Column(String, index=True)
    description = Column(String, index=True)
    experience = Column(Integer)
    salary = Column(Integer)
    job_id = Column(Integer, ForeignKey("employers.id"))

    employer = relationship("Employer", back_populates="job_lists")

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    Qualification = Column(String, index=True)
    hashed_password = Column(String)
    
    jobs_applied = relationship("applied_job", back_populates="user")


class applied_job(Base):
    __tablename__ = "applied_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_role = Column(String, index=True)
    location = Column(String, index=True)
    description = Column(String, index=True)
    experience = Column(Numeric(10,2))
    salary = Column(Numeric(10,2))
    job_id = Column(Integer, ForeignKey("candidates.id"))

    user = relationship("Candidate", back_populates="jobs_applied")