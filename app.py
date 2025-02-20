import streamlit as st
import pandas as pd
import os 
from io import BytesIO

st.set_page_config(page_title="💿Data Sweeper", layout='wide')

# Styles
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# set up
st.title("💿Data Sweeper")
st.write("Transform Your files between CSV and Excel formats with built-in data cleaning and visualizaion!")

upload_files = st.file_uploader("Upload your files (CSV or Excel):", type=["CSV", "xlsx"], accept_multiple_files=True)

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()


        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file format. Please upload a CSV or Excel file:{file_ext}")
            continue

        # Display info about the file
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Type:** {file_ext}")
        st.write(f"**File Size:** {file.size/1024} bytes")

        # Show 5 rows of the df
        st.write("Preview the Head of the Dataframe:")
        st.dataframe(df.head())

        # Options for data cleaning
        st.subheader("🛠 Data Cleaning Options:")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Filled!")


        # Choose specific columns to keep or convert
        st.subheader("🎯 Select Columns to Keep or Convert:")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        #  Visualization chart
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])


        # Convert the File => CSV or Excel
        st.subheader("🔃 Conversion Options:")
        conversion_type = st.radio(f"Conver {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download the file
            st.download_button(
                label=f"🔽 Click here to download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )

st.success("🎉All Files Processed!")

                