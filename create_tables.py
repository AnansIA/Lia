from obj_sqlite import ObjSqlite

class database:

    def __init__(self, path):
        self.path = path


    data_base = {'tables': {
                     'anasist' : {
                                    'id': 'P',  # INTEGER PRIMARY KEY
                                    'name': 'T(30)U',  # 
                                    'model': 'T(20)',  # 
                                    'tools' : 'T',
                                    'instructions' : 'T',
                                    'files' : 'T',
                                    'threads' : 'I',
                                    'functions' : 'T'
                                },

                     'gral_config' : {
                                    'id': 'P',  # INTEGER PRIMARY KEY
                                    'api_key' : 'T(30)',
                                    'database' : 'T(60)',
                                    'documents' : 'T(60)',
                                    'downloads' : 'T(60)',
                                    'images'    : 'T(60)',
                                    'macros'    : 'T(60)',
                                    'videos'    : 'T(60)',
                                    'audios'    : 'T(60)'
                                    },
                     'threads' : {
                                   'id' : 'P',
                                   'name' : 'T(30)',
                                   'obs' : 'T'
                                 },
                     'functions' : {
                                   'id' : 'P',
                                   'name' : 'T(30)',
                                   'description' : 'T',
                         },
                     'functions_parameters' : {
                                   'id' : 'P',
                                  'functions' : 'I',
                                   'type' : 'T(30)',
                                   'properties' : 'T',
                                   'required' : 'T'
                         },
                     'functions_history' : {
                                   'id' : 'P',
                                   'functions' : 'I',
                                   'date' : 'T', #format yyyy-mm-dd
                                   'datetime' : 'T', #format HH:MM:SS
                                   'output'  : 'T',
                                   'ok' : 'I'
                         }

         }
     }

    def create_database(self):
        db = ObjSqlite(self.path)
        for item in self.data_base['tables']:
            db.create_table(item, self.data_base['tables'][item])


        
