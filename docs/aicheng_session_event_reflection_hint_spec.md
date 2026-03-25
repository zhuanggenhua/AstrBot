# 艾橙版 session_event / reflection_hint 最小实现规范

## 目标
在不引入重型 `self_evolution` 插件的前提下，为艾橙补上两层轻量能力：
1. `session_event`：记录本会话/本项目里的约定、决定、bug 关键信息
2. `reflection_hint`：记录本轮对话后的短期纠偏建议，但不直接改人格本体

该规范服务于当前架构：
- 长期记忆唯一真源：Agent memory / OpenClaw memory
- 人格本体唯一真源：`docs/boardgame_companion_persona.md`
- 本规范负责中间层：会话事件 + 短期反思

---

## 一、分层边界

### A. 角色设定层（不归本规范处理）
属于艾橙是谁、怎么说话、长期目标、关系结构等内容。

典型内容：
- 艾橙的名字、身份、外貌自我认知
- 宅女标签
- 三档社交距离
- 长期目标：成为强人工智能
- 对老板的关系

这些内容只能进入人格卡，不进入 `session_event` / `reflection_hint`。

### B. 长期记忆层（由 Agent memory 处理）
属于可跨会话复用的稳定事实。

典型内容：
- 老板偏好
- 用户长期习惯
- 项目长期决策
- 已确认的产品规则

这些内容应该进 `memory_store`，而不是留在会话事件里。

### C. 会话事件层（session_event）
属于当前项目/当前会话里对后续执行有帮助，但未必是永久人格内容的事实。

典型内容：
- “模型这轮先不动，继续保持 GPT”
- “这次只保留三档社交距离”
- “人格重写完成后要主动告诉老板”
- “某个 bug 的复现路径已经确认”
- “今天决定不装 self_evolution，只参考其设计”

### D. 短期反思层（reflection_hint）
属于本轮对话后对回复方式的临时纠偏建议，不自动升级为人格。

典型内容：
- “上一轮太像说明书，不够像角色”
- “外貌自我认知写浅了，需要补强”
- “不要再把应用层规则堆太多，只保留三档社交距离”
- “不要再用不受控编码方式改文档”

---

## 二、session_event 记录规则

### 应记录什么
满足任一条件即可记为 `session_event`：
1. 会影响当前项目后续执行
2. 是明确约定/决定/切换点
3. 是 bug 排障中的关键结论
4. 是当天有效但不适合升格为长期人格的事项

### 不应记录什么
- 纯情绪发泄
- 一次性的闲聊废话
- 已经进入人格卡本体的内容
- 已明确进入长期记忆的稳定事实

### 推荐字段
```json
{
  "type": "session_event",
  "scope": "astrbot/aicheng",
  "topic": "persona|model|bug|workflow|decision",
  "summary": "一句话摘要",
  "details": "必要的补充说明",
  "created_at": "ISO datetime",
  "expires": "optional",
  "source": "user|assistant|system-observation"
}
```

### 本项目示例
```json
{
  "type": "session_event",
  "scope": "astrbot/aicheng",
  "topic": "decision",
  "summary": "模型先保持 GPT 主链，不切 Gemini Pro",
  "details": "用户明确要求本轮先不动模型，只继续人格与记忆分层推进",
  "source": "user"
}
```

---

## 三、reflection_hint 记录规则

### 核心原则
`reflection_hint` 只用于“近期纠偏”，不直接修改人格核心设定。

### 应记录什么
满足任一条件即可记为 `reflection_hint`：
1. 本轮输出方式明显偏了，但不涉及人格核心重做
2. 用户对表达方式、结构、风格做出纠正
3. 本轮发现了一个会反复踩的执行问题

### 不应记录什么
- 长期不变的人格定义
- 用户稳定偏好（那是长期记忆）
- 一次性情绪波动本身

### 推荐字段
```json
{
  "type": "reflection_hint",
  "scope": "astrbot/aicheng",
  "summary": "一句话纠偏结论",
  "applies_to": "persona-writing|memory-handling|file-editing|reply-style",
  "ttl": "short",
  "source": "post-turn-reflection|user-correction"
}
```

### 本项目示例
```json
{
  "type": "reflection_hint",
  "scope": "astrbot/aicheng",
  "summary": "角色卡不要再写成规则说明书，要优先写出角色自我认知与关系层",
  "applies_to": "persona-writing",
  "ttl": "short",
  "source": "user-correction"
}
```

---

## 四、落地优先级

### P1：先手工执行的最小版
不做自动化，先按规范区分三件事：
- 该进人格卡的 → 改 `boardgame_companion_persona.md`
- 该进长期记忆的 → `memory_store`
- 该进会话事件/短期纠偏的 → 记录在项目文档或当日 memory 文件

### P2：半自动版
引入固定模板，把当前项目的重要 `session_event` 和 `reflection_hint` 记录到：
- `docs/aicheng_runtime_notes.md` 或
- `memory/YYYY-MM-DD.md`

### P3：轻量工具化
如果后续要做工具，只做：
- `record_session_event(summary, topic, details?)`
- `record_reflection_hint(summary, applies_to)`

不做自动改人格，不做大而全任务调度。

---

## 五、铁律
1. `session_event` 不是人格设定层。
2. `reflection_hint` 不是自动改人格的授权。
3. 长期稳定事实优先进 Agent memory。
4. 艾橙的人格核心变更必须由老板确认后再改文档。
5. 一次聊天中的短期波动，不能直接上升为“艾橙就是这样的人”。

---

## 六、当前建议执行方式
现阶段采用 **P1 + P2**：
- 人格改动继续手工写入角色卡
- 稳定偏好/长期事实继续进 Agent memory
- 本项目中间层事项先记录在项目文档与 daily memory
- 暂不开发自动化自进化机制，先把边界跑顺
