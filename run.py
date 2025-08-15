#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
遊戲技能描述對比分析工具 - 啟動腳本
"""

import os
import sys
import subprocess

def check_dependencies():
    """檢查依賴是否已安裝"""
    try:
        import flask
        import openai
        print("✅ 所有依賴已安裝")
        return True
    except ImportError as e:
        print(f"❌ 缺少依賴: {e}")
        return False

def install_dependencies():
    """安裝依賴"""
    print("正在安裝依賴...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依賴安裝完成")
        return True
    except subprocess.CalledProcessError:
        print("❌ 依賴安裝失敗")
        return False

def main():
    print("🎮 遊戲技能描述對比分析工具")
    print("=" * 50)
    
    # 檢查依賴
    if not check_dependencies():
        print("\n正在嘗試安裝依賴...")
        if not install_dependencies():
            print("請手動執行: pip install -r requirements.txt")
            return
    
    # 檢查模板目錄
    templates_path = os.path.join(os.path.dirname(__file__), "templates")
    if not os.path.exists(templates_path):
        print(f"❌ 找不到 templates 目錄: {templates_path}")
        return
    
    # 啟動應用
    print("\n🚀 啟動應用...")
    print("📱 請在瀏覽器中訪問: http://localhost:5000")
    print("⏹️  按 Ctrl+C 停止應用")
    print("-" * 50)
    
    try:
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 應用已停止")
    except Exception as e:
        print(f"❌ 啟動失敗: {e}")

if __name__ == "__main__":
    main()
