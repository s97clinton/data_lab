from sqlalchemy import create_engine

def create_engine(user: str, password: str, database: str, host: str = 'localhost', port: int = 3306):
    connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)

    return engine
