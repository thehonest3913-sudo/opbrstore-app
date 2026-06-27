import streamlit as st
import gspread
import json

def get_worksheet():
    try:
        # قراءة البيانات من الـ Secrets
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(dict(creds_dict))
        
        # التأكد من الـ ID (انسخه مرة أخرى من الرابط للتأكد)
        spreadsheet_id = '1KqtT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        
        # محاولة فتح الشيت
        sh = gc.open_by_key(spreadsheet_id)
        return sh.sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        return "خطأ: الملف غير موجود! تأكد من الـ ID ومن أنك شاركت الملف مع إيميل الـ service account."
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
