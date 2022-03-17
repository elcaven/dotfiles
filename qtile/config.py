# vim:fileencoding=utf-8:ft=python:foldmethod=marker
#: Imports {{{
import os
import subprocess
import psutil

from typing import List  # noqa: F401

from libqtile import bar, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.log_utils import logger

# Layout imports
from libqtile.layout.stack import Stack
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
from qtile_extras.widget import Sep
from qtile_extras.widget.decorations import RectDecoration

from colorschemes import catppuccin as colors
#: }}}

#: Hooks {{{
@hook.subscribe.startup_once
def autostart():
    logger.info("Startup hook called")
    home = os.path.expanduser('/home/simon/.config/qtile/autostart.sh')
    subprocess.call([home])

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
#: }}}

#: Key bindings {{{
mod = "mod4"
alt_key = "mod1"
terminal = "kitty"
scr_locker = "betterlockscreen -l"

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.group.next_window(), desc="Move focus down"),
    Key([mod], "k", lazy.group.prev_window(), desc="Move focus up"),
    Key([alt_key], "j", lazy.group.next_window(), desc="Move window focus to other window"),
    Key([mod], "u", lazy.next_urgent()),
    Key([mod, "shift"], "f", float_to_front),

    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "h", lazy.layout.grow(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.shrink(), desc="Grow window to the right"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "o", lazy.layout.maximize(), desc="Reset all window sizes"),
    Key([mod, "control"], "Return", lazy.layout.flip()),

    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "space", lazy.window.toggle_floating()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "control"], 'j', lazy.next_screen(), desc='Next monitor'),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Restart Qtile"),
    Key([mod, "control", "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show combi")),
    Key([mod], "q", lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu -lines 6")),

    Key([], "XF86MonBrightnessDown", lazy.spawn("sudo ybacklight -dec 1")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("sudo ybacklight -inc 1")),

    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([mod], "d", lazy.spawn("emacs")),
    Key([mod], "n", lazy.spawn("kitty -e lvim")),
    Key([mod], "a", lazy.spawn("kitty -e lvim /home/simon/projects/personal/dotfiles/qtile/config.py")),
    Key([mod], "e", lazy.spawn("kitty -e ranger")),
    Key([mod], "z", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], "p", lazy.group['scratchpad'].dropdown_toggle('insomnia')),
    Key([mod], "o", lazy.group['scratchpad'].dropdown_toggle('browser')),
    Key([alt_key], "l", lazy.spawn(scr_locker)),
    Key([mod], "b", lazy.hide_show_bar("top")),

    # Dunst
    Key(["control"], "space", lazy.spawn("dunstctl close")),
    Key(["control", "shift"], "space", lazy.spawn("dunstctl close-all"))
]
#: }}}

#: Groups {{{
groups = [
    Group(name='1', layout='monadtall'),
    Group(name='2', layout='stack', matches=[
        Match(wm_class='jetbrains-idea'),
        Match(wm_class='jetbrains-toolbox')]),
    Group(name='3', layout='monadtall'),
    Group(name='4', layout='monadtall'),
    Group(name='5', layout='monadtall'),
    Group(name='6', layout='monadtall'),
    Group(name='7', layout='monadtall'),
    Group(name='8', layout='stack', matches=[
        Match(wm_class='slack'),
        Match(wm_class='teams-for-linux'),
        Match(wm_class='microsoft teams - preview'),
        Match(wm_class='microsoft teams - insiders'),
        Match(wm_class='hexchat'),
        Match(wm_class='discord')]),
    Group(name='9', layout='stack', matches=[Match(wm_class="evolution")]),
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
    #layout.Max(**layout_theme),
    Stack(margin=7, num_stacks=1, border_width=0),
    MonadTall(**layout_theme, single_border_width=0, single_margin=7, ratio=0.6),
    MonadWide(**layout_theme, single_border_width=0, single_margin=7, ratio=0.6),
]
#: }}}

#: Bar {{{
widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono Bold", fontsize=11, background=colors.background
)
extension_defaults = widget_defaults.copy()

delimiter_widget = Sep(
    padding=10,
    linewidth=2,
    size_percent=70,
    foreground=colors.alternate_foreground
)

layout_decor = {
    "decorations": [RectDecoration(colour=colors.widget_current_layout, radius=3, filled=True, padding=4, margin=5)],
}
cpu_decor = {
    "decorations": [RectDecoration(colour=colors.cpu_color, radius=3, filled=True, padding=4, margin=5)],
}
mem_decor = {
    "decorations": [RectDecoration(colour=colors.mem_color, radius=3, filled=True, padding=4, margin=5)],
}
date_decor = {
    "decorations": [RectDecoration(colour=colors.date_color, radius=3, filled=True, padding=4, margin=5)],
}

decorationBar = bar.Bar(
    [
        Spacer(length=5),
        GroupBox(
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
            borderwidth=2,
            margin_x=2,
            margin_y=4,
            padding_x=1,
            spacing=4,
            disable_drag=True,
            hide_unused=False,
            font="JuliaMono SemiBold"
        ),
        Spacer(length=5),
        CurrentLayout(**layout_decor, fmt="{}", padding=10, foreground=colors.alternate_foreground),
        Spacer(length=2),
        WindowCount(fmt="[{}]", foreground=colors.widget_current_layout, padding=0),
        Spacer(length=3),
        WindowName(for_current_screen=True, padding=0),
        Spacer(length=8),
        CPU(**cpu_decor, format="cpu {load_percent}%", padding=10, foreground=colors.alternate_foreground),
        Spacer(length=5),
        Memory(**mem_decor, format="mem {MemUsed:.0f}Mb", padding=10, foreground=colors.alternate_foreground),
        Spacer(length=5),
        Clock(**date_decor, format="%a %d %b, %H:%M", padding=10, foreground=colors.alternate_foreground),
        Spacer(length=5),
        Systray(padding=2, background=colors.background),
        Spacer(length=10),
    ],
    25
)

simpleBar = bar.Bar(
    [
        Spacer(length=5),
        GroupBox(
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
            borderwidth=2,
            margin_x=2,
            margin_y=4,
            padding_x=1,
            spacing=4,
            disable_drag=True,
            hide_unused=False,
            font="JuliaMono SemiBold"
        ),
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
        Spacer(length=10),
        Systray(padding=2, background=colors.background),
        Spacer(length=10),
    ],
    23,
)

screens = [
    Screen(top=decorationBar)
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
floating_layout = Floating(
    **layout_border,
    float_rules=[
        *Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
        Match(title='Reminders'),  # Evolution reminders
        Match(wm_class='copyq')
    ])
auto_fullscreen = True
focus_on_window_activation = "focus"
reconfigure_screens = True
follow_mouse_focus = True
auto_minimize = True
wmname = "LG3D"
#: }}}
