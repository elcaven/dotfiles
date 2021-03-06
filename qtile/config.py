# vim:fileencoding=utf-8:ft=python:foldmethod=marker
#: Imports {{{
import os
import subprocess
import psutil
import nerdfonts as nf

from typing import List  # noqa: F401

from libqtile import bar, hook
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, ScratchPad, DropDown, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger

# Layout imports
from libqtile.layout.max import Max
from libqtile.layout.floating import Floating
from libqtile.layout.xmonad import MonadTall, MonadWide

# Widget imports
from qtile_extras.widget import (
    CPU, Memory, Spacer, TextBox, GroupBox, WindowCount, CurrentLayout, CurrentLayoutIcon, WindowName, Clock, Systray, Chord, GenPollText, WidgetBox
)
from qtile_extras.widget.decorations import RectDecoration, BorderDecoration

from colorschemes import catppuccin as colors
#: }}}

#: Variables {{{
mod = "mod4"
alt_key = "mod1"
terminal = "kitty"
scr_locker = "betterlockscreen -l"
window_resize = "window resize"
window_move = "window move"
spawn="spawn"
#: }}}

#: Hooks {{{
@hook.subscribe.startup_once
def autostart():
    logger.info("Startup hook called")
    home = os.path.expanduser('/home/simon/.config/qtile/scripts/autostart.sh')
    subprocess.Popen([home])

@hook.subscribe.screen_change
def screen_change(event):
    #logger.info("Screen change hook called %s", event)
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

@lazy.function
def focus_next_screen(qtile):
    lazy.next_screen()
    group = qtile.current_group
    if group.current_window is not None:
        win = group.current_window
        win.window.warp_pointer(win.width // 2, win.height // 2)

def get_notification_status():
    status = subprocess.check_output(['dunstctl', 'is-paused']).decode('utf-8').strip()
    if status == "true":
        return nf.icons["fa_bell_slash"]
    else:
        return nf.icons["fa_bell"]

def toggle_notification_status():
    subprocess.call(['dunstctl', 'set-paused', 'toggle'])

@lazy.function
def open_dashboard(qtile):
    home = os.path.expanduser('/home/simon/.config/qtile/scripts/eww_dashboard.sh')
    subprocess.call([home])

def calendar_popup():
    home = os.path.expanduser('/home/simon/.config/qtile/scripts/eww_calendar_popup.sh')
    subprocess.call([home])
#: }}}

#: Key bindings {{{
keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.group.next_window(), desc="Move focus to next window"),
    Key([mod], "k", lazy.group.prev_window(), desc="Move focus to previous window"),
    Key([mod], "u", lazy.next_urgent()),
    Key([mod, "shift"], "f", float_to_front),
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

    Key([], "XF86MonBrightnessDown", lazy.spawn("sudo ybacklight -dec 3")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("sudo ybacklight -inc 3")),

    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([alt_key], "l", lazy.spawn(scr_locker)),
    Key([mod], "b", lazy.hide_show_bar("top")),
    Key([mod], "y", open_dashboard()),

    # ScratchPads
    Key([mod], "z", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], "p", lazy.group['scratchpad'].dropdown_toggle('insomnia')),
    Key([mod], "o", lazy.group['scratchpad'].dropdown_toggle('browser')),

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
        Key([], "q", lazy.spawn("kitty -e lvim /home/simon/projects/personal/dotfiles/qtile/config.py")),
        Key([], "d", lazy.spawn("kitty -e lvim /home/simon/projects/personal/dotfiles"))],
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

#: Widgets {{{
# widget_defaults = dict(
#     font="JetBrainsMonoExtraBold Nerd Font Mono",
#     fontsize=11, 
#     background=colors.background
# )

widget_defaults = dict(
    font="JetBrainsMonoExtraBold Nerd Font Mono",
    fontsize=11,
    padding=3,
    background=colors.background,
    decorations=[
        BorderDecoration(
            colour=colors.background,
            border_width=[5, 0, 4, 0],
        )
    ],
)
extension_defaults = widget_defaults.copy()

