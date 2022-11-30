return require('packer').startup(function(use)
	use 'wbthomason/packer.nvim'

    use 'nvim-lua/plenary.nvim'
    use 'nvim-lua/popup.nvim'
    use 'nvim-telescope/telescope.nvim'

    use 'neovim/nvim-lspconfig'
    use 'folke/which-key.nvim'

    use 'ThePrimeagen/vim-be-good'

	use 'catppuccin/nvim'

    use 'hrsh7th/cmp-nvim-lsp'
    use 'hrsh7th/cmp-buffer'
    use 'hrsh7th/cmp-path'
    use 'Hrsh7th/cmp-cmdline'
    use 'hrsh7th/nvim-cmp'

    use 'norcalli/nvim-colorizer.lua'

    use 'L3MON4D3/LuaSnip'
    use 'saadparwaiz1/cmp_luasnip'

    use 'rust-lang/rust.vim'

    use {
        'nvim-lualine/lualine.nvim',
        requires = { 'kyazdani42/nvim-web-devicons', opt = true }
    }
    use("nvim-treesitter/nvim-treesitter", {
        run = ":TSUpdate"
    })
end)
