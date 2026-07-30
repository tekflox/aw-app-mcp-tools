export function createClient({ apiUrl, fetchImpl = fetch }) {
  async function status() {
    const res = await fetchImpl(apiUrl('/status'));
    if (!res.ok) throw new Error(`GET /status -> ${res.status}`);
    return res.json();
  }

  async function mcpConfig() {
    const res = await fetchImpl(apiUrl('/mcp.json'));
    if (!res.ok) throw new Error(`GET /mcp.json -> ${res.status}`);
    return res.json();
  }

  return { status, mcpConfig };
}
