from flask import Flask
import random

app = Flask(__name__)

@app.route("/")
def home():
    return "RadarSimOps Active"

@app.route("/radar")
def radar():
    return {
        "target_distance_km": round(random.uniform(1, 30), 2),
        "signal_strength": round(random.uniform(0.5, 1.0), 2)
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
