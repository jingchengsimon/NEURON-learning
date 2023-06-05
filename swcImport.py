import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

swc_file = 'cell1'
segs = pd.read_csv('./{x}.swc'.format(x=swc_file),comment='#',sep=' ', 
    names=['id','type','x','y','z','r','pid'])
segs_ = segs.merge(segs,left_on='id',right_on='pid',suffixes=[None, '_p'])
print(segs_['type'])
print("done")
