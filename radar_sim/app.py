from flask import Flask, jsonify
import random

app = Flask(__name__)

# עצמים בסיסיים שהרדאר יכול לזהות
OBJECTS = [
    {"name": "F-16 Falcon", "type": "Fighter Jet"},
    {"name": "Boeing 747", "type": "Commercial Airliner"},
    {"name": "AH-64 Apache", "type": "Attack Helicopter"},
]

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/radar/status")
def radar_status():
    return jsonify({
        "radar_online": True,
        "mode": "simulation"
    })

@app.route("/radar/objects")
def radar_objects():
    objects = []
    for i, base_obj in enumerate(OBJECTS, start=1):
        objects.append({
            "id": i,
            "name": base_obj["name"],
            "type": base_obj["type"],
            "distance_km": round(random.uniform(5, 80), 1),  # מספר עשרוני פשוט
            "speed_kmh": random.randint(200, 900)          # מספר שלם
        })

    return jsonify({
        "objects_detected": len(objects),
        "objects": objects
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
