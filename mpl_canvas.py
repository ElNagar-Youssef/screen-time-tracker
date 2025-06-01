import datetime
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from math import ceil


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=9, height=3, dpi=100, bgcolor = "#3b3b3b"):
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor=bgcolor)
        self.axes = self.fig.add_subplot(111, facecolor=bgcolor)
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)

        # Additional formatting options
        self.fig.tight_layout()
        self.axes.tick_params(axis='both', colors="white")

    def plot_weekly_bar(self, x, y):
        self.axes.clear()
        bars = self.axes.bar(x, y, align='center', picker=True)
        
        self.axes.set_title("This Week", color="white", fontsize=16)

        # Set the x-axis labels to display the days of the week
        self.axes.set_xticks(range(7))
        self.axes.set_xticklabels(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
        self.axes.set_xlim(-0.5, 6.5)

        # Set the y-axis labels to display the time in hours
        max_y = max(y) if y else 4
        self.axes.set_yticks(range(0, 25, 2), [f"{hour}h" for hour in range(0, 25, 2)])
        self.axes.set_ylim(0, ceil(max_y / 4) * 4) # Display time up to the nearest 6 hours.

        # Color the bar representing today in purple
        today = datetime.date.today().isoformat()
        for bar, date in zip(bars, x):
            if date == today:
                bar.set_color('MediumOrchid')

        self.axes.grid(True, which='both', axis='y', linestyle='--', linewidth=0.5)
        self.fig.tight_layout()
        self.draw()
        return bars

    # selected_date is a string in the format "YYYY-MM-DD"   
    def plot_daily_bar(self, x, y, selected_date):
        self.axes.clear()
        self.axes.bar(x, y, align='edge')

        # Set the title based on the selected date
        if selected_date == datetime.date.today().isoformat():
            self.axes.set_title(f"Today", color="DeepSkyBlue", fontsize=16)
        else:
            formatted_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").strftime("%b %d (%A)")
            self.axes.set_title(formatted_date, color="white", fontsize=16)
        
        self.axes.set_xticks(range(0, 24, 6), ["12 AM", "6 AM", "12 PM", "6 PM"])
        self.axes.set_xlim(0, 24)

        self.axes.set_yticks(range(0, 61, 15), ["0", "15m", "30m", "45m", "60m"])
        self.axes.set_ylim(0, 60)

        self.axes.grid(True, which='both', axis='both', linestyle='--', linewidth=0.5)
        self.fig.tight_layout()
        self.draw()
