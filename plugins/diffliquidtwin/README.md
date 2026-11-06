# RDA Cooling Lab for Codex

Build cooling models, run simulations and Python analyses, and explore results in linked 3D views and charts with the Red Dot AI hosted service.

## Version 0.3.0

This package documents Wave 4A Platform tools: asynchronous calibration,
static control/design optimization, observability and D/A/E sensor design;
sampled SafetyEnvelope diagnostics; additional field cold plates and
valve/expansion-tank inputs; opt-in DSX fault interlocks and shared primary
multi-DU solves. Tool availability follows the connected service's discovery,
not the plugin version. Existing default DSX behavior remains unchanged.
See the [skill contract](skills/diffliquidtwin/SKILL.md#wave-4a-tools-and-opt-in-physics)
for submission, retrieval, assumptions and paired Engine compatibility gaps.

Wave 4B support in the same `0.3.0` client package documents Platform/Engine
`0.8.0`: `assimilate_states` for EKF/MHE streaming or batch state/parameter
estimation, and opt-in `inertialHydraulics` for pipe momentum and pump rotor
coast-down. See [Wave 4B usage and limits](skills/diffliquidtwin/SKILL.md#wave-4b-assimilation-and-inertial-hydraulics).
The connected service must advertise these tools and controls; plugin
installation alone does not enable them.

## Install

Add [RDA-SG/diffliquidtwin-plugins](https://github.com/RDA-SG/diffliquidtwin-plugins) as a marketplace in Codex and install **RDA Cooling Lab**. Complete Casdoor sign-in with an authorized account. Anyone may install; service access requires authorization. See [installation and sign-in](GETTING_STARTED.md).

Ask Codex to open RDA Cooling Lab. Modeling instructions stay in the conversation. Resume an existing experiment using its session ID.

## Connection

The marketplace is `rda-cooling-lab`; the plugin and MCP namespace are `diffliquidtwin`. The remote endpoint is `https://diffliquidtwin-mcp.demo.rda.ai/mcp`.

The plugin contains skills, display assets and a remote HTTP MCP configuration. No local Python, Node or simulation backend is required. Casdoor OAuth credentials are managed by the host and never distributed in this repository. Authorized users currently share team workspaces.

The Platform supplies the viewer, tools, simulations and stored results. Inspect returned model assumptions, solver settings and result provenance when interpreting simulations.

Only the Codex package is currently provided. A future Claude Code package can share this repository while using its own manifest and marketplace entry.

See the [harness development guide](https://github.com/RDA-SG/diffliquidtwin-plugins/blob/main/HARNESS_DEVELOPMENT.md) for OAuth, MCP Apps, session and acceptance requirements.

New experiments use the service's automatic Engine method selection. An automatic thermal-step limit is JSON `null`; positive caps and explicit methods remain available. Read saved execution evidence for actual methods, fallbacks and tolerance scope. The plugin supplies no solver or frontend bundle.
