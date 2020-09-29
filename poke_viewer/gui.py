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
        self.create_info_container(2, 0)
        self.create_types_widget()
        self.create_abilities_widget()
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
        self.display_abilities(pokemon.abilities)

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

    def create_info_container(self, xcoord, ycoord):
        self.info_container = tkinter.Frame(self.root)
        self.info_container.grid(column=xcoord, row=ycoord)

    def create_types_widget(self):
        self.types_frame = tkinter.Frame(self.info_container)
        self.types_frame.pack(side="top")

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
        self.destroy_all_in_frame(self.types_frame.pack_slaves)
        for t in types:
            lbl = tkinter.Label(self.types_frame, text=t,
                                bg=self.type_colours(t), padx=10)
            lbl.pack(side="left")

    def destroy_all_in_frame(self, frame_slavetype):
        list_grid = frame_slavetype()
        for item in list_grid:
            item.destroy()

    def create_add_delete_buttons(self, xcoord, ycoord):
        frame = tkinter.Frame(self.root)
        frame.grid(column=xcoord, row=ycoord)
        add_button = tkinter.Button(frame, text="add",
                                    command=self.add_pokemon_menu)
        add_button.pack(side="left", padx=(0, 10), ipadx=7)
        delete_button = tkinter.Button(frame, text="delete",
                                       command=self.del_pokemon)
        delete_button.pack(side="left", padx=(0, 15))

    def add_pokemon_menu(self):
        self.popup = tkinter.Tk()
        textfield = tkinter.Entry(self.popup)
        textfield.pack(side="left")
        enter = tkinter.Button(self.popup, text="enter",
                               command=lambda:
                                   self.write_pokemon(textfield.get()))
        enter.pack(side="left")

    def write_pokemon(self, name):
        print(name)
        if Pokemonster.add_pokemon(name) == 0:
            self.listbox.insert("end", name)
            self.popup.destroy()

    def del_pokemon(self):
        Pokemonster.pokedex.pop(self.listbox.curselection()[0])
        self.listbox.delete(tkinter.ACTIVE)

    def create_abilities_widget(self):
        self.abilities_frame = tkinter.Frame(self.info_container)
        self.abilities_frame.pack(side="bottom")

    def display_abilities(self, abilities):
        self.destroy_all_in_frame(self.abilities_frame.grid_slaves)
        positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
        count = 0
        for ability in abilities:
            ab_but = tkinter.Button(self.abilities_frame, text=ability)
            ab_but.grid(column=positions[count][0],
                        row=positions[count][1])
            count += 1
