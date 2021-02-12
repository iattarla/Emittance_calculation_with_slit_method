import numpy as np
def SmoothData(data,nsmooth):
    leng=len(data)
    ww=int(leng*0.01)
    ret=data
    
    for i in range(nsmooth):
        tmp=[]
        for j in range(leng):
            sum_=0
            if j<=ww:
                min_=0
                max_=j+ww
            if (leng-j)<=ww:
                min_=j-ww
                max_=leng
            else:
                min_=j-ww
                max_=j+ww
            
            for k in range(min_,max_):
                sum_=sum_+ret[k]/(max_-min_)
            
            tmp.append(sum_)
        ret=tmp
    return np.array(ret)

def FindExtremum(data):
    data=data
    from scipy.signal import find_peaks
    ind_maxs, _ = find_peaks(np.array(data), height=0)
    ind_mins, _ = find_peaks(np.array(-data+max(data)), height=0)
    return ind_mins,ind_maxs

import math
def StandartDeviation(data,mu):
    leng=len(data)
    tmp=0
    M=0
    for i in range(leng):
        tmp=tmp+data[i]*(i-mu)**2
        if data[i]!=0:
            M=M+1
    calc2=(M-1)/M*sum(data)
    calc=math.sqrt(tmp/calc2)
    
    return calc

def Gaussian(mean,sigma,A,size):
    ret=[]
    for x in range(size):
        gau=math.exp((-(x-mean)**2)/(2*sigma**2))/math.sqrt(2*math.pi*sigma**2)
        ret.append(gau)
    maxx=max(ret)
    for i in range(size):
        ret[i]=A*ret[i]/maxx
    return ret

def MultiGaussFit(data):
    smooth=SmoothData(data,2)
    smooth=smooth/max(smooth)
    
    local=FindExtremum(smooth)
    ind_mins=local[0]
    ind_maxs=local[1]

    while (len(ind_maxs)>=len(ind_mins)):
        ind_maxs=ind_maxs[1:-1]
                
    A_maxs=smooth[ind_maxs]
    
    leng=len(smooth)
    gauss_=[0]*leng
    for i in range(len(ind_maxs)):
        
        s_data=[]
        for j in range(ind_mins[i],ind_mins[i+1]):
            s_data.append(smooth[j])
        
        mu=ind_maxs[i]-ind_mins[i]
        std_=StandartDeviation(s_data,mu)
        
        gauss2_=Gaussian(ind_maxs[i],std_,A_maxs[i],leng)
        
        for j in range(leng):
            gauss_[j]=gauss_[j]+gauss2_[j]
    
    return ind_maxs,ind_mins,A_maxs,gauss_
    
    
    
    
    
