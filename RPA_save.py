from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.analysis_type import Classic
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation
import os
import pandas as pd
from datetime import datetime
import numpy as np
from pyrqa.computation import RPComputation

for month_use in range(1, 13):
    pdfile = pd.read_csv("darwin_pos_total.csv")
    pdfile = pdfile[pdfile["m"] == month_use]
    lstTime = list(pdfile["GPST"])
    pdfile["doy"] = [datetime.strptime(lstTime[ix], "%Y-%m-%d %H:%M:%S").timetuple().tm_yday for ix in range(len(lstTime))]
    minDay = min(pdfile["doy"])
    pdfile["doy hr"] = [(datetime.strptime(lstTime[ix], "%Y-%m-%d %H:%M:%S").timetuple().tm_yday - minDay) * 24 + datetime.strptime(lstTime[ix], "%Y-%m-%d %H:%M:%S").hour for ix in range(len(lstTime))]

    num_days = len(set(list(pdfile["doy"])))
    time_step = 24
    time_series = list(range(num_days * time_step))
    
    used_col = "horizontal(deg)"
    dicti_new = dict()
    last_val = 0
    for t1 in time_series:
        newdf = pdfile[pdfile["doy hr"] == t1]
        if len(newdf):
            dicti_new[t1] = np.median(list(newdf[used_col]))
            last_val = dicti_new[t1]
        else:
            dicti_new[t1] = last_val

    ks = list(dicti_new.keys())
    vs = list(dicti_new.values())
    
    if not os.path.isdir("month_result/" + str(month_use)):
        os.makedirs("month_result/" + str(month_use))
    new_dict_ks = {"x": ks, "y": vs}
    new_df_ks = pd.DataFrame(new_dict_ks)
    new_df_ks.to_csv("month_result/" + str(month_use) + "/data_points_" + str(month_use) + ".csv", index = False)

    data_points = vs

    time_series = TimeSeries(data_points, embedding_dimension = 1, time_delay = 1)
    settings = Settings(time_series, analysis_type = Classic, neighbourhood = FixedRadius(1), similarity_measure = EuclideanMetric, theiler_corrector = 0)
    computation = RQAComputation.create(settings, verbose = True)
    result = computation.run()
    result.min_diagonal_line_length = 2
    result.min_vertical_line_length = 2
    result.min_white_vertical_line_length = 2

    res_csv = {"Number of recurrence points": result.number_of_recurrence_points,
            "The total number of lines in the recurrent plot (NRLINE)": result.number_of_diagonal_lines(result.min_diagonal_line_length) + result.number_of_vertical_lines(result.min_vertical_line_length),
            "The average length of line structures (L)": (result.number_of_diagonal_lines_points(result.min_diagonal_line_length) + result.number_of_vertical_lines_points(result.min_vertical_line_length)) / (result.number_of_diagonal_lines(result.min_diagonal_line_length) + result.number_of_vertical_lines(result.min_vertical_line_length)),
            "Shannon entropy: Shannon information entropy of line lengths longer than the minimum length (ENTR)": result.entropy_diagonal_lines + result.entropy_vertical_lines,
            "Entropy measure normalized by the number of lines observed in the plot (rENTR)": (result.entropy_diagonal_lines + result.entropy_vertical_lines) / (result.number_of_diagonal_lines(result.min_diagonal_line_length) + result.number_of_vertical_lines(result.min_vertical_line_length)),
            "Recurrence rate (RR)": result.recurrence_rate,
            "Total number of diagonal lines having a minimum length": result.number_of_diagonal_lines(result.min_diagonal_line_length),
            "Total number of recurrence points that form diagonal lines having a minimum length": result.number_of_diagonal_lines_points(result.min_diagonal_line_length),
            "Determinism (DET)": result.determinism,
            "Average diagonal line length (L)": result.average_diagonal_line,
            "Longest diagonal line length (L_max)": result.longest_diagonal_line,
            "Entropy of diagonal lines (L_entr)": result.entropy_diagonal_lines,
            "Entropy of diagonal lines normalized by the number of diagonal lines observed in the plot (L_rentr)": result.entropy_diagonal_lines / result.number_of_diagonal_lines(result.min_diagonal_line_length),
            "Divergence (DIV)": result.divergence,
            "Average vertical line length (V)": result.number_of_vertical_lines_points(result.min_vertical_line_length) / result.number_of_vertical_lines(result.min_vertical_line_length),
            "Total number of vertical lines having a minimum length": result.number_of_vertical_lines(result.min_vertical_line_length),
            "Total number of recurrence points that form vertical lines having a minimum length": result.number_of_vertical_lines_points(result.min_vertical_line_length),
            "Laminarity (LAM)": result.laminarity,
            "Trapping time (TT)": result.trapping_time,
            "Longest vertical line length (V_max)": result.longest_vertical_line,
            "Entropy of vertical lines (V_entr)": result.entropy_vertical_lines,
            "Entropy of vertical lines normalized by the number of vertical lines observed in the plot (V_rentr)": result.entropy_vertical_lines / result.number_of_vertical_lines(result.min_vertical_line_length),
            "Total number of white vertical lines having a minimum length": result.number_of_white_vertical_lines(result.min_white_vertical_line_length),
            "Total number of white points that form white vertical lines having a minimum length": result.number_of_white_vertical_lines(result.min_white_vertical_line_length),
            "Average white vertical line length (W)": result.average_white_vertical_line,
            "Longest white vertical line length (W_max)": result.longest_white_vertical_line,
            "Entropy of white vertical lines (W_entr)": result.entropy_white_vertical_lines,
            "Entropy of white vertical lines normalized by the number of white vertical lines observed in the plot (W_rentr)": result.entropy_white_vertical_lines / result.number_of_white_vertical_lines(result.min_white_vertical_line_length),
            "Longest white vertical line length inverse (W_div)": result.longest_white_vertical_line_inverse,
            "Ratio determinism / recurrence rate (DET/RR)": result.ratio_determinism_recurrence_rate,
            "Ratio laminarity / determinism (LAM/DET)": result.ratio_laminarity_determinism}
    new_dict = {"metric": list(res_csv.keys()), "value": list(res_csv.values())}
    new_df = pd.DataFrame(new_dict)
    new_df.to_csv("month_result/" + str(month_use) + "/metrics_" + str(month_use) + ".csv", index = False)
    
    for k in res_csv:
        print(k, res_csv[k])

    computation = RPComputation.create(settings)
    result_RQA = computation.run()

    np.save("month_result/" + str(month_use) + "/matrix_" + str(month_use) + ".npy", result_RQA.recurrence_matrix_reverse)