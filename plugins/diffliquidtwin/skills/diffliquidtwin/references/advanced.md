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

Use advertised calibrate_parameters, optimize_controls, optimize_design,
analyze_observability and design_sensors for supported bounded scalar Engine
parameters/observations. These are separate jobs; they do not mutate current
inputs. Read-only sessions cannot execute. Existing cancellation/retention applies.
Declare physical bounds and scales for mixed pressure/temperature/flow objectives.
Use actual Engine attribute names and units, not presentation labels.

executionScope=initial concerns the operating point. Where advertised, scenario
scope and observationTimesS follow actual Hall warmup/control/event clocks with
right-continuous samples. Generic schedules or unsupported objectives need an
explicitly requested Python workflow. AD interface support does not establish a
complete trajectory's gradient grid accuracy. Respect paused studies and the
user's compute scope; retain live tensors across differentiable wrappers.

## Explicit reduced-only capabilities

Conservative is the default where admitted. Reduced remains frozen and explicit;
its quasi-steady HX/transparent-pipe behavior must not be applied to conservative
models, which retain declared inventories and transport dynamics. Discover actual
component/model applicability instead of combining schema-listed features.

Existing reduced EKF/fixed-window MHE requires an explicit supported reduced
selection. Declare states, slow parameters, SI prior/process variances and
continuation consistently. Do not switch physical models silently or reset
physical/control continuation merely to make a request run.

Optional inertia/coast-down, field plates, expansion references and shared primary
coupling have joint applicability limits. Read static admission and actual
execution reports. Unsupported combinations must fail visibly rather than
falling back to different physics. Complete-trajectory gradient qualification is
separate from local derivative interfaces.
