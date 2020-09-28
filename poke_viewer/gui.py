import tkinter
from pokemonster import Pokemonster

class Application():
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.geometry('350x250')
        self.create_pokedex_widget(0, 0)
        self.create_sprite_widget(1, 0)
        
    def init_tkinter_vars(self):
        self.selected_pokemon_var = tkinter.StringVar()
    
    def create_pokedex_widget(self, xcoord, ycoord):
        frame = tkinter.Frame(self.root)
        frame.grid(row=xcoord, column=ycoord)

        self.listbox = tkinter.Listbox(frame)
        self.listbox.pack(side="left")

        for pokemon in Pokemonster.list_pokedex():
            self.listbox.insert(tkinter.END, pokemon)
        
        self.listbox.select_set(0)
        self.listbox.bind("<<ListboxSelect>>", self.make_selection)
        self.make_selection()
  
    def make_selection(self, event=None):
        #gets the index of the current selection from the listbox
        index = self.listbox.curselection()[0]
        #uses index to retrieve name of pokemon
        name = Pokemonster.list_pokedex()[index]
        #initalizes pokemonster object from the name
        self.pokemon = Pokemonster(name)
        print(self.pokemon.to_string)
        
    def convert_to_img(self, sprite):
        pass
    
    def create_sprite_widget(self, xcoord, ycoord):
        imgLbl = tkinter.Label(self.root, borderwidth=2, relief="groove",
                               width=150, height=150)
        imgLbl.grid(row=xcoord, column=ycoord)