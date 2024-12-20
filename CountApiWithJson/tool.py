import json

# Đường dẫn tới file JSON của bạn
file_path = 'main.json'
output_file = 'main.txt'

# Đọc file JSON
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Danh sách để lưu trữ các API cùng với URL của chúng
api_list = []

def list_and_count_apis(items, parent=""):
    for item in items:
        if 'item' in item:
            new_parent = f"{parent} > {item['name']}" if parent else item['name']
            list_and_count_apis(item['item'], new_parent)
        else:
            api_name = f"{parent} > {item['name']}" if parent else item['name']
            # Lấy URL raw nếu có
            url = item['request']['url']['raw'] if 'url' in item['request'] and 'raw' in item['request']['url'] else "No URL found"
            api_list.append((api_name, url))

# Liệt kê và đếm API
list_and_count_apis(data['item'])

# Đếm số lượng API
api_count = len(api_list)

# Xuất kết quả ra file .txt
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(f"Số lượng API trong collection: {api_count}\n\n")
    f.write("Danh sách các API:\n")
    for i, (api, url) in enumerate(api_list, 1):
        f.write(f"{i}. {api} - URL: {url}\n")

print(f"Kết quả đã được xuất ra file {output_file}")
