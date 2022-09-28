from fastapi import FastAPI, HTTPException, BackgroundTasks
from typing import List
from models.schemas import *
from models.db import DB
from models.models import MaintenanceTicket
from models.repository import Repository
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError

import uvicorn, os, json, requests, asyncio


user = os.environ.get('DB_USER', "root")
password = os.environ.get('DB_PASS', "root")
host = os.environ.get('DB_HOST', "localhost")
database = os.environ.get('DB_DATABASE', "roomr")
namespace = os.environ.get('NAMESPACE', "test")

db = DB(user, password, host, database)
repository = Repository(db)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    try:
        await repository.create_all()
    except OperationalError:
        SystemExit()

@app.get("/Health")
async def health_check():
    return {"status": 200}

@app.post("/MaintenanceTicket/{houseId}")
async def create_maintenance_ticket(houseId: int, request: MaintenanceTicketSchema):
    maintenanceTicket = MaintenanceTicket(houseId, **request.dict())
    monad = await repository.insert(maintenanceTicket)
    if monad.error_status:
        return HTTPException(status_code=monad.error_status["status"], detail=monad.error_status["reason"])
    maintenanceTicket.setImageURL(maintenanceTicket.id)
    return maintenanceTicket.to_json()
  
@app.get("/House/{houseId}/MaintenanceTicket")
async def get_maintenance_ticket_by_house_id(houseId: int):
    maintenanceTicket = MaintenanceTicket(houseId)
    results = await repository.get_all(maintenanceTicket)
    return [result.to_json() for result in results]

@app.get("/MaintenanceTicket/{maintenanceTicketId}")
async def get_maintenance_ticket(maintenanceTicketId: int):
    maintenanceTicket = MaintenanceTicket(houseId=0)
    maintenanceTicket.id = maintenanceTicketId
    print(maintenanceTicket.to_json())
    result = await repository.get(maintenanceTicket)
    if not result:
        return HTTPException(status_code=404, detail="Not Found")
    return result.to_json()


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8083)