# Connecting another harness to DiffLiquidTwin

This guide is for agents implementing a Claude or other harness package. Reuse the existing remote MCP service, tool contracts and MCP App frontend. This repository currently provides a Codex package; it does not include a tested Claude implementation.

## Repository boundaries

- This public repository contains client manifests, skills, installation instructions and display assets. Use the target harness's actual package format and keep each installation entry independently testable.
- Platform owns the MCP endpoint, OAuth resource validation, workspace state, job workers, result storage and the viewer bundle. Engine owns numerical integration and model execution. Neither belongs in a thin client package.
- The Codex references are [`plugin.json`](plugins/diffliquidtwin/.codex-plugin/plugin.json), [`.mcp.json`](plugins/diffliquidtwin/.mcp.json) and the [skill](plugins/diffliquidtwin/skills/diffliquidtwin/SKILL.md). They illustrate the boundary, not a manifest format to copy into another harness.

## Connection and OAuth

The hosted endpoint is `https://diffliquidtwin-mcp.demo.rda.ai/mcp`, using Streamable HTTP. Private deployments supply their own endpoint.

Use the harness's native OAuth client. Follow the endpoint's `401` challenge and protected-resource metadata, then authorization-server discovery. Use authorization code with PKCE S256, the advertised registration mechanism (CIMD or DCR when supported), and the endpoint's resource identifier in authorization and token requests. Let the harness generate its own callback and store and refresh credentials. Do not copy Codex's callback, client identity or cached tokens into another harness.

Client-registration support must be verified against the target harness and live discovery. If its native client cannot use the advertised registration mechanism, report that specific gap before adding an adapter or asking the authentication administrator for a pre-registered client. A static bearer-token example is not the normal installation path.

The service checks access-token validity and resource audience. Successful login to the same issuer alone does not grant access to this resource. Preserve rejection of expired, revoked, wrong-resource and ID tokens. Do not put user tokens, client secrets, deployment credentials or private configuration in this repository, skills, HTML or browser JavaScript.

## Tools, workspaces and sessions

Negotiate MCP with `initialize`, then read `tools/list` and `resources/list`. The server's current schemas are authoritative; avoid a copied tool catalog or a client-specific simulation API.

1. `open_hall({})` creates a workspace and editable application session. Keep its returned `sessionId` and `workspaceId`.
2. Pass that explicit `sessionId` to subsequent stateful tools. An MCP transport session and a DiffLiquidTwin application session have different lifetimes.
3. `open_hall({"sessionId":"…"})` reopens the same application session. `open_hall({"workspaceId":"…"})` opens an existing workspace read-only. Use `sourceWorkspaceId` to create an editable input copy when required; it does not copy historical results.
4. Use the returned draft revision for edits. On a revision conflict, reread the inputs and reconcile the human or agent's newer edit. After a transport timeout, query state before retrying a write or submitting another job.

Keep saved-run inputs and execution evidence separate from current draft edits. Async simulation tools return jobs that must be polled to a terminal state. Reopening a panel should reuse its saved session and results, without submitting another simulation. Preserve structured content, errors and metadata instead of flattening all responses into text.

## Reusing the MCP App

Obtain the UI resource from `open_hall` tool metadata (`_meta.ui.resourceUri`) or resource discovery; do not hardcode a resource version. The service publishes the viewer as `text/html;profile=mcp-app`. Run that resource in the harness's MCP App container with its declared CSP, theme, size, inputs and tool results.

Allow the App's `callServerTool` requests through the same authenticated connection. The `hall_api` tool is App-visible and carries `action`, `args` and `sessionId`; its response payload is in `_meta.payload`. Preserve that metadata and the server's visibility declarations. Model-facing tools retain their published names and schemas.

Keep the viewer's existing panel-instance binding and applied-state reporting. A requested camera or playback change is not proof the panel displayed it; inspect the applied revision and panel context. A reopened panel takes ownership according to the service's existing rules. Do not invent a new host/session routing layer.

Message, model-context attachment and fullscreen capabilities are optional and must follow capability negotiation. A harness without MCP Apps can still use the numerical tools, but cannot claim interactive viewer support. A standalone browser preview verifies page behavior only; the target harness needs its own native panel and screenshot checks.

## Solver configuration and results

New experiments use Engine `method="auto"` and `max_thermal_step_s=null`. `null` delegates thermal-step selection to Engine; zero is invalid. Positive caps and explicit methods remain available. Read current schemas rather than maintaining a separate method list. The service's configuration summary is suitable for ordinary inspection; request full configuration for detailed diagnosis.

Outer integration timing, control timing, output recording and internal thermal steps are distinct. Keep unchanged fields when patching one setting. Saved execution evidence records the actual methods, fallbacks, work and tolerance scope; a requested `auto` method or a successful run alone is not a global accuracy guarantee. Inspect model assumptions and result provenance before interpreting temperatures, flows or pressures.

## Minimum acceptance for a new harness

- Parse and install its real manifest; discover tools and the current UI resource.
- Complete native OAuth login, reconnect and refresh; verify an unauthenticated request is rejected. Do not rely on copied tokens.
- Create one explicit session; alternate human and agent edits and check revision conflicts without losing newer inputs.
- Read configuration summary and full detail; save an explicit method/cap and restore `auto`/`null` through the actual form and tool path.
- Run the default DSX experiment, inspect its immutable inputs and actual execution report, and load the saved result.
- If the harness supports MCP Apps, exercise Equipment/Cooling, component selection and Inspection, result playback, a screenshot, and reopening the same session without rerunning.
- Record which capabilities were actually tested. Keep a missing native panel capability visible instead of replacing it with an unrelated browser or backend-only claim.

Add only the target harness package and the smallest demonstrated transport adaptation. Backend deployment, OAuth policy changes and numerical changes require their own scoped work in their owning repositories.
