---@type ChadrcConfig
local M = {}

-- Path to overriding theme and highlights files
local highlights = require "custom.highlights"

M.ui = {
  theme = "catppuccin",
  theme_toggle = { "catppuccin", "rosepine" },
  transparency = true,

  hl_override = highlights.override,
  hl_add = highlights.add,

  statusline = {
    theme = "minimal",
    separator_style = "default",
  },

  tabufline = {
    enabled = true,
  },
  nvdash = {
    load_on_startup = true,
  },
}

M.plugins = "custom.plugins"
M.mappings = require "custom.mappings"

return M
