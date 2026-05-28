import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from slanplot.distribution.calendar import CalendarHeatmap

def main():
    # MATLAB's demo1 sets rng(1) -> equivalent for python
    np.random.seed(1)
    
    # Generate continuous dates
    dates = pd.date_range(start='2020-01-01', end='2022-12-31')
    
    # Generate smoothed random values
    v = np.random.randn(len(dates))
    v = pd.Series(v).rolling(window=10, min_periods=1, center=True).mean().values
    
    fig, ax = plt.subplots(figsize=(15, 4))
    fig.patch.set_facecolor('white')
    
    ch = CalendarHeatmap(year=2021, dates=dates, values=v, ax=ax, month_lim=(1, 12))
    ch.draw()
    
    plt.savefig("output_calendar.png", dpi=300, bbox_inches='tight')
    print("Saved demo1_calendar.png")

if __name__ == "__main__":
    main()
