# %% task
# numpy is **not** pre-imported in this exercise: that's your job.
# %% wrong
import numpy
# %% wrong
import math as np
# %% case: `np` is defined
assert "np" in dir(), "`np` is not defined. Write `import numpy as np`."
# %% case: `np` is the numpy module
import numpy as _numpy
assert np is _numpy, "`np` is defined but it isn't numpy. Write `import numpy as np`."
