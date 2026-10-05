class Task:
    name = ""
    description = ""

    def run(self, config):
        raise NotImplementedError
