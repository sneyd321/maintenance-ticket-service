from models.monad import RepositoryMaybeMonad

class Repository:

    def __init__(self, db):
        self.db = db


    async def insert(self, maintenanceTicket):
        async with self.db.get_session() as session:
           
            monad = await RepositoryMaybeMonad(maintenanceTicket) \
                .bind(self.db.insert)
            maintenanceTicketFromDB = monad.get_param_at(0)
            maintenanceTicketFromDB.setImageURL(maintenanceTicketFromDB.id)
            monad = await RepositoryMaybeMonad(maintenanceTicketFromDB) \
                .bind(self.db.update)
            if monad.has_errors():
                return monad
            return await RepositoryMaybeMonad() \
                .bind(self.db.commit)
            
  
           



    async def get(self, maintenanceTicket):
        async with self.db.get_session():
            monad = await RepositoryMaybeMonad(maintenanceTicket) \
                .bind_data(self.db.get)
            return await monad.bind(self.db.commit)
         
    async def get_all(self, maintenanceTicket):
        async with self.db.get_session():
            return await RepositoryMaybeMonad(maintenanceTicket) \
                .bind_data(self.db.get_by_house_id)
            