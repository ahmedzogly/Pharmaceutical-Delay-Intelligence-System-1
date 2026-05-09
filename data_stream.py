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
        data = self.simulator.get_sample_data(30)
        return self._apply_feature_engineering(data)
    
    def _apply_feature_engineering(self, df):
        """Apply feature engineering to raw shipment data"""
        df = df.copy()
        df["route_efficiency_score"] = ((10 - df["traffic_congestion_level"]) * 0.3 +
            (10 - df["route_risk_level"]) * 0.4 + df["handling_equipment_availability"] * 0.3).clip(0, 10)
        df["supply_chain_health"] = (df["supplier_reliability_score"] * 0.4 +
            df["order_fulfillment_status"] * 0.3 + (1 - df["port_congestion_level"]/10) * 0.3).clip(0, 1)
        df["temp_deviation_from_ideal"] = abs(df["iot_temperature"] - 5)
        df["cargo_risk_indicator"] = (df["temp_deviation_from_ideal"] * 0.5 +
            (1 - df["cargo_condition_status"]) * 0.3 + df["weather_condition_severity"] * 0.2)
        df["driver_performance"] = (df["driver_behavior_score"] * 0.6 +
            df["fatigue_monitoring_score"] * 0.4).clip(0, 1)
        df["operational_bottleneck"] = (df["loading_unloading_time"] * 0.4 +
            df["customs_clearance_time"] * 0.4 + df["lead_time_days"] * 0.2)
        df["weather_traffic_impact"] = df["weather_condition_severity"] * df["traffic_congestion_level"]
        return df
    
    def get_high_risk_shipments(self):
        """Get shipments flagged as high risk"""
        data = self.simulator.get_sample_data(50)
        data = self._apply_feature_engineering(data)
        
        # Calculate risk scores using same logic as PharmaRiskScorer
        weights = {
            "cargo_risk_indicator": 0.25, "route_efficiency_score": 0.15,
            "supply_chain_health": 0.15, "driver_performance": 0.10,
            "operational_bottleneck": 0.15, "weather_traffic_impact": 0.10,
            "port_congestion_level": 0.10
        }
        
        def calculate_risk_score(row):
            score = 0
            score += row["cargo_risk_indicator"] * weights["cargo_risk_indicator"] * 10
            score += (10 - row["route_efficiency_score"]) * weights["route_efficiency_score"]
            score += (1 - row["supply_chain_health"]) * weights["supply_chain_health"] * 10
            score += (1 - row["driver_performance"]) * weights["driver_performance"] * 10
            score += min(row["operational_bottleneck"] / 5, 1) * weights["operational_bottleneck"] * 10
            score += min(row["weather_traffic_impact"] / 10, 1) * weights["weather_traffic_impact"] * 10
            score += (row["port_congestion_level"] / 10) * weights["port_congestion_level"] * 10
            return min(max(score * 10, 0), 100)
        
        data['risk_score'] = data.apply(calculate_risk_score, axis=1)
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
