from flask import Flask, render_template, request, jsonify
import openai
import os
import json
from datetime import datetime

app = Flask(__name__)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-here'

class SkillAnalyzer:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)
    
    def analyze_skill_descriptions(self, old_description, new_description):
        """使用GPT-5-mini分析技能描述對比"""
        
        prompt = f"""
請作為一個專業的遊戲技能描述分析師，對比以下兩個技能描述版本：

舊版本描述：
{old_description}

新版本描述：
{new_description}

請進行以下分析，並使用清晰的格式：

1. 內容一致性檢查：
   - 兩個版本的技能內容是否相同？
   - 是否有遺漏或新增的技能效果？
   - 數值、條件、觸發機制是否一致？

2. 描述合理性分析：
   - 新描述是否符合遊戲邏輯？
   - 是否有描述不清晰或矛盾的地方？
   - 技能效果描述是否完整？

3. 中文文法檢查：
   - 語句是否通順？
   - 用詞是否準確？
   - 是否有語法錯誤？
   - 標點符號使用是否正確？

4. 建議改進：
   - 針對發現的問題提供具體改進建議
   - 提供更優雅的表達方式

請以結構化的方式回答，使用以下格式：
- 對於通過的項目使用 ✅ 符號
- 對於有問題的項目使用 ❌ 符號  
- 對於需要注意的項目使用 ⚠️ 符號
- 標明每個問題的嚴重程度（輕微/中等/嚴重）
"""

        try:
            # 使用 Responses API（gpt-5-mini 要求）
            response = self.client.responses.create(
                model="gpt-5-mini",
                input=(
                    "你是一個專業的遊戲技能描述分析師，擅長發現技能描述中的問題。\n\n" + prompt
                ),
                max_output_tokens=4000,
            )
            analysis_text = getattr(response, "output_text", None)
            if not analysis_text:
                # 後備：嘗試從結構化輸出中提取
                try:
                    analysis_text = "".join(
                        part.get("text", "")
                        for item in getattr(response, "output", [])
                        for part in getattr(item, "content", [])
                        if isinstance(part, dict)
                    )
                except Exception:
                    analysis_text = ""

            return {
                "success": True,
                "analysis": analysis_text or "（無內容返回）",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json()
        api_key = data.get('api_key')
        old_description = data.get('old_description', '').strip()
        new_description = data.get('new_description', '').strip()
        
        # 驗證輸入
        if not api_key:
            return jsonify({"success": False, "error": "請輸入OpenAI API Key"})
        
        if not old_description or not new_description:
            return jsonify({"success": False, "error": "請輸入舊版本和新版本的技能描述"})
        
        # 創建分析器並進行分析
        analyzer = SkillAnalyzer(api_key)
        result = analyzer.analyze_skill_descriptions(old_description, new_description)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"success": False, "error": f"分析過程中發生錯誤: {str(e)}"})

@app.route('/save_analysis', methods=['POST'])
def save_analysis():
    """保存分析結果到本地文件"""
    try:
        data = request.get_json()
        
        # 創建分析記錄
        analysis_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "old_description": data.get('old_description'),
            "new_description": data.get('new_description'),
            "analysis_result": data.get('analysis_result')
        }
        
        # 保存到文件
        filename = f"skill_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join('analysis_logs', filename)
        
        # 確保目錄存在
        os.makedirs('analysis_logs', exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(analysis_record, f, ensure_ascii=False, indent=2)
        
        return jsonify({"success": True, "message": f"分析結果已保存到 {filename}"})
        
    except Exception as e:
        return jsonify({"success": False, "error": f"保存失敗: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5000'))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug, host='0.0.0.0', port=port)
