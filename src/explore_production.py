"""
Step 1 (cont.) — First look: monthly oil production per producer well over
the life of the field. This is the plot that tells us, at a glance, whether
wells behave independently or seem to move together (a first visual hint of
connectivity, before any graph is built).
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from load_data import load_monthly

OUT_DIR = Path(__file__).resolve().parents[1] / "notebooks"
OUT_DIR.mkdir(exist_ok=True)


def main() -> None:
    monthly = load_monthly()
    monthly["date"] = pd.to_datetime(dict(year=monthly["Year"], month=monthly["Month"], day=1))

    fig, ax = plt.subplots(figsize=(11, 6))
    for well, group in monthly.groupby("Wellbore name"):
        group = group.sort_values("date")
        ax.plot(group["date"], group["Oil"], marker="o", markersize=2, label=well)

    ax.set_title("Volve field — monthly oil production by well (2007–2016)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Oil (Sm3/month)")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()

    out_path = OUT_DIR / "01_monthly_oil_by_well.png"
    fig.savefig(out_path, dpi=150)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
