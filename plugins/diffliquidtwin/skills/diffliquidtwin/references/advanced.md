# Advanced Python analysis and differentiable tasks

Read this for requested analysis/objectives beyond ordinary JSON simulation.
Discover current schemas and actual applicability; this is not a tool catalog.

Plugin **0.5.0** targets Platform **0.12.4** and Engine **0.12.1** as
source candidates, without announcing deployment or a `1.0` release.

## Simulation scope and physical evidence

The skill's [shared scope and physical evidence rules](../SKILL.md#simulation-scope-and-physical-evidence)
apply to all advanced tasks, including inventory admission and NPSH coverage.
The sections below add Python publication details and differentiation diagnostics.

## Differentiation diagnostics

Preserve returned `differentiationStatus` and `differentiationReason` separately
from trajectory qualification. Status precedence is
`unavailable > non_differentiable > saturated > differentiable`:

- `unavailable`: disabled AD, failed equilibrium, unsupported derivative order,
  or an opaque/non-AD callback. Never serialize missing evidence as `0.0`.
- `non_differentiable`: active kink/switching boundary, including a connectivity
  or pressure-gauge change, pump shutoff or hard PID clamp.
- `saturated`: an authoritative smooth zero-slope saturation/deadband with a
  fixed connectivity/gauge map. A zero local actuator slope cannot override a
  simultaneous switching boundary.
- `differentiable`: active AD with smooth dependence and no straddled kink.

`gradientQualification` independently reports `qualified`, `failed`,
`not_requested` or `inherited_source_evidence`; exact cache reuse may report
`reused`. Preserve the returned scope and executed layers. Smooth local AD
support alone does not qualify a trajectory; saturation does not mean broken AD.
Use reproducible synthetic multi-circuit reference cases for calibration,
assimilation and efficiency/capacity comparisons. Keep real customer/site data
out of this repository and compare feasible results against explicit baseline
controls without assuming a fixed percentage improvement.

## Python execution and publication

`run_analysis` uses a supported executable scene, explicit
model or immutable simulation-backed saved-run source and
the shared asynchronous scheduler. Inspect the actual worker context and APIs;
ctx exposes model, scene, scenario and output directory. Publish numerical fields
through ctx.publish and artifacts through ctx.publish_artifact. Both require
simulation-backed runIds (simulation or solver-backed analysis) or a sceneId with
solverModel, plus explicit provenance relating content to simulation inputs/load
schedules, outputs, model diagnostics or derived postprocessing. A visual-only
scene without model/sourceRunId is rejected. An unused solverModel or unrelated
runId never authorizes arbitrary external charts/fields. Fields use exact
entity IDs, sorted seconds, time-major values, explicit units/provenance and null
for unavailable data; they cannot impersonate builtins. Actual solver/spatial
associations drive geometry. Publish registered bytes for remote images.

Retain job IDs, poll terminal status and explain actual errors. Opening an
artifact or live selection trend uses the existing analysis surface separately
from publication. Associate saved content with its real run/entity/time/window
so the user can revisit evidence. Immutable source snapshots preserve independence
from source deletion without establishing predictions under changed inputs.

## Parameter, control and observation tasks

Use the six advertised task tools: `calibrate_parameters`, `optimize_controls`
(static setpoints or initial-scope PID gain/setpoint tuning), `optimize_design`, `analyze_observability`, `design_sensors`
and `assimilate_states` for supported bounded scalar Engine parameters/observations.
The first five tools run as asynchronous jobs. `assimilate_states` defaults to a
synchronous single step with `measurements`, while `trajectory` mode defaults to
an asynchronous batch; its `asynchronous` option explicitly overrides the default.
Poll asynchronous jobs with `get_task_result(jobId)` to terminal status;
synchronous assimilation returns JSON directly. Tasks do not mutate current
inputs. Read-only sessions cannot execute. Existing cancellation/retention applies
to jobs; polling does not keep them.
Declare physical bounds and scales for mixed pressure/temperature/flow objectives.
Use actual Engine attribute names and units, not presentation labels.

executionScope=initial concerns the operating point. Where advertised, scenario
scope and observationTimesS follow actual Hall warmup/control/event clocks with
right-continuous samples. Generic solver scenes also support scenario schedules.
`scenarioAggregation="mean"` retains legacy scalar measurements.
`scenarioAggregation="time_resolved"`, or per-channel calibration arrays aligned
with `observationTimesS`, retains the time-major trajectory. Declare arrays for
every calibration channel in this mode. `jacobianMode="auto"|"fwd"|"rev"`
selects observability and sensor-design AD routing; sensor selection retains
each physical sensor's complete temporal block.

