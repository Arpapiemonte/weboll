#!/usr/bin/env python
import os
import sys
from pathlib import Path

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")

    # This allows easy placement of apps within the interior
    # website directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "website"))

    execute_from_command_line(sys.argv)
