from Jumpscale import j

logger = j.logger.get('schema.log')

class Schema:
    def __init__(self, schema=None):
        self.schema = schema
        self.schema_obj = None
        self.log = logger
        if not self.schema:
            self.schema = """
                          @url = test.schema
                          name = (S)
                          """
            self.logger.info("default schema is used")
            
    @property
    def schema_object(self):
        self.schema_obj = j.data.schema.get(schema_text_path=self.schema)
        return self.schema_obj
   
    def new(self):
        self.schema_obj = self.schema_obj or self.schema_object
        return self.schema_obj.new()
    
