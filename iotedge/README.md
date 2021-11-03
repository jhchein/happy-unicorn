# Useful

az iot hub invoke-module-method --method-name "RestartModule" -n aiot-ml -d edge-anomaly-detection -m '$edgeAgent' --method-payload "{'schemaVersion': '1.0', 'id': 'SimulatedTemperatureSensor'}"
