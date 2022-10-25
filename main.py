from fastapi import FastAPI, HTTPException
from models.schemas import *
from models.db import DB
from models.Firebase import Firebase
from models.models import MaintenanceTicket
from models.repository import Repository

import uvicorn, os, json, requests, asyncio

user = os.environ.get('DB_USER', "test")
password = os.environ.get('DB_PASS', "homeowner")
host = os.environ.get('DB_HOST', "localhost")
database = os.environ.get('DB_DATABASE', "roomr")

db = DB(user, password, host, database)
repository = Repository(db)

firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()

app = FastAPI()

@app.get("/Health")
async def health_check():
    return {"status": 200}

@app.post("/MaintenanceTicket")
async def create_maintenance_ticket(request: MaintenanceTicketSchema):
    maintenanceTicket = MaintenanceTicket(firebase, **request.dict())
    monad = await repository.insert(maintenanceTicket)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return maintenanceTicket.to_json()
  
@app.get("/House/{houseId}/MaintenanceTicket")
async def get_maintenance_ticket_by_house_id(houseId: int, query: Union[int, None] = None):
    if query:
        maintenanceTicket = MaintenanceTicket(firebase, houseId=houseId)
        maintenanceTicket.id = query
        monad = await repository.get(maintenanceTicket)
        if monad.has_errors():
            return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
        return monad.get_param_at(0).to_json()

    maintenanceTicket = MaintenanceTicket(firebase, houseId=houseId)
    monad = await repository.get_all(maintenanceTicket)
    if monad.has_errors():
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    return [result.to_json() for result in monad.get_param_at(0)]

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8083)