group_box_settings = {
    "padding": 2,
    "borderwidth": 2,
    "active": colors.foreground,
    "inactive": colors.groupbox_inactive,
    "disable_drag": True,
    "rounded": True,
    "highlight_color": colors.highlight_color,
    "block_highlight_text_color": colors.highlight_color,
    "highlight_method": "block",
    "block_highlight_text_color": colors.alternate_foreground,
    "urgent_alert_method": "text",
    "urgent_text": colors.groupbox_urgent,
    "this_current_screen_border": colors.groupbox_current_screen_border,
    "this_screen_border": colors.groupbox_screen_border,
    "other_current_screen_border": colors.groupbox_other_current_screen_border,
    "other_screen_border": colors.groupbox_other_screen_border,
    "foreground": colors.foreground,
    "background": colors.alternate_background,
    "urgent_border": colors.groupbox_urgent,
    "spacing": 4,
}


blockDecor = {
    "decorations": [RectDecoration(radius=0, filled=True, padding_y=3, use_widget_background=True)], }

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
    font="JetBrainsMono Bold"
)

chordWidget = Chord(
    font="JetBrainsMonoExtraBold Nerd Font Mono",
    fontsize=11,
    width=7,
    background=colors.background,
    margin=0, padding=0, fmt="",
    chords_colors={
        '': (colors.background, 'ffffff'),
        window_resize: (colors.window_resize_chord_color, 'ffffff'),
        window_move: (colors.window_move_chord_color, 'ffffff'),
        spawn: (colors.spawn_chord_color, 'ffffff'),
    },
    decorations=[
        BorderDecoration(
            colour=colors.background,
            border_width=[0, 0, 0, 0],
        )
    ],
)

doNotDisturbIcon = GenPollText(
    func=get_notification_status, 
    update_interval=0.1, 
    foreground=colors.notification_color,
    background=colors.alternate_background,
    mouse_callbacks={"Button1": toggle_notification_status},
    fontsize=21, padding=2, margin=0)

systrayWidgetBox = WidgetBox(
    widgets = [
        Systray(padding=2, background=colors.background),
        # doNotDisturbIcon
    ],
    font = "JetBrainsMonoExtraBold Nerd Font Mono", fontsize=18,
    close_button_location = "right", text_open = "???", text_closed = "???")

roundedLeftSide = TextBox(
    text="???",
    foreground=colors.alternate_background,
    fontsize=19,
    padding=0,
)
roundedRightSide = TextBox(
    text="???",
    foreground=colors.alternate_background,
    fontsize=19,
    padding=0,
)
#: }}}

