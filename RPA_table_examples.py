import pandas as pd
import numpy as np

metric_dict = dict()
names_list =  ["sin", "normal", "ar", "brownian", "logistic"]
translate =  {"sin": "Sine", "normal": "Normal", "ar": "A-R", "brownian": "Brownian", "logistic": "Logistic"}
multiply_dict = {"RR": 0, "DET": 0, "NRLINE": 0, "L": 0, "L_entr": 0, "L_rentr": 4, "LAM": 0, "TT": 0}
rounding_dict = {"RR": 3, "DET": 4, "NRLINE": 0, "L": 3, "L_entr": 3, "L_rentr": 4, "LAM": 4, "TT": 3}
translate_metr = {"RR": "RR", "DET": "DET", "NRLINE": "NRLINE", "L": "L", "L_entr": "ENTR", "L_rentr": "rENTR", "LAM": "LAM", "TT": "TT"}
for name in names_list:
    metric_values = pd.read_csv("examples/" + name + "/metrics_" + name + ".csv", index_col = False)
    metric_dict[name] = {"RR": 0, "DET": 0, "NRLINE": 0, "L": 0, "L_entr": 0, "L_rentr": 0, "LAM": 0, "TT": 0}
    for ix in range(len(metric_values["metric"])):
        metric, value = metric_values["metric"][ix], metric_values["value"][ix]
        for metr in metric_dict[name]:
            if "(" in metric and metric[:-1].split("(")[1] == metr:
                metric_dict[name][metr] = value
                
start_table = "\\begin{table}[H]\n"
start_table += "\\caption{RPA predictors for characteristic classes of recurrence plots.\\label{tab:examples}}\n"
start_table += "\\begin{tabularx}{\\textwidth}{" + "C" * (1 + len(names_list)) + "}\n\\toprule\n"
start_table += "\\textbf{Function} & " + (" & ").join(["$\\textbf{" + str(translate[name]) + "}$" for name in names_list])
start_table += " \\\\\n\\midrule\n"
for metr in rounding_dict:
    addition = (" ($\\times 10^{-" + str(multiply_dict[metr]) + "}$)") * (multiply_dict[metr] > 0)
    metr_list = [translate_metr[metr] + addition]
    for name in names_list:
        if rounding_dict[metr]:
            metr_list.append("$" + str(np.round(metric_dict[name][metr] * (10 ** multiply_dict[metr]), rounding_dict[metr])) + "$")
        else:
            metr_list.append("$" + str(int(metric_dict[name][metr] * (10 ** multiply_dict[metr]))) + "$")
    start_table += (" & ").join(metr_list) + " \\\\\n"
start_table += "\\bottomrule\n\\end{tabularx}\n\\end{table}"
print(start_table.replace(".0$", "$"))