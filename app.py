import streamlit as st
import gspread
from datetime import datetime # استدعاء مكتبة الوقت

# 1. إعداد الصفحة
st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

# 2. دالة الاتصال
def get_worksheet():
    try:
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(dict(creds_dict))
        spreadsheet_id = '1KqtxT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        return sh.sheet1
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

# 3. واجهة الإدخال
price = st.text_input("سعر المنتج")

# 4. زر الإضافة
if st.button("إضافة للمخزون"):
    if not price:
        st.error("يرجى إدخال السعر!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(ws)
        else:
            try:
                # جلب التاريخ والوقت الحالي
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # البحث عن الصف التالي في العمود A
                col_a_values = ws.col_values(1)
                next_row = len(col_a_values) + 1
                if next_row < 2: next_row = 2 # للبدء بعد العناوين
                
                # الكتابة: التاريخ في A، السعر في B
                ws.update_cell(next_row, 1, now)
                ws.update_cell(next_row, 2, str(price))
                
                st.success(f"تم تسجيل السعر {price} في الصف {next_row} بتاريخ {now}")
            except Exception as e:
                st.error(f"خطأ أثناء الكتابة: {e}")
