local cmp = require'cmp'

local remap = require("elcaven.keymap")
local nnoremap = remap.nnoremap
local inoremap = remap.inoremap

cmp.setup({
    snippet = {
        expand = function(args)
            require('luasnip').lsp_expand(args.body)
        end,
    },
    mapping = cmp.mapping.preset.insert({
        ['<C-b>'] = cmp.mapping.scroll_docs(-4),
        ['<C-f>'] = cmp.mapping.scroll_docs(4),
        ['<C-Space>'] = cmp.mapping.complete(),
        ['<C-e>'] = cmp.mapping.abort(),
        ['<CR>'] = cmp.mapping.confirm({ select = true }),
    }),
    sources = cmp.config.sources({
        { name = 'nvim_lsp' },
        { name = 'luasnip' },
    }, {
        { name = 'buffer' },
    })
})

local capabilities = require('cmp_nvim_lsp').default_capabilities(vim.lsp.protocol.make_client_capabilities())
local function config(_config)
	return vim.tbl_deep_extend("force", {
		on_attach = function()
			nnoremap("gd", function() vim.lsp.buf.definition() end)
			nnoremap("K", function() vim.lsp.buf.hover() end)
			nnoremap("<leader>vws", function() vim.lsp.buf.workspace_symbol() end)
			nnoremap("<leader>vd", function() vim.diagnostic.open_float() end)
			nnoremap("[d", function() vim.diagnostic.goto_next() end)
			nnoremap("]d", function() vim.diagnostic.goto_prev() end)
			nnoremap("<leader>vca", function() vim.lsp.buf.code_action() end)
			nnoremap("<leader>vco", function() vim.lsp.buf.code_action({
                filter = function(code_action)
                    if not code_action or not code_action.data then
                        return false
                    end

                    local data = code_action.data.id
                    return string.sub(data, #data - 1, #data) == ":0"
                end,
                apply = true
            }) end)
			nnoremap("<leader>vrr", function() vim.lsp.buf.references() end)
			nnoremap("<leader>vrn", function() vim.lsp.buf.rename() end)
			inoremap("<C-h>", function() vim.lsp.buf.signature_help() end)
		end,
	}, _config or {})
end

require('lspconfig')['pyright'].setup(config({
    config(),
    capabilities = capabilities
}))

require('lspconfig')['sumneko_lua'].setup(config({
    capabilities = capabilities,
    settings = {
        Lua = {
            diagnostics = {
                globals = {'vim'}
            }
        }
    }
}))

require('lspconfig')['rust_analyzer'].setup(config({
    capabilities = capabilities
}))

require('lspconfig')['gopls'].setup(config({
    cmd = { "gopls", "serve" },
    filetypes = { "go", "gomod" },
    capabilities = capabilities
}))

require('lspconfig')['bashls'].setup(config({
    capabilities = capabilities
}))
