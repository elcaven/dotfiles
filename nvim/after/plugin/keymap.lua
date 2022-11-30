local Remap = require("elcaven.keymap")
local nnoremap = Remap.nnoremap
local vnoremap = Remap.vnoremap
local inoremap = Remap.inoremap
local xnoremap = Remap.xnoremap
local nmap = Remap.nmap

-- which-key
require("which-key").setup{}

-- Telescope
local builtin = require('telescope.builtin')
nnoremap("<leader>ff", function ()
   builtin.find_files()
end, {desc='Telescope: find files'})

nnoremap("<leader>fg", function ()
   builtin.live_grep()
end, {desc='Telescope: live grep'})

nnoremap("<leader>fb", function ()
   builtin.buffers()
end, {desc='Telescope: find buffer'})

nnoremap("<leader>fh", function ()
   builtin.live_grep()
end, {desc='Telescope: help tags'})

-- Netrw
nnoremap("<leader>dd", ":Ex<CR>", {desc='Open explore'})

-- Other
nnoremap("<C-d>", "<C-d>zz")
nnoremap("<C-u>", "<C-u>zz")
vnoremap("<C-c>", "*y")

vnoremap("J", ":m '>+1<CR>gv=gv")
vnoremap("K", ":m '<-2<CR>gv=gv")
