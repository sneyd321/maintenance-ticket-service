from typing import Set, Union, List
from pydantic import BaseModel


class DescriptionSchema(BaseModel):
    descriptionText: str

class UrgencySchema(BaseModel):
    name: str

class SenderSchema(BaseModel):
    firstName: str
    lastName: str
    email: str

class MaintenanceTicketSchema(BaseModel):
    houseId: int
    description: Union[DescriptionSchema, None]
    urgency: Union[UrgencySchema, None]
    sender: Union[SenderSchema, None]



