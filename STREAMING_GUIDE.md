# 📡 Real-Time Data Streaming Integration Guide

## 🎯 مرحباً بك في نظام البيانات المتدفقة!

تم تطوير البرنامج الكامل الآن للعمل مع بيانات متدفقة **حقيقية من العمليات الجارية** كما لو كان في شركة توزيع أدوية فعلية.

---

## 🚀 المميزات الجديدة

### 1️⃣ **📡 Real-Time Monitor (صفحة جديدة)**
```
Navigation → 📡 Real-Time Monitor
↓
عرض مباشر لـ:
- البيانات المتدفقة من أنظمة التتبع
- حالة الشحنات النشطة
- الإنذارات الفورية
- رسوم بيانية حية
```

### 2️⃣ **مصادر البيانات المدعومة**

| المصدر | الاستخدام | الحالة |
|--------|----------|--------|
| **مولّد محاكاة** (Simulator) | تطوير واختبار | ✅ يعمل الآن |
| **قاعدة بيانات** | شركات حقيقية | 🔧 تكوين مطلوب |
| **API REST** | معالجة سحابية | 🔗 سهل التكامل |
| **Message Queue** | بيانات فورية عالية | 📨 معايير صناعة |

---

## 🔧 الدوال الرئيسية

### `LiveDataStreamSimulator` 
نموذج محاكاة البيانات المتدفقة:

```python
from data_stream import LiveDataStreamSimulator

# إنشاء مثيل
simulator = LiveDataStreamSimulator(shipment_count=100)

# الحصول على دفعة من الشحنات (5 شحنات)
batch = simulator.get_next_batch(batch_size=5)

# شحنة واحدة فقط
single = simulator.get_latest_shipment()
```

### `DatabaseStreamSimulator`
محاكاة قاعدة بيانات متصلة:

```python
from data_stream import DatabaseStreamSimulator

db = DatabaseStreamSimulator(refresh_interval=5)  # تحديث كل 5 ثوان

# جلب الشحنات النشطة
active = db.get_active_shipments()

# الشحنات عالية المخاطر
high_risk = db.get_high_risk_shipments()
```

---

## 📊 البيانات المتدفقة المتاحة

كل شحنة تتضمن 22 عامل بيانات:

```
📦 معرف الشحنة (shipment_id)
📍 موقع GPS (latitude/longitude)
🌡️ درجة الحرارة من أجهزة IoT
🌦️ حالة الطقس والازدحام المروري
📦 حالة البضاعة والمخزون
🚗 أداء السائق والتعب
🚢 ازدحام الميناء
💰 تكاليف الشحن والطلب
⏱️ أوقات التحميل والجمارك
```

---

## 🔌 كيفية الربط ببيانات حقيقية من شركتك

### **الخيار 1: ملف CSV متحديث**
```python
import pandas as pd

def stream_from_csv(file_path, chunk_size=10):
    while True:
        df = pd.read_csv(file_path)
        yield df.tail(chunk_size)
        time.sleep(5)  # تحديث كل 5 ثوان
```

### **الخيار 2: قاعدة بيانات (PostgreSQL/MySQL)**
```python
import psycopg2

def stream_from_database():
    conn = psycopg2.connect("dbname=pharma user=admin")
    cursor = conn.cursor()
    
    while True:
        cursor.execute("""
            SELECT * FROM shipments 
            WHERE created_at > now() - interval '5 minutes'
            ORDER BY created_at DESC
        """)
        yield pd.DataFrame(cursor.fetchall())
        time.sleep(5)
```

### **الخيار 3: API REST**
```python
import requests

def stream_from_api(api_url):
    while True:
        response = requests.get(f"{api_url}/live-shipments")
        yield pd.DataFrame(response.json())
        time.sleep(5)
```

### **الخيار 4: Message Queue (Kafka/RabbitMQ)**
```python
from kafka import KafkaConsumer
import json

def stream_from_kafka(topic):
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    for msg in consumer:
        yield pd.DataFrame([msg.value])
```

---

## 📱 لوحة المراقبة الحية - تتضمن:

### ✅ **KPI Cards**
- عدد الشحنات النشطة
- نسبة المخاطر العالية
- انتهاكات درجة الحرارة
- متوسط درجة المخاطر

### ✅ **جدول البيانات المباشر**
- قائمة الشحنات عالية المخاطر
- تحديث فوري مع كل بيانات جديدة
- ألوان تنبيهات لحالات حرجة

### ✅ **رسوم بيانية حية**
- توزيع درجات الحرارة
- توزيع درجات المخاطر
- خريطة المسارات النشطة

### ✅ **Auto-Refresh**
- تحديث تلقائي كل 5 ثوان
- يمكن التحكم من لوحة التحكم
- زر تحديث يدوي فوري

---

## 🎮 كيفية الاستخدام

### الخطوة 1: اختر البيانات المتدفقة
ترك البرنامج كما هو (محاكاة) أو ربط به بنظامك الفعلي

### الخطوة 2: اذهب إلى Real-Time Monitor
```
📱 التطبيق > 📡 Real-Time Monitor
```

### الخطوة 3: شاهد البيانات تتحدث مباشرة
- شحنات جديدة تظهر فوراً
- التنبؤات تتحدث في الوقت الفعلي
- الإنذارات تظهر للحالات الحرجة

### الخطوة 4: اتخذ إجراءات فورية
- كل شحنة عالية المخاطر لها توصية فورية
- درجات حرارة خاطئة = تحويل شحنة
- تأخيرات متوقعة = جدولة بديلة

---

## 🔐 الأمان والامتثال

- ✅ لا توجد بيانات PII مخزنة
- ✅ الإرسال مشفر (HTTPS/SSL)
- ✅ سجلات تدقيق لكل قرار
- ✅ متوافق مع GDP/FDA

---

## 🚀 الخطوات التالية

### للتطوير الإضافي:

1. **ربط قاعدة بيانات فعلية**
   - عدّل `data_stream.py`
   - استخدم `DatabaseStreamSimulator` كقالب

2. **إضافة نبضات (Webhooks)**
   - إشعارات فورية عند الأحداث الحرجة
   - تكامل مع Slack/Email

3. **التخزين التاريخي**
   - حفظ جميع التنبؤات
   - تحليل الأداء على المدى الطويل

4. **لوحة تحكم متقدمة**
   - مقارنة الأداء
   - تقارير مخصصة
   - إحصائيات الدقة

---

## 📞 الدعم والمساعدة

للمزيد من المعلومات، اطلع على:
- `app.py` - كود التطبيق الرئيسي
- `data_stream.py` - وحدة البيانات المتدفقة
- `README.md` - التوثيق العام
