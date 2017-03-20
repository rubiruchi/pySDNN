#! /usr/bin/env python
# -*- coding:utf-8 -*-
""" Copyright (C) 2017 Yu Kabasawa

This is licensed under an MIT license. See the readme.md file
for more information.

"""

import numpy as np


class PatternCoding(object):
    """ PatternCodingクラスは実数とコードパターンの対応関係の管理を行うクラスです.


    コードパターンとは :math:`\{-1,1\}` を要素とする :math:`M` 次元ベクトルを指し,
    コーディングとは実数をコードパターンに変換する事を指します.

    PatternCodingクラスでは :math:`N` 次元の実数ベクトルを一括して扱い,
    コーディングの出力結果は :math:`N \\times M` 次元ベクトルです.

    コードパターンは以下の条件を満たす.

    - 入力次元ごとに異なるパターンを持つ
    - 重複が無い
    - -1と1の数の数が等しい

    Parameters
    ----------
    code_pattern_dim : int
        コードパターンベクトルの次元数 n
    input_division_num : int
        実数の分割数 q
    reversal_num : int
        反転数 r
    input_dim : int
        入力データの次元数 N
    """

    def __init__(self, code_pattern_dim, input_division_num, reversal_num, input_dim):
        self.code_pattern_dim = code_pattern_dim
        self.input_division_num = input_division_num
        self.reversal_num = reversal_num

        self.input_dim = input_dim
        # コードパターン対応表 shape = (self.input_dim, self.division_num, self.code_pattern_dim)
        self.code_pattern_table = []

        self._create_code_pattern_table()

    def _create_code_pattern_table(self):
        """実数とコードパターンの対応表を作成する"""

        for i in range(self.input_dim):
            self.code_pattern_table.append(self._create_code_pattern())

        self.code_pattern_table = np.stack(self.code_pattern_table)

        return None

    def _create_code_pattern(self):
        """コードパターンを作成する

        Returns
        -------
        code_pattern : ndarray, shape = (division_num,code_pattern_dim)

        """

        code_pattern = []
        binary_vector = np.ones(self.code_pattern_dim)
        binary_vector[:int(self.code_pattern_dim / 2)] = -1
        np.random.shuffle(binary_vector)
        code_pattern.append(binary_vector)

        while len(code_pattern) < self.input_division_num:
            while True:
                tmp_binary_vector = np.copy(code_pattern[-1])
                # select reverse index
                index1 = list(
                    np.random.choice(np.where(tmp_binary_vector == -1)[0], size=self.reversal_num, replace=False))
                index2 = list(
                    np.random.choice(np.where(tmp_binary_vector == 1)[0], size=self.reversal_num, replace=False))
                index = index1 + index2

                # reverse selected index
                tmp_binary_vector[index] *= -1

                # if tmp_binary_vector is included in code_pattern, add to code_pattern
                if not any((tmp_binary_vector == x).all() for x in code_pattern):
                    code_pattern.append(tmp_binary_vector)
                    break

        return np.array(code_pattern)

    def coding(self, X):
        """ コードパターン表から入力された実数に対応するコードパターンを取得する

        Parameters
        ----------
        X : ndarray
            入力データ

        Returns
        -------
        code_pattern : ndarray, shape =(binary_vector_dim * input_dim),(binary_vector_dim * input_dim,input_data_num)

        """

        if X.ndim == 1:
            pattern_list = []
            for feature_index, element in enumerate(X):
                index = int(np.floor(element * self.input_division_num))

                pattern_list.append(self.code_pattern_table[feature_index, index])

            return np.ravel(pattern_list)

        elif X.ndim == 2:
            matrix_list = []
            for x in X:
                pattern_list = []
                for i, element in enumerate(x):
                    index = int(np.floor(element * self.input_division_num))

                    pattern_list.append(self.code_pattern_table[i][index])
                matrix_list.append(np.ravel(pattern_list))
            code_pattern = np.array(matrix_list)
            return code_pattern
        else:
            raise ValueError('input data dimensions must be 1d or 2d')


class SelectiveDesensitization(PatternCoding):
    """
    パターンを選択的不感化する
    .. math::

       \phi : x \mapsto \mathbf{p}

    """

    def __init__(self, binary_vector_dim, division_num, reversal_num=1):
        super().__init__(binary_vector_dim, division_num, reversal_num)

    def pattern_to_sd_pattern(self, pattern1, pattern2):
        sd_pattern = (1 + pattern1) * pattern2 / 2.0
        return sd_pattern

    def num_to_sd_pattern(self, X):
        """
        選択的不感化したパターンを返す



        Parameters
        ----------
        X : array, shape = (n_features,)

        Returns
        -------
        sd_pattern : ndarray, shape = (n_features * (n_features - 1) / 2 * binary_vector_dim,)
        """
        sd_pattern_list = []
        for x in X:
            pattern_list = []
            for i, element in enumerate(x):
                index = int(np.floor(element * self.division_num))
                pattern_list.append(self.code_pattern_table[i][index])
            sd_pattern = []
            for i, pattern1 in enumerate(pattern_list):
                for j, pattern2 in enumerate(pattern_list):
                    if i == j:
                        continue
                    else:
                        sd_pattern.append(self.pattern_to_sd_pattern(pattern1, pattern2))

            sd_pattern_list.append(np.ravel(sd_pattern))
        return np.array(sd_pattern_list)
