# Installing Skills for Ollama

## The Key Discovery

Ollama does not discover or load Agent Skills by itself. Ollama runs a language
model and provides APIs such as chat completion and tool calling. A separate
**agent harness**—for example, OpenCode, Codex, Claude Code, Goose, OpenClaw, or
Open WebUI—finds the skills, tells the model which skills are available, and
loads the selected instructions.

Consequently, this command starts a model but does not scan a skills directory:

```bash
ollama run qwen3.5:9b
```

To use skills, run the Ollama model through a skills-aware agent:

```bash
ollama launch opencode --model qwen3.5:9b
```

or:

```bash
ollama launch codex --model qwen3.5:9b
```

Ollama maintains a current list of its supported
[agent integrations](https://docs.ollama.com/integrations). The Agent Skills
standard defines the contents of a skill directory, but the agent harness
decides which directories to search.

!!! info "Model runtime versus agent harness"
    **Ollama** loads model weights, performs inference, and supports function
    calling. The **agent harness** scans for `SKILL.md`, builds the skill catalog,
    gives the model file and shell tools, and manages the agent loop. Skills are
    therefore a harness capability, not a property stored in the model weights.

## How Skill Discovery Works

The open [Agent Skills specification](https://agentskills.io/specification)
defines a skill as a directory containing at least one file named exactly
`SKILL.md`:

```text
skill-name/
├── SKILL.md
├── scripts/       # optional
├── references/    # optional
└── assets/        # optional
```

A skills-aware agent normally uses
[progressive disclosure](https://agentskills.io/client-implementation/adding-skills-support):

1. At session startup, the harness scans its configured skill roots and reads
   only each skill's `name` and `description`.
2. The harness places this compact catalog in the model's context or exposes it
   through a skill-loading tool.
3. When a request matches a description, the model asks the harness to load the
   complete `SKILL.md`.
4. Referenced scripts, templates, and documentation are loaded only when the
   skill needs them.

The model does not independently search the filesystem. It can only see the
catalog and tools supplied by the harness.

## The Portable Skills Directory

The most widely supported cross-client convention is:

```text
# Project-specific skills
<project>/.agents/skills/<skill-name>/SKILL.md

# Skills available to the current user in every project
~/.agents/skills/<skill-name>/SKILL.md
```

Client-native directories also exist:

| Agent harness | Project directory | User directory |
|---------------|-------------------|----------------|
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` and `$CODEX_HOME/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |

OpenCode additionally scans `.agents/skills/` and `.claude/skills/` at both
project and user scope. It can also load an arbitrary directory configured in
`opencode.json`. See the current
[OpenCode skill discovery documentation](https://opencode.ai/docs/skills).

For a broader comparison of agent-specific locations and precedence rules, see
[Agent Skill Portability Strategy](./skill-portability-strategy/index.md).

## Recommended Setup for This Repository

The skills in this repository use supporting scripts, references, templates,
and schemas. Install or link the complete skill directories; copying only the
`SKILL.md` files will leave many workflows incomplete.

### Option 1: Configure OpenCode to Read the Repository

OpenCode provides the simplest direct-directory configuration. Create an
`opencode.json` file in the project where OpenCode will run:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "skills": [
    "/Users/dan/Documents/ws/ibook-skills/skills"
  ]
}
```

Then launch OpenCode through Ollama:

```bash
ollama launch opencode --model qwen3.5:9b
```

This keeps `/Users/dan/Documents/ws/ibook-skills/skills/` as the single source
of truth. Edits in the repository become available without copying the skill
collection. Do not add `skills/archived/` as a separate source; archived skills
are retained for reference and should not be advertised alongside their active
meta-skills.

### Option 2: Link Skills into the Portable User Directory

For Codex, OpenCode, Gemini CLI, Cursor, and GitHub Copilot, place links to the
active skill directories under:

```text
~/.agents/skills/
```

The resulting layout should resemble:

```text
~/.agents/skills/
├── book-installer -> /Users/dan/Documents/ws/ibook-skills/skills/book-installer
├── microsim-generator -> /Users/dan/Documents/ws/ibook-skills/skills/microsim-generator
├── chapter-content-generator -> /Users/dan/Documents/ws/ibook-skills/skills/chapter-content-generator
└── ...
```

The repository's `scripts/bk-install-skills` script currently installs links
under `~/.claude/skills/`. To use that script for a portable Ollama-backed
agent, change its `TARGET_DIR` to `~/.agents/skills/`, or extend it to install
to both locations. Preserve its exclusion of `skills/archived/`.

After installing the links, launch Codex with Ollama:

```bash
ollama launch codex --model qwen3.5:9b
```

Ollama's [Codex integration guide](https://docs.ollama.com/integrations/codex)
also documents persistent profiles and manual `codex --oss` configuration.

### Option 3: Import Skills into Open WebUI

Open WebUI manages skills in its Workspace rather than scanning
`~/.agents/skills/`:

1. Open **Workspace → Skills**.
2. Create a skill or import its Markdown.
3. Attach the skill to an Open WebUI model, or select it for an individual chat.
4. Enable native function calling when using model-attached, lazily loaded
   skills.

Open WebUI injects a skill directly when it is selected for a chat. For a skill
attached to a model, it advertises a manifest and lets the model call the
`view_skill` tool to retrieve the full instructions. That lazy-loading path
requires native function calling. See
[Open WebUI Skills](https://docs.openwebui.com/features/workspace/skills/).

Open WebUI is convenient for instruction-only skills. It is less convenient
for this repository's resource-rich skills unless their supporting files and
execution environment are also made available to the model.

## Choosing a Small Ollama Model

A model does not need to be trained specifically on Agent Skills. It needs to
follow detailed instructions and, when the harness uses lazy activation, call
tools reliably. Ollama identifies compatible models with the **Tools** label in
its [model catalog](https://ollama.com/search?c=tools).

Practical compact candidates include:

| Model family | Useful sizes | Notes |
|--------------|--------------|-------|
| Qwen 3.5 | 4B, 9B | Strong general starting point; prefer 9B for multi-step skills |
| Ministral 3 | 3B, 8B, 14B | Edge-oriented models with tool support |
| Granite 4 | 1B, 3B | Compact tool-capable models; 3B is the more practical choice |
| Llama 3.2 | 3B | Small general model with tool support |
| Command R7B | 7B | Compact model designed for retrieval and tool-oriented work |
| LFM 2.5 | 8B | Edge model designed for reliable tool calling |

Very small function-calling models can emit a correctly structured tool call
but still struggle to choose the right skill, follow a long workflow, or
recover after a failed command. The skills in this repository include
multi-stage educational workflows and can load substantial reference material.
An 8B–9B model is therefore a more realistic starting point than a sub-3B
model.

Context length matters as much as parameter count. Ollama recommends at least a
64K-token context window for its Codex integration. A short context may fit the
skill catalog but truncate the activated instructions, project files, tool
results, or conversation history.

## Verification

After installation, start a new agent session from a working directory where
the skills should be visible. Ask the agent:

```text
List the available skills related to MicroSims and explain which skill you
would use to create a Chart.js educational simulation. Do not create files.
```

A successful installation should produce an answer based on the descriptions
of `microsim-generator` and related utilities. If the skill is missing, check:

- The selected application is an agent harness, not a plain `ollama run`
  session.
- The skill root is one the harness scans or is explicitly configured.
- Every active skill is a directory containing an uppercase `SKILL.md`.
- The frontmatter contains a valid `name` and a specific `description`.
- The directory name matches the frontmatter `name`.
- Skill permissions and the harness's skill-loading tool are enabled.
- Native function calling is enabled when the harness uses a tool to activate
  skills.
- The model has enough context space for the selected workflow.

The central troubleshooting question is: **Which component is responsible for
skill discovery?** If the answer is merely “Ollama,” a skills-aware harness is
still missing.
