import pandas as pd # pip install pandas openpyxl
import streamlit as st # pip install streamlit
import plotly.graph_objects as go # pip install plotly

# Set Streamlit page configuration
# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/

st.set_page_config(
    page_title="Data",
    page_icon=":chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Data")
st.markdown("Data is being shown")

@st.cache_data
def load_data(file):
    try:
        data = pd.read_excel(file)
        return data
    except Exception as e:
        st.error(f"An error occurred: {e}")

uploaded_data = st.sidebar.file_uploader("Choose a file to upload", type=["xlsx", "xls"])

if uploaded_data is not None:
    if uploaded_data.name.split('.')[-1] in ['xlsx', 'xls']:
        df = load_data(uploaded_data)
        if df is not None:
            
            # Example Plotly Visualization (Chart)            
            st.subheader("Chart")
            st.dataframe(df)
            
            # Example Plotly Visualization (Bar Chart)
            st.subheader("Bar Chart")
            fig = go.Figure(data=[go.Bar(x=df[df.columns[1]], y=df[df.columns[4]], marker_color='royalblue')])
            fig.update_layout(title='Bar Chart', xaxis_title='X-axis', yaxis_title='Y-axis')
            st.plotly_chart(fig)

            # Example Plotly Visualization (Line Chart)
            st.subheader("Line Chart")
            fig = go.Figure(data=[go.Scatter(x=df[df.columns[1]], y=df[df.columns[0]], mode='lines+markers')])
            fig.update_layout(title='Line Chart', xaxis_title='X-axis', yaxis_title='Y-axis')
            st.plotly_chart(fig)

            # Example Plotly Visualization (3D Scatter Plot)
            st.subheader("3D Scatter Plot")
            fig = go.Figure(data=[go.Scatter3d(x=df[df.columns[0]], y=df[df.columns[1]], z=df[df.columns[2]], mode='markers')])
            fig.update_layout(title='3D Scatter Plot', scene=dict(xaxis=dict(title=df.columns[0]), yaxis=dict(title=df.columns[1]), zaxis=dict(title=df.columns[2])))
            st.plotly_chart(fig)

    else:
        st.error("Unsupported file type. Please upload an Excel file (.xlsx or .xls).")
else:
    st.info("Upload a file to get started", icon="ℹ️")