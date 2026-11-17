# Install and sign in to RDA Cooling Lab for Codex

The thin plugin connects to `https://diffliquidtwin-mcp.demo.rda.ai/mcp`.
Codex manages native OAuth sign-in, credential storage and refresh. Users need
no local Python, Node, Torch or backend.

## Install

Add this repository's marketplace in Codex and install **RDA Cooling Lab**.
The marketplace points to `plugins/diffliquidtwin`; that directory contains the
client package. Its manifest references the remote HTTP `.mcp.json`. Use native
connection discovery/sign-in; avoid registering the same URL twice. Installing
alone grants no service access: sign in with an authorized account. Ask Codex
to open Cooling Lab to show the native panel.

## Prepare, run and inspect

Ask for a parameterized room or a composed scene. Visual geometry needs a
supported numerical association before simulation. Have the agent explain
coverage/engineering assumptions, validate settings and save without running
when requested. A newer plugin cannot upgrade an older service.

Current inputs and displayed results are independent. **Run simulation** executes
saved current inputs; **Run displayed inputs** explicitly repeats historical
inputs. Configuration shows the source and effective timing. Limited timing
edits preserve explicit sampling/events; out-of-range dependent times require
correction. Numerical channels can be queried/plotted without geometry. Coloring
requires an actual export or explicit mapping.

Safety warnings concern sampled checks and declared limits. Missing limits and
unknown absolute pressure are coverage gaps. Energy evidence and requested
accuracy qualification appear in configuration details. Missing reports do not
mean successful checks. Optional qualification can add reference computation;
trajectory-gradient qualification is separate. Availability follows connected
capabilities; Plugin **0.5.0** is paired with Platform **0.12.3** and Engine
**0.12.1** as source candidates, without announcing production deployment. When
persistent settings are absent, the agent can explain which explicitly requested
one-run workflows remain available.

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

## Authentication requirements for operators

The service advertises protected-resource metadata, authorization discovery,
PKCE S256 and supported client registration. The host manages its own callback
and client identity; the plugin fixes neither. The access-token audience must
identify the full MCP resource URL. The service checks signature, issuer,
expiration, subject, audience and revocation with the configured provider;
provider outages fail access checks. Never put secrets/tokens in plugin files,
conversations, HTML or tool arguments. No static-token or local bypass is shipped.

## Restore an experiment

open_hall() creates a workspace and application session. Retain sessionId for
subsequent state tools and restore it with open_hall(sessionId=...). Login and
application sessions have separate lifetimes; reconnecting needs no new
experiment. list_workspaces discovers retained experiments. workspaceId opens
read-only; sourceWorkspaceId copies inputs into an editable experiment without
historical results. The hosted service uses an authorized shared team library,
without individual data isolation.

## Retention and cleanup

Experiments supports search, paging, viewing and explicit deletion. Continue
experiment copies inputs. Closing a panel/session deletes nothing; restarting
retains unexpired data. Keep protects selected results and their dependencies;
new runs/experiments otherwise follow temporary retention. Actual viewing and
queries count as use; background polling/lists do not.

Default retention: empty untouched workspace 24 hours; failed/cancelled/
interrupted jobs 7 days; temporary successful runs 14 days; inactive temporary
workspaces 30 days. The latest successful result is retained at least through
workspace last-use plus 30 days. Retained workspaces still have a finite lifetime;
explicitly kept results/actual analysis dependencies stay protected. Running/
queued jobs and online viewers are protected. The server checks expiration
periodically and capacity before new computation; cleanup never cancels active
jobs automatically.

Clean up previews exact candidates, estimated reclaimable bytes and skip reasons.
Execution rechecks state and uses those explicit IDs, excluding later jobs.
Deleting kept content requires explicit inclusion. Deleting a workspace removes
inputs, scenes, loads, results, analysis and sessions. Agents use the same
get_storage_status/set_retention/cleanup_workspace workflow with sessionId.

Hard-linked snapshots make logical size differ from reclaimable/actually freed
space; source deletion need not free its full logical size. Failed file removal
reports pending cleanup/warnings for retry. Missing displayed sources show
unavailable instead of selecting unrelated results. Report capacity reclaimed
only after actual disk release.

## Troubleshooting

Verify service authorization and reconnect through host connection settings for
sign-in errors. Retain sessionId. Report loaded interface build, service version
and actual job error where available. The package includes no local bridge or
frontend build. Use repository Issues without private data/credentials. Loader
success, backend access and native-panel rendering are distinct checks.
