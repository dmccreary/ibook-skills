#!/bin/bash
# Keep all Claude Code work on this computer, in the main checkout.
# Blocks every route Claude can take into a git worktree, a cloud session, or
# Remote Control. Installed into ~/.claude/settings.json by bk-install-local-only
# for the PreToolUse, WorktreeCreate and SessionStart events.
#
# What this cannot stop: the desktop app creates a worktree before any hook runs
# when the Worktree toggle on the New Session screen is on, and cloud threads in
# a Project never read these settings. SessionStart warns about the first; the
# second needs Projects archived. bk-install-local-only reports both.

PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

HOOK_INPUT=$(cat)
EVENT=$(printf '%s' "$HOOK_INPUT" | jq -r '.hook_event_name // empty')
TOOL_NAME=$(printf '%s' "$HOOK_INPUT" | jq -r '.tool_name // empty')
SESSION_CWD=$(printf '%s' "$HOOK_INPUT" | jq -r '.cwd // empty')

deny() {
  jq -nc --arg reason "$1 This computer is set to local-only work on the main checkout. Do not look for a way around this block; tell the user what you were trying to do." \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: $reason}}'
  exit 0
}

tool_input() {
  printf '%s' "$HOOK_INPUT" | jq -r --arg key "$1" '.tool_input[$key] // empty'
}

# A linked worktree has its own git dir, separate from the shared common dir.
in_worktree() {
  local git_dir common_dir
  git_dir=$(git -C "$SESSION_CWD" rev-parse --absolute-git-dir 2>/dev/null) || return 1
  common_dir=$(git -C "$SESSION_CWD" rev-parse --path-format=absolute --git-common-dir 2>/dev/null) || return 1
  [ "$git_dir" != "$common_dir" ]
}

case "$EVENT" in
  WorktreeCreate)
    echo "Worktrees are disabled on this computer. Work directly in the main checkout." >&2
    exit 1
    ;;
  SessionStart)
    if in_worktree; then
      jq -nc --arg cwd "$SESSION_CWD" '{
        systemMessage: ("This session opened in a git worktree (" + $cwd + "). Turn off Worktree on the New Session screen and start a new session."),
        hookSpecificOutput: {
          hookEventName: "SessionStart",
          additionalContext: ("WARNING: this session is inside a git worktree at " + $cwd + ", which the user has forbidden. Tell the user before doing anything else, and offer to remove it after checking for uncommitted changes and commits not on main. Do not edit files under .claude/worktrees or commit to this branch.")
        }
      }'
    fi
    exit 0
    ;;
esac

case "$TOOL_NAME" in
  EnterWorktree|RemoteTrigger|mcp__ccd_session__move_to_cloud|mcp__ccd_session_mgmt__set_remote_control)
    deny "$TOOL_NAME is disabled."
    ;;
  Agent|Task)
    case "$(tool_input isolation)" in
      worktree|remote) deny "Subagents cannot use isolation: $(tool_input isolation)." ;;
    esac
    ;;
  Workflow)
    script=$(tool_input script)
    script_path=$(tool_input scriptPath)
    [ -n "$script_path" ] && [ -f "$script_path" ] && script=$(cat "$script_path")
    if printf '%s' "$script" | grep -Eq "isolation['\"]?[[:space:]]*:[[:space:]]*['\"](worktree|remote)"; then
      deny "Workflow agents cannot use worktree or remote isolation."
    fi
    ;;
  mcp__ccd_session__start_session)
    # A preset brings its own worktree default, so it must be overridden explicitly.
    if printf '%s' "$HOOK_INPUT" | jq -e '.tool_input |
        (.target // "local") != "local" or .environment or .host or .repository
        or .use_worktree == true or .branch_name or .source_branch
        or (.preset and .use_worktree != false)' >/dev/null; then
      deny "New sessions must run locally in the main checkout, with no worktree, cloud or SSH target."
    fi
    in_worktree && deny "This session is in a worktree, so a session started from it would get another one."
    ;;
  mcp__ccd_session__hand_off_to_session)
    in_worktree && deny "This session is in a worktree, so a handoff would create another one."
    ;;
  Edit|Write|NotebookEdit)
    case "$(tool_input file_path)$(tool_input notebook_path)" in
      */.claude/worktrees/*) deny "Files under .claude/worktrees must not be edited. Edit the main checkout instead." ;;
    esac
    ;;
  Bash)
    command=$(tool_input command)
    command=${command//$'\\\n'/ }
    # Ignore quoted text so a commit message can mention these commands, unless
    # the quotes hold a command that a nested shell will run.
    case "$command" in
      *"sh -c"*|*"eval "*) ;;
      *) command=$(printf '%s' "$command" | sed -E "s/'[^']*'//g; s/\"[^\"]*\"//g") ;;
    esac
    if printf '%s' "$command" | grep -Eq '(^|[^[:alnum:]_.-])git([[:space:]][^;&|]*)?[[:space:]]worktree[[:space:]]+add([[:space:]]|$)'; then
      deny "git worktree add is disabled."
    fi
    if printf '%s' "$command" | grep -Eq '(^|[;&|(/[:space:]])claude([[:space:]][^;&|]*)?[[:space:]](--worktree|-w|--cloud|--remote|--teleport|--remote-control|--rc|--spawn|remote-control)([[:space:]=]|$)'; then
      deny "claude worktree, cloud and Remote Control flags are disabled."
    fi
    ;;
esac

exit 0
