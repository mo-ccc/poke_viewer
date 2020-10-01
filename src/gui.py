import tkinter as tk
from pokemonster import Pokemonster
from io import BytesIO
from PIL import Image as pil_image, ImageTk as pil_image_tk
import requests


class Application():
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(bg="white")
        self.root.geometry('500x200')
        self.images = []
        # imgLbl
        self.imgLbl = tk.Label(self.root, borderwidth=2, relief="groove",
                               width=150, height=150, bg="white")
        self.imgLbl.grid(column=1, row=0, rowspan=2)
        # info_container
        self.info_container = tk.Frame(self.root, height=30, bg="white")
        self.info_container.grid(column=2, row=0, sticky="nw",
                                 rowspan=3)
        # types_widget
        self.types_frame = tk.Frame(self.info_container, bg="white")
        self.types_frame.pack(side="top")
        # abilities_widget
        self.abilities_frame = tk.Frame(self.info_container, bg="white")
        self.abilities_frame.pack(side="top")
        # ability_info
        self.text = tk.Label(self.info_container, text="click a button",
                             width=30, wraplength=200,
                             anchor="nw", justify="left", bg="white")
        self.text.pack(side="bottom")
        # shiny_button
        self.shiny_button = tk.Button(self.root, text="shiny",
                                      command=self.toggle_form)
        self.shiny_button.grid(column=1, row=2)
        # self.listbox
        self.create_pokedex_widget(0, 0)
        # self.popup
        self.create_add_delete_buttons(0, 2)

    def create_pokedex_widget(self, xcoord, ycoord):
        # create a frame and place on root grid
        frame = tk.Frame(self.root)
        frame.grid(column=xcoord, row=ycoord, rowspan=2)

        # create a vertical scrollbar and place in right side of frame
        scrollbar = tk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # create a list box and place in left side of frame
        # scrollbar controls the yscroll of the listbox
        self.listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side="left")
        # config scroll bar to manage listbox
        scrollbar.config(command=self.listbox.yview)

        # fill listbox with list of pokemon
        for pokemon in Pokemonster.list_pokedex():
            self.listbox.insert(tk.END, pokemon)

        # set listbox selection to 0
        self.listbox.select_set(0)
        # bind list box selection to function make_selection
        self.listbox.bind("<<ListboxSelect>>", self.make_selection)
        # call make selection so that the selected element <0> is used
        self.make_selection()

    def get_current_selection(self):
        # gets the index of the current selection from the listbox
        index: int = self.listbox.curselection()[0]
        # uses index to retrieve name of pokemon
        name: str = Pokemonster.list_pokedex()[index]
        # initalizes pokemonster object from the name
        return Pokemonster(name)

    def make_selection(self, event=None):
        pokemon: Pokemonster = self.get_current_selection()
        print(pokemon.to_string)
        self.display_sprite_img(pokemon.sprites, "default")
        self.display_types(pokemon.types)
        self.display_abilities(pokemon.abilities)

    def display_sprite_img(self, sprites, sprite):
        data = requests.get(sprites[sprite]).content
        raw_bytes = pil_image.open(BytesIO(data))
        img = pil_image_tk.PhotoImage(raw_bytes)
        self.imgLbl.configure(image=img)
        self.images = []
        self.images.append(img)
        self.images.append(sprite)

    @classmethod
    def convert_link_2_img(cls, link):
        data = requests.get(link).content
        raw_bytes = pil_image.open(BytesIO(data))
        return pil_image_tk.PhotoImage(raw_bytes)

    colort = {
        "fire": "red", "water": "blue", "ground": "brown",
        "poison": "purple", "grass": "green", "bug": "lawn green",
        "dragon": "slate blue", "fighting": "IndianRed1",
        "flying": "sky blue", "ghost": "plum1", "psychic": "pink",
        "ice": "PaleTurquoise1", "electric": "yellow",
        "rock": "burlywood3"
    }

    @classmethod
    def type_colours(cls, color):
        if color in cls.colort:
            return cls.colort[color]
        return "grey"

    def destroy_all_in_frame(self, frame_slavetype):
        list_grid = frame_slavetype()
        for item in list_grid:
            item.destroy()

    def display_types(self, types):
        self.destroy_all_in_frame(self.types_frame.pack_slaves)
        for t in types:
            lbl = tk.Label(self.types_frame, text=t,
                           bg=self.type_colours(t), padx=10)
            lbl.pack(side="left")

    def create_add_delete_buttons(self, xcoord, ycoord):
        frame = tk.Frame(self.root, bg="white")
        frame.grid(column=xcoord, row=ycoord, sticky="n")
        add_button = tk.Button(frame, text="add",
                               command=self.add_pokemon_menu)
        add_button.pack(side="left", padx=(0, 10), ipadx=7)
        delete_button = tk.Button(frame, text="delete",
                                  command=self.del_pokemon)
        delete_button.pack(side="left", padx=(0, 15))

    def add_pokemon_menu(self):
        self.popup = tk.Tk()
        textfield = tk.Entry(self.popup)
        textfield.pack(side="left")
        enter = tk.Button(self.popup, text="enter",
                          command=lambda:
                          self.write_pokemon(textfield.get()))
        enter.pack(side="left")

    def write_pokemon(self, name):
        print(name)
        if Pokemonster.add_pokemon(name) == 0:
            self.listbox.insert("end", name)
            self.popup.destroy()

    def del_pokemon(self):
        try:
            Pokemonster.pokedex.pop(self.listbox.curselection()[0])
            self.listbox.delete(tk.ACTIVE)
        except IndexError:
            return

    def display_abilities(self, abilities):
        self.destroy_all_in_frame(self.abilities_frame.grid_slaves)
        positions: list = [(0, 0), (1, 0), (0, 1), (1, 1)]
        count: int = 0
        for ability in abilities:
            tk.Button(self.abilities_frame, text=ability.name,
                      command=lambda a=ability:
                      self.display_ability_info(a.info)
                      ).grid(column=positions[count][0],
                             row=positions[count][1])
            count += 1

    def display_ability_info(self, ability_info):
        self.text.config(text=ability_info)

    def toggle_form(self, *event):
        pokemon: Pokemonster = self.get_current_selection()
        if "default" in self.images:
            self.display_sprite_img(pokemon.sprites, "shiny")
        else:
            self.display_sprite_img(pokemon.sprites, "default")
