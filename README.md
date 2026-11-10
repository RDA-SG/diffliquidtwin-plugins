# RDA Cooling Lab for Codex

Build cooling models, run simulations and Python analyses, and explore results in linked 3D views and charts with the Red Dot AI hosted service.

## Install

Add [RDA-SG/diffliquidtwin-plugins](https://github.com/RDA-SG/diffliquidtwin-plugins) as a marketplace in Codex and install **RDA Cooling Lab**. Complete Casdoor sign-in with an authorized account. Anyone may install; service access requires authorization. See [installation and sign-in](plugins/diffliquidtwin/GETTING_STARTED.md).

Ask Codex to open RDA Cooling Lab. Modeling instructions stay in the conversation. Resume an existing experiment using its session ID.

## Connection

The marketplace is `rda-cooling-lab`; the plugin and MCP namespace are `diffliquidtwin`. The remote endpoint is `https://diffliquidtwin-mcp.demo.rda.ai/mcp`.

The plugin contains skills, display assets and a remote HTTP MCP configuration. No local Python, Node or simulation backend is required. Casdoor OAuth credentials are managed by the host and never distributed in this repository. Authorized users currently share team workspaces.

The Platform supplies the viewer, tools, simulations and stored results. Inspect returned model assumptions, solver settings and result provenance when interpreting simulations.

Only the Codex package is currently provided. A future Claude Code package can share this repository while using its own manifest and marketplace entry.

New experiments use the service's automatic Engine method selection. An automatic thermal-step limit is JSON `null`; positive caps and explicit methods remain available. Read saved execution evidence for actual methods, fallbacks and tolerance scope. The plugin supplies no solver or frontend bundle.

## Development

The [ordinary-simulation upgrade design](docs/PLUGIN_PRODUCT_UPGRADE_DESIGN.md)
records the implemented Plugin, MCP and UI work for the unreleased 0.10.0 service
candidate, including independent review and the remaining native-host release
gate. The hosted service has not been upgraded by this work.

For Claude or another harness, follow the [harness development guide](HARNESS_DEVELOPMENT.md). The server publishes the shared frontend and current tool schemas.

The root `.agents/plugins/marketplace.json` is the primary marketplace entry. The nested `plugins/.agents/plugins/marketplace.json` supports local marketplace registration. Do not register both sources with the same marketplace name.

Run `python -m pytest tests` to check package paths and exercise the installed Codex plugin loader. The loader test requires the Codex CLI.
