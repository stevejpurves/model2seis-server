import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import misc
from tqdm import tqdm

model_dir = "./datasets/model/"
out_model_dir = "./datasets/pynoddy_ricker10/trainA/"
seismic_dir = "./datasets/seismic_r10/"
out_seismic_dir = "./datasets/pynoddy_ricker10/trainB/"


filenames = []
for filename in os.listdir(model_dir):
    if filename.endswith(".npy"):
        filenames.append(filename)
        
counter = 1
for filename in tqdm(filenames):
    print filename
    data = np.load(model_dir+filename)
    misc.imsave(out_model_dir+str(counter)+"_A.png", data)
    split_str =filename.split("_")
    seismic_filename = "_".join([split_str[0], "seismic_r10"]+split_str[2:])
    data = np.load(seismic_dir+seismic_filename)
    misc.imsave(out_seismic_dir+str(counter)+"_B.png", data)
    counter += 1 
