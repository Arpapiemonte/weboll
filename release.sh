#!/bin/sh
# Weboll release script: update the version strings in `config/version.py` and `package.json`
#
# Usage:
# - commit all the changes you want to release to whatever branch
# - launch this script from the base dir of the project
# - commit all changes and ship
#
# To increment the mayor.minor part, tag a commit as in:
#   git tag -a -m 'start of 1.0 version' 1.0 HEAD
#
# Copyright (C) 2025 Arpa Piemonte - Dipartimento Naturali e Ambientali
# This file is part of weboll (the bulletin back-office for ARPA Piemonte).
# weboll is licensed under the AGPL-3.0-or-later License.
# License text available at https://www.gnu.org/licenses/agpl.txt

set -e

DATE=$(git log -n1 | grep '^Date:' | sed 's/Date: *\(.*\)/\1/g')
DATE_SHORT=$(git log --date=short -n1 | grep '^Date:' | sed 's/Date: *\(.*\)/\1/g')
GIT_MAJOR=$(git describe --long | cut -d- -f1 | cut -d. -f1)
GIT_MINOR=$(git describe --long | cut -d- -f1 | cut -d. -f2)
GIT_PATCH=$(git describe --long | cut -d- -f2)
GIT_COMMIT=$(git log -n1 --pretty='%h')
GIT_VERSION="$GIT_MAJOR.$GIT_MINOR.$GIT_PATCH+$GIT_COMMIT"

sed -i "s/\"version\": \".*\"/\"version\": \"$GIT_VERSION\"/g" package.json
echo "__version__ = \"$GIT_VERSION\"" > config/version.py
echo "__date__ = \"$DATE\"" >> config/version.py
sed -i "s/softwareVersion: \".*\"$/softwareVersion: \"$GIT_VERSION\"/g" publiccode.yml
sed -i "s/releaseDate: \".*\"$/releaseDate: \"$DATE_SHORT\"/g" publiccode.yml

echo "$GIT_VERSION"
