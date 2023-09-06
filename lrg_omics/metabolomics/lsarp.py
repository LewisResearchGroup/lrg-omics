
def extract_metadata_from_lsarp_metabolomics(df):
    df["MS-file"].apply(lambda x: x.split("_")[5])
    df["MS_COLUMN"] = df["MS-file"].apply(lambda x: x.split("_")[5])
    df["PLATE"] = df["MS-file"].apply(lambda x: x.split("_")[0])
    df["PLATE_ROW"] = df["MS-file"].apply(
        lambda x: x.split("_")[7][0].replace("S", "H")
    )
    df["PLATE_COL"] = df["MS-file"].apply(lambda x: x.split("_")[7][1:])
    df["PLATE_COL"] = [e if e.isnumeric() else "00" for e in df.PLATE_COL]
    df["ISOLATE_NBR"] = df["MS-file"].apply(lambda x: x.split("__")[1])
    df["RUN_NUMBR"] = df["MS-file"].apply(extract_run_number)
    
    
def extract_run_number(name):
    for e in name.split('_'):
        if e.startswith('RN'):
            return int(e[2:])