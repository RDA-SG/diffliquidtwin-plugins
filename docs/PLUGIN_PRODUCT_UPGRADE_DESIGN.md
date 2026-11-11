# Plugin and product upgrade design for the ordinary-simulation release

Current integration status (2026-11-12): Engine 0.10.0 and Platform 0.10.2
are deployed; Plugin 0.3.1 is the client source/release baseline. Production
native interaction passed after refreshing the host connection catalog,
including saved-result trends, English/Chinese release dialogs and actual
832/319 CSS-pixel layouts. Automatic historical-card replacement remains
unqualified. Platform owns `prototype/DEPLOYMENT_20261111.md` and the separately
verified menu follow-up that is merged in source but not deployed. Source
integration preserves fixed production artifacts and deferred gradient work.
The candidate acceptance below retains its original chronology and scope.

Status (2026-11-11): A–E are implemented and accepted for the agreed ordinary
simulation candidate. E passed isolated installation, actual native-host ordinary
workflows and final source-only numerical-selection rechecking. Automatic host
remount and cross-build replacement remain unqualified; supported explicit
same-session reopening was verified. Browser and SDK checks alone do not pass
the native gate.
At the candidate acceptance boundary, no publication, deployment or
full-gradient studies had occurred. The candidate pairing was Plugins 0.3.1
with Engine/Platform 0.10.0. Version 1.0 requires an explicit user request.

## 1. Outcome and ownership

A user can ask an agent to prepare a supported cooling scene, review its
settings and admission result, save without running, start an ordinary
simulation without Python, and inspect numerical results with applicable
safety, energy and accuracy evidence. Reopening preserves saved configuration
and immutable results. Geometry alone remains unsolved.

The conversation remains the main modeling/configuration surface. The UI
provides review, limited timing edits, progress and results. Advanced data is
available on demand; no JSON editor, wizard, separate dashboard or client-side
solver is required.

| Repository | Responsibility |
| --- | --- |
| Plugins | Agent routing, capability discovery, skill/reference content, installation/release notes and accurate listing/starter prompts. |
| Platform | Persistent scene settings, MCP schemas, report capture/read interfaces, UI presentation and numerical discovery/mapping. |
| Engine | Existing physical laws, admission, energy/transport observations and derivatives remain authoritative. No new physics or solver optimization is proposed. |

Reuse the remote HTTP MCP connection, native host OAuth, MCP App resource,
workspace/session ownership, optimistic revisions, job scheduler, cancellation,
retention and result readers. Plugin and service versions are independent.

## 2. Verified gaps and boundary

The Plugins package supplies a remote connection and skill/assets. It bundles
no frontend, Engine or static tool implementation. Its 0.3.0 connection is not
pinned to an Engine/Platform version; the service supplies tool schemas and UI.
This does not prove native-host acceptance of a changed workflow.

Inspection of current Plugins and the 0.10.0 candidate found:

Source baselines for this review: Plugins main `9f59387`, Platform candidate
`4cc55c9`, and Engine candidate `55f476e`. The proposal is not a statement about
which candidate is running on the public service.

| Gap | Source boundary | Required outcome |
| --- | --- | --- |
| Stale guidance | Plugin SKILL run signature omits sceneId; composed runs route through analysis; reduced thermal behavior is described globally. | Ordinary JSON execution and truthful model/gradient limits. |
| Incomplete scene settings | run_simulation accepts sceneId/config; configure_scenario still uses Hall scope/schema. | Validate and persist ordinary scene settings without submitting a job. |
| Ambiguous input source | UI startRun uses sourceRunId while a generic result is displayed; Current inputs omits a scene selector. | Saved current scene settings and historical result inputs have explicit, independent bindings. |
| Incomplete discovery | describe_hall exposes Hall scenarioSchema, not first-class ordinary-scene settings/capability limits. | Discover the shared actual schema and applicable admission conditions. |
| Reports disconnected | Ordinary evidence lives in observationSummary; standard report access and renderSafetyStatus do not consistently consume it. | Agent and UI read the same report meanings. |
| Evidence can be lost | Worker safety rows coalesce by timestamp; energy recording depends on selected output times. | Preserve event-side safety extrema and formal-t0 storage independently of output selection. |
| Numerical UI incomplete | Raw channels are queryable, but chart selection filters through spatial entities. | Unmapped numerical results survive discovery, selection and plotting. |
| Generic settings UI disabled | ConfigurationPanel disables generic edits and treats sampling as a scalar interval. | Honest saved-run review and a narrow, lossless timing edit contract. |

