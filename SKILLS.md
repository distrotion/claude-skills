# Skills — command reference

18 skills installed · about 1242 tokens of descriptions load at the start of every session.

Generated from `~/.claude/skills/*/SKILL.md` by `skills-doc.py` — edit a skill, then re-run the script.

## Ship a unit

_build, test on the machine, push — the daily plant workflow_

`localtest` → `localtest-end` → `buildup`

### localtest

Run the whole system (Node backend + built Flutter web) on the machine like production before deploy (real built asset, not debug/hot-reload)

Say: `localtest <unit>` · `โลคอลเทส` · `ทดสอบก่อนขึ้นจริง` · `รัน built front + backend บนเครื่อง`

### localtest-end

Close a running localtest — kill backend+front, free the ports, restore UI config that points at localhost back to the real server. The closing counterpart of localtest

Say: `localtest-end` · `ปิด/หยุด/จบ localtest` · `เลิกเทสแล้ว`

### buildup

Deploy pipeline for Flutter web + Node: build → deploy into the DEPLOY repo → push 2 gits

Say: `buildup <unit>` · `buildup all` · `บิลด์อัพ` · `อัพขึ้นจริง`

### pushcode

Commit + push source code to git safely (prevent secret/.env/build/node_modules leaks, verb-first message, pull --rebase before push). Separate from buildup (which pushes only DEPLOY)

Say: `push code` · `push ขึ้น git` · `ดันโค้ดขึ้น` · `commit แล้ว push`

### envlocal

View/adjust `.env.local` + endpoint config as a table (each endpoint points to localhost or the real server) before/during localtest

Say: `envlocal` · `ดู .env.local` · `config endpoint ชี้ไปไหน` · `ปรับ env local`

### new-unit

Create a new unit/plant from a clone (backend+UI+deploy), change all port/IP/names + grep old values down to 0 + add to the buildup/localtest table

Say: `new unit` · `สร้าง plant ใหม่` · `clone unit ... เป็น ...` · `เพิ่มหน่วยงานใหม่`

## Hold the standard

_audit code against the central standard, then fix it_

`check-code-std` → `convert-to-std`

### gen-flutter-std

Check Flutter performance against the FL- section in PERFORMANCE-STANDARD.md → report PASS/WARN/FAIL. Check only, no code changes

Say: `gen flutter std` · `ตรวจ flutter std` · `audit flutter performance`

### gen-nodejs-std

Check Node/Express backend performance against the ND- section → report PASS/WARN/FAIL. Check only, no code changes

Say: `gen nodejs std` · `ตรวจ node std` · `audit backend performance`

### gen-flutter-nodejs-std

Check fullstack performance (Flutter+Node) against FL-/ND-/FS- + the connection points + reference app T1–T5. Check/produce a spec, no code changes

Say: `gen flutter+nodejs std` · `ตรวจ fullstack std` · `audit ระบบทั้ง front+back`

### check-code-std

Audit code against the central standards (framework std + perf FL-/ND-/FS- + noti/login + security) and plan the fixes, before handing off to convert-to-std. Check + plan only, no code changes

Say: `check code std` · `ตรวจโค้ดตามมาตรฐาน` · `audit code std` · `เช็คโค้ดเทียบ std แล้ววางแผน`

### convert-to-std

Actually change code to pass the performance standard (the FAIL items from gen ... std) — pilot one unit at a time + localtest before propagating. Unlike gen ... std, which only checks

Say: `convert to std` · `แก้ให้ผ่าน std` · `fix ตามมาตรฐาน performance`

## How Claude answers

_reply length and working discipline_

### terse

Turn terse reply mode ON or OFF (short, low-token replies — no tables/decoration, still correct grammar)

Say: `terse on` · `terse off` · `terse` · `ตอบสั้น` · `เปิดโหมดสั้น`

### caveman

Turn caveman reply mode ON or OFF — ultra-short caveman speech to cut output tokens hard ("file big. me fix. test pass.")

Say: `file big. me fix. test pass.` · `caveman on` · `caveman off` · `caveman` · `โหมดมนุษย์ถ้ำ`

### stop-slop

Guard against AI slop and scope creep in one pass: cut filler/over-engineering/invented abstractions, and refuse work outside what was asked

Say: `stop slop` · `stop slope` · `no slop` · `อย่าบานปลาย` · `ทำเฉพาะที่สั่ง`

## Manage the setup

_what Claude remembers, what is running, what tools exist_

### claude-mem

Inspect and manage what Claude loads every session — memory files, MEMORY.md index, CLAUDE.md — with a size/token report, plus add, prune, consolidate

Say: `claude mem` · `ดู memory` · `จำอะไรไว้บ้าง` · `ล้าง memory` · `เพิ่ม memory`

### task-observer

Show what background work is running right now — subagents, workflows, background shell tasks, monitors — with status, elapsed time, and what is stuck

Say: `task observer` · `งานที่รันอยู่` · `เช็คงานเบื้องหลัง` · `workflow ถึงไหนแล้ว` · `อะไรค้างอยู่`

### find-skill

Find the right skill for a job — search installed skills first, then marketplaces, and say plainly if none fits (and whether to build one)

Say: `find skill` · `หา skill` · `มี skill อะไรบ้าง` · `skill ไหนใช้ดี` · `skill for ...`

### dohandoff

Summarize a session into a handoff document (what was done, design rationale, status, how to continue) so a person/AI can take over

Say: `dohandoff` · `ทำ handoff` · `สรุปส่งต่องาน` · `เขียน doc ให้คนอื่นทำต่อ`
