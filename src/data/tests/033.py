# %% task
# Store them as `np.datetime64` days in `yesterday`, `today` and `tomorrow`.
# %% wrong
today = np.datetime64('today')
yesterday = today - np.timedelta64(1, 'D')
tomorrow = today + np.timedelta64(2, 'D')
# %% wrong
import datetime
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)
# %% case: All three are np.datetime64
_bad = [n for n in ("yesterday", "today", "tomorrow") if not isinstance(eval(n), np.datetime64)]
assert not _bad, f"{', '.join(_bad)} should be np.datetime64 values. Start from `np.datetime64('today')`."
# %% case: `today` is today
_today = np.datetime64('today', 'D')
assert today == _today, f"today is {today}, expected {_today}."
# %% case: `yesterday` is one day before today
assert yesterday == _today - np.timedelta64(1, 'D'), f"yesterday is {yesterday}, expected {_today - np.timedelta64(1, 'D')}."
# %% case: `tomorrow` is one day after today
assert tomorrow == _today + np.timedelta64(1, 'D'), f"tomorrow is {tomorrow}, expected {_today + np.timedelta64(1, 'D')}."
