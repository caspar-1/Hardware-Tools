from  hardware_tools import noise_calcs as nc
import numpy as np



class OP_AMP():
    def __init__(self,en:float=0,in_p:float=0,in_n:float=0):
        """
        ### params:
            en  :float
                input noise voltage nV/√Hz    
            in_p :float
                input noise current pos pA/√Hz    
            in_n :float
                input noise current neg pA/√Hz    
        """
        self.en=en/1e9 
        self.in_p=in_p/1e12
        self.in_n=in_n/1e12



AD745J=OP_AMP(3.2,0.0069,0.0069)




def add_noise_sources(sources:list[float])->float:
    def square(v):
        return v*v
    x=map(square,sources)
    return np.sqrt(x)


class inverting_amp():
    """
                Inverting Amp
                                   R1
                             ----/\/\/\---
                            |             |
                      R2    | |\          |
    IN--------------/\/\/\----|-\         |
        |                     |  \________|____
        / R3        R4        |  /
        \         --/\/\/\----|+/
        /         |           |/
        |         0     
        0
    """
    def __init__(self,r1,r2,r3,r4,Rs,temp=300,bw=20000,amp=OP_AMP()):
        self.r1=r1
        self.r2=r2
        self.r3=r3
        self.r4=r4
        self.rs=Rs

        
        def parallel(a,b):
            return(a*b)/(a+b)

        rp_a=parallel(self.rs,self.r3)
        rp_b=parallel(self.rs,self.r2)
        rp_c=parallel(self.r2,self.r3)
        self.r1_nf=1
        self.r2_nf=self.r1/(self.r2+rp_a)
        self.r3_nf=(self.r1/self.r2)*rp_b/(rp_b+self.r3)
        self.r4_nf=1+self.r1/(self.r2+rp_a)
        self.rs_nf=(self.r1/self.r2)*rp_c/(rp_c+self.rs)
        self.ein_nf=1+self.r1/(self.r2+rp_a)

        self.en_rs=nc.noise_voltage(self.rs,temp,bw)
        self.en_r1=nc.noise_voltage(self.r1,temp,bw)
        self.en_r2=nc.noise_voltage(self.r2,temp,bw)
        self.en_r3=nc.noise_voltage(self.r3,temp,bw)
        self.en_r4=nc.noise_voltage(self.r4,temp,bw)

        self.eno_r1=self.en_r1*self.r1_nf
        self.eno_r2=self.en_r2*self.r2_nf
        self.eno_r3=self.en_r3*self.r3_nf
        self.eno_r4=self.en_r4*self.r4_nf
        self.eno_rs=self.en_rs*self.rs_nf
        self.eno_eni=amp.en*self.rs_nf


        print("R1={: 8d}  en = {:0.3e}    en = {:0.3e}".format(self.r1,self.en_r1,self.eno_r1))
        print("R2={: 8d}  en = {:0.3e}    en = {:0.3e}".format(self.r2,self.en_r2,self.eno_r2))
        print("R3={: 8d}  en = {:0.3e}    en = {:0.3e}".format(self.r3,self.en_r3,self.eno_r3))
        print("R4={: 8d}  en = {:0.3e}    en = {:0.3e}".format(self.r4,self.en_r4,self.eno_r4))
        print("RS={: 8d}  en = {:0.3e}    en = {:0.3e}".format(self.rs,self.en_rs,self.eno_rs))


        eo_total=add_noise_sources([self.eno_r1,self.eno_r2,self.eno_r3,self.eno_r4,self.eno_rs,self.eno_eni])



"""
Non Inverting Amp
                  R1
            ----/\/\/\----
            |             |
      R2    | |\          |
  --/\/\/\----|-\        |
  |           |  \________|____
  0   R3      |  /
IN--/\/\/\----|+/
              |/
      
    
"""





if __name__=="__main__":
    i=inverting_amp(10000,1000,50,0,50)
    print(i)
