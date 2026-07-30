import { createClient } from './client.js';

const SLUG = 'mcp-tools';

export function register(host) {
  const client = createClient({
    apiUrl: (sub) => `/api/apps/${SLUG}${sub}`,
    fetchImpl: (path, init) => host.sdk.api.fetch(path, init),
  });

  function McpToolsNavPill() {
    const [label, setLabel] = host.React.useState('MCP tools');
    host.React.useEffect(() => {
      client.status()
        .then((r) => setLabel(`${r.tools.length} MCP tools`))
        .catch(() => setLabel('MCP tools'));
    }, []);
    return host.h('span', { title: 'Playwright MCP tools installed by aw-app-mcp-tools' }, label);
  }

  host.registerSlot('core.nav', McpToolsNavPill);
}

export default register;
