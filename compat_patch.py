# compat_patch.py

import pkgutil

# Patch for Python 3.13 compatibility
if not hasattr(pkgutil, "ImpImporter"):
    pkgutil.ImpImporter = lambda *args, **kwargs: None