All five observation channels are available: `pressure:<node>` [Pa],
`flow:<component>` [m3/s], `temperature:<node>` [K],
`ode_state:<component>.<temp_state>` [K], and `elec_power:<component>` [W].
Use independent Kelvin aliases from the actual model, never raw `E_*` energy
coordinates. Initial thermal/power observations select coupled evaluation.

Structured design `objective` terms add normalized `flowTargets` (1e-3 m3/s),
`temperatureTargets` (1 K), smooth `chipPeakWeight` (LogSumExp, tau=1 K,
`referenceK=273.15` by default), and `elecPowerWeight` (1 kW).
`powerComponents` optionally selects electrical consumers; omission includes all.
`safetyPenalty={enabled:true,method:"softplus"|"huber",weight:1}` adds the
Engine envelope using `scenario.safetyLimits`, with or without scene metadata.
Pipe velocity and adjacent pump-inlet areas retain live optimized diameters.
Limits remain explicit illustrative assumptions, not equipment certification.
Legacy `objective={flow:"pipe",target:0.001}` remains supported.

For minimum plant electrical power (Min-PUE under matched IT load), combine
`elecPowerWeight`, `temperatureCeilings`, and `safetyPenalty`. Bound actual
equipment controls: economizer valve opening, chiller `command`/`T_chw_set`,
pump `N`, and tower `fan_speed`. Retain the baseline load, wet-bulb temperature,
equipment and tolerances in comparisons; report watts and feasibility separately.

For maximum thermal capacity, add positive `thermalPowerMaximizeWeight` and
learnable `coldplate_power` (or `Q_chip`) / prescribed-heat `Q_air_W` coordinates.
The objective subtracts weight times distinct selected thermal watts / 1e6 W;
optional `thermalPowerComponents` restricts the component IDs. At least one
active thermal coordinate is required. Omitted objective mode becomes `coupled`.
Never specify both cold-plate aliases on one component; `air_ntu` coils reject
thermal-power coordinates because their duty depends on UA and air inlet state.
In scenario scope, candidates override heat inputs during rollout, including
scheduled heat inputs, so comparisons use executed candidate power.

`temperatureCeilings=[{target:"ode_state:coil.T_coil",maxK:315,weight:1000}]`
also accepts `temperature:<node>` and `chip_peak`. All ceilings use Kelvin.
Each adds `weight * mean(softplus(T - maxK))` (1 K width); default weight is 1000.
Every declared `observationTimesS` sample participates even with mean aggregation.
The result reports worst-sample `thermalMargins`, `thermalFeasible`,
`safetyEnvelope`, `safetyFeasible` and mean total `electricalPowerW`. Sum the
distinct thermal coordinates from returned parameters for capacity comparisons;
retain fixed and time-varying non-optimized loads separately.
Soft penalties do not guarantee feasibility: reject infeasible candidates and
retain a hot spike even when the trajectory mean is cool. Neither samples nor
initial-point gradient certificates establish continuous-time safety.

A composable workflow is: qualify the initial parameter point's declared
trajectory with `gradientQualification`; recover hydraulic/thermal parameters
with `calibrate_parameters` from pressure, flow, Kelvin temperature and
`elec_power` observations; track HX/coil UA or chiller COP degradation through
first-order conservative EKF/MHE `assimilate_states`; then optimize plant power
or thermal capacity. Keep each task's initial-point certificate and its scope,
check both feasibility flags, and compare against a matched baseline.
Publish baseline/candidate numeric fields with `publish_result_fields` for 3D
selection, and persist ECharts charts plus table summaries with `publish_artifact`.
Task JSON alone has no simulation frames; associate publications with an actual
completed analysis/simulation and declare units, entity IDs and provenance.

Scenario `controllers` admit pump `N`, valve/PICV `opening`/`u`, tower
`fan_speed`, CRAH `fan_speed`/`T_air_in`/`Q_air_W`, and chiller
`command`/`T_chw_set`. A `splitRange` (or `split_range`) list replaces the
single component/attribute binding. Each row declares `control_key`,
`u_min`, `u_max`, `out_min`, and `out_max` in physical SI units.
PID command bounds must lie in [0,1]; descending output ranges are allowed.
`optimize_controls.options.controller` uses that declaration in initial scope;
`optimizeSetpoint=true` includes the working setpoint alongside PID gains.
Initial-scope PID optimization requires `sampleIntervalS == scenario.dt`;
scenario replay and live editor sessions support independent sampling clocks.
The 2D editor displays temperature setpoints/actuators in Celsius and power
in watts, preserves SI values on export, and connects every split-range target.
Unsupported objectives need an explicitly requested Python workflow. AD interface support does not establish a
complete trajectory's gradient grid accuracy. Respect paused studies and the
user's compute scope; retain live tensors across differentiable wrappers.

## Trajectory gradient qualification

