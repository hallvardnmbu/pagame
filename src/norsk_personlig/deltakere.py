import tkinter as tk


class Deltakere:
    def __init__(self):
        """
        Object for å legge til deltakere.
        """

        self.antall_deltakere = 0
        self.entry_names = []
        self.deltakere = []

        self.window = tk.Tk()
        self.window.geometry('640x480')
        self.window.title("Legg til deltakere")

        self.label_players = tk.Label(self.window, text="Antall deltakere:")
        self.label_players.pack()
        self.entry_players = tk.Entry(self.window)
        self.entry_players.pack()

        self.label_names = tk.Label(self.window, text="Navn:")
        self.label_names.pack()

        self.button_update = tk.Button(self.window, text="Oppdater", command=self._update_names)
        self.button_update.pack()

        self.button_submit = tk.Button(self.window, text="Ferdig", command=self._create_players)
        self.button_submit.pack()

        self.window.mainloop()

    def _update_names(self):
        self.antall_deltakere = int(self.entry_players.get())
        for entry in self.entry_names:
            entry.destroy()

        self.entry_names = []
        for _ in range(self.antall_deltakere):
            entry = tk.Entry(self.window)
            entry.pack()
            self.entry_names.append(entry)

    def _create_players(self):
        for entry in self.entry_names:
            self.deltakere.append(entry.get())
        self.window.destroy()
