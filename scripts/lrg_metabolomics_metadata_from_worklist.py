import argparse
from pathlib import Path as P
from lrg_omics.metabolomics.worklists import read_worklist, get_metadata_from_worklist


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Read ThermoFisher worklist and extract data.')
    parser.add_argument('-f', dest='fn_inp', help='Input ThermoFisher workist file (csv format)')
    parser.add_argument('-o', dest='fn_out', help='Output file name', default='metadata.csv')
    parser.add_argument('--groupby')
    args = parser.parse_args()

    fn_inp = args.fn_inp
    fn_out = args.fn_out        

    assert fn_inp.lower().endswith('.csv')
    assert fn_out.lower().endswith('.csv')

    worklist = read_worklist(fn_inp)
    metadata = get_metadata_from_worklist(worklist)

    if args.groupby is not None:
        fn_out = P(fn_out).stem
        for ndx, grp in metadata.groupby(args.groupby):
            _fn_out = f'{fn_out}_{ndx}.csv'
            assert not P(_fn_out).is_file(), f'{_fn_out} already exists'
            grp.to_csv(_fn_out, index=False)
    else:
        assert not P(fn_out).is_file(), f'{fn_out} already exists'
        metadata.to_csv(fn_out)

