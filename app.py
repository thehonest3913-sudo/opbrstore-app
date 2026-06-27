import streamlit as st
import gspread
import json

# 1. إعداد واجهة البرنامج
st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

# 2. دالة الاتصال باستخدام المتغير النصي (الطريقة الأكثر استقراراً)
def get_worksheet():
    try:
        # قراءة النص الخام من الـ Secrets وتحويله لقاموس (Dictionary)
        creds_json = st.secrets["GCP_CREDENTIALS"]
        creds_dict = json.loads(creds_json)
        
        # الاتصال بجوجل
        gc = gspread.service_account_from_dict(creds_dict)
        spreadsheet_id = '1KqtT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        
        # اختيار الورقة الأولى
        return sh.sheet1 
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

# 3. واجهة الإدخال
name = st.text_input("اسم المنتج")
price = st.number_input("السعر", min_value=0.0)

# 4. زر الإضافة
if st.button("إضافة للمخزون"):
    if not name:
        st.error("من فضلك اكتب اسم المنتج!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(ws) # عرض رسالة الخطأ إذا وجدت
        else:
            # إضافة البيانات: السعر في العمود A، فراغ في B، والاسم في العمود C
            ws.append_row([price, "", name])
            st.success(f"تمت إضافة {name} بسعر {price} بنجاح!")
            st.balloons() 

# 5. عرض المنتجات
if st.button("تحديث وعرض المخزون"):
    ws = get_worksheet()
    if isinstance(ws, str):
        st.error(ws)
    else:
        data = ws.get_all_values()
        st.table(data)
