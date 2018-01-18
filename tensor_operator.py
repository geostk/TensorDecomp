import numpy as np

def Khatri_Rao_prod(A, B):
    if A.shape[1] != B.shape[1]:
        raise ValueError("The colmuns dim of A and B should be the same.")

    K = A.shape[1]
    output = []
    for i in np.arange(K):
        vec1,vec2 = A[:,i], B[:,i]
        vec1 = vec1.reshape(len(vec1), 1)
        vec2 = vec2.reshape(len(vec2), 1)
        output.append(np.kron(vec1, vec2).flatten())

    output = np.array(output).T
    return output

def mode_n_matricization(X, n, dim_list):
    """
    arguments
        X : ndarray
            In [229]: X.shape
            Out[229]: (3, 4, 2)
        n : int
        dim_list : list of int
            In [231]: dim_list
            Out[231]: [3, 4, 2]

    returns
        output : ndarray
        If dim_list = [3,4,2], n=2, then output is (2, 3*4) matrix.
    """
    I_n = dim_list[n]
    output = []
    for i in np.arange(I_n):
        output.append(np.take(X, indices=i, axis=n).T.flatten())

    output = np.array(output)
    return output

if __name__ == '__main__':
    pass