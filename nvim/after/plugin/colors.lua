require("catppuccin").setup({
    flavour = "mocha", -- latte, frappe, macchiato, mocha
    transparent_background = true,
    styles = {
        comments = "NONE",
        functions = "bold",
        keywords = "bold",
        strings = "NONE",
        variables = "bold"
    }
})

vim.cmd("colorscheme catppuccin")
