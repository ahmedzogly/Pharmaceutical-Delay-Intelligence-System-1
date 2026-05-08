# 🔌 Integration Examples
# أمثلة على كيفية ربط البرنامج ببيانات حقيقية من أنظمة شركتك

"""
الملف يحتوي على كود جاهز للاستخدام مباشرة مع أنظمتك الفعلية
"""

# =====================================================
# 1️⃣ ربط مع ملف CSV متحديث (تحديث يدوي أو آلي)
# =====================================================

def integrate_with_csv():
    """
    اتصل بملف CSV يتم تحديثه من نظام الشركة كل دقيقة
    مثالي للشركات الصغيرة والمتوسطة
    """
    import pandas as pd
    import time
    from datetime import datetime
    
    CSV_PATH = "company_shipments.csv"  # ضع مسار الملف
    
    while True:
        try:
            # قراءة الملف
            df = pd.read_csv(CSV_PATH)
            
            # تعديل أسماء الأعمدة حسب نظامك
            required_cols = [
                'shipment_id', 'iot_temperature', 'cargo_condition_status',
                'port_congestion_level', 'vehicle_gps_latitude', 'vehicle_gps_longitude'
                # أضف الأعمدة الأخرى المطلوبة
            ]
            
            # تحقق من وجود الأعمدة
            if all(col in df.columns for col in required_cols):
                print(f"✅ تم قراءة {len(df)} شحنة في {datetime.now()}")
                yield df
            else:
                print(f"❌ أعمدة ناقصة في الملف")
                
        except Exception as e:
            print(f"❌ خطأ: {e}")
        
        time.sleep(60)  # قراءة كل دقيقة

# =====================================================
# 2️⃣ ربط مع قاعدة بيانات PostgreSQL
# =====================================================

def integrate_with_postgresql():
    """
    اتصال مباشر بقاعدة بيانات شركتك
    مثالي للشركات الكبيرة
    
    المتطلبات:
    pip install psycopg2-binary
    """
    import psycopg2
    import pandas as pd
    import time
    
    DB_CONFIG = {
        'host': 'your-db-server.com',      # عنوان الخادم
        'database': 'pharma_db',           # اسم قاعدة البيانات
        'user': 'admin',                   # اسم المستخدم
        'password': 'your-password',       # كلمة المرور
        'port': 5432
    }
    
    def fetch_shipments():
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            query = """
            SELECT * FROM shipments 
            WHERE status = 'in_transit'
            AND created_at > NOW() - INTERVAL '1 hour'
            ORDER BY created_at DESC
            """
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            print(f"❌ DB Error: {e}")
            return None
    
    while True:
        df = fetch_shipments()
        if df is not None and len(df) > 0:
            print(f"✅ جلب {len(df)} شحنة من قاعدة البيانات")
            yield df
        time.sleep(30)  # تحديث كل 30 ثانية


# =====================================================
# 3️⃣ ربط مع API REST (خدمة ويب)
# =====================================================

