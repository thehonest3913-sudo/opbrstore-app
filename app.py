import streamlit as st
import gspread
import json
import base64

st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

def get_worksheet():
    try:
        # 1. جلب النص المشفر من الـ Secrets
        encoded_json = st.secrets["GCP_JSON"]
        
        # 2. فك التشفير (Base64 -> JSON String)
        decoded_bytes = base64.b64decode(encoded_json)
        creds_dict = json.loads(decoded_bytes)
        
        # 3. الاتصال بجوجل
        gc = gspread.service_account_from_dict(creds_dict)
        sh = gc.open_by_key('1KqtT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w')
        return sh.sheet1
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

name = st.text_input("اسم المنتج")
price = st.text_input("السعر")

if st.button("إضافة للمخزون"):
    if not name or not price:
        st.error("يرجى إدخال اسم المنتج والسعر!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(ws)
        else:
            try:
                ws.append_row([str(price), "", name])
                st.success(f"تمت إضافة {name} بنجاح!")
            except Exception as e:
                st.error(f"خطأ أثناء الكتابة: {e}")
