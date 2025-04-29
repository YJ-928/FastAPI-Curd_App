# FastAPI-Curd_App
### The FastAPI Curd APP connects with PostgreSQL and enables us to perform CURD operations on it

## FastApi Curd App:

### i. Connects FastAPI with postgres using SQLAlchemy module

### ii. Performs Curd operations based on request recieved from client or web browser

### iii. Data or Request body is also obtained from the client using API End-Points or Routes or Paths

### iv. We are also adding proper response and request codes using
###     --> from fastapi import status,HTTPException
###     -> status provides a list of all status codes
###     -> HTTPException allows us to raise an exception and provide a detailed response

## @In-code Execution/Steps:-

# Import modules
--> from fastapi import FastAPI, status, HTTPException
--> from sqlalchemy import create_engine, Column, Integer, String, Float
--> from sqlalchemy.orm import sessionmaker
--> from sqlalchemy.ext.declarative import declarative_base
--> from pydantic import BaseModel
--> from typing import Optional

DIALECT = "postgresql"
USER = "username"
PASSWORD = "password"
HOST = "host"
PORT = "port"
DATABASE_NAME = "database_name"

''' NOTE:- To get the above details from a database, 
    Run the PSQL command (PSQL: PostgreSQL Command Line Interface):-
    ---> SELECT * FROM pg_settings WHERE name = 'port';
'''

DATABASE_URL = "DIALECT://USER:PASSWORD@HOST:PORT/DATABASE_NAME"

# Create a Engine and a Sessionmaker by binding the created Engine to it:-
--> Engine = create_engine(DATABASE_URL)
--> SessionCreator = sessionmaker(bind = Engine, autoflush = False, autocommit = False)

# Create session and use it to execute queries
--> Session = SessionCreator() # To create a new session
--> Session.query() # To query the database
--> session.commit() # To save changes to database
--> Session.flush() # To wait till all commit requests have executed
--> Session.close() # To close this created session

# To create tables and actually store information we use models
# models are created using Base object created as follows:-
--> Base = declarative_base()
--> class Model_Name(Base):
    # Table
    __tablename__ = 'Table Name Here'
    # Columns
    column_1 = Column(Integer, primary_key = True) # Integer Primary Column
    column_2 = Column(String, nullable = False) # String Required Column
    column_3 = Column(String, nullable = True) # String Not Required Column
    column_4 = Column(Float, nullable = False) # Float Required Column

# To create a Resquest Body or Response Body for fastapi http operations (get,post,put,delete)
# We need to define a Schema using Pydantic Schemas called BaseModel
--> class Schema(BaseModel):
    # Columns along with datatypes
    column_1 : int # Required Column
    column_2 : str = None # Not Required Column
    column_3 : Optional[str] # Optional Column
    column_4 : float
    column_5 : bool = True # Column with default value

# We are also using tags (list element) to display the app nicely in documentation
