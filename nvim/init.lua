require('core.plugin')
require('core.lsp')
require('user.keybindings')
require('user.evil_lualine')

-- General settings
vim.notify = require('notify')
vim.wo.relativenumber = true

-- Colorscheme
local catppuccin = require('catppuccin')
catppuccin.setup({
		transparent_background = true,
		styles = {
			comments = "NONE",
			functions = "bold",
			keywords = "bold",
			strings = "NONE",
			variables = "bold",
		}
})
vim.g.catppuccin_flavour = "frappe"
vim.cmd[[colorscheme catppuccin]]

-- Treesitter
local configs = require'nvim-treesitter.configs'

configs.setup {
	highlight = {
		enable = true,
	}
}

-- Status bar
--require("feline").setup({
--	components = require('catppuccin.core.integrations.feline'),
--})
