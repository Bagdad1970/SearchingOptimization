from src.entities.point import Point
from src.model.model import Model
from src.model.strategies.gradient_descent import GradientDescent
from src.presenter.plot_presenter import PlotPresenter
from src.views.mainview import MainView
from src.views.options_views.gradient_descent import GradientDescentOptions
from src.function_from_str import function_from_str


class Presenter:
    def __init__(self, *, view: MainView, model: Model):
        self.view = view
        self.model = model

        self.view.set_presenter(self)

        self.iterations = self.view.Iterations

        self.options = None
        self.change_method()

        self.connect_signals()

    def connect_signals(self):
        self.view.SpecificMethod.currentTextChanged.connect(self.change_method)
        self.view.ExecuteButton.clicked.connect(self.execute)

    def set_plot_presenter(self, plot_presenter: PlotPresenter):
        self.plot_presenter = plot_presenter

    def set_option_widget(self):
        if self.view.Options.widget() is not None:
            self.view.Options.removeWidget(self.view.ui.Options.widget())
        self.view.Options.addWidget(self.options)

    def change_method(self):
        self.model.remove_point_observers()
        current_text = self.view.SpecificMethod.currentText()
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

        self.plot.set_surface()

        function = self.get_function()
        method_params = self.options.get_params()
        self.model.set_params(function, **method_params)

        self.model.execute()

    def set_surface(self):
        point = self.options.get_point()
        function = self.get_function()
        self.plot.set_full_plot(function=function, point=point)