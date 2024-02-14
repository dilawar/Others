# Plot for Akshaya

import sys
from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def main(datafile: Path):
    print(f"[INFO] Plotting {datafile}")
    df = pd.read_csv(datafile)
    # plt.figure(figsize=(6,4))
    # ax = plt.subplot(1, 1, 1)
    ax = sns.stripplot(df, alpha=0.3, zorder=1, size=4, jitter=0.05, color="0.5")
    ax = sns.boxplot(
        df, width=0.5, linewidth=2, boxprops={"zorder": 3, "facecolor": "none"},
        showfliers=False
    )

    plt.tight_layout()
    plt.savefig(datafile.with_suffix(".png"))
    plt.show()


if __name__ == "__main__":
    main(Path(sys.argv[1]))
