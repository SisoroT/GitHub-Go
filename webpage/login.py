from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

#Example login and password
givenUser = "fakeUser"
givenPass = "hunter2"

#Registration object. 
class Register(Base):
    __tablename__ = "Logins"

    #Username and Password columns defined. These make up the 2 columns of our SQL database
    uName = Column("Username", String, primary_key=True)
    password = Column("Password", String)

    #object constructor
    def __init__(self, uName, password):
        self.uName = uName
        self.password = password
    #return function of object as string
    def __repr__(self):
        return f"({self.uName}) ({self.password})"
    
#SQL engine that converts python code to SQL code. Creates mydb.db file. 
#Use SQLite Viewer extention to view accounts.db contents.
engine = create_engine("sqlite:///accounts.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

#If the variables for the passed username and passed password are not null or length == 0
#search the database for the username. 
#if the username is not found print username not found
#if the username is found, check if the given password matches.
if givenUser and givenPass:

    results = session.query(Register).filter(Register.uName == givenUser).all()
    
    if len(results)>0:
        print("Username Found")
        for f in results:
            if f.password == givenPass:
                print(f.uName + " logged in")
            else:
                print("INCORRECT PASSWORD")
    else:
        print("USERNAME NOT FOUND")

elif not givenPass or not givenUser:
    print("User or password null")