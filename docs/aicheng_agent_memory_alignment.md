# 艾橙轻量注入 × Agent memory 对齐方案

## 目标
把艾橙当前已经确定的四层轻量自动注入方案，和现有 Agent memory / OpenClaw memory 工具能力做一一对齐。

四层：
1. `role-core`
2. `relevant-memory`
3. `session-event`
4. `reflection-hint`

目标不是新增一套并行记忆系统，而是：
- 保留 Agent memory 作为唯一长期记忆真源
- 让会话事件和短期纠偏有明确容器
- 让后续自动注入有可执行的来源与顺序

---

## 一、层级对齐表

| 层级 | 数据来源 | 是否用 Agent memory | 备注 |
|---|---|---:|---|
| role-core | `docs/boardgame_companion_persona.md` 提炼摘要 | 否 | 这是角色硬设定，不走普通记忆召回 |
| relevant-memory | `memory_store / memory_recall` | 是 | 唯一长期记忆真源 |
| session-event | 项目文档 / 当日 memory / 后续独立事件容器 | 暂不直接依赖 | 当前先手工/半自动 |
| reflection-hint | 项目文档 / 当日 memory / 后续独立提示容器 | 暂不直接依赖 | 只做短期纠偏，不进人格本体 |

---

## 二、Agent memory 应承担什么

### 只承担长期、稳定、可跨会话复用的信息
适合进入 Agent memory 的内容：
- 老板的稳定偏好
- 已确认的长期项目决策
- 用户稳定身份/偏好信息
- 已反复确认的角色长期约束

### 不承担什么
不建议让 Agent memory 直接承担：
- 每轮临时状态
- 本轮风格纠偏
- 某次任务中的短期临时决定
- 角色卡核心设定正文

原因：
- 否则会把长期记忆库污染成“混杂日志”
- 会导致 recall 时噪声变大
- 容易把短期状态误当长期人格

---

## 三、四层对应的实际操作

### 1. role-core
#### 来源
- `docs/boardgame_companion_persona.md`

#### 当前做法
- 手工维护
- 角色重大变更时直接改文档并重写回 AstrBot

#### 后续建议
- 再抽一份短摘要文件，例如：`docs/aicheng_role_core_runtime.md`
- 只保留运行时最必要的 8~12 条摘要

---

### 2. relevant-memory
#### 来源
- OpenClaw `memory_store`
- OpenClaw `memory_recall`

#### 当前做法
- 对长期事实/偏好/决策，继续走 Agent memory

#### 推荐写入标准
适合 `memory_store` 的内容必须满足至少一条：
1. 跨会话仍然有价值
2. 属于稳定偏好/稳定事实/长期决定
3. 后面很可能再次被问到

#### 例子
适合写入：
- 老板要求：艾橙重写完成后要主动回报
- 老板偏好：模型这轮先保持 GPT，不动 Gemini Pro
- 老板偏好：应用层只保留三档社交距离

不适合写入：
- 这一轮我有点写歪了
- 某次输出太像说明书
- 刚刚某条消息里的临时情绪

---

### 3. session-event
#### 来源
当前先用：
- `docs/aicheng_session_event_reflection_hint_spec.md`
- `memory/YYYY-MM-DD.md`
- 项目进度文档

#### 当前做法
- 先手工记录本项目关键事件
- 不额外创建并行数据库

#### 适合存什么
- 当前项目里的重要执行决定
- Bug 排障关键节点
- 当天有效的工作约定
- 某次阶段性结论

#### 后续可选升级
后面如确有必要，可做一份轻量结构化文件：
- `apps/astrbot/AstrBot/docs/aicheng_session_events.jsonl`

但现在先不引入新容器，避免复杂度上升。

---

### 4. reflection-hint
#### 来源
当前先用：
- `docs/aicheng_session_event_reflection_hint_spec.md`
- `memory/YYYY-MM-DD.md`
- 项目文档中的纠偏小节

#### 当前做法
- 只记录最近有效的一两条纠偏
- 不长期累积成噪声堆

#### 适合存什么
- 这轮写法不要像说明书
- 不要再把设定和记忆混写
- 写文档必须 clean UTF-8

#### 不适合存什么
- 稳定不变的人格定义
- 可以直接升级为角色卡正文的内容
- 过期的执行提醒

---

## 四、推荐工作流

### 当出现新信息时，按顺序判断
1. **这是艾橙是谁吗？**
   - 是 → 改 `boardgame_companion_persona.md`
2. **这是长期稳定事实吗？**
   - 是 → `memory_store`
3. **这是当前项目的重要事件/决定吗？**
   - 是 → 记入 session-event 容器（当前先落项目文档/日记）
4. **这是短期纠偏吗？**
   - 是 → 记入 reflection-hint 容器（当前先落项目文档/日记）
5. 都不是 → 不记，直接处理当前对话

---

## 五、对齐后的最小运行模型

### 当前已具备
- 角色硬设定文档
- Agent memory 作为长期记忆底座
- session-event / reflection-hint 规范文档
- 当日记忆文件作为过渡容器

### 当前还没自动化
- session-event 独立存储
- reflection-hint 独立存储
- 自动拼装四层注入块
- 查询按意图自动分流

### 但已经能稳定执行
因为现在至少已经做到：
- 有边界
- 有规则
- 有落点
- 不会再把所有东西混进一个地方

---

## 六、下一步建议

### P1
从现在开始，所有关于艾橙的新信息，都按本文件的四步判断流程处理。

### P2
为 role-core 单独抽一个运行时摘要文件，减少后续 prompt 体积。

### P3
如果验证确实需要，再把 `session-event` / `reflection-hint` 升级成轻量结构化文件，而不是一开始就上复杂系统。