from sqlalchemy.ext.asyncio import create_async_engine

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, update, delete
from sqlalchemy.future import select
from models.models import MaintenanceTicket, Urgency, Description
from sqlalchemy.orm import joinedload

class DB:

    def __init__(self, user, password, host, database):
        self.engine = create_async_engine(f"mysql+aiomysql://{user}:{password}@{host}/{database}", echo=True, pool_pre_ping=True)
        Session = sessionmaker(bind=self.engine, expire_on_commit=False, class_=AsyncSession)
        self.session = Session()
        

    def get_session(self):
        return self.session
        
    async def get(self, data):
        result = await self.session.execute(select(MaintenanceTicket).where(MaintenanceTicket.id == data.id))
        return result.scalars().first()


    async def get_by_house_id(self, data):
        result = await self.session.execute(select(MaintenanceTicket).options(joinedload(MaintenanceTicket.urgency)).options(joinedload(MaintenanceTicket.description)).where(MaintenanceTicket.houseId == data.houseId))
        return result.scalars().all()



    async def insert(self, data):
        self.session.add(data)
            
    async def commit(self):
        await self.session.commit()
    
    async def rollback(self):
        await self.session.rollback()
    
    async def update(self, data):
        await self.session.execute(update(MaintenanceTicket).where(MaintenanceTicket.id == data.id).values(data.to_dict()))
       
    