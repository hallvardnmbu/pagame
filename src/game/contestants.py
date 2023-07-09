import tkinter as tk


class Contestants:
    def __init__(self):
        """
        Object for adding contestants.
        """

        self.n_contestants = 0
        self.entry_names = []
        self.contestants = []

        self.window = tk.Tk()
        self.window.geometry('640x480')
        self.window.title("Add contestants")

        self.label_players = tk.Label(self.window, text="Number of contestants:")
        self.label_players.pack()
        self.entry_players = tk.Entry(self.window)
        self.entry_players.pack()

        self.label_names = tk.Label(self.window, text="Name:")
        self.label_names.pack()

        self.button_update = tk.Button(self.window, text="Update", command=self._update_names)
        self.button_update.pack()

        self.button_submit = tk.Button(self.window, text="Continue", command=self._create_players)
        self.button_submit.pack()

        self.window.mainloop()

    def _update_names(self):
        self.n_contestants = int(self.entry_players.get())
        for entry in self.entry_names:
            entry.destroy()

        self.entry_names = []
        for _ in range(self.n_contestants):
            entry = tk.Entry(self.window)
            entry.pack()
            self.entry_names.append(entry)

    def _create_players(self):
        for entry in self.entry_names:
            self.contestants.append(entry.get())
        self.window.destroy()
