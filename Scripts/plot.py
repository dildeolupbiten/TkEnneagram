# -*- coding: utf-8 -*-

from .entry import EntryFrame
from .enneagram import Enneagram
from .constants import HOUSE_SYSTEMS
from .modules import (
    np, pd, td, tk, plt, FigureCanvasTkAgg, NavigationToolbar2Tk
)


class Plot(tk.Toplevel):
    def __init__(self, info, jd, hsys, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.date = pd.to_datetime(jd, unit="D", origin="julian")
        self.title(info["Name"])
        self.left_frame = tk.Frame(master=self)
        self.left_frame.pack(side="left", fill="both")
        self.right_frame = tk.Frame(master=self)
        self.right_frame.pack(side="left")
        self.figure = plt.Figure()
        self.canvas = FigureCanvasTkAgg(
            figure=self.figure,
            master=self.right_frame
        )
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.navbar = NavigationToolbar2Tk(
            canvas=self.canvas,
            window=self.right_frame
        )
        self.date_frame = tk.Frame(master=self.left_frame)
        self.date_frame.pack()
        self.create_label(
            text="Local",
            date=f"{info['Date']} {info['Time']}",
            row=0
        )
        self.create_label(
            text="UTC",
            date=self.date.strftime("%d.%m.%Y %H:%M"),
            row=1
        )
        self.backward = EntryFrame(
            master=self.left_frame,
            texts=["Time Interval (min)", "Number of Intervals"],
            title="Backward (From UTC)",
            position="vertical",
            color="black"
        )
        self.backward.pack()
        self.forward = EntryFrame(
            master=self.left_frame,
            texts=["Time Interval (min)", "Number of Intervals"],
            title="Forward (From UTC)",
            position="vertical",
            color="black"
        )
        self.forward.pack()
        self.plot_button = tk.Button(
            master=self.left_frame,
            text="Plot",
            command=lambda: self.command(
                info=info,
                hsys=hsys,
                title=""
            )
        )
        self.plot_button.pack()

    def create_label(self, text, date, row):
        label = tk.Label(master=self.date_frame, text=text, fg="red")
        label.grid(row=row, column=0, sticky="w")
        value = tk.Label(master=self.date_frame, text=date)
        value.grid(row=row, column=1, sticky="w")

    def binom_graph(self, x, y, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(x, y)
        y = sorted(list(set(y)))
        self.figure.legend(*ax.get_legend_handles_labels())
        self.figure.gca().set_xlabel("Hour")
        self.figure.gca().set_xticks(x)
        self.figure.gca().set_xticklabels(
            [i.strftime("%H:%M") for i in x]
        )
        self.figure.gca().set_ylabel("Enneagram Type")
        self.figure.gca().set_yticks(y)
        self.figure.gca().set_yticklabels([f"Type-{i}" for i in y])
        for label in ax.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_fontsize(8)
            if label.get_text() == self.date.strftime("%H:%M"):
                label.set_color("red")
        self.figure.gca().set_title(title)
        self.figure.subplots_adjust(
            left=0.2,
            bottom=0.4,
            right=0.9,
            top=0.9,
            wspace=0.2,
            hspace=0
        )
        self.canvas.draw()

    def command(self, info, hsys, title):
        dates = self.get_dates(widget=self.backward, multiply=-1)
        dates += [self.date]
        dates += self.get_dates(widget=self.forward, multiply=1)
        y = []
        x = []
        for date in dates:
            result = Enneagram(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=date.hour,
                minute=date.minute,
                second=date.second,
                lat=float(info["Latitude"]),
                lon=float(info["Longitude"]),
                hsys=HOUSE_SYSTEMS[hsys],
                utc=True
            )
            result = result.get_all_scores()
            total = []
            for i in ["sign", "house"]:
                for k, v in result[i].items():
                    if k in ["Dayscores", "Effect of Houses"]:
                        total.append(np.array([*v.values()][:-1]))
            total = [round(float(i), 2) for i in total[0] * total[1]]
            x += [date]
            y += [total.index(max(total)) + 1]
        self.binom_graph(x=sorted(x), y=y, title=title)

    def get_dates(self, widget, multiply):
        time_interval = widget.widgets["Time Interval (min)"].get()
        number_of_intervals = widget.widgets["Number of Intervals"].get()
        if all([time_interval, number_of_intervals]):
            time_interval = int(time_interval) * multiply
            number_of_intervals = int(number_of_intervals)
            return [
                self.date + td(minutes=time_interval * (i + 1))
                for i in range(number_of_intervals)
            ]
        else:
            return []
