# -*- coding: utf-8 -*-

from .modules import tk, ttk


class EntryFrame(tk.Frame):
    def __init__(
            self,
            texts,
            title,
            position="horizontal",
            color="red",
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.label = tk.Label(master=self, text=title, fg="red")
        self.label.grid(row=0, column=0, columnspan=2)
        self.widgets = self.create_widgets(
            texts=texts,
            position=position,
            color=color
        )
        
    def create_widgets(self, texts, position, color):
        widgets = {}
        for index, text in enumerate(texts):
            label = tk.Label(master=self, text=text, fg=color)
            entry = ttk.Entry(master=self, width=5)
            if position == "horizontal":
                label.grid(row=1, column=index)
                entry.grid(row=2, column=index)
            elif position == "vertical":
                label.grid(row=index + 1, column=0)
                entry.grid(row=index + 1, column=1)
            entry.bind(
                sequence="<KeyRelease>",
                func=self.delete_nonnumeric_chars
            )
            widgets[text] = entry
        return widgets

    @staticmethod
    def delete_nonnumeric_chars(event):
        try:
            int(event.widget.get())
        except ValueError:
            index = event.widget.index("insert")
            event.widget.delete(index - 1, "end")
