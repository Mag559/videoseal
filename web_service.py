from flask import Flask, request, jsonify, send_file, abort
from werkzeug.utils import secure_filename
import tempfile
import os
import io
import json
import base64

from algorithm import interface

app = Flask(__name__)


def _save_uploaded_file(file_storage):
    filename = secure_filename(file_storage.filename) or "upload"
    suffix = os.path.splitext(filename)[1] or ""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    file_storage.save(tmp.name)
    tmp.close()
    return tmp.name


@app.route("/hide", methods=["POST"])
def hide_endpoint():
    # parse key
    key = request.form.get("key")
    if key is None:
        return jsonify({"error": "'key' form field is required"}), 400
    try:
        key = int(key)
    except ValueError:
        return jsonify({"error": "'key' must be an integer"}), 400

    # parse message (support several forms)
    message = None
    if "message" in request.form:
        message = request.form["message"]
    elif "message_int" in request.form:
        try:
            message = int(request.form["message_int"])
        except ValueError:
            return jsonify({"error": "'message_int' must be an integer"}), 400
    elif "message_bits" in request.form:
        try:
            message = json.loads(request.form["message_bits"])
            if not isinstance(message, list):
                raise ValueError()
        except Exception:
            return jsonify({"error": "'message_bits' must be a JSON list of integers (0/1)"}), 400
    elif "message_file" in request.files:
        f = request.files["message_file"]
        message = f.read()
    else:
        # fallback: try to read raw body if any
        if request.data:
            try:
                decoded = request.data.decode()
                message = decoded
            except Exception:
                message = request.data

    if message is None:
        return jsonify({"error": "No message provided. Provide form field 'message' (text), 'message_int', 'message_bits' (JSON list) or upload 'message_file'"}), 400

    # parse image
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded. Use form field 'image'"}), 400
    img_file = request.files["image"]

    # save uploaded image to a temp file
    in_path = _save_uploaded_file(img_file)
    out_tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
    out_path = out_tmp.name
    out_tmp.close()

    try:
        interface.hide(message, key, in_path, out_path)
    except Exception as e:
        # cleanup temp files
        try:
            os.unlink(in_path)
        except Exception:
            pass
        try:
            os.unlink(out_path)
        except Exception:
            pass
        raise

    # send file
    return send_file(out_path, as_attachment=True, download_name="watermarked.png")


@app.route("/detect", methods=["POST"])
def detect_endpoint():
    key = request.form.get("key")
    if key is None:
        return jsonify({"error": "'key' form field is required"}), 400
    try:
        key = int(key)
    except ValueError:
        return jsonify({"error": "'key' must be an integer"}), 400

    message_type = request.form.get("message_type", "str")
    if message_type not in ("str", "bytes", "int", "bits"):
        return jsonify({"error": "message_type must be one of: str, bytes, int, bits"}), 400

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded. Use form field 'image'"}), 400
    img_file = request.files["image"]
    in_path = _save_uploaded_file(img_file)

    try:
        if message_type == "str":
            msg = interface.detect(str, key, in_path)
            result = {"type": "str", "result": msg}
        elif message_type == "bytes":
            data = interface.detect(bytes, key, in_path)
            b64 = base64.b64encode(data).decode()
            result = {"type": "bytes", "result_b64": b64}
        elif message_type == "int":
            n = interface.detect(int, key, in_path)
            result = {"type": "int", "result": n}
        else:  # bits
            bits = interface.detect(list, key, in_path)
            result = {"type": "bits", "result": bits}
    finally:
        try:
            os.unlink(in_path)
        except Exception:
            pass

    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
