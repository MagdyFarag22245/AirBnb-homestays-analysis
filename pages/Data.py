# importing libraries
import pandas as pd
import streamlit as st
from zipfile import ZipFile



zip_file_path = "D:\Study\Epsilon DS\Bnb_project\sources\Airbnb_Open_Data.zip"
with ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall()
extracted_files = zip_ref.namelist()
csv_file_name = extracted_files[0] 
df = pd.read_csv(csv_file_name)
# Title
st.markdown(" <center>  <h1> AirBnb Dataset </h1> </font> </center> </h1> ",
            unsafe_allow_html=True)


# Link of Data
st.markdown('<a href="https://www.kaggle.com/datasets/arianazmoudeh/airbnbopendata/data"> <center> Link to Dataset  </center> </a> ', unsafe_allow_html=True)

# Show data
st.write(df)