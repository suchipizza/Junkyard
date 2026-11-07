"""Junkyard: parametric, agent-ready mechanical parts for robots.

M1 ships the data layer only: schemas, vocabularies, loaders and reference
resolution. The public API (search, get, generate, add, export) arrives in M4.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("junkyard-robotics")
except PackageNotFoundError:  # running from a source tree without install
    __version__ = "0.0.0+unknown"

#: Version of the record schemas in section 5 of the PRD.
SCHEMA_VERSION = "0.2.0"

__all__ = ["SCHEMA_VERSION", "__version__"]
