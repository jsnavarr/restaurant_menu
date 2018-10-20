## restaurant_menu exercise
**restaurant_menu** is a _udacity_ exercise to demostrate what was learned in the classroom. 
It list all the restaurants in the database (restaurantmenu) with links to edit/delete them and to show their menu.
It also display the menu for each restaurant with links to edit/delete any menu item.

## How to run the program
**log_project** has been tested using _python 3.6.3_ so the recommendation is to use that version. You can try other version and program may still run.
To run the program just open a terminal and run:`python restaurant_menu.py`

## restaurant_menu design
**restaurant_menu** code design is simple, it follows a CRUD functionality for restaurant and menu so there are 4 functions (CRUD) for each of them:
  - **C**reate
    - to add a new restaurant
    - to add a new menu item
  - **R**ead
    - to display all restaurants
    - to display all menu items in a restaurant
  - **U**pdate
    - to edit a restaurant name
    - to edit a menu item (name, price, description, course)
  - **D**elete
    - to delete a restaurant
    - to delete a menu item