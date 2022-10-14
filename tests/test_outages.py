from models.db import DB
from models.repository import Repository
from models.models import MaintenanceTicket
from models.Firebase import Firebase

import pytest, asyncio, json

db = DB("test", "homeowner", "localhost", "roomr")
repository = Repository(db)
firebase = Firebase()
firebase.setServiceAccountPath(r"./models/static/ServiceAccount.json")
firebase.init_app()

@pytest.mark.asyncio
async def test_Maintenance_Ticket_Service_returns_an_error_when_database_fails_to_connect():
    with open("./tests/test.json", mode="r") as test:
        maintenanceTicketData = json.load(test)
        maintenanceTicket = MaintenanceTicket(firebase, **maintenanceTicketData)
    monad = await repository.insert(maintenanceTicket)
    assert monad.error_status == {"status": 502, "reason": "Failed to connect to database"}
 
