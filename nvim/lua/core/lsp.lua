local lspconfig = require'lspconfig'
local completion = require'completion'

local function custom_on_attach(client)
	print('Attaching to ' .. client.name)
	completion.on_attach(client)
end

local default_config = {
	on_attach = custom_on_attach,
}

-- setup language servers here
--lspconfig.tsserver.setup(default_config)
lspconfig.pyright.setup({})
lspconfig.sumneko_lua.setup({})
