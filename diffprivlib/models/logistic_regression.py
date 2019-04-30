import numpy as np
from scipy.optimize import minimize
from sklearn.base import BaseEstimator

from diffprivlib.mechanisms import Vector


class LogisticRegression(BaseEstimator):
    def __init__(self, epsilon, lam=0.01, verbose=0):
        self.epsilon = epsilon
        self.verbose = verbose
        self.lam = lam
        self.beta = None

    def decision_function(self, X):
        pass

    def predict_proba(self, X):
        pass

    @staticmethod
    def loss(beta, x, label):
        exponent = beta[0] + np.dot(beta[1:], x)
        return np.log(1 + np.exp(exponent)) - label * exponent

    def fit(self, X, y, sample_weight=None):
        del sample_weight
        n, d = X.shape
        beta0 = np.zeros(d + 1)

        def objective(beta):
            total = 0

            for i in range(n):
                total += self.loss(beta, X[i, :], y[i])

            total /= n
            total += self.lam / 2 * np.linalg.norm(beta) ** 2

            return total

        vector_mech = Vector().set_dimensions(d, n).set_epsilon(self.epsilon).set_lambda(self.lam)
        noisy_objective = vector_mech.randomise(objective)

        noisy_beta = minimize(noisy_objective, beta0, method='Nelder-Mead').x
        self.beta = noisy_beta

        return self

    def predict(self, X):
        pass
