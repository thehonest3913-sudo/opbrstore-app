import streamlit as st
import gspread
import json

st.title("📦 لوحة تحكم Opbrstore")

def get_worksheet():
    try:
        creds_json = st.secrets["GCP_CREDENTIALS"]
        creds_dict = json.loads(creds_json)
        gc = gspread.service_account_from_dict(creds_dict)
        spreadsheet_id = '1KqtT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        return sh.sheet1 
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

name = st.text_input("اسم المنتج")
price = st.text_input("السعر")

if st.button("إضافة للمخزون"):
    # هنا قمنا بتعديل الشرط ليشمل الاسم والسعر معاً
    if not name or not price:
        st.error("يرجى التأكد من إدخال كل من اسم المنتج والسعر!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(ws)
        else:
            try:
                ws.append_row([price, "", name])
                st.success(f"تمت إضافة {name} بنجاح!")
            except Exception as e:
                st.error(f"خطأ أثناء الكتابة في الشيت: {e}")
