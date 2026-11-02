# DiffLiquidTwin Plugins 开发指引

## 本仓库职责

本仓库 `RDA-SG/diffliquidtwin-plugins` 是公开的客户端插件仓库，维护 marketplace 清单、插件清单、skills、展示资源、安装说明及客户端适配。

- 当前 Codex 插件位于 `plugins/diffliquidtwin/`。根目录 `.agents/plugins/marketplace.json` 是主要 marketplace 入口，`plugins/.agents/plugins/marketplace.json` 支持本地注册；不要同时注册两个同名 marketplace。
- Claude 等客户端适配可以放在本仓库，分别维护各自的清单、安装入口和格式验证。共享内容按实际兼容性复用，保证现有客户端仍可安装和使用。
- 插件通过远程 HTTP MCP 使用 Platform。服务端负责前端页面、仿真、持久化和授权；本仓库不打包后端、Engine 或前端构建产物。
- 任何人可以安装插件，使用服务需要获得 Casdoor 授权。MCP 使用客户端原生 OAuth，优先 CIMD、兼容 DCR，并采用 PKCE S256。凭据由客户端宿主管理；不在插件中写死 client secret、token、回调端口或客户端身份来绕过发现和授权。
- 公开内容不得包含凭据、私有实验数据或内部部署配置。

## 关联仓库与位置

仓库 URL 是权威标识；以下相对路径仅描述常见的同级 checkout 布局，不是构建或安装前提。独立 worktree 中应重新定位目标仓库，核对 remote，不能直接假设 `../` 指向正确目录。

| 仓库 | 地址 | 常见本地位置 | 职责与基线 |
| --- | --- | --- | --- |
| Platform | https://github.com/RDA-SG/diffliquidtwin-platform | `../diffliquidtwin-platform` | MCP、OAuth 集成、Web UI、存储、部署；`main` |
| RDA Engine | https://github.com/cap-dcwiz/DiffLiquidTwin | `../diffliquidtwin-engine` | 模型、求解器和性能优化；`rda/main`。`main` 跟踪上游 |
| Engine 上游 | https://github.com/ZHANG-QINGANG/DiffLiquidTwin | `../DiffLiquidTwin` | 上游持续开发与通用改进贡献；目标分支按贡献任务确认 |

修改 HTML、JavaScript、CSS 或 MCP 原生面板时，到 Platform 的 `ui/` 开发、构建和验证；其 MCP 默认提供构建后的 `ui/dist/hall.html`。修改认证服务端、MCP 工具或部署也归 Platform。修改求解器归 RDA Engine。上游默认只读参考，贡献需有对应任务授权。

## 跨仓库开发与并行任务

1. 开始前明确涉及的仓库和验收结果，检查每个实际 checkout 的路径、remote、分支、工作区状态及 `git worktree list`。读取目标仓库的根和路径范围内 `AGENTS.md`；多文件夹项目的主目录指令不会替代附加仓库指令。
2. 本仓和 Platform 通常从确认过的最新 `main` 建立任务分支，Engine 从 `rda/main` 建立；默认前缀为 `codex/`，用户明确指定的命名优先。
3. 并行写入时，每个将修改的仓库使用独立分支和独立 worktree。Codex 自动 worktree 仅隔离主仓库，附加目录可能仍是共享 checkout。记录任务实际路径，并使用显式 cwd 或 `git -C <checkout>` 执行操作。
4. 保留其他任务的未提交改动、分支和环境；不擅自 stash、reset、clean 或切换共享 checkout 的分支。并行任务隔离可变虚拟环境、构建目录、数据库及服务端口。
5. 各仓分别提交和审查，记录配套接口及版本依赖。涉及依赖变化时通常按 Engine → Platform → Plugins 验证；Platform 发布使用固定 Engine commit 或不可变制品版本。跨仓提交没有原子性，需要保持中间版本兼容。
6. 跨仓修改时检查 Platform 的开发与发布约束；没有本地 checkout 或权限时，先完成不依赖它的工作，再明确报告缺失信息或权限。不要为插件单仓任务自动拉取、修改或部署其他仓库。
7. 完成后报告各仓提交、安装方法、测试结果及未验证项。生产部署按用户授权执行。确认成果已保存且任务验收后，清理本任务的临时 worktree 与可重建产物，保留未保存成果和必要证据。

## 验证

插件内容或清单变化时，执行现有检查：

```bash
python -m pytest tests
node --test tests/test_plugin_listing.mjs
```

Python loader 验收需要可运行的 Codex CLI。新增客户端适配时，增加对应的真实格式、加载或安装验证，检查已有 Codex 安装兼容性。MCP 接口或认证变化还需要针对目标服务验证客户端实际采用的发现、登录及工具调用流程。

仅文档变更按影响检查准确性、路径和 Git diff，无需为说明文字增加占位测试。包验证、在线 MCP 调用及原生面板验收分别报告；本地预览或后端状态不能代替原生面板实际验收。
