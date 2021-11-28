import numpy as np
from matplotlib import pyplot as plt


def plot_metabolomics_hist2d(
    df, figsize=(10, 10), dpi=300, set_dim=True, cmap="binary"
):

    if set_dim:
        plt.figure(figsize=figsize, dpi=dpi)

    fig = plt.hist2d(
        df["retentionTime"],
        df["m/z array"],
        weights=df["intensity array"].apply(np.log1p),
        bins=[15 * 60 // 2, 10000],
        vmin=1,
        vmax=20,
        cmap=cmap,
        range=([0, 15], [0, 1000]),
    )

    plt.xlabel("Retention Time [min]")
    plt.ylabel("M/Z")
    plt.yticks(range(0, 1100, 300))
    plt.grid()

    return fig
