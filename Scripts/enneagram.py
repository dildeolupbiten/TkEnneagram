# -*- coding: utf-8 -*-

from .modules import np
from .scores import scores
from .zodiac import Zodiac


class Enneagram:
    def __init__(
            self,
            year,
            month,
            day,
            hour,
            minute,
            second,
            lat,
            lon,
            hsys,
    ):
        self.chart = Zodiac(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            lat=lat,
            lon=lon,
            hsys=hsys
        )
        self.patterns = self.chart.patterns()

    def get_chart_scores(self, which):
        n1, n2 = 0, 0
        result = {}
        for p in self.patterns:
            if p[n1] in scores[which]:
                if which == "sign":
                    n2 = 1
                elif which == "house":
                    if p[n1] in ["Ascendant", "Midheaven"]:
                        n2 = 1
                    else:
                        n2 = -1
                result[f"{p[n1]} in {p[n2]}"] = scores[which][p[n1]][p[n2]]
        return result

    def get_total_score(self, which, name):
        result = self.get_chart_scores(which=which)
        total = np.array([1 for _ in range(9)])
        _total = {name: {}}
        for pattern, score in result.items():
            total = total * np.array([*score.values()][:-1])
        total = {f"Type-{i}": round(j, 2) for i, j in enumerate(total, 1)}
        _total[name].update(total)
        _total[name]["Total"] = round(
            sum(v for k, v in _total[name].items()), 2
        )
        result.update(_total)
        return result

    def get_all_scores(self):
        return {
            k: self.get_total_score(which=k, name=v)
            for k, v in {
                "sign": "Dayscores",
                "house": "Effect of Houses"
            }.items()
        }
