import tkinter as tk
from pokemonster import Pokemonster
from io import BytesIO
from PIL import Image as pil_image, ImageTk as pil_image_tk
import requests


class Application():
    def __init__(self):
        self.root = tk.Tk()
        # make root window background white
        self.root.configure(bg="white")
        self.root.title("poke_viewer 1.0")
        # make root window fixed
        self.root.resizable(False, False)
        self.root.geometry('500x200')
        self.images = []
        # tkinter label to contain image
        self.imgLbl = tk.Label(self.root, borderwidth=2, relief="groove",
                               width=150, height=150, bg="white")
        self.imgLbl.grid(column=1, row=0, rowspan=2)
        # tkinter frame to contain types, abilities, ability_info
        self.info_container = tk.Frame(self.root, height=30, bg="white")
        self.info_container.grid(column=2, row=0, sticky="nw",
                                 rowspan=3)
        # frame to hold types
        self.types_frame = tk.Frame(self.info_container, bg="white")
        self.types_frame.pack(side="top")
        # frame to hold abilities
        self.abilities_frame = tk.Frame(self.info_container, bg="white")
        self.abilities_frame.pack(side="top")
        # ability_info label instantiated
        self.ability_info_text = tk.Label(self.info_container,
                                          text="click a button",
                                          width=30, wraplength=200,
                                          anchor="nw", justify="left",
                                          bg="white")
        self.ability_info_text.pack(side="bottom")
        # tkinter button to toggle between shiny and default img
        self.shiny_button = tk.Button(self.root, text="shiny",
                                      command=self.toggle_form)
        self.shiny_button.grid(column=1, row=2)
        # self.listbox is created with a scrollbar
        # method below
        self.create_pokedex_widget(0, 0)
        # creates an add and delete button under listbox
        # method below
        self.create_add_delete_buttons(0, 2)
        # popup
        # creates a new window
        self.popup = tk.Tk()
        # hides window from view
        self.popup.withdraw()
        # if the root window is escaped call self.root_terminate...
        self.root.protocol("WM_DELETE_WINDOW",
                           lambda: self.root_terminate_protocol())
        '''
        if the popup window is escaped withdraw the popup instead of
        terminating
        '''
        self.popup.protocol("WM_DELETE_WINDOW",
                            lambda: self.popup.withdraw())
        self.popup.title("add pokemon")
        self.popup.resizable(False, False)
        # popup window has an entry field to take user input
        self.textfield = tk.Entry(self.popup)
        self.textfield.pack(side="left", padx=20, pady=10)
        '''
        button next to entry field to submit user input
        on click calls write_pokemon passing textfield value
        as a parameter
        '''
        enter = tk.Button(self.popup, text="enter",
                          command=lambda:
                          self.write_pokemon(self.textfield.get()))
        enter.pack(side="left", padx=5)

    def root_terminate_protocol(self):
        # terminates the root window
        self.root.destroy()
        # terminates the pop up window
        # popup should go after or the application may stall
        self.popup.destroy()

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
        for pokemon in Pokemonster.pokedex:
            self.listbox.insert(tk.END, pokemon)

        # set listbox selection to 0
        self.listbox.select_set(0)
        # bind list box selection to function make_selection
        self.listbox.bind("<<ListboxSelect>>", self.make_selection)
        # call make selection so that the selected element <0> is used
        self.make_selection()

    @property
    def current_selection(self):
        # gets the index of the current selection from the listbox
        index: int = self.listbox.curselection()[0]
        # uses index to retrieve name of pokemon
        name: str = Pokemonster.pokedex[index]
        # initalizes pokemonster object from the name
        return Pokemonster(name)

    def make_selection(self, *events):
        # stores pokemon object from function return
        pokemon: Pokemonster = self.current_selection
        print(pokemon.to_string)
        # passes the pokemon attributes to the functions
        self.display_sprite_img(pokemon.sprites, "default")
        self.display_types(pokemon.types)
        self.display_abilities(pokemon.abilities)

    '''
    uses link to make a request to download the sprite image.
    the image is made into a type compatible with tkinter
    using the pillow module called by convert_link_2_img
    function.
    the image is appended to the images list along with the
    name of the image. Doing so keeps the image in memory
    and prevents deallocation.
    '''
    def display_sprite_img(self, sprites, sprite):
        img = self.convert_link_2_img(sprites[sprite])
        photo = pil_image_tk.PhotoImage(img)
        self.imgLbl.configure(image=photo)
        self.images = []
        self.images.append(photo)
        self.images.append(sprite)

    # converts a http link of a png image into a pillow image
    # pillow image can be displayed by tkinter
    @classmethod
    def convert_link_2_img(cls, link):
        data = requests.get(link).content
        return pil_image.open(BytesIO(data))

    '''
    a dictionary containing element type keys with corresponding
    color values
    '''
    colort: dict = {
        "fire": "red", "water": "blue", "ground": "brown",
        "poison": "purple", "grass": "green", "bug": "lawn green",
        "dragon": "slate blue", "fighting": "IndianRed1",
        "flying": "sky blue", "ghost": "plum1", "psychic": "pink",
        "ice": "PaleTurquoise1", "electric": "yellow",
        "rock": "burlywood3"
    }

    '''
    uses the colort dictionary to get the appropriate color
    to be displayed by tkinter. if the color is not in the
    dictionary this function returns "grey"
    '''
    @classmethod
    def type_2_color(cls, color):
        if color in cls.colort:
            return cls.colort[color]
        return "grey"

    # destroys all tkinter widgets in a frame
    # frame is passed in with the slave type following
    # e.g. destroy_all_in_fram(frame.pack_slaves)
    def destroy_all_in_frame(self, frame_slavetype):
        slave_list = frame_slavetype()
        for widget in slave_list:
            widget.destroy()

    def display_types(self, types):
        # destroys all widgets in type frame
        self.destroy_all_in_frame(self.types_frame.pack_slaves)
        # replaces those widgets with new label widgets
        for t in types:
            lbl = tk.Label(self.types_frame, text=t,
                           bg=self.type_2_color(t), padx=10)
            lbl.pack(side="left")

    # creates a frame and creates two button widgets inside
    def create_add_delete_buttons(self, xcoord, ycoord):
        frame = tk.Frame(self.root, bg="white")
        frame.grid(column=xcoord, row=ycoord, sticky="n")
        # add_button calls the add_pokemon_menu function on click
        add_button = tk.Button(frame, text="add",
                               command=self.add_pokemon_menu)
        add_button.pack(side="left", padx=(0, 10), ipadx=7)
        # delete_button calls the del_pokemon function on click
        delete_button = tk.Button(frame, text="delete",
                                  command=self.del_pokemon)
        delete_button.pack(side="left", padx=(0, 15))

    def add_pokemon_menu(self):
        self.popup.deiconify()

    def write_pokemon(self, name):
        print(name)
        # adds the pokemon to the Pokemonster.pokedex list
        # checks return value for error
        if Pokemonster.add_pokemon(name) == 0:
            '''
            if pokemon was successfully added insert it in the listbox
            then remove the contents currently in the textfield
            then hide the popup.
            '''
            self.listbox.insert("end", name)
            self.textfield.delete(0, "end")
            self.popup.withdraw()

    def del_pokemon(self):
        try:
            # removes pokemon from pokedex list in Pokemonster class
            Pokemonster.remove_pokemon(self.current_selection.name)
            # then removes the pokemon from the listbox
            self.listbox.delete(tk.ACTIVE)
        except IndexError:
            return

    def display_abilities(self, abilities):
        # destroys all slaves in abilities frame
        self.destroy_all_in_frame(self.abilities_frame.grid_slaves)
        # a list of grid coordinates
        positions: list = [(0, 0), (1, 0), (0, 1), (1, 1)]
        count: int = 0
        # for each ability in abilities create a button
        # the count is used to place it on a grid
        # the button calls the display_ability_info function
        # the button passes the correspond ability info the function
        for ability in abilities:
            tk.Button(self.abilities_frame, text=ability.name,
                      command=lambda a=ability:
                      self.display_ability_info(a.info)
                      ).grid(column=positions[count][0],
                             row=positions[count][1])
            # count is incremented for next ability
            count += 1
            if count > 3:
                return

    def display_ability_info(self, ability_info):
        # changes info text to ability_info parameter
        self.ability_info_text.config(text=ability_info)

    # called by the shiny button
    def toggle_form(self, *events):
        try:
            pokemon: Pokemonster = self.current_selection
        except IndexError:
            print("No pokemon")
            return
        '''
        if self.images currently has the default image
        display the shiny sprite
        otherwise display the default sprite
        '''
        if "default" in self.images:
            self.display_sprite_img(pokemon.sprites, "shiny")
        else:
            self.display_sprite_img(pokemon.sprites, "default")
