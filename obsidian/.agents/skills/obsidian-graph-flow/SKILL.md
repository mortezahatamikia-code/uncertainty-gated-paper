---
name: obsidian-graph-flow
description: >-
  Deconstructs user goals and complex requests into an Obsidian knowledge graph of tasks, specs, and architecture notes.
  Provides a Trello/Kanban workflow (Backlog, Todo, Doing, Done) using Obsidian Canvas and markdown graphs.
  Autonomously executes tasks step-by-step, synthesizes emergent tasks/ideas from completed work, maintains real-time graph
  backlinks, and keeps the visual Canvas board updated. Use this skill when the user mentions Obsidian, task breakdown,
  Trello/Kanban boards, graph planning, or AI-assisted brainstorming and execution.
---

# 🧠 Obsidian Graph & Trello-Style Task Management Flow

This skill turns Antigravity into an autonomous project execution engine paired with an Obsidian Knowledge Graph and interactive Trello-style Canvas.

Obsidian acts as the project's living brain, visual roadmap, Kanban board, and ideation workshop.

---

## 🏗️ 1. Core Structures: Board, Graph, & Notes

```text
<workspace-root>/
├── .obsidian/                 # Graph colors, app settings, core plugins
├── Project Board.canvas       # 🎨 Visual Trello-style Board (Backlog, To Do, Doing, Done)
├── 00 - Dashboard.md          # 📊 Central MOC & HTML Kanban Overview
├── Specs/                     # 📋 Functional specs & requirements
├── Architecture/              # 🏛️ System design & ADRs
├── Tasks/                     # 📌 Atomic task notes with dependency links
└── Logs/                      # 📜 Execution history & diffs
```

### Four-Stage Task Lifecycle & Graph Colors
1. 💡 **Backlog & Ideas** (`#task/backlog` - Slate / `#idea` - Gold): Uncommitted thoughts, AI-generated proposals, raw user ideas.
2. 📋 **To Do** (`#task/todo` - Blue `rgb: 3899126`): Concrete, fully specified tasks ready for implementation.
3. ⚡ **Doing / In Progress** (`#task/in-progress` - Orange `rgb: 16096779`): Currently being implemented by Antigravity.
4. ✅ **Done** (`#task/done` - Green `rgb: 2278750`): Implemented, tested, and verified.
5. 🔴 **Blocked** (`#task/blocked` - Red `rgb: 15680580`): Waiting on prerequisite tasks.

---

## 🔄 2. Dynamic Workflow & Emergent Task Synthesis

### Phase 1: Intake & Decomposition
1. Create `Specs/SPEC-<id>.md` and architecture notes if needed.
2. Break down into atomic tasks (`Tasks/TSK-<id>.md`) with:
   - `depends_on: ["[[Tasks/TSK-...]]"]`
   - `blocks: ["[[Tasks/TSK-...]]"]`
3. Wire tasks onto `Project Board.canvas` under the **To Do** column with connecting arrows.

### Phase 2: Autonomous Step-by-Step Implementation
1. **Select Task**: Pick the next unblocked task in To Do.
2. **Move to Doing**:
   - Update frontmatter: `status: in_progress` and tag `#task/in-progress`.
   - Update `Project Board.canvas` (move card to Doing column).
3. **Execute**: Code, edit files, and build features in the workspace.
4. **Verify**: Run tests and commands to ensure correctness.
5. **Move to Done**:
   - Update frontmatter: `status: done` and tag `#task/done`.
   - Update `Project Board.canvas` (move card to Done column).
   - Log execution summary in `Logs/`.

### Phase 3: 🧬 Emergence & AI Brainstorming (Task Synthesis)
When two or more related tasks are completed (e.g. TSK-001 & TSK-002):
1. **Synthesize Findings**: Evaluate what was produced or learned.
2. **Spawn Follow-up Tasks or Insights**:
   - If a new enhancement, refactoring, or creative idea emerges, create a new note (`Tasks/TSK-...` or `Ideas/IDEA-...`).
   - Add frontmatter: `derived_from: ["[[Tasks/TSK-001]]", "[[Tasks/TSK-002]]"]`.
   - In `Project Board.canvas`, create a new node and draw directed edges from the parent tasks to the new emergent task.
   - Place it in **Backlog** (for user review) or **To Do** (if directly needed for the goal).
3. **Present to User**: Highlight the newly synthesized task and the visual connection in the graph/canvas!

---

## 🎨 3. Keeping Canvas & Graph in Sync

- Whenever tasks change state or new tasks are synthesized, update `Project Board.canvas`:
  - `nodes`: update coordinates `x` to match the target column (`col-backlog`, `col-todo`, `col-doing`, `col-done`).
  - `edges`: add edges representing dependencies (`fromNode` -> `toNode`) or synthesis (`derived_from`).
- In markdown task notes, always keep wikilinks active: `[[Tasks/TSK-xxx]]` so the global Graph View (`Ctrl + G`) reflects the exact same relationship.
