import os
import json
from glob import glob
from flask import Flask, render_template, send_from_directory, request, jsonify

app = Flask(__name__)

# Set your exact target directory here
CROPS_BASE_DIR = "/hpc/groups/pollinator-monitoring/runs/detect/run_2026-08-17_17-37-03/crops_2026-08-17_17-37-03"
PINNED_FILE = "pinned.json"

def load_pinned():
    if os.path.exists(PINNED_FILE):
        with open(PINNED_FILE, "r") as f:
            return json.load(f)
    return []

def save_pinned(pinned_list):
    with open(PINNED_FILE, "w") as f:
        json.dump(pinned_list, f)

@app.route("/")
def index():
    image_extensions = ("*.jpg", "*.jpeg", "*.png")
    all_files = []
    
    # Grab images recursively inside your specific crops folder
    for ext in image_extensions:
        all_files.extend(glob(os.path.join(CROPS_BASE_DIR, "**", ext), recursive=True))
    
    # Sort by modification time (newest first)
    all_files.sort(key=os.path.getmtime, reverse=True)
    
    # Convert absolute paths to relative web paths
    relative_files = [os.path.relpath(f, CROPS_BASE_DIR) for f in all_files]
    pinned = load_pinned()
    
    # Filter out pinned items from recent stream
    recent = [f for f in relative_files if f not in pinned][:100]
    
    return render_template("index.html", recent=recent, pinned=pinned, folder=os.path.basename(CROPS_BASE_DIR))

# CRITICAL FIX: Restored <path:filename> parameter
@app.route("/media/<path:filename>")
def serve_image(filename):
    return send_from_directory(CROPS_BASE_DIR, filename)

@app.route("/api/pin", methods=["POST"])
def toggle_pin():
    data = request.json
    rel_path = data.get("filepath")
    pinned = load_pinned()
    
    if rel_path in pinned:
        pinned.remove(rel_path)
    else:
        pinned.append(rel_path)
        
    save_pinned(pinned)
    return jsonify({"success": True, "pinned": pinned})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=32967, debug=False)
