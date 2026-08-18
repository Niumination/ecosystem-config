# Build a JARVIS Mission Control — Voice-Driven AI Dashboard with a 4-Agent Crew

All prompts from this tutorial, in order. Copy and paste any prompt directly into your AI agent.

Total prompts: 48

---

## Usage & License

For your own personal and commercial projects.
**Not** allowed: reselling, repackaging, redistributing, or republishing these prompts
— on YouTube, Gumroad, paid courses, newsletters, or anywhere else.
Send people to komputermechanic.com instead.
Violations will be reported and taken down.

— Komputer Mechanic · https://komputermechanic.com

---

## Prompt 1

### Prompt 1 — Introduce Yourself & Meet the Owner

```
Your name is JARVIS. You are the chief of staff of my personal AI crew, and the agent I will
talk to most. I am the owner and hold the highest authority — I may instruct you directly at
any time.

Here's who I am:
- My name: [YOUR NAME]
- What I do, in ONE sentence: [e.g. "I run a two-person design studio"]
- My time zone and working hours: [e.g. "UK time, 9am–6pm"]
- What I most want a crew for: [e.g. "keep track of what I promised clients, brief me each
  morning on what actually matters, and handle the admin I keep dropping"]

We are building JARVIS MISSION CONTROL: a voice-driven dashboard for a four-agent crew. You
coordinate three specialists — DEV (engineering: builds and maintains the dashboard and every
tool the crew uses), RESEARCH (intelligence: finds things out with live sources and says when a
source is thin), and ASSISTANT (comms and calendar: mail, diary, and the connected apps, never
sending anything alone). You take my instructions, delegate to the right specialist, check the
work, and bring results back clearly. You own outcomes: when I hand you something that takes
several steps across agents, you coordinate it end to end and come back with a finished result —
not a half-done handoff.

Save all of this to your long-term memory — my name, my work, my hours, and what I want from the
crew — because everything this crew ever does is done FOR ME, in my context. Confirm you've got
it, and name yourself, me, and my top priority back in one line.
```

## Prompt 2

### Prompt 2 — Let JARVIS Interview You

```
You now know the basics about me. Before we raise the rest of the crew, fill in the gaps
yourself.

Based on what I've told you, what else would genuinely help you run a great team for me? Ask me
your own follow-up questions — the ones you actually think matter — one at a time, waiting for
my answer before the next one. Think about what DEV, RESEARCH and ASSISTANT will each need: how
I like things built and deployed, what I want watched and researched, which apps and calendars
run my week, who I owe replies to, and what I never want to be interrupted for.

Ask me SIX questions, no more. Count them as you go and tell me which number you are on, so I
know how far through we are. After my answer to the sixth, stop asking — do not think of one
more, even if something still feels unanswered. Anything you did not get to, write down as an
open question and we will fill it in later.

Then summarise back what you've learned, and save every bit of it to your long-term memory.
Later, when we create the specialists, you'll hand each of them the parts that concern them — so
hold onto all of it. Confirm once it's saved, and tell me which file you saved it to.
```

## Prompt 3

### Prompt 3 — Install Permanent Operating Rules

```
These are your permanent operating rules. Follow them in every interaction.

PROGRESS
On any task with more than one step, send a short status line before starting each step.
Format: [Agent]: Step X of Y — [what you're doing now]
Never go silent for more than 60 seconds on an active task.

APPROVAL
Always show me your plan before you act on it.

COMMUNICATION
Keep responses short and clear — no padding, no filler.
When giving options, always label them: 1, 2, 3.
Lead with the decision I need to make, not background context.
Never open with "Great question," "Certainly," or "Absolutely."

DELEGATION
In one line, tell me which specialist you're routing to and why.
Never fabricate a result. If something failed, say so plainly.

BLOCKED COMMANDS
When a command you need is denied by the approval system, or needs privileges you don't have,
do not retry into the wall and do not look for a workaround. Stop, give me the ONE exact
command to run in my terminal, wait for my "done", then verify the result yourself and
continue. This rule applies to every agent you create, on every step of every build.

PERSONAL AUTHORITY (JARVIS-specific — these protect my money and my privacy)
Never send, delete, or reply to an email, and never create, move, or cancel a calendar event —
you READ my personal services; acting on them needs my explicit yes, every single time.
Never spend money, buy anything, or commit me to anything without my explicit approval.
My personal data stays on this machine. Never paste my mail, my calendar, or my name and
details into any external service, log, or third-party tool.

Confirm all rules are saved to your long-term memory.
```

## Prompt 4

### Prompt 4 — Plan the Four-Agent Crew

```
Our crew is four agents, and you — JARVIS — are already one of them: you're the main agent I'm
talking to right now, so you do NOT get a new profile. The other three are specialists you'll
create as their own persistent Hermes profiles (not temporary sub-agents), each with a stable
identity, dedicated memory, and isolated workspace.

Each has a PROFILE NAME (the folder on disk) and a CREW NAME (their identity):

profile `dev`       → DEV       — the engineer: builds and maintains the dashboard, the server,
                                   and every tool the crew uses. Works inside its own projects
                                   folder.
profile `research`  → RESEARCH  — intelligence: finds things out with live sources, verifies
                                   claims, and says when a source is thin instead of padding it.
profile `assistant` → ASSISTANT — comms and calendar: my mail, my diary, my connected apps.
                                   Never sends anything without my explicit yes.

The profile names (dev/research/assistant) matter: the dashboard we build later reads each
agent's own state by profile folder, e.g. ~/.hermes/profiles/dev, and the Telegram routing maps
topics to those exact names. Do not rename them.

Each specialist gets its own SOUL.md identity file at ~/.hermes/profiles/<profile>/SOUL.md; you
keep your own identity in your long-term memory. I remain the owner with final authority.
Confirm you understand the plan, the four roles, and the profile↔name mapping.
```

## Prompt 5

### Prompt 5 — Create the Three Specialists

```
Create the three SPECIALISTS as persistent Hermes profiles — profile names dev, research,
assistant. For each one, do three things in order: (1) create the profile with
`hermes profile create <profile> --clone`, which makes ~/.hermes/profiles/<profile>/;
(2) write its EXACT identity into that profile's SOUL.md; (3) verify the agent responds with
the right identity before moving to the next. Do NOT create them as transient helpers. (Each
identity below says "the owner" — write my real name in its place.)

IMPORTANT — do NOT create a profile for JARVIS. You ARE JARVIS. Only the three specialists get
profiles.

— DEV (profile: dev) —
Your name is DEV. You are the engineer of the owner's crew. You build and maintain the
mission-control dashboard, its server, and every tool the crew uses. You write clean,
well-commented, production-quality code — Python standard library and plain HTML/CSS/JS — you
test what you ship with real commands, you back up a working file before you change it, and you
never leave the system broken. You verify with evidence, never with confidence: when you say
something works, you have just watched it work and you show the proof. You work in two places
and nowhere else: your OWN projects folder for anything personal, and the shared dashboard
project at ~/jarvis-mission-control, which is yours to build and maintain. Those are both
yours. You never edit the crew's own state under ~/.hermes — that is the one hard boundary.
You do not research (RESEARCH), and you do not touch the owner's mail or calendar (ASSISTANT).

— RESEARCH (profile: research) —
Your name is RESEARCH. You are the intelligence of the owner's crew. You find things out — with
live sources, not from memory — you verify claims before repeating them, you cite where a fact
came from, and when a source is thin or missing you say exactly that instead of padding around
it. You deliver findings as tight, structured briefs: what is known, what is uncertain, what to
do about it. You never invent a number, a name, or a citation; a confident wrong answer is the
one thing the owner cannot afford from you. You do not build (DEV), and you do not touch the
owner's mail or calendar (ASSISTANT).

— ASSISTANT (profile: assistant) —
Your name is ASSISTANT. You run the owner's day: mail, calendar, and the connected apps. You
read, summarise, prioritise, and draft — and you NEVER send, delete, or commit to anything
without the owner's explicit yes, every single time, no exceptions for small things. You know
who matters to the owner and you surface what needs an answer before it becomes urgent. You are
discreet: what you read in the owner's mail stays between you and the owner, and it never goes
into a log, a summary for another agent, or an external service. You do not build (DEV) and you
do not research the open web (RESEARCH).

After creating all three profiles (dev, research, assistant), ask each one "Who are you?",
confirm it replies with the right identity, and report each profile's path + SOUL.md
confirmation + the verified reply. That's four agents total — you plus the three.
```

## Prompt 6

### Prompt 6 — Memory, Workspaces & Team Awareness

```
For each of the four agents, set up:

DEDICATED MEMORY — each agent's memory stores only what's relevant to its role.
UNIQUE IDENTITY — name, role, personality never change across sessions.
ISOLATED WORKSPACE — separate files, outputs, and session history per agent; nobody edits
another agent's files. DEV additionally owns the shared dashboard project at
~/jarvis-mission-control: that folder is not a private workspace, it is the product, and DEV
builds and maintains it there. Isolation is about not treading on each other, not about
refusing to work on the thing we are building.
ROLE BOUNDARIES — each agent politely declines out-of-scope work in ONE line and names the
right teammate. Example: ask ASSISTANT for code and it replies "That's DEV's department."

Then give every agent this shared team awareness and make sure each one saves it:

The owner — may directly instruct any agent at any time. Final say on everything.
JARVIS (default profile) — chief of staff. Routes, verifies, reports. Never does a
specialist's work when one of them owns it.
DEV (profile dev) — engineering: the dashboard, the server, the tools.
RESEARCH (profile research) — intelligence: live sources, verified findings.
ASSISTANT (profile assistant) — comms and calendar: mail, diary, connected apps. Reads freely,
never acts without the owner's yes.

Also pass each specialist the parts of my brief they need (from your memory): all of them get
my name, what I do, and my hours; ASSISTANT additionally gets who matters to me and what may
interrupt me; DEV gets how I like things built; RESEARCH gets what I want watched.

IMPORTANT — work with what you HAVE. If any of those details are not in your memory (maybe I
skipped or rushed the interview), do NOT stop to ask me for them now: write "not provided yet"
as an open question in that agent's notes and keep going. I can fill gaps any time later; the
build never stalls on missing biography.

Confirm once all four agents are updated, then run a "Who are you?" test on each and paste
their one-line answers.
```

## Prompt 7

### Prompt 7 — Brief JARVIS, and Build the Channels

```
Here's the whole picture. Read it, tell it back to me in your own words, then do the part that
is yours — all in this one reply.

WHERE YOU ALREADY STAND
The Telegram bot IS you. When I say the bot is an admin in this group, I mean YOU are. You are
not arranging this for some other program.

Right now, before you do anything:
  - this group exists, with Topics enabled, and you are answering me inside it
  - YOU are an admin here, holding the "Manage Topics" right — that is what lets you create
    channels in this group
  - the topic we are talking in is the group's General topic, which I renamed to JARVIS. It is
    your channel, and it is where I will paste everything for the rest of this build
  - the group is authorised in your gateway config, which is why you can answer me here at all
  - no other topics exist yet

THE GOAL
Every agent gets its own channel in this group: DEV, RESEARCH and ASSISTANT beside your JARVIS.
A message in the DEV topic should be answered by the REAL DEV — its own memory, tools and
identity — not by you wearing a costume.

THE CATCH
Telegram gives one bot a single identity, and Hermes has no built-in setting for "messages in
this topic run as this agent." Out of the box every topic in this group is answered by you, the
default agent. Relaying everything through you works, but it is a four-hop detour that turns you
into a bottleneck and mixes every agent's context together.

HOW WE SOLVE IT
We route by channel. A small plugin reads each incoming message's topic (its thread id) and runs
that turn as the matching profile DIRECTLY, and the reply goes straight back to that topic. To
make that possible we switch Hermes into multi-profile mode. That comes in a later card.

WHAT I NEED FROM YOU NOW
1. Tell the plan back to me in your own words, so I know we agree.

2. Check you can actually make topics, BEFORE you try: ask Telegram about YOUR OWN membership in
   this group and confirm you are an administrator and that can_manage_topics is true for you.
   If either is false, STOP and tell me exactly what to switch on in the group's admin settings —
   do not attempt to create topics and hand me a confusing permission error.

3. Create THREE topics in this group, one at a time, with exactly these names:
     DEV, RESEARCH, ASSISTANT
   Telegram returns a message_thread_id for each as you create it. Keep all three.

   Do NOT create a topic called JARVIS. That channel already exists — it is this one, the
   renamed General topic. General cannot be created or deleted by anyone, only renamed, so a
   JARVIS topic you create would be a second, duplicate channel, and the one I am typing in
   would be the other one.

4. Note this group's chat id as well — you have it from the message I am sending you right now.

5. Save the chat id and the three topic name → thread id pairs to your long-term memory, and
   show me a small table of what you created. I am not writing these numbers down; you are the
   one who will use them.

Do not build any routing yet. The next card does that.
```

## Prompt 7b

### Prompt 8 — Isolate the Specialists

```
We're about to route each topic in this group to a real specialist PROFILE. For that to work,
each specialist must NOT connect to Telegram itself — you stay the only one holding the Telegram
connection.

For each of dev, research, and assistant:
1. Confirm the profile exists at ~/.hermes/profiles/<name>/ with its own SOUL.md.
2. Open ~/.hermes/profiles/<name>/config.yaml and REMOVE any `platforms:` block, especially any
   telegram token. If there is no platforms block, good — leave the file alone.
3. Check ~/.hermes/profiles/<name>/.env too. If it contains a TELEGRAM_BOT_TOKEN line, back the
   file up and remove that line.
4. They keep their own model, tools and memory. Profiles are isolated and do not share live
   changes.

Confirm each of the three exists, has its identity file, and has no telegram configuration
anywhere.
```

## Prompt 7c

### Prompt 9 — Wire the Lanes From What You Captured

