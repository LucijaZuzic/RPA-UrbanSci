import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

padded_data = dict()
matr_dict = dict()
decdict = {"RR": 3, "DET": 2, "NRLINE": 0, "L": 3, "ENTR": 3, "rENTR": 4, "LAM": 2, "TT": 3}
translate =  {"sin": "Sine", "normal": "White noise", "ar": "Auto-regressive", "brownian": "Brownian motion", "logistic": "Logistic map"}
for name in ["sin", "normal", "ar", "brownian", "logistic"]:
    pdfile = pd.read_csv(name + "_time_series.csv")
    vs = list(pdfile[name])
    ks = [i for i in range(len(vs))]
    padded_data[name] = [ks, vs]
    matr = np.load("examples/" + name + "/matrix_" + name + ".npy")
    matr_dict[name] = matr
        
    plt.figure(figsize = (11, 5))
    plt.subplot(1, 2, 1)
    plt.plot(padded_data[name][0], padded_data[name][1], color = "#FF0000")
    plt.ylabel("Value")
    plt.xlabel("Time")
    plt.title("Time series - " + translate[name])

    plt.subplot(1, 2, 2)
    plt.title("Recurrence plot - " + translate[name])

    ax = sns.heatmap(1 - matr_dict[name], cmap = ["#FF0000", "#FFFFFF"], cbar = False)
    plt.axis("equal")
    plt.xticks([])
    plt.yticks([])
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    if not os.path.isdir("example_figures"):
        os.makedirs("example_figures")
    plt.savefig("example_figures/examples_" + name + ".eps", bbox_inches = "tight")
    plt.savefig("example_figures/examples_" + name + ".pdf", bbox_inches = "tight")
    plt.savefig("example_figures/examples_" + name + ".png", bbox_inches = "tight")
    plt.savefig("example_figures/examples_" + name + ".svg", bbox_inches = "tight")
    plt.close()