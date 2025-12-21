from core.service import Service

class GraphTheoryService(Service):
    displayed_name = "Теорія графів"

    def __init__(self, context):
        super().__init__(context)