import pandas as pd
from datetime import datetime
import numpy as np

translate_variable = {"horizontal(m)": "Horizontal positioning errors [$m$]", "absolute height(m)": "Vertical positioning errors [$m$]", "TEC": "Total Electron Content [$TECU$]", "Dst": "$Dst$-indices [$nT$]"}

compare_var = dict()
mean_month = dict()
best_month = dict()
worst_month = dict()
for used_col in translate_variable:
    compare_var[used_col] = dict()
    mean_month[used_col] = dict()
    best_month[used_col] = 0
    worst_month[used_col] = 0
    num_col = 0
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
        compare_var[used_col][month_use] = vs
        mean_month[used_col][month_use] = np.mean(compare_var[used_col][month_use])
        if not best_month[used_col] or mean_month[used_col][month_use] > mean_month[used_col][best_month[used_col]]:
            best_month[used_col] = month_use
        if not worst_month[used_col] or mean_month[used_col][month_use] < mean_month[used_col][worst_month[used_col]]:
            worst_month[used_col] = month_use

start_table = "\\begin{table}[H]\n"
start_table += "\\caption{The arithmetic mean for horizontal and vertical positioning errors [$m$] and $TEC$ [$TECU$] and $Dst$-index [$nT$] values for each month. The lowest value for each variable is underlined and bold, and the highest value is bold."
start_table += "\\label{tab:mean}}\n"
start_table += "\\begin{tabularx}{\\textwidth}{" + "C" * 7 + "}\n"
for month_range in [range(1, 7), range(7, 13)]:
    start_table += "\\toprule\n"
    start_table += "\\textbf{Variable} & " + (" & ").join(["$\\textbf{" + str(month_use) + "}$" for month_use in month_range])
    start_table += " \\\\\n\\midrule\n"
    for used_col in translate_variable:
        metr_list = [translate_variable[used_col]]
        for month_use in month_range:
            rounded_val = np.round(mean_month[used_col][month_use], 2)
            rounded_min = np.round(mean_month[used_col][worst_month[used_col]], 2)
            rounded_max = np.round(mean_month[used_col][best_month[used_col]], 2)
            is_min, is_max = False, False
            if rounded_val == rounded_min:
                is_min = True
            if rounded_val == rounded_max:
                is_max = True
            startval = "\\mathbf{" * is_max + "\\underline{\\mathbf{" * is_min
            endval = "}" * is_max + "}}" * is_min
            metr_list.append("$" + startval + str(rounded_val) + endval + "$")

        start_table += (" & ").join(metr_list).replace(".0$", "$").replace(".0}", "}") + " \\\\\n"
start_table += "\\bottomrule\n"
start_table += "\\end{tabularx}\n\\end{table}"
print(start_table)