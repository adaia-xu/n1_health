import os
import matplotlib.pyplot as plt

def plot_confidence_growth(growth,out_path = "data/processed/confidence_growth.png"):
    #making sure the output folder exists before saving
    os.makedirs(os.path.dirname(out_path), exist_ok = True)

    #making a figure (the entire image) and the axes together
    fig, ax = plt.subplots(figsize=(9,5))

    #plotting the 'running' mean as a line over time
    ax.plot(growth["day"], growth["running_mean"], label = "Running mean")

    #shading area between (mean  -1.96*SE) and (mean +1.96*SE)
    #1.96 --> 95% confidence interval
    ax.fill_between(
            growth["day"],
            growth["running_mean"]-1.96*growth["running_se"],
            growth["running_mean"]+1.96*growth["running_se"],
            alpha = 0.25, #we want transparency so drawings are hidden behind the line
            label = "95% confidence band",
        )

    ax.set_title("My average daily steps: the confidence grows with more data")
    ax.set_xlabel("Date")
    ax.set_ylabel("Steps per day")
    ax.legend()
    fig.autofmt_xdate() #the date labels are angled, so no overlap
    fig.tight_layout()
    fig.savefig(out_path, dpi = 150) #making the chart to disk as a png
    plt.close(fig) #free memory