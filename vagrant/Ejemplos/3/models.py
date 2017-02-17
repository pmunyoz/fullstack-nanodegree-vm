from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine





Base = declarative_base()
class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    description = Column(String(250))

    @property
    def serialize(self):
       return {
       		'id': self.id,
           'name': self.name,
           'description' : self.description
       }
 

engine = create_engine('sqlite:///puppies.db')


Base.metadata.create_all(engine)