Relevant implementation seams are Platform's `prototype/service.py`,
`prototype/workspaces.py`, `prototype/mcp_contract.py`,
`prototype/analysis_worker.py`, `examples/generic_execution.py`,
`examples/ordinary_resolution.py`, and
`ui/static/js/prototype_{controller,configuration,exploration,transition}.js`.
Plugin content lives in `plugins/diffliquidtwin/`. Findings are source-backed;
the counterexamples have not been numerically reproduced in this design task.

Existing numerical/installed-service acceptance remains evidence for its actual
scope. This upgrade adds ordinary product-flow acceptance. It makes no claim of
new physical coverage, continuous safety, universal mesh accuracy or qualified
complete-trajectory gradients.

## 3. User workflows

0. **Create an executable scene:** distinguish visual composition from numerical
   authoring. Use solverExport for supported two-port geometry-derived devices,
   explicit physical boundaries and declared device parameters/assumptions.
   It does not create four-port primary/secondary HX coupling. Such networks
   require an explicit supported solverModel with actual couplings and declared
   spatial associations. Validate the chosen model; never fill missing physics
   with display geometry. Clarify this boundary in discovery and starter prompts.
1. **Prepare without running:** read the selected scene, validate requested
   supported settings, explain assumptions/errors, then save with its revision.
   Saving queues no work and preserves the investigation view.
2. **Run current inputs:** the main Run action explicitly identifies the current
   scene and reviewed revision. Showing an old result does not change that input
   source. Show whether requested ordinary qualification adds reference runs.
3. **Inspect results:** expose actual numerical channels, model/coverage, sampled
   safety, energy and ordinary accuracy evidence. Unknown or unavailable values
   stay explicit; static admission success is not a successful solve.
4. **Edit after running:** Current inputs reads the explicitly chosen live scene;
   Displayed result reads the immutable submitted/executed snapshot. Saving the
   former preserves the latter, camera, selection, cursor and time window.
5. **Repeat a result:** a separately labeled variant action uses sourceRunId.
   Later scene changes/source deletion do not change its copied input snapshot.
6. **Reopen/copy:** settings survive reopen. Copying a scene copies its settings
   as inputs, without claiming that result certificates qualify the new copy.

The current-input scene identity is explicit UI state chosen through the existing
scene/library flow. It is not inferred from the displayed result. If its scene
is deleted or no current scene has been chosen, disable current-input Run and
show the reason; retain the explicit result-variant action. Do not introduce a
second persisted active-scene registry.

## 4. Shared configuration and execution contract

### Storage, revisions and source selectors

Store normalized ordinary `scenario` alongside `document` in the existing scene
record. Geometry/solverModel stay in document. Reuse the existing scene revision,
workspace lock and atomic writer. Add no configuration registry, extra revision
counter, job kind or transaction framework. A never-configured scene resolves
ordinary defaults with their actual provenance; borrow no Hall initialization.

A configuration write requires expectedRevision, validates against that scene's
solverModel and checks the revision before deciding whether it is a canonical
no-op. Validate-only may omit it and returns the revision read. Include provenance
in equality.
No-op saves settle UI pending state even if the revision does not advance.
Configuration saves must not call update_scene's geometry/view reset behavior.
Geometry/model edits validate geometry/export/model structure, retaining saved
settings without rejecting a geometry edit merely because an old scenario target
was removed. Reads flag settings as needing revalidation; invalid retained
targets are identified on explicit validation/Run. Never discard them silently
or manufacture device parameters. Do not solve or start a study during a read.

A run snapshots scene revision, model inputs, normalized scenario and admission
under existing immutable-job rules. Later saves cannot alter it. A missing scene
or stale supplied expectedRevision fails before queueing; omitting the revision
permits a deliberate
run of the current saved revision and returns which revision was captured.

| Scope | Selection and revision meaning |
| --- | --- |
| Current ordinary scene | Explicit sceneId; expectedRevision belongs to this scene, not the Hall draft. |
| Saved-run variant | Explicit sourceRunId; use its immutable model/config snapshot, not the current displayed scene. Reject sceneId or scene revision in the same request. |
| Hall draft | Existing Hall source/model/config semantics and expectedDraftRevision. Reject scene revision fields. |
| No selector | Resolve Hall draft consistently, independent of displayed geometry/result. Generic UI/agent callers must pass sceneId. This intentionally removes implicit view-dependent generic selection. |

