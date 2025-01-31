from src.dataset.dataset_base import Dataset
from src.oracle.oracle_base import Oracle

import numpy as np

class ASDCustomOracle(Oracle):

    def __init__(self, id, oracle_store_path, config_dict=None) -> None:
        super().__init__(id, oracle_store_path, config_dict)
        self._name = 'asd_custom_oracle'
        

    def _sub_graph(self, g, v_sub):
        '''To create the sub graph of 'g' from the list of nodes in 'v_sub'.
        '''
        g_sub = np.copy(g)
        #l_1 = [el for el in v_sub]
        l_1 = [el for el in v_sub]
        g_sub = g_sub[np.ix_(l_1,l_1)]
        return g_sub

    def _feature_extraction(self, g):
        ''' The classification funcion for the graph 'g'
        '''
        # Sub-graphs
        td_asd = [65, 70, 99, 80, 69, 6, 7, 8, 9, 13, 77, 45, 16, 81, 78, 92, 56, 57, 60, 93, 63]
        asd_td = [0, 36, 37, 38, 81, 40, 41, 74, 75, 76, 70, 72, 114, 20, 21, 73, 90, 28, 29]

        # Induced sub-graphs
        g_td_asd = self._sub_graph(g,td_asd)
        g_asd_td = self._sub_graph(g,asd_td)

        # Coefficients
        a = sum([sum(i) for i in g_td_asd])/2
        b = sum([sum(i) for i in g_asd_td])/2
        return a,b
        

    def fit(self, dataset: Dataset, split_i=-1):
        pass     
        
    def _real_predict_proba(self, data_instance):
        cls = self._real_predict(data_instance)
        if cls:
            return np.array([0,1])
        else:
            return np.array([1,0])
        
        
    def _real_predict(self, data_instance):
        g = data_instance.to_numpy_array()
        f = self._feature_extraction(g)
        # Apply the rule
        w_1 = -0.181742414867891
        w_2 = 0.04327200353999672
        bk = 3.2844839747590915 
        x = bk + w_1*f[0] + w_2*f[1]

        return 1 if x > 0 else 0

    def embedd(self, instance):
        return instance

    def write_oracle(self):
        pass

    def read_oracle(self, oracle_name):
        pass
