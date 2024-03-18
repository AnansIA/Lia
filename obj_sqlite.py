import sqlite3
from sqlite3 import Error


class ObjSqlite:
    _database = ''  # Nombre de la base de datos
    _con = None  # Conector
    _types = {  # Tipos soportados principalmente por SQLite3
        'I': 'INTEGER',
        'R': 'REAL',
        'T': 'TEXT',
        'B': 'BLOB',
        'P': 'PRIMARY KEY',
        'U': 'UNIQUE'
    }

    def __init__(self, database, connect=True):
        """Initialize the class with the name of the database as a parameter."""
        self._database = database
        if connect:
            self.sql_connection()

    def sql_connection(self):
        """Connect to the database."""
        try:
            self._con = sqlite3.connect(self._database)
        except Error as e:
            print(e)

    def sql_execute(self, sql: str, params=(), commit=True):
        """Execute SQL command."""
        try:
            cursor = self._con.cursor()
            cursor.execute(sql, params)
            if commit:
                self._con.commit()
            return [True, cursor.lastrowid or True]
        except Error as e:
            return [False, e]

    def sql_query(self, sql: str, params=()):
        """Query SQL and return rows."""
        cursor = self._con.cursor()
        try:
            cursor.execute(sql, params)
            return cursor.fetchall()
        except Error as e:
            return [e]

    def delete(self, table, value, column='id'):
        """Delete a record."""
        sql = f"DELETE FROM {table} WHERE {column} = ?"
        return self.sql_execute(sql, (value,))

    def insert(self, table: str, values: dict):
        """Insert a new record."""
        columns = ', '.join(values.keys())
        placeholders = ', '.join(['?' for _ in values])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return self.sql_execute(sql, tuple(values.values()))

    def select_all(self, table, columns='*'):
        """Select all records from a table."""
        sql = f"SELECT {columns} FROM {table}"
        return self.sql_query(sql)

    def select_count_rows(self, table: str):
        """Count rows in a table."""
        sql = f"SELECT COUNT(*) FROM {table}"
        result = self.sql_query(sql)
        return result[0][0] if result else 0

    def select_where(self, table: str, condition: str, columns='*'):
        """Select records based on a condition."""
        sql = f"SELECT {columns} FROM {table} WHERE {condition}"
        return self.sql_query(sql)

    def update(self, table: str, values: dict, condition: str):
        """Update records based on a condition."""
        set_clause = ', '.join([f"{k} = ?" for k in values])
        sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        return self.sql_execute(sql, tuple(values.values()))

  
    def create_table(self, table: str, fields: dict):
        """Create a table with given fields, interpreting compact type definitions correctly."""
        field_definitions = []
        type_mappings = {
            'T': 'TEXT',
            'I': 'INTEGER',
            'R': 'REAL',
            'B': 'BLOB',
            'C': 'TEXT',  # CHAR and VARCHAR mapped to TEXT
            'V': 'TEXT',  # VARCHAR mapped to TEXT
            'L': 'TEXT',  # CLOB mapped to TEXT
            'INT': 'INTEGER',
            'BI': 'INTEGER',  # BIGINT mapped to INTEGER
            'SI': 'INTEGER',  # SMALLINT mapped to INTEGER
            'F': 'REAL',  # FLOAT
            'D': 'REAL',  # DOUBLE mapped to REAL
            'DE': 'NUMERIC',  # DECIMAL
            'BOOL': 'INTEGER',  # BOOLEAN
            'DATE': 'TEXT',  # DATE
            'DT': 'TEXT',  # DATETIME
        }

        for field, definition in fields.items():
            column_type = []
            column_constraints = []

            # Handle PRIMARY KEY, UNIQUE, and type size
            if 'P' in definition:
                column_type.append('INTEGER PRIMARY KEY')
            if 'U' in definition:
                column_constraints.append('UNIQUE')

            # Type mapping
            for key, value in type_mappings.items():
                if key in definition:
                    column_type.append(value)
                    break  # Stop after the first match to prevent multiple type assignments

            # Size for VARCHAR
            if '(' in definition and ')' in definition:
                size = definition[definition.find("(")+1:definition.find(")")]
                column_type[-1] += f"({size})"  # Append size to the last type

            field_definitions.append(f"{field} {' '.join(column_type + column_constraints)}")

        sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join(field_definitions)})"
        print(sql)
        return self.sql_execute(sql, commit=True)


    def close(self):
        """Close the database connection."""
        if self._con:
            self._con.close()



    def insert(self, table, data):
        '''Inserta un registro en la tabla especificada.
        
        Args:
            table (str): Nombre de la tabla.
            data (dict): Diccionario con los datos a insertar.
        '''
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f'INSERT INTO {table} ({columns}) VALUES ({placeholders})'
        try:
            cur = self._con.cursor()
            cur.execute(sql, list(data.values()))
            self._con.commit()
        except Error as e:
            print(f"Error al insertar en la tabla {table}: {e}")

    def update(self, table, data, conditions):
        '''Actualiza registros en la tabla especificada según las condiciones dadas.
        
        Args:
            table (str): Nombre de la tabla.
            data (dict): Diccionario con los datos a actualizar.
            conditions (str): Condiciones para la actualización.
        '''
        set_clause = ', '.join([f"{k} = ?" for k in data])
        sql = f'UPDATE {table} SET {set_clause} WHERE {conditions}'
        try:
            cur = self._con.cursor()
            cur.execute(sql, list(data.values()))
            self._con.commit()
        except Error as e:
            print(f"Error al actualizar la tabla {table}: {e}")

    def delete(self, table, conditions):
        '''Elimina registros de la tabla especificada según las condiciones dadas.
        
        Args:
            table (str): Nombre de la tabla.
            conditions (str): Condiciones para la eliminación.
        '''
        sql = f'DELETE FROM {table} WHERE {conditions}'
        try:
            cur = self._con.cursor()
            cur.execute(sql)
            self._con.commit()
        except Error as e:
            print(f"Error al eliminar de la tabla {table}: {e}")

    def select_by_id(self, table, record_id):
        '''Selecciona un registro por su ID.
        
        Args:
            table (str): Nombre de la tabla.
            record_id (int): ID del registro a seleccionar.
            
        Returns:
            dict: Diccionario con los datos del registro o None si no se encuentra.
        '''
        sql = f'SELECT * FROM {table} WHERE id = ?'
        cur = self._con.cursor()
        cur.execute(sql, (record_id,))
        record = cur.fetchone()
        if record:
            return dict(record)
        else:
            return None

    def select(self, table, conditions=None, limit=None):
        '''Selecciona registros de la tabla según las condiciones dadas.
        
        Args:
            table (str): Nombre de la tabla.
            conditions (str, optional): Condiciones para la selección.
            limit (int, optional): Límite de registros a retornar.
            
        Returns:
            list of dict: Lista de diccionarios con los datos de los registros.
        '''
        sql = f'SELECT * FROM {table}'
        if conditions:
            sql += f' WHERE {conditions}'
        if limit:
            sql += f' LIMIT {limit}'
        cur = self._con.cursor()
        cur.execute(sql)
        records = cur.fetchall()
        return [dict(record) for record in records]
