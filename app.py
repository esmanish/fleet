from flask import Flask, render_template, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Path to the AIS data file
DATA_FILE = "ais_data.json"

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """API endpoint to provide AIS data to the frontend"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                
            # Filter out invalid data
            filtered_data = []
            for item in data:
                if 'latitude' in item and 'longitude' in item and 'mmsi' in item:
                    # Ensure timestamp exists
                    if 'timestamp' not in item:
                        item['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    filtered_data.append(item)
            
            return jsonify(filtered_data)
        else:
            return jsonify([])
    except Exception as e:
        print(f"Error reading AIS data: {e}")
        return jsonify({"error": str(e)})

@app.route('/api/stats')
def get_stats():
    """API endpoint to provide dashboard statistics"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
            
            # Calculate statistics
            vessel_count = len(set(item.get('mmsi') for item in data if 'mmsi' in item))
            
            # Average speed
            speeds = [item.get('speed') for item in data if 'speed' in item]
            avg_speed = sum(speeds) / len(speeds) if speeds else 0
            
            # Message type distribution
            message_types = {}
            for item in data:
                msg_type = item.get('message_description', 'Unknown')
                if msg_type in message_types:
                    message_types[msg_type] += 1
                else:
                    message_types[msg_type] = 1
            
            return jsonify({
                'vessel_count': vessel_count,
                'avg_speed': round(avg_speed, 1),
                'message_types': message_types,
                'last_update': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            return jsonify({
                'vessel_count': 0,
                'avg_speed': 0,
                'message_types': {},
                'last_update': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
    except Exception as e:
        print(f"Error calculating stats: {e}")
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)