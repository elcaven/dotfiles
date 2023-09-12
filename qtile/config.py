# vim:fileencoding=utf-8:ft=python
#: ---------------------------------------------------------------------------------------------------------------
#: Imports
#: ---------------------------------------------------------------------------------------------------------------
import os
import subprocess
import nerdfonts as nf
import shlex

# from typing import List  # noqa: F401

from libqtile import bar, hook
from libqtile.config import (
    Click, Drag, Group, Key, KeyChord, Match,
    ScratchPad, DropDown, Screen)
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.scripts.main import VERSION

# Layout imports
from libqtile.layout.max import Max
from libqtile.layout.floating import Floating
from libqtile.layout.xmonad import MonadTall, MonadWide

# Widget imports
from qtile_extras.widget import (
    Spacer, GroupBox, WindowCount, WindowName, Systray, Sep,
    Chord, GenPollText, WidgetBox, CurrentLayout, LaunchBar
)

from colorschemes import catppuccin as colors
from widgets.mouse_over_clock import MouseOverClock

#: ---------------------------------------------------------------------------------------------------------------
#: Variables
#: ---------------------------------------------------------------------------------------------------------------
mod = "mod4"
alt_key = "mod1"
terminal = "wezterm"
terminal_dropdown = "wezterm --config window_background_opacity=0.8 -e /home/simon/.local/bin/tmux-sessionizer dropdown"
terminal_nu_shell = "wezterm -e nu"
scr_locker = "betterlockscreen -l"
clipboard = "rofi -modi 'clipboard:greenclip print' -show"
screenshot = "flameshot gui"
powermenu = "rofi -show power-menu -modi power-menu:rofi-power-menu"
tmuxmenu = "fd --type d . $HOME | rofi -keep-right -dmenu -i -p TMUX -multi-select | xargs -I {} wezterm start --cwd {} -- /home/simon/.local/bin/tmux-sessionizer {}"

window_resize = "RESIZE"
window_move = "MOVE"
spawn = "SPAWN"

open_dotfiles = "wezterm start --cwd /home/simon/projects/personal/dotfiles -- /usr/bin/nvim"
open_qtile_config = "wezterm start --cwd /home/simon/.config/qtile -- nvim config.py"

#: ---------------------------------------------------------------------------------------------------------------
#: Hooks
#: ---------------------------------------------------------------------------------------------------------------


@hook.subscribe.startup_once
def autostart():
    autostart_script = os.path.expanduser('/home/simon/.config/qtile/scripts/autostart.sh')
    subprocess.Popen([autostart_script])


@hook.subscribe.client_focus
def bring_focused_floating_client_to_front(client):
    if client.floating:
        client.bring_to_front()


@hook.subscribe.client_new
def test(client):
    if client.name == "JetBrains Toolbox":
        client.toggle_floating()
        client.set_position_floating(100, 100)
#: ---------------------------------------------------------------------------------------------------------------
#: Functions
#: ---------------------------------------------------------------------------------------------------------------


@lazy.function
def float_to_front(qtile):
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.cmd_bring_to_front()


