import numpy as np
import math





class BER:
    """
    Bit error rate models for different modulation types
    https://www.eetimes.com/modulation-roundup-error-rates-noise-and-capacity/
    """

    MOD_DICT = {
        "BPSK": lambda m: BER.ber_bpsk(m),
        "PAM_4": lambda m: BER.ber_pam4(m),
        "PSK_M": lambda m: BER.ber_psk(m),
        "QAM_M": lambda m: BER.ber_qam(m)
    }

    @staticmethod
    def ber_bpsk(M=None):
        def Fn(snr):
            ber = 0.5*math.erfc(math.sqrt(snr))
            return ber
        return Fn

    @staticmethod
    def ber_pam4(M=None):

        def Fn(snr):
            ber = 0.75*math.erfc(math.sqrt(0.2*snr))
            return ber
        return Fn

    @staticmethod
    def ber_psk(M):
        def Fn(snr):
            ber = math.erfc(math.sqrt(snr)*math.sin(math.pi/M))
            return ber
        return Fn

    @staticmethod
    def ber_qam(M):
        def Fn(snr):
            term_1 = (2.0*(1.0-1.0/math.sqrt(M)))*math.erfc(math.sqrt(snr*(3.0/(2.0*(M-1)))))
            term_2 = (1.0-(1.0/math.sqrt(M))+(1.0/M))*math.pow(math.erfc(math.sqrt(snr*(3.0/(2.0*(M-1))))), 2.0)
            ber = term_1-term_2
            return ber
        return Fn

    @staticmethod
    def get_func(modulation_scheme, **kwargs):
        M = kwargs.get("M", None)
        wrapper_func = BER.MOD_DICT.get(modulation_scheme, None)
        func = wrapper_func(M)
        return func

    @staticmethod
    def calc(modulation, snr_db, m=None):
        snr = np.power(10, snr_db/10)
        ber = None
        if modulation in BER.MOD_DICT:
            ber_func = BER.MOD_DICT[modulation]
            ber = ber_func(snr, m)

    @staticmethod
    def snr(ber, k=4.16):
        snr = (np.exp(np.log(ber)/k))
        snr_db = 10*np.log10(1/snr)
        return snr_db




if __name__ == "__main__":


    import matplotlib.pyplot as plt
    import itertools
    
    
    snr_db = np.arange(0, 35, 1)

    tests=[("BPSK",[0]),("PSK_M",[4,8,16]),("QAM_M",[4,8,16,64,256])]


    color_iter=itertools.cycle(["red","blue","green","orange","gold","black","dimgray","lime","darkblue"])
    for t in tests:
        
        sig=t[0]
        M=t[1]

        clr=next(color_iter)
        marker_iter=itertools.cycle([ '+', '.', 'o', '*',"v","^","<",">","1","2","3","4"])
        for m in M:
            mkr=next(marker_iter)
            
            fn=BER.get_func(sig,M=m)
            vfunc = np.vectorize(fn)

            snr = np.power(10, snr_db/10)
            ber = vfunc(snr)

            p,=plt.plot(snr_db, ber,marker=mkr,color=clr)
            p.set_label("{}_{}".format(sig,m))
            plt.yscale("log")
            plt.ylim((1e-6, 1))
            
    plt.legend()
    plt.show()
