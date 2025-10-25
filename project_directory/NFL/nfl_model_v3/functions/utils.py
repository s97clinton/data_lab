from sqlalchemy import create_engine
from functions.credentials import MYSQL_USER, MYSQL_PASSWORD

def create_nfl_engine(user = MYSQL_USER, password = MYSQL_PASSWORD, host = 'localhost', port = 3306, database = 'nfl'):
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)

    return engine
