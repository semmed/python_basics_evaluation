import logging
from pathlib import Path

from nbformat import read, write, NO_CONVERT

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

cur_ipynb = Path(__file__).parent.joinpath("000_Evaluation.ipynb")
if not cur_ipynb.exists():
    raise RuntimeError("unable to locate: %s" % cur_ipynb)
logger.debug("current notebook: %s" % cur_ipynb)

with open(cur_ipynb, 'r') as fid:
    nb = read(fid, NO_CONVERT)

solution_token = "# solution"
for cell in nb.cells:
    if cell.cell_type == 'code':
        keep_row = True
        in_rows = cell.source.splitlines()
        out_rows = list()
        for row in in_rows:
            if solution_token in row:
                keep_row = False
            if keep_row:
                out_rows.append(row)
        cell.source = '\n'.join(out_rows)

        cell['outputs'] = []  # remove output data
        cell['execution_count'] = None  # reset to not executed

with open(cur_ipynb, 'w') as fod:
    write(nb, fod)



