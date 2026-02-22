import os
import json
from datetime import datetime
from flask import Flask, request, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = "uploads"
ALLOWED_EXT = {"pdf", "docx", "pptx", "doc", "xls", "xlsx", "ppt", "png", "jpg", "jpeg"}
PORT = 5000
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
CORS(app)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 * 1024

def allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    name = request.form.get("name", "anonim")
    if not file or not allowed(file.filename):
        return jsonify({"success": False, "error": "Icazəsiz fayl formatı"}), 400
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = secure_filename(f"{ts}_{name}_{file.filename}")
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    metadata = {"filename": filename, "original_name": file.filename, "uploader": name, "timestamp": ts, "size": os.path.getsize(path), "downloaded": False}
    with open(os.path.join(UPLOAD_FOLDER, f"{filename}.meta"), "w") as f:
        json.dump(metadata, f)
    return "", 204

@app.route("/api/files", methods=["GET"])
def api_list_files():
    files = []
    for f in os.listdir(UPLOAD_FOLDER):
        if f.endswith(".meta"):
            continue
        file_path = os.path.join(UPLOAD_FOLDER, f)
        meta_path = os.path.join(UPLOAD_FOLDER, f"{f}.meta")
        metadata = {}
        if os.path.exists(meta_path):
            with open(meta_path, "r") as mf:
                metadata = json.load(mf)
        files.append({"name": f, "size": os.path.getsize(file_path), "date": datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%Y-%m-%d %H:%M:%S"), "downloaded": metadata.get("downloaded", False), "uploader": metadata.get("uploader", "unknown"), "original_name": metadata.get("original_name", f)})
    return jsonify(files)

@app.route("/api/download/<filename>", methods=["GET"])
def api_download_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"success": False, "error": "Fayl tapılmadı"}), 404
    meta_path = os.path.join(UPLOAD_FOLDER, f"{filename}.meta")
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            metadata = json.load(f)
        metadata["downloaded"] = True
        with open(meta_path, "w") as f:
            json.dump(metadata, f)
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", PORT))
    app.run(host="0.0.0.0", port=port, debug=False)
