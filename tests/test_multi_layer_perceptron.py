import numpy as np
import unittest

from pysdnn.multi_layer_perceptron import MultiLayerPerceptronRegression


class Test_MultiLayerPerceptronRegression(unittest.TestCase):
    def setUp(self):
        # make sample data
        n_train_samples = 200
        n_test_samples = 100
        self.train_X = np.random.uniform(0, 1, size=[n_train_samples, 2])
        self.train_y = np.random.normal(size=n_train_samples)

        self.test_X = np.random.uniform(0, 1, size=[n_test_samples, 2])
        self.test_y = np.random.normal(size=n_train_samples)

        self.mlpr = MultiLayerPerceptronRegression(hidden_layer_num=100, eta=0.01)

    def test_fit(self):
        self.mlpr.fit(self.train_X, self.train_y)

    def test_predict(self):
        self.mlpr.fit(self.train_X, self.train_y)
        self.mlpr.predict(self.test_X)