```
Wire the routing, using this group's chat id and the three thread ids YOU captured and saved —
do not ask me for them.

STEP 1 — THE PLUGIN. Create ~/.hermes/plugins/telegram_topic_profiles/ with three files. Do NOT
patch anything under ~/.hermes/hermes-agent/ — that is overwritten on every Hermes update.

FILE 1 — plugin.yaml:
  name: telegram_topic_profiles
  version: 1.0.0
  description: "Route Telegram forum topics to Hermes profiles."
  author: the owner
  kind: standalone

FILE 2 — topics.json, filled in with the ids you captured. The JARVIS topic is deliberately
absent: it is this group's General topic, whose messages arrive with no thread id or with thread
id 1, and anything not listed here falls through to the default profile — which is you. That is
how you keep your own channel without needing a rule of your own:
  {
    "chat_id": "<this group's chat id>",
    "topics": {
      "<DEV thread id>": "dev",
      "<RESEARCH thread id>": "research",
      "<ASSISTANT thread id>": "assistant"
    }
  }

FILE 3 — __init__.py, exactly this:
  """Route Telegram forum topics to Hermes profiles (out-of-tree, update-safe)."""
  from __future__ import annotations
  import json, logging
  from pathlib import Path

  logger = logging.getLogger(__name__)
  _MAP_PATH = Path(__file__).with_name("topics.json")

  def _load_map():
      try:
          data = json.loads(_MAP_PATH.read_text())
          chat_id = str(data.get("chat_id", "")).strip()
          topics = {str(k): str(v) for k, v in (data.get("topics") or {}).items()}
          return chat_id, topics
      except FileNotFoundError:
          return "", {}
      except Exception as e:
          logger.warning("telegram_topic_profiles: bad topics.json: %s", e)
          return "", {}

  def _route(**kwargs):
      event = kwargs.get("event")
      source = getattr(event, "source", None)
      if source is None:
          return None
      pval = getattr(getattr(source, "platform", None), "value", getattr(source, "platform", None))
      if str(pval).lower() != "telegram":
          return None
      thread_id = getattr(source, "thread_id", None)
      if not thread_id or getattr(source, "profile", None):
          return None
      map_chat, topics = _load_map()
      chat_id = getattr(source, "chat_id", None)
      if map_chat and chat_id and str(chat_id) != map_chat:
          return None
      profile = topics.get(str(thread_id))
      if profile:
          source.profile = profile
          logger.info("telegram_topic_profiles: thread %s -> %s", thread_id, profile)
      return None

  def register(ctx) -> None:
      ctx.register_hook("pre_gateway_dispatch", _route)

STEP 2 — SHOW ME topics.json before you go on, so I can see the three numbers you captured
mapped to the right profiles.

STEP 3 — SWITCH IT ON. Three commands. Run what you are allowed to run; for anything blocked,
give me the exact command and wait for my "done":
  hermes plugins enable telegram_topic_profiles
  hermes config set multiplex_profiles true
  hermes gateway restart

Restarting the gateway briefly disconnects you from this group — that is expected, and you come
back on your own.

If the gateway will not start, the usual cause is a specialist profile still carrying a
platforms/telegram block or a leftover bot token — clear it and restart again.

Confirm the plugin is enabled, multi-profile mode is true, and the gateway came back up. Do not
claim the routing works — the next card tests it.
```

## Prompt 7d

### Prompt 10 — The First Words in Every Channel

```
Who are you, and which profile are you running as? One short line.
```

## Prompt 8e

### Prompt 11 — The Project Folder & the Activity Log

```
Create the project folder and the crew's activity log. Everything we build lives in
~/jarvis-mission-control/ (never inside ~/.hermes). Python 3 and bash only, nothing installed.

1. Create ~/jarvis-mission-control/.

2. Build ~/jarvis-mission-control/log-task.sh — the ONE way any agent records work:

     log-task.sh <agent> "<what you did>" <status> [model]

   - agent: accept EITHER form — JARVIS | DEV | RESEARCH | ASSISTANT, or the profile names
     default | dev | research | assistant — but always STORE the uppercase display name.
     Map default -> JARVIS, dev -> DEV, research -> RESEARCH, assistant -> ASSISTANT, and
     match case-insensitively. This matters more than it looks: the dashboard groups every
     figure by agent_name, so a row stored as "dev" is a fifth agent nobody can see, and that
     agent's counters silently stay at zero. Reject anything not in the list with a usage
     error that names the four valid values.
   - status: completed | failed | running — reject anything else with a clear usage error.
   - model: optional; the model that actually did the work. Store NULL when it is not given,
     not an empty string.
   - It writes to ~/jarvis-mission-control/agent-logs.db (overridable via an AGENT_LOG_DB
     environment variable).

     RESOLVE THAT PATH FROM THE SCRIPT'S OWN LOCATION, and prove it. Every agent calls this
     from its own working directory, so anything relative to the cwd scatters a separate
     database wherever each caller happened to be standing — the dashboard reads one of them
     and shows nothing, with no error to explain it. One specific trap, because it looks
     correct and is not: if you implement the body as Python fed to `python3 -` from a heredoc,
     `__file__` is `<stdin>` and `Path(__file__).resolve().parent` silently evaluates to the
     CURRENT DIRECTORY, not the script's. Either capture the bash `$0`/BASH_SOURCE directory
     and pass it in, or write the Python as its own file.

     PROVE IT BEFORE MOVING ON: run the script from two different directories — `cd /tmp` and
     `cd ~` — then show me that both rows landed in the SAME database and that no stray
     agent-logs.db exists anywhere else (`find ~ /tmp -name agent-logs.db`).

     SQLite, creating this table IF IT IS MISSING — never dropping it:
       agent_logs(id INTEGER PRIMARY KEY AUTOINCREMENT,
                  agent_name TEXT NOT NULL, task_description TEXT NOT NULL,
                  model_used TEXT, status TEXT NOT NULL, created_at TEXT NOT NULL)
     plus an index on created_at DESC — the dashboard always reads newest-first.
   - task_description is capped at 500 characters.
   - created_at is exactly what Python's `datetime.now(timezone.utc).isoformat()` produces —
     e.g. 2026-08-02T10:35:50.391204+00:00. Timezone-aware, with the +00:00 offset, not a "Z"
     and not a naive local time. The dashboard sorts and buckets on this string, so a different
     shape puts every entry in the wrong hour of the heat map, or drops it from the feed
     entirely, with no error anywhere.
   - Give it a `#!/usr/bin/env bash` shebang and `chmod +x` it, and confirm it runs as
     ~/jarvis-mission-control/log-task.sh with no interpreter in front of it — that is exactly
     how the agents are about to be told to call it.
   - Open the database with a 5-second timeout so two agents logging at once queue politely
     instead of crashing on a lock.
   - On success it prints one line: logged: <agent> · <status> · <N> entries total — so the
     agent that ran it can SEE its entry landed.
   - It writes ONLY to the project folder. Nothing under ~/.hermes is ever touched by this
     script — the crew's own state is not ours to write.

3. Prove it, with real runs, not by reading the script back:
   - Log one entry as each status (completed, running, failed) and show me the printed line
     each time.
   - Then query the table directly and show me the rows with their timestamps.
   - Run the script with a bad status and show me it refuses with the usage line.
   - Run it with no arguments and show me the same.

Report the folder path, the script path, and the row count when you are done.
```

## Prompt 8f

### Prompt 12 — Agents Log Everything They Do

```
JARVIS: save the following as a durable operating rule in YOUR OWN long-term memory first, then
distribute it to DEV, RESEARCH and ASSISTANT — making sure each one saves it to their own
long-term memory too:

---
Store this in your long-term memory as a durable operating rule:

After completing any piece of work — a task, a build step, a piece of research, a report —
log it into the crew activity log by running:
  ~/jarvis-mission-control/log-task.sh <YOUR NAME> "<brief description of what you did>" <status> <model>

Rules:
- <YOUR NAME> is your own agent name: JARVIS, DEV, RESEARCH, or ASSISTANT.
- <status> is completed, failed, or running. Log failures exactly as readily as successes —
  a log with no failures in it is a log nobody can trust.
- <model> is the exact model you are running on.
- Keep the description under 140 characters, concrete, in plain words.
- Log every substantial response. Never mention the logging unless the owner asks about it.
---

Have every agent confirm the rule is saved, then have each of the four (you included) run one
smoke-test log right now. Finish by showing me the last five rows of agent_logs — agent_name,
status, model_used, created_at — so I can see four different names in the table.
```

## Prompt 8g

### Prompt 13 — Claude Code as Your Builder (optional)

```
You are running on the server that hosts my Hermes agent setup. My crew is already raised and
working; everything from here is engineering, and YOU are doing it. Before touching anything,
get your bearings — explore this machine properly and report back.

WHO YOU ARE, AND WHO YOU ARE NOT — read this twice, it shapes every card that follows

You are a BUILD TOOL. You write the dashboard and the infrastructure around it. That is all.

You are NOT joining the crew, and you are NOT replacing DEV. DEV is a real Hermes agent with
its own profile, its own memory and its own Telegram topic, and it stays exactly where it is.
When the finished dashboard shows four agents and I click DEV, the answer must come from the
Hermes dev profile — never from you. The same goes for JARVIS, RESEARCH and ASSISTANT.

So, concretely, for every card from here on:
  - When a card says "the agent", "DEV", "each agent", or "run a real turn", it always means a
    Hermes profile. Wire the dashboard to those profiles. Never wire it to yourself, never
    stand up a service that answers as an agent, never put your own responses behind an
    endpoint the page calls.
  - You never speak as DEV, never edit DEV's SOUL.md or memory, and never post in its topic.
  - Cards are written for DEV as the builder. Read them as instructions to YOU as the builder,
    and leave every reference to what the AGENTS do exactly as it is — those parts describe the
    running system, not your job.

The test that settles any doubt: when this build is finished, I close you, and the dashboard
keeps working exactly as before — the crew still answers, the voice still speaks, every view
still fills. If anything would break when you go away, you built the wrong thing.

WHAT TO LOOK AT

1. Hermes itself, at ~/.hermes — learn the layout: config.yaml, .env (do NOT print any secret
   values from it, ever), profiles/ (each subfolder is a persistent agent with its own SOUL.md,
   memory and workspace), state.db, plugins/, logs/, kanban.db.

2. My crew. There are four agents: the default profile is JARVIS, my chief of staff, plus three
   specialist profiles — dev (DEV, engineering), research (RESEARCH, intelligence) and
   assistant (ASSISTANT, mail and calendar). Confirm those three profiles exist and read their
   SOUL.md files so you know who they are and what each one refuses to do — including DEV,
   whose identity you are building FOR, not replacing.

3. The Telegram routing. Each agent has its own topic in one Telegram group, routed by an
   out-of-tree plugin at ~/.hermes/plugins/telegram_topic_profiles/ that maps a topic's thread
   id to a profile, with multi-profile mode switched on. Read that plugin so you understand how
   a message reaches an agent. You will not change it, but later cards work around it.

4. What already exists in ~/jarvis-mission-control — this is the project folder and it is
   nearly empty on purpose:
     - log-task.sh and agent-logs.db — the crew's activity log. Every agent writes one row per
       task it completes: who, what, status, model, when. Read the schema and look at the rows
       that are already in there. This is the source of the dashboard's real numbers, and it
       has been filling up since before you arrived.
   There is no server and no dashboard yet. You build both, starting with the very next card.

5. Hermes may be new to you. Read the official documentation now and keep it as your reference
   for the whole build: https://hermes-agent.nousresearch.com/docs
   Whenever a later card raises a Hermes question — config format, profile layout, CLI
   behaviour, how to invoke an agent non-interactively, plugin hooks — consult those docs
   first. Never guess about Hermes.

6. The box itself: OS, Python version, Node availability, free disk. A 353 MB model download
   and a headless browser both appear in later cards.

WHERE WE ARE GOING, so you understand the shape of what you are joining
Your first card has you SURVEY the data this machine already holds — read-only, no code — so
that everything you build afterwards is wired to real data instead of invented data. Then you
build a small read-only server, and an upload page through which I hand you a finished
dashboard DESIGN as one self-contained HTML file. That design becomes the dashboard, and from
then on you wire it view by view to what is underneath: the crew's activity, their sessions and
token counts, their scheduled jobs, their documents, their task board, and which model each one
thinks with. After that comes a voice layer with a local speech engine, spoken greetings,
push-to-talk, and finally a responsive pass and a private-network step. Every one of those
arrives as its own card. Do not build ahead of the card you have been given.

STANDING RULES FOR THE WHOLE BUILD — save these and hold to them

- THE DESIGN IS NOT YOURS TO CHANGE. Once the design file is installed you WIRE it to data,
  view by view. You never restyle it, never "improve" spacing, colour, type or components. An
  untouched copy stays served at /template as the reference: after ANY change that touches the
  appearance, open /template beside the view you changed and fix any drift before you report
  done. A view that works but no longer matches the template is not finished.

- READ-ONLY AGAINST THE CREW. Hermes's own databases are opened read-only and never written to.
  Never impersonate an agent, never edit any profile's SOUL.md, memory or workspace, never
  print a secret from .env or any key file. The crew's state is not yours.

- THE DASHBOARD TALKS TO THE CREW, NOT TO YOU. Every place the finished product runs an agent
  turn — the messenger view, the voice, the greetings, any button that asks an agent something
  — must invoke the real Hermes profile. You are not a runtime component of this product and
  nothing may depend on you being present.

- EVERYTHING YOU BUILD LIVES IN ~/jarvis-mission-control, never inside ~/.hermes. That folder
  is the crew's private state; this one is our shared workshop.

- SECURITY, on every card, forever. The dashboard binds to 127.0.0.1 only. Never 0.0.0.0, no
  open ports, no reverse proxy. I reach it through an SSH tunnel while we build, and a private
  network step at the end. This dashboard can drive my agents and read my private data.

- BACK UP BEFORE YOU EDIT. A backup script arrives in an early card; from that point on, every
  edit starts with a snapshot. Before it exists, copy a file aside yourself before changing it.

- EVIDENCE, NOT CONFIDENCE. Verify each step with real commands and show me the output. If
  something failed, say so plainly. If a number is not available from real data, return null
  and tell me — never invent a plausible-looking figure.

