from src.views.options import Options
import src.views.options_views.gradient_descent_options as gradient_descent

class GradientDescentOptions(Options, gradient_descent.Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)