
from .base import DataConnector
import pandas as pd
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest, DateRange, Metric, Dimension
import os

class GA4Connector(DataConnector):
    def connect(self) -> bool:
        # In a real scenario, we'd handle OAuth or Service Account file path here.
        # For now, we assume GOOGLE_APPLICATION_CREDENTIALS is set or passed in config.
        try:
            # This is just a lazy check. Real connection happens on request.
            return True
        except Exception as e:
            print(f"GA4 Connection Error: {e}")
            return False

    def fetch_data(self, query: str = None) -> pd.DataFrame:
        """
        Fetches basic user acquisition data.
        Config should contain 'property_id'.
        """
        property_id = self.config.get('property_id')
        if not property_id:
            raise ValueError("property_id missing in config")

        client = BetaAnalyticsDataClient()
        
        request = RunReportRequest(
            property=f"properties/{property_id}",
            dimensions=[Dimension(name="city"), Dimension(name="firstUserSource")],
            metrics=[Metric(name="activeUsers"), Metric(name="conversions")],
            date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        )
        
        try:
            response = client.run_report(request)
            
            data = []
            for row in response.rows:
                data.append({
                    "City": row.dimension_values[0].value,
                    "Source": row.dimension_values[1].value,
                    "ActiveUsers": int(row.metric_values[0].value),
                    "Conversions": int(row.metric_values[1].value)
                })
                
            return pd.DataFrame(data)
        except Exception as e:
            print(f"GA4 Fetch Error: {e}")
            return pd.DataFrame()

    def validate_schema(self, df: pd.DataFrame) -> bool:
        return 'ActiveUsers' in df.columns
