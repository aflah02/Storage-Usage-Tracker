# Storage Usage Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![File Size Tracker](app_screenshot.png)

The File Size Tracker is a simple Streamlit app that provides details for the sizes of all files and folders inside a specified directory. With this app, you can quickly get an overview of the space occupied by different files and subdirectories in a specific folder.

I went ahead and built this simple web app as the detail view in Windows File Explorer kinda sucks 😣

## Getting Started

### Installation

1. Clone this repository to your local machine.
2. Ensure you have Python installed (Python 3.6 or later).
3. Install the required dependencies by running the following command:

```
pip install -r requirements.txt
```

### Usage

1. Navigate to the directory where you have cloned the repository.
2. Run the Streamlit app by executing the following command:

```
streamlit run main.py
```

3. The app will open in your default web browser.

### Instructions

1. Upon opening the app, you will see a button on clicking which you can choose the directory you want to analyze.
2. You can also choose whether to show only files or only folders, or both.
3. Optionally you can also decide to filter files based on a specific extension.
4. The app will display a table listing all files and folders within the specified directory, along with their respective sizes in a human-readable format (e.g., KB, MB, GB).
5. The total size of the directory will also be shown at the top of the table.

## Contributing

If you find any issues or have suggestions to improve the File Size Tracker app, please feel free to open an issue or submit a pull request in this repository. Your contributions are highly appreciated!

## License

This project is licensed under the MIT License - see the [LICENSE](https://opensource.org/license/mit/) file for details.
---
