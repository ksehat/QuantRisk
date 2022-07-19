from scipy.io import loadmat
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import sys

data_address = sys.argv[1]
try:
    dest_address = sys.argv[2]
except:
    dest_address = None
if dest_address is None:
    dest_address = "./data.csv"

def datenum_to_datetime(datenum):
    """
    Convert Matlab datenum into Python datetime.

    Args:
        datenum (datenum): Date in datenum format

    Returns:
        datetime : object corresponding to datenum
    """
    days = datenum % 1
    hours = days % 1 * 24
    minutes = hours % 1 * 60
    seconds = minutes % 1 * 60
    return datetime.fromordinal(int(datenum)) + timedelta(days=int(days)) \
                        + timedelta(hours=int(hours)) \
                        + timedelta(minutes=int(minutes)) \
                        + timedelta(seconds=round(seconds)) \
                        - timedelta(days=366)

dmat = loadmat(data_address)

def forward_curve_generator(dmat):
    dates = (dmat["ForwardCurve"][0][0])[0]
    vals = (dmat["ForwardCurve"][0][0])[3]
    return pd.Series(data = [float(vals[i][0]) for i in range(vals.shape[0])], index = [datenum_to_datetime(dates[i][0]) for i in range(dates.shape[0])])

# target = server_mat_data['targetMatrix']

original_df = pd.DataFrame(data=dmat['predictorMatrix'], index=[datenum_to_datetime(d) for d in dmat['dates'].squeeze()], columns=np.concatenate(dmat['labels'][0]))

original_df["target"] = dmat["targetMatrix"]

forward_curve = (dmat["ForwardCurve"][0][0])[3]
original_df["Forward Curve"] = forward_curve_generator(dmat)

original_df.to_csv(dest_address)