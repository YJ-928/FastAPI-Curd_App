# ---------------------------- Main Code Start ----------------------------
# ---------------------------- Imports ----------------------------
# SqlAlchemy
from sqlalchemy import create_engine,Column,Integer,Float,String,Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# FastAPI
from fastapi import FastAPI,status,HTTPException
# Pydantic
from pydantic import BaseModel
# Typing
from typing import Optional,List

# ---------------------------- Database Config Details ----------------------------
# Database Details
DB_NAME = "fastapidb"
USER = "postgres"
PASSWORD = "928187"
PORT = "5432"
HOST = "localhost"
# Dialect and Driver Details
DIALECT = "postgresql"
DRIVER = "psycopg2"
# Database url required by the engine
DATABASE_URL = f"{DIALECT}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

# ---------------------------- Base ----------------------------
# Delcaring Base
Base = declarative_base()

# ---------------------------- Base Class ----------------------------
# Creating SqlAlchemy Base class Students
class Students(Base):
    # Tablename
    __tablename__ = 'students'
    # Table columns
    student_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(), primary_key=False, nullable=False)
    score = Column(Float, primary_key=False, nullable=False)
    address = Column(Text(), primary_key=False, nullable=True)

# ---------------------------- Pydantic Class ----------------------------
# Pydantic class for response model
class StudentSchema(BaseModel):
    student_id: int
    name: str
    score: float
    address: Optional[str] = None

    class Config:
        from_attributes = True # To enable conversion from sqlalchemy orm to pydantic

# Pydantic class for returning data as list
class StudentListSchema(BaseModel):
    students: List[StudentSchema]

# ---------------------------- Engine, Session & Database Connection ----------------------------
# Creating Engine
Engine = create_engine(DATABASE_URL)

# Connecting to Database
Connection = Engine.connect()

# Creating SessionMaker
SessionCreator = sessionmaker(bind=Engine, autoflush=False, autocommit=False)

# ---------------------------- Database Tables Deletion & Creation ----------------------------
# Deleting any exisiting tables to avoid duplication errors
# Only for testing, not needed in final code
# Students.__table__.drop(Engine)

# Creating the defined table in connected database
Base.metadata.create_all(Engine)

# ---------------------------- FastAPI CURD Opearions ----------------------------
# FastAPI application instance
app = FastAPI()

# Root
@app.get('/', tags = ['root'])
async def root():
    return {'Welcome':'FastAPI Curd Application Starting... Ready'}

# Create
@app.post('/student/create', status_code = status.HTTP_201_CREATED, tags = ['create student'])
async def create_student(new_student:StudentSchema):
    # Check if student already exists
    session = SessionCreator()
    student_exists = session.query(Students).filter_by(student_id = new_student.student_id).first()
    if not student_exists:
        # Create student object to add data from pydantic model to base model
        student_obj = Students(
            student_id = new_student.student_id,
            name = new_student.name,
            score = new_student.score,
            address = new_student.address
        )
        session.add(student_obj) # Add to queue
        session.commit() # Ready queue to commit
        session.flush() # Wait for all commits to finish
        session.close() # Close the session
        return {'Success':'New student created successfully'}
    else:
        session.close()
        raise HTTPException(status_code = status.HTTP_226_IM_USED, detail = "Student already exists")
    
# Update
@app.put('/student/update/{id}',status_code = status.HTTP_200_OK, tags = ['update student'])
async def update_student(id:int,new_student:StudentSchema):
    # Check if given id student is present in db
    session = SessionCreator()
    student_exists = session.query(Students).filter_by(student_id = id).first()
    if student_exists:
        # Update new values
        student_exists.name = new_student.name
        student_exists.score = new_student.score
        student_exists.address = new_student.address
        session.commit()
        session.flush()
        session.close()
        return {'Success':'Student updated successfully'}
    else:
        session.close()
        # return {'Failure':'Student not found'}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Student with id {id} not found")
    
# Retrieve all
# Here we require the reponse module created from pydantic
# As we need to return all data fetched from db as list
@app.get('/student/retrieve',response_model = StudentListSchema, status_code = status.HTTP_302_FOUND, tags = ['read students'])
async def retrieve_students():
    session = SessionCreator()
    Records = session.query(Students).all() # SELECT * FROM Students;
    Student_Records = [
        StudentSchema(student_id=record.student_id,name=record.name,score=record.score,address=record.address)
        for record in Records] # List comprehension to generate a list of all student records
    session.close()
    return {'students': Student_Records}

# Retrieve one
@app.get('/student/retrieve/{id}',response_model = StudentSchema, status_code = status.HTTP_302_FOUND, tags = ['read students'])
async def retrieve_student_id(id:int):
    # Retrieve only one student data matching the given id
    session = SessionCreator()
    student_exists = session.query(Students).filter_by(student_id = id).first()
    session.close()
    if student_exists:
        return student_exists # To convert student_exists to Schema format and return
    else:
        # return {'Message':'Student not found'}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Student with id {id} not found")

# Delete all
@app.delete('/student/delete', status_code = status.HTTP_200_OK, tags = ['delete students'])
async def delete_student():
    session = SessionCreator()
    # To delete all student records we need to loop through all records and delete one at a time
    student_records = session.query(Students).all()
    if student_records:
        for record in student_records:
            session.delete(record) # Keep adding to queue
        # Commit the delete operations in queue
        session.commit()
        session.flush()
        session.close()
        return {'Success':'All students data deleted successfully'}
    else:
        session.close()
        # return {'Failure':'No records found to delete'}
        raise HTTPException(status_code = status.HTTP_204_NO_CONTENT, 
                            detail = f"No records found to delete")
    
# Delete one
@app.delete('/student/delete/{id}', status_code = status.HTTP_200_OK, tags = ['delete students'])
async def delete_student_id(id:int):
    session = SessionCreator()
    # Check if student with that id exists
    student_exists = session.query(Students).filter_by(student_id = id).first()
    if student_exists:
        session.delete(student_exists)
        session.commit()
        session.flush()
        session.close()
        return {'Success':'Student deleted successfully'}
    else:
        session.close()
        # return {'Failure':'Student not found'}
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"Student with id {id} not found")
    
# ---------------------------- Main Code End ----------------------------