import os
import pathlib
import sys
from catalog_schema import validate_tree

try:
    entries = validate_tree(pathlib.Path(sys.argv[1]),
        pathlib.Path(sys.argv[2]) if len(sys.argv)>2 else None,
        os.environ.get('PR_AUTHOR_ID'),('74422918',))
except (ValueError,KeyError,OSError,TypeError,IndexError) as error:
    print('::error::'+str(error).replace('\n',' ')[:500])
    sys.exit(1)
print(f'{len(entries)} entries validated. No skill was executed. Human review is still required.')
