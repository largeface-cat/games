import numpy as np
import time
scale = 10
while 1:
    wait_t = (np.random.random() + 0.5) * scale
    time.sleep(wait_t)
    start = time.time_ns()
    input('Press Enter!')
    end = time.time_ns()
    print((end-start) / 1e6)