Discover `gradientQualification` in the connected scenario and task schemas
before using it. Ordinary JSON runs declare the policy in `config`; the five
transient task tools declare it in `options.gradientQualification`. It is
separate from observable-only `meshQualification`, which exposes Engine's
thermal-resolution workflow (`solvers/thermal_resolution.py`). `thermalResolution`
is not a Platform config field. Use observable refinement for physical outputs under absolute SI
budgets; use gradient qualification before relying on declared trajectory
sensitivities for calibration, design, controls, observability or sensor choice.
Never combine the policies on the same request. No opt-in means no gradient
qualification rollouts; ordinary simulation retains its existing compute budget.

Policy fields:

- `enabled` defaults to true. `candidates` is a nonempty increasing array of
  positive integer meshes or axis-to-integer maps; `references` contains exactly
  two strictly finer meshes. `axes` declares each axis through `components` or
  `componentTypes`; vector meshes must match its keys. It can refine pipes,
  HX passages, CRAH coils, chillers/condenser legs and towers where admitted.
- `parameters` contains `{component,parameter,value,bounds:[low,high]}` rows.
  Ordinary scenario policies can address `controller:0`, `controller:1`, etc.
  (zero-based indices in `controllers`) with `kp`, `ki`, `kd` or `setpoint`;
  component and controller tensors retain live reverse/forward derivatives.
  Task policies retain the task's own parameter scope.
  `observations` maps names to actual measurement declarations (or lists
  channels), and `timesS` specifies strictly increasing common formal samples.
- `relativeGradientBudget` defaults to `0.01`, `gradientFloor` to `1e-8`.
  Optional `observableBudgets` adds positive absolute SI channel budgets;
  `absoluteBudgets` is an alternative spelling, never combined with it.
- `fdStep=1e-6`, `fdRtol=1e-5`, `fdAtol=1e-7` control frozen-trace central FD.
  The Engine records and replays the accepted implicit schedule to compare
  reverse AD, forward JVP and FD at the same initial parameter point.
- Optional `dtCandidates=[dt,dt/2,dt/4]` requests temporal convergence. All
  duration, event and formal sample times must align with every step; default
  recording tracks each step. Non-geometric triples fail. Without this field,
  Layer 2 reports `not_requested`; machine-floor differences have no fitted
  order. `auto` resolves to SDIRK2 for qualification, without changing physics.

For example, refine an actual pipe while measuring its flow:

```json
{
  "candidates": [{"transport": 2}],
  "references": [{"transport": 4}, {"transport": 8}],
  "axes": {"transport": {"components": ["pipe"]}},
  "parameters": [{"component": "pipe", "parameter": "d", "value": 0.02, "bounds": [0.01, 0.03]}],
  "observations": {"flow:pipe": "flow:pipe"},
  "timesS": [0, 1], "dtCandidates": [1, 0.5, 0.25],
  "relativeGradientBudget": 0.01, "fdStep": 0.000001,
  "fdRtol": 0.00001, "fdAtol": 0.0000001
}
```

A transient task defaults omitted `parameters`, `observations` and `timesS` to
its own parameters, measurement/objective channels and `observationTimesS`.
Initial-scope `optimize_controls` defaults times to its positive rollout steps.
Explicit conflicting scope declarations fail. Steady-only initial calibration,
design, observability and sensor tasks reject trajectory qualification; use
`executionScope="scenario"`. Qualification runs once at theta_0 before iteration,
and every objective/gradient evaluation reuses the selected fixed mesh. The
workspace caches exact policy, physics, execution, scope and numerical-source
identity (including Engine task code); unchanged requests report `reused` without
repeating three-grid solves. Changed inputs require new evidence.

Read `get_observation_reports(runId).thermal_transport.gradient_certificate`
alongside `resolution_certificate`. Inspect `layer1_ad_fd_parity`,
`layer2_temporal_convergence`, selected `resolution`, `references`,
`candidate_relative_error`, `reference_relative_change` and the declared budget.
The three-grid error includes candidate/reference error plus reference change.
`get_hall(runId,includeConfiguration=true).configuration.reports.gradientAccuracy`
provides bounded evidence, including task jobs. `get_task_result(jobId).result`
exposes full `gradientQualification` and `gradientCertificate` evidence. Saved
`model.json` retains `thermal_transport.gradient_certificate`. The bilingual
configuration panel reports gradient accuracy and structured layer diagnostics.
Edited source variants without verified fresh/reused evidence are downgraded to
`inherited_source_evidence`. Certificates cover the evaluated initial parameter
point, observations, times and aggregation/scope only. They provide measured
three-grid agreement, without a continuum proof or off-point iterate guarantee.

## Component parameters and conservative cooling towers

