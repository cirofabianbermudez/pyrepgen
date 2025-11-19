import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import logging

def create_commit_plot(all_dates: list, all_counts: list, 
                       email: str, author: str, 
                       x_lim_start: str, x_lim_end: str,
                       y_lim_top: str, y_lim_bottom: str,
                       marker_left: str, marker_right: str) -> None:
    """
    Creates and shows a plot of commits over time.

    Args:
        all_dates (list): List of dates.
        all_counts (list): List of commit counts corresponding to the dates.
    """
    # Create figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    # Set font settings
    plt.rcParams["font.family"] = "sans-serif"
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "GitLab Sans"]

    # Plot data
    ax.plot(all_dates, all_counts,
        color="#7282ee", 
        linewidth=3,
        marker="o",
        markersize=8,
        label="Commits"
    )

    # Grid
    ax.grid(True, axis="y", linestyle="-", alpha=0.5, linewidth=2)

    # Axis labels
    ax.fill_between(all_dates, all_counts, 0, alpha=0.3, color="#7282ee")
    ax.set_ylabel("Commits", fontsize=20, fontweight="bold", labelpad=15)
    # ax.set_xlabel("Month", fontsize=16, fontweight="bold")
    
    # Axis ticks configuration
    ax.tick_params(axis="x", colors="#626168", labelsize=20)
    ax.tick_params(axis="y", colors="#626168", labelsize=20)

    # ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))

    # Set axis limits
    if y_lim_top is None:
        y_lim_top = max(all_counts) + 1

    ax.set_ylim(0, y_lim_top)

    # start = datetime(2024, 9, 15).date()
    # end   = datetime(2024, 10, 18).date()
    if x_lim_start is None or x_lim_end is None:
        # Automatic
        x_lim_start = all_dates[0]
        x_lim_end   = all_dates[-1]
    ax.set_xlim(x_lim_start, x_lim_end)

    # Vertical lines and marker texts

    # Find first non zero commit date
    ax.axvline(marker_left, color="#7282ee", linewidth=5, alpha=0.3)
    ax.axvline(marker_right, color="#7282ee", linewidth=5, alpha=0.3)

    # First commits text
    label_height = y_lim_top * 0.75
    ax.annotate(
        f"{marker_left.strftime("%b %#d, %Y")}",
        xy=(marker_left, label_height),
        xycoords="data",
        xytext=(8, 0),
        textcoords="offset points",
        fontsize=20,
        color="#333333",
        fontweight="bold",
        ha="left",
        va="bottom",
    )

    # Last commits text
    ax.annotate(
        f"{marker_right.strftime("%b %#d, %Y")}",
        xy=(marker_right, label_height),
        xycoords="data",
        xytext=(-8, 0),
        textcoords="offset points",
        fontsize=20,
        color="#333333",
        fontweight="bold",
        ha="right",
        va="bottom",
    )

    # Title
    ax.set_title(
        f"{author}\n",
        fontsize=32,
        fontweight="bold",
        loc="left"
    )

    # Total commits in the range
    total_commits = 0
    work_days = 0
    for d, count in zip(all_dates, all_counts):
        if marker_left <= d <= marker_right:
            total_commits += count
            if count > 0:
                work_days += 1
    
    logging.info("Generating commit plot")
    logging.info(f"xlim: {marker_left.strftime('%Y-%m-%d')} to {marker_right.strftime('%Y-%m-%d')}")
    logging.info(f"y_lim: {y_lim_top} to 0")
    logging.info(f"Total commits in range: {total_commits}")
    logging.info(f"Total work days: {work_days}")

    ax.text(
        0, 1.03,
        f"{total_commits} commits ({email})",
        transform=ax.transAxes,
        fontsize=20,
        color="#626168",
        fontweight="normal",
        ha="left",
        va="bottom"
    )

    ax.text(
        1, 1.125,
        f"Time: {work_days} working days",
        transform=ax.transAxes,
        fontsize=20,
        color="#7282ee",
        fontweight="normal",
        ha="right",
        va="bottom"
    )

    ax.legend(fontsize=14)
    fig.tight_layout()
    plt.show()
