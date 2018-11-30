#!/usr/bin/env python
import argparse
import numpy as np
from os.path import abspath, expanduser

import chainer
import chainer.functions as F
import chainer.links as L
from .mlp import MLP

def main():
    parser = argparse.ArgumentParser(description='Chainer example: MNIST')
    parser.add_argument('--gpu', '-g', type=int, default=-1,
                        help='GPU ID (negative value indicates CPU)')
    parser.add_argument('--out', '-o', default='~/model_root',
                        help='Directory to output the result')
    parser.add_argument('--unit', '-u', type=int, default=5,
                        help='Number of units')
    parser.add_argument('--filename', default='mlp.model',
                        help='Model filename')
    args = parser.parse_args()

    print('GPU: {}'.format(args.gpu))
    print('# unit: {}'.format(args.unit))
    print('')

    # get the absoult path
    args.out = abspath(expanduser(args.out))

    # Set up a neural network to train
    # Classifier reports softmax cross entropy loss and accuracy at every
    # iteration, which will be used by the PrintReport extension below.
    model = L.Classifier(MLP(args.unit, 10))

    # Load the MNIST dataset
    train, test = chainer.datasets.get_mnist()

    # Load weight
    chainer.serializers.load_npz('{}/{}'.format(args.out, args.filename), model)

    # Run inference
    x = chainer.Variable(np.asarray([test[0][0]])) # test data 
    t = chainer.Variable(np.asarray([test[0][1]])) # labels
    y = model.predictor(x).data # inference result
    pred_label = y.argmax(axis=1)

    print('The test data label:',np.asarray([test[0][1]]))
    print('result:', pred_label[0])


if __name__ == '__main__':
    main()
