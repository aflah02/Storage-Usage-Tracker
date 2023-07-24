import streamlit as st

# Select a directory
import os
import subprocess
from pathlib import Path
import pandas as pd

def get_folder_path():
    global folder_path
    path = os.path.abspath('lib')
    p = subprocess.Popen(['python3','tkDirSelector.py'], cwd=path,stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result, error = p.communicate()
    p.terminate()
    if isinstance(result,bytes):
        return result.decode('utf-8')
    if isinstance(result,str):
        return result
    else:
        return None

folder_path = None

st.title("Storage Usage Analyzer")

if st.button("Select Folder"):
    folder_path = get_folder_path()

if folder_path and os.path.isfile(folder_path):
    st.write("You selected a file, not a folder.")

if folder_path:
    folder_path = folder_path.strip()
    st.write("You selected: ", folder_path)
    data = []
    for f in os.listdir(folder_path):
        size = 0
        isFile = os.path.isfile(os.path.join(folder_path,f))
        if isFile:
            size = os.path.getsize(os.path.join(folder_path,f))
        else:
            size = sum(file.stat().st_size for file in Path(
                os.path.join(folder_path,f)
            ).rglob('*'))
        data.append(
            {
                "name": f,
                "size": size,
                "isFile": isFile
            }
        )
    # sort by size
    data = sorted(data, key=lambda k: k['size'], reverse=True)
    df = pd.DataFrame(data)
    total_size = df['size'].sum()
    # column names
    df.columns = ['Name', 'Size', 'isFile']
    # if size is greater than 1 GB, convert to GB, if greater than 1 MB, convert to MB, else convert to KB
    df['Size'] = df['Size'].apply(lambda x: str(round(x/1024/1024/1024,2))+" GB" if x > 1024*1024*1024 else str(round(x/1024/1024,2))+" MB" if x > 1024*1024 else str(round(x/1024,2))+" KB")
    st.write("Files/Folders in the selected folder:")
    # if size is greater than 1 GB, convert to GB, if greater than 1 MB, convert to MB, else convert to KB
    total_size = str(round(total_size/1024/1024/1024,2))+" GB" if total_size > 1024*1024*1024 else str(round(total_size/1024/1024,2))+" MB" if total_size > 1024*1024 else str(round(total_size/1024,2))+" KB"
    st.write("Total Size:", total_size)
    st.table(df)