Persistent generic configuration accepts sceneId, not sourceRunId. To copy saved
inputs, read the run snapshot and explicitly save a complete config to a chosen
scene. No implicit solverModel overwrite follows from opening a result.

### Complete configuration, not an implicit patch

For ordinary scenes, `config` is a complete replacement in both save and
one-run override. Omitted settings resolve ordinary defaults or documented
absence; they do not inherit arbitrary saved values. Empty collections clear
only fields whose schema allows emptiness. Null clears only explicitly nullable
fields. Reject Hall recipes, model convenience fields and top-level
`duration/dt/recordIntervalS/solver` patches with sceneId. No new patch language
is needed. Existing Hall convenience behavior stays scoped to Hall.

With sceneId and no config, Run uses saved settings. With sourceRunId and no
config, it uses the saved run settings. An explicit config replaces settings
for that job only; it does not save to a scene/draft. Agents and the UI performing
a small edit first read the complete current config, change chosen fields and
submit the complete result with the checked revision.

Treat normalized timesS as the explicit effective output schedule. The current
normalizer does not retain whether these times were generated or user-supplied;
do not infer that origin from equal spacing. Changing dt preserves timesS.
The first UI increment edits only duration, dt and warmupSeconds. It displays
sampling truthfully and leaves event/control/qualification schedules untouched.
Shortening duration rejects dependent out-of-range times; it never trims them.
Changing explicit schedules remains an agent action. Required endpoint insertion
and qualification-time additions are shown in validation's effective preview.
A later regular-output convenience control needs an explicit intent contract.

### Public interfaces (proposed)

| Existing surface | Change |
| --- | --- |
| describe_hall | Advertise ordinarySceneScenarioSchema and applicability from shared schemas/admission, not a second Plugin schema catalog. |
| get_scene(sceneId) | Return saved/resolved scenario, provenance and the existing revision alongside document/geometry. |
| configure_scenario | Add sceneId/expectedRevision and the shared ordinary normalizer; complete-config semantics above. Retain Hall expectedDraftRevision. |
| run_simulation | Saved-settings fallback, explicit selectors and scene expectedRevision checking above; preserve show/source snapshot rules. |
| Existing configuration action | Add an explicit sceneId read, returning that revision; runId reads immutable submitted/executed settings. Reject conflicting sources. Both this UI consumer and get_scene use the same resolved settings authority. |
| get_hall(runId, includeConfiguration=true) | Extend the existing configuration response with bounded admission, accuracy, energy and safety summaries/detail descriptors. Add no second includeReports/reportDetail API. |
| query_results | Add a mutually exclusive report selector for paged safety/energy observations that current published fields cannot represent; keep existing numeric-query behavior. |
| list_entities / query_results | Discover/query numerical node, component and declared-observation identities independently of geometry. |

validateOnly must be an actual boolean true and works in read-only sessions.
Change the workspace mutation gate, which currently rejects scenario before
reading that flag. Validation changes no scene/draft/view/job/result/evidence or
qualification-cache state and queues no work. Normal access/session bookkeeping
may persist; zero disk writes is not the contract.

Validation checks schema, initial-state names/values, events, controls, observation
targets and qualification declarations, then uses Engine admission on the actual
prepared model. It performs no hydraulic Newton solve, transient rollout or grid
study. Return normalized inputs, scope/revision, applicability, runtime conditions
and actionable field/component errors. Never switch to reduced automatically.
Reuse existing error envelopes and conflict handling; do not add an error
framework or classify errors by matching human-readable messages.

Persist admission in the existing job record before its first save. Attaching
it only to the returned job copy does not provide later evidence. Runtime
convergence, reservoir conditions, safety and mesh budgets remain runtime claims.
Discovery distinguishes default conservative, explicitly frozen reduced,
unsupported combinations, derivative interfaces and separate trajectory-gradient
qualification; schema membership alone does not establish component support.

## 5. Common reports and necessary capture corrections

Use one report-contract authority across MCP/UI in the existing configuration/result path.
Adapt authoritative Hall/ordinary records; do not duplicate them into a new
store, recompute physics or run simulations while reading reports. Missing
historical evidence stays unavailable; do not backfill it through hidden solves.
Reuse configuration's solver/model/timing/execution fields and the existing
safetyEnvelope/alerts consumer contract. Populate an accurate bounded ordinary
safety summary from the preserved observations and expose the same meaning in
configuration. No second inspection mode or report store is needed.

