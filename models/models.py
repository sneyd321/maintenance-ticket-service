
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class MaintenanceTicket(Base):
    __tablename__ = 'maintenance_ticket'

    id = Column(Integer(), primary_key=True)
    houseId = Column(Integer(), nullable=False)
    urgency = relationship("Urgency", lazy="joined", uselist=False, backref="maintenance_ticket")
    description = relationship("Description", lazy="joined", uselist=False, backref="maintenance_ticket")
    sender = relationship("Sender", lazy="joined", uselist=False, backref="maintenance_ticket")
    name = Column(String(50), nullable=False)
    imageURL = Column(String(223), nullable=True)
    datePosted = Column(Date(), nullable=False)
    firebaseId = Column(String(20), nullable=False)
    
    def __init__(self, firebase, **kwargs):
        self.id = kwargs.get("id")
        self.houseId = kwargs.get("houseId")
        self.name = "MaintenanceTicket"
        self.urgency = Urgency(**kwargs.get("urgency", {}))
        self.description = Description(**kwargs.get("description", {}))
        self.sender = Sender(**kwargs.get("sender", {}))
        self.datePosted = datetime.datetime.utcnow().date()
        self.firebase = firebase
        self.firebaseId = self.firebase.get_firebase_id(senderEmail=self.sender.email)

    

    def setImageURL(self, id):
        blob = self.firebase.create_blob_no_cache(f"MaintenanceTicket/MaintenanceTicket_{id}.jpg")
        blob.upload_from_string(b"", content_type="image/jpeg")
        self.imageURL = blob.public_url

    def to_json(self):
        return {
            "houseId": self.houseId,
            "id": self.id,
            "name": self.name,
            "urgency": self.urgency.to_json(),
            "description": self.description.to_json(),
            "sender": self.sender.to_json(),
            "imageURL": self.imageURL,
            "datePosted": self.datePosted if isinstance(self.datePosted, str) else self.datePosted.strftime("%Y/%m/%d") ,
            "firebaseId": self.firebaseId
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "imageURL": self.imageURL,
            "datePosted": self.datePosted,
            "firebaseId": self.firebaseId
        }


class Sender(Base):
    __tablename__ = "maintenance_ticket_sender"
    id = Column(Integer(), primary_key=True)
    maintenance_ticket_id = Column(Integer(), ForeignKey('maintenance_ticket.id'))
    firstName = Column(String(100), nullable=False)
    lastName = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)

    def __init__(self, **kwargs):
        self.firstName = kwargs.get("firstName")
        self.lastName = kwargs.get("lastName")
        self.email = kwargs.get("email")

    def to_dict(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email
        }

    def to_json(self):
        return {
            "firstName": self.firstName,
            "lastName": self.lastName,
            "email": self.email
        }


class Description(Base):
    __tablename__ = 'description'
    id = Column(Integer(), primary_key=True)
    maintenance_ticket_id = Column(Integer, ForeignKey('maintenance_ticket.id'))
    descriptionText = Column(String(140))

    def __init__(self, **kwargs):
        self.descriptionText = kwargs.get("descriptionText", "")

    def to_json(self):
        return {
            "descriptionText": self.descriptionText
        }

  
class Urgency(Base):
    __tablename__ = 'urgency'
    id = Column(Integer(), primary_key=True)
    maintenance_ticket_id = Column(Integer, ForeignKey('maintenance_ticket.id'))
    name = Column(String(10))
    

    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")

    def to_json(self):
        return {
            "name": self.name
        }






