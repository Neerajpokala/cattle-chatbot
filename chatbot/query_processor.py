import re
import streamlit as st
from typing import Dict

class SimpleQueryProcessor:
    def __init__(self):
        self.cow_pattern = r'cow[_-]?(\d+)'
        self.metric_keywords = {
            'temperature': ['temperature', 'temp', 'fever', 'hot', 'cold'],
            'behavior': ['behavior', 'behaviour', 'activity', 'doing', 'grazing', 'walking', 'resting'],
            'location': ['location', 'where', 'position', 'place'],
            'accelerometer': ['accelerometer', 'accx', 'accy', 'accz', 'acceleration', 'movement'],
            'health': ['health', 'healthy', 'sick', 'wellness', 'fine', 'okay']
        }
        self.time_keywords = {
            'current': ['current', 'now', 'present', 'latest', 'today'],
            'yesterday': ['yesterday'],
            'last_hour': ['last hour', 'past hour'],
            'last_week': ['last week', 'past week']
        }
    
    def extract_cow_id(self, query: str) -> str:
        """Extract cow ID from query"""
        match = re.search(self.cow_pattern, query.lower())
        return f"cow-{match.group(1)}" if match else None
    
    def extract_metric(self, query: str) -> str:
        """Extract what metric user is asking about"""
        query_lower = query.lower()
        for metric, keywords in self.metric_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return metric
        return 'general'
    
    def extract_time_context(self, query: str) -> str:
        """Extract time context from query"""
        query_lower = query.lower()
        for time_type, keywords in self.time_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return time_type
        return 'current'
    
    def process_query(self, query: str) -> Dict:
        """Process user query and extract information"""
        processed = {
            'cow_id': self.extract_cow_id(query),
            'metric': self.extract_metric(query),
            'time_context': self.extract_time_context(query),
            'original_query': query
        }
        
        # Debug info in sidebar
        with st.sidebar:
            st.subheader("🔍 Query Analysis")
            st.json(processed)
        
        return processed