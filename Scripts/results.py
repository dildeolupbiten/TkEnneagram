# -*- coding: utf-8 -*-

from .modules import tk
from .messagebox import MsgBox
from .spreadsheet import Spreadsheet


class Results(tk.Toplevel):
    def __init__(
            self,
            info,
            enneagram_scores,
            enneagram_wing_scores,
            path,
            icons,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.title("Results")
        self.resizable(width=False, height=False)
        self.create_info_widgets(info=info)
        self.create_enneagram_results(
            scores=enneagram_scores,
            title="Enneagram Distribution"
        )
        self.create_enneagram_wing_results(
            scores=enneagram_wing_scores,
            title="Enneagram Wing Distribution"
        )
        self.export_button = tk.Button(
            master=self,
            text="Export",
            command=lambda: self.export(
                info=info,
                data=[enneagram_scores, enneagram_wing_scores],
                icons=icons,
                path=path
            )
        )
        self.export_button.pack()

    def create_info_widgets(self, info):
        frame = tk.Frame(master=self)
        frame.pack(fill="both")
        for index, (k, v) in enumerate(info.items()):
            if index < 6:
                column = 0
                row = index
            else:
                column = 4
                row = index - 6
                if index == 6:
                    f = tk.Frame(master=frame, width=20)
                    f.grid(row=row, column=3)
            for i, j in enumerate([k, ":", v]):
                if j == v:
                    font = "Default 10"
                    fg = "black"
                else:
                    font = "Default 10"
                    fg = "red"
                title = tk.Label(
                    master=frame,
                    text=j,
                    font=font,
                    fg=fg
                )
                title.grid(
                    row=row,
                    column=column + i,
                    sticky="w",
                )

    def create_enneagram_results(self, scores, title):
        frame = tk.Frame(master=self)
        frame.pack()
        header = tk.Label(
            master=frame,
            text=title,
            font="Default 12",
            fg="red"
        )
        header.pack()
        sub_frame = tk.Frame(master=frame)
        sub_frame.pack()
        values = []
        for index, (k, v) in enumerate(scores.items()):
            title = tk.Label(
                master=sub_frame,
                text=k,
                font="Default 9",
                fg="blue"
            )
            title.grid(row=0, column=index, padx=5)
            score = tk.Label(master=sub_frame, text=v)
            score.grid(row=1, column=index, padx=5)
            values.append(v)
        title = tk.Label(
            master=sub_frame,
            text="Total",
            font="Default 9",
            fg="blue"
        )
        title.grid(row=0, column=9, padx=5)
        score = tk.Label(master=sub_frame, text=sum(values))
        score.grid(row=1, column=9, padx=5)

    def create_enneagram_wing_results(self, scores, title):
        frame = tk.Frame(master=self)
        frame.pack()
        values = []
        header = tk.Label(
            master=frame,
            text=title,
            font="Default 12",
            fg="red"
        )
        header.pack()
        sub_frame = tk.Frame(master=frame)
        sub_frame.pack()
        for index, (key, value) in enumerate(scores.items()):
            sub_sub_frame = tk.Frame(master=sub_frame)
            sub_sub_frame.grid(row=0, column=index, padx=5)
            title = tk.Label(
                master=sub_sub_frame,
                text=key,
                font="Default 9",
                fg="blue"
            )
            title.grid(row=0, column=0, columnspan=2)
            for i, (k, v) in enumerate(value.items()):
                title = tk.Label(
                    master=sub_sub_frame,
                    text=k,
                    font="Default 9",
                    fg="purple"
                )
                title.grid(row=1, column=i)
                score = tk.Label(master=sub_sub_frame, text=v)
                score.grid(row=2, column=i)
                values.append(v)
        sub_sub_frame = tk.Frame(master=sub_frame)
        sub_sub_frame.grid(row=0, column=9, padx=5)
        title = tk.Label(
            master=sub_sub_frame,
            text="Total",
            font="Default 9",
            fg="blue"
        )
        title.grid(row=0, column=0, columnspan=2)
        title = tk.Label(
            master=sub_sub_frame,
            text="",
            font="Default 9"
        )
        title.grid(row=1, column=1)
        score = tk.Label(master=sub_sub_frame, text=sum(values))
        score.grid(row=2, column=1)

    @staticmethod
    def export(info, data, icons, path):
        Spreadsheet(
            info=info,
            data=data,
            algorithm=None,
            hsys=None,
            filename=path
        )
        MsgBox(
            title="Info",
            level="info",
            icons=icons,
            message="Successfully exported!"
        )
