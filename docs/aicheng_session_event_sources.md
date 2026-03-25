# 艾橙 session-event 候选来源清单

## 当前阶段可用来源（按优先级）

### 1. 项目进度文档 `progress.md`
适合抽取：
- 当前阶段决定
- 已完成/待完成节点
- 本轮有效的执行策略

### 2. 当日记忆 `memory/YYYY-MM-DD.md`
适合抽取：
- 当天仍有效的老板要求
- 本轮明确拍板的执行约束
- 本轮仍有效的中间决策

### 3. 项目专项规范文档
适合抽取：
- 当前阶段约束
- 已确认的工作流边界
- 与艾橙当前实现直接相关的规则

候选文档：
- `docs/agent_memory_vs_self_evolution_plan.md`
- `docs/aicheng_session_event_reflection_hint_spec.md`
- `docs/aicheng_lightweight_auto_injection_plan.md`
- `docs/aicheng_agent_memory_alignment.md`
- `docs/aicheng_injection_execution_order.md`

### 4. 最近一次明确拍板的聊天结论
适合抽取：
- “模型先不动”
- “只保留三档社交距离”
- “艾橙重写完成后要主动回报”

---

## 不应作为 session-event 来源的内容
- 普通闲聊废话
- 角色卡正文
- 长期稳定偏好（应进 Agent memory）
- 已过期的临时情绪波动

---

## 当前建议
当前先从以下两类里抽：
1. `progress.md`
2. `memory/YYYY-MM-DD.md`

这两类已经足够覆盖当前项目的大部分有效 session-event。