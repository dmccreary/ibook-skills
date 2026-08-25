# Getting Started Guide for Installing Textbook Generation Skills in Claude Code

This document guides you through the steps to install a set of Claude Code Skills
used to generate intelligent textbook on your local computer so they are accessible to Claude Code.

This Document has two sections:

1. A [Quick Start Summary](#quick-start-summary) for experienced users that understand UNIX shell command
2. A [Detailed Installations Options](#detailed-installation-options-for-new-users) for users that have never use the UNIX shell

At the end of this getting started guild you should be 
able to run all the skills and book-building utilities in this project.

!!! Note
    Claude Code does not currently run on the Windows PowerShell.  See details below
    on how to install Claude Code on the MicroSoft Windows System for Linus (WSL).

## Quick Start Summary

#### Diagram: Install Book Building Environment

<!-- Such a wild bug.  A top level document like /docs/getting-started.md can't use a relative path like "./sims" ! -->
<iframe src="/ibook-skills/sims/install-book-env/main.html" width="100%" height="400px" scrolling="no"></iframe>
[View the Install Book Building Environment Fullscreen](sims/install-book-env/main.html)


Here's a quick overview of the five main steps of the installation process.
These steps assume you are familiar with using the UNIX Terminal or shell.
You can find details on teach step later in the document in the [Detailed Installation Options for New Users](#detailed-installation-options-for-new-users).
The Quick Start steps if you are an experienced UNIX user and have git already installed on your computer.

### Step 1: Clone the Claude Skills GitHub Repo

Download the ibook-skills repository from GitHub to your local drive.

```bash
mkdir -m "$HOME/projects"
cd "$HOME/projects"
git clone https://github.com/dmccreary/ibook-skills
```

### Step 2: Set the BK_HOME and Configure PATH
Set environment variables in your shell startup file.
Set `BK_HOME` and add `~/.local/bin` to your `PATH` if it is not already on your path

```bash
BK_HOME="$HOME/projects/ibook-skills"
export PATH="$HOME/.local/bin:$PATH"
```

Restart you shell and type: ```echo $BK_HOME``` to verify the environment variable is set

### Step 3: Install The Book Building Scripts

Install book utilities
Run `bk-install-scripts` to install book-building commands

```bash
$BK_HOME/scripts/bk-install-scripts
```

Type ```bk``` and you should see a list of the book building commmands

### Step 4: Install Claude Skills

To install skills globally, you just need to type the following command

```
bk-install-skills
```

This installs every skill into each agent present on your machine — `~/.claude/skills/`,
`~/.codex/skills/`, and `~/.gemini/antigravity/skills/`.

### Step 5 Verify installation

Check that everything is working correctly by asking Claude what skills it knows about.

```bash
claude
what skills do you know about?
```

Here is a sample response:

```
⏺ I have access to 23 specialized skills in this repository for creating intelligent educational textbooks.
  Here's an overview:...
```

!!! Warning
    The installation process only installs **symbolic links** in your ~./local/bin and your ~/.claude/skills.
    This allows you to just do a `git pull` on the claudes-skill repo to get new updates to existing skills.
    You must not delete the ibook-skills repo or the skills will stop working.
    When new skills or scripts are added you MUST reinstall them to get the new symbolic links installed.
    When in doubt do a git pull and rerun the installers for both scripts and skills.

Detailed instructions for each step are provided below.

## Detailed Installation Options For New Users

This section of the Getting Started Guide walks new users through some of the 
detailed step-by-step guide for getting the Claude skills loaded into
your local computer.  It is intended for users that are new to the UNIX shell.


There are two installation options for Claude skills:

1. **Option 1: Global Skills** - The skills will be usable by all your projects. If you are creating multiple textbooks you should choose this option. (Recommended)
2. **Option 2: Project Skills** - If you are only working on a single textbook you can use this option. If you are using many other skills on other projects that might have conflicting skill names, this is a good choice.

The book-building utilities are always installed globally to `~/.local/bin`.

### Prerequisites

#### Git Installation

Git comes install on many operating systems including

1. MacOS
2. Linux (many versions)
3. Raspberry Pi OS
4. Windows Subsystem for Linux (WSL)

!!! note
    Although git can be installed on Windows, you can't run Claude with PowerShell.
    You must run the Windows Subsystem for Linux (WSL) or the git bash shell.
    When you use Visual Studio Code, it must be configured to use these shells
    in the Terminal View.

You can test that git is installed by running:

```sh
git --version
```

Sample response:
```
git version 2.50.1 (Apple Git-155)
```

#### Background on UNIX Environment Variables

The Claude Skills depend on running a set of UNIX shell commands.
To find the shell commands the UNIX shell looks in a series of specified locations
in your PATH variable.  You can see your current PATH by doing the following:

```sh
echo $PATH
```

By default, the claude program and the book building scripts are stored in a
directory that your personal account always has write access to.
This is called your "Hidden Local Binaries" location.

```sh
ls ~/.local/bin
```

The tilde character `~` is a shorthand for the home directory you are in when your shell starts up.
This is referred to as your `$HOME` directory.  Note that you should never put `~` in your startup file.
Always use `$HOME` in the startup files.

Before installing the skills, you must complete two important setup steps:

### 1. Set the BK_HOME Environment Variable

The `BK_HOME` environment variable must point to the root directory of your cloned ibook-skills repository. Add this to your shell startup file:

**For Bash** (add to `~/.bashrc` or `~/.bash_profile`):
```bash
export BK_HOME=~/projects/ibook-skills
```

**For Zsh** (add to `~/.zshrc`):
```bash
export BK_HOME=~/projects/ibook-skills
```

**For Fish** (add to `~/.config/fish/config.fish`):
```fish
set -gx BK_HOME /Users/YOUR_USERNAME/Documents/ws/ibook-skills
```

Replace `$HOME/projects/ibook-skills` with the actual path where you cloned the repository.

### 2. Add ~/.local/bin to Your PATH

The book-building scripts will be installed to `~/.local/bin`. Ensure this directory is in your PATH:

**For Bash** (add to `~/.bashrc` or `~/.bash_profile`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**For Zsh** (add to `~/.zshrc`):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**For Fish** (add to `~/.config/fish/config.fish`):
```fish
set -gx PATH $HOME/.local/bin $PATH
```

After adding these lines, restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc, depending on your shell
```

## Downloading the Skills

The best way to download the skills is to use the git clone command:

```sh
cd ~/projects  # or your preferred workspace directory
git clone https://github.com/dmccreary/ibook-skills.git
```

This assumes that `projects`  is the directory where you check out your GitHub repositories. 
You can use any directory you prefer, just remember to update your `BK_HOME` environment variable accordingly.

## Installing Book-Building Scripts

Before installing the Claude skills, you should install the book-building utility scripts. 
These are scripts prefixed with `bk-` that help you manage and build intelligent textbooks.

Run the installation script:

```sh
cd $BK_HOME/scripts
./bk-install-scripts
```

This script will:
- Create symbolic links for all `bk-*` scripts in `$BK_HOME/scripts/`
- Place the links in `$HOME/.local/bin` for easy command-line access
- Verify that `$HOME/.local/bin` is in your PATH
- Display a list of all installed book utilities

After installation, you can use commands like `bk-book-status`, `bk-build`, and other book utilities from anywhere in your terminal.

## Installing Claude Skills

After you have downloaded the repository and installed the book-building scripts, you have two options for installing the Claude skills:

1. **Personal Level:** Install these skills for ALL your projects. (Recommended)
2. **Project Level:** Install these skills for a specific project

The first option will allow you to work on many different intelligent textbook projects without duplicating the skills on your local computer. It is highly recommended.

The only reason that you might want to use the second option for specific projects is if you are doing complex development such as creating different versions of these skills.

## Skill Installation for ALL Projects

We will do this by creating symbolic links from each agent's skills directory to the
skills in the cloned repository.

Run the installation script:

```sh
bk-install-skills
```

It installs into every agent present on the machine, so the three stay in sync:

```
▸ Claude Code -> ~/.claude/skills
    linked book-chapter-generator
    linked book-installer
    linked chapter-content-generator
    ...
    14 linked, 0 already current, 0 pruned
    1 slash command(s) -> ~/.claude/commands

▸ OpenAI Codex -> ~/.codex/skills
    14 linked, 0 already current, 0 pruned
    wrapped command ibook as a Codex skill

▸ Google Antigravity -> ~/.gemini/antigravity/skills
    14 linked, 0 already current, 0 pruned

Summary: 42 linked, 0 already current, 0 pruned, 2 extra(s)
Served: claude codex antigravity
✓ All selected agents are current.
```

Agents that aren't installed on the machine are skipped. Narrow the run with
`--only claude`, preview it with `--dry-run`, or inspect current state with
`--list`.

## Getting Updates

These skills will be updated frequently. To install the latest release, just run git pull:

```sh
cd $BK_HOME
git pull
```

After pulling updates, you may need to re-run the installation scripts if new scripts or skills were added:

```sh
cd $BK_HOME/scripts
./bk-install-scripts   # For book-building utilities
./bk-install-skills    # For agent skills
```

## Details of the Installation script

The script will create a set of symbolic link commands, one for each skill file in this repo.

```sh
#!/bin/bash

   # Create the target directory if it doesn't exist
   # CHANGE $HOME to be the project you are working on
   # $HOME = ~
   # $HOME = /User/NAME/projects/PROJECT_NAME/.claude/skills
   mkdir -p $HOME/.claude/skills

   # Get the absolute path of the skills directory
   SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/skills" && pwd)"

   # Create symbolic links for each skill folder
   for skill_dir in "$SKILLS_DIR"/*; do
       if [ -d "$skill_dir" ]; then
           skill_name=$(basename "$skill_dir")
           target_link="$HOME/.claude/skills/$skill_name"

           # Remove existing symlink if it exists
           if [ -L "$target_link" ]; then
               rm "$target_link"
           fi

           # Create the symbolic link
           ln -s "$skill_dir" "$target_link"
           echo "Created symlink: $HOME/.claude/skills/$skill_name -> $skill_dir"
       fi
   done

   echo "Done! All skill symlinks created in $HOME/.claude/skills"
```

If you want to change the links to work in your specific project, just change the
path where the links are created.

Change:

```sh
$HOME = ~
```

to be:

```sh
$HOME = /User/NAME/projects/PROJECT_NAME/.claude/skills
```

## Testing Your Skill List

```
What skills do you know about.  Check the ~/.claude/skills/ area.
```

Response:

```
You have 8 skills installed in ~/.claude/skills/:

  1. faq-generator - Generates FAQ content
  2. glossary-generator - Creates glossary entries
  3. intelligent-textbook - Works with intelligent textbook content
  4. intelligent-textbook-creator - Creates intelligent textbooks
  5. learning-graph-generator - Generates learning graphs
  6. microsim-p5 - Creates p5.js micro-simulations
  7. moving-rainbow - Creates moving rainbow animations
  8. quiz-generator - Generates quiz content
```

## Add the /ibook Command

Claude Code allows you to add custom slash commands defined by markdown files in
`~/.claude/commands/` (or `.claude/commands/` inside a project). This repository
ships one: `/ibook`, the runbook that tells you which skill to run next.

**Option 1: Install globally (recommended):**
```sh
bk-install-skills
```

In addition to symlinking every skill into each agent's skills directory, this
symlinks every command in `commands/*.md` into `~/.claude/commands/` — so
`/ibook` and any future command become available globally.

**Option 2: Install for a specific project:**
```sh
mkdir -p .claude/commands
cp $BK_HOME/commands/ibook.md .claude/commands/ibook.md
```

To list installed skills there is no slash command — ask Claude directly, or run
`bk-list-skills` from the shell.

## Sample Slash Command Execution

Type `/ib` into Claude Code and the `/ibook` command should be listed

![](img/claude-code-skill-command.png)

**Result:**

```
Available Claude Skills (8 total)

  Educational Content Creation:
  - faq-generator (user) - Generates FAQs from course content
  - glossary-generator (user) - Creates ISO 11179-compliant glossaries
  - quiz-generator (user) - Creates Bloom's Taxonomy-aligned quizzes

  Intelligent Textbook Development:
  - intelligent-textbook (user) - Complete workflow for AI-generated textbooks
  - intelligent-textbook-creator (user) - Creates MkDocs Material textbooks (Level 2-5)
  - learning-graph-generator (user) - Generates 300-600 concept learning graphs

  Interactive Simulations:
  - microsim-p5 (user) - Creates p5.js educational MicroSims

  Hardware Projects:
  - moving-rainbow (user) - MicroPython for Raspberry Pi Pico NeoPixels

  All 8 skills are from your user directory (~/.claude/skills/). No project-specific skills found in .claude/skills/.

```

## Verifying Your Installation

After completing all installation steps, verify everything is working:

**1. Check environment variables:**
```sh
echo $BK_HOME
# Should output: /Users/YOUR_USERNAME/Documents/ws/ibook-skills (or your path)

echo $PATH | grep -o "$HOME/.local/bin"
# Should output: /Users/YOUR_USERNAME/.local/bin
```

**2. Check book-building utilities:**
```sh
which bk-book-status
# Should output: /Users/YOUR_USERNAME/.local/bin/bk-book-status

bk-book-status --help  # Test a book utility
```

**3. Check Claude skills:**
```sh
ls ~/.claude/skills/
# Should list all installed skills (learning-graph-generator, glossary-generator, etc.)
```

**4. Test the /ibook command in Claude Code:**
Type `/ibook` in Claude Code and it should show the textbook build runbook.
To list installed skills, run `bk-list-skills` or just ask Claude.

## Configuring Permissions

The default Claude Code permission behavior is very strict and will prompt you for many operations. For efficient workflow when working on textbook projects, you can configure permissions to be more permissive.

**IMPORTANT**: Only use permissive settings when working in a safe, version-controlled directory (like a Git repository). This way, you can always revert unwanted changes.

Create or edit `.claude/settings.json` in your project directory:

```json
{
  "permissions": {
    "allow": [
      "Skill(*)",
      "Bash(*:*)",
      "FileSystem(read:./**/*.*,write:./**/*.*)"
    ],
    "deny": [],
    "ask": []
  }
}
```

This configuration:
- Allows all skills to run without prompting
- Allows all bash commands
- Allows reading and writing all files in the current project directory (`./**/*.*`)

Since your work is in a Git repository, you can always review changes with `git diff` and revert if needed.

## Troubleshooting

### BK_HOME not set error

If you get an error saying `BK_HOME environment variable is not set`:

1. Add the export to your shell startup file (see Prerequisites section)
2. Restart your terminal or run: `source ~/.bashrc` (or `~/.zshrc`)
3. Verify with: `echo $BK_HOME`

### Scripts not found in PATH

If you get `command not found` when trying to run `bk-*` commands:

1. Check that `~/.local/bin` is in your PATH: `echo $PATH | grep .local/bin`
2. Add the export to your shell startup file (see Prerequisites section)
3. Restart your terminal or run: `source ~/.bashrc` (or `~/.zshrc`)
4. Re-run the installation: `cd $BK_HOME/scripts && ./bk-install-scripts`

### Skills not showing up in Claude Code

If skills don't appear when you try to use them:

1. Check that symlinks were created: `ls -la ~/.claude/skills/`
2. Re-run the installation: `bk-install-skills`
3. Restart Claude Code
4. Ask Claude: "What skills do you have access to?", or run `bk-list-skills`

### /ibook command not working

If the `/ibook` slash command doesn't work:

1. Check that the command file exists: `ls ~/.claude/commands/ibook.md`
2. Re-run: `bk-install-skills`
3. Restart Claude Code

(There is no `/skills` command; it was retired. Use `bk-list-skills`.)

### Permission denied when running scripts

If you get permission denied errors:

1. Make scripts executable: `chmod +x $BK_HOME/scripts/*.sh`
2. For specific scripts: `chmod +x $BK_HOME/scripts/bk-install-scripts`

## Next Steps

Once you have successfully installed the skills and utilities, you can:

1. **Create a new intelligent textbook project** - Use the `intelligent-textbook-creator` skill
2. **Generate a learning graph** - Use the `learning-graph-generator` skill
3. **Create interactive simulations** - Use the `microsim-p5` skill
4. **Generate course content** - Use the `glossary-generator`, `quiz-generator`, and `faq-generator` skills

For detailed documentation on each skill, visit the [skills documentation](https://dmccreary.github.io/ibook-skills/) or run `bk-list-skills`.



