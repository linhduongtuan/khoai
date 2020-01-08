# coding=utf-8

"""Data Frame Tools."""
import numpy as np


def reduce_mem_usage(df, verbose=True):
    """ A function reduce memory of DataFrame.
    Parameters:
                df: DataFrame
                    A table of data.
                veborse: bool
                    Show mem. usage decreased.
    Output:
                DataFrame
    """

    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage().sum() / 1024**2
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and \
                        c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and \
                        c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and \
                        c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and \
                        c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                c_prec = df[col].apply(lambda x: np.finfo(x).precision).max()
                if c_min > np.finfo(np.float16).min and \
                        c_max < np.finfo(np.float16).max and \
                        c_prec == np.finfo(np.float16).precision:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and \
                        c_max < np.finfo(np.float32).max and \
                        c_prec == np.finfo(np.float32).precision:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)

    end_mem = df.memory_usage().sum() / 1024**2
    if verbose:
        res = 100 * (start_mem - end_mem) / start_mem
        print("""Mem. usage decreased
                 to {:5.2f} Mb ({:.1f}% reduction)""".format(end_mem,
                                                             res))

    return df


def calibrate(data, train_pop, target_pop, sampled_train_pop, sampled_target_pop):
    """ Calibrate data after undersample data.
    Parameters:
                data: float array
                    probability prediction Array.
                train_pop: int
                    Number of data in training data.
                target_pop: int
                    Number of target class (minority class) in the training dataset.
                sampled_train_pop: int
                    Number of data in training dataset after undersampling.
                sampled_target_pop: int
                    Number of the target class(minority class) in the training dataset after undersampling.
    Return:     
                data: float array
                    probability prediction Array after calibrate.
    """
    A = data * (target_pop / train_pop) / (sampled_target_pop / sampled_train_pop)
    B = (1 - data) * (1 - target_pop / train_pop) / (1 - sampled_target_pop / sampled_train_pop)
    calibrated_data = A / (A+B)
    return calibrated_data
