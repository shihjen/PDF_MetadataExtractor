# Import Modules
import os
import json
import pandas as pd
import numpy as np
import streamlit as st
import streamlit_lottie as st_lottie
from pypdf import PdfReader

# Helper Function To Extract Metadata
def get_meta(file):
    reader = PdfReader(file)
    meta = reader.metadata

    return {'File_Name':file.name,
            'Size (bytes)': file.size,
            'Title':meta.title,
            'Author':meta.author,
            'Subject':meta.subject,
            'Creator':meta.creator,
            'Producer':meta.producer,
            'Creation_Date':meta.creation_date,
            'Modification_Date':meta.modification_date}

# Helper Function To Convert Pandas Dataframe Into CSV File
@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# Steamlit Page Configuration
st.set_page_config(page_title = 'PDF Metadata Extractor',
                   page_icon = None,
                   layout = 'centered',
                   initial_sidebar_state = 'auto')

# Application Title
st.title('PDF Metadata Extractor')

# Lottie Animation
with open('assets/images/lottie_cover.json','r') as f:
    lottie_cover = json.load(f)

st.lottie(lottie_cover, speed=0.5, reverse=False, loop=True, quality='low', height=500)

# Application Description
multi = '''
Welcome to the PDF Metadata Extractor! 
This user-friendly web application is designed to help you efficiently extract and manage metadata from your PDF files. 
Metadata plays a crucial role in organizing and categorizing documents, making it easier to retrieve and utilize information effectively.
'''
st.markdown(multi)

# Initialize the 'csv' variable
csv = None

# Streamlit UI - File Uploader
with st.form('my_form', clear_on_submit=True):
    uploaded_files = st.file_uploader(label='Upload PDF files', accept_multiple_files=True, type=['.pdf'], label_visibility='hidden')
    submitted = st.form_submit_button('Extract Metadata')

    if submitted:
        if not uploaded_files:
            st.warning('Please Upload PDF Files.')
        else:
            try:
                cont = []
                for file in uploaded_files:
                    cont.append(get_meta(file))

                # Remove the Timezone for the DateTime Data
                df = pd.DataFrame(cont)
                df['Creation_Date'] = pd.to_datetime(df['Creation_Date'], utc=True).dt.tz_localize(None)
                df['Modification_Date'] = pd.to_datetime(df['Modification_Date'], utc=True).dt.tz_localize(None)

                csv = convert_df(df)

            except Exception as e:
                st.write(f'Unexpected Error Occured: {e}')

# Streamlit UI - Download Button
if csv:
    st.download_button(
        label = 'Download Data As CSV',
        data = csv,
        file_name = 'Metadata.csv',
        mime = 'text/csv'
    )



