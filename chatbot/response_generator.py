import pandas as pd
import streamlit as st
from typing import Dict

class SimpleResponseGenerator:
    def __init__(self):
        self.templates = {
            'temperature': "🌡️ **{cow_name}** currently has a temperature of **{temperature}°C**",
            'behavior': "🐄 **{cow_name}** is currently **{behavior}** (confidence: {confidence:.1%})",
            'location': "📍 **{cow_name}** is at coordinates **({lat:.4f}, {lng:.4f})**",
            'accelerometer': "📊 **{cow_name}** accelerometer: X={AccX:.3f}g, Y={AccY:.3f}g, Z={AccZ:.3f}g",
            'health': self._generate_health_response,
            'general': "📊 **{cow_name}**: {behavior}, {temperature}°C, Activity: {activity_level:.1%}",
            'no_data': "❌ Sorry, I couldn't find data for that cow. Available cows: {available_cows}",
            'error': "🔧 Something went wrong. Please try again."
        }
    
    def _generate_health_response(self, data: Dict) -> str:
        """Generate health status response"""
        temp = data.get('temperature', 0)
        cow_name = data.get('cow_name', 'Cow')
        
        health_issues = []
        
        # Temperature check
        if temp > 39.5:
            health_issues.append(f"high temperature ({temp}°C)")
        elif temp < 38.0 and temp > 0:
            health_issues.append(f"low temperature ({temp}°C)")
        
        if health_issues:
            return f"⚠️ **{cow_name}** health alert: {', '.join(health_issues)}"
        else:
            return f"✅ **{cow_name}** appears healthy (temp: {temp}°C)"
    
    def get_available_cows(self, db_connection) -> list:
        """Get list of available cow IDs"""
        try:
            query = "SELECT DISTINCT device_id FROM cattle_inference ORDER BY device_id"
            result = db_connection.execute_query(query)
            return result['device_id'].tolist() if not result.empty else []
        except:
            return []
    
    def generate_response(self, processed_query: Dict, results: pd.DataFrame, db_connection=None) -> str:
        """Generate response based on query and results"""
        if results.empty:
            available_cows = self.get_available_cows(db_connection) if db_connection else []
            return self.templates['no_data'].format(
                available_cows=', '.join(available_cows) if available_cows else 'None found'
            )
        
        try:
            data = results.iloc[0].to_dict()
            metric = processed_query['metric']
            
            # Display data in sidebar for debugging
            with st.sidebar:
                st.subheader("📊 Retrieved Data")
                st.json(data)
            
            if metric == 'temperature':
                return self.templates['temperature'].format(
                    cow_name=data.get('cow_name', 'Unknown'),
                    temperature=data.get('temperature', 'N/A')
                )
            elif metric == 'behavior':
                return self.templates['behavior'].format(
                    cow_name=data.get('cow_name', 'Unknown'),
                    behavior=data.get('predicted_behavior', 'unknown'),
                    confidence=data.get('confidence', 0)
                )
            elif metric == 'location':
                return self.templates['location'].format(
                    cow_name=data.get('cow_name', 'Unknown'),
                    lat=data.get('location_lat', 0),
                    lng=data.get('location_lng', 0)
                )
            elif metric == 'accelerometer':
                return self.templates['accelerometer'].format(
                    cow_name=data.get('cow_name', 'Unknown'),
                    AccX=data.get('AccX', 0),
                    AccY=data.get('AccY', 0),
                    AccZ=data.get('AccZ', 0)
                )
            elif metric == 'health':
                return self._generate_health_response(data)
            else:
                return self.templates['general'].format(
                    cow_name=data.get('cow_name', 'Unknown'),
                    behavior=data.get('predicted_behavior', 'N/A'),
                    temperature=data.get('temperature', 'N/A'),
                    activity_level=data.get('activity_level', 0)
                )
        
        except Exception as e:
            return self.templates['error']