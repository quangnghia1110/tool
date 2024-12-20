from flask import Flask, render_template, request, jsonify, send_from_directory, Response, stream_with_context, send_file
import os
import json
from werkzeug.utils import secure_filename
from MigrateSQLSERVERtoMYSQL.sql_converter import SQLConverter
from YouTubeToMP3.youtube_converter import YouTubeConverter
from queue import Queue
from Formatters.formatter import CodeFormatter
from MarkdownEditor.markdown_editor import MarkdownEditor
from WebsiteChecker.website_checker import WebsiteChecker
from WheelsOfName.wheel import WheelOfNames
from ToolDownloader.downloader import ToolDownloader

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Đảm bảo thư mục data tồn tại
data_dir = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Tạo các thư mục cần thiết
required_dirs = [
    'uploads',
    'data',
    'static/sounds',
    'YouTubeToMP3/downloads',
    'YouTubeToMP3/temp'
]

for directory in required_dirs:
    os.makedirs(directory, exist_ok=True)

# Khởi tạo SQL converter
sql_converter = SQLConverter()

# Thêm khởi tạo converter sau phần khởi tạo sql_converter
youtube_converter = YouTubeConverter()

# Khởi tạo formatter
code_formatter = CodeFormatter()

# Khởi tạo markdown editor
markdown_editor = MarkdownEditor()

# Khởi tạo website checker
website_checker = WebsiteChecker()

# Thêm khởi tạo
wheel_of_names = WheelOfNames()

# Thêm khởi tạo
tool_downloader = ToolDownloader()

def ensure_json_files():
    json_files = {
        'data/tools.json': [],
        'data/wheels.json': [],
        # Thêm các file JSON khác nếu cần
    }
    
    for filepath, default_content in json_files.items():
        if not os.path.exists(filepath):
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                json.dump(default_content, f)

# Gọi function khi khởi động app
ensure_json_files()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools/migrate-sql', methods=['GET', 'POST']) 
def migrate_sql():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.sql'):
            return jsonify({'error': 'Only SQL files are allowed'}), 400

        try:
            # Đọc nội dung file SQL
            sql_content = file.read().decode('utf-8')
            
            # Chuyển đổi SQL
            converted_sql = sql_converter.convert(sql_content)
            
            return jsonify({'result': converted_sql})

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return render_template('tools/migrate_sql.html')

@app.route('/tools/youtube-to-mp3', methods=['GET', 'POST'])
def youtube_to_mp3():
    return render_template('tools/youtube_to_mp3.html')

