# Screen Time Tracker

A desktop application written in Python that monitors and logs your screen time on Windows. It uses PyQt5 for the graphical user interface, Matplotlib for interactive data visualizations, and SQLite for persistent logging. The application runs in the background, minimizes to the system tray, and displays detailed usage statistics.

## Features

- **Real-Time Tracking:**\
  Detects and logs the active foreground application using Windows APIs (`win32gui`, `win32process`, `psutil`).

- **Data Logging:**\
  Records session data (start time, end time, duration, process name) into an SQLite database.

- **Interactive Visualizations:**

  - **Weekly View:**\
    Displays a bar chart showing daily usage (in hours) for the past week, with days labeled as Sun, Mon, Tue, etc.\
    Click on any bar to switch to an hourly view for that day.
  - **Daily View:**\
    Shows a bar chart with hourly usage (in minutes) for a selected day.

- **Top Apps Usage:**\
  Presents a table of your most-used applications along with their usage times.

- **System Tray Integration:**\
  When closed, the application minimizes to the system tray to continue tracking in the background.

## Installation

### Requirements

- Python 3.8+
- [PyQt5](https://pypi.org/project/PyQt5/)
- [Matplotlib](https://pypi.org/project/matplotlib/)
- [psutil](https://pypi.org/project/psutil/)
- [pywin32](https://pypi.org/project/pywin32/)
- [qdarktheme](https://pypi.org/project/pyqtdarktheme/)

### Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/ElNagar-Youssef/screen-time-tracker.git
   cd screen-time-tracker
   ```

2. **Create a Virtual Environment (optional):**

   ```bash
   python -m venv venv
   # Activate the virtual environment:
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install PyQt5 matplotlib psutil pywin32 qdarktheme
   ```

## Usage

Run the application by executing:

```bash
python main.py
```

- **Weekly View:**\
  The app opens in weekly view by default, displaying a bar chart for the past week.\
  Clicking a bar will switch to the daily (hourly) view for that day.

- **Daily View:**\
  The daily view shows a breakdown of screen time per hour for the selected day.

- **System Tray:**\
  Clicking the close ("X") button minimizes the application to the system tray.\
  Right-click the tray icon to restore or quit the application.

- **Quit:**\
  Use the tray icon's "Quit" option or the Quit button in the main window to stop tracking and exit the app.

## Project Structure

```
screen-time-tracker/
├── main.py              # Main application entry point (UI, plotting, etc.)
├── tracker.py           # Screen time tracking logic (Windows-specific)
├── database.py          # SQLite database handling (initialization, logging)
├── data_queries.py      # Functions for aggregating logged data
├── mpl_canvas.py        # Custom Matplotlib canvas for embedding graphs in PyQt5
└── README.md            # Project documentation
```
