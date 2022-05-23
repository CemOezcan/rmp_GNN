import pickle

from src import util
from src.tasks.AbstractTask import AbstractTask
from data.data_loader import get_data, DATA_DIR
from util.Types import *  # TODO change
from torch.utils.data import DataLoader  # NOTE not accessed
from torch.utils.data import TensorDataset  # NOTE not accessed
import torch
import plotly.graph_objects as go
from src.algorithms.AbstractIterativeAlgorithm import AbstractIterativeAlgorithm
from src.algorithms.FlagSimulator import MeshSimulator
from src.data.dataset import load_dataset

device = torch.device('cuda')

class MeshTask(AbstractTask):
    # TODO comments and discussion about nested functions
    def __init__(self, algorithm: AbstractIterativeAlgorithm, config: ConfigDict):
        """
        Initializes all necessary data for a classification task.

        Args:
            config: A (potentially nested) dictionary containing the "params" section of the section in the .yaml file
                used by cw2 for the current run.
        """
        super().__init__(algorithm=algorithm, config=config)
        self._raw_data = get_data(config=config)
        self._rollouts = config.get('task').get('rollouts')
        self.train_loader = get_data(config=config)

        self._test_loader = get_data(config=config, split='test', split_and_preprocess=False)

        self.mask = None

        self._algorithm.initialize(task_information=config)
        self._dataset_name = config.get('task').get('dataset')

    def run_iteration(self):
        assert isinstance(
            self._algorithm, MeshSimulator), "Need a classifier to train on a classification task"
        self._algorithm.fit_iteration(train_dataloader=self.train_loader)

    # TODO add trajectories from evaluate method
    def get_scalars(self) -> ScalarDict:
        assert isinstance(self._algorithm, MeshSimulator)
        return self._algorithm.evaluator(self._test_loader, self._rollouts)

    def plot(self) -> go.Figure:
        if not self._input_dimension == 2:
            raise NotImplementedError(
                "plotting not supported for {}-dimensional features", self._input_dimension)
        # 2d classification, allowing for a contour plot
        assert isinstance(self._algorithm, MeshSimulator)
        points_per_axis = 5
        X = self.raw_data.get("X")
        y = self.raw_data.get("y")
        bottom_left = np.min(X, axis=0)
        top_right = np.max(X, axis=0)
        x_margin = (top_right[0] - bottom_left[0]) / 2
        y_margin = (top_right[1] - bottom_left[1]) / 2
        x_positions = np.linspace(
            bottom_left[0] - x_margin, top_right[0] + x_margin, num=points_per_axis)
        y_positions = np.linspace(
            bottom_left[1] - y_margin, top_right[1] + y_margin, num=points_per_axis)
        evaluation_grid = np.transpose([np.tile(x_positions, len(y_positions)),
                                        np.repeat(y_positions, len(x_positions))])

        good_samples = X[y == 1]
        bad_samples = X[y == 0]

        reward_evaluation_grid = self._algorithm.predict(evaluation_grid)
        reward_evaluation_grid = reward_evaluation_grid.reshape(
            (points_per_axis, points_per_axis))
        reward_evaluation_grid = np.clip(
            a=reward_evaluation_grid, a_min=-3, a_max=3)
        fig = go.Figure(data=[go.Contour(x=x_positions, y=y_positions, z=reward_evaluation_grid,
                                         colorscale="Portland", ),
                              go.Scatter(x=good_samples[::10, 0], y=good_samples[::10, 1],
                                         mode="markers", fillcolor="green", showlegend=False),
                              go.Scatter(x=bad_samples[::10, 0], y=bad_samples[::10, 1],
                                         mode="markers", fillcolor="red", showlegend=False)
                              ])
        return fig
