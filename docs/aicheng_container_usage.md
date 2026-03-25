# 艾橙轻量容器使用说明

## 已创建容器
- `docs/aicheng_session_events.jsonl`
- `docs/aicheng_reflection_hints.jsonl`

## 用途
### session_events.jsonl
记录当前项目/当前会话中仍然有效的重要事件、约定、决定、阶段状态。

### reflection_hints.jsonl
记录当前阶段仍然有效的短期纠偏提示，用于轻微扶正输出方式，不用于自动改人格本体。

## 读写规则
### session_event
适合写入：
- 仍然有效的项目决定
- 当前阶段模型/策略/工作流结论
- bug 排障中的关键状态

不适合写入：
- 长期稳定偏好（应进 Agent memory）
- 角色本体设定（应改角色卡）
- 已过期的临时情绪

### reflection_hint
适合写入：
- 当前阶段最重要的 1~5 条纠偏
- 用户明确指出的表达偏差
- 本轮执行中暴露出的高价值短期规则

不适合写入：
- 稳定人格定义
- 可直接升级为角色卡正文的内容
- 无时效性的旧提醒

## 维护规则
- `session_event` 保留 active 条目，过期后改为 `status: inactive` 或移除
- `reflection_hint` 默认短期有效；过期、已吸收进人格卡、或不再 relevant 时，标记 inactive 或删除
- 每次新增条目后，优先避免重复摘要
- 自动注入时：
  - `session_event` 最多取 3 条 active 且相关项
  - `reflection_hint` 最多取 1 条 active 且相关项

## 当前状态
当前容器已初始化并写入本项目第一批有效条目，可作为后续半自动/自动注入的稳定来源。