@lazy.function
def focus_next_screen(qtile):
    if qtile.current_screen.index == len(qtile.screens) - 1:
        qtile.focus_screen(0)
    else:
        qtile.focus_screen(qtile.current_screen.index + 1)
    win = qtile.current_group.current_window
    if win is not None:
        win.window.warp_pointer(win.width // 2, win.height // 2)


@lazy.function
def tmux_session_finder(qtile):
    tmux_script = os.path.expanduser("/home/simon/.local/bin/tmux-session-finder.sh")
    subprocess.Popen([tmux_script])


def get_notification_status():
    status = subprocess.check_output(
        ['dunstctl', 'is-paused']).decode('utf-8').strip()
    if status == "true":
        return nf.icons["fa_bell_slash"]
    else:
        return nf.icons["fa_bell"]


def toggle_notification_status():
    logger.info("Toggling notification status")
    subprocess.call(['dunstctl', 'set-paused', 'toggle'])

#: ---------------------------------------------------------------------------------------------------------------
#: Key bindings
#: ---------------------------------------------------------------------------------------------------------------
keys = [

    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.group.next_window(), desc="Move focus to next window"),
    Key([mod], "k", lazy.group.prev_window(), desc="Move focus to previous window"),
    Key([mod], "u", lazy.next_urgent()),
    Key([mod, "shift"], "f", float_to_front),
    Key([mod, "control"], "Return", lazy.layout.flip()),

    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod, "shift"], "Return", lazy.spawn(terminal_nu_shell), desc="Launch multiplex terminal"),

    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "space", lazy.window.toggle_floating()),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod, "shift"], "m", lazy.window.toggle_maximize()),
    Key([mod, "control"], "j", focus_next_screen(), desc='Next monitor'),

    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload Qtile config"),
    Key([mod, "control", "shift"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show combi")),
    Key([mod], "q", lazy.spawn(powermenu)),
    Key([mod], "t", tmux_session_finder()),
    Key([mod, "shift"], "h", lazy.spawn(clipboard)),

    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl s 5%-")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl s 5%+")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl -- set-sink-volume 0 +1%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl -- set-sink-volume 0 -1%")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),

    Key([], "Print", lazy.spawn(screenshot)),
    Key([mod, "control"], "l", lazy.spawn(scr_locker)),
    Key([mod], "b", lazy.hide_show_bar("top")),

    # Eww widgets
    Key([mod], "y", lazy.spawn("eww open --toggle dashboard")),
    Key([mod], "c", lazy.spawn("eww open --toggle calendar_popup")),

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
        mode=True,
        name=window_resize
    ),
    KeyChord([mod], "m", [
        Key([], "f", lazy.layout.flip(), desc="Flip layout"),
        Key([], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
        Key([], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
        Key([], "j", lazy.layout.shuffle_down(), desc="Move window down"),
        Key([], "k", lazy.layout.shuffle_up(), desc="Move window up")],
        mode=True,
        name=window_move
    ),
    KeyChord([mod], "s", [
        Key([], "e", lazy.spawn("emacs")),
        Key([], "l", lazy.spawn("wezterm -e nvim")),
        Key([], "m", lazy.spawn("wezterm -e btop")),
        Key([], "j", lazy.spawn("wezterm -e /home/simon/.local/bin/jo")),
        Key([], "c", lazy.spawn("discord")),
        Key([], "q", lazy.spawn(open_qtile_config)),
        Key([], "d", lazy.spawn(open_dotfiles))],
        name=spawn
    ),
]

#: ---------------------------------------------------------------------------------------------------------------
#: Groups
#: ---------------------------------------------------------------------------------------------------------------
groups = [
    Group(name='1', layout='monadtall', matches=[
        Match(wm_class='Vivaldi-stable')]),
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
        Match(title='Microsoft Teams'),
        Match(wm_class='discord')]),
    Group(name='9', layout='max', matches=[
        Match(wm_class="firefox"),
        Match(wm_class="evolution")]),
    Group(name='0', layout='max', matches=[
        Match(wm_class="notion-app"),
        Match(wm_class="notion-app-enhanced"),
        Match(wm_class="openlens")]),
]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(toggle=True),
            desc="Switch to group {}".format(i.name)),
        Key([mod, "shift"], i.name,
            lazy.window.togroup(i.name, switch_group=True),
            desc="Switch to & move focused window to group {}".format(i.name)),
    ])

# Append scratchpad after setting up group keybinds
groups.append(ScratchPad("scratchpad", [
    DropDown("term", terminal_dropdown, opacity=1, height=0.4, x=0, width=0.998, on_focus_lost_hide=True),
    DropDown("insomnia", "insomnia", opacity=1, height=0.997, x=0, width=0.998, on_focus_lost_hide=True),
    DropDown("browser", "qutebrowser", opacity=1, height=0.997, x=0, width=0.998, on_focus_lost_hide=True),
]))

#: ---------------------------------------------------------------------------------------------------------------
#: Widgets
#: ---------------------------------------------------------------------------------------------------------------
widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono ExtraBold",
    fontsize=11,
    padding=3,
    background=colors.background,
)
extension_defaults = widget_defaults.copy()

group_box_settings = {
    "padding": 1,
    "margin_y": 4,
    # "fontsize": 14,
    "borderwidth": 2,
    "center_aligned": True,
    "active": colors.foreground,
    "inactive": colors.groupbox_inactive,
    "hide_unused": False,
    "disable_drag": True,
    "rounded": False,
    "highlight_color": colors.highlight_color,
    "block_highlight_text_color": colors.block_highlight_text_color,
    "highlight_method": "block",
    "urgent_alert_method": "text",
    "urgent_text": colors.groupbox_urgent,
    "this_current_screen_border": colors.groupbox_current_screen_border,
    "this_screen_border": colors.groupbox_screen_border,
    "other_current_screen_border": colors.groupbox_other_current_screen_border,
    "other_screen_border": colors.groupbox_other_screen_border,
    "foreground": colors.foreground,
    "background": colors.background,
    "urgent_border": colors.groupbox_urgent,
    "spacing": 2,
    "visible_groups": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "font": "JetBrainsMono Nerd Font Mono Bold"
}

chordWidget = Chord(
    font="JetBrainsMonoExtraBold Nerd Font Mono Bold",
    fontsize=11,
    background=colors.pink,
    margin=0, padding=0, fmt="  {}  ",
    chords_colors={
        '': (colors.background, colors.background),
        window_resize: (colors.window_resize_chord_color, colors.background),
        window_move: (colors.window_move_chord_color, colors.background),
        spawn: (colors.spawn_chord_color, colors.background),
    },
)

doNotDisturbIcon = GenPollText(
    func=get_notification_status,
    update_interval=0.1,
    foreground=colors.foreground,
    background=colors.background,
    mouse_callbacks={"Button1": toggle_notification_status},
    fontsize=21, padding=2, margin=0)

