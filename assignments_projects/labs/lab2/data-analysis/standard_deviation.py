# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import app


class Standard_Deviation:
    def __init__(self, data_set1, data_set2, size):
        self.data_sat1 = data_set1
        self.data_sat2 = data_set2
        self.size = size
        self.mean_data_set_1 = 0.0
        self.mean_data_set_2 = 0.0
        self.std_data_set_1 = 0.0
        self.std_data_set_2 = 0.0

    def calculate_mean(self):
        self.mean_data_set_1 = np.mean(self.data_sat1)
        self.mean_data_set_2 = np.mean(self.data_sat2)

    def calculate_standard_deviation(self):
        self.std_data_set_1 = np.std(self.data_sat1)
        self.std_data_set_2 = np.std(self.data_sat2)



