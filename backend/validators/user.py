from pydantic import BaseModel, field_validator, EmailStr, validate_email

login_username = ''

algerian_phone_number_regex = ""


class LoginValidator(BaseModel):
    login: str
    password: str

    @field_validator('login')
    def validate_login(cls, login):
        global login_username
        login_username = login
        valid = False
        if login.strip().__len__() > 3:
            valid = True
        elif validate_email(login):
            valid = True
        if not valid:
            raise ValueError('Invalid login')
        return login

    @field_validator('password')
    def validate_password(cls, password):
        if password.__len__() < 8 and login_username != 'admin':
            raise ValueError('Invalid password')
        return password


class RegisterValidator(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    password: str

    @field_validator('firstname')
    def validate_firstname(cls, firstname):
        if firstname.__len__() < 3:
            raise ValueError('Invalid firstname')
        return firstname

    @field_validator('lastname')
    def validate_lastname(cls, lastname):
        if lastname.__len__() < 3:
            raise ValueError('Invalid lastname')
        return lastname

    @field_validator('email')
    def validate_email(cls, email):
        if not validate_email(email):
            raise ValueError('Invalid email')
        return email

    @field_validator('password')
    def validate_password(cls, password):
        if password.__len__() < 8:
            raise ValueError('Invalid password')
        return password
