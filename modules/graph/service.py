from core.service import Service

from graph_theory.IO.GraphLoaderJSON import GraphLoaderJSON
from graph_theory.controller.GraphController import GraphController
from graph_theory.engine.GraphViewer import GraphViewer

from .commands import *
import glob


class GraphTheoryService(Service):
    displayed_name = "Теорія графів"

    def __init__(self, context):
        super().__init__(context)
        self.default_schema = r"D:\python\python\IndividualCreativeAssignment\modules\graph\schemas\graph_schema.json"
        self.schema_files = []
        self.picked_schema = None
        self.graph = None
        self.controller = None
        self.viewer = None

        self.register_command(ShowSchema.name, ShowSchema)
        self.register_command(InitSchema.name, InitSchema)
        self.register_command(InitGraph.name, InitGraph)
        # self.register_command(SetupViewer.name, SetupViewer)

    def get_schema_files(self):
        self.schema_files = glob.glob('modules/graph/schemas/*.json')
        menu = [f"{i + 1}. {schema}" for i, schema in enumerate(self.schema_files)]
        menu.insert(0, "Оберіть схему")
        return "\n".join(menu)

    def pick_schema(self, schema_index):
        max_index = len(self.schema_files)
        if not 1 <= max_index <= max_index:
            raise ValueError("Не коректний індекс")
        self.load_graph_from_json(self.schema_files[schema_index-1])
        return "Схему завантажено"

    def load_graph_from_json(self, schema_path):
        self.graph = GraphLoaderJSON().load(self.default_schema)

    def setup_controller(self):
        if not self.graph:
            raise BaseException("Немає завантаженого графа")
        self.controller = GraphController(self.graph)

    def test_graph(self):
        return str(self.graph)

    def setup_viewer(self):
        self.viewer = GraphViewer(self.controller, width=1000, height=800)
        self.viewer.run()
