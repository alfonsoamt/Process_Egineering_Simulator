import pandas as pd

class Simulator:
    # This class represents the simulator environment 

    def __init__(self):
        self.database = None #This is de database information
        self.errors = []    # This is a severe error list
        self.warnings = []  # This is a warming error list

    # This method loads the Perry's handbook data
    def load_perry(self):
        self.database =  pd.read_csv("./properties/Database.csv",index_col=("Name"))
        return self.database

class Variable:
    # This class represents a variable. It could be a process variable or parameters from equations

    def __init__(self, value, units):

        self.value = value      # Variable value
        self.units = units      # Variable units
        self.units_c = None     # Variable units database for units convertion
        self.v_type = ""        # Variable type

    # This method converts the variable units
    def Converter(self):
        pass

class Temperature(Variable):
    # Variable: Temperature

    def __init__(self, value, units):

          super().__init__(value, units)
          self.v_type = "Temperature"
          self.units_c = pd.DataFrame({"K":[lambda T: T , lambda T: T + 273.15, lambda T: (T + 459.67) * 5 / 9, lambda T: T * 5 / 9],
          "°C":[lambda T: T - 273.15, lambda T: T, lambda T: (T - 32) * 5 /9, lambda T: (T - 491.67) * 5 / 9],
          "°F":[lambda T: (T * 9 / 5) -459.67, lambda T: (T * 9 / 5) + 32, lambda T: T, lambda T: T - 459.67],
          "R":[lambda T: T * 9 / 5, lambda T: (T + 273.15) * 9 / 5, lambda T: T + 459.67, lambda T: T]}, 
          index = ["K", "°C", "°F", "R"])

    def Converter(self, Tunits):

          self.value = round(self.units_c.at[self.units, Tunits](self.value), 2)
          self.units = Tunits
    
class Pressure(Variable):
    # Variable: Pressure

    def __init__(self, value, units):
        super().__init__(value, units)
        self.v_type = "Pressure"
        self.units_c = pd.read_csv('./units/Pressure.csv', index_col = 0) 

    def Converter(self, Punits):

        self.value = self.value * self.units_c.at[self.units, Punits]
        self.units = Punits

class MolarVolume(Variable):
    # Variable: Molar volume

    def __init__(self, value, units):
        super().__init__(value, units)
        self.v_type = "MolarVolume"
        self.units_c = pd.read_csv('./units/MolarVolume.csv', index_col = 0) 

    def Converter(self, MVunits):

        self.value = self.value * self.units_c.at[self.units, MVunits]
        self.units = MVunits

class MolarHeatCapacity(Variable):

    def __init__(self, value, units):
        super().__init__(value, units)
        self.v_type = "Molar heat capacity"
        self.units_c = None

    def Converter(self, MHCunits):

        self.value = self.value * self.units_c.at[self.units, MHCunits]
        self.units = MHCunits

class MolarEnthalpy(Variable):

    def __init__(self, value, units):
        super().__init__(value, units)
        self.v_type = "Molar enthalpy"
        self.units_c = None

    def Converter(self, MHunits):

        self.value = self.value * self.units_c.at[self.units, MHunits]
        self.units = MHunits

class MolarGibbs(Variable):

    def __init__(self, value, units):
        super().__init__(value, units)
        self.v_type = "Molar Gibbs energy"
        self.units_c = None

    def Converter(self, MGunits):

        self.value = self.value * self.units_c.at[self.units, MGunits]
        self.units = MGunits  

class MolarEntropy(Variable):

    def __init__(self, value, units):
        super().__init__(value, units)
        self.v_type = "Molar entropy"
        self.units_c = None

    def Converter(self, MSunits):

        self.value = self.value * self.units_c.at[self.units, MSunits]
        self.units = MSunits 

class MolarWeight(Variable):

    def __init__(self, value):
        super().__init__(value, "None")
        self.v_type = "Molar weight"
        self.units_c = None