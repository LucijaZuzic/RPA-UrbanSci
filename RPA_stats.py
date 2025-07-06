import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime
import os

xs, ys = [], []
for month_use in range(1, 13):
    data_points = pd.read_csv("month_result/" + str(month_use) + "/data_points_" + str(month_use) + ".csv", index_col = False)
    ks = list(data_points["x"])
    vs = list(data_points["y"])
    xs.extend(ks)
    ys.extend(vs)

titles = ["Hr", "{Q}_{1}", "Median", "Mean", "{Q}_{3}", "Max.", "SD"]
start_table = "\\begin{table}[H]\n"
start_table += "\\caption{The $1^{st}$ quartile (${Q}_{1}$), median ($2^{nd}$ quartile), mean, $3^{rd}$ quartile (${Q}_{3}$), maximum ($Max.$)"
start_table += ", and standard deviation ($SD$) for the hourly median horizontal errors in \\textdegree."
start_table += "The lowest value in each column is underlined and bold, and the highest value in each column is bold.\\label{tab:stats}}\n"
start_table += "\\begin{tabularx}{\\textwidth}{" + "C" * (len(titles) + 1) + "}\n\\toprule\n"
join_titles = (" &").join(["$\\mathbf{" + t + "}$" for t in titles])
start_table += join_titles + " \\\\\n\\midrule\n"
min_for_metric = {ix: 100 for ix in range(len(titles))}
max_for_metric = {ix: -100 for ix in range(len(titles))}
for h in range(24):
    fx = [ys[ix] for ix in range(h, len(ys), 24)]
    vals = [np.quantile(fx, 0.25), np.median(fx), np.mean(fx), np.quantile(fx, 0.75), max(fx), np.std(fx)]
    for ix in range(len(vals)):
        if vals[ix] < min_for_metric[ix]:
            min_for_metric[ix] = vals[ix]
        if vals[ix] > max_for_metric[ix]:
            max_for_metric[ix] = vals[ix]
for h in range(24):
    fx = [ys[ix] for ix in range(h, len(ys), 24)]
    vals = [np.quantile(fx, 0.25), np.median(fx), np.mean(fx), np.quantile(fx, 0.75), max(fx), np.std(fx)]
    vals_join = []
    for ix in range(len(vals)):
        is_min = False
        is_max = False
        if vals[ix] == min_for_metric[ix]:
            is_min = True
        if vals[ix] == max_for_metric[ix]:
            is_max = True
        startval = "\\mathbf{" * is_max + "\\underline{\\mathbf{" * is_min
        endval = "}" * is_max + "}}" * is_min
        vals_join .append("$" + startval + str(np.round(vals[ix], 2)) + endval + "$")
    start_table += "$" + str(h) + "$ & " + (" & ").join(vals_join) + " \\\\\n"
start_table += "\\bottomrule\n\\end{tabularx}\n\\end{table}"
print(start_table.replace(".0$", "$").replace(".0}", "}"))