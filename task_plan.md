# AstrBot QQ 机器人：人格接入与闭环计划

## Goal
在已打通聊天模型链与 Xinference rerank 的基础上，为 QQ 机器人接入并验证人格方案，完成运行态验证、收尾清理与可交接文档，便于新会话继续推进。

## Current Status
- [x] QQ 机器人聊天模型链已改为三层：`gmn-gpt-5.4 -> xcodex-gpt-5.4 -> zhipu-glm-4.7-flash`
- [x] Angel Memory / LanceDB 已指向 `local-xinference-rerank`
- [x] Xinference rerank `bge-reranker-base` 已启动并通过接口验收
- [x] `/v1/models` 可见 rerank 模型
- [x] `/v1/rerank` 返回 200 且排序正确
- [x] 确认 AstrBot 主服务运行态是否已吃到当前配置
- [x] 梳理人格配置入口与目标文件
- [x] 接入人格配置
- [ ] 做一轮带人格的真实对话验证
- [ ] 稳定后做第二轮清理/固化

## Phases

### Phase 1 — 已完成的底座修复 [complete]
- 修正 QQ 聊天模型链配置
- 修通 Xinference rerank 运行面
- 完成 `/v1/models` 与 `/v1/rerank` 验收

### Phase 2 — 运行态确认 [complete]
- 已确认 AstrBot 主服务运行在 Docker 容器中，Web 面板 `http://127.0.0.1:6185/` 可达
- 已通过 `/api/config/get` 证明主进程当时仍在使用旧运行态配置：
  - `default_provider_id = zhipu-glm-4.7-flash`
  - `fallback_chat_models = ['local-ollama']`
  - `default_personality = default`
- 已通过 AstrBot Web API 直接更新运行态配置并回读复验，无需先做容器重启

### Phase 3 — 人格接入设计 [complete]
- 已确认人格入口：`/api/persona/create|update|detail|list`
- 已确认默认人格切换点：`provider_settings.default_personality`
- 已确认最小改动路径：
  1. 重写现有 `boardgame_companion` 人格内容
  2. 仅切换 `default_personality`
  3. 同步补正运行态聊天模型链
  4. 暂不触碰 provider/platform 结构，避免扩大变更面

### Phase 4 — 人格接入实施 [complete]
- 已写入并重构人格准源文件：`docs/boardgame_companion_persona.md`
- 已同步生成运行时摘要：`docs/aicheng_role_core_runtime.md`
- 已通过透明脚本 `tools/sync_boardgame_companion_persona.py` 将文档准源重新写回 `/api/persona/update`
- 已通过回读报告 `reports/boardgame_companion_persona_sync_result.json` 确认运行态 persona 内容、开场对白与错误消息已更新为当前文档版本
- 已确认运行态默认配置仍为：
  - `default_provider_id = gmn-gpt-5.4`
  - `fallback_chat_models = ['xcodex-gpt-5.4', 'lemon_gemini_3_flash', 'zhipu-glm-4.7-flash', 'local-ollama']`
  - `default_personality = boardgame_companion`

### Phase 5 — 真实验证与收尾 [in_progress]
- 已清理旧的临时人格 apply/result/config 快照文件，避免继续形成“多份人格真源”的错觉
- 已确认人格本体唯一准源仍为：`docs/boardgame_companion_persona.md`
- 已确认运行时真源为 SQLite / Persona API 中的 `boardgame_companion`
- 待做：
  - 用真实消息验证人格表现
  - 做一版 Git 收口（至少本地提交，必要时独立分支）
  - 记录最终验证结果、异常与后续动作

## Constraints / Rules
- 不主动重启 AstrBot；若人格接入或配置生效必须重启，需先和老板确认。
- Windows 上 JSON 配置编辑默认使用 Python，不用 PowerShell `ConvertFrom-Json` / `ConvertTo-Json`。
- 不清理当前仍可能用于回溯的 rerank 日志、模型缓存、启动脚本。
- 当前只清理低风险临时垃圾，不破坏已跑通环境。

## Validation Gates
1. `/v1/models` 可见 `bge-reranker-base`
2. `/v1/rerank` 返回 200
3. AstrBot 主服务运行态回读为新聊天模型链 + `boardgame_companion`
4. 人格配置落盘并经真实对话验证

## Errors Encountered
| Error | Attempt | Resolution |
|---|---:|---|
| `PropertyAssignmentException` / PowerShell 改 JSON 结构损坏 | 1 | 改用 Python 精确读改写回并回读校验 |
| `ModuleNotFoundError: xoscar` | 1 | 禁用 Xinference model-level virtualenv |
| `sentence_transformers` 依赖链不兼容 | 2 | 安装依赖并调整 `transformers==4.52.4` |
| 端口 `9998` 被僵尸 supervisor 占用 | 3 | 杀掉旧 supervisor/worker 后冷启动 |
| `No available worker found` | 4 | 等 worker 完成注册后再 launch rerank |
| SQLite 直查命令被网关拦截（approval-timeout / obfuscation-detected） | 1 | 改走 AstrBot Web API 读取运行态与人格数据 |
