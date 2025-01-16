"""
An example script which connects to the PeakNDT Micropulse and acquires a
single FMC data set.
"""

import matplotlib.pyplot as plt
import numpy as np
from pybrain.instruments.peakndt import Micropulse


with Micropulse(
    ip_address = '10.1.1.2',
    port = 1067,
    acquisition = 'FMC',
) as mp:
    exp_data = mp.acquire()
    
    
fig, ax = plt.subplots(figsize=(8, 4))
ax.imshow(
    np.abs(exp_data.time_data[exp_data.tx == exp_data.rx]),
    extent=[
        exp_data.time[0],
        exp_data.time[-1],
        min(exp_data.tx),
        max(exp_data.tx),
    ],
)
ax.set_xlabel('Time (us)')
ax.set_ylabel('Array Element No.')
ax.set_title('FMC Response')
fig.colorbar(label='|z| (arb)')
plt.show()