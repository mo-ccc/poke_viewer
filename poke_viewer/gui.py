import tkinter
from pokemonster import Pokemonster

class Application():
    def __init__(self):
        self.master = None
        self.root = tkinter.Tk()
        self.root.geometry('350x250')
        self.create_pokedex_view(0, 0)
        
    def init_tkinter_vars(self):
        self.selected_pokemon_var = tkinter.StringVar()
    
    def create_pokedex_view(self, xcoord, ycoord):
        frame = tkinter.Frame(self.root)
        frame.grid(row=xcoord, column=ycoord)

        listbox = tkinter.Listbox(frame)
        listbox.pack(side="left")

        for pokemon in Pokemonster.list_pokedex():
            listbox.insert(tkinter.END, pokemon)

        listbox.bind("<<ListboxSelect>>", self.make_selection(listbox))
        listbox.select_set(0)
        self.make_selection(listbox)
  
    def make_selection(self, listbox):
        #gets the index of the current selection from the listbox
        index = listbox.curselection()[0]
        #uses index to retrieve name of pokemon
        name = Pokemonster.list_pokedex()[index]
        #initalizes pokemonster object from the name
        pokemon = Pokemonster(name)
        print(pokemon.to_string)
        