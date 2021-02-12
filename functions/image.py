def fromData(data_addr):
    with open(data_addr, 'r') as f:
        r_data = [[float(num) for num in line.split(' ')] for line in f]
    lx=len(r_data)
    ly=len(r_data[1])
    
    import imageio
    imageio.imwrite('out.png', r_data)
    
    x=[0]*lx
    y=[0]*ly
    
    for i in range(lx):
        for j in range(ly):
            x[i]=x[i]+r_data[i][j]
            y[j]=y[j]+r_data[i][j]
    return x,y

def fromImage(imag_addr):
    import numpy as np
    import matplotlib.pyplot as plt
    from PIL import Image

    fname = imag_addr
    image = Image.open(fname).convert("L")
    r_data = np.asarray(image)
    import imageio
    imageio.imwrite('out.png', r_data)
    
    lx=len(r_data)
    ly=len(r_data[1])
    
    x=[0]*lx
    y=[0]*ly
    
    for i in range(lx):
        for j in range(ly):
            x[i]=x[i]+r_data[i,j]
            y[j]=y[j]+r_data[i,j]
    return x,y
