return require('packer').startup(function(use)
	use 'wbthomason/packer.nvim'
   
    use("nvim-lua/plenary.nvim")
    use("nvim-lua/popup.nvim")
    use("nvim-telescope/telescope.nvim")

    use 'neovim/nvim-lspconfig'

	use 'catppuccin/nvim'

    use {
        'nvim-lualine/lualine.nvim',
        requires = { 'kyazdani42/nvim-web-devicons', opt = true }
    }
end)
