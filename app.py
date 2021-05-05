# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 13:46:56 2021

@author: vipusinghal
"""

import streamlit as st
import pandas as pd
import os
import base64

st.title('Mails Information Extractor ')

data=[]
# import pdb;pdb.set_trace()
file = st.file_uploader("Upload Files",type=['txt','pdf','docs'])
if file is not None:
    st.write('You selected `%s`' % file.name)
    file=str(file.read(),"cp1252")
    
    file=file.split('\n')
    # file=open(file.name,'r')
    for line in file:
        line=line.strip()
        if line!='':
            data.append(line)
#     file_details = {"FileName":filename.name,"FileType":filename.type,"FileSize":filename.size}
#     st.write(file_details)
     
def file_selector(folder_path='.'):
    filenames = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

# filename = file_selector()
# st.write('You selected `%s`' % filename.name)

# file=str(file.read(),"utf-8")
    
# file=file.split('\n')
# print(file)
# file=open(filename.name,'r')


# for line in file:
#     line=line.strip()
#     if line!='':
#         data.append(line)
# print(data)
extracted_data=[]
for i in range(len(data)):#line in file:
    if 'From:	Deloitte Meeting & Event Services' in data[i]:
        j=i+1
        temp=0
        while True:
            j=j+1
            # print('j:',j)
            if 'From:' in data[j] and 'Deloitte Meeting & Event Services' not in data[j] and temp==0:
                temp=1
                # print(data[j])
                try:
                    mail=data[j].split(': ')[1]
                    name=mail.split('<')[0].strip()
                    email=mail.split('<')[1].strip('>').strip()
                    # print(mail)
                except:
                    mail=''
            if 'Sent:' in data[j]:
                # print(data[j])
                try:
                    date=data[j].split(': ')[1]
                    # print(date)
                except:
                    date=''
            if 'Subject: [EXT]' in data[j]:
                # print(data[j+1])
                msg=''
                k=j
                while True:
                    k=k+1
                    if 'From:	Deloitte Meeting & Event Services' in data[k]:
                        break
                    if k>=len(data)-1:
                        msg=msg+data[k]
                        break
                    msg=msg+data[k]
                    
                # print(msg)
            if 'From:	Deloitte Meeting & Event Services' in data[j] or j>=len(data)-1:
                # print()
                try:
                    lst=[name,email,date,msg[:1000]]
                    extracted_data.append(lst)
                except:
                    lst=[name,email,date,'']
                    extracted_data.append(lst)
                break

df = pd.DataFrame(extracted_data, columns=["Name","Email", "Date and Time", "Body"])

st.write('Total Emails:', df.shape[0])
if st.checkbox('Show Data'):
    st.write(df)
    
def download_link(object_to_download, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')

    """
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # some strings <-> bytes conversions necessary here
    b64 = base64.b64encode(object_to_download.encode()).decode()

    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

# st.markdown(download_link(df), unsafe_allow_html=True)
    
if st.button('Download Data as CSV'):
    tmp_download_link = download_link(df, 'output.csv', 'Click here to download your data!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)