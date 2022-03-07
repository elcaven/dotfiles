#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $1 &
  fi
}

run "nm-applet"
run "pasystray"
run "blueman-applet"
run "clipit -n"
run "copyq"
run "cbatticon"
run "trackball"
run "/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1"
autorandr --change
nitrogen --restore
run "picom --experimental-backends -b"
/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,gpg
xcalib /home/simon/.colorprofiles/90T02_LQ156R1.icm
