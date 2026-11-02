import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';

const plugin=new URL('../plugins/diffliquidtwin/',import.meta.url);
const manifest=JSON.parse(readFileSync(new URL('.codex-plugin/plugin.json',plugin),'utf8'));
const listing=manifest.interface;

test('Codex plugin listing contains valid starter prompts and packaged presentation assets',()=>{
  assert.ok(Array.isArray(listing.defaultPrompt));
  assert.ok(listing.defaultPrompt.length>0&&listing.defaultPrompt.length<=3);
  for(const prompt of listing.defaultPrompt){
    assert.equal(typeof prompt,'string');assert.ok(prompt.trim());
    assert.ok(!/[\r\n]/.test(prompt));assert.ok([...prompt].length<=128);
  }
  for(const field of ['logo','logoDark','composerIcon','composerIconDark']){
    const asset=listing[field];assert.ok(asset.startsWith('./assets/'));
    assert.ok(existsSync(new URL(asset,plugin)));
  }
});

test('remote MCP configuration leaves OAuth client discovery to the host',()=>{
  const {mcpServers}=JSON.parse(readFileSync(new URL('.mcp.json',plugin),'utf8'));
  const server=mcpServers.diffliquidtwin;
  assert.equal(server.type,'http');
  assert.equal(new URL(server.url).protocol,'https:');
  assert.deepEqual(Object.keys(server).sort(),['type','url']);
  assert.equal(manifest.mcpServers,'./.mcp.json');
});
