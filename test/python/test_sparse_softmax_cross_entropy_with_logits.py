# ==============================================================================
#  Copyright 2018-2020 Intel Corporation
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ==============================================================================
"""nGraph TensorFlow bridge ReluGrad operation test

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pytest

import tensorflow as tf
from tensorflow.python.framework import constant_op
from tensorflow.python.ops.gen_nn_ops import sparse_softmax_cross_entropy_with_logits
import numpy as np
from common import NgraphTest

np.random.seed(5)


class TestSparseSoftmaxCrossEntropyWithLogitsOperations(NgraphTest):

    def test_sparse_softmax_cross_entropy_with_logits_2d(self):
        num_classes = 10
        batch_size = 1000
        total_size = num_classes * batch_size
        labels = constant_op.constant(
            self.generate_random_numbers(batch_size, 0, num_classes - 1,
                                         "DTYPE_INT"),
            shape=[batch_size])
        features = constant_op.constant(
            self.generate_random_numbers(total_size, 0.0, 1.0),
            shape=[batch_size, num_classes])

        out = sparse_softmax_cross_entropy_with_logits(features, labels)
        sess_fn = lambda sess: sess.run(out)

        expected = self.without_ngraph(sess_fn)
        result = self.with_ngraph(sess_fn)

        assert np.allclose(result[0], expected[0], rtol=0, atol=1e-02)
        assert np.allclose(result[1], expected[1], rtol=0, atol=1e-02)
