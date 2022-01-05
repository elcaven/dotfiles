#!/bin/bash

#notify-send "Screen has changed"
trackball
xrandr --output eDP1 --set "Broadcast RGB" "Full"
xrandr --output DP2-3 --set "Broadcast RGB" "Full"
xrandr --output DP-2-3 --set "Broadcast RGB" "Full"
nitrogen --restore
