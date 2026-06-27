import streamlit as st
import gspread

# إعداد الصفحة
st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

# دالة الاتصال
def get_worksheet():
    try:
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(dict(creds_dict))
        spreadsheet_id = '1KqtxT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        return sh.sheet1
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

# واجهة الإدخال
name = st.text_input("اسم المنتج")
price = st.text_input("السعر")

# زر الإضافة
if st.button("إضافة للمخزون"):
    if not name or not price:
        st.error("يرجى إدخال البيانات!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(ws)
        else:
            try:
                # [السعر في A، فراغ في B، الاسم في C]
                ws.append_row([str(price), "", str(name)])
                st.success(f"تمت إضافة {name} بنجاح!")
            except Exception as e:
                st.error(f"خطأ أثناء الكتابة: {e}")

# زر عرض المخزون
if st.button("عرض المخزون"):
    ws = get_worksheet()
    if isinstance(ws, str):
        st.error(ws)
    else:
        try:
            data = ws.get_all_values()
            if len(data) <= 1:
                st.warning("المخزون فارغ.")
            else:
                # عرض البيانات في جدول
                st.table(data)
        except Exception as e:
            st.error(f"خطأ أثناء جلب البيانات: {e}")
