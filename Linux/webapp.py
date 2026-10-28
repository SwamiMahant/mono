"""Minimal web companion for Linux + iPhone (no Mac required).

Run:  python webapp.py
Then open http://<linux-ip>:5000 on the iPhone's Safari.
"""
from flask import Flask, render_template, request, jsonify
import mss
from PIL import Image
import io, base64, time

app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/capture")
def capture():
    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[1])
    img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return jsonify({"image": "data:image/png;base64," + b64, "size": img.size})

@app.route("/focus", methods=["POST"])
def focus():
    data = request.get_json(force=True) or {}
    task = data.get("task", "")
    minutes = int(data.get("minutes", 30))
    return jsonify({"status": "started", "task": task, "minutes": minutes, "started_at": time.time()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
