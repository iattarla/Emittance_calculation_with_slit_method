#####################################
# Ali Can CANBAY        04/01/2021
#####################################
#python run.py
#####################################
import sys
sys.path.insert(1, 'functions')
import emittance as emt
import fitting as ft
import image as im
import smoothing as smo
import numpy as np
import matplotlib.pyplot as plt

screen_size=0.04
L=0.115

r_data=im.fromImage("L0115_s004_e20.png")
Intensity_y=np.array(r_data[0])
Intensity_x=np.array(r_data[1])

height=max(Intensity_x)
Intensity_x[Intensity_x < height*0.1]=0
Intensity_x=Intensity_x/height

x=np.linspace(0,(len(Intensity_x)-1)*screen_size/len(Intensity_x),num=len(Intensity_x))
output=ft.MultiGaussFit(Intensity_x)

ind_maxs=output[0]
ind_mins=output[1]
A_maxs=output[2]
gauss_=output[3]

plt.plot(x,Intensity_x)
plt.plot(x,gauss_)
plt.show()

#emit=emt.EmittanceCalc(x,gauss_,ind_mins,ind_maxs,L)
emit=emt.EmittanceCalc(x,gauss_,ind_mins,ind_maxs,L)*10/14.374; # with experimental scale factor
emit=format(emit*1e6, '.3f')

print(emit)
