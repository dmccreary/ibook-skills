# Workshop Pre-Work

Before you come to the workshop you must have Claude Code installed
with all the intelligent textbook skills installed in a Claude Code
skills directory. You should also have a GitHub account
created and an initial GitHub repository setup with a
template intelligent textbook installed in the GitHub
repository. Having all these components installed
before you come to our class allows us all to focus
on creation of the textbook, not the installation of
the software.

!!! warning "System Requirements"
    Claude Code is a Linux shell system. You must have one of the following:

    1. A Mac running macOS
    2. A PC running Linux
    3. A virtual machine such as Docker running Linux
    4. A Raspberry Pi
    5. A Windows system running WSL (Windows Subsystem for Linux)
    6. A cloud-server account running Linux

    **Claude Code does not run well on native Windows.** Windows users must install WSL first.

---

## Step 1: Create a GitHub Account

If you don't already have a GitHub account:

1. Go to [https://github.com](https://github.com)
2. Click **Sign up**
3. Follow the prompts to create your account
4. Verify your email address

!!! tip "Verification"
    You should be able to log in at [https://github.com](https://github.com) and see your dashboard.

---

## Step 2: Create Your Book Repository

1. Log in to GitHub
2. Click the **+** icon in the top right corner
3. Select **New repository**
4. Name your repository (e.g., `my-intelligent-book`)
5. Select **Public** (required for GitHub Pages)
6. Check **Add a README file**
7. Click **Create repository**

!!! tip "Verification"
    Your repository should be visible at `https://github.com/YOUR_USERNAME/my-intelligent-book`

---

## Step 3: Create a Claude Account

You need a Claude Pro ($20/month) or Max ($100/month) subscription to use Claude Code.

1. Go to [https://claude.ai](https://claude.ai)
2. Sign up or log in
3. Navigate to your account settings
4. Subscribe to Claude Pro or Max

!!! hint "Which Plan?"
    - **Pro ($20/month)**: Good for learning and moderate usage
    - **Max ($100/month)**: Better for heavy usage and longer conversations

---

## Step 4: Install Claude Code

Follow the official quickstart guide to install Claude Code:

**For macOS/Linux:**

```bash
npm install -g @anthropic-ai/claude-code
```

Or if you don't have npm:

```bash
curl -fsSL https://claude.ai/install.sh | sh
```

!!! note "Detailed Instructions"
    See the full [Claude Code Quickstart Guide](https://docs.anthropic.com/en/docs/claude-code/quickstart) for your specific platform.

!!! tip "Verification"
    Run the following command to verify installation:
    ```bash
    claude --version
    ```
    You should see a version number displayed.

---

## Step 5: Log In to Claude Code

1. Open your terminal
2. Run the `claude` command:
   ```bash
   claude
   ```
3. Once Claude Code starts, type:
   ```
   /login
   ```
4. Follow the prompts to authenticate with your Claude account

!!! tip "Verification"
    After logging in, you should see a message confirming your authentication.

---

## Step 6: Install Package Managers

### For macOS Users

Install Homebrew (the macOS package manager):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

!!! warning "Admin Rights Required"
    You must have administrator privileges on your Mac to install Homebrew.

After installation, follow the instructions displayed to add Homebrew to your PATH.

!!! tip "Verification"
    ```bash
    brew --version
    ```
    You should see a version number like `Homebrew 4.x.x`.

### For Windows Users (WSL)

1. Open PowerShell as Administrator
2. Run:
   ```powershell
   wsl --install
   ```
3. Restart your computer
4. Open "Ubuntu" from the Start menu
5. Create a username and password when prompted

!!! tip "Verification"
    Open Ubuntu and run:
    ```bash
    lsb_release -a
    ```
    You should see Ubuntu version information.

---

## Step 7: Install GitHub CLI (`gh`)

The GitHub CLI allows Claude Code to authenticate with your GitHub account.

**For macOS:**
```bash
brew install gh
```

**For Ubuntu/Debian/WSL:**
```bash
sudo apt update
sudo apt install gh
```

!!! tip "Verification"
    ```bash
    gh --version
    ```
    You should see output like `gh version 2.x.x`.

---

## Step 8: Authenticate GitHub CLI

1. Run the authentication command:
   ```bash
   gh auth login
   ```
2. Select **GitHub.com**
3. Select **HTTPS**
4. Select **Yes** when asked to authenticate Git with your GitHub credentials
5. Select **Login with a web browser**
6. Copy the one-time code displayed
7. Press Enter to open your browser
8. Paste the code and authorize the application

!!! tip "Verification"
    ```bash
    gh auth status
    ```
    You should see: `Logged in to github.com as YOUR_USERNAME`

---

## Step 9: Create Your Projects Directory

Create a directory to hold all your projects:

```bash
mkdir -p ~/projects
cd ~/projects
```

!!! tip "Verification"
    ```bash
    pwd
    ```
    Should display `/Users/YOUR_USERNAME/projects` (macOS) or `/home/YOUR_USERNAME/projects` (Linux/WSL).

---

## Step 10: Clone Your Book Repository

Replace `YOUR_USERNAME` with your actual GitHub username:

```bash
cd ~/projects
git clone https://github.com/YOUR_USERNAME/my-intelligent-book.git
```

!!! tip "Verification"
    ```bash
    ls ~/projects
    ```
    You should see `my-intelligent-book` listed.

---

## Step 11: Clone the Claude Skills Repository

```bash
cd ~/projects
git clone https://github.com/dmccreary/ibook-skills.git
```

!!! tip "Verification"
    ```bash
    ls ~/projects
    ```
    You should see both `my-intelligent-book` and `ibook-skills` listed.

---

## Step 12: Configure Your Shell Environment

Add environment variables to your shell configuration file.

**For macOS (zsh):**
```bash
echo 'export BK_HOME="$HOME/projects/ibook-skills"' >> ~/.zshrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
```

**For Linux/WSL (bash):**
```bash
echo 'export BK_HOME="$HOME/projects/ibook-skills"' >> ~/.bashrc
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

Now reload your shell configuration:

**For macOS:**
```bash
source ~/.zshrc
```

**For Linux/WSL:**
```bash
source ~/.bashrc
```

!!! tip "Verification"
    ```bash
    echo $BK_HOME
    ```
    Should display `/Users/YOUR_USERNAME/projects/ibook-skills` or `/home/YOUR_USERNAME/projects/ibook-skills`.

---

## Step 13: Install the Book-Building Scripts

```bash
cd ~/projects/ibook-skills
./scripts/bk-install-scripts
```

!!! tip "Verification"
    ```bash
    which bk
    ```
    Should display a path like `/Users/YOUR_USERNAME/.local/bin/bk`.

---

## Step 14: Install the Claude Skills

```bash
./scripts/bk-install-skills
```

!!! tip "Verification"
    ```bash
    ls ~/.claude/skills
    ```
    You should see a list of skills including `learning-graph-generator`, `microsim-generator`, etc.

---

## Step 15: Install MkDocs

This installs MkDocs and the Material theme using Conda:

```bash
bk-install-mkdocs
```

!!! note "This May Take Several Minutes"
    The script creates a Conda environment and installs all required Python packages.

!!! tip "Verification"
    ```bash
    conda activate mkdocs
    mkdocs --version
    ```
    Should display something like `mkdocs, version 1.x.x`.

---

## Step 16: Initialize Your Book

```bash
cd ~/projects/my-intelligent-book
mkdocs new .
```

This creates the basic MkDocs structure with:

- `mkdocs.yml` - Configuration file
- `docs/index.md` - Your homepage

!!! tip "Verification"
    ```bash
    ls
    ```
    You should see `mkdocs.yml` and a `docs` directory.

---

## Step 17: Commit and Push Your Changes

```bash
git status
git add .
git commit -m "Initial MkDocs setup"
git push
```

!!! tip "Verification"
    Go to your repository on GitHub. You should see the `mkdocs.yml` file and `docs` folder.

---

## Step 18: Deploy to GitHub Pages

```bash
mkdocs gh-deploy
```

This builds your site and deploys it to GitHub Pages.

!!! warning "First Deployment"
    The first deployment may take a few minutes. You may also need to enable GitHub Pages in your repository settings:

    1. Go to your repository on GitHub
    2. Click **Settings** → **Pages**
    3. Under "Source", select **Deploy from a branch**
    4. Select the **gh-pages** branch
    5. Click **Save**

!!! tip "Verification"
    Your book should be visible at:
    ```
    https://YOUR_USERNAME.github.io/my-intelligent-book
    ```
    (Replace `YOUR_USERNAME` with your GitHub username)

---

## Testing Your Installation

Run through these tests to verify everything is working correctly.

### Test 1: Verify Skills Are Installed

List your installed skills:

```sh
ls ~/.claude/skills
```

You should see output similar to:

```
book-chapter-generator          glossary-generator              moving-rainbow
book-installer                  learning-graph-generator        pi-keys-generator
chapter-content-generator       linkedin-announcement-generator quiz-generator
concept-classifier              microsim-generator              readme-generator
faq-generator                   microsim-utils                  reference-generator
                                                                skill-creator
```

!!! success "Expected Result"
    You should see approximately 15-20 skill directories listed.

### Test 2: Verify the `bk` Command

Run the book utilities menu:

```sh
bk
```

You should see a menu like this:

```
════════════════════════════════════════════════════════════════
Build/Book Utilities
════════════════════════════════════════════════════════════════
BK_HOME: /home/YOUR_USERNAME/projects/ibook-skills

   1. bk                                  Build/Book utilities menu
   2. bk-analyze-skill-usage              Generate a comprehensive skill usage analysis...
   3. bk-batch-capture-screenshots        Batch Screenshot Capture for MicroSims
   ...
════════════════════════════════════════════════════════════════
```

!!! success "Expected Result"
    The menu should display with `BK_HOME` pointing to your ibook-skills directory.

!!! warning "Troubleshooting"
    If you see `command not found: bk`, make sure you:

    1. Ran `./scripts/bk-install-scripts` from the ibook-skills directory
    2. Added `$HOME/.local/bin` to your PATH
    3. Reloaded your shell with `source ~/.zshrc` or `source ~/.bashrc`

### Test 3: Verify Your Book Is Published

Open your browser and navigate to:

```
https://YOUR_USERNAME.github.io/my-intelligent-book
```

Replace `YOUR_USERNAME` with your actual GitHub username.

!!! success "Expected Result"
    You should see your MkDocs site with a default homepage.

!!! warning "Troubleshooting"
    If you see a 404 error:

    1. Wait a few minutes - GitHub Pages can take time to deploy
    2. Check your repository settings to ensure GitHub Pages is enabled
    3. Verify the `gh-pages` branch exists in your repository

---

## Testing Claude Code Skills

Now let's verify Claude Code can see and use your skills.

### Test 4: Start Claude Code

```bash
cd ~/projects/my-intelligent-book
claude
```

### Test 5: Ask About Available Skills

Once Claude Code starts, type:

```
What skills do you know about for building intelligent textbooks and MicroSims?
```

!!! success "Expected Result"
    Claude should list skills including:

    - `learning-graph-generator`
    - `microsim-generator`
    - `chapter-content-generator`
    - `glossary-generator`
    - And others...

### Test 6: List All Skills

You can also list them from the shell:

```
bk-list-skills
```

!!! success "Expected Result"
    Claude should display a formatted list of all available skills with their descriptions.

---

## Quick Reference Checklist

Use this checklist to verify your installation is complete:

- [ ] GitHub account created and logged in
- [ ] Book repository created (`my-intelligent-book`)
- [ ] Claude Pro or Max subscription active
- [ ] Claude Code installed (`claude --version` works)
- [ ] Logged in to Claude Code (`/login` completed)
- [ ] Homebrew installed (macOS) or WSL installed (Windows)
- [ ] GitHub CLI installed (`gh --version` works)
- [ ] GitHub CLI authenticated (`gh auth status` shows logged in)
- [ ] Projects directory created (`~/projects`)
- [ ] Book repository cloned
- [ ] Claude-skills repository cloned
- [ ] Environment variables set (`echo $BK_HOME` shows path)
- [ ] Book scripts installed (`which bk` shows path)
- [ ] Claude skills installed (`ls ~/.claude/skills` shows skills)
- [ ] MkDocs installed (`mkdocs --version` works)
- [ ] Book initialized (`mkdocs.yml` exists)
- [ ] Changes committed and pushed to GitHub
- [ ] Book deployed to GitHub Pages (site is visible)

!!! tip "Need Help?"
    If you encounter issues during setup, please:

    1. Take a screenshot of any error messages
    2. Note which step you're on
    3. Bring your questions to the workshop - we'll help you troubleshoot!

---

## What's Next?

Once you've completed all the pre-work, you're ready for the workshop! We'll cover:

1. Creating your course description
2. Generating a learning graph
3. Building chapter structures
4. Creating interactive MicroSims
5. Publishing your intelligent textbook

See you at the workshop!