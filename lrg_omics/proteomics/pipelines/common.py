from pathlib import Path as P

def maybe_create_symlink(src, dst):
    if not os.path.isfile(dst):
        os.symlink(src, dst)
               
def create_mqpar(param, raw, fasta, label, outfilename='mqpar.xml'):
    with open(get_param_template(param), 'r') as file:
        string = file.read()\
                     .replace('__RAW__', raw)\
                     .replace('__FASTA__', str(FASTA/P(fasta)))\
                     .replace('__LABEL__', label)
    with open(outfilename, 'w') as file:
        file.write(string)
    assert os.path.isfile(outfilename)
