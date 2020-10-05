# -*- coding: utf-8 -*-

from .modules import swe

SIGNS = {
    "Aries": {
        "symbol": "\u2648",
        "color": "#FF0000"
    },
    "Taurus": {
        "symbol": "\u2649",
        "color": "#00FF00"
    },
    "Gemini": {
        "symbol": "\u264A",
        "color": "#FFFF00"
    },
    "Cancer": {
        "symbol": "\u264B",
        "color": "#0000FF"
    },
    "Leo": {
        "symbol": "\u264C",
        "color": "#FF0000"
    },
    "Virgo": {
        "symbol": "\u264D",
        "color": "#00FF00"
    },
    "Libra": {
        "symbol": "\u264E",
        "color": "#FFFF00"
    },
    "Scorpio": {
        "symbol": "\u264F",
        "color": "#0000FF"
    },
    "Sagittarius": {
        "symbol": "\u2650",
        "color": "#FF0000"
    },
    "Capricorn": {
        "symbol": "\u2651",
        "color": "#00FF00"
    },
    "Aquarius": {
        "symbol": "\u2652",
        "color": "#FFFF00"
    },
    "Pisces": {
        "symbol": "\u2653",
        "color": "#0000FF"
    }
}

PLANETS = {
    "Sun": {
        "number": swe.SUN,
        "symbol": "\u2299"
    },
    "Moon": {
        "number": swe.MOON,
        "symbol": "\u263E"
    },
    "Mercury": {
        "number": swe.MERCURY,
        "symbol": "\u263F"
    },
    "Venus": {
        "number": swe.VENUS,
        "symbol": "\u2640"
    },
    "Mars": {
        "number": swe.MARS,
        "symbol": "\u2642"
    },
    "Jupiter": {
        "number": swe.JUPITER,
        "symbol": "\u2643"
    },
    "Saturn": {
        "number": swe.SATURN,
        "symbol": "\u2644"
    },
    "Uranus": {
        "number": swe.URANUS,
        "symbol": "\u2645"
    },
    "Neptune": {
        "number": swe.NEPTUNE,
        "symbol": "\u2646"
    },
    "Pluto": {
        "number": swe.PLUTO,
        "symbol": "\u2647"
    },
    "Node": {
        "number": swe.TRUE_NODE,
        "symbol": "\u260A"
    },
    "Chiron": {
        "number": swe.CHIRON,
        "symbol": "\u26B7"
    },
    "Lilith": {
        "number": swe.MEAN_APOG,
        "symbol": "\u26B8"
    },
    "Asc": {
        "number": None,
        "symbol": "Asc"
    },
    "MC": {
        "number": None,
        "symbol": "MC"
    }
}

HOUSE_SYSTEMS = {
    "Placidus": "P",
    "Koch": "K",
    "Porphyrius": "O",
    "Regiomontanus": "R",
    "Campanus": "C",
    "Equal": "E",
    "Whole Signs": "W"
}

CATEGORIES = {
    p: {
        s: {
            f"{str(i).zfill(2)} - {str(i + 1).zfill(2)}": (
                p_index + 
                s_index + 
                i + 
                10000 + 
                (30 * s_index) + 
                (360 * p_index)
            )
            for i in range(30)
        } for s_index, s in enumerate(SIGNS)
    } for p_index, p in enumerate(PLANETS) if p in ["Sun", "Moon", "Asc", "MC"]
}
