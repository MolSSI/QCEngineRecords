"""
QCEngineVault
A collection of input and output files for QCEngine parsers.
"""

# Make Python 2 and 3 imports work the same
# Safe to remove with Python 3-only code
from __future__ import absolute_import

# Add imports here
from .qcenginevault import *

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
