import math
from hardware_tools import constants 
from hardware_tools import conversions


def noise_voltage(resistance:float,temperature:float,Bandwidth:float)->float:
    """caluculate thermal noise voltage"""
    noise=math.sqrt(4*constants.k*temperature*Bandwidth*resistance)
    return noise


def noise_power_dbm(temperature:float,Bandwidth:float)->float:
    """caluculate thermal noise power"""
    noise_pwr=conversions.w_2_dbm(constants.k*temperature*Bandwidth)
    return noise_pwr