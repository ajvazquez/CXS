"""
Generates symlink for legacy sources.
"""
import glob
import os

current = os.path.dirname(os.path.abspath(__file__))
dirs = os.path.dirname(os.path.abspath(__file__)).split("/")
base = current+"/../../"

files = glob.glob(base+"cxs/**/*.py", recursive=True)
dest = base+"src/"

for f in files:
    df = f.split("/")[-1]
    dir = f.split("/")[-2]
    if df == "__init__.py":
        continue
    if dir == "tests":
        continue
    df = dest+df
    f = os.path.normpath(f)
    df = os.path.normpath(df)
    #os.system("echo {} {}".format(f, df))
    os.system("unlink {}".format(df))
    os.system("ln -s {} {}".format(f, df))
