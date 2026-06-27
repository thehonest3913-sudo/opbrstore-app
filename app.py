import streamlit as st
import gspread

# إعداد الصفحة
st.set_page_config(page_title="Opbrstore cPanel", page_icon="📦")
st.title("لوحة تحكم (cPanel) - Opbrstore")

# الاتصال بجوجل شيتس باستخدام البيانات الموجودة في الخزنة (Secrets)
def get_google_sheet():
    try:
        # قراءة البيانات من الـ Secrets
        creds_dict = st.secrets["gcp_service_account"]
        # الاتصال
        gc = gspread.service_account_from_dict(creds_dict)
        # فتح الملف بالـ ID
        spreadsheet_id = '1KqtT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        return sh.get_worksheet(0)
    except Exception as e:
        return str(e)

# واجهة إضافة المنتج
name = st.text_input("اسم المنتج")
price = st.number_input("السعر", min_value=0.0)

if st.button("إضافة للمخزون"):
    if not name:
        st.warning("يرجى إدخال اسم المنتج!")
    else:
        ws = get_google_sheet()
        if isinstance(ws, str):
            st.error(f"خطأ في الاتصال: {ws}")
        else:
            ws.append_row([name, price])
            st.success(f"تمت إضافة {name} بنجاح!")