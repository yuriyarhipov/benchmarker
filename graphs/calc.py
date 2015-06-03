from models import Calculation

class Calc(object):

    def __init__(self, calculation_name):
        Calculation.objects.get(calculation_name = calculation_name)
        self.calculation_name = calculation_name




