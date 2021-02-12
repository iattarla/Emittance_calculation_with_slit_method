# meanx     : mean position of all beamlets.
# meanXj    : mean position of j-th beamlet.
# meanxpj   : mean divergence of j-th beamlet.
# meanxp    : mean divergence of all beamlets.
# sigmaj    : rms spot size of j-th beamlet on screen.
# sigmapj   : rms divergence of j-th beamlet.def EmittanceCalc(x,weight,mins,maxs,L_slitscreen):
import numpy as np
import math
##########
##########
def mean_xslit(x,data,ind_mins,ind_maxs,xslits):
    tmp=0
    for i in range(len(xslits)):
        weight=0
        for j in range(ind_mins[i],ind_mins[i+1]):
            weight=weight+data[j]
        
        tmp=tmp+weight*xslits[i]
    return tmp/sum(data)

def var_x(x,data,ind_mins,ind_maxs,xslits):
    mx=mean_xslit(x,data,ind_mins,ind_maxs,xslits)
    tmp=0
    for i in range(len(xslits)):
        weight=0
        for j in range(ind_mins[i],ind_mins[i+1]):
            weight=weight+data[j]
        tmp=tmp+weight*(xslits[i]-mx)**2
    return tmp/sum(data)
##########
##########
def mean_Xj(x,data,ind_mins,ind_maxs,xslits):
    tmp=[]
    for i in range(len(xslits)):
        weight=0
        X_=0
        for j in range(ind_mins[i],ind_mins[i+1]):
            weight=weight+data[j]
            X_=X_+x[j]*data[j]
        tmp.append(X_/weight)
    return tmp

def mean_xdotj(x,data,ind_mins,ind_maxs,L_slitscreen,xslits):
    mXj=mean_Xj(x,data,ind_mins,ind_maxs,xslits)
    return(mXj-xslits)/L_slitscreen

def mean_xdot(x,data,ind_mins,ind_maxs,L_slitscreen,xslits):
    mxdotj=mean_xdotj(x,data,ind_mins,ind_maxs,L_slitscreen,xslits)
    tmp=0
    for i in range(len(xslits)):
        weight=0
        for j in range(ind_mins[i],ind_mins[i+1]):
            weight=weight+data[j]
        tmp=tmp+weight*mxdotj[i]
    return tmp/sum(data)
    
def sigmaj(x,data,ind_mins,ind_maxs,L_slitscreen,xslits):
    mXj=mean_Xj(x,data,ind_mins,ind_maxs,xslits)
    tmp=[]
    for i in range(len(xslits)):
        weight=0
        X2_=0
        for j in range(ind_mins[i],ind_mins[i+1]):
            weight=weight+data[j]
            X2_=X2_+data[j]*(x[j]-mXj[i])**2
        tmp.append(math.sqrt(X2_/weight))
    return np.array(tmp)/L_slitscreen

def var_xdot(x,data,ind_mins,ind_maxs,L_slitscreen,xslits):
    mxdotj=mean_xdotj(x,data,ind_mins,ind_maxs,L_slitscreen,xslits)
    mxdot=mean_xdot(x,data,ind_mins,ind_maxs,L_slitscreen,xslits)
    sigj=sigmaj(x,data,ind_mins,ind_maxs,L_slitscreen,xslits)
    
    tmp=0
    for i in range(len(xslits)):
        weight=0
        for j in range(ind_mins[i],ind_mins[i+1]):
            weight=weight+data[j]
        tmp=tmp+weight*( sigj[i]**2+(mxdotj[i]-mxdot)**2  )
    return tmp/sum(data)
##########
##########
def mean_xxdot(x,data,ind_mins,ind_maxs,L_slitscreen,xslits):
    mxdotj=mean_xdotj(x,data,ind_mins,ind_maxs,L_slitscreen,xslits)
    mx=mean_xslit(x,data,ind_mins,ind_maxs,xslits)
    mxdot=mean_xdot(x,data,ind_mins,ind_maxs,L_slitscreen,xslits)
    tmp=0
    for i in range(len(xslits)):
        weight=0
        for j in range(ind_mins[i],ind_mins[i+1]):
            weight=weight+data[j]
        tmp=tmp+weight*xslits[i]*mxdotj[i]
    N=sum(data)
    ret=(tmp-sum(data)*mx*mxdot)
    return ret/N
##########
##########    
def EmittanceCalc(x,data,ind_mins,ind_maxs,L_slitscreen):
    ####################
    ####################
    leng=len(ind_maxs)
    xs=[0]
    dxs=2.25e-3+100e-6
    for i in range(int((leng-1)/2)):
        xs.append(xs[-1]+dxs)
    xs1=np.array(xs[1:])
    xs2=np.sort(-xs1)

    xs=[]
    xs=np.concatenate((xs2,[0], xs1))+max(xs1)
    #####################
    #####################    
    
    varx=var_x(x,data,ind_mins,ind_maxs,xs)
    varxdot=var_xdot(x,data,ind_mins,ind_maxs,L_slitscreen,xs)
    meanxxdot=mean_xxdot(x,data,ind_mins,ind_maxs,L_slitscreen,xs)
    
    #print(varx)
    #print(varxdot)
    #print(meanxxdot)
    
    emit=math.sqrt(varx*varxdot-meanxxdot**2)

    return emit
