#Script de inicialización de la Aplicación lIA
#imports
import os
from create_tables import database
import winlia


script_dir = os.path.dirname(os.path.abspath(__file__))
#variables
path_database = os.path.join(script_dir, 'database/lia.db')
path_css = os.path.join(script_dir, 'winlia.css')
dat_database = ''
#functions

def exist_path(path, file=True):
    if file:
        file_exists = os.path.isfile(path)
    else:
        file_exists = os.path.isdir(path)
    return file_exists





def check_configs(path):
    #chequeamos si existe una Api Key.
    pass    
    #chequeamos que esten cargados las carpetas.



if __name__ == "__main__":
    #Chequeo base de datos.
    obj_database = database(path_database)
    if not exist_path(path_database):
        winlia.show_message("[-] Base de datos no encontrada la generaremos.", path_css, 3000)
        obj_database.create_database()
    else:
        winlia.show_message("[+] Base de datos encontrada, cargaremos info.", path_css, 3000)
        data_base = obj_database.data_base
    #Chequeos generales.


