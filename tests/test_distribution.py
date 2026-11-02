from html.parser import HTMLParser


import json


import os


from pathlib import Path


import queue


import shutil


import subprocess


import threading


import time


import pytest


ROOT = Path(__file__).resolve().parents[1]


PLUGIN = ROOT / 'plugins/diffliquidtwin'


def test_marketplaces_resolve_the_thin_codex_plugin():
    for base in (ROOT, ROOT / 'plugins'):
        catalog = json.loads((base / '.agents/plugins/marketplace.json').read_text())
        entry = next(item for item in catalog['plugins'] if item['name'] == 'diffliquidtwin')
        assert entry['source']['path'].startswith('./')
        assert (base / entry['source']['path']).resolve() == PLUGIN
    manifest = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text())
    assert manifest['name'] == 'diffliquidtwin'
    assert (PLUGIN / 'skills/diffliquidtwin/SKILL.md').is_file()
    for field in ('logo', 'logoDark', 'composerIcon', 'composerIconDark'):
        assert (PLUGIN / manifest['interface'][field]).is_file()
    # Package contents are an installation contract: no local runtime or UI can
    # hide a deployment error by taking the place of the service-owned App.
    assert {path.name for path in PLUGIN.iterdir()} == {
        '.codex-plugin', '.claude-plugin', '.mcp.json', 'skills', 'assets', 'README.md',
        'GETTING_STARTED.md'}


def test_claude_marketplace_resolves_the_same_thin_plugin():
    catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
    assert catalog['name'] == 'rda-cooling-lab'
    entry = next(item for item in catalog['plugins'] if item['name'] == 'diffliquidtwin')
    assert entry['source'].startswith('./')
    assert (ROOT / entry['source']).resolve() == PLUGIN
    claude = json.loads((PLUGIN / '.claude-plugin/plugin.json').read_text())
    codex = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text())
    # One package, two client manifests: identity, release and the remote
    # server declaration must not drift between hosts.
    assert claude['name'] == codex['name'] == entry['name']
    assert claude['version'] == codex['version'] == entry['version']
    assert claude['mcpServers'] == codex['mcpServers'] == './.mcp.json'
    assert (PLUGIN / claude['skills']).resolve() == (PLUGIN / codex['skills']).resolve()
    # OAuth client details belong to the host's discovery (CIMD/DCR), never
    # to the published package.
    assert not {'oauth', 'clientId', 'clientSecret', 'headers', 'env'} & set(claude)


def test_installed_claude_validator_accepts_plugin_and_marketplace():
    claude = shutil.which('claude')
    if claude is None:
        pytest.skip('Claude Code CLI is required for native manifest validation')
    for target in (PLUGIN, ROOT):
        result = subprocess.run([claude, 'plugin', 'validate', '--strict', str(target)],
                                capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, result.stdout + result.stderr


def test_installed_codex_parser_discovers_the_remote_server(tmp_path):
    codex = shutil.which('codex')
    if codex is None:
        pytest.skip('Codex CLI is required for native plugin-loader acceptance')
    # Exercise the consumer: unsupported manifest fields otherwise produce an
    # apparently valid plugin with an empty server list. No user config/login
    # is read or changed, and plugin/read never connects to the MCP endpoint.
    codex_state = tmp_path / 'codex-state'
    codex_state.mkdir()
    replies = queue.Queue()
    with (tmp_path / 'codex-stderr.log').open('w') as log:
        process = subprocess.Popen([codex, 'app-server'], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=log, text=True, bufsize=1,
            cwd=tmp_path, env=dict(os.environ, CODEX_HOME=str(codex_state)))

        def read_lines():
            for line in process.stdout:
                try:
                    replies.put(json.loads(line))
                except json.JSONDecodeError:
                    continue

        reader = threading.Thread(target=read_lines, daemon=True)
        reader.start()

        def request(request_id, method, params):
            process.stdin.write(json.dumps(dict(id=request_id, method=method, params=params)) + '\n')
            process.stdin.flush()
            deadline = time.monotonic() + 15
            while time.monotonic() < deadline:
                response = replies.get(timeout=max(.1, deadline-time.monotonic()))
                if response.get('id') == request_id:
                    assert 'error' not in response, response
                    return response['result']
            raise TimeoutError(f'Codex did not answer {method}')

        try:
            request(1, 'initialize', dict(clientInfo=dict(name='dlt-package-test', version='1'),
                                          capabilities=dict(experimentalApi=True)))
            process.stdin.write('{"method":"initialized","params":{}}\n')
            process.stdin.flush()
            result = request(2, 'plugin/read', dict(
                marketplacePath=str(ROOT / '.agents/plugins/marketplace.json'), pluginName='diffliquidtwin'))
            assert result['plugin']['mcpServers'] == ['diffliquidtwin']
        finally:
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
            reader.join(timeout=2)

