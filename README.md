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

This package supports differentiable thermo-hydraulic simulation and
simulation-driven analysis/optimization. Solver-free external BI uploads are
outside scope. `start_analysis` (MCP `run_analysis`) requires a solver-backed
scene, an explicit executable model or a simulation-backed `sourceRunId`.
`publish_fields` (MCP `publish_result_fields`) and `publish_artifact` require
both a simulation/solver-backed anchor and an explicit simulation-derived
content relationship; an unrelated run ID or unused solver model is insufficient.
Simulation input/load-schedule charts and saved-run postprocessing remain valid.

Conservative equipment admission requires declared liquid/metal inventory or an
explicitly selected reference equipment assumption with recorded provenance.
Otherwise admission fails; reduced physics requires an explicit user choice.
Equipment bounding boxes cannot supply silent thermal inventory; pipe inventory
may derive from explicit inner bore and routed length.
Pump NPSH uses explicit `suctionDiameter` / `inletArea` first, then a unique
single direct suction pipe bore. Multi-branch suction is `unavailable`.
A configured NPSH constraint with unknown suction area has incomplete safety
coverage and cannot establish `safe=True` or `safetyFeasible=True`; provide
suction geometry before claiming safety.

Read `differentiationStatus` and `differentiationReason`:
`differentiable | saturated | non_differentiable | unavailable` distinguish
smooth dependence, authoritative smooth zero-slope saturation, switching/kinks
and missing derivative evidence. Missing derivatives must never become numeric
zero. These states are independent of `gradientQualification`; a status alone
does not certify trajectory-gradient accuracy.

## Development

The [ordinary-simulation upgrade design](docs/PLUGIN_PRODUCT_UPGRADE_DESIGN.md)
records the implemented Plugin, MCP and UI work and its acceptance boundaries.
The current source candidate is Plugin **0.5.0**, paired with Platform
**0.12.3** and Engine **0.12.1**. This pairing does not announce deployment
or a published client release; existing installations follow the host's normal
update workflow.

Production native interaction passed after the host connection catalog was
refreshed: actual saved-result trends, English/Chinese release dialogs and
832/319 CSS-pixel layouts were exercised. Supported explicit same-session
reopening is verified; automatic replacement of every historical cached card
remains unqualified. Platform owns `prototype/DEPLOYMENT_20261111.md` and the
separate, locally verified menu follow-up that is merged in source but not
deployed. Source integration does not change the fixed production installation
or resume deferred full-gradient studies.

For Claude or another harness, follow the [harness development guide](HARNESS_DEVELOPMENT.md). The server publishes the shared frontend and current tool schemas.

The root `.agents/plugins/marketplace.json` is the primary marketplace entry. The nested `plugins/.agents/plugins/marketplace.json` supports local marketplace registration. Do not register both sources with the same marketplace name.

Run `python -m pytest tests` to check package paths and exercise the installed Codex plugin loader. The loader test requires the Codex CLI.
