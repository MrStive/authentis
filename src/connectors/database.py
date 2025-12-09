
from .base import DataConnector
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

class SQLConnector(DataConnector):
    def connect(self) -> bool:
        try:
            # Config expects 'connection_string'
            conn_str = self.config.get('connection_string')
            self.engine = create_engine(conn_str)
            with self.engine.connect() as conn:
                pass
            return True
        except SQLAlchemyError as e:
            print(f"SQL Connection Error: {e}")
            return False

    def fetch_data(self, query: str = None) -> pd.DataFrame:
        if not query:
            raise ValueError("Query string required for SQL connector")
        
        try:
            return pd.read_sql(query, self.engine)
        except Exception as e:
            print(f"SQL Fetch Error: {e}")
            return pd.DataFrame()

    def validate_schema(self, df: pd.DataFrame) -> bool:
        # Generic validator
        return not df.empty
