# AIS Vessel Tracking Dashboard

This project is a web-based dashboard for visualizing maritime vessel data received from AIS (Automatic Identification System) signals using the Fleetmon R400N AIS receiver.

## Project Overview

The system consists of two main components:

1. **AIS Data Collector** - A Python script that connects to the AIS receiver, decodes incoming NMEA messages, and stores vessel position data in a JSON file.

2. **Web Dashboard** - A Flask-based web application that visualizes the vessel data on an interactive map with additional analytics.

## Features

- Real-time vessel tracking on an interactive map
- Vessel information display (MMSI, position, speed, course)
- Position history visualization using Plotly
- Vessel list with quick navigation
- Basic statistical information (vessel count, average speed)

## Installation

### Prerequisites

- Python 3.7 or higher
- Serial port access (for connecting to the AIS receiver)
- Git (for cloning the repository)

### Setup Instructions

1. **Clone the repository**

```bash
git clone [repository-url]
cd ais-vessel-tracker
```

2. **Create a virtual environment (recommended)**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- On Windows:
```bash
venv\Scripts\activate
```

- On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Configure the AIS data collector**

Edit the `collect_data` function in the AIS decoder script to use the correct serial port:

```python
# Change COM3 to your AIS receiver's port
ser = serial.Serial(port='COM3', baudrate=38400, timeout=1)
```

## Running the Application

### 1. Start the AIS data collector

```bash
python ais_decoder.py
```

This will start collecting AIS data and save it to `ais_data.json`.

### 2. Start the web dashboard

```bash
python app.py
```

The dashboard will be accessible at http://localhost:5000

## Project Structure

- `ais_decoder.py` - Script for collecting and decoding AIS data
- `app.py` - Flask web application
- `templates/index.html` - Dashboard interface
- `ais_data.json` - Data storage file (created by the decoder)

## Workshop Extension Ideas

Here are some ideas for extending the dashboard during the workshop:

1. Add filtering options for vessels by type or speed
2. Implement vessel tracking history with time playback
3. Create heatmaps of vessel density
4. Add collision prediction/proximity alerting
5. Implement data analytics for traffic patterns
6. Integrate with other data sources (weather, port information)

## Troubleshooting

- **No data appearing:** Ensure the AIS receiver is properly connected and the correct COM port is specified
- **Serial port error:** Check that you have permissions to access the serial port
- **Map not loading:** Check your internet connection (required for map tiles)

## Resources

- [AIS Message Types and Formats](https://gpsd.gitlab.io/gpsd/AIVDM.html)
- [Leaflet.js Documentation](https://leafletjs.com/reference.html)
- [Plotly.js Documentation](https://plotly.com/javascript/)
- [Flask Documentation](https://flask.palletsprojects.com/)
