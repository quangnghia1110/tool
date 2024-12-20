import re

class SQLConverter:
    def __init__(self):
        # Mapping kiểu dữ liệu
        self.type_mapping = {
            'NVARCHAR\s*\(\s*MAX\s*\)': 'LONGTEXT',
            'NVARCHAR\s*\((\d+)\)': r'VARCHAR(\1)',
            'VARCHAR\s*\(\s*MAX\s*\)': 'LONGTEXT',
            'DATETIME2': 'DATETIME',
            'UNIQUEIDENTIFIER': 'CHAR(36)',
            'NTEXT': 'LONGTEXT',
            'TEXT': 'LONGTEXT',
            'NCHAR': 'CHAR',
            'BIT': 'TINYINT(1)',
            'MONEY': 'DECIMAL(19,4)',
            'SMALLMONEY': 'DECIMAL(10,4)',
            'IMAGE': 'LONGBLOB',
            'VARBINARY\s*\(\s*MAX\s*\)': 'LONGBLOB',
            'HIERARCHYID': 'VARCHAR(255)',
            'DECIMAL': 'DECIMAL',
            'NUMERIC': 'DECIMAL'
        }

        # Mapping các hàm
        self.function_mapping = {
            'GETDATE\(\)': 'NOW()',
            'CURRENT_TIMESTAMP': 'NOW()',
            'GETUTCDATE\(\)': 'UTC_TIMESTAMP()',
            'ISNULL\((.*?),(.*?)\)': r'IFNULL(\1,\2)',
            'COALESCE': 'COALESCE',
            'CONVERT\((.*?),(.*?),(.*?)\)': self._convert_function,
            'CAST\((.*?) AS (.*?)\)': self._cast_function,
            'LEN\((.*?)\)': r'LENGTH(\1)',
            'CHARINDEX\((.*?),(.*?)\)': r'LOCATE(\1,\2)',
            'SUBSTRING\((.*?),(.*?),(.*?)\)': r'SUBSTRING(\1,\2,\3)',
            'DATEADD\((.*?),(.*?),(.*?)\)': self._dateadd_function,
            'DATEDIFF\((.*?),(.*?),(.*?)\)': self._datediff_function,
            'UPPER\((.*?)\)': r'UPPER(\1)',
            'LOWER\((.*?)\)': r'LOWER(\1)',
            'RTRIM\((.*?)\)': r'RTRIM(\1)',
            'LTRIM\((.*?)\)': r'LTRIM(\1)',
            'REPLACE\((.*?),(.*?),(.*?)\)': r'REPLACE(\1,\2,\3)',
            'NEWID\(\)': 'UUID()',
            'ROW_NUMBER\(\)': 'ROW_NUMBER()'
        }

    def _convert_function(self, match):
        """Xử lý hàm CONVERT của SQL Server"""
        parts = match.group().split(',')
        if len(parts) != 3:
            return match.group()
        
        data_type = parts[0].replace('CONVERT(', '').strip()
        value = parts[1].strip()
        style = parts[2].replace(')', '').strip()
        
        # Chuyển đổi format date
        if data_type.upper() in ['DATETIME', 'DATE']:
            return f"STR_TO_DATE({value}, '%Y-%m-%d %H:%i:%s')"
        
        return f"CAST({value} AS {self._convert_data_type(data_type)})"

    def _cast_function(self, match):
        """Xử lý hàm CAST của SQL Server"""
        value = match.group(1)
        data_type = match.group(2)
        return f"CAST({value} AS {self._convert_data_type(data_type)})"

    def _dateadd_function(self, match):
        """Chuyển đổi hàm DATEADD"""
        parts = match.group().split(',')
        if len(parts) != 3:
            return match.group()
        
        interval = parts[0].replace('DATEADD(', '').strip().upper()
        number = parts[1].strip()
        date = parts[2].replace(')', '').strip()
        
        interval_map = {
            'YEAR': 'YEAR',
            'MONTH': 'MONTH',
            'DAY': 'DAY',
            'HOUR': 'HOUR',
            'MINUTE': 'MINUTE',
            'SECOND': 'SECOND'
        }
        
        mysql_interval = interval_map.get(interval, 'DAY')
        return f"DATE_ADD({date}, INTERVAL {number} {mysql_interval})"

    def _datediff_function(self, match):
        """Chuyển đổi hàm DATEDIFF"""
        parts = match.group().split(',')
        if len(parts) != 3:
            return match.group()
        
        interval = parts[0].replace('DATEDIFF(', '').strip().upper()
        start_date = parts[1].strip()
        end_date = parts[2].replace(')', '').strip()
        
        interval_map = {
            'YEAR': 'YEAR',
            'MONTH': 'MONTH',
            'DAY': 'DAY',
            'HOUR': 'HOUR',
            'MINUTE': 'MINUTE',
            'SECOND': 'SECOND'
        }
        
        mysql_interval = interval_map.get(interval, 'DAY')
        return f"TIMESTAMPDIFF({mysql_interval}, {start_date}, {end_date})"

    def _convert_data_type(self, sql_type):
        """Chuyển đổi kiểu dữ liệu"""
        sql_type = sql_type.strip().upper()
        for pattern, mysql_type in self.type_mapping.items():
            if re.match(pattern, sql_type, re.IGNORECASE):
                return re.sub(pattern, mysql_type, sql_type, flags=re.IGNORECASE)
        return sql_type

    def convert_syntax(self, sql):
        """Chuyển đổi cú pháp SQL Server sang MySQL"""
        # Xóa schema [dbo].
        sql = re.sub(r'\[dbo\]\.', '', sql)
        
        # Chuyển đổi [table_name] thành `table_name`
        sql = re.sub(r'\[(.*?)\]', r'`\1`', sql)
        
        # Xóa WITH (NOLOCK)
        sql = re.sub(r'WITH\s*\(\s*NOLOCK\s*\)', '', sql, flags=re.IGNORECASE)
        
        # Chuyển đổi TOP n thành LIMIT n
        sql = re.sub(r'TOP\s+(\d+)', r'LIMIT \1', sql, flags=re.IGNORECASE)
        
        # Xử lý IDENTITY
        sql = re.sub(r'IDENTITY\(\d+,\s*\d+\)', 'AUTO_INCREMENT', sql, flags=re.IGNORECASE)
        
        # Xử lý GO command
        sql = re.sub(r'\nGO\b', ';', sql, flags=re.IGNORECASE)
        
        return sql

    def convert_functions(self, sql):
        """Chuyển đổi các hàm SQL Server sang MySQL"""
        result = sql
        for pattern, replacement in self.function_mapping.items():
            if callable(replacement):
                # Nếu replacement là một hàm
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
            else:
                # Nếu replacement là một chuỗi
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        return result

    def convert_data_types(self, sql):
        """Chuyển đổi kiểu dữ liệu SQL Server sang MySQL"""
        result = sql
        for pattern, mysql_type in self.type_mapping.items():
            result = re.sub(pattern, mysql_type, result, flags=re.IGNORECASE)
        return result

    def convert(self, sql):
        """Chuyển đổi toàn bộ SQL Server sang MySQL"""
        # Chuẩn hóa xuống dòng
        sql = sql.replace('\r\n', '\n')
        
        # Chuyển đổi theo thứ tự
        sql = self.convert_data_types(sql)
        sql = self.convert_functions(sql)
        sql = self.convert_syntax(sql)
        
        return sql 