import streamlit as st
import gspread

# إعداد الصفحة
st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

def get_worksheet():
    try:
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(dict(creds_dict))
        spreadsheet_id = '1KqtxT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
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
            try:
                # الترتيب: [العمود A، العمود B (فارغ)، العمود C]
                ws.append_row([str(price), "", str(name)])
                st.success(f"تمت إضافة {name} في العمود C بنجاح!")
            except Exception as e:
                st.error(f"خطأ أثناء الكتابة: {e}")

# زر عرض المخزون (يعرض بدءاً من الصف الثالث)
if st.button("عرض المخزون"):
    ws = get_worksheet()
    if isinstance(ws, str):
        st.error(ws)
    else:
        try:
            data = ws.get_all_values()
            if len(data) < 3:
                st.warning("المخزون فارغ أو لم نصل للصف الثالث بعد.")
            else:
                # عرض البيانات بدءاً من الصف الثالث (الفهرس 2)
                st.table(data[2:]) 
        except Exception as e:
            st.error(f"خطأ أثناء جلب البيانات: {e}")
