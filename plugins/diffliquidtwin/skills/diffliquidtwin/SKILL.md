---
name: diffliquidtwin
description: Build liquid-cooling scenes, run supported simulations, and inspect saved numerical results in linked 3D views and charts through RDA Cooling Lab.
---

# RDA Cooling Lab

Use the connected service for modeling, simulation and saved-result exploration.
Platform supplies tools/UI/storage; Engine supplies physics. Read tools/list and
describe_hall for actual capabilities. Installing this thin plugin does not
upgrade its backend. Read [advanced analysis](references/advanced.md) only for
Python or differentiable-task workflows; ordinary and safety rules are here.

## Sessions, sources and recovery

open_hall() creates an independent workspace and editable application session.
Retain sessionId and pass it to stateful calls. Reopen with that sessionId; login
and MCP transport identity do not choose an application session. list_workspaces
finds retained experiments. workspaceId opens read-only; sourceWorkspaceId copies
inputs into an editable workspace without historical results. Recover a
connection by reusing the session; check actual state before retrying a timed-out
write or job submission.

Keep current inputs, displayed immutable results and camera independent. Read
revisions before editing, reconcile conflicts and preserve newer user edits.
Use explicit sceneId for a current ordinary scene and sourceRunId for a deliberate
saved-run variant. Displaying a result does not replace current settings or pick
the next Run inputs. Reopening a panel does not authorize another computation.

## Build and run ordinary scenes

Use create_hall for parameterized rooms and create_scene/update_scene for composed
equipment, ports, groups and pipes. Geometry uses metres and rotationY radians.
Exact routes retain supplied paths; explicit auto routing connects declared
ports around geometry. Geometry alone has no numerical coverage.

Attach an executable supported solverModel, or use advertised solverExport for
supported two-port devices with explicit physical boundaries and constitutive
parameters. Export follows actual routes, elevations and port connectivity.
Four-port primary/secondary HX networks need an explicit solverModel and real
couplings. The two-port exporter does not infer them. Declare engineering
assumptions, their source and uncertainty. Do not manufacture hidden inventory,
conductance or ratings. Reference equipment may remain visual-only.

For ordinary simulation, prefer JSON configuration over Python analysis:

1. Read get_scene(sceneId), saved scenario, numerical association and revision.
2. If configure_scenario advertises sceneId and the ordinary schema, validate a
   complete config with validateOnly=true. It checks static admission and targets
   without a solve, job or input mutation. Read-only sessions may validate.
3. Save the complete accepted config with sceneId and expectedRevision. For a
   small edit, modify the full config just read, preserving controls, limits,
   events and output times. Omission resolves ordinary defaults; it is not a
   patch. Hall recipes/convenience patches stay scoped to Hall.
4. Run sceneId with the reviewed revision. Omitted config uses saved settings;
   explicit config is a complete one-run replacement and saves nothing. Use
   sourceRunId for an immutable result variant; no selector uses the Hall draft.
5. Retain jobId, poll get_hall/list_simulations to terminal status, and inspect
   actual saved inputs/execution. A queued job or static admission is no result.

If persistent scene settings are absent but run_simulation advertises sceneId/
config, an explicitly requested one-run experiment may still use them. Explain
that it does not save settings. Never replace a save-only request with a run or
send guessed fields to an older service.

Discover warmupSeconds, canonical initialState, SI boundary/actuator events,
controllers, observations, explicit timesS and optional meshQualification from
the connected schema. Changing dt preserves explicit output times. Invalid
dependent times require correction; do not silently trim events or loosen
precision. Default conservative support is subject to actual Engine admission.
Reduced remains frozen and explicit, with different physical assumptions.

## Inspect results and physical evidence

get_hall(runId,includeConfiguration=true) returns actual model/solver settings,
origins, initialization, clocks, execution reports and bounded evidence. Static
admission does not certify runtime convergence, safety or accuracy. Ordinary
qualification applies only to its declared observables, budgets and exact
validated inputs; reuse is not a universal scene certificate. It does not qualify
trajectory gradients. Keep full-trajectory gradient studies separate and respect
the user's compute scope or paused work.

Discover exact solver-node/component/observation descriptors using list_entities
kinds/query/pagination. Preserve full IDs, including colons; use discovered metric
IDs, units and unavailable nulls in query_results. Numerical results do not require
geometry. Only actual export associations or explicit physical mappings permit
3D coloring. Names, positions and matching counts cannot establish a mapping.
Multiple ports/paths need a declared measurement, not an arbitrary outlet.

Safety is sampled. A violation may coexist with incomplete coverage. Distinguish
no limits, no samples, unavailable checks, unknown absolute pressure, evaluated
pass and violation. Zero alerts alone proves nothing. Read actual limit
assumptions, scope, worst margin/entity/time and sampling. Never invent a rating
or turn an arbitrary gauge into absolute pressure with an assumed offset.

Energy evidence separates storage, external/boundary power and physical/junction/
assembly defects. HX internal exchange is not extra external heat; fan electricity
is separate from liquid heat. Storage change from formal t0 requires its recorded
baseline. Sampled power quadrature is not an integration-stage energy identity.
Do not fabricate thresholds or reconstruct constitutive duty from mixed nodes.
Inherited source observations are not predictions for edited inputs.

When advertised, query_results(report=safety|energy,limit/offset) reads detailed
scalar evidence and preserves coincident event observations. Reject combinations
with ordinary metric/entity/aggregate selectors. Follow nextOffset/hasMore;
missing historical reports remain unavailable, without hidden recomputation.

## Present, retain and clean

Use focus_hall to select exact entities, results, metrics and time/window, or to
open the existing selection trend. Unmapped numerical channels can plot without
camera targets. Request camera movement explicitly and only for spatial objects;
selection does not imply movement. Geometry previews have no computed readings.

view.sequence acknowledges receipt, not rendering. Check actual
context.appliedViewSequence, source/selection and viewError before claiming that
the panel displayed a request. Read actual camera pose/transition after movement.
Preserve the user's investigation and unsaved input when saving or queueing.

Publish sourced fields for derived numerical data and artifacts for durable
charts/tables/Markdown/images. Publishing and opening are separate actions.
Use registered image bytes for remote services, not caller-local paths. Imported
loads require declared units, elapsed/absolute time basis, IT/liquid power basis,
interpolation and conserved total/per-member allocation. Importing does not bind
a source; apply it through the service's explicit binding/snapshot tools.

Keep requested results and dependencies through existing retention controls.
Closing a panel deletes nothing. Preview cleanup candidates and delete only in
the requested scope, respecting active jobs and kept content. Use host-managed
OAuth and never expose credentials in content, tools or code.
