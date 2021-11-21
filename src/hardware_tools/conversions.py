import math
import numpy as np

"""
collection of simple conversion tools
"""



def pk_2_rms(peak:float)->float:
    """convert peak --> rms"""
    rms=peak/np.sqrt(2)
    return rms

def rms_2_pk(rms:float)->float:
    """convert rms  --> peak"""
    pk=rms*np.sqrt(2)
    return pk

def w_2_dbm(watts:float)->float:
    """convert watts --> dbm"""
    return 10.0*np.log10(watts/0.001)

def dbm_2_w(dbm:float)->float:
    """convert dbm --> watts"""
    return np.power(10,dbm/10)



def sum_dbm(dbm_list:list[float])->float:
    """sum a list of dbm values, return dbm"""
    w=map(dbm_2_w, dbm_list)
    sum_w=sum(w)
    dbm=w_2_dbm(sum_w)
    return dbm



add_dbm=lambda a,b:sum_dbm([a,b])
sub_dbm=lambda a,b:sum_dbm([a,-b])



 
def nfdb_2_noiseTemp(noise_fig_db:float,Tref:float=290)->float:
    """convert noise figure(db) --> noise temperature"""
    noise_fig=np.power(10,(noise_fig_db/10))
    rx_noise_temp=(noise_fig-1)*Tref
    return rx_noise_temp


def noiseTemp_2_nfdb(noise_temp:float,Tref:float=290)->float:
    """convert noise temperature --> noise figure(db)"""
    noise_fig=10*np.log10((noise_temp/Tref)+1)
    return noise_fig