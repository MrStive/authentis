
from abc import ABC, abstractmethod
import pandas as pd
from typing import Optional, Dict, Any

class DataConnector(ABC):
    """Abstract Base Class for all data connectors."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    def connect(self) -> bool:
        """Establish connection to the source."""
        pass

    @abstractmethod
    def fetch_data(self, query: Optional[str] = None) -> pd.DataFrame:
        """Fetch data from the source and return as DataFrame."""
        pass

    @abstractmethod
    def validate_schema(self, df: pd.DataFrame) -> bool:
        """Check if fetched data matches expected schema."""
        pass
