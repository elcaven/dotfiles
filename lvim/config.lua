--[[
lvim is the global options object

Linters should be
filled in as strings with either
a global executable or a path to
an executable
]]

-- general
lvim.log.level = "warn"
lvim.format_on_save = false
lvim.colorscheme = "catppuccin"
lvim.transparent_window = true

vim.opt.relativenumber = true

-- keymappings [view all the defaults by pressing <leader>Lk]
lvim.leader = "space"
lvim.keys.normal_mode["<C-s>"] = ":w<cr>"

lvim.builtin.dashboard.active = true
lvim.builtin.notify.active = true
lvim.builtin.terminal.active = true
lvim.builtin.nvimtree.setup.view.side = "left"
lvim.builtin.nvimtree.show_icons.git = 0

-- if you don't want all the parsers change this to a table of the ones you want
lvim.builtin.treesitter.ensure_installed = {
  "bash",
  "c",
  "javascript",
  "json",
  "lua",
  "python",
  "typescript",
  "css",
  "rust",
  "java",
  "yaml",
}

lvim.builtin.treesitter.ignore_install = { "haskell" }
lvim.builtin.treesitter.highlight.enabled = true

-- Settings for catppuccin theme
local catppuccin = require('catppuccin')
catppuccin.setup({
  styles = {
   comments = "NONE",
   functions = "bold",
   keywords = "bold",
   strings = "NONE",
   variables = "bold",
  }
})

-- Additional Plugins
lvim.plugins = {
  { 'Mofiqul/dracula.nvim' },
  { 'khaveesh/vim-fish-syntax' },
  { 'catppuccin/nvim', as = 'catppuccin' },
  { 'elkowar/yuck.vim'}
}

-- lua lsp setup
local opts = {
  settings = {
    Lua = {
      diagnostics = {
        globals = { 'awesome', 'tag', 'screen', 'client' }
      }
    }
  }
}
require("lvim.lsp.manager").setup("sumneko_lua", opts)
