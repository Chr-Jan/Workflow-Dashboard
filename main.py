import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import plotly.graph_objects as go  # pip install plotly
import pypyodbc as odbc  # pip install pypyodbc

DRIVER_NAME = "ODBC Driver 17 for SQL Server"
SERVER_NAME = "Your SQL server name"
DATABASE_NAME = "your database name"

connection_string = f"""
    DRIVER={{{DRIVER_NAME}}};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trusted_Connection=yes;
"""

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
def load_data(file=None):
    if file is not None:
        try:
            data = pd.read_excel(file)
            return data
        except Exception as e:
            st.error(f"Error loading Excel file: {e}")
            return None
    else:
        try:
            conn = odbc.connect(connection_string)
            query = "SELECT * FROM YourTableName"  # Replace 'YourTableName' with your actual table name
            data = pd.read_sql(query, conn)
            conn.close()
            return data
        except Exception as e:
            st.error(f"Error connecting to SQL database: {e}")
            return None

uploaded_data = st.sidebar.file_uploader("Choose a file to upload", type=["xlsx", "xls"])

if uploaded_data is not None:
    df = load_data(file=uploaded_data)
else:
    df = load_data()

if df is not None:
    st.subheader("Data")
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
    st.info("Upload a file to get started", icon="ℹ️")
