from pydantic import BaseModel


class LoginResponseDTO(BaseModel):
    access_token: str

class RegisterRequestDTO(BaseModel):
    username: str
    password: str

    # ! TODO: добавить EmailStr
