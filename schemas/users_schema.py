# from pydantic import BaseModel, EmailStr, HttpUrl, Field
# from typing import Optional, List
#
#
# class Address(BaseModel):
#     address: str
#     city: str
#     coordinates: dict
#     postalCode: str
#     state: str
#
#
# class Bank(BaseModel):
#     cardExpire: str
#     cardNumber: str
#     cardType: str
#     currency: str
#     iban: str
#
#
# class Company(BaseModel):
#     address: Address
#     department: str
#     name: str
#     title: str
#
#
# class Hair(BaseModel):
#     color: str
#     type: str
#
#
# class User(BaseModel):
#     id: int
#     firstName: str
#     lastName: str
#     maidenName: Optional[str] = None
#     age: int = Field(..., ge=0)
#     gender: str
#     email: EmailStr
#     phone: str
#     username: str
#     password: str
#     birthDate: str
#     image: HttpUrl
#     bloodGroup: str
#     height: float
#     weight: float
#     eyeColor: str
#     hair: Hair
#     domain: Optional[str] = None
#     ip: str
#     address: Address
#     macAddress: str
#     university: str
#     bank: Bank
#     company: Company
#     ein: str
#     ssn: str
#     userAgent: str
#     friends: Optional[List[dict]] = []  # Можно создать отдельную модель для друзей
#
#
# class UsersResponse(BaseModel):
#     users: List[User]
#     total: int
#     skip: int
#     limit: int

from pydantic import BaseModel, EmailStr, HttpUrl, Field, model_validator
from typing import Optional, List


# 🔧 Рекурсивный хелпер: заменяет "" на None
def replace_empty_strings(obj):
    if isinstance(obj, str) and obj.strip() == "":
        return None
    elif isinstance(obj, dict):
        return {k: replace_empty_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_empty_strings(v) for v in obj]
    else:
        return obj


class Coordinates(BaseModel):
    lat: Optional[float] = None
    lng: Optional[float] = None


class Address(BaseModel):
    address: Optional[str] = None
    city: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    postalCode: Optional[str] = None
    state: Optional[str] = None


class Bank(BaseModel):
    cardExpire: Optional[str] = None
    cardNumber: Optional[str] = None
    cardType: Optional[str] = None
    currency: Optional[str] = None
    iban: Optional[str] = None


class Company(BaseModel):
    address: Optional[Address] = None
    department: Optional[str] = None
    name: Optional[str] = None
    title: Optional[str] = None


class Hair(BaseModel):
    color: Optional[str] = None
    type: Optional[str] = None


class User(BaseModel):
    id: int
    firstName: str
    lastName: str
    maidenName: Optional[str] = None
    age: int = Field(..., ge=0)
    gender: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    birthDate: Optional[str] = None
    image: Optional[HttpUrl] = None
    bloodGroup: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    eyeColor: Optional[str] = None
    hair: Optional[Hair] = None
    domain: Optional[str] = None
    ip: Optional[str] = None
    address: Optional[Address] = None
    macAddress: Optional[str] = None
    university: Optional[str] = None
    bank: Optional[Bank] = None
    company: Optional[Company] = None
    ein: Optional[str] = None
    ssn: Optional[str] = None
    userAgent: Optional[str] = None
    friends: Optional[List[dict]] = []

    @model_validator(mode='before')
    @classmethod
    def converter_empty_strings(cls, values):
        return replace_empty_strings(values)


class UsersResponse(BaseModel):
    users: List[User]
    total: int
    skip: int
    limit: int
