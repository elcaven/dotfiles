####################################################################################################
# Imports
####################################################################################################
import os
import subprocess

from typing import List  # noqa: F401

from libqtile import bar, layout, hook, qtile
from qtile_extras import widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.log_utils import logger

from colorschemes import deep_ocean as colors
from qtile_extras.widget.decorations import RectDecoration


####################################################################################################
# Hooks
####################################################################################################
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('/home/simon/.config/qtile/autostart.sh')
    subprocess.call([home])


@hook.subscribe.screen_change
def screen_change(event):
    home = os.path.expanduser('/home/simon/.config/qtile/scripts/screen_change.sh')
    subprocess.call([home])


####################################################################################################
# Functions
####################################################################################################
@lazy.function
def float_to_front(qtile):
    logger.info("Bring floating windows to front")
    for group in qtile.groups:
        for window in group.windows:
            if window.floating:
                window.cmd_bring_to_front()

####################################################################################################
# Key bindings
####################################################################################################
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

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show combi")),
    Key([mod], "p", lazy.spawn("dmenu_run")),
    Key([mod], "q", lazy.spawn("rofi -show power-menu -modi power-menu:rofi-power-menu -lines 6")),

    Key([], "XF86MonBrightnessDown", lazy.spawn("sudo ybacklight -dec 1")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("sudo ybacklight -inc 1")),

    Key([], "Print", lazy.spawn("flameshot gui")),
    Key([mod], "d", lazy.spawn("emacs")),
    Key([mod], "a", lazy.spawn("emacs /home/simon/projects/personal/dotfiles")),
    Key([mod], "e", lazy.spawn("kitty -e ranger")),
    Key([mod], "z", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], "p", lazy.group['scratchpad'].dropdown_toggle('insomnia')),
    # Key([mod], "n", lazy.group['scratchpad'].dropdown_toggle('boostnote')),
    # Key([mod], "b", lazy.group['scratchpad'].dropdown_toggle('browser')),
    Key([alt_key], "l", lazy.spawn(scr_locker)),
    Key([mod], "b", lazy.hide_show_bar("top")),
    # Key(["control", "shift"], "h", lazy.spawn("/home/simon/.local/bin/clipmenu-rofi"))

    # Dunst
    Key(["control"], "space", lazy.spawn("dunstctl close")),
    Key(["control", "shift"], "space", lazy.spawn("dunstctl close-all"))
]

####################################################################################################
# Groups
####################################################################################################
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
        Match(wm_class='hexchat'),
        Match(wm_class='discord')]),
    Group(name='9', layout='max', matches=[Match(wm_class="evolution")]),
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
    #DropDown("boostnote", "boostnote", opacity=1, height=0.997, x=0, width=0.998, on_focus_lost_hide=True),
]))

####################################################################################################
# Theming
####################################################################################################


layout_border = dict(
    border_width=2,
    border_focus=colors.border_focus,
    border_normal=colors.border_normal,
)

layout_theme = {
    **layout_border,
    "margin": 5,
}

####################################################################################################
# Layouts
####################################################################################################
layouts = [
    layout.Max(**layout_theme),
    layout.MonadTall(**layout_theme, single_border_width=0, single_margin=0, ratio=0.6),
    layout.MonadWide(**layout_theme, single_border_width=0, single_margin=0, ratio=0.6),
]

####################################################################################################
# Bar
####################################################################################################
widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono Bold", fontsize=11, background=colors.background
)
extension_defaults = widget_defaults.copy()

delimiter_widget = widget.Sep(
    padding=10,
    linewidth=2,
    size_percent=70,
    foreground=colors.alternate_foreground
)
decor = {
    "decorations": [
        RectDecoration(colour=colors.alternate_background, radius=3, filled=True, padding=4, margin=5)
    ]
}

rectDecorationBar = bar.Bar(
    [
        widget.Spacer(length=3),
        widget.GroupBox(**decor,
            spacing=4, padding=2, margin_x=7,
            highlight_method="block",
            borderwidth=1,
            urgent_alert_method="text",
            urgent_text=colors.groupbox_urgent,
            block_highlight_text_color=colors.block_highlight_text_color,
            this_current_screen_border=colors.groupbox_current_screen_border,
            this_screen_border=colors.groupbox_screen_border,
            other_screen_border=colors.groupbox_other_screen_border,
            other_current_screen_border=colors.groupbox_other_current_screen_border,
            highlight_color=colors.highlight_color,
            inactive=colors.groupbox_inactive,
            disable_drag=True,
            hide_unused=False,
            font="JuliaMono SemiBold"
        ),
        widget.CurrentLayout(**decor, padding=10, foreground=colors.widget_current_layout),
        widget.Spacer(length=3),
        widget.WindowCount(fmt="[{}]", padding=0, foreground=colors.widget_window_count),
        widget.WindowName(),
        widget.Spacer(length=3),
        widget.CPU(**decor, format="cpu:{load_percent}%", padding=10, foreground=colors.cpu_color),
        widget.Memory(**decor, format="mem:{MemUsed:.0f}Mb", padding=10, foreground=colors.mem_color),
        widget.Clock(**decor, format="%a %d %b, %H:%M", padding=10, foreground=colors.date_color),
        widget.Spacer(length=3),
        widget.Systray(padding=2, padding_x=5, background=colors.background),
        widget.Spacer(length=5),
    ],
    27
)

simpleBar = bar.Bar(
    [
        widget.Spacer(length=5),
        widget.GroupBox(
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
        widget.Spacer(length=5),
        widget.WindowCount(fmt="[{}]", padding=0, foreground=colors.widget_current_layout),
        widget.CurrentLayout(fmt="[{}]", padding=0, foreground=colors.widget_window_count),
        widget.Spacer(length=3),
        widget.WindowName(for_current_screen=True),
        widget.Spacer(length=8),
        #delimiter_widget,
        widget.CPU(format="cpu:{load_percent}%", padding=8, foreground=colors.cpu_color),
        #delimiter_widget,
        widget.Memory(format="mem:{MemUsed:.0f}Mb", padding=8, foreground=colors.mem_color),
        #delimiter_widget,
        widget.Clock(format="%a %d %b, %H:%M", padding=8, foreground=colors.date_color),
        widget.Spacer(length=3),
        #delimiter_widget,
        widget.Systray(padding=2, background=colors.background),
        widget.Spacer(length=10),
    ],
    23,
)

screens = [
    Screen(top=simpleBar)
]


####################################################################################################
# Configurations
####################################################################################################
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
floating_layout = layout.Floating(
    **layout_border,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
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

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
