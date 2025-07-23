"""
view.py - Export Cattle Inference Data to CSV

This script exports the entire cattle inference table with device information
to a CSV file in the local directory.

Usage:
    python view.py

Output:
    - cattle_inference_export.csv (complete data with cow names)
    - cattle_devices_export.csv (device information)
"""

import pandas as pd
from sqlalchemy import create_engine, text
import os
from datetime import datetime

class CattleDataExporter:
    def __init__(self):
        # SQLite database path
        self.database_path = os.path.join('database', 'cattle_monitoring.db')
        self.engine = None
        self.setup_engine()
    
    def setup_engine(self):
        """Setup SQLAlchemy engine"""
        try:
            self.engine = create_engine(f'sqlite:///{self.database_path}')
            print(f"✅ Connected to database: {self.database_path}")
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return None
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """Execute SQL query and return DataFrame"""
        try:
            if self.engine:
                with self.engine.connect() as conn:
                    result = conn.execute(text(query))
                    df = pd.DataFrame(result.fetchall(), columns=result.keys())
                    return df
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"❌ Query execution error: {e}")
            return pd.DataFrame()
    
    def export_inference_data(self, filename: str = None) -> str:
        """Export complete inference data with cow information to CSV"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cattle_inference_export_{timestamp}.csv"
        
        print("🔍 Querying inference data...")
        
        # Query to get all inference data with cow information
        query = """
        SELECT 
            ci.id,
            ci.device_id,
            cd.cow_id,
            cd.cow_name,
            ci.timestamp,
            ci.predicted_behavior,
            ci.confidence,
            ci.temperature,
            ci.location_lat,
            ci.location_lng,
            ci.activity_level,
            ci.AccX,
            ci.AccY,
            ci.AccZ,
            ci.created_at
        FROM cattle_inference ci
        LEFT JOIN cattle_devices cd ON ci.device_id = cd.device_id
        ORDER BY ci.timestamp DESC
        """
        
        df = self.execute_query(query)
        
        if df.empty:
            print("❌ No data found in inference table")
            return None
        
        # Save to CSV
        try:
            df.to_csv(filename, index=False)
            print(f"✅ Inference data exported successfully!")
            print(f"📁 File: {filename}")
            print(f"📊 Records: {len(df)}")
            print(f"📈 Columns: {len(df.columns)}")
            
            # Display summary
            self.display_summary(df)
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return None
    
    def export_devices_data(self, filename: str = None) -> str:
        """Export cattle devices data to CSV"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cattle_devices_export_{timestamp}.csv"
        
        print("🔍 Querying devices data...")
        
        query = "SELECT * FROM cattle_devices ORDER BY device_id"
        df = self.execute_query(query)
        
        if df.empty:
            print("❌ No data found in devices table")
            return None
        
        try:
            df.to_csv(filename, index=False)
            print(f"✅ Devices data exported successfully!")
            print(f"📁 File: {filename}")
            print(f"📊 Records: {len(df)}")
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return None
    
    def display_summary(self, df: pd.DataFrame):
        """Display data summary"""
        print("\n📊 DATA SUMMARY:")
        print("=" * 50)
        
        # Basic info
        print(f"Total Records: {len(df)}")
        print(f"Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        # Devices summary
        device_counts = df['device_id'].value_counts()
        print(f"\n🐄 Records per Device:")
        for device, count in device_counts.items():
            cow_name = df[df['device_id'] == device]['cow_name'].iloc[0]
            print(f"  {device} ({cow_name}): {count} records")
        
        # Behavior distribution
        behavior_counts = df['predicted_behavior'].value_counts()
        print(f"\n🎯 Behavior Distribution:")
        for behavior, count in behavior_counts.items():
            percentage = (count / len(df)) * 100
            print(f"  {behavior}: {count} ({percentage:.1f}%)")
        
        # Temperature stats
        temp_stats = df['temperature'].describe()
        print(f"\n🌡️ Temperature Statistics:")
        print(f"  Average: {temp_stats['mean']:.2f}°C")
        print(f"  Range: {temp_stats['min']:.1f}°C - {temp_stats['max']:.1f}°C")
        
        # Activity level stats
        activity_stats = df['activity_level'].describe()
        print(f"\n📈 Activity Level Statistics:")
        print(f"  Average: {activity_stats['mean']:.2f}")
        print(f"  Range: {activity_stats['min']:.2f} - {activity_stats['max']:.2f}")
        
        # Accelerometer stats
        print(f"\n📊 Accelerometer Data Ranges:")
        print(f"  AccX: {df['AccX'].min():.3f}g to {df['AccX'].max():.3f}g")
        print(f"  AccY: {df['AccY'].min():.3f}g to {df['AccY'].max():.3f}g") 
        print(f"  AccZ: {df['AccZ'].min():.3f}g to {df['AccZ'].max():.3f}g")
    
    def export_latest_data_only(self, filename: str = None) -> str:
        """Export only the latest reading for each device"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"cattle_latest_data_{timestamp}.csv"
        
        print("🔍 Querying latest data for each device...")
        
        query = """
        SELECT 
            ci.device_id,
            cd.cow_name,
            ci.timestamp,
            ci.predicted_behavior,
            ci.confidence,
            ci.temperature,
            ci.location_lat,
            ci.location_lng,
            ci.activity_level,
            ci.AccX,
            ci.AccY,
            ci.AccZ
        FROM cattle_inference ci
        LEFT JOIN cattle_devices cd ON ci.device_id = cd.device_id
        WHERE ci.timestamp = (
            SELECT MAX(timestamp) 
            FROM cattle_inference 
            WHERE device_id = ci.device_id
        )
        ORDER BY ci.device_id
        """
        
        df = self.execute_query(query)
        
        if df.empty:
            print("❌ No latest data found")
            return None
        
        try:
            df.to_csv(filename, index=False)
            print(f"✅ Latest data exported successfully!")
            print(f"📁 File: {filename}")
            print(f"📊 Records: {len(df)} (latest for each cow)")
            
            # Show latest data
            print(f"\n📋 Latest Data Preview:")
            for _, row in df.iterrows():
                print(f"  {row['device_id']} ({row['cow_name']}): {row['predicted_behavior']}, {row['temperature']}°C")
            
            return filename
            
        except Exception as e:
            print(f"❌ Error saving CSV: {e}")
            return None
    
    def get_database_info(self):
        """Display database information"""
        print("\n🗄️ DATABASE INFORMATION:")
        print("=" * 50)
        
        # Check if database exists
        if not os.path.exists(self.database_path):
            print("❌ Database file not found!")
            return
        
        # Get table info
        devices_count = self.execute_query("SELECT COUNT(*) as count FROM cattle_devices")
        inference_count = self.execute_query("SELECT COUNT(*) as count FROM cattle_inference")
        
        if not devices_count.empty and not inference_count.empty:
            print(f"📊 Cattle Devices: {devices_count['count'].iloc[0]} records")
            print(f"📈 Inference Records: {inference_count['count'].iloc[0]} records")
            print(f"💾 Database Size: {os.path.getsize(self.database_path) / 1024:.1f} KB")
        
        # Show available devices
        devices_df = self.execute_query("SELECT device_id, cow_name FROM cattle_devices ORDER BY device_id")
        if not devices_df.empty:
            print(f"\n🐄 Available Cattle:")
            for _, row in devices_df.iterrows():
                print(f"  {row['device_id']}: {row['cow_name']}")

def main():
    """Main function with menu options"""
    print("🐄 CATTLE DATA EXPORTER")
    print("=" * 50)
    
    exporter = CattleDataExporter()
    
    # Show database info
    exporter.get_database_info()
    
    print("\n📋 EXPORT OPTIONS:")
    print("1. Export ALL inference data (complete history)")
    print("2. Export LATEST data only (current status)")
    print("3. Export devices information")
    print("4. Export everything")
    
    try:
        choice = input("\nSelect option (1-4) or press Enter for option 1: ")
        
        if choice == "2":
            # Latest data only
            filename = exporter.export_latest_data_only()
            
        elif choice == "3":
            # Devices only
            filename = exporter.export_devices_data()
            
        elif choice == "4":
            # Everything
            print("\n📦 Exporting all data...")
            inference_file = exporter.export_inference_data()
            devices_file = exporter.export_devices_data()
            latest_file = exporter.export_latest_data_only()
            
            print(f"\n✅ All exports completed:")
            if inference_file:
                print(f"   📈 Complete data: {inference_file}")
            if devices_file:
                print(f"   🐄 Devices: {devices_file}")
            if latest_file:
                print(f"   📊 Latest: {latest_file}")
            
        else:
            # Default: All inference data
            filename = exporter.export_inference_data()
        
        print(f"\n🎉 Export completed successfully!")
        
    except KeyboardInterrupt:
        print(f"\n👋 Export cancelled by user")
    except Exception as e:
        print(f"\n❌ Error during export: {e}")

if __name__ == "__main__":
    main()