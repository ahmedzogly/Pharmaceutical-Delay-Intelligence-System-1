# 🚀 Simulated Real-Time Data Stream Generator
# Simulates live shipment data from operational systems

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random

class LiveDataStreamSimulator:
    """
    Simulates real-time pharmaceutical shipment data
    as if it's coming from:
    - GPS tracking systems
    - IoT temperature sensors
    - Port systems
    - Warehouse management systems
    """
    
    def __init__(self, shipment_count=100):
        self.shipment_count = shipment_count
        self.current_shipment = 0
        self.shipments = self._generate_shipments()
    
    def _generate_shipments(self):
        """Generate synthetic shipment data"""
        shipments = []
        for i in range(self.shipment_count):
            shipment = {
                "shipment_id": f"PH-2026-{str(i+1).zfill(5)}",
                "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 1440)),
                "vehicle_gps_latitude": round(np.random.uniform(30, 50), 4),
                "vehicle_gps_longitude": round(np.random.uniform(-120, -70), 4),
                "traffic_congestion_level": round(np.random.uniform(0, 10), 2),
                "route_risk_level": round(np.random.uniform(0, 10), 2),
                "handling_equipment_availability": round(np.random.uniform(0.5, 1.0), 2),
                "iot_temperature": round(np.random.normal(5, 1.5), 2),  # Ideal: 2-8°C
                "cargo_condition_status": round(np.random.uniform(0.7, 1.0), 2),
                "weather_condition_severity": round(np.random.uniform(0, 1), 2),
                "port_congestion_level": round(np.random.uniform(0, 10), 2),
                "driver_behavior_score": round(np.random.uniform(0.7, 1.0), 2),
                "fatigue_monitoring_score": round(np.random.uniform(0.7, 1.0), 2),
                "supplier_reliability_score": round(np.random.uniform(0.75, 1.0), 2),
                "loading_unloading_time": round(np.random.uniform(0.5, 5), 2),
                "customs_clearance_time": round(np.random.uniform(0.5, 5), 2),
                "lead_time_days": random.randint(1, 15),
                "fuel_consumption_rate": round(np.random.uniform(4, 8), 2),
                "eta_variation_hours": round(np.random.uniform(0, 5), 2),
                "warehouse_inventory_level": random.randint(100, 2000),
                "order_fulfillment_status": round(np.random.uniform(0.7, 1.0), 2),
                "shipping_costs": round(np.random.uniform(300, 1000), 2),
                "historical_demand": random.randint(1000, 10000),
            }
            shipments.append(shipment)
        return shipments
    
    def get_next_batch(self, batch_size=5):
        """
        Get next batch of shipments (simulates continuous stream)
        """
        if self.current_shipment >= len(self.shipments):
            self.current_shipment = 0  # Restart
        
        batch = self.shipments[self.current_shipment:self.current_shipment + batch_size]
        self.current_shipment += batch_size
        
        return pd.DataFrame(batch)
    
    def get_latest_shipment(self):
        """Get single latest shipment"""
        if self.current_shipment >= len(self.shipments):
            self.current_shipment = 0
        
        shipment = self.shipments[self.current_shipment]
        self.current_shipment += 1
        
        return pd.DataFrame([shipment])
    
    def reset(self):
        """Reset stream to beginning"""
        self.current_shipment = 0
    
    @staticmethod
    def get_sample_data(n=50):
        """Get n random sample shipments"""
        simulator = LiveDataStreamSimulator(n)
        return pd.DataFrame(simulator.shipments)


class DatabaseStreamSimulator:
    """
    Simulates reading from a real database with polling
    (In production, this would connect to actual systems)
    """
    
    def __init__(self, refresh_interval=5):
        """
        Initialize database stream
        refresh_interval: seconds between data pulls
        """
        self.refresh_interval = refresh_interval
        self.last_update = datetime.now()
        self.simulator = LiveDataStreamSimulator()
    
    def fetch_new_shipments(self):
        """
        Fetch new shipments from 'database'
        In production: connects to actual DB, API, or message queue
        """
        now = datetime.now()
        if (now - self.last_update).seconds >= self.refresh_interval:
            self.last_update = now
            return self.simulator.get_next_batch(batch_size=3)
        return None
    
    def get_active_shipments(self):
        """Get all currently active shipments"""
        return self.simulator.get_sample_data(30)
    
    def get_high_risk_shipments(self):
        """Get shipments flagged as high risk"""
        data = self.simulator.get_sample_data(50)
        # Filter to include potential high-risk cases
        data['temp_deviation'] = abs(data['iot_temperature'] - 5)
        data['risk_score'] = (
            data['temp_deviation'] * 0.3 + 
            (1 - data['cargo_condition_status']) * 0.3 +
            data['port_congestion_level'] / 10 * 0.2 +
            (1 - data['driver_behavior_score']) * 0.2
        ) * 100
        return data[data['risk_score'] > 40].head(10)


# For testing
if __name__ == "__main__":
    # Test the simulator
    simulator = LiveDataStreamSimulator(100)
    
    print("📊 Sample Batch:")
    print(simulator.get_next_batch(3))
    print("\n🔄 Latest Shipment:")
    print(simulator.get_latest_shipment())
    
    # Test database simulator
    db_simulator = DatabaseStreamSimulator()
    print("\n🏢 Active Shipments (simulated from DB):")
    print(db_simulator.get_active_shipments().head())
