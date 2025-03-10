from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# Setting up the base class for SQLAlchemy models
Base = declarative_base()

# Defining the Audition class
class Audition(Base):
    __tablename__ = 'auditions'
    
    id = Column(Integer, primary_key=True)  # Unique ID for each audition
    actor = Column(String(50), nullable=False)  # Name of the actor
    location = Column(String(50), nullable=False)  # Where the audition took place
    phone = Column(String(15), nullable=False)  # Contact number
    hired = Column(Boolean, default=False)  # Whether they got the role
    role_id = Column(Integer, ForeignKey('roles.id'))  # Link to the Role table

    role = relationship('Role', back_populates='auditions')

    def call_back(self):
        """Marks the audition as hired."""
        self.hired = True

# Defining the Role class
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)  # Unique ID for each role
    character_name = Column(String)  # Name of the character
    
    auditions = relationship('Audition', back_populates='role')

    @property
    def actors(self):
        """Returns a list of actor names for this role."""
        return [audition.actor for audition in self.auditions]

    @property
    def locations(self):
        """Returns a list of locations where auditions happened for this role."""
        return [audition.location for audition in self.auditions]

    def lead(self):
        """Finds the first hired audition or says no one was hired."""
        hired = [audition for audition in self.auditions if audition.hired]
        return hired[0] if hired else 'No actor has been hired for this role'

    def understudy(self):
        """Finds the second hired audition or says no one was hired for understudy."""
        hired = [audition for audition in self.auditions if audition.hired]
        return hired[1] if len(hired) > 1 else 'No actor has been hired for understudy for this role'


# Setting up the database
engine = create_engine('sqlite:///theater.db')  
Base.metadata.create_all(engine)  
Session = sessionmaker(bind=engine)  
session = Session()  

# Creating a role
role = Role(character_name='Hamlet')  

# Creating auditions
audition1= Audition(actor='James Carter', location='Atlanta', phone='4567891234', role=role)
audition2 = Audition(actor='Emily Zhang', location='San Francisco', phone='7891234567', role=role)
audition3 = Audition(actor='Luis Fernandez', location='Miami', phone='3216549870', role=role)

# Adding everything to the database
session.add(role)  
session.add_all([audition1, audition2, audition3])  
session.commit()  
