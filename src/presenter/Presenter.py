from src.Plot import Plot
from src.entities.Point import Point
from src.model.Model import Model
from src.model.strategies.GradientDescent import GradientDescent
from src.views.MainView import MainView
from src.views.MethodsOptions import GradientDescentOptions
from src.function_from_str import function_from_str


class Presenter:
    def __init__(self, *, view: MainView, model: Model):
        self.view = view
        self.model = model

        self.view.set_presenter(self)

        self.plot = Plot()
        self.set_plot()

        self.iterations = self.view.ui.Iterations

        self.options = None
        self.change_method()

        self.connect_signals()

    def connect_signals(self):
        self.view.ui.SpecificMethod.currentTextChanged.connect(self.change_method)
        self.view.ui.ExecuteButton.clicked.connect(self.execute)

    def set_option_widget(self):
        if self.view.ui.Options.widget() is not None:
            self.view.ui.Options.removeWidget(self.view.ui.Options.widget())
        self.view.ui.Options.addWidget(self.options)

    def set_plot(self):
        self.view.ui.Plot.addWidget(self.plot)

    def change_method(self):
        self.model.remove_point_observers()
        current_text = self.view.ui.SpecificMethod.currentText()
        if current_text == "Градиентный спуск":
            self.model.set_strategy(GradientDescent())
            self.options = GradientDescentOptions()

        self.set_option_widget()
        self.model.add_observer(self)
        self.set_surface()

    def get_point(self, function, point: Point):
        self.plot.set_point(function=function, point=point)

    def get_iteration(self, iteration_info: str):
        self.iterations.appendPlainText(iteration_info)

    def get_stop_reason(self, stop_reason: str):
        self.iterations.appendPlainText(stop_reason)

    def set_params(self):
        function = self.get_function()
        method_params = self.options.get_params()  # сделать точку для всех алгоритмов
        self.model.set_params(function, **method_params)

    def get_function(self):
        return function_from_str(self.view.get_function())

    def execute(self):
        self.view.clean_iterations()

        self.set_surface()

        function = self.get_function()
        method_params = self.options.get_params()
        self.model.set_params(function, **method_params)

        self.model.execute()

    def set_surface(self):
        point = self.options.get_point()
        function = self.get_function()
        self.plot.set_full_plot(function=function, point=point)