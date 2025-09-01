import pandas as pd
import numpy as np
from datetime import datetime

translate_variable = {"horizontal(m)": "horizontal positioning errors [$m$]", "height(m)": "vertical positioning errors [$m$]", "Dst": "$Dst$-indices [$nT$]"}

translate =  {"sin": "Sine", "normal": "White noise", "ar": "Auto-regressive", "brownian": "Brownian motion", "logistic": "Logistic map"}
translate =  {"sin": "Sine", "normal": "Normal", "ar": "AR", "brownian": "Brownian", "logistic": "Logistic"}
number_ranges = 2
metric_dict_example = dict()
names_list =  ["sin", "normal", "ar", "brownian", "logistic"]
total_dict = dict()
for name in names_list:
    total_dict[name] = dict()
    metric_values_example = pd.read_csv("examples/" + name + "/metrics_" + name + ".csv", index_col = False)
    metric_dict_example[name] = {"RR": 0, "DET": 0, "NRLINE": 0, "L": 0, "L_entr": 0, "L_rentr": 0, "LAM": 0, "TT": 0}
    metric_dict_example[name] = {"RR": 0, "DET": 0, "L_rentr": 0, "LAM": 0}
    for ix in range(len(metric_values_example["metric"])):
        metric, value = metric_values_example["metric"][ix], metric_values_example["value"][ix]
        for metr in metric_dict_example[name]:
            if "(" in metric and metric[:-1].split("(")[1] == metr:
                metric_dict_example[name][metr] = value
    for used_col in translate_variable:
        metric_dict = dict()
        multiply_dict = {"RR": 0, "DET": 0, "NRLINE": 0, "L": 0, "L_entr": 0, "L_rentr": 4, "LAM": 0, "TT": 0}
        multiply_dict = {"RR": 0, "DET": 0, "L_rentr": 4, "LAM": 0}
        rounding_dict = {"RR": 3, "DET": 4, "NRLINE": 0, "L": 3, "L_entr": 3, "L_rentr": 4, "LAM": 4, "TT": 3}
        rounding_dict = {"RR": 3, "DET": 4, "L_rentr": 4, "LAM": 4}
        translate_metr = {"RR": "RR", "DET": "DET", "NRLINE": "NRLINE", "L": "L", "L_entr": "ENTR", "L_rentr": "rENTR", "LAM": "LAM", "TT": "TT"}
        translate_metr = {"RR": "RR", "DET": "DET", "L_rentr": "rENTR", "LAM": "LAM"}
        for month_use in range(1, 13):
            metric_values = pd.read_csv("month_result_" + str(used_col) + "/" + str(month_use) + "/metrics_" + str(month_use) + ".csv", index_col = False)
            metric_dict[month_use] = {"RR": 0, "DET": 0, "NRLINE": 0, "L": 0, "L_entr": 0, "L_rentr": 0, "LAM": 0, "TT": 0}
            metric_dict[month_use] = {"RR": 0, "DET": 0, "L_rentr": 0, "LAM": 0}
            for ix in range(len(metric_values["metric"])):
                metric, value = metric_values["metric"][ix], metric_values["value"][ix]
                for metr in metric_dict[month_use]:
                    if "(" in metric and metric[:-1].split("(")[1] == metr:
                        value_new = abs(value - metric_dict_example[name][metr])
                        metric_dict[month_use][metr] = value_new
        for month_range in [range(1, 13)]:
            range_size = int(len(month_range) // number_ranges)
            start_month = datetime(year = 2014, day = 1, month = min(month_range)).strftime("%B")
            end_month = datetime(year = 2014, day = 1, month = max(month_range)).strftime("%B")
            start_table = "\\begin{table}[H]\n"
            start_table += "\\caption{RPA results for the " + translate_variable[used_col] + " in $2024$, separated by month, and compared to the " + translate[name] + " function. The lowest value for each variable is underlined and bold, and the highest value is bold."
            start_table += "\\label{tab:" + name + "_" + used_col + "_" + str(min(month_range)) + "-" + str(max(month_range)) + "}}\n"
            start_table += "\\begin{tabularx}{\\textwidth}{" + "C" * (1 + range_size) + "}\n"
            min_for_metric = {metr: 10 ** 20 for metr in rounding_dict}
            max_for_metric = {metr: -10 ** 20 for metr in rounding_dict}
            for metr in rounding_dict:
                for month_use in month_range:
                    if metric_dict[month_use][metr] < min_for_metric[metr]:
                        min_for_metric[metr] = metric_dict[month_use][metr]
                    if metric_dict[month_use][metr] > max_for_metric[metr]:
                        max_for_metric[metr] = metric_dict[month_use][metr]
            for range_number in range(number_ranges):
                start_table += "\\toprule\n"
                start_table += "\\textbf{Month} & " + (" & ").join(["$\\textbf{" + str(month_use) + "}$" for month_use in month_range[range_size * range_number:range_size * (range_number + 1)]])
                start_table += " \\\\\n\\midrule\n"
                for metr in rounding_dict:
                    addition = (" ($\\times 10^{-" + str(multiply_dict[metr]) + "}$)") * (multiply_dict[metr] > 0)
                    metr_list = ["$" + translate_metr[metr] + "$" + addition]
                    for month_use in month_range[range_size * range_number:range_size * (range_number + 1)]:
                        is_min = False
                        is_max = False
                        if rounding_dict[metr]:
                            rounded_val = np.round(metric_dict[month_use][metr] * (10 ** multiply_dict[metr]), rounding_dict[metr])
                            rounded_min = np.round(min_for_metric[metr] * (10 ** multiply_dict[metr]), rounding_dict[metr])
                            rounded_max = np.round(min_for_metric[metr] * (10 ** multiply_dict[metr]), rounding_dict[metr])
                        else:
                            rounded_val = int(metric_dict[month_use][metr] * (10 ** multiply_dict[metr]))
                            rounded_min = int(min_for_metric[metr] * (10 ** multiply_dict[metr]))
                            rounded_max = int(max_for_metric[metr] * (10 ** multiply_dict[metr]))
                        if rounded_val == rounded_min:
                            is_min = True
                        if rounded_val == rounded_max:
                            is_max = True
                        startval = "\\mathbf{" * is_max + "\\underline{\\mathbf{" * is_min
                        endval = "}" * is_max + "}}" * is_min
                        if rounding_dict[metr]:
                            metr_list.append("$" + startval + str(np.round(metric_dict[month_use][metr] * (10 ** multiply_dict[metr]), rounding_dict[metr])) + endval + "$")
                        else:
                            metr_list.append("$" + startval + str(int(metric_dict[month_use][metr] * (10 ** multiply_dict[metr]))) + endval + "$")
                    start_table += (" & ").join(metr_list).replace(".0$", "$").replace(".0}", "}") + " \\\\\n"
                start_table += "\\bottomrule\n"
            start_table += "\\end{tabularx}\n\\end{table}"
            #print(start_table)
            total_dict[name][used_col] = metric_dict

range_size_second = 6
for metr in ["RR"]:#[total_dict["sin"]["Dst"][1]]:
    for used_col in translate_variable:
        strpr1 = []
        strpr2 = []
        addition = (" ($\\times 10^{-" + str(multiply_dict[metr]) + "}$)") * (multiply_dict[metr] > 0)
        metr_list_start = "($|\Delta " + translate_metr[metr] + "|$)" + addition
        start_table_part = "\\begin{table}[H]\n"
        start_table_part += "\\caption{RPA results for the " + translate_variable[used_col] + " in $2024$, separated by month, and compared to the characteristic classes of recurrence plots by the absolute value of the difference in $" + translate_metr[metr] + "$ " + metr_list_start + ". "
        start_table_part += "The name and value are listed for the characteristic classes of recurrence plots with the lowest absolute value of the difference in $" + translate_metr[metr] + "$ for each month " + metr_list_start + "."
        start_table_part += "\\label{tab:compare_" + metr + "_" + used_col + "_" + str(min(month_range)) + "-" + str(max(month_range)) + "}}\n"
        start_table_part += "\\begin{tabularx}{\\textwidth}{" + "C" * (1 + range_size_second) + "}\n"
        for month_range in [range(1, 13)]:
            for month_use in month_range:
                    closest = (-1, 10 ** 20)
                    for name in names_list:
                        v = total_dict[name][used_col][month_use][metr] 
                        if v < closest[1]:
                            closest = (translate[name], v)
                    #print(used_col, month_use, metr, closest)
                    strpr1.append(closest[0])
                    vr = "($" + str(np.round(closest[1] * (10 ** multiply_dict[metr]), rounding_dict[metr])) + "$)"
                    strpr2.append(vr)
            for index_start in range(0, 12, range_size_second):   
                start_table_part_begin = "\\toprule\n"
                start_table_part_begin += "\\textbf{Month} & " + (" & ").join(["$\\textbf{" + str(month_use) + "}$" for month_use in month_range[index_start:index_start + range_size_second]])
                start_table_part_begin += " \\\\\n\\midrule\n"
                start_table_part += start_table_part_begin + "Class & " + (" & ").join(strpr1[index_start:index_start + range_size_second]) + " \\\\\n"
                start_table_part += metr_list_start + " & " + (" & ").join(strpr2[index_start:index_start + range_size_second]) + " \\\\\n\\bottomrule\n"
        start_table_part += "\\end{tabularx}\n\\end{table}"
        print(start_table_part)