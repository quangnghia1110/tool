from flask import Flask, render_template, request, jsonify
import base64
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('formatter.html')

@app.route('/export-image', methods=['POST'])
def export_image():
    try:
        # Nhận data URL của ảnh từ client
        image_data = request.json.get('imageData')
        if not image_data:
            return jsonify({'error': 'No image data received'}), 400

        # Xử lý data URL
        image_data = image_data.split(',')[1]
        image_binary = base64.b64decode(image_data)
        
        # Tạo tên file độc nhất
        filename = f"code_snapshot.png"
        
        # Lưu ảnh
        image = Image.open(BytesIO(image_binary))
        image.save(f"static/exports/{filename}")
        
        return jsonify({
            'success': True,
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 