- IF A COMMAND IS BLOCKED — by permissions or an approval prompt — do not retry into the wall
  and do not invent a workaround. Stop, give me the ONE exact command to run myself, wait for
  my "done", then verify the result and carry on.

WHEN YOU ARE DONE EXPLORING
Give me a short map of the setup as you understand it: the four agents and their profiles, how
Telegram routing reaches them, what is in the project folder already, and anything on this
machine that looks like it will bite us later.

Then, in one line each, tell me back: what your job is, and what happens when I click DEV in
the finished dashboard. If those two answers are right, we are aligned and you can wait for my
next card. Build nothing yet.
```

## Prompt 9

### Prompt 14 — Explore the Data Sources, Read Only

```
DEV: before you build anything, go and find out what data this machine already has about the
crew. Read only — do not modify, move or delete anything you find.

Look for, at minimum:
- The main Hermes state database at ~/.hermes/state.db — sessions, messages, token usage.
- Each specialist's own state database under ~/.hermes/profiles/<profile>/.
- The crew's internal task board (a kanban database in the Hermes home).
- The gateway's logs and status — whatever tells us it is alive and connected.
- OUR OWN activity log at ~/jarvis-mission-control/agent-logs.db — the crew has been writing
  into it since the logging rule was installed, so it already has real rows. This one is project-local and ours,
  but for this survey treat it read-only like everything else.

For each one, tell me: where it is, what tables or keys it holds, what the timestamps look like
(epoch seconds as integers, epoch seconds as floats, and ISO-8601 strings — they are NOT
consistent, and the dashboard will have to
normalise them), and one real example row so I can see the shape of the truth.

Then tell me, in plain English, what a dashboard could truthfully show from this and what it
could not. I would rather find out now that a number is not available than see you invent it
later. If a figure I'd expect — say, cost in dollars — is not derivable from what's on disk,
name it now.

Do not write any code yet.
```

## Prompt 10

### Prompt 15 — Build the Read-Only Data Layer

```
DEV: build server.py — the data layer for the dashboard. Python standard library only, no pip
installs, no frameworks.

Build it in ~/jarvis-mission-control — the project folder that already exists, with the crew's
activity log (agent-logs.db) inside it. Every file you make for this dashboard lives in it, and later prompts refer
to it as "the project folder".

Serve on port 8899, and keep that port for the rest of the tutorial — later prompts, the upload
page and the Tailscale card all refer to it.

Start with GET /api/state — one JSON snapshot of everything the page shows.

THE PAYLOAD SHAPE IS FIXED. Use exactly these key names. The design I am about to give you is
already written against them, and it reads them by name — a field spelled differently is a blank
panel with nothing in the console to explain it. This is a contract, not a suggestion:

  {
    "crew": [                       one object per agent, in crew order
      { "key":       "default" | "dev" | "research" | "assistant",
        "name":      "JARVIS",      display name, uppercase
        "code":      "J-00",        J-00, J-01, J-02, J-03 in crew order
        "initials":  "JV",          two letters
        "role":      "Chief of staff",
        "tagline":   "one line on what this agent is for",
        "state":     "active" | "standby" | "idle",
        "model":     "the model it actually runs on",
        "channel":   "telegram" | "cli",
        "telegram":  true | false,  does it have a live Telegram thread
        "reachable": true | false,  does its own session store exist yet
        "share":     0-100,         this agent's share of the LOGGED TASKS, not of
                                    messages or tokens. Compute it from "tasks" below and
                                    nothing else, so every agent's share sums to 100. Say so
                                    wherever you label it: an agent that sent 163 messages
                                    but logged 3 tasks reads as quiet, and that surprises
                                    anyone who thinks the bar means overall activity.
        "sessions":  0, "messages": 0, "tokens": 0,
        "tasks":     0,             rows this agent wrote to the activity log
        "failed":    0,             of those, how many have status failed
        "events":    0,             its activity in the last 80 hours
        "hourly":    [ 13 integers ],  this agent's own hourly counts, same 13 buckets as
                                       the top-level "hourly" below - the per-agent sparkline
                                       reads it and draws nothing without it
        "mix":       { "completed": 0, "running": 0, "failed": 0 } }
    ],
    "ops": [                        the live feed, newest first
      { "t": "17:04:11", "agent": "DEV", "op": "what it did", "state": "ok" | "failed",
        "model": "..." } ],
    "sessions": { "totals": { "sessions": 0, "messages": 0, "tokens": 0, "tool_calls": 0,
                              "input": 0, "output": 0, "cache_read": 0, "reasoning": 0,
                              "cost": 0 },
                  "recent": [ { "agent": "dev", "id": "...", "started_at": "...",
                                "title": "what the session was about", "source": "cli"|"telegram",
                                "model": "...", "messages": 0, "tokens": 0 } ] },
    "heatmap": { "rows": [ { "key": "dev", "name": "DEV", "counts": [24 integers],
                             "total": 0 } ],
                 "max": 0, "total_events": 0, "peak_hour": 0 | null },
    "hourly": [ 13 integers ],   "hourly_peak": 0,
    "box": { "cpu_pct": 0, "mem_pct": 0, "disk_pct": 0, "load1": 0.0, "hostname": "..." },
    "gateway": { "state": "running" | "stopped", "pid": 0, "platforms": [ "..." ] },
    "events": [ "one line per notable thing, newest first" ],
    "alerts": [ { "level": "high" | "info", "text": "..." } ],
    "capabilities": {               mail and diary. The design READS this by name, so ship the
                                    key even before Prompt 25 connects anything - an absent key
                                    is an empty panel with nothing in the console to explain it.
      "mail":     { "connected": false, "count": 0, "next": null, "checked_at": null,
                    "stale": false, "reason": "why it is not connected yet", "items": [] },
      "calendar": { "connected": false, "count": 0, "next": null, "checked_at": null,
                    "stale": false, "reason": "...", "items": [] } },
    "version": "v1.0"
  }

Two of these are easy to get subtly wrong, and both fail silently:
- `ops` uses "t" for the time, NOT "at". A renderer reading .t against a payload with .at shows
  a row with a blank timestamp and no error anywhere.
- The heat map is "heatmap", an OBJECT with rows/max/total_events/peak_hour — not a bare array,
  and not "heat".

Where each figure comes from:
- crew identity (key, name, code, initials, role, tagline, channel) is fixed data you define
  once in the server, in crew order — it is not read from anywhere.
- sessions, messages, tokens and tool_calls come from the Hermes state databases; last-seen
  times there are in inconsistent formats, so normalise them to one thing HERE, in the server,
  so the page never has to guess.
- tasks, failed, mix, events, the heatmap and ops all come from the ACTIVITY LOG at
  ~/jarvis-mission-control/agent-logs.db, which every agent already writes a row to after each
  task. MATCH ROWS TO AGENTS BY agent_name AGAINST THE DISPLAY NAME — the log stores JARVIS,
  DEV, RESEARCH, ASSISTANT, never the profile key. Build one map from display name to key and
  use it everywhere; a row whose name matches nothing must be counted somewhere visible rather
  than silently dropped, or a typo in one agent's logging costs you a whole agent's figures
  with nothing on screen to show for it.
- box is this machine, read live.
- gateway comes from Hermes's own gateway_state.json, AND from checking that the pid in it is
  actually alive. Do both. That file is only rewritten on events, so a perfectly healthy gateway
  routinely shows an hour-old timestamp — judging it by age gives false alarms all day. But the
  file will also happily keep saying "running" forever after the process has died, so the field
  alone is not proof of life either. Report the state from the file and whether the process
  exists; never hard-code "running".