def integrate_with_api():
    """
    الاتصال مع خدمة ويب توفر بيانات الشحنات
    مثالي للأنظمة السحابية
    
    المتطلبات:
    pip install requests
    """
    import requests
    import pandas as pd
    import time
    from datetime import datetime, timedelta
    
    API_URL = "https://your-api.com/api/shipments"
    API_KEY = "your-secret-api-key"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    while True:
        try:
            # طلب الشحنات النشطة
            params = {
                "status": "in_transit",
                "since": (datetime.now() - timedelta(hours=1)).isoformat()
            }
            
            response = requests.get(API_URL, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            # تحويل إلى DataFrame
            data = response.json()
            df = pd.DataFrame(data['shipments'])
            
            print(f"✅ تم جلب {len(df)} شحنة من API")
            yield df
            
        except requests.exceptions.RequestException as e:
            print(f"❌ خطأ API: {e}")
        
        time.sleep(15)  # تحديث كل 15 ثانية


# =====================================================
# 4️⃣ ربط مع Apache Kafka (رسائل فورية)
# =====================================================

def integrate_with_kafka():
    """
    استقبال بيانات حقيقية من Kafka
    مثالي جداً للأنظمة الحديثة عالية الإنتاجية
    
    المتطلبات:
    pip install kafka-python
    """
    from kafka import KafkaConsumer
    import json
    import pandas as pd
    
    consumer = KafkaConsumer(
        'shipments',  # اسم الموضوع (Topic)
        bootstrap_servers=['localhost:9092'],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        group_id='pharma-monitor-group',
        auto_offset_reset='latest'
    )
    
    batch = []
    for message in consumer:
        shipment = message.value
        batch.append(shipment)
        
        # أرسل دفعة كل 5 رسائل
        if len(batch) >= 5:
            df = pd.DataFrame(batch)
            print(f"✅ معالجة دفعة من {len(batch)} شحنة من Kafka")
            yield df
            batch = []


# =====================================================
# 5️⃣ ربط مع Excel مع تحديث حي (Microsoft 365)
# =====================================================

def integrate_with_excel_online():
    """
    قراءة بيانات مباشرة من Excel Online
    شركتك تحدث الملف على OneDrive أو SharePoint
    
    المتطلبات:
    pip install openpyxl pyshare
    """
    import openpyxl
    import pandas as pd
    from pathlib import Path
    
    # إذا كان الملف مشاركة من خادم
    EXCEL_PATH = r"C:\Users\YourName\OneDrive - CompanyName\pharma_data.xlsx"
    
    while True:
        try:
            # قراءة الملف
            df = pd.read_excel(EXCEL_PATH, sheet_name='Current Shipments')
            
            # تصفية للبيانات النشطة فقط
            df = df[df['Status'] == 'In Transit']
            
            print(f"✅ تم قراءة {len(df)} شحنة من Excel")
            yield df
            
        except Exception as e:
            print(f"❌ خطأ Excel: {e}")
        
        import time
        time.sleep(120)  # تحديث كل دقيقتين


# =====================================================
# 6️⃣ محاكاة كاملة للاختبار (الوضع الحالي)
# =====================================================

def integrate_with_simulation():
    """
    الوضع الحالي - بيانات محاكاة
    استخدمها للتطوير والاختبار قبل الربط بالحقيقي
    """
    from data_stream import LiveDataStreamSimulator
    import pandas as pd
    
    simulator = LiveDataStreamSimulator(shipment_count=100)
    
    while True:
        batch = simulator.get_next_batch(batch_size=5)
        print(f"✅ محاكاة: جاهزة {len(batch)} شحنة جديدة")
        yield batch
        
        import time
        time.sleep(5)


# =====================================================
# 7️⃣ دالة وسيטة (Adapter Pattern)
# =====================================================

def get_data_stream(source_type='simulation', **config):
    """
    دالة موحدة لاختيار مصدر البيانات
    
    الاستخدام:
    for data in get_data_stream('csv', path='shipments.csv'):
        process_data(data)
    """
    
    if source_type == 'csv':
        return integrate_with_csv()
    
    elif source_type == 'postgresql':
        return integrate_with_postgresql()
    
    elif source_type == 'api':
        return integrate_with_api()
    
    elif source_type == 'kafka':
        return integrate_with_kafka()
    
    elif source_type == 'excel':
        return integrate_with_excel_online()
    
    elif source_type == 'simulation':
        return integrate_with_simulation()
    
    else:
        raise ValueError(f"❌ مصدر غير معروف: {source_type}")


# =====================================================
# 8️⃣ مثال عملي للاستخدام
# =====================================================

if __name__ == "__main__":
    """
    مثال على كيفية استخدام نظام البيانات المتدفقة
    """
    
    # اختر مصدر البيانات
    DATA_SOURCE = 'simulation'  # أو: 'csv', 'postgresql', 'api', 'kafka'
    
    print(f"🚀 بدء المراقبة من: {DATA_SOURCE}")
    print("=" * 50)
    
    for i, batch in enumerate(get_data_stream(DATA_SOURCE), 1):
        print(f"\n📦 دفعة #{i}")
        print(f"عدد الشحنات: {len(batch)}")
        print(f"الأعمدة: {list(batch.columns)[:5]}...")  # عرض أول 5 أعمدة
        
        if i >= 3:  # توقف بعد 3 دفعات للاختبار
            break
    
    print("\n✅ اكتمل الاختبار!")
