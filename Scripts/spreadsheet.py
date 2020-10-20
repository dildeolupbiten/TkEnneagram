# -*- coding: utf-8 -*-

from .modules import Workbook


class Spreadsheet(Workbook):
    def __init__(
            self,
            data,
            info,
            hsys,
            algorithm,
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
            "P", "Q", "R",
            "S", "T", "U"
        ]
        if algorithm:
            self.columns = ["Category"] + \
                           [f"Type-{i}" for i in range(1, 10)] + \
                           ["Total"]
            self.write_normal(
                data=data,
                info=info,
                hsys=hsys,
                algorithm=algorithm
            )
        else:
            self.write_category(
                data=data,
                info=info
            )
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

    def write_normal(self, data, info, hsys, algorithm):
        self.sheet.merge_range(
            "A1:B1",
            "Algorithm",
            self.format(bold=True)
        )
        self.sheet.merge_range(
            "C1:E1",
            algorithm,
            self.format(bold=False, align="left")
        )
        self.sheet.merge_range(
            "F1:G1",
            "House System",
            self.format(bold=True)
        )
        self.sheet.merge_range(
            f"H1:J1",
            hsys,
            self.format(bold=False)
        )
        row = 2
        r = 0
        for k, v in info.items():
            if v.isnumeric():
                value = int(v)
            else:
                try:
                    value = float(v)
                except ValueError:
                    value = v
            if row % 2 == 0:
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
        n = 0
        for i in self.columns:
            if i == "Category":
                self.sheet.merge_range(
                    f"{self.cols[n]}5:{self.cols[n + 2]}5",
                    i,
                    self.format(align="center", bold=True)
                )
            else:
                self.sheet.write(
                    f"{self.cols[n + 2]}5",
                    i,
                    self.format(align="center", bold=True)
                )
            n += 1
        for index, cols in enumerate(data, 6):
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
                    if index in [19, 35]:
                        self.sheet.write(
                            f"{self.cols[n + 2]}{index}",
                            col,
                            self.format(align="center", font_color="red")
                        )
                    elif index == 36:
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

    def write_category(self, info, data):
        row = 9
        for index, (k, v) in enumerate(info.items(), 1):
            if index < 7:
                self.sheet.merge_range(
                    f"A{index}:B{index}",
                    k,
                    self.format(bold=True)
                )
                self.sheet.write(
                    f"C{index}",
                    v,
                    self.format(bold=False, align="left")
                )
            else:
                self.sheet.merge_range(
                    f"D{index - 6}:E{index - 6}",
                    k,
                    self.format(bold=True)
                )
                self.sheet.merge_range(
                    f"F{index - 6}:J{index - 6}",
                    v,
                    self.format(bold=False, align="left")
                )
        self.sheet.merge_range(
            f"A{row}:J{row}",
            "Enneagram Distribution",
            self.format(bold=True, align="center")
        )
        values = []
        for index, (k, v) in enumerate(data[0].items()):
            self.sheet.write(
                f"{self.cols[index]}{row + 1}",
                k,
                self.format(bold=True, align="center")
            )
            self.sheet.write(
                f"{self.cols[index]}{row + 2}",
                v,
                self.format(bold=False, align="center")
            )
            values.append(v)
        self.sheet.write(
            f"J{row + 1}",
            "Total",
            self.format(bold=True, align="center")
        )
        self.sheet.write(
            f"J{row + 2}",
            sum(values),
            self.format(bold=False, align="center")
        )
        self.sheet.merge_range(
            f"A{row + 4}:S{row + 4}",
            "Enneagram Wing Distribution",
            self.format(bold=True, align="center")
        )
        values = []
        column = 0
        for index, (key, value) in enumerate(data[1].items()):
            self.sheet.merge_range(
                f"{self.cols[column]}{row + 5}:"
                f"{self.cols[column + 1]}{row + 5}",
                key,
                self.format(bold=True, align="center")
            )
            for i, (k, v) in enumerate(value.items()):
                self.sheet.write(
                    f"{self.cols[column]}{row + 6}",
                    k,
                    self.format(bold=True, align="center")
                )
                self.sheet.write(
                    f"{self.cols[column]}{row + 7}",
                    v,
                    self.format(align="center")
                )
                values.append(v)
                column += 1
        self.sheet.merge_range(
            f"S{row + 5}:S{row + 6}",
            "Total",
            self.format(bold=True, align="center")
        )
        self.sheet.write(
            f"S{row + 7}",
            sum(values),
            self.format(bold=False, align="center")
        )
