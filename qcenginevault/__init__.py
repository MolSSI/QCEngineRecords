"""
QCEngineVault
A collection of input and output files for QCEngine parsers.
"""

from .main import get_required_files, list_test_cases, list_programs, get_test_case_filenames

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions
