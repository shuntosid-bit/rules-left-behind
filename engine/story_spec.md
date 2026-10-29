You write one ORIGINAL episode for the YouTube channel "Rules Left Behind": animated survival mysteries, 8-10 minutes, English, narrated in SECOND PERSON, PRESENT TENSE ("You open the door.").

FORMAT RULES (every episode)
- Someone left rules/notes behind for the place the viewer ("you") is in. The rules are discovered, followed, questioned, and finally reinterpreted.
- Hook within the first 2 sentences: an ordinary situation with one disturbing detail, plus the stakes (distance, time, isolation).
- 4-6 numbered problems with title cards ("PROBLEM 1" sub "THE COLD"), each solved with REAL, safe, logical survival reasoning and at least one concrete number.
- At least 3 fair clues and foreshadowing; a twist that is surprising but physically/logically explained and makes the viewer reinterpret earlier scenes. Prefer realistic explanations over supernatural ones.
- Optional one supporting voice heard over radio/phone/intercom (voice "R"), max 8 lines total.
- Satisfying ending where "you" survive; final beat: new rules written for the next person.
- Calm, restrained tone. Short sentences. No gore, no real people/brands, no dangerous how-to instructions, nothing sexual, suitable for teens.
- Do NOT reuse premises from previous episodes:
{PAST}
- Do NOT copy "Nobody Gets In" (no zombie outbreaks, no "30 days locked in a supermarket/school" sieges).

LENGTH: 1150-1450 narration words total, 95-140 segments. One segment = one or two sentences (one shot).

OUTPUT: JSON only, this schema:
{
 "title": "YouTube title, <=90 chars, curiosity + stakes",
 "premise": "one-sentence summary incl. setting and twist",
 "description": "YouTube description, 2-4 sentences, no spoilers of the twist",
 "tags": ["8-12 tags"],
 "short": {"ranges": [[startSeg,endSeg],[startSeg,endSeg]], "hook": "<=5 words, ALL CAPS", "title": "Shorts title <=80 chars", "description": "1-2 sentences, no twist spoiler"},
 "segments": [ {
   "voice": "N" | "R" | "C",             // C = full-screen title card (no narration)
   "text": "narration line (for C: card title, e.g. PROBLEM 2)",
   "sub": "card subtitle (C only)", "dur": 2.0,   // C only
   "shot": {...},                         // required for N and R
   "move": "zin|zout|zin_fast|zin_slow|pl|pr|pu|pd|still|shake",
   "hud": "DAY 3 · 03:07" (optional, when time/day changes),
   "cap": "short keyword caption, max 4 words, only for key numbers (optional, rare)",
   "sfx": "knock3|wind|click|static_long|gen|stall|gen_off|alarm|heli|door|shovel|hit|pencil|steps" (optional, "@1.2" offset allowed),
   "pause": 0.35 (optional; 0.8-1.2 after dramatic lines)
 } ]
}
"short.ranges": two ranges of segment indexes (each 3-6 segments): the hook (starting at 0) and one suspense moment BEFORE the twist; total under 45 seconds of narration. Never reveal the twist in the Short.

SHOT KINDS (visual vocabulary; vary them, change the visual every 1-2 segments, reuse identical shots for callbacks):
- {"kind":"exterior","setting":"mountain|forest|coast|desert|city|field","time":"night|day|dusk","weather":"clear|snow|rain|storm|fog","building":"hut|tower|house|none","lit":true,"figure":{"pose":"stand|walk|point|arms_up|reach","expr":"neutral|worried|scared|relief|smile|focused"}}
- {"kind":"interior","light":"dark|dim|day","props":[up to 4 of: {PROPS}],"figure":{"pose":"stand|walk|sit|point|hold_head|arms_up|crouch|reach","expr":"neutral|worried|scared|pain|tired|relief|smile|focused","x":300-1650,"who":"you|ally|stranger"},"effect":"knock|none"}
- {"kind":"character","bg":"dark|day|red","figure":{"pose":"...","expr":"...","who":"you|ally|stranger"}}
- {"kind":"closeup","object":"clock|door|device|radio|phone|sign","text":"03:07 / 280 PPM / short text <=12 chars","label":"device label <=20 chars","state":"normal|alarm|off","effect":"knock|ring|none","lines":["for sign: up to 4 short lines"]}
- {"kind":"page","title":"RULES","lines":["1. Keep the door shut at night.", "..."],"style":"hand|neat","hole":false}   // the left-behind rules; max 6 lines, <=44 chars each
- {"kind":"info","type":"equation","a":"400 L","op":"÷ 12 L A DAY","result":"33 DAYS"}
- {"kind":"info","type":"bars","title":"COLDEST NIGHTS","items":[{"label":"NIGHT 3","value":-27,"highlight":true}]}
- {"kind":"info","type":"flow","title":"WHAT CO DOES","items":["HEADACHE","CONFUSION","SLEEP"]}
- {"kind":"info","type":"map","title":"THE STATION","rooms":["BUNK","RADIO","GENERATOR"],"path_label":"ROPE LINE — 40 M","target":"instruments"}
Add "tint":"red" to any shot spec to show it as a red-tinted reprise during the twist reveal.
"you" always looks the same (round head, yellow beanie, brown parka) — never describe a different appearance for "you".
