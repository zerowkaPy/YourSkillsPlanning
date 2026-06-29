from enum import Enum

from sqlalchemy.exc import IntegrityError, DataError, SQLAlchemyError

class AlchemyExcs(Enum):
    GlobalErr = SQLAlchemyError
    IntegrityErr = IntegrityError
    DataErr = DataError

    
