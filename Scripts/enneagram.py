# -*- coding: utf-8 -*-

from .zodiac import Zodiac
from .algorithm import auth
from .modules import np, json, ConfigParser


class Enneagram:
    def __init__(
            self,
            year=0,
            month=0,
            day=0,
            hour=0,
            minute=0,
            second=0,
            jd=.0,
            lat=.0,
            lon=.0,
            hsys="",
            icons=None
    ):
        self.chart = Zodiac(
            year=year,
            month=month,
            day=day,
            hour=hour,
            minute=minute,
            second=second,
            jd=jd,
            lat=lat,
            lon=lon,
            hsys=hsys
        )
        self.patterns = self.chart.patterns()
        self.scores = None
        self.icons = icons

    def get_chart_scores(self, which):
        config = ConfigParser()
        config.read("defaults.ini")
        file = config["ALGORITHM"]["selected"]
        if file == "2012_Algorithm_Placidus.json":
            if self.scores:
                pass
            else:
                self.scores = auth(
                    icons=self.icons, 
                    config_key=config["AUTH"]["key"]
                )
                if self.scores:
                    pass
                else:
                    return
        else:
            with open(
                f"Algorithms/{config['ALGORITHM']['selected']}", 
                "r"
            ) as f:
                self.scores = json.load(f)
        n1, n2 = 0, 0
        result = {}
        for p in self.patterns:
            if p[n1] in self.scores[which]:
                if which == "sign":
                    n2 = 1
                elif which == "house":
                    if p[n1] in ["Ascendant", "Midheaven"]:
                        n2 = 1
                    else:
                        n2 = -1
                result[f"{p[n1]} in {p[n2]}"] = \
                    self.scores[which][p[n1]][p[n2]]
        return result

    def get_total_score(self, which, name):
        result = self.get_chart_scores(which=which)
        if not result:
            return
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
        result = {}
        for k, v in {
            "sign": "Dayscores",
            "house": "Effect of Houses"
        }.items():
            value = self.get_total_score(which=k, name=v)
            if not value:
                return
            else:
                result[k] = value
        return result
