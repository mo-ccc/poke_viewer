# poke viewer

Application name: poke viewer
Purpose: to view pokemon in their stock and shiny form with a gui
Target: anyone of interest
Reason for development: To attempt to gain familiarirty with the tkinter library as well as to attempt to develop in python an application with automated testing alongside the use of a CI/CD pipeline

Poke viewer is an application that is built entirely on python3. Poke viewer will use 2 way communication to retrieve data from the pokeapi.co service that will be used as a backend to the gui frontend that poke viewer presents.

2 Way communication Break Down:
The application will take user input using the gui. there will be one drop down list containing 152 objects that can be selected on and a button to perform a further action with the context of the currently selected object. 

Upon selecting one of the objects from the drop down list a request will be made to pokeapi.co to retrieve the json data of the selected object. From this json another request will be made to a link contained within that will produce another json. From both files data will be parsed and displayed to the user in the form of text. For the images further api requests will be made to download them to the session.

The single button in the application will access the json of the currently displayed object to request another image be displayed. Clicking the button again will revert changes. This revert pattern will continue until a new object is selected from the drop down menu.

Modules used:
-The requests library will be used to download the json files from the internet
-The json library will be used to parse the json files that are downloaded
-The tkinter library will be used to generate the graphical user interface

User Interaction:
-The user will use the mouse to make a selection from a tkinter option-menu
-The user will be able to toggle a tkinter button with mouse click