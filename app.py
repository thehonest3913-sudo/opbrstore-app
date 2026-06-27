import streamlit as st
import gspread

# دالة الاتصال
def get_worksheet():
    try:
        # قراءة البيانات من الـ Secrets
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(dict(creds_dict))
        
        # الـ ID الصحيح الذي أرسلته لي للتو
        spreadsheet_id = '1KqtxT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        
        sh = gc.open_by_key(spreadsheet_id)
        return sh.sheet1
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

# واجهة التطبيق
st.title("📦 لوحة تحكم Opbrstore")
name = st.text_input("اسم المنتج")
price = st.text_input("السعر")

if st.button("إضافة للمخزون"):
    ws = get_worksheet()
    if isinstance(ws, str):
        st.error(ws)
    else:
        ws.append_row([str(price), "", name])
        st.success("تمت الإضافة بنجاح!")
