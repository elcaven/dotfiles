#!/bin/sh
sed -i \
         -e 's/rgb(0%,0%,0%)/#0f111a/g' \
         -e 's/rgb(100%,100%,100%)/#ffffff/g' \
    -e 's/rgb(50%,0%,0%)/#0f111a/g' \
     -e 's/rgb(0%,50%,0%)/#3FDCEE/g' \
 -e 's/rgb(0%,50.196078%,0%)/#3FDCEE/g' \
     -e 's/rgb(50%,0%,50%)/#131621/g' \
 -e 's/rgb(50.196078%,0%,50.196078%)/#131621/g' \
     -e 's/rgb(0%,0%,50%)/#ffffff/g' \
	"$@"
