# RDA Cooling Lab for Codex and Claude Code

Build cooling models, run simulations and Python analyses, and explore results in linked 3D views and charts with the Red Dot AI hosted service.

## Install

Anyone may install; service access requires an authorized Casdoor account. See [installation and sign-in](plugins/diffliquidtwin/GETTING_STARTED.md).

**Codex:** add [RDA-SG/diffliquidtwin-plugins](https://github.com/RDA-SG/diffliquidtwin-plugins) as a marketplace in Codex and install **RDA Cooling Lab**, then complete Casdoor sign-in.

**Claude Code:**

```
/plugin marketplace add RDA-SG/diffliquidtwin-plugins
/plugin install diffliquidtwin@rda-cooling-lab
```

Then run `/mcp`, select the `diffliquidtwin` server and complete Casdoor sign-in in the browser. The CLI equivalents are `claude plugin marketplace add RDA-SG/diffliquidtwin-plugins` and `claude plugin install diffliquidtwin@rda-cooling-lab`.

Ask the assistant to open RDA Cooling Lab. Modeling instructions stay in the conversation. Resume an existing experiment using its session ID.

## Connection

The marketplace is `rda-cooling-lab` in both hosts; the plugin and MCP server name are `diffliquidtwin`. The remote endpoint is `https://diffliquidtwin-mcp.demo.rda.ai/mcp`.

The plugin contains skills, display assets and a remote HTTP MCP configuration. No local Python, Node or simulation backend is required. Casdoor OAuth credentials are managed by the host and never distributed in this repository. Authorized users currently share team workspaces.

The Platform supplies the viewer, tools, simulations and stored results. Inspect returned model assumptions, solver settings and result provenance when interpreting simulations.

One package directory serves both hosts. Codex reads `.codex-plugin/plugin.json`; Claude Code reads `.claude-plugin/plugin.json`. Both manifests reference the same `.mcp.json`, skill and assets, and keep the same name and version.

The interactive 3D panel is an MCP App served by the Platform. It displays only in hosts that render MCP Apps. Claude Code does not currently document MCP App rendering, so in Claude Code the tools, simulations and saved results work without the panel.

## Development

The root `.agents/plugins/marketplace.json` is the primary Codex marketplace entry. The nested `plugins/.agents/plugins/marketplace.json` supports local Codex marketplace registration. Do not register both sources with the same marketplace name.

The root `.claude-plugin/marketplace.json` is the Claude Code marketplace entry; its `diffliquidtwin` entry points at the same `plugins/diffliquidtwin` directory. For a local checkout, use `claude plugin marketplace add <path-to-checkout>`.

Run `python -m pytest tests` and `node --test tests/test_plugin_listing.mjs`. The tests check package paths and manifest parity between hosts. They also exercise the installed Codex plugin loader and run `claude plugin validate --strict` on the plugin and marketplace. Each native check is skipped when its CLI is absent.