| Group | Required meaning |
| --- | --- |
| Scope/provenance | Requested run, numerical evidence source, actual physical coverage, input/model identity, selected transport, actual execution methods, formal/warmup clocks and sampling. |
| Admission | Checked inputs, conditions, unsupported combinations and warnings; static success says nothing about convergence/accuracy. |
| Accuracy | Current ordinary request/outcome, observations/units/budgets and reference-change evidence; not requested, pending and unavailable are valid. Gradient qualification is separate. |
| Energy | Available actual storage, change from formal t0, external/boundary powers, storage rate and physical/junction/assembly defects, with units/signs. |
| Safety | Configured and unconfigured families, actual sampling coverage, worst sampled margin/entity/time, unavailable checks and unknown absolute pressures. |

Two small producer corrections are required, beyond a read adapter:

- Preserve all evaluated event-side safety extrema/coverage before any timestamp
  coalescing. Use distinct observation identities for coincident times; retain
  event-side labels only when the producer actually knows them. Never replace a
  worse left-side margin with the later right-side state at the same timestamp.
- Capture formal-t0 stored energy after warmup under the declared time-zero
  event semantics, independently of requested output times, when reporting
  storage change. Reuse the accepted-state observation;
  do not add a solve or change events, controls, integration or sampling cuts.

Summary responses use fixed caps/counts, worst findings and detail descriptors;
size does not grow with trajectory length or entity count. The added summaries
stay bounded even under configurationDetail=full; existing initialization and
component/execution detail behavior stays scoped to that existing interface.
Detailed temporal report reads
use the existing query_results route with `report=safety|energy`,
explicit run/scope and limit/offset/nextOffset/hasMore semantics. Time/window
filters apply only to time-bearing evidence. Report selection is exclusive of
ordinary metrics/aggregate arguments; invalid combinations fail visibly.
Return stable scalar check/quantity rows with source identity, applicable entity,
observation identity/time, unit, status and value/reason. Page coincident event
observations deterministically without dropping one. Existing page-size bounds
apply; never put an unbounded nested sample/entity collection in one row.
Admission and qualification outcomes stay in the existing configuration/result
evidence path; no general report service, cursor registry or storage layer is
required. A paged detail route is still necessary for energy defects and
coincident safety observations: current numeric fields expose neither completely.

Interpretation rules:

- No limits, no samples, unavailable pressure, evaluated pass and violation stay
  distinct. A violation may coexist with incomplete coverage. Zero alerts is
  insufficient evidence; safety remains sampled, without continuous-time proof.
- Qualification outcome, job outcome and certificate presence are separate.
  Reuse requires the existing exact request/model/runtime binding. An inherited
  certificate does not qualify changed inputs. Failed jobs expose unavailable
  evidence unless an authoritative intermediate outcome was actually retained.
- Derived results identify inherited evidence's source rather than attributing
  it to a newly edited scenario. Add no certificate-repair ledger.
- Aggregate only supported independent/disjoint scopes. A coupled whole-model
  report must not be added once for each spatial detail view.
- Show declared energy budgets only when present. Never invent a pass threshold
  or hide junction defects through assembly cancellation. HX internal exchange
  is not a second external source; fan electricity is separate from liquid heat.
  Read Engine energy observations instead of reconstructing rho*q*cp*dT.
- Show actual storage change and instantaneous powers. Endpoint quadrature is
  not an exact integration-stage energy identity; any later sampled cumulative
  estimate needs a separate approximation/error basis.
- Unknown absolute pressure remains null with a reason. Display pressure datum
  and unit; an assumed atmospheric offset cannot turn a gauge into a measurement.
- Ordinary qualification does not qualify gradients. Complete-trajectory gradient
  qualification remains unqualified and paused.

## 6. Numerical entities and spatial mapping

Derive the catalog from actual saved solver/result identities and published field
descriptors. Keep solver:node:<ID>, solver:component:<ID> and
solver:observation:<ID>, carrying original source ID/type explicitly rather
than splitting punctuation. Node/component namespaces remain distinct when raw
names coincide. Include available metric IDs, SI units, sampling/provenance and
any actual spatial association. Do not infer availability from equipment kind.

