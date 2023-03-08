import numpy as np
from matplotlib import pyplot as plt


def plot_metabolomics_hist2d(
    df,
    figsize=(10, 10),
    dpi=300,
    set_dim=True,
    cmap="jet",
    rt_min=None,
    rt_max=None,
    mz_range=None,
    mz_mean=None,
    mz_width=10,
    vmin=0,
    vmax=None,
    take_log=True
):

    if set_dim:
        plt.figure(figsize=figsize, dpi=dpi)

    if mz_range is None:
      if mz_mean is None:
        mz_range = ( df.mz.min(), df.mz.max())
      else:
        dm = mz_mean * 1e-6 * mz_width
        mz_range = (mz_mean-dm, mz_mean+dm)
        
    if rt_min is None:
        rt_min = df.scan_time.min()
    if rt_max is None:
        rt_max = df.scan_time.max()

    rt_range = (rt_min, rt_max)
    
    rt_bins = int( (rt_range[1] - rt_range[0])/2 )

    fig = plt.hist2d(
        df["scan_time"],
        df["mz"],
        weights=df["intensity"].apply(np.log1p) if take_log else df["intensity"],
        bins=[rt_bins, 100],
        vmin=vmin,
        vmax=vmax,
        cmap=cmap,
        range=(rt_range, mz_range),
    )

    plt.xlabel("Scan Time [s]")
    plt.ylabel("m/z")
    plt.grid()
    plt.colorbar()
    plt.ticklabel_format(useOffset=False)
    return fig
