#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
環境設置測試腳本
"""

import os
import sys

def test_imports():
    """測試必要的模組導入"""
    print("🔍 測試模組導入...")
    
    try:
        import flask
        print(f"✅ Flask {flask.__version__}")
    except ImportError:
        print("❌ Flask 未安裝")
        return False
    
    try:
        import openai
        print(f"✅ OpenAI {openai.__version__}")
    except ImportError:
        print("❌ OpenAI 未安裝")
        return False
    
    return True

def test_files():
    """測試必要文件是否存在"""
    print("\n📁 測試文件結構...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "templates/index.html",
        "README.md"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - 文件不存在")
            all_exist = False
    
    return all_exist

def test_flask_app():
    """測試Flask應用是否可以正常啟動"""
    print("\n🚀 測試Flask應用...")
    
    try:
        from app import app
        print("✅ Flask應用導入成功")
        
        # 測試路由
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ 主頁路由正常")
            else:
                print(f"❌ 主頁路由錯誤: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Flask應用測試失敗: {e}")
        return False
    
    return True

def main():
    print("🎮 遊戲技能描述對比分析工具 - 環境測試")
    print("=" * 60)
    
    # 測試導入
    if not test_imports():
        print("\n💡 請執行: pip install -r requirements.txt")
        return
    
    # 測試文件
    if not test_files():
        print("\n💡 請檢查文件結構")
        return
    
    # 測試Flask應用
    if not test_flask_app():
        print("\n💡 請檢查Flask應用代碼")
        return
    
    print("\n🎉 所有測試通過！環境設置完成")
    print("\n📋 下一步:")
    print("1. 獲取 OpenAI API Key")
    print("2. 執行: python run.py")
    print("3. 在瀏覽器中訪問: http://localhost:5000")

if __name__ == "__main__":
    main()
