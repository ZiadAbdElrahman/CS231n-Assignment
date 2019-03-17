import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
    
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    
    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    
    num_train = X.shape[0]
    num_classes = W.shape[1]
    loss = 0.0
    for i in range(num_train):

        f_i = X[i].dot(W)
        f_i -= np.max(f_i)

        sum_j = np.sum(np.exp(f_i))
        p = lambda k: np.exp(f_i[k]) / sum_j
        loss += -np.log(p(y[i]))

        for k in range(num_classes):
            p_k = p(k)
            dW[:, k] += (p_k - (k == y[i])) * X[i]
    pass
    #############################################################################
    #                          END OF YOUR CODE                                 #
    #########################################################################
    loss /= num_train
    loss += reg * np.sum(W * W)
    dW /= num_train
    dW += reg*W

    return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    
    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    score = X.dot(W)
    score_e = np.exp(score)
    #a[np.arange(4), b]
    loss = np.sum(-np.log(score_e[np.arange(X.shape[0]),y]/np.sum(score_e,axis = 1)))
    dif = loss
    loss/= X.shape[0]
    loss += reg * np.sum(W * W)
    
    dW = X.T.dot(score_e)
    
    dW[np.arange(X.shape[0]),y] = (X.T.dot(score_e-1))[np.arange(X.shape[0]),y]
    dW /= X.shape[0]
    dW += reg*W
    
    num_train = X.shape[0]
    f = X.dot(W)
    f -= np.max(f, axis=1, keepdims=True)
    sum_f = np.sum(np.exp(f), axis=1, keepdims=True)
    p = np.exp(f)/sum_f

    loss1 = np.sum(-np.log(p[np.arange(num_train), y]))
    ind = np.zeros_like(p)
    ind[np.arange(num_train), y] = 1
    dW = X.T.dot(p - ind)
    dW /= num_train
    dW += reg*W
    pass
    #############################################################################
    #                          END OF YOUR CODE                                 #
    #############################################################################

    return loss, dW

