import joblib
import numpy as np
import streamlit as st

st.set_page_config(page_title="Linear Regression Predictor", page_icon="📈")

# تحميل الموديل مرة واحدة وتخزينه في الكاش
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()
n_features = getattr(model, "n_features_in_", 12)

st.title("📈 Linear Regression - واجهة التنبؤ")
st.write(f"الموديل ده مدرّب على **{n_features}** فيتشر. دخّل القيم تحت واضغط تنبؤ.")

# نعمل input لكل فيتشر
cols = st.columns(3)
values = []
for i in range(n_features):
    col = cols[i % 3]
    val = col.number_input(f"Feature {i + 1}", value=0.0, format="%.4f")
    values.append(val)

if st.button("تنبأ", type="primary"):
    X = np.array(values).reshape(1, -1)
    prediction = model.predict(X)[0]
    st.success(f"القيمة المتوقعة: **{prediction:.4f}**")

with st.expander("أو ارفع القيم كـ CSV/JSON"):
    raw = st.text_area("اكتب الفيتشرز مفصولة بفاصلة (comma)، بنفس الترتيب", "")
    if st.button("تنبأ من النص"):
        try:
            nums = [float(x.strip()) for x in raw.split(",") if x.strip() != ""]
            if len(nums) != n_features:
                st.error(f"لازم بالظبط {n_features} قيمة، انت بعت {len(nums)}")
            else:
                pred = model.predict(np.array(nums).reshape(1, -1))[0]
                st.success(f"القيمة المتوقعة: **{pred:.4f}**")
        except ValueError:
            st.error("تأكد إن كل القيم أرقام صحيحة")
