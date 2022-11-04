require("telescope").setup({
    defaults = {
        selection_strategy = "reset",
        sorting_strategy = "ascending",
        prompt_prefix = " > ",
        layout_strategy = "horizontal",
        layout_config = {
            horizontal = {
                prompt_position = "top",
                preview_width = 0.55,
                results_width = 0.8,
            },
            vertical = {
                mirror = false,
            },
            width = 0.87,
            height = 0.80,
            preview_cutoff = 120,
        }
    }
})

-- Telescope theming
local colors = require("catppuccin.palettes").get_palette()
local TelescopeColor = {
	TelescopeMatching = { fg = colors.flamingo },
	TelescopeSelection = { fg = colors.text, bg = colors.surface0, bold = true },

	TelescopePromptPrefix = { bg = colors.mantle },
	TelescopePromptNormal = { bg = colors.mantle },
	TelescopeResultsNormal = { bg = colors.mantle },
	TelescopePreviewNormal = { bg = colors.mantle },
	TelescopePromptBorder = { bg = colors.mantle, fg = colors.lavender },
	TelescopeResultsBorder = { bg = colors.mantle, fg = colors.lavender },
	TelescopePreviewBorder = { bg = colors.mantle, fg = colors.green },
	TelescopePromptTitle = { bg = colors.lavender, fg = colors.mantle },
	TelescopeResultsTitle = { fg = colors.mantle },
	TelescopePreviewTitle = { bg = colors.green, fg = colors.mantle },
}

for hl, col in pairs(TelescopeColor) do
	vim.api.nvim_set_hl(0, hl, col)
end