@app.route('/get-formats', methods=['POST'])
def get_formats():
    try:
        data = request.get_json()
        url = data.get('url')
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
            
        formats, title = youtube_converter.get_formats(url)
        return jsonify({
            'formats': formats,
            'title': title
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/download-format')
def download_format():
    try:
        url = request.args.get('url')
        format_id = request.args.get('format')
        if not url or not format_id:
            return jsonify({'error': 'Missing parameters'}), 400

        def generate():
            for progress in youtube_converter.download_with_progress(url, format_id):
                if progress['status'] == 'error':
                    yield f"data: {json.dumps(progress)}\n\n"
                    return
                elif progress['status'] == 'complete':
                    # Thêm đường dẫn file vào response
                    progress['download_url'] = f"/get-file?url={url}"
                yield f"data: {json.dumps(progress)}\n\n"

        response = Response(stream_with_context(generate()), mimetype='text/event-stream')
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['X-Accel-Buffering'] = 'no'
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/get-file')
def get_file():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({'error': 'Missing URL parameter'}), 400
            
        if hasattr(youtube_converter, 'current_file') and youtube_converter.current_file:
            filename = youtube_converter.current_file
            if os.path.exists(filename):
                response = send_file(
                    filename,
                    as_attachment=True,
                    download_name=os.path.basename(filename)
                )
                @response.call_on_close
                def cleanup():
                    try:
                        os.remove(filename)
                    except:
                        pass
                return response
                
        return jsonify({'error': 'File not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@app.route('/tools/count-api-json', methods=['GET', 'POST'])
def count_api_json():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.json'):
            return jsonify({'error': 'Only JSON files are allowed'}), 400

        try:
            # Đọc và phân tích file JSON
            json_content = json.loads(file.read().decode('utf-8'))
            
            # TODO: Thêm logic đếm API từ JSON
            # Ví dụ đơn giản:
            api_count = len(json_content.get('item', []))
            
            return jsonify({
                'total_apis': api_count,
                'details': json_content
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return render_template('tools/count_api_json.html')

@app.route('/tools/format-code', methods=['GET', 'POST'])
def format_code():
    if request.method == 'POST':
        try:
            content = request.form.get('code')
            language = request.form.get('language')
            
            if not content or not language:
                return jsonify({'error': 'Missing code or language'}), 400
            
            formatter_map = {
                'json': code_formatter.format_json,
                'html': code_formatter.format_html,
                'javascript': code_formatter.format_javascript,
                'css': code_formatter.format_css,
                'python': code_formatter.format_python
            }
            
            if language not in formatter_map:
                return jsonify({'error': 'Unsupported language'}), 400
                
            formatted_code = formatter_map[language](content)
            return jsonify({'result': formatted_code})

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return render_template('tools/format_code.html')

@app.route('/tools/markdown-editor', methods=['GET'])
def markdown_editor_tool():
    return render_template('tools/markdown_editor.html')

@app.route('/tools/markdown-editor/convert', methods=['POST'])
def convert_markdown():
    try:
        data = request.get_json()
        markdown_text = data.get('markdown', '')
        
        if not markdown_text:
            return jsonify({'error': 'No markdown provided'}), 400
            
        html = markdown_editor.convert_to_html(markdown_text)
        return jsonify({'html': html})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tools/markdown-editor/validate', methods=['POST'])
def validate_markdown():
    try:
        data = request.get_json()
        markdown_text = data.get('markdown', '')
        
        if not markdown_text:
            return jsonify({'error': 'No markdown provided'}), 400
            
        valid, errors = markdown_editor.validate_markdown(markdown_text)
        return jsonify({
            'valid': valid,
            'errors': errors
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/tools/website-checker', methods=['GET', 'POST'])
def website_checker_tool():
    if request.method == 'POST':
        try:
            data = request.get_json()
            url = data.get('url')
            
            if not url:
                return jsonify({'error': 'No URL provided'}), 400
                
            result = website_checker.get_full_page_screenshot(url)
            return jsonify(result)

        except Exception as e:
            return jsonify({'error': str(e)}), 400

    return render_template('tools/website_checker.html')

@app.route('/tools/wheel-of-names', methods=['GET'])
def wheel_of_names_tool():
    return render_template('tools/wheel_of_names.html')

@app.route('/tools/wheel-of-names/create/', methods=['POST'])
def create_wheel():
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400
        
        print("Received data:", data)  # Debug print
        
        success, wheel_id = wheel_of_names.create_wheel(
            data['name'],
            data['items']
        )
        print("Create result:", success, wheel_id)  # Debug print
        
        return jsonify({
            'success': success,
            'message': wheel_id if success else str(wheel_id)
        })
    except Exception as e:
        print("Error:", str(e))  # Debug print
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/tools/wheel-of-names/list/', methods=['GET'])
def list_wheels():
    wheels = wheel_of_names.get_wheels()
    print("Available wheels:", wheels)  # Debug print
    return jsonify(wheels)

@app.route('/tools/wheel-of-names/get/<wheel_id>', methods=['GET'])
def get_wheel(wheel_id):
    wheel = wheel_of_names.get_wheel(wheel_id)
    if wheel:
        return jsonify(wheel)
    return jsonify({'error': 'Wheel not found'}), 404

@app.route('/tools/wheel-of-names/spin/<wheel_id>', methods=['GET'])
def spin_wheel(wheel_id):
    success, result = wheel_of_names.spin_wheel(wheel_id)
    return jsonify({
        'success': success,
        'message': result
    })

@app.route('/tools/wheel-of-names/update/<wheel_id>', methods=['POST'])
def update_wheel(wheel_id):
    try:
        data = request.get_json()
        success, message = wheel_of_names.update_wheel(
            wheel_id,
            name=data.get('name'),
            items=data.get('items')
        )
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/tools/wheel-of-names/delete/<wheel_id>', methods=['POST'])
def delete_wheel(wheel_id):
    try:
        success, message = wheel_of_names.delete_wheel(wheel_id)
        return jsonify({
            'success': success,
            'message': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/tools/tool-downloader')
def tool_downloader_tool():
    tools = tool_downloader.get_tools()
    categories = tool_downloader.get_categories()
    return render_template('tools/tool_downloader.html', tools=tools, categories=categories)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Development
    app.run(debug=True)
else:
    # Production
    app.run(host='0.0.0.0', port=10000)