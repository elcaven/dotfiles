local wezterm = require("wezterm")

------------------------------------------------------------------------------------
-- Initialize
------------------------------------------------------------------------------------
local config = {}
if wezterm.config_builder then
	config = wezterm.config_builder()
end

------------------------------------------------------------------------------------
-- Color scheme
------------------------------------------------------------------------------------
local custom_color_scheme = wezterm.color.get_builtin_schemes()["Catppuccin Mocha"]
custom_color_scheme.background = "#161320"
custom_color_scheme.foreground = "#ffffff"
config.color_schemes = {
	["CustomCatppuccin"] = custom_color_scheme,
}
config.color_scheme = "CustomCatppuccin"

------------------------------------------------------------------------------------
-- Fonts
------------------------------------------------------------------------------------
local font = wezterm.font {
  family = "Iosevka NFM",
  weight = "Regular",
  stretch = "Normal",
  harfbuzz_features = { 'calt=0', 'clig=0', 'liga=0' },
}
config.font_size = 10
-- config.font = wezterm.font {
--   family = "JetBrainsMono NFM",
--   weight = "Regular",
--   stretch = "Normal",
--   harfbuzz_features = { 'calt=0', 'clig=0', 'liga=0' },
-- }
config.font = font

------------------------------------------------------------------------------------
-- Tab bar settings
------------------------------------------------------------------------------------
config.hide_tab_bar_if_only_one_tab = true
config.window_frame = {
  font = font,
	font_size = 9.0,
	active_titlebar_bg = "#161320",
}

------------------------------------------------------------------------------------
-- General settings
------------------------------------------------------------------------------------
-- config.window_background_opacity = 1
config.window_background_opacity = 0.9

config.window_close_confirmation = "NeverPrompt"
config.default_cursor_style = "SteadyBlock"

config.window_padding = {
	left = 10,
	right = 10,
	top = 10,
	bottom = 10,
}

return config
