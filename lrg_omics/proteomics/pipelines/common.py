import os

def maybe_create_symlink(src, dst):
    if not os.path.isfile(dst):
        os.symlink(src, dst)