list_entities reuses its existing kinds/query/pagination fields for solver-node,
solver-component and solver-observation descriptors; add no new scope filter.
query_results accepts their exact IDs. The existing trend surface
must retain a numerical target independently of resolveEntity/spatial lookup.
Support agent-driven focus_hall numerical trends and reuse the current entity
finder/metric controls for selection; add no standalone technical picker widget.
Numeric selection is distinct from camera focus; mapped entities may link to
geometry, while unmapped values still plot and remain queryable.

Record deterministic geometry-export associations when solverExport produces
pipe/device edges, internal paths and port nodes. Adapt published-field lookup,
coloring, hover, inspection and trends to those exact mappings. Direct solverModel
attachments require explicit associations; matching names alone cannot establish
that two independently supplied objects are physically identical. Multiple paths
or ports require a declared measurement/aggregation, not an arbitrary first value.
Use geometry-export associations or explicit solver/spatial mapping only. No
mapping by name resemblance, proximity or matching counts. Do not manufacture
geometry objects for solver channels. Reference-only equipment stays so. Query,
plot and mapped coloring use the same source/time/unit. Extend focus_hall only
where its published selection contract requires it; no second selection engine.

## 7. UI within the current product

Reuse Library, Model & solver, Run, configuration/results and the current trend
surface. No new modeling editor or parallel dashboard is needed.

- Show Current inputs with explicit scene/revision and Displayed result with run
  identity. Read-only result settings cannot mutate a current scene. Disable
  only unavailable actions, with a visible reason.
- Expose the limited timing edits in section 4, effective sampling, controls and
  engineering assumptions. Validate/Apply uses the loaded full config/revision;
  stale edits preserve user input and offer reread/reapply, without blind retry.
- Main Run executes current saved inputs even while an old result is visible.
  Explicit result variants use saved-run inputs. Unsaved edits block mistaken
  submission. Show the actual submitted snapshot, without switching investigation
  source merely because a configuration was saved or a job was queued.
- Reuse job.progress/job.message for queue, initialization, warmup, formal run
  and any requested accuracy study where actually reported. Add no dedicated
  phase tracker. Cancel preserves old results/settings through existing handling.
- Keep the primary status focused on safety, missing physical coverage and
  warnings. Put energy balance details and requested accuracy evidence in the
  existing configuration panel. Do not add an accuracy badge for not_requested
  or imply that optional qualification must run for every simulation. The agent
  can still read that status explicitly. Keep evaluated
  findings and coverage gaps independently visible, including a violation plus
  an unavailable family. Details are keyboard-accessible, not tooltip-only.
  Missing reports show unavailable rather than disappearing.
- Preserve camera, spatial/numeric selection, cursor/window, displayed source
  and unsaved input through configuration saves and polling. Reuse existing
  geometry equality/camera transitions; avoid showModel's reset path. Add no
  camera-state framework.
- Existing finder/metric controls and agent-opened trends support unmapped
  nodes/components/declared observations without moving the camera. Use explicit time points;
  do not invent regular spacing for nonuniform output.
- Reuse structured errors to distinguish invalid input, unsupported capability,
  conflict, solver failure, qualification failure and unavailable evidence. A
  geometry preview is never presented as computed state.

New software text, diagnostics and repository documentation remain English.

## 8. Plugin content, compatibility and versioning

Propose Plugins 0.3.1 for skill/documentation/listing corrections. Its connection
contract stays unchanged; reassess MINOR scope only if that contract changes.
Do not synchronize Plugin and backend version numbers. Engine/Platform remain
the 0.10.0 candidate; no implicit 1.0 transition. No versions change in this task.

Keep the ordinary route, source/revision rules and core safety/evidence cautions
in a concise SKILL.md. Extract lengthy advanced Python/task usage into at most
one linked reference initially, avoiding extra reads for routine tasks. Read
tools/list and describe_hall for actual schemas; do not copy an implementation
catalog or solver theory into instructions.

Correct analysis-only composed-run routing, globally applied reduced HX/pipe
behavior, unqualified field-component support, estimator guidance lacking
explicit reduced selection, and initial-only task claims that omit the existing
scenario execution scope. Distinguish local live AD support from qualified
complete-trajectory gradients. No estimator fallback changes the selected model.

