import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Plot
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(all_dates, all_counts, color="#7282ee")
ax.fill_between(all_dates, all_counts, 0, alpha=0.3, color="#7282ee")
ax.set_ylabel("Number of commits")
ax.set_ylabel("Number of commits")

# ax.xaxis.set_major_locator(mdates.MonthLocator())      # tick each month
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))


# Set y-axis limits
ax.set_ylim(0, max(all_counts) + 1)

# Set x-axis limits
# Automatic
# ax.set_xlim(all_dates[0], all_dates[-1])
# Manual
start = datetime(2024, 9, 1)
end   = datetime(2024, 10, 24)

# print(all_dates)
ax.set_xlim(start, end)

# Rotate x labels
# for label in ax.get_xticklabels():
#     label.set_rotation(90)

# Grid
ax.grid(True, axis="y", linestyle="-", alpha=0.5)

plt.show()