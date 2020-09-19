# -*- coding: utf-8 -*-

from .utilities import decrypt
from .messagebox import MsgBox
from .modules import tk, ttk, json, ConfigParser

result = None


def try_access(toplevel, key, icons):
    global result
    try:
        int(key)
    except ValueError:
        MsgBox(
            title="Warning",
            message="Key must be integer.",
            icons=icons,
            level="warning"    
        )
        return
    try:
        result = json.loads(
            decrypt(
                file="Algorithms/2012_Algorithm_Placidus.json", 
                password=int(key)))
        config = ConfigParser()
        config.read("defaults.ini")
        config["AUTH"]["key"] = key
        with open("defaults.ini", "w") as f:
            config.write(f)
    except json.decoder.JSONDecodeError:
        result = None
    if toplevel:
        toplevel.destroy()


def auth_interface(icons, config_key):
    global result
    if config_key != "None":
        try_access(
            toplevel=None,
            key=config_key,
            icons=icons,
        )
        return
    toplevel = tk.Toplevel()
    toplevel.title("Authentication")
    toplevel.protocol("WM_DELETE_WINDOW", lambda: None)
    toplevel.resizable(width=False, height=False)
    key_label = ttk.Label(master=toplevel, text="Activation Key")
    key_label.grid(row=1, column=0, sticky="w")
    key_entry = ttk.Entry(master=toplevel, width=64)
    key_entry.grid(row=1, column=1, sticky="w") 
    button = tk.Button(
        master=toplevel, 
        text="OK",
        command=lambda: try_access(
            toplevel=toplevel,
            key=key_entry.get(),
            icons=icons,
        )
    )
    button.grid(row=2, column=0, columnspan=2)
    toplevel.wait_window()
    

def auth(icons, config_key):
    global result
    auth_interface(icons=icons, config_key=config_key)
    return result
