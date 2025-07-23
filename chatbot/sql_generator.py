from typing import Dict

class SimpleSQLGenerator:
    def __init__(self):
        self.base_query = """
        SELECT ci.device_id, cd.cow_name, ci.timestamp,
               ci.predicted_behavior, ci.confidence, ci.temperature,
               ci.location_lat, ci.location_lng, ci.activity_level,
               ci.AccX, ci.AccY, ci.AccZ
        FROM cattle_inference ci
        LEFT JOIN cattle_devices cd ON ci.device_id = cd.device_id
        """
    
    def generate_query(self, processed_query: Dict) -> str:
        """Generate SQL query based on processed input"""
        where_conditions = []
        
        # Add cow ID filter
        if processed_query['cow_id']:
            where_conditions.append(f"ci.device_id = '{processed_query['cow_id']}'")
        
        # Add time filter
        if processed_query['time_context'] == 'current':
            where_conditions.append("""
                ci.timestamp = (
                    SELECT MAX(timestamp) 
                    FROM cattle_inference 
                    WHERE device_id = ci.device_id
                )
            """)
        elif processed_query['time_context'] == 'today':
            where_conditions.append("DATE(ci.timestamp) = DATE('now')")
        elif processed_query['time_context'] == 'yesterday':
            where_conditions.append("DATE(ci.timestamp) = DATE('now', '-1 day')")
        elif processed_query['time_context'] == 'last_hour':
            where_conditions.append("ci.timestamp >= datetime('now', '-1 hour')")
        elif processed_query['time_context'] == 'last_week':
            where_conditions.append("ci.timestamp >= datetime('now', '-7 days')")
        
        # Build complete query
        where_clause = " AND ".join(where_conditions)
        if where_clause:
            query = f"{self.base_query} WHERE {where_clause}"
        else:
            query = self.base_query
        
        query += " ORDER BY ci.timestamp DESC LIMIT 10"
        return query