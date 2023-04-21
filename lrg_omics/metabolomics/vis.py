import numpy as np
from matplotlib import pyplot as plt


def plot_metabolomics_hist2d(
    df,
    figsize=(10, 10),
    dpi=300,
    set_dim=True,
    cmap="jet",
    rt_range=None,
    mz_range=None,
):

    if set_dim:
        plt.figure(figsize=figsize, dpi=dpi)

    if mz_range is None:
        mz_range = (df.mz.min(), df.mz.max())

    if rt_range is None:
        rt_range = (df.scan_time.min(), df.scan_time.max())

    rt_bins = int((rt_range[1] - rt_range[0]) / 2)
    # mz_bins = int(mz_range[1] - mz_range[0])*100

    fig = plt.hist2d(
        df["scan_time"],
        df["mz"],
        weights=df["intensity"].apply(np.log1p),
        bins=[rt_bins, 100],
        vmin=1,
        vmax=15,
        cmap=cmap,
        range=(rt_range, mz_range),
    )

    plt.xlabel("Scan Time")
    plt.ylabel("M/Z")
    plt.grid()

    return fig
