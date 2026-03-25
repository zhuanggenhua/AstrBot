# Findings — AstrBot QQ 机器人 / rerank / 人格准备

## 已确认事实
- QQ 机器人实际项目目录：`C:\Users\zhuagenbao\.openclaw\workspace\apps\astrbot\AstrBot`
- 聊天模型目标主链：
  - `default_provider_id = gmn-gpt-5.4`
  - `fallback_chat_models = ['xcodex-gpt-5.4', 'zhipu-glm-4.7-flash']`
- Angel Memory 已配置：
  - `retrieval.rerank_provider_id = local-xinference-rerank`
- rerank provider 已存在于 `data/cmd_config.json`：
  - `id = local-xinference-rerank`
  - `provider_type = rerank`
  - `rerank_api_base = http://host.docker.internal:9997`
  - `rerank_model = bge-reranker-base`

## 本次排障结论
- 真正卡点主要不在 AstrBot provider 代码，而在 Xinference rerank 运行态。
- 修通路径包括：
  1. 关闭 Xinference 子虚拟环境
  2. 补齐 `tiktoken / protobuf / sentencepiece / sentence-transformers`
  3. 将 `transformers` 调整到与当前依赖兼容的 `4.52.4`
  4. 清理占用 `9998` 的僵尸 supervisor
  5. 在 worker 完成注册后再次 launch
- 最终验收结果：
  - `GET http://127.0.0.1:9997/v1/models` 返回 `bge-reranker-base`
  - `POST http://127.0.0.1:9997/v1/rerank` 返回 200 且排序正确

## 运行态确认结论（Phase 2）
- AstrBot 主服务运行在 Docker 容器中，面板地址：`http://127.0.0.1:6185/`
- 关键证据来自 AstrBot Web API，而不是磁盘文件猜测：
  - `GET /api/config/get` 初次回读显示主进程仍在用旧运行态：
    - `default_provider_id = zhipu-glm-4.7-flash`
    - `fallback_chat_models = ['local-ollama']`
    - `default_personality = default`
- 结论：此前磁盘 `cmd_config.json` 虽已改好，但运行态并未自动吃到
- 处理方式：未重启容器，直接通过 `POST /api/config/astrbot/update` 修正运行态并同步落盘
- 修正后回读：
  - `default_provider_id = gmn-gpt-5.4`
  - `fallback_chat_models = ['xcodex-gpt-5.4', 'zhipu-glm-4.7-flash']`
  - `default_personality = boardgame_companion`

## 人格接入结论（Phase 3 / 4）
- 人格配置入口已确认：
  - `GET /api/persona/list`
  - `POST /api/persona/detail`
  - `POST /api/persona/create`
  - `POST /api/persona/update`
- 默认人格切换点已确认：`provider_settings.default_personality`
- 现有人格池中已有 `boardgame_companion`
- 原 `boardgame_companion` 内容已损坏（数据库/API 返回为大量 `?`），不适合继续沿用
- 最小改动方案：
  1. 保留 persona_id：`boardgame_companion`
  2. 直接重写其 system prompt / begin dialogs / custom error message
  3. 仅把默认人格切换到 `boardgame_companion`
  4. 不改 provider/platform 结构
- 人格草案文件已保存：`docs/boardgame_companion_persona.md`
- 老板后续补充了正式版“小林玖奈”人格设定，用于直接覆盖之前临时版桌游陪玩人格。
- AstrBot 的 `begin_dialogs` 有额外约束：数量必须为偶数，按用户/助手轮流预设；首次回写正式人格时因此被拒。
- 修正 `begin_dialogs` 为 4 条后，可继续作为合法人格载荷写回。

## Gemini 首选 + fallback 新结论
- 已新增 OpenAI 兼容 provider source：`lemon_gemini_openai_source`
  - 指向用户提供的中转地址（已配置成功）
- 已新增并切换首选 provider：`lemon_gemini_3_flash`
  - 模型：`[L]gemini-3-flash-preview`
- 已按老板要求把 fallback 顺序配置为：
  1. `gmn-gpt-5.4`
  2. `xcodex-gpt-5.4`
  3. `zhipu-glm-4.7-flash`
  4. `local-ollama`
- 但点检结果表明：
  - `lemon_gemini_3_flash`：available
  - `gmn-gpt-5.4`：unavailable，原因是当前中转侧返回 `model_not_found`（`gpt-5.4` 不可用 / 账户级别不支持）
  - `xcodex-gpt-5.4`：unavailable，原因同上
  - `zhipu-glm-4.7-flash`：available
  - `local-ollama`：unavailable（本地连接错误）
- 结论：配置顺序已按要求落盘并实时生效，但在“真实可用性”上，目前有效链路实际等价于：
  - `Gemini 3 Flash -> GLM -> (若修好) 本地 Ollama`

## 人格真源与运行时收口结论（2026-03-25 夜）
- 人格本体唯一准源：`docs/boardgame_companion_persona.md`
- 运行时真正生效的人格真源：`data/data_v4.db` 的 `personas` 表，以及其对应的 `/api/persona/detail|update` 接口
- `docs/aicheng_role_core_runtime.md`、`docs/aicheng_session_events.jsonl`、`docs/aicheng_reflection_hints.jsonl` 都是辅助层，不是人格本体真源
- 之前仓库里存在旧的临时同步脚本：
  - `temp_apply_aicheng_persona.py`
  - `temp_apply_kobayashi_persona.py`
  它们会把文档重新写回 persona API，因此确实构成了“除人格文档外还有回写链路”
- 当前已新增透明、单一、可复用的同步脚本：`tools/sync_boardgame_companion_persona.py`
  - 输入：`docs/boardgame_companion_persona.md`
  - 输出：`/api/persona/update`
  - 校验报告：`reports/boardgame_companion_persona_sync_result.json`
- 旧的临时 apply/result/config/persona 快照文件已清理，避免继续制造多份来源错觉
- 运行态默认配置当前回读为：
  - `default_personality = boardgame_companion`
  - `default_provider_id = gmn-gpt-5.4`
  - `fallback_chat_models = ['xcodex-gpt-5.4', 'lemon_gemini_3_flash', 'zhipu-glm-4.7-flash', 'local-ollama']`

## 还未拿到铁证的点
- 还没做 QQ 侧真实对话验证，所以“运行态配置正确”已经确认，但“实际回复表现符合人格”还没完全闭环。
- 若真实聊天仍异常，优先排查：
  1. QQ 平台入口是否把会话正确送入当前 provider 链
  2. 日志里是否仍有外部 provider 连接失败
  3. 是否有会话级 persona / plugin 逻辑覆盖默认人格

## 低风险清理策略
- 可以清：`%TEMP%` 下本次临时验证脚本（如 `rerank_verify*.py`）
- 暂不清：
  - `temp/xinference-rerank/home/cache`
  - `supervisor*.log`
  - `worker*.log`
  - `start-supervisor-detached.ps1`
  - `start-worker-detached.ps1`
  - 已验证有效的运行面补丁
  - 本轮新增的 API 快照 / 人格草案，待真实验证后再决定是否清理

## 新会话建议入口
新会话可直接从以下问题切入：
1. 发送一条真实 QQ 消息，验证 `boardgame_companion` 是否已生效
2. 若未生效，抓 `docker logs astrbot --tail 200` 看 provider / platform 路径
3. 若已生效，补一轮验证记录并做第二轮清理
