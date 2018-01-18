import numpy as np

def make_toy_tensor1(dim_list):
    """
    arguments
        dim_list : ndarray (N,)
        Ex. 
            dim_list = np.array([3,3,3,3,12,8,56,2])
    """
    X = np.random.randn(dim_list[0])
    for dim in dim_list[1:]:
        a = np.random.randn(dim)
        X = np.tensordot(X, a, axes=0)
    return X

def make_toy_tensor2():
    X = np.arange(1,25).reshape(3,4,2, order="F")
    return X

def make_toy_tensor3(dim_list):
    """
    dim_list : ndarray (N,)
    """
    X = np.random.randn(dim_list.prod()).reshape(dim_list)
    return X

if __name__ == '__main__':
    pass