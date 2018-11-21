#!/usr/bin/env python
import argparse
import numpy as np

import chainer
import chainer.functions as F
import chainer.links as L


# Network definition
class MLP(chainer.Chain):

    def __init__(self, n_units, n_out):
        super(MLP, self).__init__()
        with self.init_scope():
            # the size of the inputs to each layer will be inferred
            self.l1 = L.Linear(None, n_units)  # n_in -> n_units
            self.l2 = L.Linear(None, n_units)  # n_units -> n_units
            self.l3 = L.Linear(None, n_out)  # n_units -> n_out

    def forward(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        return self.l3(h2)


def main():
    parser = argparse.ArgumentParser(description='Chainer example: MNIST')
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--out', '-o', default='result/mlp.model',
                        help='Directory to output the result')
    parser.add_argument('--unit', '-u', type=int, default=5,
                        help='Number of units')
    args = parser.parse_args()

    print('GPU: {}'.format(args.gpu))
    print('# unit: {}'.format(args.unit))
    print('')

    # Set up a neural network to train
    # Classifier reports softmax cross entropy loss and accuracy at every
    # iteration, which will be used by the PrintReport extension below.
    model = L.Classifier(MLP(args.unit, 10))

    # Load the MNIST dataset
    train, test = chainer.datasets.get_mnist()

    # Load weight
    chainer.serializers.load_npz(args.out, model)

    # Run inference
    x = chainer.Variable(np.asarray([test[0][0]])) # test data 
    t = chainer.Variable(np.asarray([test[0][1]])) # labels
    y = model.predictor(x).data # inference result
    pred_label = y.argmax(axis=1)

    print('The test data label:',np.asarray([test[0][1]]))
    print('result:', pred_label[0])


if __name__ == '__main__':
    main()
