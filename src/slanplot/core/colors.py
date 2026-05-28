import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import os

class SlandarerColormaps:
    def __init__(self, data_dir=None):
        if data_dir is None:
            # Point to the data directory packaged within the library
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
        self.data_dir = data_dir
        self.cm_data = {}
        self.cl_data = {}
        self.ncl_data = {}

        self._load_slanCM()
        self._load_slanCL()
        self._load_nclCM()

    def _load_slanCM(self):
        mat_path = os.path.join(self.data_dir, 'slanCM_Data.mat')
        if not os.path.exists(mat_path):
            print(f"Warning: {mat_path} not found.")
            return
        
        try:
            data = sio.loadmat(mat_path)
            names = [str(n[0][0]) if len(n)>0 and len(n[0])>0 else '' for n in data['fullNames'][0]]
            colors_structs = data['slandarerCM']['Colors'][0]
            
            # flatten colors
            colors_list = []
            for group in colors_structs:
                if len(group) > 0:
                    for c in group[0]:
                        colors_list.append(c)
            
            for i, name in enumerate(names):
                if i < len(colors_list):
                    cmap = ListedColormap(colors_list[i], name=name)
                    self.cm_data[name] = cmap
                    self.cm_data[i+1] = cmap
        except Exception as e:
            print(f"Error loading slanCM: {e}")

    def _load_slanCL(self):
        mat_path = os.path.join(self.data_dir, 'slanCL_Data.mat')
        if not os.path.exists(mat_path):
            print(f"Warning: {mat_path} not found.")
            return
        
        try:
            data = sio.loadmat(mat_path)
            names = [str(k[0]) if len(k)>0 else '' for k in data['Key'][0]]
            colors_list = [c for c in data['Color'][0]]
            
            for i, name in enumerate(names):
                if i < len(colors_list):
                    cmap = ListedColormap(colors_list[i], name=name)
                    self.cl_data[name] = cmap
                    self.cl_data[i+1] = cmap
        except Exception as e:
            print(f"Error loading slanCL: {e}")

    def _load_nclCM(self):
        mat_path = os.path.join(self.data_dir, 'nclCM_Data.mat')
        if not os.path.exists(mat_path):
            print(f"Warning: {mat_path} not found.")
            return
        
        try:
            data = sio.loadmat(mat_path)
            names = [str(n[0]) if len(n)>0 else '' for n in data['Names'][0]]
            colors_list = [c for c in data['Colors'][0]]
            
            for i, name in enumerate(names):
                if i < len(colors_list):
                    cmap = ListedColormap(colors_list[i], name=name)
                    self.ncl_data[name] = cmap
                    self.ncl_data[i+1] = cmap
        except Exception as e:
            print(f"Error loading nclCM: {e}")

    def get_cm(self, identifier):
        return self.cm_data.get(identifier, None)

    def get_cl(self, identifier):
        return self.cl_data.get(identifier, None)

    def get_ncl(self, identifier):
        return self.ncl_data.get(identifier, None)
