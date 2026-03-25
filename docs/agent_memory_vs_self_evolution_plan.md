# Agent Memory 保留方案｜吸收 self_evolution 的最小改造路线

## 结论
当前体系保留 **Agent memory / OpenClaw memory** 作为唯一长期记忆底座。

`astrbot_plugin_self_evolution` 不直接安装为正式依赖，只吸收其三类高价值设计：
1. 记忆分层（profile / session_event / reflection_hint）
2. 查询按意图分流（recent_context / daily_summary / session_event / user_profile / fallback）
3. 轻量反思（self_correction / explicit_facts / cognitive_bias）

不吸收其重型运行时行为模块：
- affinity
- SAN
- 主动插嘴 / 社交参与规划
- 元编程 / 人格自进化审批
- 大而全 prompt 注入体系

---

## 为什么保留 Agent memory
### 适合作为唯一真源
Agent memory 更像纯粹的长期记忆底座：
- 可存储
- 可检索
- 可更新
- 可删除
- 可跨会话延续

相比之下，self_evolution 把记忆、画像、反思、社交行为、SAN、affinity 混在一起，更像“人格运行框架”，不适合作为当前唯一核心记忆系统。

### 更适合艾橙当前阶段
艾橙目前的关键任务是：
- 把角色本体写准
- 分清什么进入设定，什么进入记忆
- 保持人格稳定，不被过多运行时模块拉偏

因此保留 Agent memory，更符合当前阶段目标。

---

## 参考 self_evolution 后应新增的三层记忆模型

### Layer A — 角色设定（不进长期记忆工具库）
这是“艾橙是谁”的硬设定，写在人格卡 / 角色文档里，不走普通记忆工具自动抽取。

包含：
- 姓名、身份、长期目标
- 外貌自我认知
- 与老板的关系
- 三档社交距离
- 口头禅定位
- 宅女标签
- 理性压情感、害羞表现方式

### Layer B — 长期人物 / 用户记忆（进入 Agent memory）
这是可长期积累并跨会话复用的信息。

包含：
- 用户偏好
- 用户身份线索
- 项目长期约定
- 角色长期稳定偏好
- 老板的明确偏好 / 决策

建议分类：
- `preference`
- `fact`
- `decision`
- `entity`

### Layer C — 会话事件 / 一次性纠偏（不直接并入角色设定）
这一层借鉴 self_evolution，但采用轻量实现。

包含：
- 某次会话中的 bug 反馈摘要
- 某次群聊/私聊的临时约定
- 对近期回复风格的纠偏提示

细分：
1. `session_event`
   - 记录本次会话中的约定、安排、关键事实
2. `reflection_hint`
   - 仅作为短期纠偏，不直接进人格本体

---

## 参考 self_evolution 后应新增的查询分流

### 1. recent_context
回答：刚刚在聊什么 / 最近在聊什么
来源：聊天上下文，而不是长期记忆库

### 2. session_event
回答：之前是不是约定过什么 / 这个 bug 前面说到哪一步
来源：本项目会话事件摘要

### 3. user_profile
回答：老板偏好什么 / 某用户是什么风格
来源：Agent memory 的长期条目

### 4. fallback_memory
回答：普通长期事实召回
来源：Agent memory_recall

### 不做 daily_summary 的重型自动化
目前阶段不引入 self_evolution 那套“每日总结任务 + scope 知识库写入”，避免体系变重。
如后续确实有需要，再单独评估。

---

## 轻量反思机制（建议吸收）

### 目标
不是让人格自动乱改，而是让系统在每轮会话后只产出两类信息：
1. `explicit_facts`：可以安全进入长期记忆的事实
2. `self_correction`：仅供近期参考的短期纠偏

### 规则
- `explicit_facts` → 进入 Agent memory
- `self_correction` → 写入短期项目文件或会话提示，不自动改人格卡
- 任何长期人格变更，必须人工确认后再改角色卡

### 这样做的好处
- 能学习
- 但不会人格漂移
- 不会因为一次聊天就把艾橙改坏

---

## 明确不采纳的部分
以下内容不建议直接进入当前体系：
- affinity 情感积分
- SAN 精力系统
- 主动插嘴 / eavesdropping
- 元编程 / 自动改代码
- 重型 prompt 注入配置系统
- scope 知识库日报自动汇总

原因：
- 会让系统复杂度飙升
- 容易和现有 Angel Memory / Agent memory / 艾橙人格本体职责重叠
- 影响人格稳定性与排障效率

---

## 实施顺序（最小落地）

### Phase 1 — 规则固化
- 固化“设定 vs 记忆 vs 会话事件”三层边界
- 把艾橙本体继续稳定在角色卡中

### Phase 2 — 轻量事件层
- 增加一份项目内的 `session_event` 记录规范
- bug、约定、决定走事件层，不污染人格本体

### Phase 3 — 轻量反思层
- 会话后只提炼：
  - 可持久事实
  - 短期纠偏
- 不自动改角色卡

### Phase 4 — 查询分流
- 问“你是谁 / 老板偏好” → 查设定/长期记忆
- 问“刚刚说到哪” → 查上下文
- 问“之前约定过什么” → 查事件层

---

## 当前建议
现阶段先不要安装 `astrbot_plugin_self_evolution`。
先把以下三件事做稳：
1. 艾橙角色卡稳定
2. Agent memory 作为唯一长期记忆真源
3. 轻量 session_event / reflection_hint 机制独立出来

等这三件事稳定后，再决定是否从 self_evolution 继续抽更多机制。