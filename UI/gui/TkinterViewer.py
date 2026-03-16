import tkinter as tk
from core.events import Event, EventType
from core.parameter import ChoiceParameter


class TkinterViewer:
    def __init__(self, context):
        self.context = context
        self.root = tk.Tk()
        self.root.title("Individual Creative Assignment")
        self.root.geometry("1000x600")

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.services = {"Вийти": ""}
        self.commands = {}

        self.sidebar = tk.Frame(self.root, width=300, bg="#ffffff", relief="sunken", bd=1)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        self.sidebar.pack_propagate(False)

        self.footer = tk.Frame(self.root, height=30, bg="#ffffff", relief="sunken", bd=1)
        self.footer.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.status = tk.Label(self.footer, text="Ready", fg="black", bg="#ffffff", anchor="w")

        self.status.pack(fill=tk.X)

        self.main_area = tk.Frame(self.root, bg="white")
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.current_params_values = {}
        self.current_params_widgets = {}

    def on_closing(self):
        self.context.events.emit(Event(EventType.EXIT))

    def handle_event(self, event):
        self.status.config(text=event)
        if event.type == EventType.START:
            self.show_services_sidebar()

        elif event.type == EventType.SERVICE_AVAILABLE:
            service_name = event.data["service_name"]
            self.services[service_name] = event.data["service"]
            self.show_services_sidebar()

        elif event.type == EventType.COMMAND_AVAILABLE:
            command_name = event.data['name']
            self.commands[command_name] = {
                "command_cls": event.data["command_cls"],
                "service": event.data["service_name"]
            }

        elif event.type == EventType.SHOW_SERVICES_MENU:
            self.show_services_sidebar()

        elif event.type == EventType.SERVICE_SELECTED:
            self.show_commands_sidebar(event.data["service_name"])

        elif event.type == EventType.EXECUTE_COMMAND:
            self.show_params_form(event.data["service_name"], event.data["command_name"])

        elif event.type == EventType.COMMAND_EXECUTED:
            self.show_result("Результат", str(event.data["result"]))

        elif event.type == EventType.ERROR:
            self.show_result("Помилка", str(event.data["error_message"]))

        elif event.type == EventType.EXIT:
            self.root.destroy()

    def clear_sidebar(self):
        for widget in self.sidebar.winfo_children():
            widget.destroy()

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_services_sidebar(self):
        self.clear_sidebar()
        tk.Label(self.sidebar, text="Сервіси", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

        for name in self.services:
            if name == "Вийти":
                tk.Button(self.sidebar, text=name, width=300, command=self.on_closing, bg="#ff9999").pack(
                    side=tk.BOTTOM)
            else:
                tk.Button(self.sidebar, text=name, width=300,
                          command=lambda n=name: self.context.events.emit(
                              Event(EventType.SERVICE_SELECTED, service_name=n))).pack()

    def show_commands_sidebar(self, service_name):
        self.clear_sidebar()
        tk.Label(self.sidebar, text=f"Команди\n{service_name}", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)

        commands_for_service = [k for k, v in self.commands.items() if v["service"] == service_name]

        for cmd_name in commands_for_service:
            tk.Button(self.sidebar, text=cmd_name, width=300,
                      command=lambda c=cmd_name: self.context.events.emit(
                          Event(EventType.EXECUTE_COMMAND, command_name=c, service_name=service_name)
                      )).pack()

        tk.Button(self.sidebar, text="<- До сервісів", width=300, command=self.show_services_sidebar,
                  bg="#cccccc").pack(
            side=tk.BOTTOM)

    def show_result(self, title, message, color="white"):
        self.clear_main_area()
        self.main_area.configure(bg=color)
        tk.Label(self.main_area, text=title, font=("Arial", 16, "bold"), bg=color).pack(pady=20)
        tk.Label(self.main_area, text=message, font=("Arial", 12), bg=color, justify=tk.LEFT, wraplength=600).pack(
            padx=20, pady=10, fill=tk.BOTH, expand=True)
        tk.Button(self.main_area, text="Очистити", width=20, command=self.clear_main_area).pack(pady=20)

    def show_params_form(self, service_name, command_name):
        self.clear_main_area()
        self.main_area.configure(bg="white")
        service = self.services[service_name]
        command_cls = self.commands[command_name]["command_cls"]

        tk.Label(self.main_area, text=f"Команда: {command_name}", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        if hasattr(command_cls, "description"):
            tk.Label(self.main_area, text=command_cls.description, wraplength=600, bg="white").pack(pady=5)

        params = []
        if hasattr(command_cls, "get_params"):
            params = command_cls.get_params(service)
        elif hasattr(command_cls, "expected_params"):
            params = command_cls.expected_params

        if not params:
            self.execute_with_params(command_cls, service, [])
            return

        self.current_params_values = {}
        self.current_params_error_labels = {}

        form_frame = tk.Frame(self.main_area, bg="white")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20)

        for param in params:
            param_container = tk.Frame(form_frame, bg="white")
            param_container.pack(fill=tk.X, pady=2)

            param_frame = tk.Frame(param_container, bg="white")
            param_frame.pack(fill=tk.X)

            tk.Label(param_frame, text=f"{param.display_name}:", width=20, anchor="w", bg="white").pack(side=tk.LEFT)
            tk.Label(param_frame, text=f"{param.description}:", width=20, anchor="w", bg="white").pack(side=tk.RIGHT)

            if param.parse == bool:
                var = tk.BooleanVar(value=False)
                self.current_params_values[param.name] = var
                tk.Checkbutton(param_frame, variable=var, bg="white").pack(side=tk.LEFT)

            elif param.parse in (int, float):
                if isinstance(param, ChoiceParameter):
                    val_var = tk.DoubleVar(value=0.0) if param.parse == float else tk.IntVar(value=0)
                    self.current_params_values[param.name] = val_var
                    values = param.choices
                    for value in values:
                        tk.Radiobutton(param_frame, text=value, value=value, variable=val_var).pack(side=tk.LEFT)
                else:
                    val_var = tk.DoubleVar(value=0.0) if param.parse == float else tk.IntVar(value=0)
                    self.current_params_values[param.name] = val_var

                    tk.Button(param_frame, text="-100", command=lambda v=val_var: v.set(v.get() - 100)).pack(
                        side=tk.LEFT)
                    tk.Button(param_frame, text="-10", command=lambda v=val_var: v.set(v.get() - 10)).pack(side=tk.LEFT)
                    tk.Button(param_frame, text="-1", command=lambda v=val_var: v.set(v.get() - 1)).pack(side=tk.LEFT)

                    label = tk.Label(param_frame, textvariable=val_var, width=10, relief="sunken")
                    label.pack(side=tk.LEFT, padx=5)

                    tk.Button(param_frame, text="+1", command=lambda v=val_var: v.set(v.get() + 1)).pack(side=tk.LEFT)
                    tk.Button(param_frame, text="+10", command=lambda v=val_var: v.set(v.get() + 10)).pack(side=tk.LEFT)
                    tk.Button(param_frame, text="+100", command=lambda v=val_var: v.set(v.get() + 100)).pack(
                        side=tk.LEFT)

            error_label = tk.Label(param_container, text="", fg="red", bg="white", font=("Arial", 8))
            error_label.pack(anchor="w", padx=(145, 0))
            self.current_params_error_labels[param.name] = error_label

        tk.Button(self.main_area, text="Виконати", bg="#99ff99", height=2, width=30,
                  command=lambda: self.collect_and_execute(command_cls, service, params)).pack(pady=20)
        tk.Button(self.main_area, text="Скасувати", command=self.clear_main_area).pack()

    def collect_and_execute(self, command_cls, service, params_meta):
        args = []
        is_valid = True

        for label in self.current_params_error_labels.values():
            label.config(text="")

        for p in params_meta:
            try:
                val = self.current_params_values[p.name].get()
                converted_val = p.convert(str(val))
                args.append(converted_val)
            except (ValueError, tk.TclError) as e:
                is_valid = False
                error_msg = str(e)
                if isinstance(e, tk.TclError):
                    error_msg = "Невірний формат числа"
                self.current_params_error_labels[p.name].config(text=error_msg)

        if is_valid:
            self.execute_with_params(command_cls, service, args)

    def execute_with_params(self, command_cls, service, args):
        cmd_instance = command_cls(service, *args)
        self.context.events.emit(Event(EventType.RUN_COMMAND, command=cmd_instance))

    def update_gui(self):
        try:
            self.root.update()
        except tk.TclError:
            pass
