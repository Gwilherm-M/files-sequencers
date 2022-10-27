from pprint import pprint
import pathlib as plb
import logging as log
import argparse
from sequencers import files_sequences

FORMAT = "%(asctime)s %(levelname)s %(message)s"
log.basicConfig(
    format=FORMAT,
    # level=log.INFO,
    filemode="w",
)
# if __name__ == "__main__":
parser = argparse.ArgumentParser(
    description="Reformate view of seqences files."
)
parser.add_argument(
    "-p", "--path", type=str, default="", help="Path at explorer."
)

args = parser.parse_args()
path = plb.Path(args.path)

if str(path) == ".":
    path = path.cwd()
    log.info(f"Path is not set. Choise automatic {path}.")
elif not path.is_dir():
    log.fatal("Path is not directoy.")
    raise ValueError("Path is not directoy.")
elif not path.exists():
    log.fatal("Path not exists.")
    raise

files = (str(path_f.name) for path_f in path.iterdir())
pprint(files_sequences.format_sequences(files))

# from package_a.main import main
# if __name__ == '__main__':
#     main()
