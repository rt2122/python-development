import os
import sys
import venv
from tempfile import TemporaryDirectory
import subprocess

with TemporaryDirectory() as tmpdir:
    venv.create(tmpdir, with_pip=True)
    subprocess.run([os.path.join(tmpdir, 'bin/pip'), 'install', 'pyfiglet'], capture_output=True)
    subprocess.run([os.path.join(tmpdir, 'bin/python3'), '-m', 'figdate'] + sys.argv[1:])

