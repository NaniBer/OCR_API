from flask import Flask, request, jsonify
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)



@app.route('/')
def home():
    return jsonify({"message": "🧾 OCR API is live on Render!"})


@app.route('/extract-text', methods=['POST'])
def extract_text():
    image_bytes = request.data
    if not image_bytes:
        return jsonify({"error": "No image uploaded"}), 400

    try:
        # Read image with OpenCV
        np_img = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Preprocess for OCR
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        gray = cv2.medianBlur(gray, 3)

        # Optional: resize if too large
        h, w = gray.shape
        if w > 1000:
            scale = 1000 / w
            gray = cv2.resize(gray, (int(w*scale), int(h*scale)))

        # Extract text
        text = pytesseract.image_to_string(gray)

        return jsonify({"success": True, "extracted_text": text.strip()})

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
