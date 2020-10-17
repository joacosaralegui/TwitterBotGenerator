class RasaObject:
    _idx = 0

    def __init__(self, texts):
        self.texts = texts
        RasaObject._idx += 1
        self._hash = RasaObject._idx

    def get_id(self):
        return self._id

    def join(obj1, obj2, Type):
        texts = list(set(obj1.texts).union(set(obj2.texts)))
        return Type(texts)
        
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, RasaObject):
            return self.texts == other.texts
        return False

    def __hash__(self):
        return self._hash

class Intent(RasaObject):

    def __init__(self, texts):
        super().__init__(texts)
        self._id = f'intent_{RasaObject._idx}'

    def nlu_declaration(self):
        text_str = "".join(f"- \"{t}\"\n" for t in self.texts)
        return f"## intent:{self._id}\n{text_str}\n"  

    def domain_declaration(self):
        return f"  - {self._id}\n"

    def story_declaration(self):
        return f"* {self._id}\n"
        

class Response(RasaObject):

    def __init__(self, texts):
        super().__init__(texts)
        self._id = f'utter_{RasaObject._idx}'

    def domain_declaration(self):
        text_str = "".join([f"    - text: \"{t}\"\n\n" for t in self.texts])
        return f"  {self._id}:\n{text_str}\n"

    def story_declaration(self):
        return f"  - {self._id}\n"