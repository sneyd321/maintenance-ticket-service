from models.monad import RepositoryMaybeMonad

class Repository:

    def __init__(self, db):
        self.db = db


    async def insert(self, maintenanceTicket):
        async with self.db.get_session() as session:
            monad = await RepositoryMaybeMonad(maintenanceTicket) \
                .bind_data(self.db.get)
            if monad.get_param_at(0):
                return RepositoryMaybeMonad(error_status={"status": 409, "reason": "Failed to insert data into database"})
            await RepositoryMaybeMonad(maintenanceTicket) \
                .bind(self.db.insert)
            await RepositoryMaybeMonad() \
                .bind(self.db.flush)
            maintenanceTicket.setImageURL(maintenanceTicket.id)
            await RepositoryMaybeMonad(maintenanceTicket) \
                .bind(self.db.update)
            return await RepositoryMaybeMonad() \
                .bind(self.db.commit)
        
    async def get_all(self, maintenanceTicket):
        async with self.db.get_session():
            return await RepositoryMaybeMonad(maintenanceTicket) \
                .bind_data(self.db.get_by_house_id)

    async def get(self, maintenanceTicket):
        async with self.db.get_session():
            return await RepositoryMaybeMonad(maintenanceTicket) \
                .bind_data(self.db.get)
            