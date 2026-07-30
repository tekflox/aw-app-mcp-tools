function c({ apiUrl: s, fetchImpl: n = fetch }) {
  async function e() {
    const t = await n(s("/status"));
    if (!t.ok) throw new Error(`GET /status -> ${t.status}`);
    return t.json();
  }
  async function o() {
    const t = await n(s("/mcp.json"));
    if (!t.ok) throw new Error(`GET /mcp.json -> ${t.status}`);
    return t.json();
  }
  return { status: e, mcpConfig: o };
}
const r = "mcp-tools";
function l(s) {
  const n = c({
    apiUrl: (o) => `/api/apps/${r}${o}`,
    fetchImpl: (o, t) => s.sdk.api.fetch(o, t)
  });
  function e() {
    const [o, t] = s.React.useState("MCP tools");
    return s.React.useEffect(() => {
      n.status().then((a) => t(`${a.tools.length} MCP tools`)).catch(() => t("MCP tools"));
    }, []), s.h("span", { title: "Playwright MCP tools installed by aw-app-mcp-tools" }, o);
  }
  s.registerSlot("core.nav", e);
}
export {
  l as default,
  l as register
};
