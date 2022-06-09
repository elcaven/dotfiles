# vim:fileencoding=utf-8:ft=python:foldmethod=marker
#: Imports {{{
import os
import subprocess
import psutil
import nerdfonts as nf

from typing import List  # noqa: F401

from libqtile import bar, hook, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.log_utils import logger

# Layout imports
from libqtile.layout.max import Max
from libqtile.layout.floating import Floating
from libqtile.layout.xmonad import MonadTall, MonadWide

# Widget imports
from qtile_extras.widget import CPU
from qtile_extras.widget import Memory
from qtile_extras.widget import Spacer
from qtile_extras.widget import TextBox
from qtile_extras.widget import GroupBox
from qtile_extras.widget import WindowCount
from qtile_extras.widget import CurrentLayout
from qtile_extras.widget import WindowName
from qtile_extras.widget import Clock
from qtile_extras.widget import Systray
from qtile_extras.widget import Chord
from qtile_extras.widget import GenPollText
from qtile_extras.widget.decorations import RectDecoration

from qtile_extras.popup.toolkit import (
    PopupRelativeLayout, PopupImage, PopupText, PopupWidget
)

from colorschemes import catppuccin as colors
#: }}}

#: Hooks {{{
@hook.subscribe.startup_once
def autostart():
    logger.info("Startup hook called")
    home = os.path.expanduser('/home/simon/.config/qtile/autostart.sh')
    subprocess.Popen([home])

@hook.subscribe.screen_change
def screen_change(event):
    logger.info("Screen change hook called", event)
    home = os.path.expanduser('/home/simon/.config/qtile/scripts/screen_change.sh')
    subprocess.call([home])

@hook.subscribe.client_new
def swallow(window):
    pid = window.window.get_net_wm_pid()
    ppid = psutil.Process(pid).ppid()
    cpids = {c.window.get_net_wm_pid(): wid for wid, c in window.qtile.windows_map.items()}
    for i in range(5):
        if not ppid:
            return
        if ppid in cpids:
            parent = window.qtile.windows_map.get(cpids[ppid])
            parent.minimized = True
            window.parent = parent
            return
        ppid = psutil.Process(ppid).ppid()

@hook.subscribe.client_killed
def unswallow(window):
    if hasattr(window, 'parent'):
        window.parent.minimized = False
#: }}}

#: Functions {{{
@lazy.function
def float_to_front(qtile):
    logger.info("Bring floating windows to front")
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.cmd_bring_to_front()

def get_notification_status():
    status = subprocess.check_output(['dunstctl', 'is-paused']).decode('utf-8').strip()
    if status == "true":
        return nf.icons["fa_bell_slash"]
    else:
        return nf.icons["fa_bell"]

def toggle_notification_status():
    subprocess.call(['dunstctl', 'set-paused', 'toggle'])

def show_graphs(qtile):
    controls = [
        PopupWidget(
            widget=widget.CPUGraph(),
            width=0.45,
            height=0.45,
            pos_x=0.05,
            pos_y=0.05
        ),
        PopupWidget(
            widget=widget.NetGraph(),
            width=0.45,
            height=0.45,
            pos_x=0.5,
            pos_y=0.05
        ),
        PopupWidget(
            widget=widget.MemoryGraph(),
            width=0.9,
            height=0.45,
            pos_x=0.05,
            pos_y=0.5
        )
    ]

    layout = PopupRelativeLayout(
        qtile,
        width=1000,
        height=200,
        controls=controls,
        background="00000060",
        initial_focus=None,
        close_on_click=False
    )
    layout.show(centered=True)
#: }}}

#: Key bindings {{{
mod = "mod4"
alt_key = "mod1"
terminal = "kitty"
scr_locker = "betterlockscreen -l"