A Plugin upgrade does not deploy its backend. Check advertised configure_scenario
sceneId/generic schema support instead of trusting a version label. Without
persistent scene configuration, a service that advertises run_simulation(sceneId,
config) can still perform an explicitly requested one-run experiment. Explain
that it does not save settings; never substitute a run for a save-only request.
Otherwise report the missing capability; do not guess fields or change physics.
Retain supported Hall/analysis use through discovery without building
a backward-compatibility framework. Update installation/listing/starter content
around available user tasks, not historical wave names. Use small generic public
examples, without private acceptance fixtures, inventories or deployment config.

## 9. Proposed delivery order, effort and acceptance

These are preliminary elapsed-agent ranges, separated from passive waits; they
are not human staffing estimates or measured commitments. They are retained as
design estimates; implementation was subsequently authorized. No managed
execution plan was introduced. The status above records the remaining gate.

| Step | Deliverable | Code/content work | Active verification | Passive waits |
| --- | --- | --- | --- | --- |
| A | Saved settings, explicit source/revision binding, discovery and validation | 1–2 h | 0.5–1 h | Small fixture/build runs, usually minutes |
| B | Necessary capture, bounded reports, exact export mapping and numeric discovery/query | 1.5–3 h | 1–2 h | Small real-component runs, minutes |
| C | Correct current/result Run, settings, visible safety/reports and existing trends | 1.5–3 h | 1–2 h | Build/browser/test waits, minutes |
| D | Plugin skill/reference/listing and connection/package checks | 0.5–1 h | 0.25–0.5 h | Minimal |
| E | Isolated installed-service and supported native-host flow acceptance | 0.5–1 h setup | 0.5–1.5 h | Host availability and matched ordinary acceptance runs |

This totals approximately 8–17 active agent-hours before parallel savings.
It retains real observation-capture and paging tests omitted by the smallest
content-only estimate. Passive solver time is separate: matched complete cases
retain their existing three-minute-per-case inference goal, while explicitly
requested qualification references/cache misses can add work. Host access wait
has no reliable estimate. None of these design estimates is a benchmark.

Expected runtime impact is small but must be measured. A/C/D change input,
read/UI and instruction paths, not the transient kernel. B preserves existing
observation cadence and adds one formal-t0 energy observation rather than new
integration steps/control ticks. Summaries and mappings are produced from saved
observations; paged reads start no solve. Event-side retention adds some record
metadata/storage. Measure capture/write time and peak memory on small fixtures,
then repeat the matched complete acceptance cases because these callbacks change.
Do not promise zero overhead or recover time by reducing observations/accuracy.

A and report meaning precede UI consumers; B and D can overlap after their
contracts stabilize. Keep one writer per isolated repository. Engine requires
no implementation in this proposal; if a genuine Engine defect appears, report
it and reassess scope. Do not solve it through UI or topology changes.

Required gates:

1. **Settings/source:** validate-only in read-only sessions, stale/no-op revision
   handling, atomic save/read/run, reopening/copying, explicit one-run overrides,
   and a timing-only edit preserving non-default events, warmup, limits and
   nonuniform samples. Invalid dependent times fail without trimming. No-selector
   behavior is independent of the displayed scene/result.
2. **Run/UI binding:** display A, save current inputs B without changing view,
   main Run submits B; explicit variant submits A. Current-input reads identify
   their scene. Deleted current scenes cannot fall through to another source.
   Preserve dirty edits/camera/selection/cursor/window during save and polling.
3. **Actual report capture/read:** a worse event-left safety margin followed by
   a safe right state survives; formal-t0 energy exists after warmup even when
   output times exclude zero. Show violation and incomplete coverage together.
   Later report pages are readable; summary size is bounded. Unknown pressure,
   qualification request/outcome/binding and independent/coupled scopes remain
   distinct. Use actual write-to-read data, not prose checks or canned reports.
4. **Real interfaces:** use small supported pipe/pump/plate/storage/tower fixtures
   where applicable, and unsupported combinations for admission rejection. Do
   not claim support just to populate a report. Include a geometry-exported scene
   whose exact mappings drive coloring/hover/inspection/trend. Numeric nodes/components with
   equal raw names and declared observations must plot without spatial mappings;
   compare queried/rendered values, units, source and sampling.
5. **Physics/AD seams:** equations, tolerances, state, control/event clocks and
   live Tensor paths remain unchanged. Run targeted reverse/native/functional/FD
   checks if changed wrappers touch those paths. Resume no full-gradient job.
