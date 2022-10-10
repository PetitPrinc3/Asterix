#!/bin/bash

UUID=$(/usr/bin/wget --no-check-certificate -qO- "https://uupdump.net/known.php?q=windows+10+21h2+arm64" | grep 'href="\./selectlang\.php?id=.*"' -o | sed 's/^.*id=//g' | sed 's/"$//g' | head -n1)
WIN_LANG="en-us"

/usr/bin/mkdir tmp

/usr/bin/wget --no-check-certificate -O "tmp/uupdump.zip" "https://uupdump.net/get.php?id={UUID}&pack={WIN_LANG}&edition=professional&autodl=2"

cd tmp

/usr/bin/unzip -q "uupdump.zip"
/bin/bash uup_download_linux.sh

mv *.ISO winarm.iso