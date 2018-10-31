import matplotlib.pyplot as plt
import numpy as np

def sigmoid(x): 
    x = x / (1024*1024*512)                                     
    nop = 64 / (1 + 8*(np.exp(-x)))
    if(nop < 8):
        return int(nop)
    else:
        return 8 * int(round(nop / 8))


mb = 1024*1024
print(sigmoid(2*1024*mb))