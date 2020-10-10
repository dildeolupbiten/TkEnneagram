# -*- coding: utf-8 -*-

from .messagebox import MsgBox
from .modules import np, tk, ttk
from .spreadsheet import Spreadsheet
from .utilities import dd_to_dms, convert_degree
from .constants import HOUSE_SYSTEMS, SIGNS, PLANETS


class Treeview(ttk.Treeview):
    def __init__(
            self,
            columns,
            wide,
            values=None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.columns = columns
        if values:
            self.style = ttk.Style()
            self.style.configure("Treeeview.Cell", fieldbackground="red")
        else:
            self.x_scrollbar = tk.Scrollbar(
                master=self.master,
                orient="horizontal"
            )
            self.configure(
                xscrollcommand=self.x_scrollbar.set,
                height=5
            )
            self.x_scrollbar.configure(command=self.xview)
            self.x_scrollbar.pack(side="bottom", fill="x")
        self.y_scrollbar = tk.Scrollbar(
            master=self.master,
            orient="vertical"
        )
        self.configure(
            yscrollcommand=self.y_scrollbar.set,
            style="Treeview"
        )
        self.y_scrollbar.configure(command=self.yview)
        self.y_scrollbar.pack(side="right", fill="y")
        self.configure(
            show="headings",
            columns=[f"#{i + 1}" for i in range(len(self.columns))],
            height=10 if not wide else 20,
            selectmode="extended"
        )
        self.pack(side="left", expand=True, fill="both")
        for index, column in enumerate(self.columns):
            if values:
                if index == 0:
                    width = 200
                    anchor = "w"
                else:
                    width = 75
                    anchor = "center"
            else:
                width = 125
                anchor = "center"
            self.column(
                column=f"#{index + 1}",
                minwidth=75,
                width=width,
                anchor=anchor,
            )
            self._heading(col=index, text=column, values=values)
        self.bind(
            sequence="<Control-a>",
            func=lambda event: self.select_all()
        )
        self.bind(
            sequence="<Control-A>",
            func=lambda event: self.select_all()
        )
        if values:
            self.insert_values(values)

    def _heading(self, col, text, values):
        if values:
            self.heading(column=f"#{col + 1}", text=text)
        else:
            self.heading(
                column=f"#{col + 1}",
                text=text,
                command=lambda: self.sort(col=col, reverse=False)
            )

    def sort(self, col: int, reverse: bool):
        column = [
            (self.set(k, col), k)
            for k in self.get_children("")
        ]
        try:
            column.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            column.sort(reverse=reverse)
        for index, (val, k) in enumerate(column):
            self.move(k, "", index)
        self.heading(
            column=col,
            command=lambda: self.sort(col=col, reverse=not reverse)
        )

    def select_all(self):
        for child in self.get_children():
            self.selection_add(child)

    def insert_values(self, values):
        count = 0
        total = []
        for i in ["sign", "house"]:
            for k, v in values[i].items():
                if k in ["Dayscores", "Effect of Houses"]:
                    total.append(np.array([*v.values()][:-1]))
                    self.insert(
                        parent="",
                        index=count,
                        value=[k, *v.values()],
                        tags=("total",)
                    )
                    self.tag_configure('total', foreground="red")
                else:
                    self.insert(
                        parent="",
                        index=count,
                        value=[k, *v.values()]
                    )
                count += 1
        total = [round(float(i), 2) for i in total[0] * total[1]]
        total += [round(sum(total), 2)]
        arr = ["Total Scores"]
        arr += total
        self.insert(
            parent="",
            index=count,
            value=arr,
            tags=("last", )
        )
        self.tag_configure('last', foreground="blue")


class TreeviewToplevel(tk.Toplevel):
    def __init__(
            self,
            values,
            info,
            hsys,
            icons,
            patterns,
            algorithm,
            wide=False,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title("Enneagram Scores")
        self.hsys = {v: k for k, v in HOUSE_SYSTEMS.items()}[hsys]
        self.resizable(width=False, height=False)
        self.top_frame = tk.Frame(master=self)
        self.top_frame.pack(fill="both")
        self.info_frame = tk.Frame(master=self.top_frame)
        self.info_frame.pack(fill="both", side="left")
        self.pattern_frame = tk.Frame(master=self.top_frame)
        self.pattern_frame.pack(fill="both", side="left", padx=100)
        self.treeview_frame = tk.Frame(master=self)
        self.treeview_frame.pack(fill="both")
        self.columns = ["Category"] + \
                       [f"Type-{i}" for i in range(1, 10)] + \
                       ["Total"]
        self.treeview = Treeview(
            master=self.treeview_frame,
            values=values,
            wide=wide,
            columns=self.columns,
        )
        self.button = tk.Button(
            master=self,
            text="Export",
            command=lambda: self.export(info, icons, algorithm)
        )
        self.button.pack()
        self.create_info_widgets(info, patterns, algorithm)

    def create_info_widgets(self, info, patterns, algorithm):
        column = 0
        for j, k in zip(
                ["Algorithm", "House System"],
                [algorithm, self.hsys]
        ):
            title = tk.Label(
                master=self.info_frame,
                text=j,
                font="Default 12 bold"
            )
            colon = tk.Label(
                master=self.info_frame,
                text=":",
                font="Default 12 bold"
            )
            value = tk.Label(master=self.info_frame, text=k)
            title.grid(row=0, column=column + 0, sticky="w")
            colon.grid(row=0, column=column + 1, sticky="w")
            value.grid(row=0, column=column + 2, sticky="w")
            column += 3
        row = 1
        r = 0
        for k, v in info.items():
            title = tk.Label(
                master=self.info_frame,
                text=k,
                font="Default 12 bold"
            )
            colon = tk.Label(
                master=self.info_frame,
                text=":",
                font="Default 12 bold"
            )
            value = tk.Label(master=self.info_frame, text=v)
            if row % 2 == 0:
                title.grid(row=row - r - 1, column=3, sticky="w")
                colon.grid(row=row - r - 1, column=4, sticky="w")
                value.grid(row=row - r - 1, column=5, sticky="w")
                r += 1
            else:
                title.grid(row=row - r, column=0, sticky="w")
                colon.grid(row=row - r, column=1, sticky="w")
                value.grid(row=row - r, column=2, sticky="w")
            row += 1
        title = tk.Label(
            master=self.pattern_frame,
            text="Astrological Results",
            font="Default 12 bold"
        )
        title.pack()
        frame = tk.Frame(master=self.pattern_frame)
        frame.pack()
        row = 0
        column = 0
        padx = 0
        for p in patterns:
            if p[0] in ["Ascendant", "Midheaven"]:
                planet = p[0]
                sign = SIGNS[p[1]]["symbol"]
                color = SIGNS[p[1]]["color"]
                dms = dd_to_dms(convert_degree(p[2])[0])
                frmt = [planet, sign, dms]
            else:
                planet = PLANETS[p[0]]["symbol"]
                sign = SIGNS[p[1]]["symbol"]
                color = SIGNS[p[1]]["color"]
                dms = dd_to_dms(convert_degree(p[2])[0])
                house = p[-1]
                frmt = [planet, sign, dms, house]
            for col, i in enumerate(frmt):
                if i == sign:
                    fg = color
                else:
                    fg = "black"
                label = tk.Label(
                    master=frame,
                    text=i,
                    fg=fg,
                    font="Default 8"
                )
                label.grid(
                    row=row, 
                    column=col + column, 
                    sticky="w", 
                    padx=padx if col == 0 else 0
                )
            row += 1
            if row % 5 == 0:
                row = 0
                column += 4
                padx = 10

    def export(self, info, icons, algorithm):
        Spreadsheet(
            data=[
                self.treeview.item(i)["values"]
                for i in self.treeview.get_children()
            ],
            filename=f"{info['Name']}_{self.hsys}_"
                     f"{info['Time'].replace(':', 'h')}_"
                     f"{algorithm.replace('.json', '')}.xlsx",
            info=info,
            hsys=self.hsys,
            algorithm=algorithm
        )
        MsgBox(
            title="Info",
            message="Successfully exported!",
            level="info",
            icons=icons
        )
