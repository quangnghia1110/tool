import random
import json
import os
from datetime import datetime

class WheelOfNames:
    def __init__(self):
        self.wheels_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'wheels.json')
        self._ensure_data_directory()

    def _ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.wheels_file), exist_ok=True)
        if not os.path.exists(self.wheels_file):
            with open(self.wheels_file, 'w') as f:
                json.dump([], f)

    def create_wheel(self, name, items):
        """Tạo một vòng quay mới"""
        try:
            if not name or not items:
                return False, "Name and items are required"

            with open(self.wheels_file, 'r') as f:
                wheels = json.load(f)
            
            new_wheel = {
                'id': str(random.randint(10000, 99999)),
                'name': name,
                'items': items,
                'history': []
            }
            
            wheels.append(new_wheel)
            
            with open(self.wheels_file, 'w') as f:
                json.dump(wheels, f, indent=4)
                
            return True, new_wheel['id']
        except Exception as e:
            return False, str(e)

    def get_wheels(self):
        """Lấy danh sách các vòng quay"""
        try:
            with open(self.wheels_file, 'r') as f:
                return json.load(f)
        except Exception:
            return []

    def get_wheel(self, wheel_id):
        """Lấy thông tin một vòng quay cụ thể"""
        wheels = self.get_wheels()
        for wheel in wheels:
            if wheel['id'] == wheel_id:
                return wheel
        return None

    def spin_wheel(self, wheel_id):
        """Quay vòng quay và trả về kết quả"""
        try:
            wheels = self.get_wheels()
            for wheel in wheels:
                if wheel['id'] == wheel_id:
                    if not wheel['items']:
                        return False, "No items in wheel"
                    
                    result = random.choice(wheel['items'])
                    
                    # Lưu lịch sử
                    wheel['history'].append({
                        'result': result,
                        'timestamp': str(datetime.now())
                    })
                    
                    with open(self.wheels_file, 'w') as f:
                        json.dump(wheels, f, indent=4)
                    
                    return True, result
                    
            return False, "Wheel not found"
        except Exception as e:
            return False, str(e)

    def update_wheel(self, wheel_id, name=None, items=None):
        """Cập nhật thông tin vòng quay"""
        try:
            wheels = self.get_wheels()
            for wheel in wheels:
                if wheel['id'] == wheel_id:
                    if name:
                        wheel['name'] = name
                    if items:
                        wheel['items'] = items
                    
                    with open(self.wheels_file, 'w') as f:
                        json.dump(wheels, f, indent=4)
                    
                    return True, "Wheel updated successfully"
            
            return False, "Wheel not found"
        except Exception as e:
            return False, str(e)

    def delete_wheel(self, wheel_id):
        """Xóa một vòng quay"""
        try:
            wheels = self.get_wheels()
            wheels = [w for w in wheels if w['id'] != wheel_id]
            
            with open(self.wheels_file, 'w') as f:
                json.dump(wheels, f, indent=4)
                
            return True, "Wheel deleted successfully"
        except Exception as e:
            return False, str(e) 