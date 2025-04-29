import time
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# Global variable to store the decoded AIS data
ais_data = []

# MQTT Configuration
MQTT_BROKER = "192.168.31.192"
MQTT_PORT = 1883
MQTT_TOPIC = "vessel/ais"

def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    print(f"Connected to MQTT broker with result code {rc}")
    client.subscribe(MQTT_TOPIC)
    print(f"Subscribed to topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    """Callback when a message is received from MQTT"""
    global ais_data
    
    try:
        # Parse the JSON message
        decoded = json.loads(msg.payload.decode('utf-8'))
        
        # Only add messages with valid position data
        if 'latitude' in decoded and 'longitude' in decoded:
            # Keep data list at a reasonable size (max 1000 entries)
            if len(ais_data) >= 1000:
                ais_data.pop(0)  # Remove oldest entry
            
            # Add the new data
            ais_data.append(decoded)
            
            # Print basic info
            mmsi = decoded.get('mmsi', 'Unknown')
            msg_type = decoded.get('message_type', 'Unknown')
            lat = decoded.get('latitude', 0)
            lon = decoded.get('longitude', 0)
            print(f"Received: MMSI {mmsi}, Type {msg_type}, Position: {lat:.4f}, {lon:.4f}")
            
            # Save to file
            with open("ais_data.json", "w") as f:
                json.dump(ais_data, f, indent=2)
    except Exception as e:
        print(f"Error processing message: {e}")

def collect_data():
    """Main function to collect AIS data from MQTT"""
    # Initialize MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    print("AIS data collection started. Connecting to MQTT broker...")
    
    try:
        # Connect to the MQTT broker
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        
        # Start the MQTT loop
        client.loop_forever()
        
    except KeyboardInterrupt:
        print("\nData collection stopped by user")
    except Exception as e:
        print(f"Error in data collection: {e}")
    finally:
        client.disconnect()
        print("MQTT disconnected")

if __name__ == "__main__":
    print("Starting AIS data collection via MQTT...")
    collect_data()
