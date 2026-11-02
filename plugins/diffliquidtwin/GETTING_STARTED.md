# RDA Cooling Lab：Codex 与 Claude Code 安装与登录

薄插件连接 `https://diffliquidtwin-mcp.demo.rda.ai/mcp`。宿主（Codex 或 Claude Code）负责通过 [Red Dot AI 统一认证中心](https://auth.internal.rda.ai) 登录、保存 token 和刷新凭据。插件使用端无需 Python、Node、Torch 或本地后端。


## Codex 安装

在 Codex 的插件目录中添加本仓库的 marketplace，再安装 **RDA Cooling Lab**。仓库中 `.agents/plugins/marketplace.json` 指向 `plugins/diffliquidtwin`；只分发这个目录即可。包内 `.codex-plugin/plugin.json` 引用 `.mcp.json`，后者只配置 `type:"http"` 和远程 MCP URL，由 Codex 自动发现认证信息。已有插件连接时，不再添加同 URL 的手工 MCP 条目。

安装或连接时完成浏览器中的 Red Dot AI 登录。登录后在对话中请求创建冷却场景，调用 `open_hall` 打开原生交互面板。界面提供独立的 English / 中文切换。

## Claude Code 安装

在 Claude Code 会话中添加本仓库 marketplace 并安装插件：

```
/plugin marketplace add RDA-SG/diffliquidtwin-plugins
/plugin install diffliquidtwin@rda-cooling-lab
```

命令行等价写法为 `claude plugin marketplace add RDA-SG/diffliquidtwin-plugins` 和 `claude plugin install diffliquidtwin@rda-cooling-lab`。仓库根目录的 `.claude-plugin/marketplace.json` 指向同一个 `plugins/diffliquidtwin` 目录；包内 `.claude-plugin/plugin.json` 引用同一个 `.mcp.json` 和 skill。

安装后在会话中运行 `/mcp`，选择 `diffliquidtwin` 服务器，在浏览器中完成 Red Dot AI 登录。无浏览器环境可使用 `claude mcp login` 的 `--no-browser` 选项。Claude Code 通过服务发现自动选择 CIMD 或 DCR，回调使用本机随机端口；插件不配置 `oauth.clientId` 或 `callbackPort`，回调地址由认证中心依据客户端元数据或注册信息校验。token 由 Claude Code 保存和刷新。`claude -p` 等非交互运行无法完成 OAuth 登录，需先在交互会话中登录。

插件提供的工具在 Claude Code 中以 `mcp__plugin_diffliquidtwin_diffliquidtwin__` 为前缀。交互 3D 面板是 Platform 提供的 MCP App，仅在支持渲染 MCP App 的宿主中显示；Claude Code 目前未说明支持渲染，因此在 Claude Code 中可以正常建模、仿真、查询结果和发布分析内容，但可能看不到面板。

## 部署者需要先完成的认证配置

认证中心需公布受保护资源 metadata、OAuth discovery、PKCE S256，并支持 CIMD 与 DCR。当前线上部署已具备这些能力。Codex 默认 `auto` 优先选择 CIMD，条件不满足时使用 DCR；Claude Code 同样自动发现 CIMD 或 DCR。认证中心从客户端元数据或注册信息校验宿主自己生成的回调。插件不固定 client ID、回调地址或端口。网页 SSO 保留自己的预注册配置。

宿主依据服务发现请求的 OAuth `resource` 是完整的 MCP URL，签发的 access token 必须将该 URL 放在 audience 中。服务端验证签名、issuer、过期时间、subject 和 audience，并向 Casdoor userinfo 检查 token 是否仍然有效。认证中心不可达时服务拒绝访问。

不要把 client secret、access token、refresh token 放进插件文件、对话、工具参数或仓库。插件没有静态 token 或本地配置文件的认证后门。

## 恢复实验

`open_hall()` 创建独立 workspace 和 session。后续状态工具都需要它返回的 `sessionId`。重新打开同一实验使用 `open_hall(sessionId=...)`；`list_workspaces` 可发现保存的实验。

`open_hall(workspaceId=...)` 为现有实验创建只读会话；`open_hall(sourceWorkspaceId=...)` 复制输入到可编辑实验，不复制大体积历史结果。当前服务向获得应用访问权限的团队账号提供共享实验库。

## 保留和清理

History 中的 **Keep** 保留结果和依赖，**Clean up** 先列出候选，再执行确认的删除。运行中的任务、在线查看中的内容和保留的依赖受到保护。关闭面板不会删除实验。Agent 使用 `get_storage_status`、`set_retention`、`cleanup_workspace` 执行同一工作流。

## 排错

登录失败时，确认 Casdoor 账号已获 DiffLiquidTwin 服务授权，再使用宿主的连接管理重新登录（Codex 的连接管理，或 Claude Code 的 `/mcp`）。安装插件本身不授予服务权限。

连接恢复后使用已有 sessionId 恢复实验。登录状态与实验会话分别管理，不需要为重新连接创建新实验。

服务端由 Red Dot AI 维护；插件不携带本地 Python bridge 或前端构建产物。问题反馈请使用此公开仓库的 Issues，并避免提交令牌、凭据或私有实验数据。

## 详细保留和清理规则

`Experiments` 显示团队共享实验，支持搜索、分页和每行直接删除。点击名称查看；
`Continue experiment` 复制输入后继续修改。当前实验的名称会返回原观察位置。
删除前会列出仿真、场景和分析数量，并提示将删除保留内容与关联会话；运行或排队
中的任务须先取消。查看旧实验的只读状态不影响目录中的实验管理入口。

新工作区和新仿真默认是临时内容。History 中的 `Keep` 保留选定结果，工作区菜单
中的保留操作保存当前输入及选定的结果和解释；之后的新试跑仍按临时规则回收。
也可直接告诉 Codex 或 Claude：“保留这个结果和解释作为团队示例”。保留的分析保护它实际
引用的结果。查询和实际查看会延长使用时间，列表、后台轮询和健康检查不会。

默认期限为：未编辑且未运行的空工作区 24 小时；失败、取消、中断任务 7 天；成功
临时仿真 14 天；闲置临时工作区 30 天。期限从结束或最近实际使用时间计算。
最近一次成功结果至少保留至工作区最近实际使用后的 30 天；保留工作区也使用这个
有限期限，明确 Keep 的结果和分析来源持续保留。排队、运行和在线查看的内容受到保护。
服务端每小时检查到期内容，并在接纳新计算前检查容量。清理不会自动取消任务。

History 的 `Clean up` 预览当前工作区的候选、预计释放空间及跳过原因，执行时
重新检查状态。可以让 Codex 或 Claude 清理当前实验中的失败或过期试跑。删除保留内容需要
明确包含保留内容；删除整个实验会删除输入、场景、负载、结果、分析和关联会话。
关闭面板或会话不删除实验，重启服务保留未过期的数据。

agent 使用 `get_storage_status` 查看容量和当前工作区规则，`set_retention` 设置
工作区、运行或分析内容的保留状态，`cleanup_workspace` 预览及执行当前工作区的
清理。所有操作携带当前 `sessionId`。执行批次使用预览返回的明确运行 ID，防止
预览之后的新任务被纳入删除。全团队自动回收由服务端统一规则执行。

清理报告区分文件逻辑大小、预计可回收大小和实际释放空间；分析快照可能有硬链接，
删除原结果未必释放其全部大小。结果删除后旧会话显示来源不可用，不会自动跳到
另一套结果。文件清除失败时，内容先从实验中移除，报告待清除空间和警告，服务端
稍后重试；只有磁盘实际释放的空间计入释放量。Casdoor OAuth 登录后使用团队公共权限，
不提供个人数据隔离。
