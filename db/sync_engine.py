from sqlalchemy import create_engine
from envs import DB_URL


engine = create_engine(DB_URL, echo=True) # type: ignore