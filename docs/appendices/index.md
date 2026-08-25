# Book Appendices

Supplementary case studies and deep-dive write-ups that don't fit the main chapter sequence but are useful reference material for understanding how this repository works and evolved.

- [Skill Portability Strategy](./skill-portability-strategy/index.md) - how we have
designed these skills to be useful across the major AI development tools (Claude Code, OpenAI ChatGPT, Google Antigravity, Cursor etc.).  The key is that the AI tools MUST support the Agent Skill
standards.  If they support skills we will make an effort to test them.

- [Installing Skills for Ollama](./installing-skills-for-ollama.md) — why Ollama
  models need a skills-aware agent harness, how skill-directory discovery works,
  and how to configure OpenCode, Codex, or Open WebUI to use this repository's
  skills with a local model.

- [Skill Refactor with Fable 5](./skill-refactor-fable-5.md) — a case study on how the intelligent-textbook skill library evolved since Claude Skills launched in October 2025, why it periodically needs re-architecting, and how a 29-skill, over-budget catalog was consolidated to 14 skills through an agent-authored, human-reviewed, phase-by-phase refactor.
- [Delegating Image Generation to an External Agent](./imaging-agent-delegation.md) — how to hand image work to a tool Claude Code cannot drive (ChatGPT desktop, Google Antigravity) and get it back verified: a filesystem work queue whose entire protocol is a filename, automated acceptance checks, notification channels that degrade gracefully, and what a machine can and cannot validate about a generated illustration.
