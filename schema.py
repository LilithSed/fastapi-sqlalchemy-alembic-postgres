from pydantic import BaseModel


class Employee(BaseModel):
    first_name: str
    last_name: str
    age: int
    position: str
    remote: bool = False  # default False

    class Config:
        orm_mode = True


