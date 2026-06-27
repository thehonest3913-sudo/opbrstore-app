import streamlit as st
import gspread

# 1. إعداد واجهة البرنامج
st.set_page_config(page_title="مخزني", page_icon="📦")
st.title("📦 لوحة تحكم Opbrstore")

# 2. دالة الاتصال (تستخدم الـ Secrets التي حفظناها)
def get_worksheet():
    try:
        # قراءة البيانات من الـ Secrets
        creds_dict = st.secrets["gcp_service_account"]
        gc = gspread.service_account_from_dict(creds_dict)
        
        # فتح الشيت بالـ ID الخاص بك
        spreadsheet_id = '1KqtT9GcNs1Zb4UJ6pT00kDLYsKDyi_cWf3wqfxRB1w'
        sh = gc.open_by_key(spreadsheet_id)
        
        # اختيار الورقة الأولى (تأكد أنك سميتها Sheet1 أو غيرها)
        return sh.sheet1 
    except Exception as e:
        return str(e)

# 3. واجهة الإدخال
name = st.text_input("اسم المنتج")
price = st.number_input("السعر", min_value=0.0)

# 4. زر الإضافة
if st.button("إضافة للمخزون"):
    if not name:
        st.error("من فضلك اكتب اسم المنتج!")
    else:
        ws = get_worksheet()
        if isinstance(ws, str):
            st.error(f"خطأ في الاتصال بجوجل: {ws}")
        else:
            # إضافة الصف
            ws.append_row([name, price])
            st.success(f"تمت إضافة {name} بنجاح!")
            st.balloons() # احتفال صغير

# 5. عرض المنتجات الموجودة حالياً (للتأكد أن الإضافة تمت)
if st.button("تحديث وعرض المخزون"):
    ws = get_worksheet()
    if not isinstance(ws, str):
        data = ws.get_all_values()
        st.table(data)
