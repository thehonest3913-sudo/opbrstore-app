import streamlit as st
import gspread

# 1. إعداد الصفحة
st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

# 2. دالة الاتصال
def get_worksheet():
    try:
        # قراءة البيانات من القسم gcp_service_account
        creds_dict = st.secrets["gcp_service_account"]
        gc = gspread.service_account_from_dict(creds_dict)
        spreadsheet_id = '1KqtT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
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
        st.error("يرجى التأكد من إدخال اسم المنتج والسعر!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(ws) # عرض رسالة الخطأ في حال وجودها
        else:
            try:
                ws.append_row([price, "", name])
                st.success(f"تمت إضافة {name} بسعر {price} بنجاح!")
            except Exception as e:
                st.error(f"خطأ أثناء الإضافة للشيت: {e}")

# 5. عرض المنتجات
if st.button("تحديث وعرض المخزون"):
    ws = get_worksheet()
    if isinstance(ws, str):
        st.error(ws)
    else:
        data = ws.get_all_values()
        st.table(data)