6. **Package and installation:** repository-native Plugin loader/distribution/
   listing checks, fixed Engine/Platform artifacts, actual imports/UI build and
   isolated service data. Record the verified combination; nominal versions alone
   do not identify unreleased builds.
7. **Native host:** exercise the ordinary flow using an isolated connection
   actually supported by the target MCP App host. Keep OAuth, SDK transport,
   browser preview and native-panel evidence separate. If isolation is unavailable,
   mark native interaction untested. Fetching HTML cannot pass that gate. Do not
   invent host APIs or change production endpoint/auth policy to make it pass.
8. **Regression/performance:** reuse unaffected numerical evidence. Repeat matched
   complete ordinary cases if execution/evidence callbacks, accepted inputs or
   sampling change; retain the existing three-minute inference target, unchanged
   physics/tolerances/runtime/workers and report result deltas separately. Cache
   misses and requested qualification reference work are reported separately.
   Do not relax accuracy or resume complete-gradient research.

The proposed release boundary includes A–E. Defer regular-output convenience
editing, standalone numeric/accuracy dashboards, richer 3D overlays and advanced-task UI. Exclude new auth/
transport layers, harness packages, schedulers/registries, continuous safety
proof, physical-model expansion, GPU, gradient repair and production cutover.

## 10. Independent review and adjudication

Three read-only Larva reviews were completed: frontend-engineer, senior-engineer
and tech-cofounder. All requested design revision; none establishes runtime
acceptance. The parent checked the cited source seams and revised this proposal.
It has not been resubmitted as a final unanimous approval. Implementation is proceeding under the subsequent user request; installed and
native acceptance remain separate gates.

| Reviewer | Finding | Parent decision and revision |
| --- | --- | --- |
| frontend-engineer | Run can select old-result inputs; Current inputs can read Hall while a generic result is shown. | Accepted after inspecting startRun and ConfigurationPanel/configuration. Sections 3–4 and 7 bind input scene/revision explicitly and separate main Run from result variants. |
| frontend-engineer | Spatial filters drop unmapped numeric channels; small edits can overwrite sampling intent; safety gaps can disappear. | Accepted. Required numeric selection/trend binding through existing controls, full-config timing edits and mixed violation/unavailable gates added. No standalone widget is required. |
| senior-engineer | Replacement/patch/source meaning is ambiguous; read adapters cannot recover discarded event-side safety or t0 energy. | Accepted after inspecting set_scenario/start, normalize_config, ordinary worker and runner observers. Section 4 defines replacement/selectors; section 5 permits narrow capture corrections. |
| senior-engineer | Full report details lack bounded continuation; inherited certificates/job outcomes can mislead. | Accepted. Section 5 uses paged query_results, separate evidence source/outcome and exact qualification binding; no ledger/backfill. |
| Both engineering reviewers | Readonly gate precedes validation; no-op/camera/numeric UI seams need explicit coverage. | Accepted. Existing gate, atomic writer, query and transition paths are named; no new framework is justified. |
| tech-cofounder | Missing executable-authoring workflow and exact solverExport mapping; geometry edits could be blocked by stale scenario targets. | Accepted after reading geometry_solver, list_entities and published-field lookup. Added workflow 0, authoritative export mappings, existing kinds filtering and validation-time rejection of retained invalid settings. The current starter prompt promises visualization, so it is not itself proof of broken simulation; the runnable boundary still needs explanation. |
| tech-cofounder | Reuse configuration/safety/progress surfaces; avoid routine accuracy jargon and splitting ordinary safety rules into extra files. | Accepted. Removed includeReports/reportDetail, new scope filter, standalone numeric picker and unrequested accuracy badges. Core ordinary/safety rules remain in SKILL; at most one advanced reference. Estimates reduced with the smaller surface. |
| tech-cofounder | Remove all common-report detail work and route unmapped numeric identities through the spatial index. | Partially rejected. Existing fields omit coincident event-side safety and whole-model energy defects, requiring a bounded existing query extension. Numeric discovery/focus is shared, but numerical-only identities must not become camera/spatial targets. No new report service/store is proposed. |
| tech-cofounder | Enable generic solver editing and promise a 4.5–8.5-hour complete delivery. | Deferred/qualified. The first generic UI edit set remains timing only; advanced solver composition stays conversational. A broader schedule range accounts for independently identified capture/paging, real-component and native-host verification; passive waits remain separate. |
