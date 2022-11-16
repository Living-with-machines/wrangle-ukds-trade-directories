from pathlib import Path

import shutil

from .errors import NotAFileError


def _copy(self, target):
    try:
        assert self.is_file()
    except AssertionError:
        raise NotAFileError(self)

    target.parent.mkdir(parents=True, exist_ok=True)

    shutil.copy(str(self), str(target))


Path.copy = _copy
