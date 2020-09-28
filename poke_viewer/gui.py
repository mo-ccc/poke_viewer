import tkinter
from pokemonster import Pokemonster
from io import BytesIO
from PIL import Image as pil_image, ImageTk as pil_image_tk
import requests


class Application():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('400x250')
        self.create_sprite_widget(1, 0)
        self.create_types_widget(2, 0)
        self.create_pokedex_widget(0, 0)
        self.create_add_delete_buttons(0, 1)

    def create_pokedex_widget(self, xcoord, ycoord):
        # create a frame and place on root grid
        frame = tkinter.Frame(self.root)
        frame.grid(column=xcoord, row=ycoord)

        # create a vertical scrollbar and place in right side of frame
        scrollbar = tkinter.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # create a list box and place in left side of frame
        # scrollbar controls the yscroll of the listbox
        self.listbox = tkinter.Listbox(frame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left")
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
        pokemon = Pokemonster(name)
        print(pokemon.to_string)
        self.display_sprite_img(pokemon.sprites, "default")
        self.display_types(pokemon.types)

    def create_sprite_widget(self, xcoord, ycoord):
        self.imgLbl = tkinter.Label(self.root, borderwidth=2, relief="groove",
                                    width=150, height=150)
        self.imgLbl.grid(column=xcoord, row=ycoord)

    def display_sprite_img(self, sprites, sprite):
        data = requests.get(sprites[sprite]).content
        raw_bytes = pil_image.open(BytesIO(data))
        img = pil_image_tk.PhotoImage(raw_bytes)
        self.imgLbl.configure(image=img)
        self.images = []
        self.images.append(img)

    @classmethod
    def convert_link_2_img(cls, link):
        data = requests.get(link).content
        raw_bytes = pil_image.open(BytesIO(data))
        return pil_image_tk.PhotoImage(raw_bytes)

    def create_types_widget(self, xcoord, ycoord):
        self.types_frame = tkinter.Frame(self.root)
        self.types_frame.grid(column=xcoord, row=ycoord)

    colort = {
        "fire": "red", "water": "blue", "ground": "brown",
        "poison": "purple", "grass": "green", "bug": "lawn green",
        "dragon": "slate blue", "fighting": "IndianRed1",
        "flying": "sky blue", "ghost": "plum1", "psychic": "pink",
        "ice": "PaleTurqoise1", "electric": "yellow",
        "rock": "burlywood3"
    }

    @classmethod
    def type_colours(cls, color):
        if color in cls.colort:
            return cls.colort[color]
        return "grey"

    def display_types(self, types):
        list_grid = self.types_frame.pack_slaves()
        for label in list_grid:
            label.destroy()
        for t in types:
            lbl = tkinter.Label(self.types_frame, text=t,
                                bg=self.type_colours(t), padx=10)
            lbl.pack(side="left")

    def create_add_delete_buttons(self, xcoord, ycoord):
        frame = tkinter.Frame(self.root)
        frame.grid(column=xcoord, row=ycoord)
        add_button = tkinter.Button(frame, text="add",
                                    command=self.add_pokemon)
        add_button.pack(side="left", padx=(0, 10), ipadx=7)
        delete_button = tkinter.Button(frame, text="delete")
        delete_button.pack(side="left", padx=(0, 15))

    def add_pokemon(self):
        popup = tkinter.Tk()
        textfield = tkinter.Entry(popup)
        textfield.pack(side="left")
        enter = tkinter.Button(popup, text="enter")
        enter.pack(side="left")

    def del_pokemon(self):
        self.listbox.delete(tkinter.ACTIVE)
