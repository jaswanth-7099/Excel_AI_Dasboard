import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Dark theme for Seaborn/Matplotlib
plt.style.use("dark_background")
sns.set_palette("bright")

# Page setup
st.set_page_config(page_title="Excel AI Dashboard", layout="wide")

st.markdown("<h1 style='color:#00FFAA;'>📊 Excel AI Dashboard</h1>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("📤 Upload CSV or Excel", type=["csv", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.markdown("### 🧾 Data Preview")
    st.dataframe(df.head())

    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if len(numeric_cols) >= 2:
        st.markdown("### 📊 Chart Generator")

        col1, col2, col3 = st.columns(3)
        with col1:
            chart_type = st.selectbox("Choose Chart Type", ["Bar", "Line", "Scatter", "Heatmap"])
        with col2:
            x_axis = st.selectbox("Select X-axis", numeric_cols, index=0)
        with col3:
            y_axis = st.selectbox("Select Y-axis", numeric_cols, index=1)

        fig, ax = plt.subplots(figsize=(10, 5))
        
        if chart_type == "Bar":
            sns.barplot(data=df, x=x_axis, y=y_axis, ax=ax)
        elif chart_type == "Line":
            sns.lineplot(data=df, x=x_axis, y=y_axis, ax=ax)
        elif chart_type == "Scatter":
            sns.scatterplot(data=df, x=x_axis, y=y_axis, ax=ax)
        elif chart_type == "Heatmap":
            corr = df[numeric_cols].corr()
            sns.heatmap(corr, annot=True, cmap="viridis", ax=ax)

        ax.set_title(f"{chart_type} Plot: {x_axis} vs {y_axis}", color='cyan')
        st.pyplot(fig)

        st.markdown("### 📈 Summary Stats")
        st.write(df[numeric_cols].describe().style.background_gradient(cmap='viridis'))

    else:
        st.warning("⚠️ At least 2 numeric columns required for visualization.")

else:
    st.info("📁 Upload a dataset to get started.")
