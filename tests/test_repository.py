from models.db import DB
from models.repository import Repository
from models.models import MaintenanceTicket
from models.Firebase import Firebase

import pytest, asyncio, json


firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()

@pytest.mark.asyncio
async def test_Maintenance_Ticket_Service_returns_an_error_on_integrity_error():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    with open("./tests/test.json", mode="r") as test:
        maintenanceTicketData = json.load(test)
        maintenanceTicket = MaintenanceTicket(firebase, **maintenanceTicketData)
        maintenanceTicket.id = 1
    monad = await repository.insert(maintenanceTicket)
    monad = await repository.insert(maintenanceTicket)
    assert monad.error_status == {"status": 409, "reason": "Failed to insert data into database"}


@pytest.mark.asyncio
async def test_Maintenance_Ticket_Service_returns_empty_list_when_when_querying_multiple_entries():
    db = DB("test", "homeowner", "localhost", "roomr")
    repository = Repository(db)
    maintenanceTicket = MaintenanceTicket(firebase, houseId=-1)
    monad = await repository.get_all(maintenanceTicket)
    assert monad.get_param_at(0) == []