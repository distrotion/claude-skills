#!/usr/bin/env python3
"""Regenerate the skill reference (SKILLS.md + skills.html) from the SKILL.md files.

Source of truth = ~/.claude/skills/*/SKILL.md frontmatter. Run this after adding,
renaming, or editing any skill, then redeploy the artifact to refresh the bookmark.
The page keeps the reader's pins and custom groups in their browser (localStorage),
so regenerating never wipes them.
"""
import datetime
import html
import json
import pathlib
import re

HOME = pathlib.Path.home()
SKILLS_DIR = HOME / ".claude" / "skills"
OUT_MD = HOME / ".claude" / "SKILLS.md"
OUT_HTML = HOME / ".claude" / "skills.html"

# Default group order = how the work actually flows, not alphabetical.
GROUPS = [
    ("Ship a unit", "build, test on the machine, push — the daily plant workflow",
     ["localtest", "localtest-end", "buildup", "pushcode", "envlocal", "new-unit"]),
    ("Hold the standard", "audit code against the central standard, then fix it",
     ["gen-flutter-std", "gen-nodejs-std", "gen-flutter-nodejs-std", "check-code-std", "convert-to-std"]),
    ("How Claude answers", "reply length and working discipline",
     ["terse", "caveman", "stop-slop"]),
    ("Manage the setup", "what Claude remembers, what is running, what tools exist",
     ["claude-mem", "task-observer", "find-skill", "dohandoff"]),
]

# Real sequences worth drawing as a chain (order carries meaning).
CHAINS = {
    "Ship a unit": ["localtest", "localtest-end", "buildup"],
    "Hold the standard": ["check-code-std", "convert-to-std"],
}


