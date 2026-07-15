# forje-ai

[🇧🇷 Português](./README.md) | 🇺🇸 English

> Personal skill plugin for [Claude Code](https://claude.com/claude-code) — my way of working on personal projects, packaged so I can carry it from repo to repo (and lend it out to whoever wants it).

This carries no compliance rules, no data-protection checklist, no
corporate process — it's built for personal projects: no ticket, no
approval from anyone else, no audit checklist. Free to use: clone, change,
and redistribute as you like.

## Table of contents

- [What this is](#what-this-is)
- [How it works](#how-it-works)
- [Installation](#installation)
- [How to test it](#how-to-test-it)
- [Day-to-day usage](#day-to-day-usage)
- [The skills](#the-skills)
- [Why "living docs" save tokens (and time)](#why-living-docs-save-tokens-and-time)
- [Repo structure](#repo-structure)
- [How to add a new skill](#how-to-add-a-new-skill)
- [Roadmap / future ideas](#roadmap--future-ideas)
- [License](#license)

## What this is

A **Claude Code plugin**: a bundle of `skills` (`SKILL.md` files with
natural-language instructions) that Claude Code loads automatically once
the plugin is enabled. Each skill teaches Claude to run a type of task the
way I prefer — implementing a feature, reviewing code, keeping context docs
up to date, or grilling me with questions before I make a rushed decision.

The core idea: my personal projects are small, have no ticket tracker, no
other dev reviewing alongside me — but I still benefit from the same
discipline of "plan before coding" and "documentation that keeps itself in
sync" that I rely on professionally. This plugin is that discipline, minus
the corporate scaffolding around it.

## How it works

A Claude Code plugin is just a folder with a manifest and a collection of
skills:

```
forje-ai/
├── .claude-plugin/
│   ├── plugin.json        # plugin name, version, description
│   └── marketplace.json   # how Claude Code discovers/installs this plugin
└── skills/
    └── <skill-name>/
        └── SKILL.md        # frontmatter (name + description) + instructions
```

When the plugin is enabled in a session, Claude Code reads the `name` and
`description` of every `SKILL.md` (without loading the full body) and uses
that to decide, from your natural-language request, which skill to invoke —
there's no magic keyword or memorized command. Asking "review the code I
just wrote" is enough for Claude to recognize that `forje-code-review`
applies and load its full content only at that moment.

One thing this plugin deliberately does **not** do: force-load the skill
index on every session via a `SessionStart` hook. `forje-registry` is just
another skill; Claude invokes it when it makes sense (for example, if you
ask "what skills do I have available here?"). That's intentional — it keeps
the plugin simple and avoids a fixed token cost every session. If I ever
want that guarantee, it's a matter of adding a `hooks/hooks.json` — see
[Roadmap](#roadmap--future-ideas).

## Installation

Prerequisite: [Claude Code](https://claude.com/claude-code) installed.

### 1. Have the repo somewhere Claude Code can reach

Local (testing on your own machine) or a remote git repo (GitHub, say, if
you're installing on another machine or sharing with someone):

```bash
git clone https://github.com/<your-username>/forje-ai.git
```

### 2. Register the marketplace

Inside a Claude Code session (any directory):

```
/plugin marketplace add C:/path/where/you/cloned/forje-ai
```

— or, from GitHub directly:

```
/plugin marketplace add https://github.com/<your-username>/forje-ai.git
```

### 3. Install the plugin

```
/plugin install forje-ai@forje-ai
```

### 4. Enable it wherever you want to use it

By default the plugin becomes available globally (`user` scope) right
after `install`. To check or disable it, `/plugin` opens the interactive
manager. Under the hood, this writes an entry to `~/.claude/settings.json`:

```jsonc
{
  "enabledPlugins": {
    "forje-ai@forje-ai": true
  },
  "extraKnownMarketplaces": {
    "forje-ai": {
      "source": { "source": "git", "url": "https://github.com/<your-username>/forje-ai.git" }
    }
  }
}
```

Editing that file directly works too, but prefer the `/plugin` commands —
they take care of the cache and `installed_plugins.json` for you.

## How to test it

Once installed, open Claude Code in any personal project (any folder with
code) and verify each piece:

**1. The skills show up in the picker.** Type `/` and check that
`forje-ai:forje-flow-feature` (and the others) appear in the list — this
confirms the plugin installed and each `SKILL.md` has valid YAML
frontmatter (broken frontmatter makes a skill silently disappear from the
list).

**2. Natural-language invocation.** Without typing `/`, write a request that
matches a skill's trigger and see if Claude invokes it on its own, for
example:

```
review the code I just wrote
```

If it mentions using `forje-code-review`, it worked.

**3. Explicit invocation.** If you want to force a specific skill without
relying on automatic matching:

```
/forje-ai:forje-code-review
```

**4. End-to-end flow.** The most realistic test: pick a small personal
project (or spin up a throwaway one) and run the full cycle —
`forje-docs-bootstrap` to generate the docs, then ask for a small feature
(`forje-flow-feature` should load the generated docs instead of scanning
the project from scratch), then `forje-code-review` on the resulting diff.

## Day-to-day usage

There's no command to memorize — it's just normal conversation. A few
example requests and the skill they trigger:

| You say | Skill that kicks in |
|---|---|
| "create an endpoint that lists the user's orders" | `forje-flow-feature` |
| "review this code before I commit" | `forje-code-review` |
| "generate docs for this project, it has nothing documented" | `forje-docs-bootstrap` |
| "the docs for this project look out of date" | `forje-docs-sync --report` |
| "I just changed the payment flow, update the docs" | `forje-docs-sync --apply` |
| "grill me about this decision to use a queue instead of a webhook" | `forje-grilling` |
| "I want to create a new skill for myself" | `forje-skill-authoring` |

## The skills

### `forje-flow-feature` — implement without process
Drives a feature, bug fix, or refactor from request to tested code:
understands the request, loads the project's `CLAUDE.md`/living docs (if
any), decides whether it's worth pausing to sketch a plan before coding
(trivial changes skip it; changes involving a design decision don't),
implements following the conventions the repo already uses, and tests the
happy path plus at least one failure case. No ticket, no external approval
— just enough structure to avoid coding blind.

### `forje-code-review` — a second pair of eyes
Read-only review of the current diff (or a specific branch). Lean
checklist: does the code do what it's supposed to and handle errors? Is
there abstraction beyond what the task needed? Any hardcoded secret,
injection risk, unnecessary dependency? Every finding comes with
`file:line` and a classification (blocking / important / suggestion) — no
empty praise, no unsubstantiated nitpicks.

### `forje-docs-sync` — keeps documentation living
An engine that compares the context docs (`docs/*.md`, declared in a
`.claude/context.yaml` manifest) against the current state of the code and
flags what drifted. Runs in two modes: `--report` (lists drift only,
touches nothing — used before planning from the docs) and `--apply` (fixes
the docs, used at the end of an implementation to record what changed).
This skill is the reason the docs don't rot after the first week.

### `forje-docs-bootstrap` — generates documentation from scratch
For when the project has no context doc yet. Detects the project's profile
(.NET backend, Node, Python, React/Vite frontend) from evidence in the repo
itself (`.csproj`, `package.json`, `pyproject.toml`...), confirms the set of
docs to generate with you, and produces one document at a time — each with
a dedicated read of the code, never a shallow "general summary". Finishes
by creating `.claude/context.yaml`, the manifest that `forje-docs-sync`
uses afterward.

### `forje-grilling` — interrogates me before I mess up
For decisions with several dependent branches ("if I choose A here, that
changes what I do at B and C down the line"), a generic confirmation ("does
this make sense, should I proceed?") lets the hidden implication slip by.
This skill runs an interview instead: one question at a time, each already
paired with a recommendation and the reasoning behind it, never two
questions bundled together, only acting once no ambiguity is left.

### `forje-skill-authoring` — how to author a new skill in this plugin
Meta-skill: naming conventions, file structure, frontmatter format, and the
checklist I follow before considering a skill done — no compliance
scaffolding, just clarity and consistency.

## Why "living docs" save tokens (and time)

This is the part most worth understanding, because it isn't obvious at
first glance.

**The problem without living docs.** Every time you ask for something in a
project Claude "doesn't know" yet, it has to rebuild its understanding from
scratch: open the folder tree, grep for conventions, read several files to
infer the architecture, piece together business rules scattered across the
code. That burns a large amount of context tokens — and it repeats **every
new session**, because Claude doesn't retain memory from one session to the
next.

**What `forje-docs-bootstrap` does.** It pays that exploration cost **once**,
in a structured way (one doc at a time, each with a defined focus —
architecture, folder structure, conventions, business rules), and writes
the result as markdown inside the repo itself. From then on, understanding
the project no longer requires reading the entire codebase — just 3 or 4
doc files, which are orders of magnitude smaller than the full codebase.

**What `forje-docs-sync` does on top of that.** Instead of re-reading the
full docs against the full code every time (which would still be
expensive), it keeps a marker (`sync.last_synced_commit`) and only looks at
the **diff** since the last sync — `git log`/`git diff` over a handful of
files, not a full audit. Drift is the exception, not the rule: most
sessions don't touch anything the docs cover, so `--report` finishes in
seconds without spending tokens reading unchanged code.

**What `.claude/context.yaml` does on top of that.** Each doc declares which
folders (`covers`) it describes. When a skill like `forje-flow-feature`
needs context, it cross-references the requested task with that mapping
and loads **only the relevant docs** for that change — not the whole set. A
task that only touches the payment module doesn't pull in the
authentication doc alongside it. This keeps the context window lean even in
projects with many accumulated docs.

Summing up the chain: **bootstrap** trades "read the code every session" for
"read the docs every session" (much cheaper) → **incremental sync** trades
"re-read everything" for "re-read only what changed" (cheaper still) →
**manifest with `covers`** trades "load every doc" for "load only the docs
relevant to the task" (leaving the rest of the context budget for the code
itself, which is what actually matters during implementation).

## Repo structure

```
forje-ai/
├── .claude-plugin/
│   ├── plugin.json         # plugin manifest (name, version, description)
│   └── marketplace.json    # marketplace manifest (how to install)
├── skills/
│   ├── forje-registry/         # index — read this first to see what exists
│   ├── forje-flow-feature/     # implement without process
│   ├── forje-code-review/      # personal review
│   ├── forje-docs-sync/        # keeps living docs up to date
│   ├── forje-docs-bootstrap/   # generates living docs from scratch
│   ├── forje-grilling/         # interview before a non-trivial decision
│   └── forje-skill-authoring/  # how to author a new skill here
├── README.md        # this file, in Portuguese
└── README.en.md      # English version
```

## How to add a new skill

1. Create `skills/<name>/SKILL.md` with frontmatter `name` (matching the
   folder name) + `description` (what it does + when to invoke it, in 1-2
   sentences — this is the text that decides whether Claude recognizes the
   trigger).
2. Follow the structure and checklist in `forje-skill-authoring` — short
   body, numbered steps, hard rules only when there's something that should
   never happen.
3. List the skill in the table in `skills/forje-registry/SKILL.md`.
4. If the change is something worth distributing (new skill, behavior
   tweak), bump the version in `.claude-plugin/plugin.json` **and**
   `.claude-plugin/marketplace.json` (same number in both) — that's what
   lets anyone who already installed it notice there's an update.

## Roadmap / future ideas

- `hooks/` with `SessionStart` — in case I ever want the skill index to
  always load, instead of relying on description-based recognition.
- A new-project setup skill (`forje-flow-init`?) — scaffolding for a
  preferred language/framework, already wired with `.gitignore`, lint, and
  test config.

## License

MIT — see [`LICENSE`](./LICENSE). Use, copy, modify, and redistribute
freely; keep the copyright notice.
