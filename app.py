import streamlit as st
import gspread
from datetime import datetime

# 1. إعداد الصفحة
st.set_page_config(page_title="سجل المبيعات", page_icon="📈")
st.title("📈 لوحة تسجيل الأسعار")

# 2. دالة الاتصال
def get_worksheet():
    try:
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(dict(creds_dict))
        spreadsheet_id = '1KqtxT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        return sh.sheet1
    except Exception as e:
        return None # نرجع None في حالة الخطأ

# 3. واجهة الإدخال
price = st.text_input("أدخل السعر:")

# 4. زر الإضافة
if st.button("إضافة للمخزون"):
    if not price:
        st.error("يرجى إدخال السعر!")
    else:
        ws = get_worksheet()
        if ws is None:
            st.error("فشل الاتصال بملف الشيت، تأكد من الـ Secrets!")
        else:
            try:
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # البحث عن الصف التالي
                col_a = ws.col_values(1)
                next_row = len(col_a) + 1
                if next_row < 2: next_row = 2
                
                # التسجيل
                ws.update_cell(next_row, 1, now)
                ws.update_cell(next_row, 2, str(price))
                st.success("تم الحفظ بنجاح!")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")

# 5. زر العرض
if st.button("عرض السجل"):
    ws = get_worksheet()
    if ws:
        data = ws.get_all_values()
        st.table(data)
    else:
        st.error("لا يمكن الوصول للبيانات.")
