import openai
from config import configurations

class Asistente:

    def __init__(self):
        """
        Inicializa una instancia de la clase Asistente.
        """
        self.configs = None  # Carga la configuración desde el módulo de configuración.
        self.assistant = None  # Inicialmente, no hay ningún asistente configurado.

    

    def load_assistant(self, assistant):
        self.configs = configurations()
        values = self.configs.get_config(assistant)
        openai.api_key = self.configs.get_api_key()  # Establece la clave API de OpenAI.
        return self.create_assistant(values['name'],
                                     values['instructions'],
                                     values['tools'],
                                     values['model'])


    def create_assistant(self, name, instructions, tools, model):
        """
        Crea un nuevo asistente en la plataforma de OpenAI.

        Args:
            name (str): El nombre del asistente.
            instructions (str): Las instrucciones para el asistente.
            tools (list): Lista de herramientas habilitadas para el asistente.
            model (str): El modelo de OpenAI a utilizar.

        Returns:
            dict: La respuesta de la API de OpenAI al crear el asistente.
        """
        self.assistant = openai.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=model
        )
        return self.assistant

    

    def retrieve_assistant(self, assistant_id):
        """
        Recupera un asistente existente por su ID.

        Args:
            assistant_id (str): El ID del asistente a recuperar.

        Returns:
            dict: La respuesta de la API de OpenAI al recuperar el asistente.
        """
        self.assistant = openai.beta.assistants.retrieve(assistant_id)
        return self.assistant

    

    def delete_assistant(self, assistant_id):
        """
        Elimina un asistente existente por su ID.

        Args:
            assistant_id (str): El ID del asistente a eliminar.

        Returns:
            dict: La respuesta de la API de OpenAI al eliminar el asistente.
        """
        response = openai.beta.assistants.delete(assistant_id)
        return response

    

    def update_assistant(self, assistant_id, name, instructions, tools, model):
        """
        Actualiza un asistente existente por su ID.

        Args:
            assistant_id (str): El ID del asistente a actualizar.
            name (str): El nuevo nombre del asistente.
            instructions (str): Las nuevas instrucciones para el asistente.
            tools (list): La nueva lista de herramientas para el asistente.
            model (str): El nuevo modelo de OpenAI a utilizar.

        Returns:
            dict: La respuesta de la API de OpenAI al actualizar el asistente.
        """
        self.assistant = openai.beta.assistants.update(
            assistant_id,
            name=name,
            instructions=instructions,
            tools=tools,
            model=model
        )
        return self.assistant

    

    def list_assistants(self):
        """
        Lista todos los asistentes existentes.

        Returns:
            dict: La respuesta de la API de OpenAI al listar los asistentes.
        """
        return openai.beta.assistants.list()

    

    def create_file(self, file_path, purpose):
        """
        Crea un nuevo archivo en la plataforma de OpenAI.

        Args:
            file_path (str): La ruta al archivo que se va a cargar.
            purpose (str): El propósito del archivo.

        Returns:
            dict: La respuesta de la API de OpenAI al crear el archivo.
        """
        with open(file_path, 'rb') as file:
            response = openai.files.create(file=file, purpose=purpose)
        return response

    

    def delete_file(self, file_id):
        """
        Elimina un archivo existente por su ID.

        Args:
            file_id (str): El ID del archivo a eliminar.

        Returns:
            dict: La respuesta de la API de OpenAI al eliminar el archivo.
        """
        response = openai.files.delete(file_id)
        return response

    


    def create_thread(self):
        """
        Crea un nuevo thread para la conversación con el asistente.

        Returns:
            dict: La respuesta de la API de OpenAI al crear el thread.
        """
        thread = openai.beta.threads.create()
        return thread

    


    def retrieve_thread(self, thread_id):
        """
        Recupera un thread existente por su ID.

        Args:
            thread_id (str): El ID del thread a recuperar.

        Returns:
            dict: La respuesta de la API de OpenAI al recuperar el thread.
        """
        thread = openai.beta.threads.retrieve(thread_id)
        return thread

    


    def create_message(self, thread_id, role, content, file_ids, metadata=None):
        """
        Crea un nuevo mensaje en un thread existente.

        Args:
            thread_id (str): El ID del thread donde se creará el mensaje.
            role (str): El rol del creador del mensaje (p.ej., 'user').
            content (str): El contenido del mensaje.
            file_ids (list): Lista de IDs de archivos asociados al mensaje.
            metadata (dict, optional): Metadatos adicionales para el mensaje.

        Returns:
            dict: La respuesta de la API de OpenAI al crear el mensaje.
        """
        message = openai.beta.threads.messages.create(
            thread_id=thread_id,
            role=role,
            content=content,
            file_ids=file_ids,
            metadata=metadata
        )
        return message

    


    def retrieve_message(self, thread_id, message_id):
        """
        Recupera un mensaje existente por su ID.

        Args:
            thread_id (str): El ID del thread del mensaje.
            message_id (str): El ID del mensaje a recuperar.

        Returns:
            dict: La respuesta de la API de OpenAI al recuperar el mensaje.
        """
        message = openai.beta.threads.messages.retrieve(thread_id=thread_id, message_id=message_id)
        return message

    



    def create_run(self, thread_id, assistant_id, model=None, instructions=None, additional_instructions=None, tools=None, metadata=None):
        """
        Crea una nueva ejecución (run) para un asistente en un thread específico.

        Args:
            thread_id (str): El ID del thread donde se ejecutará el run.
            assistant_id (str): El ID del asistente que ejecutará el run.
            model (str, optional): El modelo de OpenAI a utilizar en el run.
            instructions (str, optional): Las instrucciones para el asistente en el run.
            additional_instructions (str, optional): Instrucciones adicionales para el run.
            tools (list, optional): Herramientas habilitadas para el asistente en el run.
            metadata (dict, optional): Metadatos adicionales para el run
        """
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            model=model,
            instructions=instructions,
            additional_instructions=additional_instructions,
            tools=tools,
            metadata=metadata,
        )
        return run

    


    def retrieve_run(self, thread_id, run_id):
        """
        Recupera una ejecución (run) existente por su ID.

        Args:
            thread_id (str): El ID del thread asociado al run.
            run_id (str): El ID del run a recuperar.

        Returns:
            dict: La respuesta de la API de OpenAI al recuperar el run.
        """
        run = openai.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        return run

    


    def cancel_run(self, thread_id, run_id):
        """
        Cancela una ejecución (run) en progreso por su ID.

        Args:
            thread_id (str): El ID del thread asociado al run.
            run_id (str): El ID del run a cancelar.

        Returns:
            dict: La respuesta de la API de OpenAI al cancelar el run.
        """
        run = openai.beta.threads.runs.cancel(thread_id=thread_id, run_id=run_id)
        return run

    


    def list_runs(self, thread_id):
        """
        Lista todas las ejecuciones (runs) existentes en un thread específico.

        Args:
            thread_id (str): El ID del thread para listar los runs.

        Returns:
            dict: La respuesta de la API de OpenAI al listar los runs.
        """
        runs = openai.beta.threads.runs.list(thread_id=thread_id)
        return runs




    def submit_tool_outputs_to_run(self, thread_id, run_id, tool_outputs):
        """
        Envía los resultados de las herramientas a una ejecución (run) que los requiere.

        Args:
            thread_id (str): El ID del thread asociado al run.
            run_id (str): El ID del run que requiere los resultados de las herramientas.
            tool_outputs (list): Lista de salidas de las herramientas.

        Returns:
            dict: La respuesta de la API de OpenAI al enviar los resultados de las herramientas al run.
        """
        run = openai.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_outputs
        )
        return run





