from pydantic import BaseModel, EmailStr


class LoginResponseDTO(BaseModel):
    access_token: str

class RegisterRequestDTO(BaseModel):
    username: str
    password: str

    email: EmailStr