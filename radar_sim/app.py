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

# ---------- דשבורד פשוט ב-HTML ----------

@app.route("/dashboard")
def dashboard():
    # מחזיר HTML פשוט עם JS שמדבר עם ה-API
    return """
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <title>RadarSimOps Dashboard</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { margin-bottom: 5px; }
            .status { margin-bottom: 15px; }
            table { border-collapse: collapse; width: 100%; max-width: 700px; }
            th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
            th { background: #f0f0f0; }
            .online { color: green; font-weight: bold; }
            .offline { color: red; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>RadarSimOps Dashboard</h1>
        <div class="status">
            <div>Radar status: <span id="radarStatus">Loading...</span></div>
            <div>Mode: <span id="radarMode">Loading...</span></div>
        </div>

        <h2>Detected Objects</h2>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Distance (km)</th>
                    <th>Speed (km/h)</th>
                </tr>
            </thead>
            <tbody id="objectsTableBody">
            </tbody>
        </table>

        <script>
            async function loadStatus() {
                try {
                    const res = await fetch('/radar/status');
                    const data = await res.json();
                    const statusEl = document.getElementById('radarStatus');
                    const modeEl = document.getElementById('radarMode');

                    if (data.radar_online) {
                        statusEl.textContent = 'ONLINE';
                        statusEl.className = 'online';
                    } else {
                        statusEl.textContent = 'OFFLINE';
                        statusEl.className = 'offline';
                    }

                    modeEl.textContent = data.mode || 'unknown';
                } catch (e) {
                    console.error(e);
                }
            }

            async function loadObjects() {
                try {
                    const res = await fetch('/radar/objects');
                    const data = await res.json();
                    const tbody = document.getElementById('objectsTableBody');
                    tbody.innerHTML = '';

                    (data.objects || []).forEach(obj => {
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td>${obj.id}</td>
                            <td>${obj.name}</td>
                            <td>${obj.type}</td>
                            <td>${obj.distance_km}</td>
                            <td>${obj.speed_kmh}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                } catch (e) {
                    console.error(e);
                }
            }

            async function refreshAll() {
                await loadStatus();
                await loadObjects();
            }

            // טעינה ראשונית
            refreshAll();
            // ריענון כל 5 שניות
            setInterval(refreshAll, 5000);
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
