-- which-key
require("which-key").setup{}

-- Telescope
local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', builtin.find_files, {desc='Telescope: find files'})
vim.keymap.set('n', '<leader>fg', builtin.live_grep, {desc='Telescope: live grep'})
vim.keymap.set('n', '<leader>fb', builtin.buffers, {desc='Telescope: find buffer'})
vim.keymap.set('n', '<leader>fh', builtin.help_tags, {desc='Telescope: help tags'})

-- Netrw
vim.keymap.set('n', '<leader>dd', ":Lexplore %:p:h<CR>", {})
vim.keymap.set('n', '<leader>da', ":Ex<CR>", {})
