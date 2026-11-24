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

## Simulation scope and physical evidence

The package supports simulation-driven analysis and optimization; solver-free
external BI uploads are outside scope. The packaged skill defines the shared
[simulation scope and physical evidence rules](plugins/diffliquidtwin/skills/diffliquidtwin/SKILL.md#simulation-scope-and-physical-evidence),
including solver-backed publication, declared equipment inventory, incomplete
NPSH coverage and derivative diagnostics. Consult those rules before claiming
physical coverage, safety or gradient accuracy.

## Development

The [ordinary-simulation upgrade design](docs/PLUGIN_PRODUCT_UPGRADE_DESIGN.md)
is a historical record of the implemented Plugin, MCP and UI work and its
original acceptance boundaries.
The current source candidate is Plugin **0.5.0**, paired with Platform
**0.12.4** and Engine **0.12.1**. This pairing does not announce deployment
or a published client release; existing installations follow the host's normal
update workflow.

Historical production acceptance (2026-11-12) passed after the host connection
catalog was refreshed: actual saved-result trends, English/Chinese release dialogs and
832/319 CSS-pixel layouts were exercised. Supported explicit same-session
reopening is verified; automatic replacement of every historical cached card
remained unqualified at that boundary. Platform's
`prototype/DEPLOYMENT_20261111.md` records that deployment and the separate,
locally verified menu follow-up that was merged in source but not deployed.
This historical evidence does not qualify the current source pairing. Source integration does not change the fixed production installation
or resume deferred full-gradient studies.

For Claude or another harness, follow the [harness development guide](HARNESS_DEVELOPMENT.md). The server publishes the shared frontend and current tool schemas.

The canonical Codex marketplace entry is `.agents/plugins/marketplace.json` at the repository root.

Run `python -m pytest tests` to check package paths and exercise the installed Codex plugin loader. The loader test requires the Codex CLI.