# Chord names
window_resize = "window resize"
window_move = "window move"
spawn="spawn"

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.group.next_window(), desc="Move focus to next window"),
    Key([mod], "k", lazy.group.prev_window(), desc="Move focus to previous window"),
    Key([mod], "u", lazy.next_urgent()),
    Key([mod, "shift"], "f", float_to_front),

    #Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    #Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    #Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    #Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    #Key([mod, "control"], "h", lazy.layout.grow(), desc="Grow window to the left"),
    #Key([mod, "control"], "l", lazy.layout.shrink(), desc="Grow window to the right"),
    #Key([mod], "o", lazy.layout.maximize(), desc="Reset all window sizes"),
    Key([mod, "control"], "Return", lazy.layout.flip()),

    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "space", lazy.window.toggle_floating()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "control"], 'j', lazy.next_screen(), desc='Next monitor'),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload Qtile config"),
    Key([mod, "control", "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show combi")),
    Key([mod], "q", lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu -lines 6")),

    Key([], "XF86MonBrightnessDown", lazy.spawn("sudo ybacklight -dec 1")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("sudo ybacklight -inc 1")),

    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([mod], "z", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], "p", lazy.group['scratchpad'].dropdown_toggle('insomnia')),
    Key([mod], "o", lazy.group['scratchpad'].dropdown_toggle('browser')),
    Key([alt_key], "l", lazy.spawn(scr_locker)),
    Key([mod], "b", lazy.hide_show_bar("top")),
    Key([mod, "shift"], "q", lazy.function(show_graphs)),

    # Dunst
    Key(["control"], "space", lazy.spawn("dunstctl close")),
    Key(["control", "shift"], "space", lazy.spawn("dunstctl close-all")),

    # Chords
    KeyChord([mod], "i", [
        Key([], "l", lazy.layout.grow()),
        Key([], "h", lazy.layout.shrink()),
        Key([], "n", lazy.layout.normalize()),
        Key([], "m", lazy.layout.maximize(), desc="Reset all window sizes")],
        mode=window_resize
    ),
    KeyChord([mod], "m", [
        Key([], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
        Key([], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
        Key([], "j", lazy.layout.shuffle_down(), desc="Move window down"),
        Key([], "k", lazy.layout.shuffle_up(), desc="Move window up")],
        mode=window_move
    ),
    KeyChord([mod], "s", [
        Key([], "e", lazy.spawn("emacs")),
        Key([], "l", lazy.spawn("kitty -e lvim")),
        Key([], "r", lazy.spawn("kitty -e ranger")),
        Key([], "q", lazy.spawn("kitty -e lvim /home/simon/projects/personal/dotfiles/qtile/config.py"))],
        mode=spawn
    ),
]
#: }}}

#: Groups {{{
groups = [
    Group(name='1', layout='monadtall'),
    Group(name='2', layout='max', matches=[
        Match(wm_class='jetbrains-idea'),
        Match(wm_class='jetbrains-toolbox')]),
    Group(name='3', layout='monadtall'),
    Group(name='4', layout='monadtall'),
    Group(name='5', layout='monadtall'),
    Group(name='6', layout='monadtall'),
    Group(name='7', layout='monadtall'),
    Group(name='8', layout='max', matches=[
        Match(wm_class='slack'),
        Match(wm_class='teams-for-linux'),
        Match(wm_class='microsoft teams - preview'),
        Match(wm_class='microsoft teams - insiders'),
        Match(wm_class='hexchat'),
        Match(wm_class='discord')]),
    Group(name='9', layout='max', matches=[
        Match(wm_class="evolution")]),
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(toggle=True),
            desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])

# Append scratchpad after setting up group keybinds
groups.append(ScratchPad("scratchpad", [
    DropDown("term", "kitty", opacity=1, height=0.4, x=0, width=0.998, on_focus_lost_hide=True),
    DropDown("insomnia", "insomnia", opacity=1, height=0.997, x=0, width=0.998, on_focus_lost_hide=True),
    DropDown("browser", "qutebrowser", opacity=1, height=0.997, x=0, width=0.998, on_focus_lost_hide=True),
]))
#: }}}

#: Layouts {{{
layout_border = dict(
    border_width=2,
    border_focus=colors.border_focus,
    border_normal=colors.border_normal,
)

layout_theme = {
    **layout_border,
    "margin": 7,
}

layouts = [
    Max(margin=7, border_width=0),
    MonadTall(**layout_theme, single_border_width=0, single_margin=7, ratio=0.6),
    MonadWide(**layout_theme, single_border_width=0, single_margin=7, ratio=0.6),
]

floating_layout = Floating(
    **layout_border,
    float_rules=[
        *Floating.default_float_rules,
        Match(title='Reminders'),  # Evolution reminders
        Match(wm_class='copyq')
    ])
#: }}}

#: Bar {{{
widget_defaults = dict(
    font="JetBrainsMonoExtraBold Nerd Font Mono",
    fontsize=11, 
    background=colors.background
)
extension_defaults = widget_defaults.copy()