def parse_skill(path: pathlib.Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    fm = text.split("---", 2)[1]
    name = re.search(r"^name:\s*(.+)$", fm, re.M)
    folded = re.search(r"^description:\s*>-\s*\n((?:[ \t]+.*\n?)+)", fm, re.M)
    if folded:
        body = " ".join(line.strip() for line in folded.group(1).splitlines())
    else:
        plain = re.search(r"^description:\s*(.+)$", fm, re.M)
        body = plain.group(1) if plain else ""
    body = re.sub(r"\s+", " ", body).strip()
    triggers = [t for t in re.findall(r'"([^"]+)"', body) if t.lower() != "skill"]
    summary = re.split(r"\s*Trigger:|\s*Toggle:", body)[0].strip().rstrip(".")
    return {"name": name.group(1).strip() if name else path.parent.name,
            "summary": summary, "triggers": triggers}


def est_tokens(text: str) -> int:
    thai = sum(1 for c in text if 0x0E00 <= ord(c) <= 0x0E7F)
    return int(thai + (len(text) - thai) * 0.25)


def collect():
    found, total = {}, 0
    for p in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        s = parse_skill(p)
        if s:
            found[s["name"]] = s
            total += est_tokens(s["summary"] + " ".join(s["triggers"]))
    ordered, seen = [], set()
    for title, blurb, names in GROUPS:
        rows = [found[n] for n in names if n in found]
        seen.update(n for n in names if n in found)
        if rows:
            ordered.append({"title": title, "blurb": blurb, "chain": CHAINS.get(title, []),
                            "skills": rows})
    rest = [s for n, s in found.items() if n not in seen]
    if rest:
        ordered.append({"title": "Not grouped yet",
                        "blurb": "newly added — sort it into a group once its use settles",
                        "chain": [], "skills": rest})
    return ordered, total


def write_md(groups, total, count):
    out = ["# Skills — command reference", "",
           f"{count} skills installed · about {total} tokens of descriptions load at the start "
           "of every session.", "",
           "Generated from `~/.claude/skills/*/SKILL.md` by `skills-doc.py` — edit a skill, "
           "then re-run the script.", ""]
    for g in groups:
        out += [f"## {g['title']}", "", f"_{g['blurb']}_", ""]
        if g["chain"]:
            out += ["`" + "` → `".join(g["chain"]) + "`", ""]
        for s in g["skills"]:
            trig = " · ".join(f"`{t}`" for t in s["triggers"][:5]) or "—"
            out += [f"### {s['name']}", "", s["summary"], "", f"Say: {trig}", ""]
    OUT_MD.write_text("\n".join(out), encoding="utf-8")


CSS = """
:root{
  --ink:#1D2733; --ink-soft:#5A6675; --ink-faint:#8794A3;
  --ground:#EDF0F4; --surface:#FFFFFF; --line:#DCE2EA; --line-soft:#E9EDF2;
  --accent:#1E6FD9; --accent-soft:#EAF0FE; --pin:#D69E2E;
  --shadow:0 1px 2px rgba(18,32,48,.06), 0 8px 24px -16px rgba(18,32,48,.25);
  --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,monospace;
  --sans:system-ui,-apple-system,"Segoe UI",sans-serif;
}
@media (prefers-color-scheme:dark){
  :root{
    --ink:#E5EAF0; --ink-soft:#9AA7B6; --ink-faint:#6C7A8A;
    --ground:#0E141B; --surface:#161E27; --line:#26313D; --line-soft:#1E2731;
    --accent:#6BA5F5; --accent-soft:#17253A; --pin:#E0B457;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px -18px rgba(0,0,0,.8);
  }
}
:root[data-theme="dark"]{
  --ink:#E5EAF0; --ink-soft:#9AA7B6; --ink-faint:#6C7A8A;
  --ground:#0E141B; --surface:#161E27; --line:#26313D; --line-soft:#1E2731;
  --accent:#6BA5F5; --accent-soft:#17253A; --pin:#E0B457;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 10px 28px -18px rgba(0,0,0,.8);
}
:root[data-theme="light"]{
  --ink:#1D2733; --ink-soft:#5A6675; --ink-faint:#8794A3;
  --ground:#EDF0F4; --surface:#FFFFFF; --line:#DCE2EA; --line-soft:#E9EDF2;
  --accent:#1E6FD9; --accent-soft:#EAF0FE; --pin:#D69E2E;
  --shadow:0 1px 2px rgba(18,32,48,.06), 0 8px 24px -16px rgba(18,32,48,.25);
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.55;-webkit-font-smoothing:antialiased}
.wrap{max-width:1080px;margin:0 auto;padding:40px 24px 96px;display:flex;flex-direction:column;gap:30px}

.masthead{display:flex;flex-wrap:wrap;align-items:flex-end;gap:20px;
  border-bottom:2px solid var(--ink);padding-bottom:18px}
.masthead h1{margin:0;font-size:clamp(26px,4vw,38px);font-weight:680;letter-spacing:-.022em;
  text-wrap:balance;flex:1 1 320px}
.masthead .sub{color:var(--ink-soft);font-size:13.5px;max-width:42ch}
.stamp{font-family:var(--mono);font-size:11px;letter-spacing:.09em;text-transform:uppercase;
  color:var(--ink-faint)}

.gauges{display:grid;grid-template-columns:repeat(auto-fit,minmax(146px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);border-radius:10px;overflow:hidden}
.gauge{background:var(--surface);padding:14px 16px;display:flex;flex-direction:column;gap:3px}
.gauge b{font-size:22px;font-weight:660;letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.gauge span{font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-faint);
  font-family:var(--mono)}

.tools{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
#q{flex:1 1 240px;min-width:0;padding:11px 14px;border:1px solid var(--line);border-radius:9px;
  background:var(--surface);color:var(--ink);font:inherit;font-size:14px}
#q::placeholder{color:var(--ink-faint)}
select,button.ghost{padding:10px 12px;border:1px solid var(--line);border-radius:9px;
  background:var(--surface);color:var(--ink);font:inherit;font-size:13px;cursor:pointer}
.count{font-family:var(--mono);font-size:12px;color:var(--ink-faint);font-variant-numeric:tabular-nums;
  margin-left:auto}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}

.group{display:flex;flex-direction:column;gap:12px}
.group-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 14px}
.group-head h2{margin:0;font-size:13px;font-weight:640;letter-spacing:.1em;text-transform:uppercase}
.group-head p{margin:0;color:var(--ink-soft);font-size:13px}
.chain{display:flex;flex-wrap:wrap;align-items:center;gap:7px;font-family:var(--mono);font-size:11.5px;
  color:var(--ink-soft);background:var(--accent-soft);border:1px solid var(--line);
  border-radius:999px;padding:5px 12px;width:fit-content}
.chain i{font-style:normal;color:var(--accent)}

.rows{display:flex;flex-direction:column;gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:11px;overflow:hidden;box-shadow:var(--shadow)}
.row{background:var(--surface);padding:14px 16px;display:grid;
  grid-template-columns:28px minmax(150px,210px) 1fr auto;gap:4px 16px;align-items:start}
.row:hover{background:var(--accent-soft)}
.pin{grid-row:span 2;border:0;background:none;cursor:pointer;font-size:15px;line-height:1;
  padding:2px;color:var(--ink-faint);border-radius:6px}
.pin[aria-pressed="true"]{color:var(--pin)}
.name{font-family:var(--mono);font-size:13.5px;font-weight:600;color:var(--accent);word-break:break-word}
.what{color:var(--ink-soft);font-size:13.5px;margin:0}
.move{font-family:var(--mono);font-size:11px;color:var(--ink-faint);max-width:150px}
.say{grid-column:3 / -1;display:flex;flex-wrap:wrap;gap:6px;margin-top:5px}
.say code{font-family:var(--mono);font-size:11.5px;background:var(--ground);color:var(--ink-soft);
  border:1px solid var(--line-soft);border-radius:6px;padding:2.5px 8px;white-space:nowrap;cursor:copy}
.say code:hover{border-color:var(--accent);color:var(--accent)}

.foot{border-top:1px solid var(--line);padding-top:16px;color:var(--ink-faint);font-size:12.5px;
  display:flex;flex-wrap:wrap;gap:6px 18px}
.foot code{font-family:var(--mono);font-size:12px;color:var(--ink-soft)}
.empty{background:var(--surface);border:1px dashed var(--line);border-radius:11px;padding:26px;
  text-align:center;color:var(--ink-faint);font-size:13.5px}
.toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);background:var(--ink);
  color:var(--ground);font-family:var(--mono);font-size:12px;padding:8px 14px;border-radius:8px;
  opacity:0;pointer-events:none}
.toast.on{opacity:1}
@media (max-width:660px){
  .row{grid-template-columns:26px 1fr;gap:4px 12px}
  .what,.say{grid-column:2 / -1}
  .move{grid-column:2 / -1;max-width:none;margin-top:6px}
}
@media (prefers-reduced-motion:no-preference){
  .row{transition:background .12s ease}
  .toast{transition:opacity .18s ease}
}
"""

JS = r"""
const KEY = 'skills-doc-v1';
const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } };
let state = load();
state.pinned = state.pinned || [];
state.custom = state.custom || {};      // skill name -> custom group name
state.mode   = state.mode   || 'flow';  // flow | custom | az
const save = () => localStorage.setItem(KEY, JSON.stringify(state));

const app = document.getElementById('app');
const q = document.getElementById('q');
const modeSel = document.getElementById('mode');
const counter = document.getElementById('count');
const toastEl = document.getElementById('toast');
modeSel.value = state.mode;

const all = DATA.flatMap(g => g.skills.map(s => ({ ...s, home: g.title })));
const groupNames = () => [...new Set([...DATA.map(g => g.title), ...Object.values(state.custom)])];

function toast(msg){
  toastEl.textContent = msg; toastEl.classList.add('on');
  clearTimeout(toast.t); toast.t = setTimeout(() => toastEl.classList.remove('on'), 1400);
}

function buildSections(){
  const term = q.value.trim().toLowerCase();
  const match = s => !term || (s.name + ' ' + s.summary + ' ' + s.triggers.join(' ')).toLowerCase().includes(term);
  const visible = all.filter(match);
  const pinned = visible.filter(s => state.pinned.includes(s.name));
  const rest = visible.filter(s => !state.pinned.includes(s.name));
  const out = [];
  if (pinned.length) out.push({ title: 'Pinned', blurb: 'your shortlist — click the star to remove', chain: [], skills: pinned });

  if (state.mode === 'az'){
    out.push({ title: 'A–Z', blurb: 'every skill, alphabetical', chain: [],
               skills: [...rest].sort((a,b) => a.name.localeCompare(b.name)) });
  } else if (state.mode === 'custom'){
    const buckets = {};
    rest.forEach(s => { const g = state.custom[s.name] || 'Unsorted'; (buckets[g] = buckets[g] || []).push(s); });
    Object.keys(buckets).sort().forEach(t => out.push({ title: t, blurb: 'your grouping', chain: [], skills: buckets[t] }));
  } else {
    DATA.forEach(g => {
      const skills = rest.filter(s => s.home === g.title);
      if (skills.length) out.push({ ...g, skills });
    });
  }
  counter.textContent = visible.length + (visible.length === 1 ? ' skill' : ' skills');
  return out;
}

function render(){
  const sections = buildSections();
  app.innerHTML = '';
  if (!sections.length){
    app.innerHTML = '<div class="empty">No skill matches that. Say <code>find skill</code> in chat and Claude will look further.</div>';
    return;
  }
  const names = groupNames();
  sections.forEach(sec => {
    const el = document.createElement('section');
    el.className = 'group';
    const chain = sec.chain && sec.chain.length
      ? `<div class="chain">${sec.chain.map(c => c).join(' <i>&rarr;</i> ')}</div>` : '';
    el.innerHTML = `<div class="group-head"><h2>${esc(sec.title)}</h2><p>${esc(sec.blurb)}</p></div>${chain}
      <div class="rows"></div>`;
    const rows = el.querySelector('.rows');
    sec.skills.forEach(s => {
      const on = state.pinned.includes(s.name);
      const row = document.createElement('article');
      row.className = 'row';
      row.innerHTML = `
        <button class="pin" aria-pressed="${on}" title="${on ? 'Unpin' : 'Pin to top'}">${on ? '★' : '☆'}</button>
        <div class="name">${esc(s.name)}</div>
        <p class="what">${esc(s.summary)}</p>
        <select class="move" title="Move to a group">
          ${names.map(n => `<option${(state.custom[s.name] || s.home) === n ? ' selected' : ''}>${esc(n)}</option>`).join('')}
          <option value="__new">+ new group…</option>
        </select>
        <div class="say">${s.triggers.slice(0,6).map(t => `<code title="Click to copy">${esc(t)}</code>`).join('')}</div>`;
      row.querySelector('.pin').onclick = () => {
        state.pinned = on ? state.pinned.filter(n => n !== s.name) : [...state.pinned, s.name];
        save(); render(); toast(on ? 'Unpinned ' + s.name : 'Pinned ' + s.name);
      };
      row.querySelector('.move').onchange = e => {
        let g = e.target.value;
        if (g === '__new'){
          g = (prompt('New group name') || '').trim();
          if (!g){ render(); return; }
        }
        state.custom[s.name] = g; state.mode = 'custom'; modeSel.value = 'custom';
        save(); render(); toast(s.name + ' → ' + g);
      };
      row.querySelectorAll('.say code').forEach(c => {
        c.onclick = () => { navigator.clipboard?.writeText(c.textContent); toast('Copied: ' + c.textContent); };
      });
      rows.appendChild(row);
    });
    app.appendChild(el);
  });
}

function esc(t){ return String(t).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m])); }

q.addEventListener('input', render);
modeSel.addEventListener('change', () => { state.mode = modeSel.value; save(); render(); });
document.getElementById('reset').onclick = () => {
  if (!confirm('Clear your pins and custom groups?')) return;
  state = { pinned: [], custom: {}, mode: 'flow' }; modeSel.value = 'flow'; save(); render(); toast('Reset');
};
render();
"""


def write_html(groups, total, count, stamp):
    data = json.dumps(groups, ensure_ascii=False)
    parts = [
        "<title>Skills — command reference</title>",
        f"<style>{CSS}</style>",
        '<div class="wrap">',
        '<header class="masthead">',
        "<h1>Skills — command reference</h1>",
        '<div class="sub">Everything Claude can run on this Mac, and the words that start it. '
        "Type the phrase in chat — no slash needed.</div>",
        f'<div class="stamp">generated {stamp}</div>',
        "</header>",
        '<section class="gauges">',
        f'<div class="gauge"><b>{count}</b><span>skills installed</span></div>',
        f'<div class="gauge"><b>{total}</b><span>tokens per session</span></div>',
        f'<div class="gauge"><b>{len(groups)}</b><span>default groups</span></div>',
        '<div class="gauge"><b>pin</b><span>saved in this browser</span></div>',
        "</section>",
        '<div class="tools">',
        '<input id="q" type="search" placeholder="Filter by name, purpose, or trigger phrase…" aria-label="Filter skills">',
        '<select id="mode" aria-label="Grouping"><option value="flow">Group: workflow</option>'
        '<option value="custom">Group: mine</option><option value="az">Group: A–Z</option></select>',
        '<button class="ghost" id="reset" type="button">Reset</button>',
        f'<span class="count" id="count">{count} skills</span>',
        "</div>",
        '<main id="app"></main>',
        '<footer class="foot">',
        "<span>Source of truth: <code>~/.claude/skills/*/SKILL.md</code></span>",
        "<span>Rebuild: <code>python3 ~/.claude/skills-doc.py</code></span>",
        "<span>Pins and groups stay in this browser</span>",
        "</footer></div>",
        '<div class="toast" id="toast" role="status"></div>',
        f"<script>const DATA={data};{JS}</script>",
    ]
    OUT_HTML.write_text("\n".join(parts), encoding="utf-8")


def main():
    groups, total = collect()
    count = sum(len(g["skills"]) for g in groups)
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    write_md(groups, total, count)
    write_html(groups, total, count, stamp)
    print(f"{count} skills · ~{total} tokens/session")
    print(f"wrote {OUT_MD}\nwrote {OUT_HTML}")


if __name__ == "__main__":
    main()
