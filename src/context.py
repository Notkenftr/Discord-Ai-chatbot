class Context:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def init(self):
        if self._initialized:
            return self

        self.logging = None
        self._initialized = True
        return self