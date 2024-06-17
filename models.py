from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    position = Column(String, nullable=False)
    remote = Column(Boolean, default=False)

    def __init__(self, first_name, last_name, age, position, remote):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.position = position
        self.remote = remote
