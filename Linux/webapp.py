"""Web companion for Linux + iPhone (no Mac required).

Run:  python webapp.py
Open http://<linux-ip>:5000 on the iPhone's Safari.
Set OPENAI_API_KEY to enable screen classification.
"""
import os, io, base64, time
import mss
from PIL import Image
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__, template_folder="templates")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY", "")

def capture_b64():
    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[1])
    img = Image.frombytes("RGB", shot.size, shot.bgra, "raw", "BGRX")
    # downscale for API
    img.thumbnail((1280, 1280))
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=70)
    return base64.b64encode(buf.getvalue()).decode(), img.size

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/capture")
def capture():
    b64, size = capture_b64()
    return jsonify({"image": "data:image/jpeg;base64," + b64, "size": size})

@app.route("/focus", methods=["POST"])
def focus():
    data = request.get_json(force=True) or {}
    task = data.get("task", "")
    minutes = int(data.get("minutes", 30))
    return jsonify({"status": "started", "task": task, "minutes": minutes, "started_at": time.time()})

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json(force=True) or {}
    task = data.get("task", "focus")
    if not OPENAI_KEY:
        return jsonify({"error": "OPENAI_API_KEY not set"}), 400
    b64, _ = capture_b64()
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You classify whether a screenshot shows the user on-task. Reply with only: on_task, off_task, or uncertain."},
            {"role": "user", "content": [
                {"type": "text", "text": f"Task: {task}. Is the user on task?"},
                {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64," + b64}},
            ]},
        ],
        "max_tokens": 10,
    }
    try:
        r = requests.post("https://api.openai.com/v1/chat/completions",
                          headers={"Authorization": "Bearer " + OPENAI_KEY},
                          json=payload, timeout=30)
        r.raise_for_status()
        answer = r.json()["choices"][0]["message"]["content"].strip().lower()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"activity": answer, "checked_at": time.time()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
