import tkinter as tk
from core.events import Event, EventType
from core.response import Response, TextBox, PlotBox
from UI.common.presentation.proxy import ParameterUIAssembler
from UI.common.presentation.hint import RangeHint, OrderHint, ChoiceHint, LargeTextHint, ListboxHint


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
            result = event.data["result"]
            if isinstance(result, Response):
                self.show_response("Результат", result)
            else:
                self.show_result("Результат", str(result))

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

    def show_response(self, title, response: Response, color="white"):
        self.clear_main_area()
        self.main_area.configure(bg=color)
        tk.Label(self.main_area, text=title, font=("Arial", 16, "bold"), bg=color).pack(pady=10)

        container = tk.Frame(self.main_area, bg=color)
        container.pack(fill=tk.BOTH, expand=True, padx=20)

        for box in response.boxes:
            if isinstance(box, TextBox):
                tk.Label(container, text=box.text, font=("Arial", 12), bg=color, justify=tk.LEFT, wraplength=600).pack(
                    anchor="w", pady=5)
            elif isinstance(box, PlotBox):
                self._draw_plot(container, box.plot_points)

        tk.Button(self.main_area, text="Очистити", width=20, command=self.clear_main_area).pack(pady=10)

    def _draw_plot(self, parent, points):
        if not points:
            return

        canvas_width = 600
        canvas_height = 300
        padding = 40

        canvas = tk.Canvas(parent, width=canvas_width, height=canvas_height, bg="white", highlightthickness=1, highlightbackground="black")
        canvas.pack(pady=10)

        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        range_x = max_x - min_x if max_x != min_x else 1
        range_y = max_y - min_y if max_y != min_y else 1

        def scale_x(x):
            return padding + (x - min_x) * (canvas_width - 2 * padding) / range_x

        def scale_y(y):
            return canvas_height - (padding + (y - min_y) * (canvas_height - 2 * padding) / range_y)

        canvas.create_line(padding, canvas_height - padding, canvas_width - padding, canvas_height - padding, arrow=tk.LAST) # X
        canvas.create_line(padding, canvas_height - padding, padding, padding, arrow=tk.LAST) # Y

        scaled_points = [(scale_x(x), scale_y(y)) for x, y in points]
        
        for i in range(len(scaled_points) - 1):
            p1 = scaled_points[i]
            p2 = scaled_points[i+1]
            canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="blue", width=2)
            canvas.create_oval(p1[0]-3, p1[1]-3, p1[0]+3, p1[1]+3, fill="red")
        
        last_p = scaled_points[-1]
        canvas.create_oval(last_p[0]-3, last_p[1]-3, last_p[0]+3, last_p[1]+3, fill="red")

        canvas.create_text(canvas_width - padding, canvas_height - padding + 15, text="X")
        canvas.create_text(padding - 15, padding, text="Y")

    def show_params_form(self, service_name, command_name):
        self.clear_main_area()
        self.main_area.configure(bg="white")
        service = self.services[service_name]
        command_cls = self.commands[command_name]["command_cls"]

        tk.Label(self.main_area, text=f"Команда: {command_name}", font=("Arial", 14, "bold"), bg="white").pack(pady=10)
        if hasattr(command_cls, "description"):
            tk.Label(self.main_area, text=command_cls.description, wraplength=600, bg="white").pack(pady=5)

        assembler = ParameterUIAssembler(command_cls, service)
        ui_params = assembler()

        if not ui_params:
            self.execute_with_params(command_cls, service, [])
            return

        def get_order(p_proxy):
            for hint in p_proxy.ui_hints:
                if isinstance(hint, OrderHint):
                    return hint.order_number
            return 999

        ui_params.sort(key=get_order)

        self.current_params_values = {}
        self.current_params_error_labels = {}

        form_frame = tk.Frame(self.main_area, bg="#cccccc")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        form_frame.columnconfigure(0, weight=0)
        form_frame.columnconfigure(1, weight=1)
        form_frame.columnconfigure(2, weight=0)

        # Header
        tk.Label(form_frame, text="Параметр", font=("Arial", 10, "bold"), bg="#eeeeee", relief=tk.RIDGE, bd=1).grid(
            row=0, column=0, sticky="nsew")
        tk.Label(form_frame, text="Значення", font=("Arial", 10, "bold"), bg="#eeeeee", relief=tk.RIDGE, bd=1).grid(
            row=0, column=1, sticky="nsew")
        tk.Label(form_frame, text="Опис", font=("Arial", 10, "bold"), bg="#eeeeee", relief=tk.RIDGE, bd=1).grid(
            row=0, column=2, sticky="nsew")

        for i, param_proxy in enumerate(ui_params):
            row_index = (i + 1) * 2 - 1

            tk.Label(form_frame, text=f"{param_proxy.display_name}:", width=25, anchor="w", bg="white", relief=tk.RIDGE, bd=1).grid(
                row=row_index, column=0, sticky="nsew", rowspan=2)
            
            tk.Label(form_frame, text=f"{param_proxy.description}", width=25, anchor="w", bg="white", relief=tk.RIDGE, bd=1, wraplength=200).grid(
                row=row_index, column=2, sticky="nsew", rowspan=2)

            parse_type = param_proxy.parse
            
            choices = []
            range_hint = None
            large_text = False
            listbox_hint = None
            
            for hint in param_proxy.ui_hints:
                if isinstance(hint, ChoiceHint):
                    choices = hint.choices
                elif isinstance(hint, RangeHint):
                    range_hint = hint
                elif isinstance(hint, LargeTextHint):
                    large_text = True
                elif isinstance(hint, ListboxHint):
                    listbox_hint = hint

            widget_container = tk.Frame(form_frame, bg="white", relief=tk.RIDGE, bd=1)
            widget_container.grid(row=row_index, column=1, sticky="nsew")

            if large_text:
                text_widget = tk.Text(widget_container, height=5, width=40)
                text_widget.pack(fill=tk.X, expand=True)
                self.current_params_values[param_proxy.name] = text_widget

            elif listbox_hint:
                lb_frame = tk.Frame(widget_container)
                lb_frame.pack(fill=tk.X, expand=True)
                scrollbar = tk.Scrollbar(lb_frame, orient=tk.VERTICAL)
                listbox = tk.Listbox(lb_frame, height=listbox_hint.height, yscrollcommand=scrollbar.set)
                scrollbar.config(command=listbox.yview)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                for choice in listbox_hint.choices:
                    listbox.insert(tk.END, choice)
                self.current_params_values[param_proxy.name] = listbox

            elif choices:
                val_var = tk.StringVar(value=str(choices[0]))
                self.current_params_values[param_proxy.name] = val_var
                option_menu = tk.OptionMenu(widget_container, val_var, *choices)
                option_menu.pack(side=tk.LEFT)

            elif parse_type == bool:
                var = tk.BooleanVar(value=False)
                self.current_params_values[param_proxy.name] = var
                tk.Checkbutton(widget_container, variable=var, bg="white").pack(side=tk.LEFT)

            elif parse_type in (int, float):
                val_var = tk.StringVar(value="0")
                self.current_params_values[param_proxy.name] = val_var

                def validate_range(event, var=val_var, rh=range_hint, pt=parse_type):
                    if rh is None:
                        return
                    try:
                        val = pt(var.get())
                        if rh.min_value is not None and val < rh.min_value:
                            var.set(str(rh.min_value))
                        elif rh.max_value is not None and val > rh.max_value:
                            var.set(str(rh.max_value))
                    except ValueError:
                        if rh.min_value is not None:
                            var.set(str(rh.min_value))
                        elif rh.max_value is not None:
                            var.set(str(rh.max_value))
                        else:
                            var.set("0")

                if range_hint:
                    def update_from_scale(val, var=val_var):
                        var.set(str(val))

                    if range_hint.min_value is not None and range_hint.max_value is not None:
                        entry = tk.Entry(widget_container, textvariable=val_var, width=10)
                        entry.bind("<FocusOut>", validate_range)
                        entry.pack(side=tk.LEFT, padx=5)

                        scale = tk.Scale(widget_container, from_=range_hint.min_value, to=range_hint.max_value,
                                       orient=tk.HORIZONTAL, length=200, showvalue=0,
                                       resolution=1 if parse_type == int else 0.1,
                                       command=update_from_scale)
                        scale.set(range_hint.min_value)
                        scale.pack(side=tk.LEFT, padx=5)
                        
                        def sync_scale(*args, s=scale, v=val_var, pt=parse_type):
                            try:
                                val = pt(v.get())
                                s.set(val)
                            except (ValueError, tk.TclError):
                                pass

                        val_var.trace_add("write", sync_scale)
                        val_var.set(str(range_hint.min_value))
                        
                    elif range_hint.min_value is not None:
                        spin = tk.Spinbox(widget_container, from_=range_hint.min_value, to=999999,
                                        increment=1 if parse_type == int else 0.1,
                                        textvariable=val_var, width=10)
                        spin.bind("<FocusOut>", validate_range)
                        spin.pack(side=tk.LEFT, padx=5)
                        val_var.set(str(range_hint.min_value))
                    elif range_hint.max_value is not None:
                        spin = tk.Spinbox(widget_container, from_=-999999, to=range_hint.max_value,
                                        increment=1 if parse_type == int else 0.1,
                                        textvariable=val_var, width=10)
                        spin.bind("<FocusOut>", validate_range)
                        spin.pack(side=tk.LEFT, padx=5)
                        val_var.set(str(range_hint.max_value))
                else:
                    entry = tk.Entry(widget_container, textvariable=val_var, width=10)
                    entry.pack(side=tk.LEFT, padx=5)

            else:
                val_var = tk.StringVar()
                self.current_params_values[param_proxy.name] = val_var
                tk.Entry(widget_container, textvariable=val_var, width=30).pack(side=tk.LEFT)

            error_label = tk.Label(form_frame, text="", fg="red", bg="white", font=("Arial", 8), relief=tk.RIDGE, bd=1)
            error_label.grid(row=row_index + 1, column=1, sticky="nsew")
            self.current_params_error_labels[param_proxy.name] = error_label

        button_container = tk.Frame(self.main_area, bg="white", height=100)
        button_container.pack(fill=tk.X, side=tk.BOTTOM)
        
        tk.Button(button_container, text="Виконати", bg="#99ff99", height=2, width=30,
                  command=lambda: self.collect_and_execute(command_cls, service, ui_params)).place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        tk.Button(button_container, text="Скасувати", command=self.clear_main_area).place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    def collect_and_execute(self, command_cls, service, params_meta):
        args = []
        is_valid = True

        for label in self.current_params_error_labels.values():
            label.config(text="")

        for p in params_meta:
            try:
                widget_or_var = self.current_params_values[p.name]
                if isinstance(widget_or_var, tk.Text):
                    val = widget_or_var.get("1.0", tk.END).strip()
                elif isinstance(widget_or_var, tk.Listbox):
                    selection = widget_or_var.curselection()
                    if selection:
                        val = widget_or_var.get(selection[0])
                    else:
                        val = ""
                else:
                    val = widget_or_var.get()
                
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
