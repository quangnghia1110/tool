from flask import Flask, render_template, request, jsonify
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Đảm bảo thư mục uploads tồn tại
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools/count-api', methods=['GET', 'POST'])
def count_api():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({'error': 'Only JSON files are allowed'}), 400

        try:
            # Đọc và parse JSON
            json_data = json.load(file)
            api_list = []

            def list_and_count_apis(items, parent=""):
                for item in items:
                    if 'item' in item:
                        new_parent = f"{parent} > {item['name']}" if parent else item['name']
                        list_and_count_apis(item['item'], new_parent)
                    else:
                        api_name = f"{parent} > {item['name']}" if parent else item['name']
                        url = item['request']['url']['raw'] if 'url' in item['request'] and 'raw' in item['request']['url'] else "No URL found"
                        api_list.append({'name': api_name, 'url': url})

            list_and_count_apis(json_data['item'])
            
            return jsonify({
                'count': len(api_list),
                'apis': api_list
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return render_template('tools/count_api.html')

if __name__ == '__main__':
    app.run(debug=True) 