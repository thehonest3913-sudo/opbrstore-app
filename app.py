import streamlit as st
import gspread

st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

def get_worksheet():
    try:
        # الاتصال المباشر عبر الـ Secrets
        creds = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(dict(creds))
        sh = gc.open_by_key('1KqtT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w')
        return sh.sheet1
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

name = st.text_input("اسم المنتج")
price = st.text_input("السعر")

if st.button("إضافة للمخزون"):
    if not name or not price:
        st.error("يرجى إدخال البيانات!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(ws)
        else:
            ws.append_row([str(price), "", name])
            st.success("تمت الإضافة!")

if st.button("عرض المخزون"):
    ws = get_worksheet()
    if isinstance(ws, str):
        st.error(ws)
    else:
        st.table(ws.get_all_values())
