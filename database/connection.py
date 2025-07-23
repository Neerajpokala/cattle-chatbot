import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
import os

class DatabaseConnection:
    def __init__(self):
        # SQLite database path
        self.database_path = os.path.join(os.path.dirname(__file__), 'cattle_monitoring.db')
        self.engine = None
    
    @st.cache_resource
    def get_engine(_self):
        """Get cached SQLAlchemy engine"""
        try:
            engine = create_engine(f'sqlite:///{_self.database_path}')
            return engine
        except Exception as e:
            st.error(f"Database connection error: {e}")
            return None
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query using text() and return DataFrame"""
        try:
            engine = self.get_engine()
            if engine:
                with engine.connect() as conn:
                    result = conn.execute(text(query))
                    # Convert to DataFrame
                    df = pd.DataFrame(result.fetchall(), columns=result.keys())
                    return df
            else:
                return pd.DataFrame()
        except Exception as e:
            st.error(f"Query execution error: {e}")
            return pd.DataFrame()
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            engine = self.get_engine()
            if engine:
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT COUNT(*) as count FROM cattle_devices"))
                    count = result.fetchone()[0]
                    return count > 0
            return False
        except Exception as e:
            st.error(f"Connection test failed: {e}")
            return False
    
    def get_available_cows(self) -> pd.DataFrame:
        """Get list of available cows"""
        query = """
        SELECT device_id, cow_name
        FROM cattle_devices
        ORDER BY device_id
        """
        return self.execute_query(query)