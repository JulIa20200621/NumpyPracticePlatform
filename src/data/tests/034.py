# %% task
# Store the dates in `Z` (an array of `datetime64[D]`).
# %% wrong
Z = np.arange('2016-07-01', '2016-07-31', dtype='datetime64[D]')
# %% wrong
Z = np.arange('2016-07', '2016-08', dtype='datetime64[M]')
# %% case: `Z` holds dates (datetime64[D])
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.dtype == np.dtype('datetime64[D]'), f"Z should have dtype datetime64[D] (days), got {Z.dtype}. Pass `dtype='datetime64[D]'`."
# %% case: `Z` has all 31 days of July 2016
assert len(Z) == 31, f"July has 31 days, but Z has {len(Z)}." + (" The stop of `np.arange` is excluded: stop at '2016-08' (or '2016-08-01')." if len(Z) == 30 else "")
assert Z[0] == np.datetime64('2016-07-01') and Z[-1] == np.datetime64('2016-07-31'), f"Z should go from 2016-07-01 to 2016-07-31, got {Z[0]} to {Z[-1]}."
