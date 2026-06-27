import streamlit as st
import gspread

# 1. إعداد الصفحة
st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

# 2. دالة الاتصال
def get_worksheet():
    try:
        creds_dict = st.secrets["gcp"]
        gc = gspread.service_account_from_dict(dict(creds_dict))
        spreadsheet_id = '1KqtxT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        return sh.sheet1
    except Exception as e:
        return f"خطأ في الاتصال: {e}"

# 3. واجهة الإدخال
name = st.text_input("اسم المنتج")
price = st.text_input("السعر")

# 4. زر الإضافة (بالمنطق الجديد)
if st.button("إضافة للمخزون"):
    if not name or not price:
        st.error("يرجى إدخال البيانات!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(ws)
        else:
            try:
                # البحث عن أول صف فارغ في العمود A
                col_a_values = ws.col_values(1)
                next_row = len(col_a_values) + 1
                
                # إجبار الكود على البدء من الصف الثالث إذا كان الجدول فارغاً
                if next_row < 3:
                    next_row = 3
                
                # الكتابة بدقة
                ws.update_cell(next_row, 1, str(price)) # السعر في العمود A
                ws.update_cell(next_row, 2, "")         # العمود B فارغ
                ws.update_cell(next_row, 3, str(name))  # الاسم في العمود C
                
                st.success(f"تمت الإضافة في الصف {next_row} بنجاح!")
            except Exception as e:
                st.error(f"خطأ أثناء الكتابة: {e}")

# 5. زر عرض المخزون (يعرض بدءاً من الصف الثالث)
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
                # عرض البيانات بدءاً من الصف الثالث (فهرس 2)
                st.table(data[2:]) 
        except Exception as e:
            st.error(f"خطأ أثناء جلب البيانات: {e}")
