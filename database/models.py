# database/models.py - Simplified tables
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    Float,
    DateTime,
    insert,
    text,
)
import os
from datetime import datetime, timedelta
import random

# Create SQLite engine
database_path = os.path.join(os.path.dirname(__file__), 'cattle_monitoring.db')
engine = create_engine(f"sqlite:///{database_path}")
metadata_obj = MetaData()

# Define cattle_devices table (simplified)
cattle_devices = Table(
    "cattle_devices",
    metadata_obj,
    Column("device_id", String(50), primary_key=True),
    Column("cow_id", String(50)),
    Column("cow_name", String(100)),
)

# Define cattle_inference table (with accelerometer data)
cattle_inference = Table(
    "cattle_inference",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("device_id", String(50)),
    Column("timestamp", DateTime),
    Column("predicted_behavior", String(50)),
    Column("confidence", Float),
    Column("temperature", Float),
    Column("location_lat", Float),
    Column("location_lng", Float),
    Column("activity_level", Float),
    Column("AccX", Float),  # X-axis acceleration
    Column("AccY", Float),  # Y-axis acceleration  
    Column("AccZ", Float),  # Z-axis acceleration
    Column("created_at", DateTime),
)

def create_sample_data():
    """Create tables and insert sample data"""
    
    # Create all tables
    metadata_obj.create_all(engine)
    print("✅ Tables created successfully")
    
    # Sample cattle devices data (simplified)
    devices_data = [
        {
            "device_id": "cow-101",
            "cow_id": "COW001",
            "cow_name": "Bessie"
        },
        {
            "device_id": "cow-102", 
            "cow_id": "COW002",
            "cow_name": "Daisy"
        },
        {
            "device_id": "cow-103",
            "cow_id": "COW003", 
            "cow_name": "Moobert"
        },
        {
            "device_id": "cow-104",
            "cow_id": "COW004",
            "cow_name": "Luna"
        },
        {
            "device_id": "cow-105",
            "cow_id": "COW005",
            "cow_name": "Ruby"
        }
    ]
    
    # Insert cattle devices
    with engine.connect() as conn:
        conn.execute(insert(cattle_devices), devices_data)
        conn.commit()
        print(f"✅ Inserted {len(devices_data)} cattle devices")
    
    # Generate sample inference data (no heart_rate)
    behaviors = ['grazing', 'walking', 'resting', 'ruminating', 'standing']
    current_time = datetime.now()
    inference_data = []
    
    device_ids = ['cow-101', 'cow-102', 'cow-103', 'cow-104', 'cow-105']
    
    for device_id in device_ids:
        # Generate 25 readings per cow (current + 24 historical)
        for i in range(25):
            # Current reading (i=0) vs historical readings
            time_offset = timedelta(hours=i, minutes=random.randint(0, 59))
            
            # Create more realistic data patterns
            if i == 0:  # Current reading
                temp = round(random.uniform(38.2, 39.2), 1)  # Normal range
                confidence = round(random.uniform(0.85, 0.98), 3)  # High confidence
            else:  # Historical readings with some variation
                temp = round(random.uniform(37.8, 39.8), 1)  # Wider range
                confidence = round(random.uniform(0.70, 0.95), 3)  # Variable confidence
            
            inference_record = {
                "device_id": device_id,
                "timestamp": current_time - time_offset,
                "predicted_behavior": random.choice(behaviors),
                "confidence": confidence,
                "temperature": temp,
                "location_lat": round(40.712776 + random.uniform(-0.02, 0.02), 6),
                "location_lng": round(-74.005974 + random.uniform(-0.02, 0.02), 6),
                "activity_level": round(random.uniform(0.15, 0.90), 2),
                # Generate realistic accelerometer data
                "AccX": round(random.uniform(-2.0, 2.0), 3),  # X-axis acceleration (-2g to +2g)
                "AccY": round(random.uniform(-2.0, 2.0), 3),  # Y-axis acceleration  
                "AccZ": round(random.uniform(0.5, 1.5), 3),   # Z-axis (gravity component ~1g)
                "created_at": datetime.now()
            }
            inference_data.append(inference_record)
    
    # Insert inference data
    with engine.connect() as conn:
        conn.execute(insert(cattle_inference), inference_data)
        conn.commit()
        print(f"✅ Inserted {len(inference_data)} inference records")
    
    print(f"✅ Database created at: {database_path}")
    return database_path

def test_data():
    """Test the created data"""
    with engine.connect() as conn:
        # Test cattle devices
        result = conn.execute(text("SELECT * FROM cattle_devices")).fetchall()
        print(f"\n📊 Cattle Devices ({len(result)} records):")
        for row in result[:3]:  # Show first 3
            print(f"  {row.device_id}: {row.cow_name}")
        
        # Test latest inference data
        result = conn.execute(text("""
            SELECT ci.device_id, cd.cow_name, ci.predicted_behavior, 
                   ci.temperature, ci.confidence, ci.activity_level,
                   ci.AccX, ci.AccY, ci.AccZ, ci.timestamp
            FROM cattle_inference ci
            LEFT JOIN cattle_devices cd ON ci.device_id = cd.device_id
            ORDER BY ci.timestamp DESC
            LIMIT 5
        """)).fetchall()
        
        print(f"\n📈 Latest Inference Data ({len(result)} latest records):")
        for row in result:
            print(f"  {row.device_id} ({row.cow_name}): {row.predicted_behavior}, {row.temperature}°C")
            print(f"    AccX: {row.AccX:.3f}g, AccY: {row.AccY:.3f}g, AccZ: {row.AccZ:.3f}g, Activity: {row.activity_level:.1%}")

if __name__ == "__main__":
    create_sample_data()
    test_data()