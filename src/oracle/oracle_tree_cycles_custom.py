from src.dataset.dataset_base import Dataset
from src.oracle.oracle_base import Oracle

import numpy as np
import networkx as nx

class TreeCyclesCustomOracle(Oracle):

    def __init__(self, id, oracle_store_path, config_dict=None) -> None:
        super().__init__(id, oracle_store_path, config_dict)
        self._name = 'tree_cycles_custom_oracle'

    def fit(self, dataset: Dataset, split_i=-1):
        pass

    def _real_predict(self, data_instance):
        # Classify
        if len(nx.cycle_basis(data_instance.graph)) > 0:
            return 1 # has cycles
        else:
            return 0 # it has no cycles

    def embedd(self, instance):
        return instance

    def write_oracle(self):
        pass

    def read_oracle(self, oracle_name):
        pass