systrayWidgetBox = WidgetBox(
    widgets=[
        Systray(
            background=colors.alternate_background,
            icon_size=16,
            padding=5,
            fontsize=2,
        ),
        Spacer(
            length=6,
            background=colors.alternate_background
        )
    ],
    # font="JetBrainsMono Nerd Font Mono ExtraBold", fontsize=11,
    close_button_location="right",
    background=colors.alternate_background,
    # text_open=nf.icons["fa_angle_right"],
    # text_closed=nf.icons["fa_angle_left"],
    text_open="[-]",
    text_closed="[+]")

launchbar = LaunchBar(
    padding=2, padding_y=1,
    text_only=True,
    font="Font Awesome 6 Free", fontsize=14,
    foreground=colors.foreground, progs=[
        ("", clipboard, "Clipboard History"),
        ("", screenshot, "Screenshot"),
    ])

# separator = TextBox(fmt="::", foreground=colors.sep_color)
separator = Sep(
    foreground=colors.foreground,
    padding=7,
    size_percent=100,
)

#: ---------------------------------------------------------------------------------------------------------------
#: Bars
#: ---------------------------------------------------------------------------------------------------------------
default_bar = bar.Bar(
    [
        chordWidget,
        Spacer(length=3),
        GroupBox(**group_box_settings),
        Spacer(length=5),
        # separator,
        CurrentLayout(foreground=colors.widget_current_layout),
        WindowCount(
            text_format="[{num}]",
            background=colors.background,
            foreground=colors.widget_window_count,
        ),
        # separator,
        Spacer(length=3),
        Spacer(length=3, background=colors.alternate_background),
        WindowName(
            background=colors.alternate_background,
            foreground=colors.window_title_color,
            width=bar.CALCULATED,
            empty_group_string="",
            max_chars=150,
        ),
        Spacer(background=colors.alternate_background),
        systrayWidgetBox,
        Spacer(length=3, background=colors.alternate_background),
        Spacer(length=8),
        # separator,
        MouseOverClock(
            long_format="%a, %b %d - %H:%M",
            background=colors.background,
            foreground=colors.foreground,
            mouse_callbacks={"Button1": lazy.spawn("eww open --toggle calendar_popup")},
        ),
        # separator,
        Spacer(length=5),
        launchbar,
        # Spacer(length=5),
        doNotDisturbIcon,
        Spacer(length=5),
        # chordWidget,
    ],
    size=24,
)
default_bar_second_monitor = bar.Bar(
    [
        chordWidget,
        Spacer(length=3),
        GroupBox(**group_box_settings),
        Spacer(length=5),
        # separator,
        CurrentLayout(foreground=colors.widget_current_layout),
        WindowCount(
            text_format="[{num}]",
            background=colors.background,
            foreground=colors.widget_window_count,
        ),
        # separator,
        Spacer(length=3),
        Spacer(length=3, background=colors.alternate_background),
        WindowName(
            background=colors.alternate_background,
            foreground=colors.window_title_color,
            width=bar.CALCULATED,
            empty_group_string="",
            max_chars=150,
        ),
        Spacer(background=colors.alternate_background),
        Spacer(length=8),
        # separator,
        MouseOverClock(
            long_format="%a, %b %d - %H:%M",
            background=colors.background,
            foreground=colors.foreground,
            mouse_callbacks={"Button1": lazy.spawn("eww open --toggle calendar_popup")},
        ),
        Spacer(length=5),
    ],
    size=24
)

#: ---------------------------------------------------------------------------------------------------------------
#: Screens
#: ---------------------------------------------------------------------------------------------------------------
screen_count = len(subprocess.check_output(shlex.split("xrandr --listmonitors")).splitlines()) - 1
screens = []
if screen_count == 1:
    screens.append(Screen(
        top=default_bar
    ))
else:
    for i in range(screen_count):
        if i == screen_count - 1:
            screens.append(Screen(
                top=default_bar_second_monitor
            ))
        else:
            screens.append(Screen(
                top=default_bar
            ))

# screens = [
#     Screen(top=default_bar)
# ]

#: ---------------------------------------------------------------------------------------------------------------
#: Layouts
#: ---------------------------------------------------------------------------------------------------------------
margin = 0
border_width = 1
single_border_width = 0

layout_border = dict(
    border_width=border_width,
    border_focus=colors.border_focus,
    border_normal=colors.border_normal,
)

floating_layout_border = dict(
    border_width=border_width,
    border_focus=colors.border_focus_floating,
    border_normal=colors.border_normal,
)

layout_theme = {
    **layout_border,
    "margin": margin,
}

layouts = [
    Max(border_width=single_border_width, margin=margin,
        border_focus=colors.border_focus, border_normal=colors.border_normal),
    MonadTall(**layout_theme, single_border_width=single_border_width,
              single_margin=margin, ratio=0.6),
    MonadWide(**layout_theme, single_border_width=single_border_width,
              single_margin=margin, ratio=0.6),
]

floating_layout = Floating(
    **floating_layout_border,
    float_rules=[
        *Floating.default_float_rules,
        Match(func=lambda c: c.is_transient_for()),
    ])

#: ---------------------------------------------------------------------------------------------------------------
#: Configurations
#: ---------------------------------------------------------------------------------------------------------------
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
wmname = f"Qtile {VERSION}"
