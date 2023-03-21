#!/bin/sh
sed -i \
         -e 's/#1a1b26/rgb(0%,0%,0%)/g' \
         -e 's/#ffffff/rgb(100%,100%,100%)/g' \
    -e 's/#1a1b26/rgb(50%,0%,0%)/g' \
     -e 's/#ff9e64/rgb(0%,50%,0%)/g' \
     -e 's/#24283b/rgb(50%,0%,50%)/g' \
     -e 's/#ffffff/rgb(0%,0%,50%)/g' \
	"$@"
