import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os

padded_data = dict()
matr_dict = dict()
decdict = {"RR": 3, "DET": 2, "NRLINE": 0, "L": 3, "ENTR": 3, "rENTR": 4, "LAM": 2, "TT": 3}
for month_use in range(1, 13):
    data_points = pd.read_csv("month_result/" + str(month_use) + "/data_points_" + str(month_use) + ".csv", index_col = False)
    ks = list(data_points["x"])
    vs = list(data_points["y"])
    padded_data[month_use] = [ks, vs]
    matr = np.load("month_result/" + str(month_use) + "/matrix_" + str(month_use) + ".npy")
    matr_dict[month_use] = matr
        
    plt.figure(figsize = (11, 5))
    plt.subplot(1, 2, 1)
    plt.plot(padded_data[month_use][0], padded_data[month_use][1], color = "#FF0000")
    plt.ylabel("Median horizontal error ($\degree$) for each hour")
    plt.xlabel("Day of the month")
    ticks_x = [x for x in range(0, len(padded_data[month_use][0]), 24 * 2)]
    labels_x = [str(x // 24 + 1) for x in range(0, len(padded_data[month_use][0]), 24 * 2)]
    plt.xticks(ticks_x, labels_x)
    plt.title("Time series - " + datetime(year = 2014, day = 1, month = month_use).strftime("%B"))

    plt.subplot(1, 2, 2)
    plt.title("Recurrence plot - " + datetime(year = 2014, day = 1, month = month_use).strftime("%B"))

    ax = sns.heatmap(1 - matr_dict[month_use], cmap = ["#FF0000", "#FFFFFF"], cbar = False)
    plt.axis("equal")
    plt.xticks([])
    plt.yticks([])
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    if not os.path.isdir("months"):
        os.makedirs("months")
    plt.savefig("months/months_" + str(month_use) + ".eps", bbox_inches = "tight")
    plt.savefig("months/months_" + str(month_use) + ".pdf", bbox_inches = "tight")
    plt.savefig("months/months_" + str(month_use) + ".png", bbox_inches = "tight")
    plt.savefig("months/months_" + str(month_use) + ".svg", bbox_inches = "tight")
    plt.close()