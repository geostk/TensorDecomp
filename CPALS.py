import numpy as np
from numpy.linalg import pinv
from numpy.linalg import norm

# my modules
import tensor_operator as to
import logger
import dataloader as dl

class CPALS(object):
    def __init__(self, dim_list, rank):
        self.dim_list = dim_list
        self.rank = rank
        self.N = len(self.dim_list)
        self.fmats = self._make_init_factor_matrices(self.rank)
        self.logger = logger.CPALSLogger(columns = ["step", "obj_val"])

    def fit(self, X, iter_num=100):
        # add obj_val of random factor matrices.
        X_hat = self._calc_X_hat()
        obj_val = self.objective_func(X, X_hat)
        new_row = [0, obj_val]
        self.logger.append(new_row)

        for step in np.arange(1, iter_num+1):
            self._update_factor_matrices(X)
            X_hat = self._calc_X_hat()
            obj_val = self.objective_func(X, X_hat)
            new_row = [step, obj_val]
            self.logger.append(new_row)

        return self

    def _make_init_factor_matrix(self, dim, rank):
        """
        returns
            fmat : ndarray
        """
        fmat = np.random.randn(dim, rank)
        return fmat

    def _make_init_factor_matrices(self, rank):
        """
        returns
            fmats : ndarray
        """
        fmats = []
        for dim in self.dim_list:
            fmats.append(self._make_init_factor_matrix(dim, rank))

        fmats = np.array(fmats)
        return fmats

    def _calc_V_n(self, fmats, n):
        # need to guarantee N >= n.
        # n is python index. need to write __doc__ or raise error.
        iter_list = np.delete(np.arange(self.N), n)

        # I need to change in case of fmats is one dim.
        init = iter_list[0]
        V = np.dot(fmats[init].T, fmats[init])
        for i in iter_list[1:]:
            V *= np.dot(fmats[i].T, fmats[i])
        return V

    def _update_factor_matrix(self, X, fmats, n):
        slice_index = np.tile(True, len(fmats))
        slice_index[n] = False
        fmats_subset = fmats[slice_index]

        # start from N to 1 except for n.
        term1 = fmats_subset[-1]
        for A_n in fmats_subset[::-1][1:]:
            term1 = to.Khatri_Rao_prod(term1, A_n)

        X_n = to.mode_n_matricization(X, n, self.dim_list)
        V_n = self._calc_V_n(fmats, n)
        term2 = np.dot(X_n, term1)
        A_n_new = np.dot(term2, pinv(V_n))

        return A_n_new

    def _update_factor_matrices(self, X):
        for n in np.arange(self.N):
            self.fmats[n] = self._update_factor_matrix(X, self.fmats, n)

    def objective_func(self, X, X_hat):
        obj_val = norm((X - X_hat).reshape(X_hat.size,1), ord=2)
        # numpy.linalg.norm() is only 1D or 2D.
        return obj_val

    def _calc_X_hat(self):
        X_hat = self._calc_rank1_X_hat(self.fmats, r=0)
        for r in np.arange(1, self.rank):
            X_hat += self._calc_rank1_X_hat(self.fmats, r=r)
        return X_hat

    def _calc_rank1_X_hat(self, fmats, r):
        # modify to use lambda
        X_hat_r1 = fmats[0][:, r]
        for n in np.arange(1, self.N):
            factor = fmats[n][:, r]
            X_hat_r1 = np.tensordot(X_hat_r1, factor, axes=0)
            del factor

        return X_hat_r1

if __name__ == '__main__':
    dim_list = np.array([3,2,4])
    X = dl.make_toy_tensor3(dim_list)
    rank = 10
    model = CPALS(dim_list, rank)
    model = model.fit(X, iter_num=100)
    print(model.logger.df)


