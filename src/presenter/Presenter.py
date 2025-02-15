from src.PlotWidget import PlotWidget
from src.model.Model import Model
from src.model.strategies import GradientDescent
from src.views.MainView import MainView
from src.views.MethodsOptions import GradientDescentOptions


class Presenter:
    def __init__(self, *, view: MainView, model: Model):
        self.view = view
        self.model = model

        self.view.set_presenter(self)

        self.plot = PlotWidget()
        self.set_plot()

        self.options = None
        self.change_options()

        self.view.ui.SpecificMethod.currentTextChanged.connect(self.change_options)
        self.view.ui.ExecuteButton.clicked.connect(self.execute)

    def create_surface(self, *, x, y, function): # replace surface instead of create
        #self.plot.create_surface(x=x, y=y, function=function)
        pass

    def set_option_widget(self):
        if self.view.ui.Options.widget() is not None:
            self.view.ui.Options.removeWidget(self.view.ui.Options.widget())
        self.view.ui.Options.addWidget(self.options)

    def set_plot(self):
        self.view.ui.Plot.addWidget(self.plot)

    def get_params(self) -> dict:
        pass

    def create_strategy(self):
        current_method = self.view.ui.SpecificMethod.currentText()
        params = self.get_params()
        #if current_method == "Градиентный спуск":
        #    return GradientDescent(**params)

    def change_options(self):
        current_text = self.view.ui.SpecificMethod.currentText()
        if current_text == "Градиентный спуск":
            self.options = GradientDescentOptions()

        self.set_option_widget()

    def execute(self):
        pass

