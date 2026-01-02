"""設定資料庫管理 - 使用 SQLite 儲存應用程式設定"""
import sqlite3
import os
from typing import Optional
from pathlib import Path


class SettingsDB:
    """設定資料庫管理類"""
    
    def __init__(self, db_path: Optional[str] = None):
        """
        初始化設定資料庫
        
        Args:
            db_path: 資料庫文件路徑，如果為 None 則使用預設路徑
        """
        if db_path is None:
            # 使用應用程式數據目錄
            if os.name == 'nt':  # Windows
                app_data = os.getenv('APPDATA', os.path.expanduser('~'))
                app_dir = Path(app_data) / 'RelaxTime'
            else:
                app_dir = Path.home() / '.relaxtime'
            
            # 確保目錄存在
            app_dir.mkdir(parents=True, exist_ok=True)
            db_path = str(app_dir / 'settings.db')
        
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """初始化資料庫表結構"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 創建設定表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _get_connection(self) -> sqlite3.Connection:
        """獲取資料庫連接"""
        return sqlite3.connect(self.db_path)
    
    def set(self, key: str, value: str):
        """
        設置設定值
        
        Args:
            key: 設定鍵名
            value: 設定值（字串格式）
        """
        from datetime import datetime
        updated_at = datetime.now().isoformat()
        
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value, updated_at)
            VALUES (?, ?, ?)
        ''', (key, value, updated_at))
        
        conn.commit()
        conn.close()
    
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        獲取設定值
        
        Args:
            key: 設定鍵名
            default: 如果不存在則返回的預設值
        
        Returns:
            設定值，如果不存在則返回 default
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = cursor.fetchone()
        
        conn.close()
        
        if result:
            return result[0]
        return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """
        獲取布林值設定
        
        Args:
            key: 設定鍵名
            default: 預設值
        
        Returns:
            布林值
        """
        value = self.get(key)
        if value is None:
            return default
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def set_bool(self, key: str, value: bool):
        """
        設置布林值設定
        
        Args:
            key: 設定鍵名
            value: 布林值
        """
        self.set(key, 'true' if value else 'false')
    
    def get_int(self, key: str, default: int = 0) -> int:
        """
        獲取整數值設定
        
        Args:
            key: 設定鍵名
            default: 預設值
        
        Returns:
            整數值
        """
        value = self.get(key)
        if value is None:
            return default
        try:
            return int(value)
        except ValueError:
            return default
    
    def set_int(self, key: str, value: int):
        """
        設置整數值設定
        
        Args:
            key: 設定鍵名
            value: 整數值
        """
        self.set(key, str(value))
    
    def delete(self, key: str):
        """
        刪除設定
        
        Args:
            key: 設定鍵名
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM settings WHERE key = ?', (key,))
        
        conn.commit()
        conn.close()
    
    def get_all(self) -> dict:
        """
        獲取所有設定
        
        Returns:
            包含所有設定的字典
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT key, value FROM settings')
        results = cursor.fetchall()
        
        conn.close()
        
        return {key: value for key, value in results}


# 全局設定資料庫實例
_settings_db: Optional[SettingsDB] = None


def get_settings_db() -> SettingsDB:
    """獲取全局設定資料庫實例"""
    global _settings_db
    if _settings_db is None:
        _settings_db = SettingsDB()
    return _settings_db
