from pydantic import BaseModel


class LoginRequestDTO(BaseModel):
    grant_type: str
    
    username: str
    password: str

class LoginResponseDTO(BaseModel):
    access_token: str