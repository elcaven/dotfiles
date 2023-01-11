#!/bin/bash

function run {
  if ! pgrep $1 ;
  then
    $1 &
  fi
}

run "nm-applet --indicator"
run "pasystray"
run "blueman-applet"
run "clipit -n"
run "copyq"
run "cbatticon"
trackball
run "/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1"
autorandr --change
nitrogen --restore
run "picom -b"
/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh,gpg
xcalib /home/simon/.config/colorprofiles/Dell_AW2518HF_user.icm
