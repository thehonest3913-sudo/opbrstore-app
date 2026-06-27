import streamlit as st
import gspread
from datetime import datetime

# 1. إعداد الصفحة
st.set_page_config(page_title="سجل المبيعات", page_icon="📈")
st.title("📈 لوحة تسجيل الأسعار")

# 2. دالة الاتصال بجوجل شيت
def get_worksheet():
    try:
        # قراءة المفاتيح من الـ Secrets
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(dict(creds_dict))
        # الـ ID الخاص بملف الشيت الخاص بك
        spreadsheet_id = '1KqtxT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        return sh.sheet1
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

# 3. واجهة الإدخال
price = st.text_input("أدخل السعر هنا:")

# 4. منطق إضافة البيانات
if st.button("إضافة للمخزون"):
    if not price:
        st.error("يرجى إدخال السعر أولاً!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(ws)
        else:
            try:
                # جلب
