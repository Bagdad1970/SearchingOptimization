from src.entities.point import Point
from src.model.model import Model
from src.model.strategies.genetic_algorithm import GeneticAlgorithm
from src.model.strategies.gradient_descent import GradientDescent
from src.model.strategies.simplex_method import SimplexMethod
from src.plot_widget import PlotWidget
from src.views.mainview import MainView
from src.function_from_str import function_from_str
from src.views.options_views.options.genetic_algorithm import GeneticAlgorithmOptions
from src.views.options_views.options.gradient_descent import GradientDescentOptions
from src.views.options_views.options.simplex_method import SimplexMethodOptions


class Presenter:
    def __init__(self, *, view: MainView, model: Model):
        self.view = view
        self.model = model

        self.view.set_presenter(self)

        self.plot = PlotWidget()
        self.view.set_plot(self.plot)

        self.iterations = self.view.Iterations

        self.options = None
        self.change_method()

        self.connect_signals()

    def connect_signals(self):
        self.view.SpecificMethod.currentTextChanged.connect(self.change_method)

    def set_option_widget(self):
        # Очищаем layout (удаляем все виджеты)
        while self.view.Options.layout().count():
            item = self.view.Options.layout().takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Добавляем новый виджет
        self.view.Options.layout().addWidget(self.options)

    def add_observers(self, **observers):
        self.model.add_observer('point_observer', observers['point_observer'])
        self.model.add_observer('iteration_observer', observers['iteration_observer'])
        self.model.add_observer('stop_reason_observer', observers['stop_reason_observer'])

    def change_method(self):
        self.model.remove_observers()
        current_text = self.view.SpecificMethod.currentText()
        if current_text == "Градиентный спуск":
            self.model.set_strategy(GradientDescent())
            self.options = GradientDescentOptions()
        elif current_text == "Симплекс метод":
            self.model.set_strategy(SimplexMethod())
            self.options = SimplexMethodOptions()
        elif current_text == "Генетический алгоритм":
            self.model.set_strategy(GeneticAlgorithm())
            self.options = GeneticAlgorithmOptions()

        self.set_option_widget()
        self.view.set_function(self.model.initial_function())

        self.plot.remove_points()

        self.set_plot()
        self.add_observers(point_observer=self,
                           stop_reason_observer=self.view,
                           iteration_observer=self.view
                        )

    def get_point(self, point: Point):
        self.plot.set_point(point)

    def get_function(self):
        return self.view.get_function()

    def execute(self):
        self.view.clean_iterations()

        self.model.set_params(self.get_function(),
                              self.options.get_params()
                              )

        self.set_plot()

        self.model.execute()

    def set_plot(self):
        function = function_from_str(self.get_function())
        self.plot.set_plot(function=function,
                            point=self.options.get_point()
                           )