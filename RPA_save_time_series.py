from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.analysis_type import Classic
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation
import os
import pandas as pd
from datetime import datetime
from pyrqa.computation import RPComputation
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

translate_variable = {"horizontal(m)": "Horizontal positioning errors [$m$]", "Dst": "$Dst$-indices [$nT$]"}

nrows, ncols = 4, 3
for used_col in translate_variable:
    plt.figure(figsize = (11, 15))
    for month_use in range(1, 13):
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

        plt.subplot(nrows, ncols, month_use)
        plt.plot(ks, vs, color = "#FF0000")
        if month_use % ncols == 1:
            plt.ylabel(translate_variable[used_col])
        if month_use >= 13 - ncols:
            plt.xlabel("Day of the month")
        ticks_x = [x for x in range(0, len(ks), 24 * 60 * 4)]
        labels_x = [str(x // 24 // 60 + 1) for x in range(0, len(ks), 24 * 60 * 4)]
        plt.xticks(ticks_x, labels_x)
        if month_use == int((ncols + ncols % 2) // 2):
            plt.title(translate_variable[used_col] + "\nTime series - " + datetime(year = 2014, day = 1, month = month_use).strftime("%B"))
        else:
            plt.title("Time series - " + datetime(year = 2014, day = 1, month = month_use).strftime("%B"))
    plt.savefig("month_result_all_time_series_" + used_col + "_time_series.png", bbox_inches = "tight")
    plt.close()