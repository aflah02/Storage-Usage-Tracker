import tkinter as tk
from tkinter import filedialog

# Reference - https://github.com/streamlit/streamlit/issues/1019#issuecomment-1617476165

root = tk.Tk()
root.withdraw()
folder_path = filedialog.askdirectory()
if folder_path:
    print(folder_path)
    root.destroy()
else:
    print("no folder selected")
    root.destroy()

root.mainloop()