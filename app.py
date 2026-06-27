import streamlit as st
import gspread

# 1. إعداد الصفحة
st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

# 2. دالة الاتصال الموحدة
def get_worksheet():
    try:
        # قراءة المفاتيح من الـ Secrets
        creds_dict = st.secrets["gcp"]
        # الاتصال بجوجل شيت
        gc = gspread.service_account_from_dict(dict(creds_dict))
        # الـ ID الصحيح والمؤكد
        spreadsheet_id = '1KqtxT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        return sh.sheet1
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

# 3. واجهة الإدخال
name = st.text_input("اسم المنتج")
price = st.text_input("السعر")

# 4. زر الإضافة
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
                st.success(f"تمت إضافة {name} بسعر {price} بنجاح!")
            except Exception as e:
                st.error(f"خطأ أثناء الكتابة: {e}")

# 5. زر عرض المخزون
if st.button("عرض المخزون"):
    ws = get_worksheet()
    if isinstance(ws, str):
        st.error(ws)
    else:
        try:
            data = ws.get_all_values()
            if not data:
                st.warning("المخزون فارغ.")
            else:
                st.table(data)
        except Exception as e:
            st.error(f"خطأ أثناء جلب البيانات: {e}")
