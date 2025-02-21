import sys
import threading
import datetime
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
    QButtonGroup, QPushButton, QSystemTrayIcon, QMenu, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QFont
from tracker import Tracker
from mpl_canvas import MplCanvas
from data_queries import get_weekly_data, get_daily_data, get_daily_app_usage, get_weekly_app_usage
import qdarktheme

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        qdarktheme.setup_theme() # Apply the dark theme to the app

        self.setWindowTitle("Screen Time Tracker")
        self.setWindowIcon(QIcon("screen_time_icon.png"))
        self.setGeometry(100, 100, 800, 600)

        self.tracker = Tracker()
        self.selected_date = None
        self.weekly_days = None

        self.init_ui()
        self.create_tray_icon()
        self.setup_timer()
        self.start_tracking()


    def init_ui(self):
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()

        # Create a segmented control with two mutually exclusive buttons
        button_layout = self.create_buttons()
        self.main_layout.addLayout(button_layout)

        # Create a canvas to display the bar chart
        self.canvas = MplCanvas(self)
        self.main_layout.addWidget(self.canvas)

        # Create labels to display the total and average usage times
        self.total_label = QLabel()
        self.average_label = QLabel()

        self.total_label.setAlignment(Qt.AlignCenter)
        self.average_label.setAlignment(Qt.AlignCenter)
        self.total_label.setFont(QFont("Inter", 18))
        self.average_label.setFont(QFont("Inter", 18))

        label_layout = QHBoxLayout()
        label_layout.addWidget(self.total_label)
        label_layout.addWidget(self.average_label)

        self.main_layout.addLayout(label_layout)

        # Create a table to display usage times for each app
        self.table = QTableWidget()
        self.table.setFont(QFont("Inter", 12))
        self.table.setStyleSheet("QTableWidget { background-color: rgba(0, 0, 0, 0); }")
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["App Name", "Usage Time"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.main_layout.addWidget(self.table)

        # Exit button to stop tracking and close the app
        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_app)
        self.main_layout.addWidget(self.exit_button)

        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        self.refresh_ui()

    # Refresh the plot, table, and text details based on the selected view (daily or weekly)
    def refresh_ui(self):
        if self.daily_button.isChecked():
            # Daily view. Default to today's date if no date is selected
            if not self.selected_date:
                self.selected_date = datetime.date.today().isoformat()

            x_data, y_data = get_daily_data(self.selected_date)
            app_data = get_daily_app_usage(self.selected_date)
            total_time = sum(y_data) # In daily view, y_data is in minutes.

            self.canvas.plot_daily_bar(x_data, y_data, self.selected_date)
        else:
            # Weekly view
            self.selected_date = None
            x_data, y_data = get_weekly_data()
            app_data = get_weekly_app_usage()
                
            self.bars = self.canvas.plot_weekly_bar(x_data, y_data)

            # Save the weekly days for later use
            if not self.weekly_days:
                self.weekly_days = x_data
                self.canvas.mpl_connect("pick_event", self.on_bar_pick) # Make bars clickable.

            total_time = sum(y_data) * 60 # In weekly view, y_data is in hours. This converts it to minutes.

        # Calculate the average usage time without counting days/hours with 0 activity.
        non_zero = [v for v in y_data if v > 0] 
        average_time = total_time / len(non_zero) if non_zero else 0

        # Update the total and average labels
        self.total_label.setText(f"Total: <span style='color:DeepSkyBlue;'>{total_time // 60:.0f}h {total_time % 60:02.0f}m</span>")
        self.average_label.setText(f"Average: <span style='color:DeepSkyBlue;'>{average_time // 60:.0f}h {average_time % 60:02.0f}m</span>")
        
        # Update the table with the app usage data
        self.table.setRowCount(0)
        for row, (app_name, minutes) in enumerate(app_data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(app_name))
            self.table.setItem(row, 1, QTableWidgetItem(f"{minutes // 60:.0f}h {minutes % 60:02.0f}m"))


    def start_tracking(self):
        # Start tracking in a separate thread
        tracking_thread = threading.Thread(target=self.tracker.start_tracking, daemon=True)
        tracking_thread.start()


    def create_buttons(self):
        self.button_group = QButtonGroup()
        self.button_group.buttonClicked.connect(self.refresh_ui)
        button_font = QFont("Inter", 10)

        button_layout = QHBoxLayout()
        
        self.weekly_button = QPushButton("Weekly")
        self.weekly_button.setCheckable(True)
        self.weekly_button.setChecked(True)

        self.daily_button = QPushButton("Daily")
        self.daily_button.setCheckable(True)

        self.weekly_button.setFont(button_font)
        self.daily_button.setFont(button_font)
        
        self.button_group.addButton(self.weekly_button)
        self.button_group.addButton(self.daily_button)

        button_layout.addWidget(self.weekly_button)
        button_layout.addWidget(self.daily_button)

        return button_layout


    def setup_timer(self):
        # Update the plot and details every 3 seconds
        self.timer = QTimer(self)
        self.timer.setInterval(3000)
        self.timer.timeout.connect(self.refresh_ui)
        self.timer.start()    

    # Handle the event when the user picks a bar in the weekly view.
    def on_bar_pick(self, event):
        # Find the index of the selected bar and get the corresponding date.
        index = list(self.bars).index(event.artist)
        self.selected_date = self.weekly_days[index]
        
        self.daily_button.setChecked(True)
        self.refresh_ui()


    def create_tray_icon(self):
        self.tray_icon = QSystemTrayIcon(QIcon('screen_time_icon.png'), self)
        self.tray_icon.setVisible(True)

        tray_menu = QMenu()
        show_action = tray_menu.addAction("Show")
        show_action.triggered.connect(self.show)

        quit_action = tray_menu.addAction("Exit")
        quit_action.triggered.connect(self.exit_app)

        self.tray_icon.setContextMenu(tray_menu)


    def closeEvent(self, event):
        # Override the close event to hide the window instead of exiting.
        event.ignore()
        self.hide()


    def exit_app(self):
        self.tracker.stop_tracking()
        self.timer.stop()
        self.tray_icon.hide()
        sys.exit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
