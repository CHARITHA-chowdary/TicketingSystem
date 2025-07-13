from fastapi import FastAPI
from scripts.utils.logger import setup_logger
from scripts.Common.AppConfigurations import APP_CONFIG
from scripts.core.services.TicketManagementService import router as ticket_router
import uvicorn

logger = setup_logger()

app = FastAPI()
app.include_router(ticket_router)

if __name__ == "__main__":
    logger.info("Welcome to Support System!")
    uvicorn.run("app:app", host="0.0.0.0", port=int(APP_CONFIG.PORT), reload=True)
