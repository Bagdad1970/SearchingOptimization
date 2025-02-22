from src.views.Options import Options
import src.views.options.gradient_descent as gradient_descent

class GradientDescentOptions(Options, gradient_descent.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)