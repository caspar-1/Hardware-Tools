import numpy as np
from hardware_tools import constants


class Link:
    def __init__(self,**kwargs):
        self.transmit_pwr_dbm =kwargs.get("tx_pwr_dbm",15.0)
        self.transmitter_loss_db =kwargs.get("tx_loss", 0.2)
        self.transmit_antenna_gain_dbi = kwargs.get("tx_ant_gain",0.0)
        self.propagation_path_loss = kwargs.get("path_loss",144.0)
        self.fade_loss = kwargs.get("path_fade",4.0)
        self.receiver_antenna_gain_dbi = kwargs.get("rx_ant_gain",12.34)
        self.reciever_loss = kwargs.get("rx_loss",0.0)

        self.antenna_noise_temperature = kwargs.get("ant_noise_temp",290.0)
        self.receiver_noise_temperature_k = kwargs.get("rx_noise_temp",870.0)

        self.data_rate = kwargs.get("data_rate",2400.0)

  

    def SNR_db(self):
        """"""
        Prx = (self.transmit_pwr_dbm
               - self.transmitter_loss_db
               + self.transmit_antenna_gain_dbi
               - self.propagation_path_loss
               - self.fade_loss
               + self.receiver_antenna_gain_dbi
               - self.reciever_loss
               )

        ts = self.antenna_noise_temperature+self.receiver_noise_temperature_k
        bw = 10.0*np.log10(self.data_rate)
        Eb = Prx-bw
        #Boltzmann is in 'watts' need to multiply by 1000, or add 30db
        #to get in mW since powers are dbm
        No = (10.0*np.log10(constants.Boltzmann))+(10.0*np.log10(ts))+30
        snr = Eb-No
        return snr





if __name__ == "__main__":

    link = Link()
    print(link.SNR_db())





    