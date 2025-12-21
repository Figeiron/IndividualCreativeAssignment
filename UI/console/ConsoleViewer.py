from core.events import Event, EventType
import winsound


class ConsoleViewer:
    def __init__(self, context):
        self.context = context
        self.commands = {}
        self.services = {"Вийти": ""}

        self.exit_menu = {
            "вийти": {"EventType": EventType.EXIT},
            "повернутись в головне меню": {"EventType": EventType.SHOW_SERVICES_MENU},
        }

        self.running = True

    def handle_event(self, event):
        if event.type == EventType.EASTER_EGG:
            self.print_banner(str(event.data["message"]))
            winsound.PlaySound("sound/easter_egg_cs.wav", winsound.SND_FILENAME)

        if event.type == EventType.IDLE:
            self.show_exit_menu()
            self.pick_exit_menu_command()

        if event.type == EventType.SERVICE_AVAILABLE:
            service_name = event.data["service_name"]
            self.services[service_name] = event.data["service"]

        if event.type == EventType.COMMAND_AVAILABLE:
            command_name = event.data['name']
            self.commands[command_name] = {
                "command_cls": event.data["command_cls"],
                "service": event.data["service_name"]
            }

        if event.type == EventType.START:
            self.print_banner(self.context.data["app_name"])
            self.context.events.emit(Event(EventType.SHOW_SERVICES_MENU))

        if event.type == EventType.SHOW_SERVICES_MENU:
            self.show_service_menu()
            self.pick_service()

        if event.type == EventType.SERVICE_SELECTED:
            self.show_commands(event.data["service_name"])
            self.pick_command(event.data["service_name"])

        if event.type == EventType.EXECUTE_COMMAND:
            command_cls = self.commands[event.data["command_name"]]["command_cls"]
            service_cls = self.services[event.data["service_name"]]
            print(self.execute_command(command_cls, service_cls))

        if event.type == EventType.EXIT:
            self.running = False

        if event.type == EventType.ERROR:
            self.print_banner(str(event.data["error_message"]))

    @staticmethod
    def print_banner(title: str):
        rows = title.split("\n")
        rows_width = [len(row) for row in rows]
        max_width = max(rows_width) + 2

        print("╔" + "═" * max_width + "╗")
        for i, row in enumerate(rows):
            j = 0
            if rows_width[i] % 2 == 0:
                j = 1
            print(f"║{" " * int((max_width - rows_width[i] + j) / 2)}{row}{" " * int((max_width - rows_width[i]) / 2)}║")
        print("╚" + "═" * max_width + "╝")

    def show_service_menu(self):
        print("\n══ Доступні сервіси ══")
        for i, service in enumerate(self.services.keys(), 1):
            print(f"{i}. {service}")

    def show_exit_menu(self):
        print("\n══ Оберіть пункт ══")
        for i, service in enumerate(self.exit_menu.keys(), 1):
            print(f"{i}. {service}")

    def pick_exit_menu_command(self):
        while True:
            try:
                choice = int(input("\nОберіть пункт (номер): ")) - 1
                event_type = list(self.exit_menu.values())[choice]
                self.context.events.emit(Event(event_type["EventType"]))
                break
            except (ValueError, IndexError):
                print("Невірний вибір. Спробуйте ще раз.")

    def pick_service(self):
        while True:
            try:
                choice = int(input("\nОберіть сервіс (номер): ")) - 1
                if choice == 0:
                    self.context.events.emit(Event(EventType.EXIT))
                    break
                service_name = list(self.services.keys())[choice]
                self.context.events.emit(Event(EventType.SERVICE_SELECTED, service_name=service_name))
                break
            except (ValueError, IndexError):
                print("Невірний вибір. Спробуйте ще раз.")

    def show_commands(self, service_name):
        print(f"\n══ Команди сервісу '{service_name}' ══")
        commands_for_service = [k for k, v in self.commands.items() if v["service"] == service_name]
        for i, cmd_name in enumerate(commands_for_service, 1):
            print(f"{i}. {cmd_name}")
        print(f"{len(commands_for_service) + 1}. Повернутися до меню сервісів")  # опція Back

    def pick_command(self, service_name):
        commands_for_service = [k for k, v in self.commands.items() if v["service"] == service_name]
        while True:
            try:
                choice = int(input("\nОберіть команду (номер): "))
                if choice == len(commands_for_service) + 1:
                    self.context.events.emit(Event(EventType.SHOW_SERVICES_MENU))
                else:
                    cmd_name = commands_for_service[choice - 1]
                    self.context.events.emit(
                        Event(EventType.EXECUTE_COMMAND, command_name=cmd_name, service_name=service_name)
                    )
                break
            except (ValueError, IndexError):
                print("Невірний вибір. Спробуйте ще раз.")

    def execute_command(self, command_cls, service):
        if hasattr(command_cls, "description"):
            print(f"\nКоманда: {command_cls.description}")

        params = []
        if hasattr(command_cls, "expected_params"):
            for param in command_cls.expected_params:
                while True:
                    try:
                        value = input(f"Введіть {param}: ")
                        params.append(value)
                        break
                    except ValueError:
                        print("Невірне значення, спробуйте ще раз.")

        cmd_instance = command_cls(service, *params)
        result = cmd_instance.execute(self.context)
        return result