decor = {
    "decorations": [RectDecoration(radius=4, filled=True, padding=4, margin=5, use_widget_background=True)],
}
blockDecor = {
    "decorations": [RectDecoration(radius=0, filled=True, padding_y=3, use_widget_background=True)],
}

groupBoxWidget = GroupBox(
    highlight_method="line",
    urgent_alert_method="text",
    urgent_text=colors.groupbox_urgent,
    block_highlight_text_color="#ffffff",
    this_current_screen_border=colors.groupbox_current_screen_border,
    this_screen_border=colors.groupbox_screen_border,
    other_screen_border=colors.groupbox_other_screen_border,
    other_current_screen_border=colors.groupbox_current_screen_border,
    highlight_color=colors.highlight_color,
    inactive=colors.groupbox_inactive,
    borderwidth=2, margin_x=2, margin_y=4, padding_x=1, spacing=4,
    disable_drag=True, hide_unused=False,
    font="JuliaMono SemiBold"
)

chordWidget = Chord(
    font="JetBrainsMonoExtraBold Nerd Font Mono",
    fontsize=11,
    width=7,
    background=colors.background,
    margin=5, padding=4, fmt="",
    chords_colors={
        '': (colors.background, 'ffffff'),
        window_resize: (colors.window_resize_chord_color, 'ffffff'),
        window_move: (colors.window_move_chord_color, 'ffffff'),
        spawn: (colors.spawn_chord_color, 'ffffff'),
    }
)

    
blocksBar = bar.Bar(
    [
        chordWidget,
        Spacer(length=5),
        groupBoxWidget,
        Spacer(length=5),
        WindowCount(**blockDecor, fmt="{}", padding=5, foreground=colors.alternate_foreground, background = colors.widget_current_layout),
        CurrentLayout(**blockDecor, fmt="{}", padding=10, foreground=colors.foreground, background=colors.alternate_background),
        Spacer(length=8),
        WindowName(for_current_screen=True, padding=0),
        Spacer(length=8),
        TextBox(**blockDecor, fmt="", foreground=colors.alternate_foreground, background=colors.cpu_color, margin=0),
        CPU(**blockDecor, format="{load_percent}%", padding=10, foreground=colors.foreground, background=colors.alternate_background),
        Spacer(length=7),
        TextBox(**blockDecor, fmt="", foreground=colors.alternate_foreground, background=colors.mem_color, margin=0),
        Memory(**blockDecor, format="{MemUsed:.0f}Mb", padding=10, foreground=colors.foreground, background=colors.alternate_background),
        Spacer(length=7),
        TextBox(**blockDecor, fmt="", foreground=colors.alternate_foreground, background=colors.date_color, margin=0),
        Clock(**blockDecor, format="%a %d %b, %H:%M", padding=10, foreground=colors.foreground, background=colors.alternate_background),
        Spacer(length=5),
        Systray(padding=2, background=colors.background),
        Spacer(length=10),
    ],
    23
)

simpleBar = bar.Bar(
    [
        chordWidget,
        Spacer(length=1),
        groupBoxWidget,
        Spacer(length=5),
        WindowCount(fmt="[{}]", padding=0, foreground=colors.widget_current_layout),
        CurrentLayout(fmt="[{}]", padding=0, foreground=colors.widget_window_count),
        Spacer(length=3),
        WindowName(for_current_screen=True),
        Spacer(length=8),
        TextBox(text='cpu', padding=5, foreground=colors.cpu_color),
        CPU(format="{load_percent}%", padding=0),
        Spacer(length=12),
        TextBox(text='mem', padding=5, foreground=colors.mem_color),
        Memory(format="{MemUsed:.0f}Mb", padding=0),
        Spacer(length=12),
        TextBox(text='dt', padding=5, foreground=colors.date_color),
        Clock(format="%a %d %b, %H:%M", padding=0, margin_y=0),
        Spacer(length=12),
        Systray(padding=2, background=colors.background),
        GenPollText(
            func=get_notification_status, update_interval=0.1, 
            mouse_callbacks={"Button1": toggle_notification_status},
            fontsize=21, padding=4),
        Spacer(length=10),
    ],
    23,
)

screens = [
    Screen(top=simpleBar)
]
#: }}}

#: Configurations {{{
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "focus"
reconfigure_screens = True
follow_mouse_focus = True
auto_minimize = True
wmname = "LG3D"
#: }}}
