import os
from flask import Flask, render_template, request, jsonify
from PIL import Image
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key="AIzaSyDI8YCtA8MGHoPmOHaIZHMPQkMUwWQ2UeY")

def send_text_request(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print("❌ Text Request Error:", e)
        return "Sorry, Gemini couldn't process your request."

def image_analysis_request(image_file):
    try:
        image = Image.open(image_file)
        model = genai.GenerativeModel("gemini-pro-vision")
        response = model.generate_content(["Analyze this image and describe it.", image])
        return response.text
    except Exception as e:
        print("❌ Image Analysis Error:", e)
        return "Sorry, Gemini couldn't analyze the image."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text', methods=['POST'])
def text():
    try:
        data = request.get_json()
        user_input = data.get('message')
        print("📨 Text Input Received:", user_input)
        reply = send_text_request(user_input)
        print("📤 Gemini Reply:", reply)
        return jsonify({'response': reply})
    except Exception as e:
        print("❌ /text Route Error:", e)
        return jsonify({'response': "Error occurred while processing text."})

@app.route('/image', methods=['POST'])
def image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    try:
        image_file = request.files['image']
        print("📷 Image Uploaded:", image_file.filename)
        result = image_analysis_request(image_file)
        print("📤 Gemini Image Reply:", result)
        return jsonify({'response': result})
    except Exception as e:
        print("❌ /image Route Error:", e)
        return jsonify({'response': "Error occurred while analyzing image."})

if __name__ == '__main__':
    print("🚀 Starting Gemini Chat App...")
    app.run(debug=True)


