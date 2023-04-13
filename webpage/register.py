from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import cgi

def createRegister(regUser, regPass):
    Base = declarative_base()

    givenUser = regUser
    givenPass = regPass

    #Registration object. Given a 
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
    #Use SQLite Viewer extention of view accounts.db contents.
    engine = create_engine("sqlite:///accounts.db", echo=True)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    #If the variables for the passed username and passed password are not null or length == 0
    #search the database for the username. 
    #if the username is not found, register it to the sqlite database
    #if the username is taken, do not let user register
    if givenUser and givenPass:

        results = session.query(Register).filter(Register.uName == givenUser).all()

        if len(results)>0:
        
            print("USER ALREADY TAKEN")
        else:
            #create registration object from html form
            regInfo = Register(givenUser, givenPass)
            print("USER ADDED")
            #add the registration object
            session.add(regInfo)
            #Flush the object to the SQL database
            session.commit()

    elif not givenPass or not givenUser:
        print("User or password null")