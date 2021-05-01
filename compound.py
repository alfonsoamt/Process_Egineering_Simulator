
import numpy as np
from scipy.integrate import quad
from datetime import datetime
import pandas as pd
from simulator import *

S = Simulator()
## This file contains the Compound class
class Compound:
    
    def __init__(self, name, mw = None, Perry = True):
        
        self.name = name            # Compound name
        # Pure properties
        self.mw = mw                # molecular weight
        self.Hig_f = None   # ideal gas enthalpy of formation
        self.Gig_f = None   # ideal gas Gibbs free energy of formation
        self.Sig = None     # ideal gas entropy
        self.Hstd_c = None  # standard heat of combustion
        self.acentric = None        # acentric factor
        self.dipole = None  # magnetic dipole
        # Critical properties
        self.Tc = None      # critical temperature
        self.Pc = None      # critical pressure
        self.Vmc = None     # critical molar volume
        self.Zc = None              # critical compressibility factor
        # Thermodynamic properties
        self.Z = None               # compresibility factor
        self.Pvap = None    # vapor pressure
        self.mCPig = None   # mean ideas gas heat capacity
        self.mCPl = None    # mean liquid heat capacity    
        self.CPig = None    # ideal gas heat capacity
        self.CPl = None     # liquid heat capacity
        self.density = None # density
        # Transport properties
        self.GasVis = None  # gas viscosity
        self.LiqVis = None  # liquid viscosity
        self.GasTC = None   # gas thermal conductivity
        self.LiqTC = None   # liquid therml conductivity

        if Perry:
            # data
            self.data = S.load_perry()
            # Pure compound proprerties
            self.wt = self.data.at[self.name, "wt"]
            self.Hig_f = [self.data.at[self.name, "Hig_f"], "kJ/mol"]
            self.Gig_f = [self.data.at[self.name, "Gig_f"], "kJ/mol"]
            self.Sig = [self.data.at[self.name, "Sig"], "kJ/mol*K"]
            self.Hstd_c = [self.data.at[self.name, "Hstd_c"], "kJ/mol"]
            # Critical properties from Perry's handbook
            self.Tc = Temperature(self.data.at[self.name, "Tc"], "K")
            self.Pc = Pressure(self.data.at[self.name, "Pc"], "MPa")
            self.Vmc = MolarVolume(self.data.at[self.name, "Vc"], "m3/kmol")
            self.Zc = self.data.at[self.name, "Zc"]
            self.acentric = self.data.at[self.name, "Acentric factor"]
            
        else:
            self.data = None

        
    def CP_liquid(self, T, Tunits = "K", Report = False, f_output = False):
        # Liquid heat capacity, Perrys' handobook method.
        # T is a temperature which LCP will be calculated.
        # Report is a boolean, if True, then print the result.

        # Convert temperature units into Kelvin.
        if isinstance(T,(int, float)):
            T = Temperature(T, Tunits)

        else:
            T.Converter("K")
            self.Tc.Converter("K")
        # Equation 2 for calculating LCP     
        eq2 = ["1,2-Butanediol", "1,3-Butanediol", "Carbon monoxide", \
               "1,1-Difluoroethane", "Ethane", "Heptane", "Hydrogen", \
               "Hydrogen sulfide", "Methane", "Propane"]
        # Read parameters from the database
        C1 = self.data.loc[self.name, "CPLC1"]
        C2 = self.data.loc[self.name, "CPLC2"]
        C3 = self.data.loc[self.name, "CPLC3"]
        C4 = self.data.loc[self.name, "CPLC4"]
        C5 = self.data.loc[self.name, "CPLC5"]
        # Equaion 2
        if self.name in eq2:
            
            Tr = T.value / self.Tc.value
            t = 1- Tr
            CPL = (C1 * C1 / t) + C2 - 2 * C1 * C3 * t - C1 * C4 * t * t \
                  - ((C3 **2) * (t ** 3) / 3) - ((C3 * C4) * (t ** 4) / 2) \
                  - ((C4 **2) * (t ** 5) / 5)
            
        else:
        # Equation 1
            CPL = C1 +( C2 * T.value) +( C3 * (T.value**2)) +( C4 * (T.value ** 3)) + (C5 * (T.value ** 4))
            
        self.CPl = MolarHeatCapacity(CPL, 'J/kmol*K')
        
            
        if Report:
            print(f'The Liquid Heat Capacity of {self.name} is {self.CPl.value:,.2f} {self.CPl.units}')

        if f_output:
            return CPL#, 'J/kmol*K'
        
    def mean_CP(self, f_CP, T1, T2, units, phase, Report = False):
        # This method calculate de mean heat capacity
        T1.Converter("K")
        T2.Converter("K")
        mCP, err = quad(f_CP, T1.value, T2.value, args = (T1.units, False, True))
        S.add_warning(f'{datetime.now().strftime("%H:%M:%S")}: \
            The integral error for the mean heat capacity of {self.name} is {err:.2e}.')

        if phase == "liquid":
            self.mCPl = MolarHeatCapacity(mCP / (T2.value - T1.value), units)

            if Report:
                print(f'The Mean Liquid Heat Capacity of {self.name} is {self.mCPl.value:,.2f} {self.mCPl.units}')

        elif phase == "gas":
            self.mCPig = [mCP / (T2.value - T1.value), units]
            if Report:
                print(f'The Mean Ideal gas Heat Capacity of {self.name} is {self.mCPig.value:,.2f} {self.mCPig.units}')
            