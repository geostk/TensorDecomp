import pandas as pd
import numpy as np

class CPALSLogger(object):
    """
    Ex.
        cpalslogger = CPALSLogger(columns = ["step", "obj_val"])
        new_row = [1,2]
        cpalslogger.append(new_row)
        cpalslogger.df
               step  obj_val
            0   1.0      2.0
    """
    def __init__(self, columns=None):
        self.df = self.init_logdf(columns)

    def init_logdf(self, columns):
        if columns is None:
            # default columns
            self.columns = ["step", "obj_val"]

        self.columns = columns
        df = pd.DataFrame(columns=self.columns)
        return df

    def append(self, new_row):
        """
        arguments
            new_row : list like
                new_row vector whose shape is (n,) and n is len(columns).
        """
        new_row = np.array(new_row).reshape(1, len(self.columns))
        new_row_df = pd.DataFrame(new_row, columns=self.columns)
        self.df = pd.concat([self.df, new_row_df], ignore_index=True)


if __name__ == '__main__':
    pass