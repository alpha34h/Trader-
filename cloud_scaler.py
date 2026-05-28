import os
import time
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- ⚙️ لوحة التحكم بالسيرفر السحابي الوهمي ---
GATEWAY_URL = "http://127.0.0.1:8051/receive"  # توجيه الأسعار مباشرة لبورت بوابتك الجديد
IS_RUNNING = False

def fetch_live_prices():
    """
    محاكي جلب الأسعار الحية من TradingView وضخها للبوابة المحلية.
    يمكنك استبدال منطق التوليد هنا بـ Webhook أو سحب حقيقي من منصتك.
    """
    global IS_RUNNING
    print("[📡 خادم Vercel] تم تفعيل محرك الضخ بنجاح...")
    
    # محاكاة سعر الذهب الافتراضي للبدء
    current_price = 2345.50 
    
    while IS_RUNNING:
        try:
            # هنا يتم توليد السعر أو جلبه لايف
            import random
            current_price += round(random.uniform(-0.5, 0.5), 2)
            
            # إرسال السعر فوراً إلى بوابة تيرمكس المعتمدة 8051
            payload = {
                "gateway_id": "XAUUSD 1M",
                "price": current_price,
                "timestamp": time.time()
            }
            
            # ضخ البيانات عبر الشبكة المحلية أو عبر الروابط المحقونة
            # ملاحظة: بما أن فيرسيل سحابي وتيرمكس محلي، المعالج المركزي سيقوم بربط هذا الرابط تلقائياً
            requests.post(GATEWAY_URL, json=payload, timeout=1.0)
            print(f"[🟢 ضخ سحابي] تم إرسال السعر: {current_price} بنجاح.")
            
        except Exception as e:
            print(f"[-] فشل إرسال النبضة، البوابة قد تكون مشغولة: {e}")
            
        time.sleep(1) # ضخ السعر ثانية بثانية

@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Vercel Fake Server is running stably.",
        "endpoints": {
            "start_pumping": "/start",
            "stop_pumping": "/stop"
        }
    }), 200

@app.route('/start', methods=['GET', 'POST'])
def start_server():
    global IS_RUNNING
    if not IS_RUNNING:
        IS_RUNNING = True
        # تشغيل الضخ في الخلفية لكي لا يتجمد السيرفر السحابي
        import threading
        threading.Thread(target=fetch_live_prices, daemon=True).start()
        return jsonify({"status": "pumping_started", "target_port": 8051}), 200
    return jsonify({"status": "already_running"}), 200

@app.route('/stop', methods=['GET', 'POST'])
def stop_server():
    global IS_RUNNING
    IS_RUNNING = False
    return jsonify({"status": "pumping_stopped"}), 200

# لتوافق Vercel مع تطبيقات Flask WSGI
app.debug = False
