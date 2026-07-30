import { createClient } from './client.js';

const SLUG = 'mcp-tools';

const client = createClient({
  apiUrl: (sub) => `/api/apps/${SLUG}${sub}`,
});

async function main() {
  const output = document.getElementById('output');
  const status = document.getElementById('status');

  const body = await client.status();
  output.textContent = JSON.stringify(body.config, null, 2);
  status.textContent = `${body.tools.length} MCP tools ready`;
}

main().catch((e) => {
  document.getElementById('status').textContent = `error: ${e.message}`;
});
