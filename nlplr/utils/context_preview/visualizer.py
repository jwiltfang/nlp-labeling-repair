import pm4py

from pm4py.algo.discovery.dfg import algorithm as dfg_discovery
from pm4py.visualization.dfg import visualizer as dfg_visualization
from pm4py.algo.discovery.heuristics import algorithm as heuristics_miner

import os
from abc import ABC, abstractmethod


class GraphVisualizer(ABC):
    def __init__(self, log: pm4py.objects.log.log.EventLog):
        self.log = log
        self.graph = None

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def save_pdf(self, save_location: str):
        pass

    @abstractmethod
    def view(self):
        pass

    def get_save_location(self, save_location: str):
        return os.path.join(save_location)


class DFGraph(GraphVisualizer):
    def __init__(self, log):
        super().__init__(log)

    def run(self):
        self.graph = dfg_discovery.apply(self.log, variant=dfg_discovery.Variants.FREQUENCY)

    def save_pdf(self, save_location: str):
        parameters = {dfg_visualization.Variants.FREQUENCY.value.Parameters.FORMAT: 'pdf'}
        gviz = dfg_visualization.apply(self.graph, log=self.log, parameters=parameters,
                                       variant=dfg_visualization.Variants.FREQUENCY)
        dfg_visualization.save(gviz, self.get_save_location(save_location))
        return self.get_save_location(save_location)

    def view(self):
        gviz = dfg_visualization.apply(self.graph, log=self.log, variant=dfg_visualization.Variants.FREQUENCY)
        dfg_visualization.view(gviz)


class HeuristicsGraph(GraphVisualizer):
    def __init__(self, log):
        super().__init__(log)

    def run(self):
        parameters = heuristics_miner.Variants.CLASSIC.value.Parameters
        dependency_threshold, and_threshold, loop_two_threshold, dfg_pre_cleaning_noise_tresh = 0.5, 0.65, 0.5, 0.05
        self.graph = heuristics_miner.apply_heu(self.log,
                                                variant=heuristics_miner.Variants.CLASSIC,
                                                parameters={parameters.DEPENDENCY_THRESH: dependency_threshold,
                                                            parameters.AND_MEASURE_THRESH: and_threshold,
                                                            parameters.DFG_PRE_CLEANING_NOISE_THRESH: dfg_pre_cleaning_noise_tresh,
                                                            parameters.LOOP_LENGTH_TWO_THRESH: loop_two_threshold})

    def save_pdf(self, save_location: str):
        pm4py.save_vis_heuristics_net(self.graph, self.get_save_location(save_location))
        return save_location

    def view(self):
        pm4py.view_heuristics_net(self.graph)
