import tkinter as tk
import services as svc


def show_score(disconnected):
    window = tk.Tk()
    window.title("Placar")
    label = tk.Label(window, text="Placar dos jogares\n\n")
    label.pack()
    old_player_list = ''

    while True:
        if len(disconnected) == 1:
            break
        player_list = svc.get_score_list()
        if old_player_list != player_list:
            label.destroy()
            label = tk.Label(window, text="Placar dos jogares\n\n")
            label.pack()
            for jog in player_list.split('\n'):
                label.config(text=label.cget('text') + f"{jog}\n")
            old_player_list = player_list
        window.update()
