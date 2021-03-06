#! /usr/bin/env python
# -*- coding:utf-8 -*-

import numpy as np
import unittest

from pysdnn import SDNN


class TestSDNN(unittest.TestCase):
    def setUp(self):
        # make sample data
        n_train_samples = 20
        n_test_samples = 10
        self.train_X = np.random.uniform(0, 1, size=[n_train_samples, 3])
        self.train_y = np.random.normal(size=n_train_samples)

        self.test_X = np.random.uniform(0, 1, size=[n_test_samples, 3])
        self.test_y = np.random.normal(size=n_train_samples)

    def test_fit(self):
        self.sdnn = SDNN()
        self.sdnn.fit(self.train_X, self.train_y)

    def test_predict(self):
        self.sdnn = SDNN()
        self.sdnn.fit(self.train_X, self.train_y)
        self.sdnn.predict(self.test_X)
