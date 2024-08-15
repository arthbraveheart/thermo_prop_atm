import math as m
import matplotlib as mpl
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


 

class atm_:

 
 r=6356.766 # Raio da Terra (km)
 g=9.80665 # Aceleração da gravidade (m/s)
 mz=28964.4 # Peso molecular (Kg/mol)
 R=8314.32 # Constante dos gases ideiais (kJ.mol⁻¹.K⁻¹)

 def ref_(z_h):
    """
     

     Parameters
     ----------
     z_h : TYPE
         DESCRIPTION.

     Returns
     -------
     h : TYPE
         DESCRIPTION.
     hs : TYPE
         DESCRIPTION.
     ls : TYPE
         DESCRIPTION.
     ts : TYPE
         DESCRIPTION.
     ps : TYPE
         DESCRIPTION.

     """
   
    ref=[[0,-6.5,288.15,101325],[11,0,216.65,22632.04],[20,1,216.65,5474.875],
     [32,2.8,228.65,868.0153],[47,0,270.65,110.9057],[51,-2.8,270.6,66.93847],
     [71,-2,214.65,3.956387]]
    
    h=atm_.r*z_h/(atm_.r + z_h)
    sub= (0*(h>=0 and h<11) +1*(h>=11 and h<20) +2*(h>=20 and h<32) +3*(h>=32 and h<47)
       +4*(h>=47 and h<51) +5*(h>=51 and h<71) +6*(h>=71 and h<84.8520))

    hs=ref[sub][0] # Altitude geopotencial (km)
    ls=ref[sub][1] # Gradiente de temperatura em escala molecular (k/km)
    
    ts=ref[sub][2] # Temperatura molecular (K)
    ps=ref[sub][3] # Pressão geopotencial (Pa)
    return h,hs,ls,ts,ps

 def __init__(self,temp, press, vel_som): 
    """
     

     Parameters
     ----------
     temp : TYPE
         DESCRIPTION.
     press : TYPE
         DESCRIPTION.
     vel_som : TYPE
         DESCRIPTION.

     Returns
     -------
     None.

     """
     
    self.T_h=temp
    self.a_h=vel_som
    self.P_h=press
 
 def prop_(z_h):
    """
     

     Parameters
     ----------
     z_h : TYPE
         DESCRIPTION.

     Returns
     -------
     temp : TYPE
         DESCRIPTION.
     press : TYPE
         DESCRIPTION.
     vel_som : TYPE
         DESCRIPTION.

     """
    h,hs,ls,ts,ps= atm_.ref_(z_h)[0], atm_.ref_(z_h)[1], atm_.ref_(z_h)[2], atm_.ref_(z_h)[3], atm_.ref_(z_h)[4]
    
    temp=ts+ls*(h-hs)
    vel_som=3.6*331.45*(temp/273.15)**(0.5)
    if (ls==0):
     press=ps*(m.exp((-atm_.g*atm_.mz*(h-hs)/(atm_.R*ts))))
    else:
     press=ps*(ts/temp)**(atm_.g*atm_.mz/(atm_.R*ls))   
   
    return temp, press, vel_som
 
 def plot_():
    """
     

     Returns
     -------
     None.

     """
    
    z_h=float(input("Escolha uma altura menor que 84.8520km: ")) 
    
    tabela={'Propriedades Termodinâmicas na altura requerida':
            [atm_.ref_(z_h)[0],atm_.prop_(z_h)[0], atm_.prop_(z_h)[1], atm_.prop_(z_h)[2]] }
    print(pd.DataFrame(tabela, index= ["Altitude geopotencial (Km): ","Temperatura (K): ", " Pressão (kPa):",
                                        " Velocidade do som (km/h): "]))
    
    T=[atm_.prop_(i)[0] for i in np.arange(0,80,0.01)]
    P=[atm_.prop_(i)[1] for i in np.arange(0,80,0.01)]
    a=[atm_.prop_(i)[2] for i in np.arange(0,80,0.01)]
    
    prop_escolhida=input("Agora, escolha uma propriedade termodinâmica a ser plotada:") 
    prop_termd={'Temperatura': T, 
            'Pressão': P, 
            'Velocidade do som': a,
             }
    temp, press, vel_som = atm_.prop_(z_h)[0], atm_.prop_(z_h)[1], atm_.prop_(z_h)[2]
    atm_termd={temp: T, 
           press: P, 
           vel_som: a,
             }
    legenda={temp: 'Temperatura (K)',
         press: 'Pressão (kPa)',
         vel_som: 'Velocidade do som (Km/h)'}
    
    mpl.rcParams['legend.fontsize'] = 10
    fig = plt.figure()
    fig, (atm) = plt.subplots(1, 1)
    
    prop=temp*(prop_termd[prop_escolhida]==T) + press*(prop_termd[prop_escolhida]==P) + vel_som*(prop_termd[prop_escolhida]==a) # Ponto escolhido no gráfico
    
    plt.style.use('ggplot')
    atm.plot(prop_termd[prop_escolhida],[atm_.ref_(i)[0] for i in np.arange(0,80,0.01)],'b--') #Plotar o gráfico de escolha (Temperatura, Pressão ou Velocidade do Som) 
    atm.plot(prop,z_h, '--o') #Evidencia o ponto escolhido no gráfico
    atm.set_xlabel(legenda[prop])
    atm.set_ylabel('Geometric Altitude(Km)')
    atm.grid(True) 
    plt.show()


atm_.plot_()
