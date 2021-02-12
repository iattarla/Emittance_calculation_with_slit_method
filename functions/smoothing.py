def bsmooth(data):
    ret=data
    for i in range(4):
        for j in range(1,len(data)-1):
            ret[j]=(data[j-1]+data[j]+data[j+1])/3
    return ret

def hsmooth(data):
    leng=len(data)
    ww=int(len(data)*0.01)
    ret=[]
    for i in range(leng):
        tmp=0;
        if i<=ww:
            min_=0
            max_=i+ww
        if (leng-i)<=ww:
            min_=i-ww
            max_=leng
        else:
            min_=i-ww
            max_=i+ww
        
        for j in range(min_,max_):
            tmp=tmp+data[j]
            
        ret.append(tmp/(2*ww))
    return ret
