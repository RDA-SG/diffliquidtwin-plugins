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

Plugin **0.5.0** targets Platform **0.12.0** and Engine **0.12.0**;
this source pairing does not announce deployment or a `1.0` release.

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
saved-run variant. A Python analysis needs its original execution code; a source
ID alone cannot repeat arbitrary analysis controls. Displaying a result does not replace current settings or pick
the next Run inputs. Reopening a panel does not authorize another computation.

## Build and run ordinary scenes

Use create_hall for parameterized rooms and create_scene/update_scene for composed
equipment, ports, groups and pipes. Geometry uses metres and rotationY radians.
Exact routes retain supplied paths; explicit auto routing connects declared
ports around geometry. Geometry alone has no numerical coverage.

Attach an executable supported solverModel, or use advertised solverExport for
two-port devices (including crah_coil and cooling_tower), four-port
heat_exchanger/CDU and chiller, and one-port expansion_tank. HX ports use
secondary_in/out (or in/out) plus primary_in/out; chiller uses evap_in/out and
cond_in/out. Paired passages retain primary_hx_mapping/chiller_coupling,
primary_fluid and explicit thermal_geometry. Only the canonical
secondary/evaporator edge maps to the equipment; query the other solver passage
by its exact ID. A tank liquid port creates a 0 Pa mechanical reference and
permits solverExport.boundaryConditions=[]. Conservative transport is the
default where admitted. Exported pipe inner bores and routed lengths may supply
pipe inventory with source.basis=3d-instance-geometry. Chillers, HX/CDUs, towers,
CRAH coils and cold plates need explicit thermal_geometry or a user-selected
reference equipment assumption with recorded provenance; their 3D bounding boxes
cannot establish internal liquid/metal stores. Missing declarations reject
conservative admission; reduced physics requires an explicit user choice.
Reference assumptions remain engineering idealizations, without OEM calibration.
Reference equipment may remain visual-only.

For parameterized DSX rooms, coolingSystems selects ["TCS","HTFW"],
["TCS","HTFW","MTFW","CW"] or ["CHW","CW"]. primaryPlantMode selects
prescribed_boundary, dedicated_plant or shared_plant. shared_plant requires
solveScope=facility and sharedPrimaryLoop=true; conflicting authorities fail.
CRAH water coils, economizer HX, chillers and towers are solved where active;
air ducts remain visual context. Discover support before editing older services.

Import time-varying curves with `import_load_profile`, then snapshot them with
`bind_load_profile`; importing alone never changes the draft. Declare
`basis="it" | "liquid" | "air"`, units, interpolation, and total/per-member
allocation. Discover exact target IDs from the model:
- `liquid` requires TCS and facility/hall/DU/SU/rack/tray targets.
- `air` requires MTFW or CHW and facility/hall/DU/`target.kind="crah"`.
  Rack, SU and tray bindings are invalid for this basis.
- `it` uses the IT hierarchy and rejects CRAH. Liquid-only applies
  `liquidFraction`; hybrid adds the remaining fraction across the serving
  Hall/DU coils. Disjoint rack/SU profiles add their air shares once.
  Standalone CHW+CW sends all IT power to coils (facility/hall/DU/rack scope,
  with no cold plates).
Explicit `bindings[].entityIds` obey the same compatibility rules. Invalid
bindings leave the draft unchanged. Hybrid liquid+air and standalone air
allocations conserve total IT power; do not manually add a second air copy.

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
trajectory gradients. Where advertised, opt-in `gradientQualification` separately
measures Layer 1 frozen-trace reverse/forward AD versus finite differences,
Layer 2 optional geometric `dtCandidates` convergence, and Layer 3 three-grid
spatial gradient agreement (default `relativeGradientBudget=0.01`). Declare
`candidates`, two finer `references`, optional component/type `axes`, bounded
`parameters`, `observations` and common formal `timesS`. `fdStep`, `fdRtol` and
`fdAtol` control the parity check. See [policy fields and task defaults](references/advanced.md#trajectory-gradient-qualification).
Do not combine it with observable-only `meshQualification` (Engine thermal
resolution); ordinary runs without opt-in execute no gradient qualification.
Read `get_observation_reports(runId).thermal_transport.gradient_certificate`,
`get_hall(runId,includeConfiguration=true).configuration.reports.gradientAccuracy`,
or `get_task_result(jobId).result.gradientQualification` / `.gradientCertificate`.
`qualified` and `reused` cover the declared initial parameter point and measured
trajectory; `inherited_source_evidence` cannot qualify edited inputs. The result
is a measured three-grid refinement certificate, without an unbounded continuum
proof or a guarantee at distant optimizer iterates. Respect the user's compute
scope or paused studies.

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

The viewer's circuit filters cover TCS, HTFW, MTFW, CHW and CW. Query
temperature, pressure, drop, flow and liquidHeatKW on exact solved equipment
and route IDs. summary.entityIds remains rack-only; summary.plant carries
shared plant and gallery time series in root and non-root DU views. Chiller
sampleEdgeId selects evaporator cooling (+Q_evap); its condenser passage reports
+Q_cond, including compressor heat. CRAH/plates report positive heat absorbed
into liquid, and towers report positive rejection to ambient.

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

## Differentiable tasks and online assimilation

Use the six advertised tasks for calibration, observability, sensor selection,
design, controls and state assimilation. Read [advanced task contracts](references/advanced.md)
before submitting them. All support pressure, flow, temperature, Kelvin
`ode_state:` and `elec_power:` channels where physically available.
Scenario `time_resolved` aggregation preserves transient sensitivities;
`jacobianMode` selects auto/fwd/rev. Structured multi-loop design objectives
combine temperature/flow tracking, chip peaks, electrical power and scene-free
safety penalties. Compose `elecPowerWeight` + `temperatureCeilings` +
`safetyPenalty` for minimum plant power/PUE, or `thermalPowerMaximizeWeight` +
those constraints for maximum thermal capacity. Check returned
`thermalFeasible`, `thermalMargins` and `safetyFeasible` before comparing designs.
Use initial-point `gradientQualification` for the declared trajectory, then
calibrate, assimilate and optimize on the fixed mesh; it does not certify every
optimizer iterate. Publish comparative 3D fields with `publish_result_fields`
and ECharts/table evidence with `publish_artifact`.
PID controllers support `splitRange` multi-actuator bindings.

`assimilate_states` supports first-order conservative EKF/MHE over independent
Kelvin storage states and bounded slow parameters (64 joint coordinates), plus
reduced-model estimation. Conservative algebraic junction states and raw energy
coordinates are rejected. Streaming returns JSON directly; asynchronous batch
jobs use `get_task_result(jobId)` and have no 3D simulation frames.

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
