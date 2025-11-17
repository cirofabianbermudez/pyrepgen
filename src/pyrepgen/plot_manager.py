import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

def create_commit_plot(all_dates: list, all_counts: list) -> None:
    """
    Creates and shows a plot of commits over time.

    Args:
        all_dates (list): List of dates.
        all_counts (list): List of commit counts corresponding to the dates.
    """
    # Plot
    fig, ax = plt.subplots(figsize=(12, 6))


    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "GitLab Sans"]

    ax.plot(all_dates, all_counts,
        color="#7282ee", 
        linewidth=2,
        marker="o",
        markersize=6,
        label="Commits"
    )
    ax.fill_between(all_dates, all_counts, 0, alpha=0.3, color="#7282ee")
    ax.set_ylabel("Commits", fontsize=16, fontweight="bold")
    ax.set_xlabel("Month", fontsize=16, fontweight="bold")

    ax.tick_params(axis="x", colors="#626168", labelsize=12)
    ax.tick_params(axis="y", colors="#626168", labelsize=12)


    # ax.xaxis.set_major_locator(mdates.MonthLocator())      # tick each month
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))


    # Set y-axis limits
    ax.set_ylim(0, max(all_counts) + 1)

    # Set x-axis limits
    # Automatic
    # ax.set_xlim(all_dates[0], all_dates[-1])
    # Manual
    start = datetime(2024, 9, 15)
    end   = datetime(2024, 10, 17)

    # print(all_dates)
    ax.set_xlim(start, end)

    # Rotate x labels
    # for label in ax.get_xticklabels():
    #     label.set_rotation(90)

    # Grid
    ax.grid(True, axis="y", linestyle="-", alpha=0.5)


    initial_date = all_dates[65]
    initial_count = all_counts[65]

    # Text
    ax.text(
        initial_date, 
        initial_count,
        "Nov 4, 2025\n Commits 4",
        fontsize=18,
        color="#333333",
        ha="left",
        va="bottom",
    )

    ax.legend()
    fig.tight_layout()
    plt.show()