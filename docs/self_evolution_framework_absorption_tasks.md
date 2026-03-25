# self_evolution 架构吸收任务清单（收口版）

## 总目标
不直接安装 `astrbot_plugin_self_evolution`，保留当前 Agent memory 作为唯一长期记忆底座；只吸收其对当前体系真正有价值的架构能力，并明确边界、顺序、容器与不采纳项。

---

## 已完成

### 1. 保留策略确定
- 已确认：保留 **Agent memory / OpenClaw memory** 作为唯一长期记忆真源
- 已确认：`self_evolution` 不作为主记忆插件安装接管

### 2. 架构价值判断
- 已确认值得吸收的三类核心设计：
  1. 记忆分层
  2. 查询按意图分流
  3. 轻量反思
- 已确认不直接吸收：
  - affinity
  - SAN
  - 主动插嘴
  - 元编程
  - 重型 prompt 注入
  - 每日总结大系统

### 3. 设定 / 记忆 / 事件边界已建立
已形成以下文档：
- `docs/agent_memory_vs_self_evolution_plan.md`
- `docs/aicheng_session_event_reflection_hint_spec.md`
- `docs/aicheng_agent_memory_alignment.md`

### 4. 轻量自动注入框架已建立
已形成以下文档：
- `docs/aicheng_lightweight_auto_injection_plan.md`
- `docs/aicheng_role_core_runtime.md`
- `docs/aicheng_injection_execution_order.md`

### 5. 中间层候选来源已建立
已形成以下文档：
- `docs/aicheng_session_event_sources.md`
- `docs/aicheng_reflection_hint_sources.md`

---

## 本轮吸收任务的最终产出
框架层面已经吸收到当前体系的内容：

### A. 写入分层
- 角色硬设定 → 人格卡 / role-core
- 长期稳定事实 → Agent memory
- 当前项目事件 → session-event
- 短期纠偏 → reflection-hint

### B. 查询分流
- 人格问题 → role-core / 角色卡
- 长期事实问题 → Agent memory recall
- 当前项目连续状态 → session-event
- 最近风格纠偏 → reflection-hint

### C. 轻量自动注入
注入顺序固定为：
1. role-core
2. relevant-memory
3. session-event
4. reflection-hint

---

## 明确不纳入本轮范围
以下内容本轮不做，不再继续扩张：
- 安装 `self_evolution`
- 替换 Agent memory
- 引入 SAN / affinity / interject
- 引入自动人格漂移
- 引入重型 scope 知识库日报体系
- 引入代码级元编程 / 自我修改

---

## 后续若继续推进，只剩两条实现向任务

### Task 1 — session-event 轻量容器化
目标：
- 不再只靠 scattered 文档/日记人工承载
- 给 session-event 一个稳定轻量容器

最小建议：
- `docs/aicheng_session_events.jsonl`

### Task 2 — reflection-hint 轻量容器化
目标：
- 让短期纠偏不再散落在进度文档和日记里
- 控制其 TTL，避免越积越多

最小建议：
- `docs/aicheng_reflection_hints.jsonl`

---

## 当前阶段结论
如果以“是否完成框架吸收任务”来判断：

**是，框架吸收任务已经完成到可收口状态。**

现在缺的不是“继续想架构”，而是：
- 要不要把 session-event 做成轻量容器
- 要不要把 reflection-hint 做成轻量容器

如果老板暂时不要求继续工程化，这一波可以视为完成。