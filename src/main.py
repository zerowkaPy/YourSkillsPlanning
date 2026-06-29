from fastapi import FastAPI

from src.config import setup_logging
from src.routers import setup_routers
from src.middlwares import setup_middlewares
from src.handlers import import_handlers


app = FastAPI()
setup_middlewares(app)
import_handlers()
setup_routers(app)
setup_logging()





