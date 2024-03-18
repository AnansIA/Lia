import configparser

class configurations():
    file = "config.ini"


    def get_api_key(self):
        return str(self.read_config('gral', 'api_key'))



    def get_config(self, name_assistant):
        configs = {}
        configs['name'] = str(self.read_config(name_assistant, 'name'))
        configs['instructions'] = str(self.read_config(name_assistant, 'instructions'))
        configs['tools'] = {'type' : self.read_config(name_assistant, 'tools')}
        configs['model'] = str(self.read_config(name_assistant, 'model'))
        return configs
 
    def read_config(self, section, option):
        """
        Lee el valor de una configuración específica de un archivo INI.

        Parámetros:
        - seccion: La sección en el archivo de configuración donde se encuentra la opción.
        - opcion: La opción cuyo valor se desea leer.

        Retorna:
        - El valor de la opción solicitada.
        """
        config = configparser.ConfigParser()
        config.read(self.file)
        value = config.get(section, option)
        return value

    def update_config(self, section, option, new_value):
        """
        Actualiza el valor de una configuración específica en un archivo INI.

        Parámetros:
        - seccion: La sección en el archivo de configuración donde se encuentra la opción.
        - opcion: La opción cuyo valor se desea actualizar.
        - nuevo_valor: El nuevo valor para la opción especificada.

        Return:
        - String with the section, option and new value
        """
        config = configparser.ConfigParser()
        config.read(self.file)
        config.set(section, option, new_value)
        with open(self.file, 'w') as configfile:
            config.write(configfile)
        return f"the {option} in {section }modifycated is to {new_value}"


