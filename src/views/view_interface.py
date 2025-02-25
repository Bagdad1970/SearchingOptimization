class ViewInterface:

    def add_iteration_info(self, iteration_info):
        raise NotImplementedError

    def get_params(self):
        raise NotImplementedError

    def set_surface(self, surface):
        raise NotImplementedError