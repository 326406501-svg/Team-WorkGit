class UserRegister(BaseModel):
    username: str
    password: str

class Interest(BaseModel):
    category: str