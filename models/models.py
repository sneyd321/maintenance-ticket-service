
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.exc import OperationalError, IntegrityError
import datetime
from models.Firebase import Firebase


Base = declarative_base()
firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()

class MaintenanceTicket(Base):
    __tablename__ = 'maintenance_ticket'

    id = Column(Integer(), primary_key=True)
    houseId = Column(Integer(), nullable=False)
    
    urgency = relationship("Urgency", lazy="joined", uselist=False, backref="maintenance_ticket")
    description = relationship("Description", lazy="joined", uselist=False, backref="maintenance_ticket")
    name = Column(String(50), nullable=False)
    imageURL = Column(String(223), nullable=True)
    datePosted = Column(Date(), nullable=False)
    firebaseId = Column(String(20), nullable=True)
    
    def __init__(self, houseId, **kwargs):
        self.houseId = houseId
        self.name = kwargs.get("name", "")
        self.urgency = Urgency(**kwargs.get("urgency", {}))
        self.description = Description(**kwargs.get("description", {}))
        self.datePosted = datetime.datetime.utcnow().date()
        self.firebaseId = kwargs.get("firebaseId", "")

    def setImageURL(self, id):
        blob = firebase.create_blob_no_cache(f"MaintenanceTicket/MaintenanceTicket_{id}.jpg")
        blob.upload_from_string(b"", content_type="image/jpeg")
        self.imageURL = blob.public_url

    def to_json(self):
        return {
            "houseId": self.houseId,
            "id": self.id,
            "name": self.name,
            "urgency": self.urgency.to_json(),
            "description": self.description.to_json(),
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






