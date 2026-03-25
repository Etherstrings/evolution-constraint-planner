# 真实子代理协议

## 为什么 ECL 必须使用真实子代理

ECL 强制引入真实子代理，是为了对抗一个非常稳定的失败模式：父模型一旦锚定了自己的解释，就会下意识为它辩护。

所以这些独立阶段不是装饰性的“多叫几个 agent 看看”，而是结构性质量门。

## 硬规则

下面这些阶段必须使用真实 spawned agents：

- D / critique
- G / red-blue
- H / review
- J / compile-for-code

Stage A 可以使用 support agents，但 preprocess 的所有权和写入权仍然属于父模型。

## 通用协议

所有子代理都遵循同一套基础规则：

- 只接收当前阶段的局部上下文
- 不接收父模型偏好的最终答案
- 返回结构化 deltas，而不是直接写最终 note
- 不允许直接改 bundle 文件
- bundle 的唯一写入者始终是父模型

## 共享 delta 结构

所有独立 agent 默认返回这一结构：

```json
{
  "facts": [],
  "challenges": [],
  "conflicts": [],
  "gaps": [],
  "discard_recommendations": [],
  "follow_up_questions": [],
  "confidence": "medium",
  "evidence_refs": []
}
```

这样父模型就能集成独立发现，而不会把 bundle 的规范写入权交出去。

## Stage A 的 support agents

这些 agent 是可选的。它们主要用在原始请求很模糊、过于 solution-biased 或者内部矛盾明显的时候。

### Intent Extractor

用途：

- 推断用户字面请求背后的真实目标
- 挖出隐藏假设
- 产出值得追问的例子和反例

适用场景：

- 用户一上来就先讲解决方案，没有讲真实问题
- 请求听起来很笼统，但语气又很确定

### Reality Gap Checker

用途：

- 挑战可能是错的、残缺的、和 repo 现实不符的说法
- 揪出请求与客观现实之间的落差

适用场景：

- 用户用主观判断描述 repo 行为
- 拟议方案依赖的基础设施可能根本不存在

### Blind Spot Scout

用途：

- 找出用户还没意识到应该说出来的维度
- 逼出 non-goals、边界条件、验收含义和失败处理

适用场景：

- 请求一上来就直接进入功能构建
- 重要工作流边缘很可能还没有被命名

## D / Critique Agent

Stage D 需要一个独立 critique agent。

### 任务

- 识别伪需求
- 揪出矛盾
- 删除不可验证或浪费的需求
- 在需求冻结前挑战糟糕的拆解方式

### 它为什么存在

如果没有 D，Stage C 很容易把“写得很像样的错误需求”冻结下来。

## G / Red And Blue Agents

Stage G 需要两个独立 agent。

### Red

任务：

- 攻击边界条件
- 攻击滥用路径
- 攻击依赖故障
- 攻击非法状态转换
- 攻击恢复行为中的模糊地带

### Blue

任务：

- 对攻击给出缓解方式
- 把攻击转成明确规则
- 如果这版做不到，就把它写成残余风险

### 为什么两者缺一不可

只有 red 没有 blue，会只剩下焦虑。只有 blue 没有 red，会只剩下乐观。两者一起才会逼出清晰的防守面。

## H / Review Agent

Stage H 需要一个独立 review agent。

### 任务

- 判断下一位 coder 是否还得发明含义
- 返回 `approved`、`approved_with_conditions` 或 `rejected`
- 如果 rejected，指出最早该回流到哪个阶段

### H 保护的是什么

H 保护的是“假的 ready”。一个 bundle 看起来写得很多，不代表它真的没有高影响语义缺口。

## J / Compile-for-Code Agent

Stage J 需要一个独立 compile-for-code agent。

### 任务

- 吸收已收敛的 A-H package
- 判断这份 package 是否真的 code-ready
- 编译 execution-facing companion docs
- 确认下一条直接可执行的 code command

### 为什么 J 不等于 H

H 判断的是 ready 不 ready，J 负责把 ready 的结果编译成真正可执行的产物。一个 package 可能通过了 review，但仍然没有被编译成好用的 handoff。

## 故障处理

如果某个必需 agent 无法创建：

- 阶段 note 仍然要写
- `status` 必须写成 `blocked_by_agent_unavailable`
- `agent_mode` 必须写成 `blocked`
- 依赖这个阶段的后续阶段不能继续假装 complete

ECL 不允许在失去独立性的前提下伪造完成状态。

## 在 Codex 里的实践建议

在 Codex 里实现这套协议时：

- 子代理 prompt 要严格保持 stage-local
- 不要把你自己的答案当默认答案喂给子代理
- 把 delta 写回 note 之前，要再次对照 repo 现实
- evidence refs 要保留下来，方便 validator 和后来的人审计整个推理链
