#!/bin/sh
sed -i \
         -e 's/#0f111a/rgb(0%,0%,0%)/g' \
         -e 's/#ffffff/rgb(100%,100%,100%)/g' \
    -e 's/#0f111a/rgb(50%,0%,0%)/g' \
     -e 's/#3FDCEE/rgb(0%,50%,0%)/g' \
     -e 's/#131621/rgb(50%,0%,50%)/g' \
     -e 's/#ffffff/rgb(0%,0%,50%)/g' \
	"$@"