#: Bars {{{
#: Nebula {{{
# inspired by https://gitlab.com/Barbaross/Nebula
nebula = bar.Bar(
    [
        chordWidget,
        Spacer(length=3),
        TextBox(
            text="???",
            foreground=colors.widget_accent_foreground,
            font="Font Awesome 6 Free Solid",
            fontsize=20,
            # padding=10,
            mouse_callbacks={"Button1": open_dashboard}
        ),
        Spacer(length=5),
        roundedLeftSide,
        GroupBox(**group_box_settings),
        roundedRightSide,
        Spacer(length=5),
        roundedLeftSide,
        CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser("~/.config/qtile/icons")],
            foreground=colors.widget_current_layout,
            background=colors.alternate_background,
            padding=0, scale=0.5,
        ),
        WindowCount(            
            background=colors.alternate_background,
            foreground = colors.foreground
        ),
        roundedRightSide,
        
        Spacer(length=5),
        Spacer(),
        TextBox(
            text="??? ",
            foreground=colors.lavender,
            background=colors.background,
            # fontsize=38,
            font="Font Awesome 6 Free Solid",
        ),
        WindowName(
            background=colors.background,
            foreground=colors.window_title_color,
            width=bar.CALCULATED,
            empty_group_string="Desktop",
            max_chars=130,
            # mouse_callbacks={"Button2": kill_window},
        ),
        Spacer(),
        systrayWidgetBox,
        Spacer(length=10),
        roundedLeftSide,
        TextBox(
            text="??? ",
            font="Font Awesome 6 Free Solid",
            foreground=colors.date_color,  # fontsize=38
            background=colors.alternate_background,
            mouse_callbacks={"Button1": calendar_popup}
        ),
        Clock(
            format="%a, %b %d",
            background=colors.alternate_background,
            foreground=colors.foreground,
            mouse_callbacks={"Button1": calendar_popup}
        ),
        roundedRightSide,
        Spacer(length=5),
        roundedLeftSide,
        TextBox(
            text="??? ",
            font="Font Awesome 6 Free Solid",
            foreground=colors.date_color_alternate,
            background=colors.alternate_background,
            mouse_callbacks={"Button1": calendar_popup}
        ),
        Clock(
            format="%I:%M %p",
            foreground=colors.foreground,
            background=colors.alternate_background,
            mouse_callbacks={"Button1": calendar_popup}
        ),
        roundedRightSide,
        Spacer(length=5),
        roundedLeftSide,
        doNotDisturbIcon,
        roundedRightSide,
        Spacer(length=10)
        #TextBox(
        #    text="???",
        #    foreground=colors.red,
        #    font="Font Awesome 6 Free Solid",
        #    fontsize=20,
        #    padding=10,
        #    # mouse_callbacks={"Button1": open_powermenu},
        #),
    ],
    33,
    margin=[0, 0, 0, 0],
    #border_width=[0, 0, 3, 0],
    #border_color="#0000000",
)
#: }}}

#: Centered {{{
centeredBar = bar.Bar(
    [
        chordWidget,
        Spacer(length=2),
        groupBoxWidget,
        Spacer(length=12),
        CurrentLayout(fmt="[{}]", padding=0, foreground=colors.widget_window_count),
        WindowCount(fmt="[{}]", padding=0, foreground=colors.widget_current_layout),
        Spacer(),
        Clock(format="%a %d %b, %H:%M", padding=0, margin_y=0),
        Spacer(),
        TextBox(text='cpu', padding=5, foreground=colors.cpu_color),
        CPU(format="{load_percent}%", padding=0),
        Spacer(length=12),
        TextBox(text='mem', padding=5, foreground=colors.mem_color),
        Memory(format="{MemUsed:.0f}Mb", padding=0),
        Spacer(length=8),
        systrayWidgetBox,
        Spacer(length=10),
    ],
    23
)
#: }}}

#: Simple {{{
simpleBar = bar.Bar(
    [
        chordWidget,
        Spacer(length=1),
        groupBoxWidget,
        Spacer(length=5),
        CurrentLayout(fmt="[{}]", padding=0, foreground=colors.widget_window_count),
        WindowCount(fmt="[{}]", padding=0, foreground=colors.widget_current_layout),
        #Spacer(length=3),
        #WindowName(for_current_screen=True),
        #Spacer(length=8),
        Spacer(),
        TextBox(text='cpu', padding=5, foreground=colors.cpu_color),
        CPU(format="{load_percent}%", padding=0),
        Spacer(length=12),
        TextBox(text='mem', padding=5, foreground=colors.mem_color),
        Memory(format="{MemUsed:.0f}Mb", padding=0),
        Spacer(length=12),
        TextBox(text='dt', padding=5, foreground=colors.date_color),
        Clock(format="%a %d %b, %H:%M", padding=0, margin_y=0),
        Spacer(length=8),
        systrayWidgetBox,
        Spacer(length=10),
    ],
    23,
)
#: }}}
#: }}}

#: Screens {{{
screens = [
    Screen(top=nebula)
]
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
