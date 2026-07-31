# Skills — command reference

21 skills installed · about 1548 tokens of descriptions load at the start of every session.

Generated from `~/.claude/skills/*/SKILL.md` by `skills-doc.py` — edit a skill, then re-run the script.

## งานประจำวัน — ส่งขึ้นจริง

_บิลด์ · ทดสอบบนเครื่อง · push ขึ้น git_

`localtest` → `localtest-end` → `buildup`

### localtest

รันทั้งระบบบนเครื่องแบบ production (built asset จริง) ก่อน deploy

Say: `localtest <unit>` · `โลคอลเทส` · `ทดสอบก่อนขึ้นจริง` · `รัน built front + backend บนเครื่อง`

### localtest-end

ปิด localtest ให้สะอาด คืนพอร์ต + คืน config UI ที่ชี้ localhost

Say: `localtest-end` · `ปิด/หยุด/จบ localtest` · `เลิกเทสแล้ว`

### buildup

บิลด์ Flutter web แล้ว deploy ขึ้น repo DEPLOY + push ทั้ง 2 git

Say: `buildup <unit>` · `buildup all` · `บิลด์อัพ` · `อัพขึ้นจริง`

### pushcode

commit + push โค้ดต้นทางอย่างปลอดภัย กัน secret/build หลุด

Say: `push code` · `push ขึ้น git` · `ดันโค้ดขึ้น` · `commit แล้ว push`

### envlocal

ดูตารางว่า endpoint ไหนชี้ localhost / ชี้ server จริง แล้วปรับได้

Say: `envlocal` · `ดู .env.local` · `config endpoint ชี้ไปไหน` · `ปรับ env local`

### new-unit

สร้าง plant ใหม่จาก clone เปลี่ยน port/IP/ชื่อครบ + grep ค่าเก่าเหลือ 0

Say: `new unit` · `สร้าง plant ใหม่` · `clone unit ... เป็น ...` · `เพิ่มหน่วยงานใหม่`

## มาตรฐานโค้ด

_ตรวจโค้ดเทียบมาตรฐานกลาง แล้วแก้ให้ผ่าน_

`check-code-std` → `convert-to-std`

### gen-flutter-std

ตรวจ performance ฝั่ง Flutter ตามเกณฑ์ FL- ออกรายงาน PASS/WARN/FAIL

Say: `gen flutter std` · `ตรวจ flutter std` · `audit flutter performance`

### gen-nodejs-std

ตรวจ performance ฝั่ง Node ตามเกณฑ์ ND-

Say: `gen nodejs std` · `ตรวจ node std` · `audit backend performance`

### gen-flutter-nodejs-std

ตรวจทั้งระบบ FL-+ND-+FS- และเทียบ reference app T1–T5

Say: `gen flutter+nodejs std` · `ตรวจ fullstack std` · `audit ระบบทั้ง front+back`

### check-code-std

audit 5 มิติ (โครง/perf/noti-login/security/cross-check) แล้ววางแผนแก้

Say: `check code std` · `ตรวจโค้ดตามมาตรฐาน` · `audit code std` · `เช็คโค้ดเทียบ std แล้ววางแผน`

### secupy

ปิดช่อง broken access control — endpoint ไม่มี auth, สิทธิ์ตัดสินฝั่ง UI, ไม่ส่ง token (แก้แบบไม่ทำระบบล่ม)

Say: `secupy` · `ปิดช่อง security` · `endpoint ไม่มี auth` · `แก้ security` · `client-side auth`

### convert-to-std

ลงมือแก้โค้ดจริงให้ผ่านเกณฑ์ นำร่องทีละ unit + localtest ก่อนขยาย

Say: `convert to std` · `แก้ให้ผ่าน std` · `fix ตามมาตรฐาน performance`

## วิธีที่ Claude ตอบ

_ความยาวคำตอบ และวินัยการทำงาน_

### terse

สลับโหมดตอบสั้น ประหยัด token ~40-50% ต่อคำตอบ

Say: `terse on` · `terse off` · `terse` · `ตอบสั้น` · `เปิดโหมดสั้น`

### caveman

โหมดมนุษย์ถ้ำ ตอบสั้นสุด ประหยัด ~60-70%

Say: `file big. me fix. test pass.` · `caveman on` · `caveman off` · `caveman` · `โหมดมนุษย์ถ้ำ`

### stop-slop

กันงานมโน/ฟุ่มเฟือย + กันงานบานปลายเกินที่สั่ง

Say: `stop slop` · `stop slope` · `no slop` · `อย่าบานปลาย` · `ทำเฉพาะที่สั่ง`

## จัดการระบบ

_ความจำ · งานเบื้องหลัง · เครื่องมือที่มี_

### newsession

ล้าง context ในหน้าต่างเดิม — เก็บ handoff ให้ก่อน แล้วสั่ง /clear ต่องานได้เลย

Say: `newsession` · `เริ่มใหม่` · `ล้าง context` · `reset session` · `รีเซ็ต`

### claude-mem

ดู/จัดการสิ่งที่ Claude จำไว้ + บอกว่ากิน token เท่าไรต่อ session

Say: `claude mem` · `ดู memory` · `จำอะไรไว้บ้าง` · `ล้าง memory` · `เพิ่ม memory`

### task-observer

ดูงานเบื้องหลังทั้งหมดที่รันอยู่ + ตัวไหนค้าง

Say: `task observer` · `งานที่รันอยู่` · `เช็คงานเบื้องหลัง` · `workflow ถึงไหนแล้ว` · `อะไรค้างอยู่`

### find-skill

หา skill ที่ตรงกับงาน ในเครื่องก่อน แล้วค่อยหาใน marketplace

Say: `find skill` · `หา skill` · `มี skill อะไรบ้าง` · `skill ไหนใช้ดี` · `skill for ...`

### dohandoff

สรุป session เป็นเอกสารส่งต่อ ให้คน/AI อ่านแล้วทำต่อได้

Say: `dohandoff` · `ทำ handoff` · `สรุปส่งต่องาน` · `เขียน doc ให้คนอื่นทำต่อ`

## ยังไม่จัดกลุ่ม

_เพิ่งเพิ่มเข้ามา — จัดกลุ่มเมื่อรู้ว่าใช้ยังไง_

### localtest-s

localtest variant where the backend keeps pointing at the DB on the server (no local DB, no editing the mongo/mssql helpers)

Say: `localtest-s <unit>` · `localtest -s` · `โลคอลเทสแบบ DB server` · `เทสแต่ใช้ DB บนเซิร์ฟเวอร์`