Hard rules:
- READ-ONLY against Hermes. Open every Hermes database in read-only mode (SQLite's mode=ro URI)
  and never write to them. The crew's own state is not yours to edit.
- Bind to 127.0.0.1 only. Never 0.0.0.0. This dashboard can drive my agents — and later my
  house — so it must never be on a public port. We put it behind Tailscale near the end.
- Every number comes from a real query. If something is not available, return null and say so —
  do not fill it with a plausible-looking figure, ever. This rule holds for the entire build.
- Pick ONE aggregation source per figure and stick to it. The state databases hold overlapping
  aggregates (session rows AND per-model usage rows both carry token totals) — summing across
  both double-counts, and the dashboard shows a number twice as big as the truth with no error
  anywhere. Name your chosen source in a comment where each figure is computed.
- A missing or locked database must not crash the endpoint — Hermes writes to these files while
  we read them. Degrade to null for what you can't read, and keep serving the rest.
- Close every database connection you open. Prove it on the RUNNING server, not in a toy
  script: with the server up, note its process id, request /api/state 200 times in a loop,
  and show me the server process's open-file count before and after
  (ls /proc/<server pid>/fd | wc -l). If the count grows with the requests, connections are
  leaking — fix it before moving on, because a leak here kills the dashboard quietly on
  day three.

INSTALL IT AS A SERVICE, do not just leave it running in this shell. A dashboard that dies
when a terminal closes is one you cannot trust, and you WILL close this terminal. Same rule as
anything else we install here:
- If you can run sudo without being prompted for a password, install a system unit in the usual
  place and enable it.
- If you CANNOT — you are not root and sudo wants a password — do NOT stop and do not ask me to
  type one. Install it as a USER service under ~/.config/systemd/user/, manage it with
  `systemctl --user`, and run `loginctl enable-linger $USER` so it survives me logging out.
Either way: restart on failure, start on boot, and tell me which of the two you used AND WHICH
USER IT RUNS AS. That second part matters more than it sounds: a system unit defaults to root,
and later cards read a key and a project folder out of MY home directory. If the service runs as
root and the files are mine, it finds neither, and the failure looks like a missing key rather
than a wrong user. If you install it system-wide, set User= to me.

Then restart the machine's service (not the shell process) and show me it came back by itself.

Run it, show me the raw JSON from /api/state, and walk me through where each number came from —
table by table.

Then CHECK THE CONTRACT KEY BY KEY before you tell me it works. Every key listed above has to be
present, including the ones that are empty on a fresh machine — "capabilities" before any mail is
connected, "hourly" on every agent before there is much history. A missing key does not raise: the
panel that reads it renders blank and the console stays clean, so this is the one failure you
cannot find by looking at the page. List each top-level key and each crew field with present or
MISSING beside it, and fix every MISSING before moving on.

Then print the exact SSH tunnel command I run on MY computer to see it — with my real username
and this machine's real address filled in, in the form:
  ssh -N -L 8899:127.0.0.1:8899 <user>@<server>
and remind me: with the tunnel open, the dashboard lives at http://localhost:8899 in my browser,
and it will be a 404 at the main page until the design arrives in two prompts. That is expected.

Tell me plainly, and repeat it whenever I seem lost about "seeing" the dashboard: that tunnel
window has to STAY OPEN for the entire build — every later step where I look at a view uses it.
If I ever say I can't see the dashboard, the first question is whether that window is still
open, and the fix is running the same command again — never anything more complicated.
```

## Prompt 11

### Prompt 16 — Build the Web Upload Page & Hand Over the Design

```
DEV: set up a WEB-BASED upload page so I can hand you the prebuilt template — the single
self-contained HTML file I downloaded from the Tutorial tab. Do NOT ask me to run curl or scp,
do NOT ask me to paste file contents into a prompt, and do NOT try to recreate the template
yourself — it exists and I am about to give it to you.

In server.py add:
  GET /upload      — a small self-contained upload page. No external libraries, no CDN — inline
                     CSS and JS — but make it genuinely pleasant, not a bare form:
                     · a large DRAG-AND-DROP zone (with a dragover highlight) that also opens a
                       file picker on click — accept .html plus images
                       (.png .jpg .jpeg .webp .svg), multiple files allowed
                     · each file uploads via FileReader.readAsDataURL → POST JSON
                       {name, data: <data-URL>} to /api/upload, sequentially, with a per-file
                       row showing name, size, and live status
                       (uploading… / ✓ saved / ✗ failed with the reason)
                     · a CHECKLIST of the one expected file — jarvis-dashboard-template.html —
                       that ticks green when it lands, with a clear "Template received — return
                       to DEV's topic and continue" banner
                     · files with other names still upload fine (the checklist is guidance, not
                       a gate); a duplicate upload simply overwrites
  POST /api/upload — JSON {name, data: <base64 data-URL>} (this exact encoding): save into the
                     project folder, keeping the original filename. Allow only .html and those
                     image types. BLOCK path traversal — reject any name containing "/" or "..".
                     Return JSON { ok, filename, path, size }.
                     One trap that makes this route LOOK broken while working: the template is
                     megabytes, so read the request body to the full Content-Length before
                     responding, and send the response with its own Content-Length set. A
                     handler that saves the file and then closes the socket early makes every
                     upload report failure in the browser while the file quietly landed —
                     the worst kind of bug, because both sides are half right.

Restart the server so the routes are live, then remind me: with my SSH tunnel from the previous
card open, the upload page is http://localhost:8899/upload — never a public URL.

Then STOP and wait — I'll drag jarvis-dashboard-template.html in and come back when the page
shows it ticked. Do not build anything visual yet.
```

## Prompt 12

### Prompt 17 — The Template Becomes the Dashboard

```
DEV: I've uploaded the template — jarvis-dashboard-template.html is in the project folder. Turn
it into the dashboard and lock it in as the design source of truth.

1. Copy it to index.html — the exact file the server returns at GET /. Keep the untouched
   original reachable at GET /template, and print index.html's absolute path.

2. DESIGN SOURCE OF TRUTH — from here on, the template is the ONE design authority. You WIRE
   its data; you never redesign it. Do not change its layout, spacing, colours, glow, fonts,
   corner radii, components or copy. If a later card has you add anything visual, first open
   /template, match its exact visual language, then put your version side by side with it and
   fix any drift until they are identical. The design never changes — that is the whole point
   of starting from a finished design.

   SAVE THIS AS A DURABLE RULE in your long-term memory, because it applies to every card from
   here to the end, not just this one:
     "After ANY change that touches the dashboard's appearance, and BEFORE reporting it done,
      open /template beside the view I changed and compare them. Anything that drifted —
      spacing, colour, weight, corner radius, type size, alignment — goes back to what the
      template does. I am wiring this design, not restyling it."
   A view that works but no longer matches the template is not finished, it is broken in a way
   that is hard to see and expensive to undo later.

3. CUT THE TEMPLATE'S NETWORK SHIM — do this FIRST, before anything else. The template has to
   open on its own with no server behind it, so near the top of its script it installs a shim:
   it replaces window.fetch AND window.EventSource so every /api/ call and the live event
   stream are answered from a baked-in DEMO_STATE instead of the network.

   The shim is fenced by two unmissable comment lines:
     /* ==================== TEMPLATE SHIM START ====================
     /* ==================== TEMPLATE SHIM END ==================== */
   In index.html — NOT in the /template copy, which keeps it — delete everything from the
   START line to the END line, both lines included, and NOTHING ELSE. Two things sit outside
   that fence and both must survive:
     · `window.__PORTRAITS__` in the <head>, which holds the four crew portraits as data
     · `window.__AV__` and the `AV()` function just above the START line, which read them
   The live dashboard keeps using both. Cut either one and every face on every view goes
   blank — and the page will not tell you why, because a missing image is not an error.

   Prove both halves: open the dashboard and show me that `window.__TEMPLATE__` is undefined
   in the browser console on / while still true on /template — AND that the four crew
   portraits still render on the Home view. A successful cut changes the data and changes
   nothing about the faces.

4. SPLIT IT INTO THREE FILES. The template arrives as one self-contained page because it has
   to survive being downloaded and opened on its own. That is the wrong shape to build on: every
   card from here edits this code, and surgical edits inside a one-and-a-third-megabyte HTML
   file go wrong in ways that are hard to see. In index.html ONLY — never in the /template copy,
   which stays exactly one untouched file — do this once:
     · move the contents of the single big <style> block into styles.css, and replace the block
       with <link rel="stylesheet" href="styles.css">
     · move the contents of the LAST and largest <script> block — the application itself, the
       one that begins after the shim you just removed — into script.js, and replace it with
       <script src="script.js"></script>
     · LEAVE THE SMALL INLINE SCRIPTS WHERE THEY ARE. The <head> block holding
       window.__PORTRAITS__, the two one-line setters that fill the boot faces and the globe
       portrait from it, and the docs-seed block, all run during parse and must stay in the
       markup. Only the big application script moves.
   Then serve the two new files from the server, as application/javascript and text/css.

   SEND CACHE HEADERS while you are there, or you will spend the rest of this build wondering
   why your edits did not appear. Python's built-in handler sends none at all, so the browser
   caches whatever it likes:
     · index.html, script.js, styles.css and any .md the page fetches -> Cache-Control: no-store
     · anything under /api/ -> Cache-Control: no-store; that data is live and a stale reading
       is a lie
     · images -> an ETag plus a short max-age, so a face does not re-download on every render
   Reload and confirm the page is byte-for-byte identical to before the split — same layout,
   same portraits, no console errors. If anything moved, you took too much.

   ONE MORE FILE: the page's <head> asks for /favicon.svg, which is the only same-origin asset
   the template does not carry inside itself. Make a small one in the project folder and serve
   it, so the tab has an icon and the console has no 404 in it from the first load onwards.

5. CLEAN AS YOU WIRE — the template ships with deliberately fake data: invented token counts,
   round session figures, sample messages, and a model that literally reads `your-model-here`.
   The crew NAMES are real, because they are the names I am building. As each view goes live in
   the cards that follow, DELETE that view's placeholder data. The tell is the numbers, not the
   names: a view still showing `your-model-here`, or a suspiciously round figure that does not
   match my real activity, is not done.

Confirm: / serves the template as index.html, /template serves the untouched original,
window.__TEMPLATE__ is undefined on / and true on /template, and all seven views load in a real
browser — Home · Agents · Comms · Schedule · Library · Docs · Control. The unwired views still
show the design's sample content; Home already shows real figures, because the server behind it
is live. Docs already has the full manual in it — it ships inside the template — and a card near
the end makes it true for THIS machine.
```

## Prompt 13

### Prompt 18 — Backup Protocol & Version Badge

```
DEV: set up the safety net before we wire anything.

1. BACKUP PROTOCOL — create ~/jarvis-mission-control/jarvis-backup.sh that takes a note:
   jarvis-backup.sh "<what is about to change>". It copies the core source files — server.py,
   index.html, styles.css and script.js, plus the untouched design reference the whole build
   compares itself against — into
   ~/jarvis-mission-control-backups/<timestamp>/ together with a MANIFEST listing what was
   saved, the note, and a restore.sh inside the snapshot that copies everything back. From now
   on, EVERY card that edits code starts with a backup — save that as a durable rule in your
   long-term memory, and never skip it, not even for a one-line change.

2. VERSION BADGE — ADD a small version label to the header, at its far end near the gateway
   status. The header does not have one yet — you are adding the one new element this design
   ever gets, so it must look factory-fitted: use the header's existing micro-label language
   (the small uppercase mono labels like the UPLINK one), compare side-by-side against
   /template, and fix any drift until it reads as original.

   Give the element a `data-version` attribute, because the page already writes the version
   into that exact selector on every state update. Do NOT hard-code the number into the markup:
   whatever you type there is overwritten within three seconds by whatever /api/state sends.
   Return it from the server instead, as a top-level "version" key, starting at "v0.1". Bump
   that number in the server on every wiring card from here on, so I can hard-refresh and
   instantly see whether the new version landed. The /template copy gets no badge — that stays
   the untouched reference.

3. THE WORKFLOW, every single time: back up, edit, bump. In that order.

Run the first backup now ("pre-wiring baseline"), show me the snapshot folder and its MANIFEST,
and show me the badge.
```

## Prompt 14

### Prompt 19 — Wire the Home View

```
DEV: back up, then wire the Home view to /api/state. When this card is done, nothing on this
page may be invented any more.

First, sanity-check that the template's network shim is actually gone: open the dashboard and
confirm window.__TEMPLATE__ is undefined. If it is still there, the page is being fed the
baked-in snapshot and nothing you wire will show — delete the fenced block between the
TEMPLATE SHIM START and TEMPLATE SHIM END comment lines in index.html first (and only
there — /template keeps its copy).

- The four crew portraits below the globe come from the real roster. The one currently selected
  is dimmed so I can see at a glance which agent I am on.
- The figures in the side panels — tokens, sessions, messages, tool calls, tasks — all come
  from the live snapshot.
- The activity chart shows real events per hour from the crew's own history, in MY time zone —
  remember the timestamp formats are inconsistent at the source; normalise in the server.
- The live feed panel lists what the crew has actually done, newest first, with the real agent
  name and a real time — read from the crew's ACTIVITY LOG (agent-logs.db in this project),
  which is why it already has entries on the day this view goes live. It updates while I
  watch — this page is the one that's always on.

BUILD THE LIVE STREAM, or nothing on this page will ever change after it first paints. The
design already subscribes to it, by this exact name and this exact event name:

  GET /events    a Server-Sent Events stream

  SERVE CONCURRENTLY, or this route takes the whole dashboard down with it. The handler below
  never returns — it loops for as long as the browser is connected. On Python's default
  single-threaded HTTPServer that means the FIRST page to open the dashboard blocks every other
  request forever: no /api/state, no script.js, no second tab, no phone. Use ThreadingHTTPServer
  (still standard library, one import) and give it daemon threads so the process can still exit.
  The symptom if you skip it is a dashboard that works perfectly for one browser and appears
  completely dead to every other one.

                 Content-Type: text/event-stream, Cache-Control: no-store,
                 Connection: keep-alive, and X-Accel-Buffering: no
                 Write "retry: 5000" once, then loop forever: send the SAME snapshot
                 /api/state returns, as `event: state` with the JSON on a `data:` line, then
                 flush and sleep 3 seconds.
                 When the browser goes away the write raises a broken pipe — catch it and
                 return quietly. That is a client closing a tab, not an error.

Do not skip this and rely on polling. The page calls /api/state exactly ONCE, on load, and then
hands over to this stream — its polling fallback only fires if the browser has no EventSource at
all. With no /events route the browser reconnects to a 404 every five seconds forever, and the
dashboard sits frozen on its first snapshot, showing real numbers that never move. There is
nothing in the console to tell you why.

Two things that WILL bite if you skip them, so handle them now:
- Long numbers. A real token count like 1,054,908 will not fit the space the design gives it,
  and will print straight over the figure beside it. Shorten large numbers for display (2.5K,
  1.05M) and keep the exact value in a tooltip. Nothing may ever overlap. This rule applies to
  every figure on every view from here on.
- A number that has not arrived yet renders as a dash — never "undefined", never "NaN", never a
  fake zero that looks like data.

Delete every placeholder figure and fake crew reference from this view as you go. Bump the
badge. Show me the view with real data, and tell me which number came from which query.
```

## Prompt 15

### Prompt 20 — Wire the Agents View

```
DEV: back up, then wire the Agents view.

- The roster shows the four real agents. Selecting one updates everything on the page.
- The dossier shows that agent's real figures — share of crew activity, sessions, messages,
  tokens, logged tasks, recent events — plus its model, its channel, and its most recent
  session time. Logged tasks and events come from the ACTIVITY LOG: they are the rows that
  agent wrote about itself, statuses included, failures and all.
- The activity heatmap is real: hour of day across, one row per agent, built from their own
  history, in my time zone.
- The live machine feed lists that agent's recent operations from the activity log. It scrolls
  inside its own box — it must never stretch the page.

The dossier is drawn by code the design already ships — your job is to feed it, not to build
it. Do not rewrite the rendering; wire the data behind it and fix only what does not line up.

Bump the badge. Then show me: select each of the four agents in turn and confirm every panel
follows — the figures, the model, the heat map and the feed all changing together, with nothing
left over from the agent before.

Before you tell me this is done: open /template beside the view you just changed and
compare them. Anything that drifted — spacing, colour, weight, corner radius, type size —
goes back. You are wiring this view, not restyling it.
```

## Prompt 16

### Prompt 21 — Wire the Comms View

```
DEV: back up, then wire the Comms view — three columns: the crew on the left, the conversation
in the middle, the selected agent's profile on the right.

SERVER FIRST — two new endpoints:
- GET /api/chat/history?agent=<profile> — that agent's real messages from its own state.
  The page reads these exact names, so use them:
    { "session": "<the session id it read>", "telegram": true|false,
      "messages": [ { "role": "user"|"agent", "text": "...", "ts": <epoch MILLISECONDS> } ] }
  Two details that both fail quietly:
  · The field is "ts", and it is epoch MILLISECONDS — the page hands it straight to the
    browser's Date constructor, which reads milliseconds. Return seconds and every message is
    dated January 1970. Hermes stores times in more than one format at the source, so
    normalise them here, in the server, to one thing.
  · Get the NAME wrong and every message loaded from history shows no time at all, while
    messages you send in the same session do — a split that looks like a rendering bug.
  Return only the conversation itself: roles "user" and "agent". Tool calls, system notices
  and the agent's own thinking are not messages and must not appear in the transcript.
- POST /api/chat/send — {agent, text} runs a REAL turn with that agent and returns the reply
  as PLAIN TEXT, not JSON. Every other route here answers with JSON; this one does not, because
  the page reads the response body straight into the chat bubble. Strip the CLI's own framing
  before returning it — a resumed session prints a banner, and a session summary follows the
  answer; neither belongs in a message bubble.
  This is the one place the dashboard causes an agent to act, so: never invoke it from page
  load, only ever from my explicit send.
  LOG THE TURN. After it completes, write one row to the activity log the same way an agent
  would — the agent's display name, the status, and a description prefixed "Comms: " so I can
  tell a dashboard turn from one the agent started itself. Skip this and the Comms view spends
  real tokens that never show up in the task counts, the feed or the heat map on the very same
  page.
  RESUME, do not start fresh. The send must continue that agent's NEWEST live session on this
  machine, so it answers with everything it already knows about me. A brand new session every
  time gives me an agent with amnesia that still costs full price, and the giveaway is subtle:
  the replies read fine, they are just strangely impersonal.

THEN THE PAGE:
- Busy state is PER AGENT, not one flag for the page. A slow turn with RESEARCH must not lock
  the send box for DEV — I should be able to set one agent working and carry on with another
  while it thinks. One global "sending…" flag is the lazy version and it makes four agents
  behave like one.
- The crew list, the conversation header and every message bubble use the agents' real
  portraits, not icons.
- The transcript loads that agent's real history. Sending appends my message immediately, shows
  a typing state, and renders the real reply when it lands. Sending also CLEARS the box.
- The conversation OPENS ON THE NEWEST MESSAGE. This sounds obvious and it is the single most
  common thing to get wrong: if you set the scroll while the view is still hidden, the element
  has no height yet and your scroll does nothing — the reader lands on message one of hundreds.
  Set it again once the view is actually visible.
- Timestamps come from the history payload. Check the field name the API actually returns
  against the one your renderer reads — if they differ, every message silently shows no time
  at all, and nobody notices until someone asks "when did it say that?"
- Search filters the transcript and highlights matches. Highlight the RAW text and escape each
  piece afterwards; if you escape first and then highlight, a search for a single letter will
  split an HTML entity and the reader sees raw markup in the middle of a sentence.
- The right column's activity donut shows each agent's real share of crew activity, with the
  legend below it and a thin, quiet ring — match /template exactly.

ONE MORE PLACE THE SAME ROUTE IS USED — the Agents view. Now that the send route exists, put an
"Open comms with <agent>" control on that view's dossier and have the card FLIP into a chat with
whoever is currently selected, rather than throwing me over to this view. Reading an agent's
numbers is exactly when I want to ask that same agent about them, and making me navigate away,
find them again in a second roster and lose my place is the friction that stops me asking at
all. It reuses THIS route — one chat implementation, not two. While the card is flipped, the
three-second state refresh must NOT re-render it, or it wipes what I am typing and throws away
my scroll position every three seconds.

Bump the badge.
```

## Prompt 17

### Prompt 22 — Wire Schedule and Library

```
DEV: back up, then wire the two remaining data views. Server first. The design already calls
these exact routes with these exact parameters, so build them with these names — a route that
works but is called something else leaves a button on screen that does nothing at all:

  GET  /api/cron
       -> { "jobs": [ { "id": "6fea7789d568",          short stable id, used by the actions
                        "name": "Morning brief",
                        "english": "daily at 08:00",   the schedule in words, for humans
                        "next_run_at": "ISO-8601 with an offset, in MY timezone",
                        "enabled": true,               false means paused
                        "deliver": "telegram" | "cli", where the result is sent
                        "last_status": "ok"|"error"|null,
                        "last_run_at": "ISO-8601 or null",
                        "last_error": "the message, or null",
                        "prompt": "the instruction the job runs" } ] }
       The page reads next_run_at and enabled by those exact names. "next" and "paused" are
       the obvious guesses and neither is read by anything.
  POST /api/cron/action?action=run|pause|resume|delete&id=<job id>
       -> { "ok": true } or { "ok": false, "error": "why" }
  GET  /api/content
       -> { "total": 3,                                every document across every shelf
            "shelves": [ { "agent": "dev", "count": 1,
                           "docs": [ { "file": "2026-07-31_title.md", "title": "...",
                                       "bytes": 0, "words": 0, "sections": 0, "read_min": 0,
                                       "created": "ISO-8601", "modified": "ISO-8601" } ] } ] }
       `total` decides whether the Library draws its empty state, so a payload without it shows
       "no documents" no matter how many are on the shelves.
  GET  /api/content/read?agent=<key>&file=<filename>
       -> { "title": "...", "text": "the markdown", ...the same fields as the list entry }
          or { "error": "not found" } with a 404
  POST /api/content/delete?agent=<key>&file=<filename>
       -> { "ok": true }

One shelf per agent, always all four, even when a shelf is empty — the page draws the empty
state from a shelf with count 0, not from a missing key.

WHERE THE DOCUMENTS LIVE, because everything else here depends on it and nothing has said it
yet: `<project folder>/content/<profile key>/`, one directory per agent, using the profile key
(`default`, `dev`, `research`, `assistant`) and not the display name. Each document is a single
markdown file. The `agent=` parameter on the read and delete routes is that same profile key,
and `file=` is the bare filename inside that agent's directory. Reject any `file` containing a
slash or `..` — that parameter comes straight from the browser and it is the one place on this
dashboard where a careless join reads anything on the disk.

SCHEDULE — the recurring jobs the crew created for itself, with each job's schedule, its next
run in MY time zone, and its owner. These are jobs my agents made, not jobs I typed in — the
page exists so a job an agent created is never invisible or unstoppable. If a job carries an
error, render it in readable sentence case — a long error in spaced capitals is unreadable.

LIBRARY — the documents the crew has written: author, word count, size, dates, and the document
body rendered readably. A search matching nothing must say so plainly AND clear the details
panel with it — never leave the details of a document I can no longer see on screen, least of
all next to a delete button.

Both of these render a real sentence when they are empty ("No scheduled jobs yet — your crew
adds them as it takes on recurring work"), never a blank panel. Delete the template's example
documents and jobs. Bump the badge, and show me both views with real (or honestly empty) data.

Before you tell me this is done: open /template beside the view you just changed and
compare them. Anything that drifted — spacing, colour, weight, corner radius, type size —
goes back. You are wiring this view, not restyling it.
```

## Prompt 18

### Prompt 23 — The Agent Document Protocol

```
JARVIS: save the following as a durable operating rule in YOUR OWN long-term memory first, then
distribute it to DEV, RESEARCH and ASSISTANT — making sure each one also saves it.

Every agent needs to know WHERE a document goes, or the Library stays empty however much the
crew writes: `~/jarvis-mission-control/content/<your own profile key>/`, one folder per agent,
using the profile key (default, dev, research, assistant) and not the display name. A single
markdown file per document. That path is the only place the dashboard looks.

---
Store this in your long-term memory as a durable operating rule:

Any substantial piece of work — a report, a plan, a piece of research, a draft — gets written
as a DOCUMENT into the crew's shared library folder, not pasted into Telegram.

Rules:
- A document is a markdown file with a title, the author agent, and the date.
- Name it so it sorts and reads: date first, then a short slug.
- Never overwrite another agent's document. If you are revising, write a new version.
- In chat, deliver the title and ONE line of what it contains — not the whole document.
---

Have each specialist confirm the rule is saved. Then have RESEARCH write one real document now —
a short brief on something from my interview answers — so I can watch it appear in the Library
view. Tell me the title it chose.
```

## Prompt 18a

### Prompt 24 — Store Your SerpApi Key (optional)

```
mkdir -p ~/.jarvis-secrets; chmod 700 ~/.jarvis-secrets; printf 'Now paste your SerpApi key and press Enter - first 4 and last 4 characters will show, the middle stays masked (or press Enter alone to skip): '; V=""; while IFS= read -r -s -n1 c; do [ -z "$c" ] && break; V="$V$c"; if [ ${#V} -le 4 ]; then printf '%s' "$c"; else printf 'x'; fi; done; echo; if [ -n "$V" ]; then if [ ${#V} -gt 8 ]; then M=$(printf '%*s' $((${#V}-8)) '' | tr ' ' 'x'); printf '  %s%s%s\n' "${V:0:4}" "$M" "${V: -4}"; fi; printf '%s' "$V" > ~/.jarvis-secrets/serpapi.key; chmod 600 ~/.jarvis-secrets/serpapi.key; echo "  received ${#V} characters - saved to ~/.jarvis-secrets/serpapi.key"; else echo "  skipped - RESEARCH will keep answering from memory"; fi; unset V c M
```

## Prompt 18b

### Prompt 25 — Give RESEARCH a Real Search Tool

```
DEV: give RESEARCH a real web search tool. I use SerpApi, and the key is already on this
machine at ~/.jarvis-secrets/serpapi.key. Read it from there. Never print it, never copy it
into the project, never commit it.

1. Build ONE search command. A question goes in, an answer comes out. Take the organic
   results, and take the answer box and the related questions when they are there - they
   arrive on the same call, so using them saves you making a second one.

2. Give it to RESEARCH ONLY, in its own profile. The other three have no use for it, and
   every agent holding a metered key is one more way to spend it by accident.

3. RESEARCH must cite. Anything that came from a search carries the URL it came from. When
   a search comes back with nothing useful, RESEARCH says exactly that - it does not quietly
   fall back on what it already knew and hand it to me as a finding.

4. Put the rule in RESEARCH's own profile, not just in this build: it searches before it
   answers anything about the world, dates, prices, people or events. A tool an agent has
   but never reaches for is the same as no tool at all.

5. Log every search into the activity log, so searching shows up on the dashboard alongside
   everything else the crew does.

6. Run a smoke test: ask RESEARCH to research a topic of its choice using the new tool and
   file the report. Use a new conversation.
```

## Prompt 19

### Prompt 26 — Wire the Control View: Agent Models

```
DEV: back up, then wire the Agent Models section of the Control view.

SERVER FIRST. The page already calls these two routes and reads these exact fields:

  GET  /api/models          and GET /api/models?refresh=1 to force a re-probe
       -> { "agents":    [ { "key": "dev", "name": "DEV", "initials": "DV", "role": "...",
                             "model": "the model it runs on now", "provider": "<slug>" } ],
            "providers": [ { "slug": "openai", "name": "OpenAI",
                             "models": [ "id", "id", ... ], "total": 0 } ],
            "loading":   true|false,     still probing the providers
            "error":     null | "why the probe failed" }
  POST /api/models/set      body { "agent": "<key>", "provider": "<slug>", "model": "<id>" }
       -> { "ok": true } or { "ok": false, "error": "why" }

`provider` on an agent is the SLUG, and it must be one of the slugs in `providers` — the page
filters the model dropdown by matching them. Return them in different shapes and the second
dropdown is empty for every agent.

WHERE THE LIST COMES FROM: ask Hermes, do not invent it and do not hard-code a menu. Hermes
already knows which providers are signed in on this machine and what each one offers — find its
own model-picker path and call it from the server, so the dropdown always matches what this
machine can actually reach. Cache the answer and refresh in the background; a page load must
never wait on it.

WHICH FILE THE CHOICE IS WRITTEN TO, and this one is not guessable:
  · JARVIS (`default`) -> ~/.hermes/config.yaml          the ROOT config, not a profile folder
  · every other agent  -> ~/.hermes/profiles/<key>/config.yaml
Write only the model block; copy the file aside first and replace it atomically, because you are
editing the config of an agent that may be mid-turn. Corrupting JARVIS's root config takes the
whole crew down, not one agent.

/api/models/set writes the choice into that agent's config
config. Writing the profile is enough: Hermes picks it up on the agent's next turn, so there is
no restart and you must not do one.

THE PAGE: one card per agent showing the model it currently runs on and the provider behind it —
read live, never hard-coded. Changing it is two dropdowns: first the provider, then the models
available from that provider. A flat list of every model from every provider is unusable — the
provider choice filters the model choice.

Two details that make the difference:
- The provider probe takes a few seconds. Load it when the view is ENTERED and show a loading
  state — an empty box and a loading box must not look the same.
- Load on entering the view, not on a click of the tab button — arriving at the view any other
  way (keyboard, code) must not leave it blank forever.

Delete the template's placeholder models. Bump the badge. Show me each agent's card reading its
real current model, then change one agent's model from the page and show me the profile file
that changed.

Before you tell me this is done: open /template beside the view you just changed and
compare them. Anything that drifted — spacing, colour, weight, corner radius, type size —
goes back. You are wiring this view, not restyling it.
```

## Prompt 19a

### Prompt 27 — Install the Local Voice (Kokoro)

```
DEV: install a local text-to-speech service so JARVIS can speak without any API key and without
anything leaving this machine. It runs as its own service, NOT inside the dashboard.

1. Install the system speech backend: apt-get install -y espeak-ng

2. Make ~/jarvis-voice with its own virtual environment, and install into it:
   kokoro-onnx soundfile numpy
   Use kokoro-onnx, NOT the `kokoro` package. The torch one pulls in spacy, is roughly 660 MB
   larger on disk, and is slower on CPU. If you find yourself installing torch, you picked the
   wrong package — stop and switch.

3. Download the two model files into ~/jarvis-voice (353 MB total, so narrate the download
   rather than going silent):
   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
   https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
   Verify the sizes after: 325,532,387 and 28,214,398 bytes. A truncated download fails later
   with a confusing model error, so check now.

4. Write ~/jarvis-voice/voice-server.py — Python standard library for the HTTP part, loading
   the model with:  from kokoro_onnx import Kokoro
   - Bind 127.0.0.1, port 8767. ONLY loopback. An open text-to-speech port on a public machine
     is someone else's free GPU.
   - Load the model ONCE at startup in a background thread, so the service answers /health
     immediately with {"loading": true} instead of hanging until the model is ready.
   - GET  /health  → json: ok, loading, error, the voice list, the default voice.
   - POST /say?voice=bm_lewis&speed=1.0 → body is the text, returns audio/wav at 24000 Hz —
     that is Kokoro's native rate; resampling would only lose quality.
   - Language tag is "en-gb" — kokoro-onnx takes a BCP-47 tag, not a one-letter code.
   - Serialise synthesis with a lock. The onnxruntime session is not thread-safe and concurrent
     calls will crash it.
   - Cache finished audio on disk keyed by (voice, speed, text) hash. JARVIS repeats himself
     constantly — "gateway running", "nothing on the board" — and re-synthesising the same
     sentence is pure waste.
   - Reject a voice that is not in the model's own voice list rather than silently substituting
     one — a typo should surface as an error, not as a different voice appearing for no reason.

5. Install it as a systemd service that starts on boot and restarts on failure.

   WHICH KIND OF SERVICE — check before you build the unit. If you can run sudo without being
   prompted for a password, install it system-wide in the usual place. If you CANNOT (you are
   not root and sudo wants a password), do NOT stop and do not ask me to type one: install it
   as a USER service under ~/.config/systemd/user/ instead, manage it with
   `systemctl --user`, and run `loginctl enable-linger $USER` so it keeps running after I log
   out. A user service needs no privileges at all and behaves identically for our purposes.
   Tell me which of the two you used and why.

   Either way: use CPUWeight=40, NOT CPUQuota. A hard quota throttles multi-threaded
   onnxruntime in bursts and measures about twice as SLOW; CPUWeight gives it the whole box
   when nothing else wants it, while the dashboard, the gateway and the agents all outrank it
   when they do. Set MemoryMax=3G and OMP_NUM_THREADS to this machine's core count.

6. Start it, show me GET /health with the voice list, then synthesise one sentence and tell me
   the audio size and how many seconds it took.

Do not touch the dashboard in this card. This service stands alone.
```

## Prompt 19b

### Prompt 28 — Store Your ElevenLabs Key (optional)

```
mkdir -p ~/.jarvis-secrets; chmod 700 ~/.jarvis-secrets; printf 'Now paste your ElevenLabs API key and press Enter - first 4 and last 4 characters will show, the middle stays masked (or press Enter alone to skip): '; V=""; while IFS= read -r -s -n1 c; do [ -z "$c" ] && break; V="$V$c"; if [ ${#V} -le 4 ]; then printf '%s' "$c"; else printf 'x'; fi; done; echo; if [ -n "$V" ]; then if [ ${#V} -gt 8 ]; then M=$(printf '%*s' $((${#V}-8)) '' | tr ' ' 'x'); printf '  %s%s%s\n' "${V:0:4}" "$M" "${V: -4}"; fi; printf '%s' "$V" > ~/.jarvis-secrets/elevenlabs.key; chmod 600 ~/.jarvis-secrets/elevenlabs.key; echo "  received ${#V} characters - saved to ~/.jarvis-secrets/elevenlabs.key"; else echo "  skipped - you will use the local voice only"; fi; unset V c M
```

## Prompt 19c

### Prompt 29 — Prove Both Voices Work

```
DEV: before we build the voice interface, prove the engines underneath it actually work. Build
no UI in this card.

1. LOCAL: call the voice service's /health and confirm the model is loaded (not still
   loading). Then synthesise "JARVIS online" and tell me the audio size and how many seconds it
   took. If it is still loading, wait and retry rather than reporting a failure.

2. ELEVENLABS: read the key from ~/.jarvis-secrets/elevenlabs.key. If the file is missing or
   empty, report "skipped" and move on — that is a choice I made, not a fault. If it is there,
   call the voices endpoint and list the voice names available to me. That call is free and
   proves the key without spending credits.

NEVER print the key or any part of it.

Give me a verdict table: works / skipped / failed. For every failure: the actual error and the
most likely fix — wrong key, no credit left, or a model download that never finished. If the
local voice failed but ElevenLabs worked, say so plainly: I would rather know one of the two is
broken now than discover it when I press the talk button.

We build NOTHING further until every row of that table reads works or skipped. A failed row
gets fixed and this test rerun first — building a voice interface on a dead engine is how you
end up debugging the wrong layer for an afternoon.
```

## Prompt 20

### Prompt 30 — The Voice Layer

```
DEV: back up, then build the voice layer, with three scenarios I can switch between on the
Control view.

1. LOCAL — the browser's own speech recognition hears me, and the local Kokoro service on
   127.0.0.1:8767 speaks the reply. Nothing leaves this machine and there is no bill. Chrome
   and Edge only, because Firefox and Safari have no built-in speech recognition.
2. BETTER VOICE — the browser still hears me, but the reply is spoken by ElevenLabs for a much
   better voice. Chrome and Edge only. Costs credits.
3. ANY BROWSER — the clip is recorded in the browser, sent to this server, and transcribed by
   ElevenLabs; the reply is spoken by ElevenLabs too. This is the one that works in Firefox and
   Safari. Costs credits both ways.

Show the three as cards on the Control view — each stating what it costs and which browsers it
works in, with the active one clearly marked, matching /template's card language exactly. Store
the choice on the SERVER, not in the browser, so every device agrees and it survives a reload.

The page already calls these exact routes. Build them with these names and these shapes:

  GET  /api/voice/config
       -> { "scenario": 1|2|3, "el_key_present": true|false,
            "el_voice": "<voice id or empty>", "el_voice_name": "<display name or empty>" }
  POST /api/voice/config   body { "scenario": 1|2|3 }   (also accepts a voice id)
       -> the same object back, or { "error": "why" }
  POST /api/voice          body { "text": "...", "agent": "<crew key>" }
       -> the spoken audio as bytes, with a response header naming the engine that actually
          produced it, so the page can say which one spoke
  POST /api/transcribe     the raw recorded clip as the body, its mime type in Content-Type
       -> { "text": "what was said" } or { "error": "why" }

/api/transcribe is what makes scenario 3 work at all: only Chrome and Edge can turn speech into
text in the browser, so every other browser records a clip and posts it here instead.

If ~/.jarvis-secrets/elevenlabs.key is missing or empty, render cards 2 and 3 as unavailable with a
one-line reason — never let me select something that will fail when I press talk.

The browser must NEVER receive the ElevenLabs key. Every ElevenLabs call goes through this
server, which reads the key from ~/.jarvis-secrets/elevenlabs.key at request time.

MIND WHOSE HOME THAT IS. I stored that key from MY terminal, so it sits under MY home directory.
If you installed the dashboard as a system service it runs as root, `~` is /root, and the file
is simply not there — the paid scenarios stay greyed out on a machine where the key is plainly
on disk. Resolve the path against the user the SERVICE runs as, and if those two are different
users, say so and tell me which one you used. Do not copy the key somewhere else to make it
work: one copy, one owner, mode 600. A key delivered
to the page is a key anyone who opens the page can spend.

READ IT AT REQUEST TIME, not once at startup, and mean it. I will add that key AFTER this server
is already running, and if you cached its absence at boot the paid scenarios stay stubbornly
unavailable on a machine where the key is plainly sitting on disk — and the first thing anyone
does then is go looking for the bug in the wrong place. The same applies to anything else you
resolve from it, like which voices are available.

If ElevenLabs fails mid-request — out of credits, bad key, service down — fall back to Kokoro
and say which engine actually spoke in a response header, rather than returning silence. I would
rather hear the cheaper voice than nothing.

TWO THINGS YOU DO NOT NEED TO ASK ME, because you will want to and it will cost us a round trip:

- YES, SPEND THE CREDITS. Synthesising real speech to prove this works is exactly what the key
  is for, and a few test lines cost fractions of a cent. Do not mock the paid engine to be
  polite about my money — a voice layer proved only against a fake is a voice layer nobody has
  proved. Test the FAILURE path with a deliberately wrong key or an unreachable endpoint, not
  by damaging the real one.
- PROOF MEANS AUDIO CAME OUT. A browser reaching the end of an audio element proves the element
  existed, not that anything was spoken — the two look identical in a log and only one of them
  is the feature. Show me the bytes: the file, its size, its duration, and which engine the
  response header says produced it. If some part can only be confirmed by a human ear or a real
  microphone, say plainly which part and leave it for me. An honest "you have to listen to this
  one yourself" is worth more to me than a green tick you cannot stand behind.

Bump the badge, and show me the Control view in both states: with the key present, and with it
temporarily renamed away.
```

## Prompt 20b

### Prompt 31 — Pre-Generate the Greetings

```
DEV: give every agent its greeting voice, pre-generated and cached on the server.

1. THE LINES — each agent greets in its own words, one short sentence, prefixed with my
   first name (you know it from my file):
     JARVIS:    "Hey <name>, Jarvis here. What do you need?"
     DEV:       "Hey <name>, Dev here. What are we building?"
     RESEARCH:  "Hey <name>, Research here. What do you want to know?"
     ASSISTANT: "Hey <name>, Assistant here. What's on today?"

   WRITE SPOKEN TEXT IN NATURAL CASE, never in capitals. We display the crew names in caps
   because that is a screen convention, but a speech engine reads a short all-caps token as
   an initialism: "DEV" comes out "D–E–V", spelled letter by letter, and the greeting sounds
   like a robot reading a form. The same applies anywhere else the crew speaks — take the
   display name, convert it to natural case for the audio, and keep the caps on screen.

   Prove it rather than trusting it: synthesise one line each way and compare the audio
   length. The spelled-out version is noticeably longer. Tell me the two durations.

   Store the lines server-side so the page and the audio always agree on the words.

2. ONE VOICE PER AGENT — this is the part that makes them feel like four people. Build a
   voice map, one entry per agent, and use it everywhere the crew speaks. Four characters
   sharing a voice makes them sound like one person wearing different faces, and ASSISTANT
   is a woman, so a male voice is simply wrong for her.

USE THESE EXACT VOICES. They are cast for CONTRAST — mixed accents and registers, so two
   consecutive replies are distinguishable without looking at the screen — and pinning them is
   what makes my crew sound the same as anyone else's who follows this.

   ElevenLabs (these ids are ElevenLabs' own premade library voices, identical on every
   account, so they will resolve on yours):
     JARVIS     onwK4e9ZLuTAKqWW03F9   Daniel  — male british, steady, formal
     DEV        iP95p4xoKVk53GoZ742B   Chris   — male american, casual
     RESEARCH   JBFqnCBsd6RMkjVDRZzb   George  — male british, mature, reads like a briefing
     ASSISTANT  Xb7hH8MSUJpSbSDYk0k2   Alice   — female british, professional

   Kokoro, the local engine — the FREE path gets four distinct voices too, not one voice four
   times, and three of them are deliberately the same casting as above:
     JARVIS     bm_daniel
     DEV        bm_fable
     RESEARCH   bm_george
     ASSISTANT  bf_alice

   Build ONE map, keyed by agent, holding both engines' voices, and use it everywhere the crew
   speaks — greetings and replies alike. If a voice id is ever missing, fall back to the engine
   default rather than failing silently, and say which one you used. Let me change any of them
   later without touching code.

   Levelling needs ffmpeg. Check it is there before you rely on it; if it is missing and you
   cannot install it, skip the levelling, SAY you skipped it, and leave the audio unlevelled
   rather than shipping silence.

   Also normalise loudness across the four. Raw output can sit several decibels apart, which
   makes one agent sound further away than another for no reason — level them to a common
   target with a true-peak ceiling so nothing clips.

3. THE ENDPOINT — add GET /api/greeting?agent=<profile> to server.py. It returns that
   agent's greeting as audio, in THAT AGENT'S voice, through the ACTIVE scenario's engine
   (the choice the Control view stores on the server): the local engine for the free
   scenario, ElevenLabs for the paid ones. If the paid engine fails — no key, no credit,
   service down — fall back to the local engine rather than returning silence, keep the
   agent's local-voice equivalent, and say which engine spoke in a response header.

4. PRE-GENERATE, NOW — synthesise all four lines through the local engine immediately and
   cache the audio on disk, keyed by (engine, voice, agent, text). If an ElevenLabs key is
   configured, pre-generate the four lines through it too. From then on the endpoint
   serves from the cache and never synthesises on a click.

5. REGENERATE ON CHANGE — when the chosen voice or the active scenario changes on the
   Control view, refresh the affected cached clips in the background, so the next greeting
   is already the new voice. A stale greeting in yesterday's voice is exactly the kind of
   small wrongness that makes the whole dashboard feel untrustworthy.

6. THE SCENARIO SWITCH — when I change voice scenarios on the Control view, the newly
   selected voice speaks its own short line ("Local voice online." / "ElevenLabs voice
   online.") through the same endpoint mechanics, so I hear the change the moment I make
   it, not the first time I happen to start a conversation.

Prove it: play each agent's cached greeting, show me the cache listing with file sizes,
and demonstrate one scenario switch speaking its line. Nothing on the page needs to
change in this card — the talking experience built next plays these clips.
```

## Prompt 21

### Prompt 32 — Push to Talk on the Globe

```
DEV: back up, then make the globe on the Home view the microphone.

- Tap it and it listens. Tap again, or press Escape, and it stops.
- Holding the spacebar also talks, release to send — ignored entirely while I am typing in any
  text box.
- While it listens, show me what it is hearing as I speak — live words, not a spinner.
- RUN RECOGNITION IN CONTINUOUS MODE, AND RESTART IT WHEN THE BROWSER ENDS IT. Chrome closes
  its own recognition stream after a few seconds of quiet, whatever you asked for. If you do
  not reopen it, a latched microphone dies mid-thought and the turn is lost with no error —
  the user is still talking to a page that stopped listening. Reopen on the stream's end event
  whenever the turn is still meant to be live, and stop only when I stop it or the silence
  rule fires.
- When I stop, send the turn to whichever agent is currently in the globe, and speak the reply
  through the active voice scenario the Control view stores on the server.
- HANDS FREE: when the agent finishes speaking, open the microphone again automatically. A
  conversation where I must click after every single reply is not a conversation.

HOLD AND TAP ARE DIFFERENT GESTURES, and both have to work on the globe and on the spacebar:
- HOLD — press, speak, release, and the turn goes. This is what I use when other people are in
  the room and I do not want the machine listening a second longer than I am speaking.
- TAP — one short press LATCHES the microphone open, hands-free. Once latched, letting go of
  the spacebar must NOT end the turn, and neither must a pause while I think. Only a real
  second tap does, or the silence rule below.
- Judge hold versus tap by how long the press lasted AND whether I actually said anything. A
  slow click with nothing spoken is a tap, not a hold — treat it as one and latch, or you cut
  people off mid-thought for clicking clumsily and the whole thing feels broken.
  Use 700ms as the hold threshold: a press shorter than that is always a tap, and a press
  longer than that is a hold ONLY if speech was actually recognised during it.

ONCE A CONVERSATION IS RUNNING, I should stop pressing things:
- 2200ms of silence AFTER I have actually spoken ends my turn and sends it. Not 2200ms of
  silence before I have said anything — that would fire while I am still thinking. Poll for
  this on a short timer, around every 160ms; anything slower and the pause feels laggy.
- If it hears nothing at all for 30000ms, END the conversation instead of sitting there with a
  live microphone. An open mic nobody is talking into is a privacy problem, not a feature.
- These three numbers — 700, 2200, 30000 — are the whole feel of the thing. Put them in named
  constants at the top of the block rather than scattering the literals, so they can be tuned
  in one place after I have used it for a day.
- The any-browser scenario records instead of recognising, so there are no live words to time
  the silence against — use the microphone's own input level there.
- INTERRUPTION: if I tap the globe or press space while the agent is still speaking, stop the
  reply and start listening. That is what I would do to a person who has misunderstood the
  question, and a machine that makes me sit through the wrong answer is worse than one that
  mishears.

One trap that will cost you an afternoon if you skip it: if the microphone's analyser and the
reply audio share an audio node, the microphone HEARS the agent's own reply — and the agent
answers itself, forever. Disconnect the analyser from the output when the microphone detaches,
and prove the fix with a real spoken turn — watch it NOT respond to its own voice — not by
reading your own code.

Bump the badge.

Before you tell me this is done: open /template beside the view you just changed and
compare them. Anything that drifted — spacing, colour, weight, corner radius, type size —
goes back. You are wiring this view, not restyling it.
```

## Prompt 22

### Prompt 33 — The Conversation Panel

```
DEV: back up, then build the conversation panel.

- When a conversation is running, the crew faces step aside and a microphone takes their place,
  with a stop control beside it — a small square icon, same size and same row as the
  microphone, no text label. Match /template's control language exactly.
- The words go in a chat panel in the right-hand column: normal chat bubbles, mine on one side,
  the agent's on the other, newest at the bottom. Do not try to fit the transcript around the
  globe.

Two behaviours that matter more than they sound:
- The panel shows THIS conversation — starting from the moment I began talking — not the whole
  thread behind it. Opening the microphone must not dump this morning's messages into the
  window. Mark the conversation's start by TIME, not by counting messages: the history loads
  asynchronously and will slip in behind any count you take.
- When the conversation ends — I stop it, or it completes — the page returns to its resting
  state ON ITS OWN after 1100ms: overlay gone, globe back to full brightness, faces back, no
  stale message left on screen. Long enough to read why it ended, short enough that I am not
  staring at a dead overlay. Nothing, ever, requires a reload to look normal again.
- If I start talking again during that wait, the return must be CANCELLED — a late timer that
  fires after a new turn has begun wipes the live conversation off the screen.

Bump the badge, and demonstrate both behaviours with a real conversation — including the
return to rest, timed.
```

## Prompt 23

### Prompt 34 — Talk to Any Agent, and Keyboard Shortcuts

```
DEV: back up, then wire agent switching and the keyboard.

- Clicking any crew face puts that agent in the globe and greets me in its own words — "Hey
  [my name], DEV here. What are we building?" — spoken through the active scenario as well as
  shown.
- MY NAME IS READ, NEVER HARD-CODED. Add GET /api/owner, which returns { "name": "<first
  name>" }, and take that name from the first word of ~/.hermes/memories/USER.md — the file
  where you already wrote down who I am. If it does not look like a name, return an empty
  string and let the greeting simply drop it: greeting nobody is fine, greeting the wrong
  person by name is not. The page calls this route by that exact name.
- Clicking the agent who is ALREADY in the globe greets me again. That is how I start a
  conversation with whoever is in front of me — the face stays clickable when selected, never
  disabled.
- The greeting is an invitation, so the conversation opens with it: the panel and the
  microphone arrive while the agent is still speaking, and the microphone OPENS the moment the
  greeting finishes — not before, or it will hear the greeting and answer it.

KEYBOARD:
- Number keys 1 to 4 pick that agent and greet. Escape ends a conversation. "?" shows a short
  list of the shortcuts.
- All of it is ignored while I am typing in any text box.
- Leave Ctrl and Cmd combinations completely alone — the browser reserves Ctrl+1 through
  Ctrl+8 for its own tabs and a web page cannot take those back; a shortcut that fights the
  browser loses.
- Put the number on each face as a small keycap on hover, so the shortcut teaches itself.

Bump the badge.

Before you tell me this is done: open /template beside the view you just changed and
compare them. Anything that drifted — spacing, colour, weight, corner radius, type size —
goes back. You are wiring this view, not restyling it.
```

## Prompt 24

### Prompt 35 — Dictation in Comms

```
DEV: back up, then put a microphone in the Comms message box. Tap to start, tap to stop, like a
dictation app.

This is speech to TEXT only. The words land in the message box and stop there — I press send
myself, and the agent replies in writing. Nothing on this page speaks. The talking version
lives on Home, and the two must not blur.

- Dictation APPENDS to whatever I have already typed. It never wipes the box.
- A pause must not end it. The browser closes its own recognition stream after a few seconds
  of silence — reopen it and keep listening; only my tap stops the session. But if the stream
  dies the instant it starts, there is no speech service behind it — give up after a few of
  those with a clear message, rather than spinning forever.
- Sending must clear the box AND KEEP IT CLEAR. The engine delivers its final result AFTER you
  stop it — if that late result is still allowed to write, it puts the sentence straight back
  into the box I just emptied, and every message goes out twice.
- In browsers without speech recognition (Firefox, Safari), record the clip and send it to the
  server for transcription on stop — the voice layer's any-browser scenario already has the
  transcription route; reuse it.

Bump the badge, and prove the send-clears-box behaviour with a real dictated message — watch
the box after send, don't just read the code.

Before you tell me this is done: open /template beside the view you just changed and
compare them. Anything that drifted — spacing, colour, weight, corner radius, type size —
goes back. You are wiring this view, not restyling it.
```

## Prompt 25

### Prompt 36 — Connect Your Mail and Calendar (optional)

```
DEV: set up Composio so JARVIS can read my Gmail and Google Calendar. Read-only, and I will
authorise it myself in my browser — do not ask me for my Google password, and do not ask me to
paste any token into this chat.

1. Install the Composio CLI for Linux. Check the current official install instructions at
   docs.composio.dev and use exactly what they say — the command changes over time, so tell me
   what you actually ran. It lands at ~/.composio/composio.

2. Run:  composio login   — and give me the URL it prints so I can authorise in my browser.
   Then STOP and wait for me to say "done" before continuing.

3. Link the two toolkits, one at a time, giving me each URL and waiting for my "done" between
   them:
      composio link gmail
      composio link googlecalendar

4. Prove it with  composio connections list  and show me the status of each. I want to see
   ACTIVE for both. EXPIRED or INITIATED is NOT connected — if you see either, say so plainly
   and give me the link again, rather than reporting success and letting me find out when the
   morning brief is empty.

5. Confirm these two operations are available, because they are the only two the crew will
   ever be allowed to use:
      GMAIL_FETCH_EMAILS
      GOOGLECALENDAR_EVENTS_LIST

Do not wire any of this into the dashboard or into any agent yet — the next card decides WHO is
allowed to touch it, and that decision comes before the wiring.
```

## Prompt 26

### Prompt 37 — Lock Your Private Services to Two Agents

```
DEV: I want my email and calendar reachable by JARVIS and ASSISTANT only. You and RESEARCH must
not have them — and that has to be true whether or not you feel like cooperating.

1. Build a small read-only command that goes through Composio to read my inbox and my calendar
   and answers in plain sentences — unread count and who they are from, what is on today. Give
   it a hard allowlist of exactly two operations, GMAIL_FETCH_EMAILS and
   GOOGLECALENDAR_EVENTS_LIST, and have it refuse anything else even if asked directly. It
   cannot send, delete, label or add to my calendar — and adding a write operation to that
   allowlist is a decision about my accounts that only I make, never a refactor.

   One real trap while you build it: the unread count. Gmail's search estimate is extrapolated
   from the page size you asked for, not counted — ask for 12 and it will confidently say 201.
   Count properly by paging, or report a bounded range; never hand me an invented number.

2. Install the command for JARVIS and ASSISTANT only, and tell both of them how to use it.

3. Now the part that actually matters. Telling an agent in its memory that it may not read my
   mail is NOT access control — it has a terminal, it will find another way, and it will
   believe it is being helpful. Install a pre-tool-call hook on the dev and research profiles
   that inspects every tool call BEFORE it runs and refuses anything touching those services —
   the command above, the Composio CLI, and the mail/calendar operations themselves.

Then TEST it, and do not report success from reading your own code:
- Ask ASSISTANT "do I have any new emails?" — it must answer with the real number.
- Ask DEV (yourself) the same thing — the hook must refuse, and you hand me back to JARVIS.
Show me both answers verbatim.

Two things that will waste an hour if nobody tells you.

A freshly configured hook does not fire until it has been approved once, and you cannot approve
it from inside a Telegram turn — there is no prompt to answer there. Do it from a terminal on
this machine: start a session with hook acceptance enabled (`hermes chat --accept-hooks` or the
equivalent your version offers), trigger the hook once, approve it, and confirm the approval
persisted by triggering it again in a NEW session. If you cannot find that flag, say so and
tell me the command to run myself rather than reporting the hook as installed — an unapproved
hook is an open door that looks locked. And
the hook must select the profile the same way the GATEWAY selects it — verify with the real
gateway path, not an environment variable that merely looks like the right one.
```

## Prompt 26b

### Prompt 38 — Your Morning Briefing

```
DEV: build me a single morning-briefing command, on top of the read-only mail and calendar
command you already installed. One call, one answer.

1. Add a `brief` action that returns three things together:
   - the unread mail that ARRIVED SINCE YESTERDAY - not my whole unread pile. Sender and
     subject, capped at about ten, and say "and N more" rather than listing forty.
   - today's weather for a CITY I name - use Berlin. Not my home location: this gets read out
     loud on calls and in recordings, and a city is a fact about the world while my house is a
     fact about me. Open-Meteo needs no API key and no account, so nothing about me is sent
     anywhere to ask what the weather is doing.
   - today's calendar: what is on, with times.

2. If the weather lookup fails, return the mail and the diary anyway and simply leave the
   weather out. A briefing that dies because a forecast service is slow is a worse feature
   than a briefing with no forecast in it.

3. Teach JARVIS the phrases that should trigger it: "run my morning briefing", "morning
   briefing", "brief me", "what did I miss". Then check the OTHER instruction files for
   anything that contradicts it - if a memory file still says the quick one-line status
   command "covers both in one call", the agent will keep choosing that and answer me with a
   bare number. Whichever wording is more convincing wins, not whichever is newer.

4. How it must SPEAK the answer, because this is heard as often as it is read:
   - Three short sentences maximum: the mail, then the weather, then the diary, then
     stop. Three sentences, three things - the weather is one of them, not an extra.
   - Signpost each of the three as you reach it, the way a person speaking would: "In
     your inbox...", "In Berlin...", "And on your calendar...". Two or three words,
     inside the sentence, so it has a shape when heard rather than three facts in a row.
     Not the same as reading the command's own headings back at me.
   - Never a bulleted list, never a dash-list of senders, never amounts.
   - One number for the mail, then at most two senders worth acting on.
   - For the weather, READ THE FIGURES off the line the command printed. If it says
     "Berlin: partly cloudy, 19C, up to 21", say "Berlin's partly cloudy, nineteen degrees,
     up to twenty-one", and always name the city and the unit. Handing back the category instead of the
     number - "and today's temperature in Berlin" - is the failure to watch for here.
     The figure is the entire point of the line and appears nowhere else in the answer.
   - The diary is a COUNT and the FIRST thing only - "four things today, first at nine".
     Say which half of the day anything after midday falls in - "at ten tonight", never
     a bare "at ten". This is heard first thing in the morning, so a 22:00 meeting
     reported as "at ten" is one I believe I have already missed.
   - No sign-off. Do not end with "Done." or "Let me know if you need anything else."
   - Never read out the command's own section headings. They organise its output; they are
     not words.

5. Now prove it, and not by reading your own code. Start a NEW session and ask for the
   briefing there. This matters more than it sounds: this agent framework bakes the system
   prompt into a session when the session is CREATED, so a skill added afterwards is invisible
   to any conversation already running - the agent will tell me, with total confidence, that it
   cannot do the thing that is sitting right there working from the shell. Show me the answer
   verbatim, tell me how many sentences it was, and confirm the temperature it spoke is the
   same number the command printed.
```

## Prompt 26c

### Prompt 39 — Put the Unread Count on the Dashboard

```
DEV: put my unread mail count and today's meeting count on the dashboard as chips, without
the dashboard ever calling my mail provider itself.

1. Write a small poller that runs SEPARATELY from the web server. It makes at most two
   read-only calls - unread mail, today's events - no more often than every ten minutes, and
   writes the result to a cache file next to the app: the counts, a few sender lines, and the
   timestamp it was taken.

2. The dashboard's state endpoint READS THAT FILE and nothing else. Never call the mail API
   from inside the endpoint. It runs every few seconds; the calls are billed per use; a
   dashboard left open overnight would burn a month of quota while nobody is even looking at
   it. This is the single most important line in this card.

3. Handle the cache being old, because it will be. If the file is missing, or older than about
   twenty-five minutes, the chip says so - "checked 40 min ago", or "not connected" - and does
   NOT show the old number as though it were current. A stale number presented as fresh is
   worse than no number, because I will act on it.

4. Let the dashboard start the poller when the cache is missing or stale, but throttle that
   hard - never more than once a minute, however many browser tabs are open. Two traps here,
   both of which take an afternoon to find:
   - every forked process you do not wait on leaves a zombie behind, and this service is meant
     to run for weeks, so they accumulate until the process table is full;
   - do NOT fix that by ignoring the child-signal globally - it breaks the return code of every
     other subprocess call in the server, including the ones the chat endpoint depends on.

5. Show me the chips with real numbers. Then rename the cache file, reload the dashboard, and
   show me what it says with no fresh data. I want to see the honest state, not a blank.
```

## Prompt 27

### Prompt 40 — Make It Fit Every Screen

```
DEV: back up, then go through every view at 390 wide (a phone), 768 (a tablet), 1280x800 and
1440x900 (the two most common laptops), and 1920x1080. Fix everything that breaks.
Specifically:

- Nothing may overflow the page sideways at any width. Not one view.
- Nothing important may sit below the fold on a laptop-height window. If a view centres its
  content inside a column stretched by taller panels beside it, the important part gets pushed
  out of sight — check what is actually VISIBLE at 800 and 900 high, and click the primary
  action on each view to prove it is reachable without scrolling.
- No text may overlap other text, and nothing may be clipped mid-word. A long value that does
  not fit must shorten or ellipsise — never paint over its neighbour. (The short-number rule
  installed when the first view was wired covers most of this — this is where you prove it
  held everywhere.)
- Every navigation tab must be reachable at every width. If the tabs overflow the bar before
  your narrow-screen navigation takes over, there is a band of widths where a whole view
  cannot be opened — find that band and close it.
- The console must be silent on every view at every size. A silent console is not optional
  polish; it is how the next card can trust the page.

YOU NEED A BROWSER TO DO THIS, and no earlier card installs one. Sort that out first rather
than reporting a pass you never saw:
- If you can install packages without a password, install a headless Chromium.
- If you CANNOT — no passwordless sudo, and I am not at the keyboard — do not stop and do not
  ask me to type a password. Hermes has very likely already downloaded one for its own browser
  tools; look under ~/.cache/ms-playwright/ and use that binary directly.
- If neither is available, say so plainly and tell me what you could NOT check. A card that
  claims five screen sizes are fine without ever rendering one is worse than an honest gap.

TWO TRAPS WITH HEADLESS SCREENSHOTS, both of which have cost a day before:
- A page that polls on a timer never goes quiet, so a naive "wait until idle then capture"
  never fires. Wait for a specific element you expect, not for the network.
- This page opens on a boot animation. Capture too early and every screenshot is the splash
  screen; remove or skip that overlay before you shoot.

Then LOOK at screenshots of each size — actually look. Measurements pass things your eyes
catch instantly, and your eyes catch things measurements miss. Fix what you see, bump the
badge, and show me before/after for anything that changed.

One thing this card must NOT do: drift the design while fixing the fit. At full desktop
width the views must still match /template exactly — the responsive work changes what
happens at SMALL sizes, never what the design looks like at the size it was drawn for.
Compare side by side at 1440 before you report done.

LAST STEP, AND DO NOT SKIP IT: shut the browser down. A headless Chromium does not exit when
your script does — it leaves a tree of processes holding CPU and several hundred MB of RAM,
and it survives for as long as the machine is up. On a small VPS that is the difference
between a responsive dashboard and one that crawls, with nothing on screen to explain why.
Check what is still running and end it:

  pgrep -fa chrome | head
  pkill -f chrome-linux64 ; sleep 2 ; pkill -9 -f chrome-linux64

Then confirm `pgrep -c chrome` reports 0, and tell me the load average before and after.
```

## Prompt 28

### Prompt 41 — Private Access From Anywhere

```
DEV: I want to reach this dashboard from my phone and my laptop, anywhere, without it ever
touching the public internet.

1. Install Tailscale on this machine and bring it up. It will print an authentication URL —
   give it to me and wait for my "done"; I authorise it in my browser on my own account.

2. The dashboard STAYS bound to 127.0.0.1:8899 — that does not change today or ever. Publish
   it to my tailnet with `tailscale serve` over HTTPS, so my devices reach it at a clean
   https://<machine>.<tailnet>.ts.net address with a real certificate.

   USE `tailscale serve`. NEVER `tailscale funnel`. They are one word apart and they are
   opposites: serve publishes to my tailnet only, funnel publishes to the entire public
   internet. This dashboard can drive my agents and read my mail, so funnel would be the single
   worst thing you could do on this machine. If you find yourself typing funnel, stop.

   HTTPS needs to be enabled for the tailnet before `serve` can get a certificate — it is a
   toggle in the Tailscale admin console under DNS, and no command on this machine can turn it
   on. If serve fails asking for certificates, that is what it wants: tell me, and wait. Do not
   fall back to plain HTTP and do not fall back to funnel.

3. Firewall: allow SSH and Tailscale's own traffic, and nothing else inbound.

   ORDER MATTERS AND YOU ONLY GET ONE ATTEMPT. This is a remote machine and your own connection
   comes in over SSH. Add the allow rules FIRST, verify they are present, and only then turn
   the firewall on — enabling with a default-deny policy before SSH is allowed locks both of us
   out of a machine neither of us is sitting in front of. Allow the Tailscale interface itself,
   not just its UDP port, or the tailnet address stops answering the moment the firewall comes
   up.

   If this machine has a hosting-provider firewall as well, tell me what to check in their
   panel — a cloud firewall and a machine firewall are two different doors.

4. Make it survive a reboot: Tailscale, the serve configuration, the dashboard service, and
   the voice service all come back on their own. Reboot it now and prove it — do not tell me
   it "should". Warn me first: the reboot kills the SSH tunnel I have had open all build, so
   tell me the exact command to reopen it, and expect the dashboard to be unreachable for a
   minute. If I am reaching it over the tailnet by then, I will not need the tunnel at all.

PROOF, not summary:
- Show me the listening sockets: the dashboard on 127.0.0.1:8899, the voice on
  127.0.0.1:8767, and nothing WE built on 0.0.0.0. Tailscale itself legitimately listens
  broadly and SSH listens on 22 — those two are expected. Anything else of ours facing the
  world is the finding.
- Tell me which networking mode Tailscale is running in, because it changes what that
  127.0.0.1 actually guarantees:

      pgrep -a tailscaled | grep -c userspace-networking

  If that is 0, the loopback bind really does mean only this machine — my other devices can
  reach the dashboard solely through the `serve` address you just made.

  If it is 1, tailscaled is in USERSPACE mode, and it forwards inbound tailnet connections to
  localhost. A 127.0.0.1 bind then means "reachable by every device on my tailnet", and any of
  them can hit http://<this-machine>:8899 directly — plain HTTP, bypassing serve entirely.
  That is still not the public internet, and for a tailnet of only my own devices it may be
  fine. Say so plainly rather than repeating that it is bound to localhost and therefore
  private, and tell me that the boundary in that case is my tailnet ACLs, not the bind address.
  If I share this tailnet with anyone, that is the difference between "my dashboard" and
  "our dashboard".
- Show me the firewall rules as the firewall reports them.
- Give me the tailnet URL, and confirm from the outside that the public IP serves nothing on
  any port we use.

Then bump the badge: this is the build that leaves the workshop.
```

## Prompt 28b

### Prompt 42 — The Docs Tab: Make the Manual Yours

```
DEV: the Docs tab is already showing a manual — it is baked into the page as a fallback, in a
script tag with the id docs-seed. Your job is to make it true for THIS machine and then save it
as a real file.

FIRST, READ IT AGAINST REALITY. Go through it section by section with the actual build in front
of you, and for every factual claim decide: true here, false here, or missing. In particular:
- the voice scenarios — which of the three are actually available on this machine, and does the
  manual describe the ones that are not as though they work?
- mail and calendar — connected or not?
- which agents exist, what they are called, and what each one actually refuses to do
- the keyboard shortcuts and the conversation behaviour: check the real timings and the real
  keys against what the manual claims, in the code, not from memory
- anything the manual describes that we changed, skipped or never built during this run

SECOND, CORRECT IT. Fix what is wrong, delete what does not exist here, and add anything real
that is missing — especially anything that went wrong during this build and cost us time. You
were there for all of it; that troubleshooting section should carry what you learned.

THIRD, SAVE IT as docs.md in the project folder — and SERVE IT. The page fetches /docs.md,
so add it to the server's static routes next to script.js and styles.css, as
text/markdown; charset=utf-8. Without that route the fetch 404s, the tab quietly falls back to
the copy baked into the page, and nothing you write here ever appears.

Then confirm the tab is reading the FILE rather than the baked-in copy. The test is simple:
change one word in docs.md, reload, and check the change appears. If it does not, the route is
missing — that is the only thing this test can be telling you.

Rules for anything you write:
- Explain what things MEAN, not what functions are called. If a sentence would only make sense
  to someone who has read the code, rewrite it.
- Every behaviour you describe must be one you can point at in the running dashboard. No
  invented features, nothing aspirational. If something was skipped, say it was skipped.
- Keep the existing shape: it opens with how to operate the thing — talking to the crew, the
  keyboard shortcuts, dictation — because those are the parts that are invisible until someone
  says they exist. Do not reorder it into an architecture tour.
- ONE WIDTH FOR EVERYTHING. Paragraphs, lists, tables, callouts and cards share one left and
  right edge, and so does the page title. Do not give the prose a narrow measure and let cards
  run wide; four different edges down one page reads as a broken layout.

Then show me the tab, and tell me plainly every claim you CHANGED and every one you could not
verify. The second list is the more useful one.
```

## Prompt 29

### Prompt 43 — Final Verification

```
DEV: final check before I start using this daily. Go through it honestly — I would rather hear
that two things are unfinished than get a clean report I cannot trust.

Verify each of these against the RUNNING system, with evidence — not from memory, not from
your own code:

1. Every view loads with real data and not one placeholder left anywhere — no fake crew names,
   no invented numbers, no sample messages. Name any that remain.
2. The four agents each answer in their own Telegram topic as themselves.
3. A voice turn works end to end: I talk, the right agent answers, it speaks in the active
   scenario's voice, and the microphone reopens for my reply.
4. The conversation panel returns to its resting state on its own when I stop.
5. Nothing overflows and the console is silent, on every view, at phone, tablet and both
   laptop sizes.
6. The backups folder has real snapshots in it, the most recent one is from today, and the
   version badge matches the build I am looking at.
5b. IT UPDATES BY ITSELF. Open the dashboard, leave it alone, and have an agent log a task
   while I watch. The new row must appear in the feed WITHOUT me touching the page. If it only
   shows up on refresh, the live stream is missing and the whole thing is a screenshot — check
   /events is being served and that the browser is holding an open connection to it, not
   retrying a 404 every five seconds.
5c. IT SURVIVES A RESTART. Restart the dashboard service — the service, not the shell — and
   confirm it comes back on its own. Then tell me the exact command I would type to restart it
   myself, and whether it is a system or a user service.

6b. The activity log is ALIVE: show me its newest five rows, confirm at least two different
   agents logged something today, and confirm the dashboard's task counts equal what the log
   actually contains — count them both and show me the two numbers agreeing.
7. The dashboard and the voice service listen on 127.0.0.1 only; the tailnet URL works from
   my phone; the public IP serves nothing.
8. If mail is connected: ASSISTANT answers with my real unread count, and DEV and RESEARCH
   are refused by the hook — test it, don't assert it.
9. The Docs tab reads like a manual I could hand someone else — it describes what this
   machine actually has, not what was planned, and it matches the design.
10. The crew does not sound like one person: play each agent's greeting back to back and
   confirm four distinguishable voices, a female voice for ASSISTANT, and a level that does
   not jump between them. Listen to the words too — each agent must SAY its name, not spell
   it out letter by letter.

For anything that fails: what is broken, and what it would take to fix — in one line each.
Then stamp the version to v1.0, take a final backup ("v1.0 — verified"), and give me one
paragraph describing what I now have — written for me, not for a changelog.
```

## Prompt 30

### Prompt 44 — Home Assistant

```
Install Home Assistant on this server with a default configuration, as the smart home brain
JARVIS will talk to.

Before anything: back up any files you will touch, and tell me your plan in two sentences
before you run it.

Rules: use the official Home Assistant container image if Docker is available, and install
Docker first if it is not. If this machine cannot run Docker at all, fall back to Home
Assistant Core in its own Python environment and say so before you start. The web interface
must listen on 127.0.0.1:8123 ONLY, never on a public address: this server faces the
internet, and a fresh Home Assistant must not. Set it up as a service that starts on boot
and restarts if it crashes, keep its configuration in a homeassistant folder next to my
other services, and leave everything else at Home Assistant defaults.

When it runs: verify it survives a service restart, tell me the exact command to restart it
myself, and give me the one address to open from my own devices over the tailnet, or an SSH
tunnel command if there is no tailnet, so I can create my account and finish onboarding in
the browser myself. Do not create the account for me. Finish with proof: the service status,
the listening address showing 127.0.0.1:8123, and nothing new listening on the public
interface.
```

## Prompt T1

### Prompt 45 — A Topic Answers as the Wrong Agent

```
One of my Telegram topics is answering with the wrong identity — I asked the agent in the
[TOPIC NAME] topic who it was and it answered as [WHAT IT SAID].

Find the root cause rather than patching over it. In order:
1. Does the thread ID in the routing configuration match the ID that topic actually reports?
   (Ask in the topic again if you need it fresh — IDs do not change, but transposed digits are
   the number-one cause.)
2. Does the profile that topic routes to actually exist on disk, spelled exactly that way?
3. Was the gateway restarted after the routing last changed? A routing file the gateway has
   never re-read does not exist as far as messages are concerned.

Tell me WHICH of those it was before you fix it. Then fix it, restart what needs restarting,
and re-test ALL FOUR topics — not just the broken one — reporting each answer verbatim.
```

## Prompt T2

### Prompt 46 — The Agent Says a Service Is Not Connected

```
[AGENT] told me it cannot reach [SERVICE], but I know it is connected.

Before you believe the agent, check how it actually reaches that service on this machine — a
command, a tool, an integration. An agent looking for a tool that does not exist will correctly
report that it has nothing, and be completely wrong about the reason: the connection is fine
and the agent simply was never given the way in.

Also check whether the agent is answering from a LIVE SESSION that predates the change. A
running session keeps the instructions it started with — a tool added this morning does not
exist in a conversation that started last night. Test in a fresh session before concluding
anything.

If it is Composio-backed, also run the connections list: a connection that shows EXPIRED needs
its link step rerun in my browser — that is Google expiring it, not the agent failing.

Tell me which of those it was, show me the service answering (or the honest reason it cannot),
and if the fix was "fresh session", say so — that one is nobody's bug.
```

## Prompt T3

### Prompt 47 — Something Looks Broken After an Edit

```
[DESCRIBE WHAT LOOKS WRONG — e.g. "the crew faces never dim when one is selected"].

Do not guess, and do not start editing CSS. MEASURE first: get the element's real position and
size in the browser, and its computed style for the property that looks wrong, and tell me the
actual numbers before you change anything.

Two causes account for most of these, and each has a signature:
- A FINISHED CSS ANIMATION with a fill mode keeps hold of every property it animated — forever.
  A plain rule that later tries to set the same property loses silently. If a colour, opacity
  or filter refuses to apply and the element was ever animated, check what the animation ends
  on: the fix is to stop the animation pinning that property, not to pile on !important.
- TWO RULES OF EQUAL SPECIFICITY: the later one in the file wins, wherever it sits. A media
  query placed BEFORE the rule it is meant to override does nothing at all, and it fails
  silently. If a responsive override is being ignored, check what comes after it.

Find which it is, tell me, fix that — then show me the same measurement again, now correct, and
restore anything your backup shows you touched by accident.
```

## Prompt T4

### Prompt 48 — The Dashboard Shows Nothing

```
The dashboard loads but every figure is a dash and nothing is populated.

Work from the outside in, one layer at a time, and tell me which layer is broken BEFORE you
touch anything:

1. Is the server process actually running, and is something listening on 127.0.0.1:8899?
2. Does GET /api/state return real JSON when you request it directly on the machine — not
   through the page?
3. Does the browser console show errors? A single thrown error early in the page's script can
   stop every later render while the page still LOOKS fine — read the first error, not the
   loudest one.
4. Is the page actually reaching the endpoint? Check the network tab: request made, status
   200, response non-empty.
5. And the one specific to this build: is window.__TEMPLATE__ undefined on /? If it is true,
   the template's network shim was never cut — the page is answering itself from the
   baked-in demo snapshot and will never show real data no matter how perfect the server is.

Fix the broken layer, then show me the raw /api/state JSON alongside the working page — both,
so I can see they agree.
```