class FunctionToolCreator:
    def __init__(self, name, description):
        """
        Inicializa una instancia de FunctionToolCreator.

        Args:
            name (str): Nombre de la función a crear.
            description (str): Descripción de la función.
        """
        self.name = name
        self.description = description
        self.parameters = {}

    def add_parameter(self, name, param_type, description):
        """
        Añade un parámetro a la función.

        Args:
            name (str): Nombre del parámetro.
            param_type (str): Tipo de dato del parámetro (p.ej., 'string').
            description (str): Descripción del parámetro.
        """
        self.parameters[name] = {
            "type": param_type,
            "description": description,
        }

    def create_function_tool_for_python_code_with_url(self) -> dict:
        """
        Prepara la función para ejecutar código Python con acceso a URL.

        Returns:
            dict: La herramienta de función preparada para ser utilizada.
        """
        self.add_parameter("code", "string", "El código Python generado por el intérprete de código.")
        self.add_parameter("url", "string", "La URL a la que acceder para obtener datos.")
        
        return self.create_function_tool()

    def create_function_tool(self) -> dict:
        """
        Crea la herramienta de función con los parámetros especificados.

        Returns:
            dict: La herramienta de función configurada.
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": {
                    "type": "object",
                    "properties": self.parameters,
                    "required": list(self.parameters.keys())
                },
            },
        }

