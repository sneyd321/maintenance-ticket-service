from typing import Set, Union, List
from pydantic import BaseModel



class DescriptionSchema(BaseModel):
    descriptionText: str

class UrgencySchema(BaseModel):
    name: str

class MaintenanceTicketSchema(BaseModel):
    name: str
    description: Union[DescriptionSchema, None]
    urgency: Union[UrgencySchema, None]
    firebaseId: str

class UpdateMaintenanceTicketSchema(BaseModel):
    imageURL: str
    firebaseId: str

class MaintenanceTicketResponseSchema(BaseModel):
    id: int
    houseId: int
    name: str
    imageURL: str = None
    datePosted: str
    firebaseId: str = None
    description: Union[DescriptionSchema, None]
    urgency: Union[UrgencySchema, None]