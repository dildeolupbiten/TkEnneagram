# -*- coding: utf-8 -*-

from .constants import PLANETS
from .utilities import convert_degree, reverse_convert_degree
from .modules import os, dt, tz, swe, timezone, ConfigParser, TimezoneFinder

swe.set_ephe_path(os.path.join(os.getcwd(), "Eph"))


class Zodiac:
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
    ):
        self.local_year = year
        self.local_month = month
        self.local_day = day
        self.local_hour = hour
        self.local_minute = minute
        self.local_second = second
        self.lat = lat
        self.lon = lon
        self.hsys = hsys
        if not jd:
            self.utc_year = self.local_to_utc()["year"]
            self.utc_month = self.local_to_utc()["month"]
            self.utc_day = self.local_to_utc()["day"]
            self.utc_hour = self.local_to_utc()["hour"]
            self.utc_minute = self.local_to_utc()["minute"]
            self.utc_second = self.local_to_utc()["second"]
            self.jd = self.julday()
        else:
            self.jd = jd

    def julday(self):
        t_given = dt.strptime(
            f"{self.utc_year}.{self.utc_month}.{self.utc_day}",
            "%Y.%m.%d"
        )
        t_limit = dt.strptime("1582.10.15", "%Y.%m.%d")
        if (t_limit - t_given).days > 0:
            calendar = swe.JUL_CAL
        else:
            calendar = swe.GREG_CAL
        jd = swe.julday(
            self.utc_year,
            self.utc_month,
            self.utc_day,
            self.utc_hour
            + (self.utc_minute / 60)
            + (self.utc_second / 3600),
            calendar
        )
        deltat = swe.deltat(jd)
        return round(jd + deltat, 6)

    def local_to_utc(self):
        local_zone = tz.gettz(
            str(
                timezone(
                    TimezoneFinder().timezone_at(
                        lat=self.lat, lng=self.lon
                    )
                )
            )
        )
        utc_zone = tz.gettz("UTC")
        global_time = dt.strptime(
            f"{self.local_year}-{self.local_month}-{self.local_day} "
            f"{self.local_hour}:{self.local_minute}:{self.local_second}",
            "%Y-%m-%d %H:%M:%S"
        )
        local_time = global_time.replace(tzinfo=local_zone)
        utc_time = local_time.astimezone(utc_zone)
        return {
            "year": utc_time.year,
            "month": utc_time.month,
            "day": utc_time.day,
            "hour": utc_time.hour,
            "minute": utc_time.minute,
            "second": utc_time.second
        }

    def planet_pos(self, planet):
        degree = swe.calc(self.jd, planet)[0]
        if isinstance(degree, tuple):
            degree = degree[0]
        calc = convert_degree(degree=degree)
        return calc[1], reverse_convert_degree(calc[0], calc[1])

    def house_pos(self):
        house = []
        asc = 0
        degree = []
        for i, j in enumerate(swe.houses(
                self.jd, self.lat, self.lon,
                bytes(self.hsys.encode("utf-8")))[0]):
            if i == 0:
                asc += j
            degree.append(j)
            house.append((
                f"{i + 1}",
                j,
                f"{convert_degree(j)[1]}"))
        return house, asc, degree

    def patterns(self):
        planet_positions = []
        house_positions = []
        config = ConfigParser()
        config.read("defaults.ini")
        selected_planets = config["PLANETS"]["selected"].split(", ")
        for i in range(12):
            house = [
                int(self.house_pos()[0][i][0]),
                self.house_pos()[0][i][-1],
                float(self.house_pos()[0][i][1]),
            ]
            house_positions.append(house)
        hp = [j[-1] for j in house_positions]
        for key, value in PLANETS.items():
            if value["number"] is None:
                continue
            if key not in selected_planets:
                continue
            planet = self.planet_pos(planet=value["number"])
            house = 0
            for i in range(12):
                if i != 11:
                    if hp[i] < planet[1] < hp[i + 1]:
                        house = i + 1
                        break
                    elif hp[i] < planet[1] > hp[i + 1] \
                            and hp[i] - hp[i + 1] > 240:
                        house = i + 1
                        break
                    elif hp[i] > planet[1] < hp[i + 1] \
                            and hp[i] - hp[i + 1] > 240:
                        house = i + 1
                        break
                else:
                    if hp[i] < planet[1] < hp[0]:
                        house = i + 1
                        break
                    elif hp[i] < planet[1] > hp[0] \
                            and hp[i] - hp[0] > 240:
                        house = i + 1
                        break
                    elif hp[i] > planet[1] < hp[0] \
                            and hp[i] - hp[0] > 240:
                        house = i + 1
                        break
            planet_info = [
                key,
                planet[0],
                planet[1],
                f"House-{house}"
            ]
            planet_positions.append(planet_info)
        asc = house_positions[0] + ["House-1"]
        asc[0] = "Ascendant"
        mc = house_positions[9] + ["House-10"]
        mc[0] = "Midheaven"
        return [asc, mc] + planet_positions
