import pywt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

csv_test = pd.read_excel("AFIB1.xls")
print(csv_test)


cwtmatr, freqs=pywt.cwt(csv_test,np.arange(1,360),'morl')
plt.imshow(cwtmatr, extent=[-1, 1, 1, 31], cmap='PRGn', aspect='auto',
            vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
plt.show()
