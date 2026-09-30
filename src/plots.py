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

import numpy as np

def plot_completeness_heatmap(report, out_path = "data/processed/completeness_heatmap.png"):
    os.makedirs(os.path.dirname(out_path), exist_ok = True)

    days = report["day"].values
    has_data = report["has_data"].astype(int).values 

    #reshape into a grid: one row per week and one column per weekday
    n_weeks = int(np.ceil(len(has_data)/7)) #np.ceil to round numbers up to nearest integer
    padded = np.full(n_weeks*7, np.nan) #array to store data
    padded[:len(has_data)] = has_data
    grid = padded.reshape(n_weeks,7) #turns a flat list into a grid

    fig, ax = plt.subplots(figsize =(10, n_weeks*0.25))
    ax.imshow(grid, cmap = "Greens", aspect = "auto", vmin = 0, vmax = 1) #draws a grid with colored cells, and uses 0/1 values to pick intensity
    ax.set_title("Data completeness (green = day contains data)")
    ax.set_xlabel("Day of week (Sun-Sat, approx.)")
    ax.set_ylabel("Week number")
    fig.tight_layout()
    fig.savefig(out_path, dpi = 150)
    plt.close(fig)