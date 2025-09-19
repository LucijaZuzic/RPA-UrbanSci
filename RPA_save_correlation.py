import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

translate_variable = {"horizontal(m)": "Horizontal positioning errors [$m$]", "absolute height(m)": "Vertical positioning errors [$m$]", "TEC": "Total Electron Content [$TECU$]", "Dst": "$Dst$-indices [$nT$]"}

nrows, ncols = 4, 3
plt.figure(figsize = (11, 15), dpi = 600)
for month_use in range(1, 13):
    plt.subplot(nrows, ncols, month_use)
    compare_var = dict()
    num_col = 0
    for used_col in translate_variable:
        pdfile = pd.read_csv("data_all_" + str(month_use) + ".csv")
        lstTime = list(pdfile["GPST"])
        pdfile["doy"] = [datetime.strptime(lstTime[ix], "%Y-%m-%d %H:%M:%S").timetuple().tm_yday for ix in range(len(lstTime))]
        minDay = min(pdfile["doy"])
        pdfile["doy min"] = [(datetime.strptime(lstTime[ix], "%Y-%m-%d %H:%M:%S").timetuple().tm_yday - minDay) * 24 * 60 + datetime.strptime(lstTime[ix], "%Y-%m-%d %H:%M:%S").hour * 60 + datetime.strptime(lstTime[ix], "%Y-%m-%d %H:%M:%S").minute for ix in range(len(lstTime))]

        num_days = len(set(list(pdfile["doy"])))
        time_step = 24 * 60
        time_series = list(range(num_days * time_step))

        dicti_new = dict()
        last_val = 0
        for t1 in time_series:
            newdf = pdfile[pdfile["doy min"] == t1]
            if len(list(newdf[used_col])) == 1:
                dicti_new[t1] = list(newdf[used_col])[0]
                last_val = dicti_new[t1]
            else:
                dicti_new[t1] = last_val

        ks = list(dicti_new.keys())
        vs = list(dicti_new.values())
        compare_var[used_col + "_" + str(month_use)] = vs

    corrmap = []
    for v1 in compare_var:
        corrmap.append([])
        for v2 in compare_var:
            corrmap[-1].append(np.corrcoef(compare_var[v1], compare_var[v2])[0][1])

    print(corrmap)

    cmap1 = LinearSegmentedColormap.from_list("mycmap", ["#FFFFFF", "#FF0000"])
    if month_use == int((ncols + ncols % 2) // 2) and month_use == 2:
        plt.title("Pearson's correlation coefficients\n" + datetime(year = 2014, day = 1, month = month_use).strftime("%B"))
    else:
        plt.title(datetime(year = 2014, day = 1, month = month_use).strftime("%B"))
    sns.heatmap(corrmap, cmap = cmap1, cbar = False, annot = True, fmt = ".4f")
used_col_keys = list(translate_variable.keys())
plt.legend(handles = [mpatches.Patch(color = (1, 1, 1, 0), label = str(used_col_ix) + " - " + translate_variable[used_col_keys[used_col_ix]]) for used_col_ix in range(len(used_col_keys))], ncols = 2, bbox_to_anchor = (0.5, -0.1))

plt.savefig("correlation_variables.eps", bbox_inches = "tight")
plt.savefig("correlation_variables.png", bbox_inches = "tight")
plt.savefig("correlation_variables.svg", bbox_inches = "tight")
plt.savefig("correlation_variables.pdf", bbox_inches = "tight")
plt.close()