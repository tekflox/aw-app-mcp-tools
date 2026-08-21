---
repo: architecture
path: docs/architecture/aw-app-mcp-tools.md
source: generated
edited: false
checksum: sha256:fbfe3d0c66c2d136c8907818cf0f3170d721c1395be6c93c6a567e10d7acc052
---
# MCP Tools

- **repo**: aw-app-mcp-tools
- **layer**: app
- **technologies**: python, react
- **health** (derived): planned

Installs MCP helper tools for Agentic Workspace, starting with a ready-to-use Playwright MCP config for shared browser automation.

## Connections
- `http` → **aw-workspace** — routes mounted at /api/apps/mcp-tools

## MCP tools
_none exposed_

## Requirements
### Chave ausente cai no padrão, objeto vazio explícito é respeitado
- Given no momento do activate a config ainda não passou pela camada que aplica defaults, então uma instalação nova chega como {}
- When a lista de servidores é montada (repos/aw-app-mcp-tools/mcp_tools_app/plugin.py::build_mcp_servers:30)
- Then config sem a chave mcpServers cai em DEFAULT_MCP_SERVERS (plugin.py:20) e um {} explícito devolve nenhum servidor — distinguir "não disse nada" de "disse que não quero nada" é o ponto: sem a distinção, ou a primeira instalação sobe sem tool nenhuma, ou quem apagou todos os servidores vê o playwright reaparecer sozinho a cada boot, e o segundo caso é pior porque não há como desfazer
- intended_status: `not_implemented` · derived health: `not_implemented`
- tests: `repos/aw-app-mcp-tools/tests/test_plugin.py` (passing)

### A config do usuário é repassada literalmente, e pode acrescentar servidor arbitrário
- Given alguém quer registrar um servidor MCP próprio ao lado do playwright que vem de fábrica
- When a config é lida e repassada (repos/aw-app-mcp-tools/mcp_tools_app/plugin.py::build_mcp_servers:30, verificado por tests/test_plugin.py::test_build_mcp_servers_lets_user_add_an_arbitrary_tool:42)
- Then o conteúdo sai verbatim, com as entradas próprias e as adicionadas convivendo — o app não valida nem reescreve o que a pessoa declarou, o que a torna dona da própria lista. O custo é assumido: uma entrada malformada chega inteira ao gateway e falha lá, e não aqui, onde a mensagem de erro seria mais próxima de quem escreveu
- intended_status: `not_implemented` · derived health: `not_implemented`
- tests: `repos/aw-app-mcp-tools/tests/test_plugin.py` (passing)

### O activate escreve o mcp.json no diretório do pacote, e nunca sem playwright numa instalação nova
- Given as tools só aparecem no gateway se este app escrever o próprio mcp.json — declarar contributes.mcp não registra upstream nenhum
- When a ativação materializa o arquivo (repos/aw-app-mcp-tools/mcp_tools_app/plugin.py::write_mcp_json:46, via tests/test_plugin.py::test_activate_writes_mcp_json_from_config:73)
- Then o mcp.json é gravado no package_dir a partir da config vigente, e uma instalação com config vazia ainda assim entrega o playwright (test_activate_with_fresh_empty_config_still_ships_playwright:81) — sem essa escrita o app instala, aparece na lista, reporta saudável, e o gateway serve zero tools dele, que é a forma de falha mais silenciosa que esta casa tem
- intended_status: `not_implemented` · derived health: `not_implemented`
- tests: `repos/aw-app-mcp-tools/tests/test_plugin.py` (passing)

### O playwright padrão aponta para o container de browser compartilhado, com versão fixada
- Given o servidor MCP do playwright precisa de um browser para pilotar, e este workspace já roda um no container aw-app-browser
- When a entrada padrão é definida (repos/aw-app-mcp-tools/mcp_tools_app/plugin.py:20-25, com DEFAULT_CDP_ENDPOINT:12)
- Then o comando traz --cdp-endpoint http://aw-app-browser:9223 e o pacote é fixado em @playwright/mcp@0.0.77 — apontar para o container compartilhado é o que faz o browser que a pessoa vê ser o mesmo que o agente pilota, em vez de subir um chromium invisível ao lado. A versão fixada existe porque `-y` com versão flutuante muda a superfície de tools sem ninguém ter mexido em nada
- intended_status: `not_implemented` · derived health: `not_implemented`
- tests: `repos/aw-app-mcp-tools/tests/test_installer.py` (passing)
