# -*- coding: utf-8 -*-

from modules import Workbook


class Spreadsheet(Workbook):
    def __init__(
            self,
            data,
            info,
            hsys,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.sheet = self.add_worksheet()
        self.cols = [
            "A", "B", "C",
            "D", "E", "F",
            "G", "H", "I",
            "J", "K", "L",
            "M", "N", "O",
            "P", "Q", "R"
        ]
        self.columns = ["Category"] + \
                       [f"Type-{i}" for i in range(1, 10)] + \
                       ["Total"]
        self.write(data=data, info=info, hsys=hsys)
        self.close()

    def format(
            self,
            bold: bool = False,
            align: str = "",
            font_name: str = "Arial",
            font_size: int = 11,
            font_color: str = "black"
    ):
        return self.add_format(
            {
                "bold": bold,
                "align": align,
                "valign": "vcenter",
                "font_name": font_name,
                "font_size": font_size,
                "font_color": font_color
            }
        )

    def write(self, data, info, hsys):
        row = 1
        r = 0
        for k, v in info.items():
            if v.get().isnumeric():
                value = int(v.get())
            else:
                try:
                    value = float(v.get())
                except ValueError:
                    value = v.get()
            if row % 2 != 0:
                self.sheet.merge_range(
                    f"A{row - r}:B{row - r}",
                    k,
                    self.format(bold=True)
                )
                self.sheet.merge_range(
                    f"C{row - r}:E{row - r}",
                    value,
                    self.format(bold=False, align="left")
                )
            else:
                self.sheet.merge_range(
                    f"F{row - 1 - r}:G{row - 1 - r}",
                    k,
                    self.format(bold=True)
                )
                self.sheet.merge_range(
                    f"H{row - 1 - r}:J{row - 1 - r}",
                    value,
                    self.format(bold=False, align="left")
                )
                r += 1
            row += 1
        self.sheet.merge_range(
            f"F{row - 1 - r}:G{row - 1 - r}",
            "House System",
            self.format(bold=True)
        )
        self.sheet.merge_range(
            f"H{row - 1 - r}:J{row - 1 - r}",
            hsys,
            self.format(bold=False)
        )
        n = 0
        for i in self.columns:
            if i == "Category":
                self.sheet.merge_range(
                    f"{self.cols[n]}7:{self.cols[n + 2]}7",
                    i,
                    self.format(align="center", bold=True)
                )
            else:
                self.sheet.write(
                    f"{self.cols[n + 2]}7",
                    i,
                    self.format(align="center", bold=True)
                )
            n += 1
        for index, cols in enumerate(data, 8):
            n = 0
            for col in cols:
                if "in" in col:
                    self.sheet.merge_range(
                        f"{self.cols[n]}{index}:{self.cols[n + 2]}{index}",
                        col,
                        self.format()
                    )
                elif col in [
                        "Dayscores",
                        "Effect of Houses",
                        "Total Scores"
                ]:
                    self.sheet.merge_range(
                        f"{self.cols[n]}{index}:{self.cols[n + 2]}{index}",
                        col,
                        self.format(bold=True)
                    )
                else:
                    col = float(col)
                    if index in [21, 37]:
                        self.sheet.write(
                            f"{self.cols[n + 2]}{index}",
                            col,
                            self.format(align="center", font_color="red")
                        )
                    elif index == 38:
                        self.sheet.write(
                            f"{self.cols[n + 2]}{index}",
                            col,
                            self.format(align="center", font_color="blue")
                        )
                    else:
                        self.sheet.write(
                            f"{self.cols[n + 2]}{index}",
                            col,
                            self.format(align="center")
                        )
                n += 1
