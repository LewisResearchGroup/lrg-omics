import os

import lrg_omics

from pathlib import Path as P


def test__lrg_thermo_worklist_parser(tmpdir):

    src_dir = P(lrg_omics.__file__).parent.parent

    fn_in = P(__file__).parent.parent / "data" / "thermo" / "example-worklist.csv"

    fn_out = P(tmpdir) / "output.csv"

    assert fn_in.is_file(), fn_in
    assert not fn_out.is_file(), fn_out

    cmd = (
        f"python {src_dir}/scripts/lrg_thermo_worklist_parser.py -f {fn_in} -o {fn_out}"
    )
    os.system(cmd)

    print(cmd)

    assert fn_out.is_file(), fn_out
