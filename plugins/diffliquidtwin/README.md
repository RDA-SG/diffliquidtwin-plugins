# RDA Cooling Lab for Codex

Build cooling models, run simulations and Python analyses, and explore results in linked 3D views and charts with the Red Dot AI hosted service.

## Version 0.5.0

Guidance now covers supported ordinary composed-scene simulations, saved
settings/revisions, explicit current versus historical inputs, numerical/spatial
mapping and truthful safety/energy/accuracy evidence. Advanced Python/task usage
is available separately, including all six task tools and the synchronous versus
asynchronous assimilation modes. Plugin **0.5.0** is paired with Platform
**0.12.0** and Engine **0.12.0** as source candidates; installing this package
does not deploy its backend. Discover actual connected capabilities
instead of assuming production availability from a version number.

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