`Re_ref`, `Re_0`, `n_re` and `Q_bep_ref` are not supported component constructor
parameter names. Use `htc_reference_mdot`, `htc_hydraulic_diameter` and
`htc_flow_area` where the component admits flow-dependent HTC, and
`q_bep_fraction` for the pump's best-efficiency flow fraction. Discover actual
component applicability rather than treating these as universal parameters.

Conservative cooling towers support declared wetted inventory/thermal geometry,
transport dynamics, heat rejection and fan control. Supported tower parameters
include `thermal_mode`, `hinge_width_K`, `capacity_transition_W` and
`fan_transition_fraction`. Inspect model admission and execution evidence;
this does not qualify every coupled model or trajectory gradient.

## Multi-circuit water networks and composed equipment

Hall coolingSystems supports TCS+HTFW, standalone CHW+CW and hybrid
TCS+HTFW+MTFW+CW. CHW and MTFW are mutually exclusive. primaryPlantMode is the
plant authority: prescribed_boundary, dedicated_plant or shared_plant. A shared
plant requires facility scope and sharedPrimaryLoop=true. Do not sum its
whole-model energy ledger across DU partitions.

Use crah_coil parameters load_mode (prescribed_heat or air_ntu), Q_air_W,
UA, T_air_in [K], air_flow_kg_s, fan_speed and fan_power_rated_W. Chiller
parameters include command, T_chw_set [K], UA_evap, cooling_capacity [W],
cop_nominal, cop_temp_coeff, design_lift_K, cop_min and W_aux [W].
chiller_condenser_side carries a separate hydraulic curve and liquid inventory.
Runtime events/controllers admit coil fan_speed/T_air_in/Q_air_W, chiller
command/T_chw_set and PICV opening (canonical u); fan/command/opening bounds
are [0,1]. Read actual constructor/schema fields; do not substitute volumetric
air flow or UA_coil for the Engine's mass-flow and UA contract.

solverExport on cooling-scene/v1 supports four-port HX/CDU and chiller,
two-port CRAH/tower, and a one-port expansion_tank mechanical reference with
boundaryConditions=[]. Export preserves exact port node identities, primary
fluid assignments, paired passage couplings and explicit conservative geometry.
The 2D editor retains paired legs, geometry, parameters and runtime setpoints.
Published storedEnergyJ/externalHeatW sum represented sensible stores/sources;
mechanical expansion tanks have empty sums (zero). Gas energy and pressure-volume
work remain excluded, without an invented tank thermal inventory.

summary.plant stores temperatureC, pressureKpa, dropKpa, flowLpm and heatMW on
run.times, separately from rack summaries. query_results and viewer
hover/series resolve these from every saved DU view. liquidHeatKW reports
positive absorbed plate/CRAH heat, positive chiller evaporator removal,
positive condenser rejection (evaporator plus compressor duty), and positive
tower rejection. Select the condenser solver edge explicitly to inspect its
distinct duty; the chiller asset defaults to the evaporator.

thermalDiagnostics.energy.circuits separates TCS, HTFW, MTFW/CHW and CW
storage changes, external heat, HX exchange and boundary exchange.
Electrical terms distinguish pump, compressor/auxiliary and tower/CRAH fan
power. totalElecPowerW, totalCoolingElecJ, pueCooling and plantCop retain their
declared represented-load basis. Sampled cumulative residualJ uses quadrature;
the instantaneous Engine balance defect remains a separate certificate.
All geometry and plant ratings are illustrative unless a declared physical
source replaces them. Static admission and saved samples do not certify
OEM operation, continuous safety, spatial accuracy or trajectory gradients.

## Conservative and reduced estimation boundaries

Conservative is the default where admitted. Reduced remains frozen and explicit;
its quasi-steady HX/transparent-pipe behavior must not be applied to conservative
models, which retain declared inventories and transport dynamics. Discover actual
component/model applicability instead of combining schema-listed features.

`assimilate_states` supports first-order conservative backward-Euler EKF and
fixed-window MHE alongside reduced frozen-inlet linearly implicit Euler estimation.
Conservative dynamic states must be independent Kelvin storage aliases such as
`ode_state:coil.T_coil` or `ode_state:pipe.T_cv_0`; algebraic junctions,
mechanical references, overlapping aliases and raw Joule energy keys are rejected.
Pressure, flow, liquid-node temperature, ODE temperature and electrical-power
telemetry may be combined. The joint state-plus-parameter limit is 64.
Declare selected scalar states, bounded slow parameters, SI prior variances and
per-second process variance rates. Pass `result.continuation` with unchanged
model/options to continue. Do not switch physical models silently or reset
physical/control continuation merely to make a request run.

Optional inertia/coast-down, field plates, expansion references and shared primary
coupling have joint applicability limits. Read static admission and actual
execution reports. Unsupported combinations must fail visibly rather than
falling back to different physics. Complete-trajectory gradient qualification is
separate from local derivative interfaces.
