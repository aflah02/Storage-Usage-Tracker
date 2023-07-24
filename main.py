import streamlit as st
from st_aggrid import AgGrid, GridUpdateMode, GridOptionsBuilder, ColumnsAutoSizeMode
# Select a directory
import os
import subprocess
from pathlib import Path
import pandas as pd

# Add Page Config
st.set_page_config(
    page_title="Storage Usage Tracker",
    page_icon="📊",
    initial_sidebar_state="expanded",
)

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

st.title("Storage Usage Tracker")

if st.button("Select Folder"):
    folder_path = get_folder_path()

selections = st.multiselect("Show", ["Files", "Folders"], default=["Files", "Folders"])

show_only_files_ending_with = st.text_input("Show only files ending with (comma separated)", value="")
show_only_files_ending_with = [x.strip() for x in show_only_files_ending_with.split(",") if x.strip() != ""]
show_only_files_ending_with = [x.lower() for x in show_only_files_ending_with]

if 'Files' not in selections and 'Folders' not in selections:
    st.write("Please select at least one of Files/Folders")

if len(show_only_files_ending_with) > 0 and 'Files' not in selections:
    st.write("Please select Files in Show")

if folder_path and folder_path.strip() == "No Folder Selected":
    folder_path = None
    st.write("No Folder Selected")

if folder_path and os.path.isfile(folder_path):
    st.write("You selected a file, not a folder.")

if folder_path:
    folder_path = folder_path.strip()
    st.write("You selected: ", folder_path)
    data = []
    for f in os.listdir(folder_path):
        size = 0
        isFile = os.path.isfile(os.path.join(folder_path,f))
        if 'Files' not in selections and isFile:
            continue
        if 'Folders' not in selections and not isFile:
            continue
        if isFile and len(show_only_files_ending_with) > 0:
            if not f.lower().endswith(tuple(show_only_files_ending_with)):
                continue
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
    df = pd.DataFrame(data, columns=['Name', 'Size', 'isFile'])
    total_size = df['Size'].sum() if len(df) > 0 else 0
    df_display = df.copy()
    # if size is greater than 1 GB, convert to GB, if greater than 1 MB, convert to MB, else convert to KB
    df_display['Size'] = df_display['Size'].apply(lambda x: str(round(x/1024/1024/1024,2))+" GB" if x > 1024*1024*1024 else str(round(x/1024/1024,2))+" MB" if x > 1024*1024 else str(round(x/1024,2))+" KB")
    st.write("Files/Folders in the selected folder:")
    # if size is greater than 1 GB, convert to GB, if greater than 1 MB, convert to MB, else convert to KB
    total_size = str(round(total_size/1024/1024/1024,2))+" GB" if total_size > 1024*1024*1024 else str(round(total_size/1024/1024,2))+" MB" if total_size > 1024*1024 else str(round(total_size/1024,2))+" KB"
    st.write("Total Size:", total_size)
    # gb = GridOptionsBuilder.from_dataframe(df_display)
    # gb.configure_default_column(
    # flex=1,
    # )   
    # gridOptions = gb.build()
    AgGrid(df_display, update_mode=GridUpdateMode.SELECTION_CHANGED, columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)