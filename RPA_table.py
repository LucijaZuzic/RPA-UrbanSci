import pandas as pd
import numpy as np
from datetime import datetime

translate_variable = {"horizontal(deg)": "Horizonal error in ($\\textdegree$)", "Dst": "Dst"}

for used_col in translate_variable:
    metric_dict = dict()
    multiply_dict = {"RR": 0, "DET": 0, "NRLINE": 0, "L": 0, "L_entr": 0, "L_rentr": 4, "LAM": 0, "TT": 0}
    rounding_dict = {"RR": 3, "DET": 4, "NRLINE": 0, "L": 3, "L_entr": 3, "L_rentr": 4, "LAM": 4, "TT": 3}
    translate_metr = {"RR": "RR", "DET": "DET", "NRLINE": "NRLINE", "L": "L", "L_entr": "ENTR", "L_rentr": "rENTR", "LAM": "LAM", "TT": "TT"}
    for month_use in range(1, 13):
        metric_values = pd.read_csv("month_result_" + str(used_col) + "/" + str(month_use) + "/metrics_" + str(month_use) + ".csv", index_col = False)
        metric_dict[month_use] = {"RR": 0, "DET": 0, "NRLINE": 0, "L": 0, "L_entr": 0, "L_rentr": 0, "LAM": 0, "TT": 0}
        for ix in range(len(metric_values["metric"])):
            metric, value = metric_values["metric"][ix], metric_values["value"][ix]
            for metr in metric_dict[month_use]:
                if "(" in metric and metric[:-1].split("(")[1] == metr:
                    metric_dict[month_use][metr] = value
    for month_range in [range(1, 7), range(7, 13)]:
        start_month = datetime(year = 2014, day = 1, month = min(month_range)).strftime("%B")
        end_month = datetime(year = 2014, day = 1, month = max(month_range)).strftime("%B")
        start_table = "\\begin{table}[H]\n"
        start_table += "\\caption{RPA results for the " + translate_variable[used_col] + " in months from "
        start_table += start_month + " to " + end_month + ". The lowest value in each row is underlined and bold, and the highest value in each row is bold."
        start_table += "\\label{tab:" + str(min(month_range)) + "-" + str(max(month_range)) + "}}\n"
        start_table += "\\begin{tabularx}{\\textwidth}{" + "C" * (1 + len(month_range)) + "}\n\\toprule\n"
        start_table += "\\textbf{Month} & " + (" & ").join(["$\\textbf{" + str(month_use) + "}$" for month_use in month_range])
        start_table += " \\\\\n\\midrule\n"
        min_for_metric = {metr: 10 ** 20 for metr in rounding_dict}
        max_for_metric = {metr: -10 ** 20 for metr in rounding_dict}
        for metr in rounding_dict:
            for month_use in month_range:
                if metric_dict[month_use][metr] < min_for_metric[metr]:
                    min_for_metric[metr] = metric_dict[month_use][metr]
                if metric_dict[month_use][metr] > max_for_metric[metr]:
                    max_for_metric[metr] = metric_dict[month_use][metr]
        for metr in rounding_dict:
            addition = (" ($\\times 10^{-" + str(multiply_dict[metr]) + "}$)") * (multiply_dict[metr] > 0)
            metr_list = [translate_metr[metr] + addition]
            for month_use in month_range:
                is_min = False
                is_max = False
                if metric_dict[month_use][metr] == min_for_metric[metr]:
                    is_min = True
                if metric_dict[month_use][metr] == max_for_metric[metr]:
                    is_max = True
                startval = "\\mathbf{" * is_max + "\\underline{\\mathbf{" * is_min
                endval = "}" * is_max + "}}" * is_min
                if rounding_dict[metr]:
                    metr_list.append("$" + startval + str(np.round(metric_dict[month_use][metr] * (10 ** multiply_dict[metr]), rounding_dict[metr])) + endval + "$")
                else:
                    metr_list.append("$" + startval + str(int(metric_dict[month_use][metr] * (10 ** multiply_dict[metr]))) + endval + "$")
            start_table += (" & ").join(metr_list) + " \\\\\n"
        start_table += "\\bottomrule\n\\end{tabularx}\n\\end{table}"
        print(start_table)