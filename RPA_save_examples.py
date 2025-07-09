from pyrqa.time_series import TimeSeries
from pyrqa.settings import Settings
from pyrqa.analysis_type import Classic
from pyrqa.neighbourhood import FixedRadius
from pyrqa.metric import EuclideanMetric
from pyrqa.computation import RQAComputation
import os
import pandas as pd
from pyrqa.computation import RPComputation
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

translate =  {"sin": "Sine", "normal": "White noise", "ar": "Auto-regressive", "brownian": "Brownian motion", "logistic": "Logistic map"}

for name in ["sin", "normal", "ar", "brownian", "logistic"]:
    pdfile = pd.read_csv(name + "_time_series.csv")
    data_points = list(pdfile[name])

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
    
    if not os.path.isdir("examples/" + name):
        os.makedirs("examples/" + name)

    new_dict = {"metric": list(res_csv.keys()), "value": list(res_csv.values())}
    new_df = pd.DataFrame(new_dict)
    new_df.to_csv("examples/" + name + "/metrics_" + name + ".csv", index = False)
    
    for k in res_csv:
        print(k, res_csv[k])

    computation = RPComputation.create(settings)
    result_RQA = computation.run()

    matr_dict = result_RQA.recurrence_matrix_reverse.astype("bool")
    matr_dict = 1 - matr_dict
    step_size = 3
    matr_dict = matr_dict[::step_size, ::step_size]
    
    ks = [i for i in range(len(data_points))]
    plt.figure(figsize = (11, 5))
    plt.subplot(1, 2, 1)
    plt.plot(ks, data_points, color = "#FF0000")
    plt.ylabel("Value")
    plt.xlabel("Time")
    plt.title("Time series - " + translate[name])

    plt.subplot(1, 2, 2)
    plt.title("Recurrence plot - " + translate[name])

    cmap1 = LinearSegmentedColormap.from_list("mycmap", ["#FF0000", "#FFFFFF"])
    plt.imshow(matr_dict, cmap = cmap1)
    plt.axis("equal")
    plt.xticks([])
    plt.yticks([])
    ax = plt.gca()
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.spines['bottom'].set_visible(True)
    ax.spines['left'].set_visible(True)
    plt.savefig("examples/" + name + "/examples_" + name + ".png", bbox_inches = "tight")
    plt.close()