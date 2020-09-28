import tkinter
from pokemonster import Pokemonster
from io import BytesIO
from PIL import Image as pil_image, ImageTk as pil_image_tk
import requests


class Application():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('350x250')
        self.create_sprite_widget(1, 0)
        self.create_pokedex_widget(0, 0)

    def init_tkinter_vars(self):
        self.selected_pokemon_var = tkinter.StringVar()

    def create_pokedex_widget(self, xcoord, ycoord):
        # create a frame and place on grd
        frame = tkinter.Frame(self.root)
        frame.grid(column=xcoord, row=ycoord)

        # create a vertical scrollbar and place in right side of frame
        scrollbar = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right")

        # create a list box and place in left side of frame
        # scrollbar controls the yscroll of the listbox
        self.listbox = tkinter.Listbox(frame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left", fill="y")
        # config scroll bar to manage listbox
        scrollbar.config(command=self.listbox.yview)

        # fill listbox with list of pokemon
        for pokemon in Pokemonster.list_pokedex():
            self.listbox.insert(tkinter.END, pokemon)

        # set listbox selection to 0
        self.listbox.select_set(0)
        # bind list box selection to function make_selection
        self.listbox.bind("<<ListboxSelect>>", self.make_selection)
        # call make selection so that the selected element <0> is used
        self.make_selection()

    def make_selection(self, event=None):
        # gets the index of the current selection from the listbox
        index = self.listbox.curselection()[0]
        # uses index to retrieve name of pokemon
        name = Pokemonster.list_pokedex()[index]
        # initalizes pokemonster object from the name
        self.pokemon = Pokemonster(name)
        print(self.pokemon.to_string)
        self.display_sprite_img("default")

    def display_sprite_img(self, sprite):
        data = requests.get(self.pokemon.sprites[sprite]).content
        raw_bytes = pil_image.open(BytesIO(data))
        img = pil_image_tk.PhotoImage(raw_bytes)
        self.imgLbl.configure(image=img)
        self.images = []
        self.images.append(img)

    def create_sprite_widget(self, xcoord, ycoord):
        self.imgLbl = tkinter.Label(self.root, borderwidth=2, relief="groove",
                                    width=150, height=150)
        self.imgLbl.grid(column=xcoord, row=ycoord)
