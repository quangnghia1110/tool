import json
import os
from datetime import datetime

class ToolDownloader:
    def __init__(self):
        self.tools_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'tools.json')
        self._ensure_data_directory()
        self._init_default_tools()

    def _ensure_data_directory(self):
        os.makedirs(os.path.dirname(self.tools_file), exist_ok=True)
        if not os.path.exists(self.tools_file):
            with open(self.tools_file, 'w') as f:
                json.dump([], f)

    def _init_default_tools(self):
        """Khởi tạo danh sách công cụ mặc định"""
        default_tools = [
            # Browsers
            {
                "id": "chrome",
                "name": "Google Chrome",
                "description": "Fast and secure web browser from Google.",
                "category": "Browsers",
                "official_link": "https://www.google.com/chrome/",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://dl.google.com/chrome/install/ChromeStandaloneSetup64.exe"
                    }
                ]
            },
            {
                "id": "firefox",
                "name": "Mozilla Firefox",
                "description": "Free and open-source web browser from Mozilla.",
                "category": "Browsers",
                "official_link": "https://www.mozilla.org/firefox/",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US"
                    }
                ]
            },
            {
                "id": "edge",
                "name": "Microsoft Edge",
                "description": "Modern and fast browser built on Chromium.",
                "category": "Browsers",
                "official_link": "https://www.microsoft.com/edge",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://c2rsetup.officeapps.live.com/c2r/downloadEdge.aspx?platform=Default"
                    }
                ]
            },
            {
                "id": "python",
                "name": "Python",
                "description": "Python programming language",
                "category": "Environment",
                "official_link": "https://www.python.org/downloads/",
                "versions": [
                    {
                        "name": "Python 3.7",
                        "url": "https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe"
                    },
                    {
                        "name": "Python 3.8",
                        "url": "https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe"
                    },
                    {
                        "name": "Python 3.9",
                        "url": "https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe"
                    },
                    {
                        "name": "Python 3.10",
                        "url": "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe"
                    }
                ]
            },
            {
                "id": "java",
                "name": "Java Development Kit",
                "description": "Java Development Kit (JDK)",
                "category": "Environment",
                "official_link": "https://www.oracle.com/java/technologies/downloads/",
                "versions": [
                    {
                        "name": "JDK 17 LTS",
                        "url": "https://download.oracle.com/java/17/latest/jdk-17_windows-x64_bin.exe"
                    },
                    {
                        "name": "JDK 21 LTS",
                        "url": "https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe"
                    }
                ]
            },
            {
                "id": "nodejs",
                "name": "Node.js",
                "description": "JavaScript runtime built on Chrome's V8 JavaScript engine",
                "category": "Environment",
                "official_link": "https://nodejs.org/",
                "versions": [
                    {
                        "name": "v20 LTS",
                        "url": "https://nodejs.org/dist/v20.11.1/node-v20.11.1-x64.msi"
                    },
                    {
                        "name": "v21 Current",
                        "url": "https://nodejs.org/dist/v21.7.1/node-v21.7.1-x64.msi"
                    }
                ]
            },

            # Development
            {
                "id": "vscode",
                "name": "Visual Studio Code",
                "description": "Code editor redefined and optimized for building and debugging modern web and cloud applications.",
                "category": "Development",
                "icon": "fa-code",
                "official_link": "https://code.visualstudio.com/download",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
                    }
                ]
            },
            {
                "id": "postman",
                "name": "Postman",
                "description": "Platform for API development and testing.",
                "category": "Development",
                "icon": "fa-paper-plane",
                "official_link": "https://www.postman.com/downloads/",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://dl.pstmn.io/download/latest/win64"
                    }
                ]
            },
            {
                "id": "git",
                "name": "Git",
                "description": "Distributed version control system.",
                "category": "Development",
                "icon": "fa-code-branch",
                "official_link": "https://git-scm.com/downloads",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://github.com/git-for-windows/git/releases/download/v2.39.2.windows.2/Git-2.39.2-64-bit.exe"
                    }
                ]
            },
            {
                "id": "intellij",
                "name": "IntelliJ IDEA",
                "description": "Powerful IDE for Java development with advanced coding assistance and ergonomic design.",
                "category": "Development",
                "icon": "fa-laptop-code",
                "official_link": "https://www.jetbrains.com/idea/download/",
                "versions": [
                    {
                        "name": "Windows (Community)",
                        "url": "https://download.jetbrains.com/idea/ideaIC-2023.1.3.exe"
                    }
                ]
            },
            {
                "id": "cursor",
                "name": "Cursor",
                "description": "AI-first code editor that helps you code smarter and faster.",
                "category": "Development",
                "icon": "fa-terminal",
                "official_link": "https://cursor.sh/",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://cursor.sh/download/Cursor-win32-x64.exe"
                    }
                ]
            },

            # Database
            {
                "id": "mysql-server",
                "name": "MySQL Server",
                "description": "World's most popular open source database.",
                "category": "Database",
                "icon": "fa-database",
                "official_link": "https://dev.mysql.com/downloads/mysql/",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-8.0.33-winx64.msi"
                    }
                ]
            },
            {
                "id": "mysql-workbench",
                "name": "MySQL Workbench",
                "description": "Visual database design and administration tool for MySQL.",
                "category": "Database",
                "icon": "fa-table",
                "official_link": "https://dev.mysql.com/downloads/workbench/",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://dev.mysql.com/get/Downloads/MySQL-8.0/mysql-workbench-community-8.0.33-winx64.msi"
                    }
                ]
            },

            # Communication
            {
                "id": "zalo",
                "name": "Zalo",
                "description": "Popular messaging app in Vietnam.",
                "category": "Communication",
                "icon": "fa-comments",
                "official_link": "https://zalo.me/pc",
                "versions": [
                    {
                        "name": "Windows",
                        "url": "https://res-download-pc.zadn.vn/hybrid/ZaloSetup.exe"
                    }
                ]
            },

            # Utilities
            {
                "id": "teamviewer",
                "name": "TeamViewer",
                "description": "Remote desktop access and support software.",
                "category": "Utilities",
                "icon": "fa-desktop",
                "official_link": "https://www.teamviewer.com/download/",
                "versions": [
                    {
                        "name": "Windows",
                        "url": "https://download.teamviewer.com/download/TeamViewer_Setup.exe"
                    }
                ]
            },
            {
                "id": "ultra-viewer",
                "name": "Ultra Viewer",
                "description": "Free remote desktop software for Windows.",
                "category": "Utilities",
                "icon": "fa-display",
                "official_link": "https://www.ultraviewer.net/en/download.html",
                "versions": [
                    {
                        "name": "Windows (Full)",
                        "url": "https://www.ultraviewer.net/en/UltraViewer_setup_6.6_en.exe"
                    }
                ]
            },
            {
                "id": "winrar",
                "name": "WinRAR",
                "description": "Popular file archiver utility for Windows.",
                "category": "Utilities",
                "icon": "fa-file-zipper",
                "official_link": "https://www.win-rar.com/download.html",
                "versions": [
                    {
                        "name": "Windows x64",
                        "url": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-621.exe"
                    }
                ]
            }
        ]

        try:
            with open(self.tools_file, 'r') as f:
                current_tools = json.load(f)
                
            # Chỉ thêm công cụ mặc định nếu chưa tồn tại
            current_tool_ids = {tool['id'] for tool in current_tools}
            new_tools = [tool for tool in default_tools if tool['id'] not in current_tool_ids]
            
            if new_tools:
                current_tools.extend(new_tools)
                with open(self.tools_file, 'w') as f:
                    json.dump(current_tools, f, indent=4)
                    
        except Exception as e:
            print(f"Error initializing default tools: {str(e)}")

    def get_tools(self, category=None):
        """Lấy danh sách công cụ, có thể lọc theo category"""
        try:
            with open(self.tools_file, 'r') as f:
                tools = json.load(f)
            
            if category:
                return [tool for tool in tools if tool['category'] == category]
            return tools
        except Exception:
            return []

    def get_tool(self, tool_id):
        """Lấy thông tin chi tiết của một công cụ"""
        tools = self.get_tools()
        for tool in tools:
            if tool['id'] == tool_id:
                return tool
        return None

    def get_categories(self):
        """Lấy danh sách các category"""
        tools = self.get_tools()
        return list(set(tool['category'] for tool in tools))

    def add_tool(self, tool_data):
        """Thêm công cụ mới"""
        try:
            tools = self.get_tools()
            
            # Kiểm tra ID đã tồn tại
            if any(tool['id'] == tool_data['id'] for tool in tools):
                return False, "Tool ID already exists"
            
            tools.append(tool_data)
            
            with open(self.tools_file, 'w') as f:
                json.dump(tools, f, indent=4)
                
            return True, "Tool added successfully"
        except Exception as e:
            return False, str(e)

    def update_tool(self, tool_id, tool_data):
        """Cập nhật thông tin công cụ"""
        try:
            tools = self.get_tools()
            
            for i, tool in enumerate(tools):
                if tool['id'] == tool_id:
                    tools[i] = {**tool, **tool_data}
                    
                    with open(self.tools_file, 'w') as f:
                        json.dump(tools, f, indent=4)
                        
                    return True, "Tool updated successfully"
                    
            return False, "Tool not found"
        except Exception as e:
            return False, str(e)

    def delete_tool(self, tool_id):
        """Xóa một công cụ"""
        try:
            tools = self.get_tools()
            tools = [t for t in tools if t['id'] != tool_id]
            
            with open(self.tools_file, 'w') as f:
                json.dump(tools, f, indent=4)
                
            return True, "Tool deleted successfully"
        except Exception as e:
            return False, str(e) 