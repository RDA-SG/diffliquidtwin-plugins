# Advanced Python analysis and differentiable tasks

Read this for requested analysis/objectives beyond ordinary JSON simulation.
Discover current schemas and actual applicability; this is not a tool catalog.

## Python execution and publication

run_analysis uses a supported executable scene or immutable saved-run source and
the shared asynchronous scheduler. Inspect the actual worker context and APIs;
ctx exposes model, scene, scenario and output directory. Publish numerical fields
through ctx.publish and artifacts through ctx.publish_artifact. Fields use exact
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
(static setpoints), `optimize_design`, `analyze_observability`, `design_sensors`
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
right-continuous samples. Generic schedules or unsupported objectives need an
explicitly requested Python workflow. AD interface support does not establish a
complete trajectory's gradient grid accuracy. Respect paused studies and the
user's compute scope; retain live tensors across differentiable wrappers.

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

## Explicit reduced-only capabilities

Conservative is the default where admitted. Reduced remains frozen and explicit;
its quasi-steady HX/transparent-pipe behavior must not be applied to conservative
models, which retain declared inventories and transport dynamics. Discover actual
component/model applicability instead of combining schema-listed features.

`assimilate_states` uses reduced EKF/fixed-window MHE and requires an explicit
supported reduced selection; conservative energy-state assimilation is unsupported.
Declare selected scalar states, bounded slow parameters, SI prior variances and
per-second process variance rates. Pass `result.continuation` with unchanged
model/options to continue. Do not switch physical models silently or reset
physical/control continuation merely to make a request run.

Optional inertia/coast-down, field plates, expansion references and shared primary
coupling have joint applicability limits. Read static admission and actual
execution reports. Unsupported combinations must fail visibly rather than
falling back to different physics. Complete-trajectory gradient qualification is
separate from local derivative interfaces.
