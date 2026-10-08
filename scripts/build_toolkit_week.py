"""Generates toolkit-week.html: the 28-day Mobility Toolkit + Strength + Cardio plan.

Edit the plan here, then run: python scripts/build_toolkit_week.py
Don't hand-edit toolkit-week.html; it gets overwritten.

Each day has one version per week (.week-variant[data-week]); the week picker shows one.
Checkboxes carry a data-key (day + week + exercise) so ticks are saved by name.
"""
import html
import os
import re

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
old = open('bodyweight-rope.html', encoding='utf-8').read()
modals = old[old.index('        <!-- Info Modal -->'):old.index('    </header>')]


def e(s):
    return html.escape(s, quote=True)


def slug(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower()).strip('-')


# ---------------------------------------------------------------- Toolkit lessons
SKOOL = 'https://www.skool.com/movesmethod/classroom/828d6756?md='
UPPER = 'Shoulders, Spine, Hamstrings, Hips, Wrists'
LOWER = 'Shoulders, Ankles, Knees'
TOOLKIT = {
    1: {1: (UPPER, '19819df8dae9425fa30a3718a5d5a91b'), 2: (LOWER, 'd9d56497e21d4df784b4bdc72073c934'),
        3: ('Flow 1', '1c632f66d29a4bcb922434041606a763'), 4: (UPPER, 'a625eb49d41648b6b39e165c06a147e1'),
        5: (LOWER, '14be5d901a1c446db2edefcc650ddcbd'), 6: (UPPER, 'fbf8e67082ae48e497593ff7966454a8')},
    2: {1: (UPPER, '6fae5cbe4cf1497fbe85998fef681c43'), 2: (LOWER, '759b7464834a4e299ee081680f789786'),
        3: ('Flow 2', '4642157547784cc286d489b2f3a74a53'), 4: (UPPER, '23c834b879194699a9af390be8d5994f'),
        5: (LOWER, '5fb14054a1834922b863717607b48d3e'), 6: (UPPER, '75f7033a37f9424b99e6b67ce3aa5f61')},
    3: {1: (UPPER, '67e3ecac984349c6a3ca2205d4644f2b'), 2: (LOWER, '882abc91a8ff45ef98d938eb259e4724'),
        3: ('Flow 3', '1b0fd06851464e4e9e952c58c7528432'), 4: (UPPER, 'f6d92e15619249caad335b0c772a7eaf'),
        5: (LOWER, 'a9f0ffb3c25b4599bfa5a5ac27a6ec16'), 6: (UPPER, '619ab2c911d646de814f4a991a56a194')},
    4: {1: (UPPER, '458e9755d4304826bd0815a412377c34'), 2: ('Flow 1', 'e3f0cc9627414e5683b4247781d04028'),
        3: (LOWER, '2cdd625ad8ff4e9d8d3ed33225563ebe'), 4: ('Flow 2', '1a43914dd4fa401583cc2b4bf58978f3'),
        5: (UPPER, 'f25649e489dc49e9884bb738ca882254'), 6: ('Flow 3', '7a861b4ed2ed41a6aafa3ada83f9dae2')},
}

# ---------------------------------------------------------------- Exercise library
YT = 'https://www.youtube.com/results?search_query='
ZONE2 = 'Zone 2: an easy pace where you can talk in full sentences, at 80–90 rpm on the bike.'
EX = {
    'Dead bug': ('Lie on your back, arms up and knees over hips. Slowly lower the opposite arm and leg while keeping your lower back pressed into the floor.', 'dead+bug+exercise+form'),
    'Side plank': ('Support yourself on one forearm and the side of your feet, keeping a straight line from head to heels.', 'side+plank+form'),
    'Bird dog': ('On hands and knees, extend the opposite arm and leg, hold for 2 seconds without rotating your hips, then return.', 'bird+dog+exercise+form'),
    'Kettlebell or dumbbell halo': ('Hold the weight at chest height and circle it slowly around your head, keeping your core braced and ribs down.', 'kettlebell+halo+form'),
    'Suitcase carry': ('Carry a weight in one hand at your side and walk tall without leaning toward the weight.', 'suitcase+carry+kettlebell+form'),
    'Glute bridge': ('Lie on your back with knees bent, squeeze your glutes, and lift your hips off the floor.', 'glute+bridge+form'),
    'Goblet squat': ('Hold a dumbbell or kettlebell at your chest and squat down between your knees, chest up, then stand.', 'goblet+squat+form+tutorial'),
    'Dumbbell Romanian deadlift': ('Hold dumbbells in front of your thighs, soften your knees, and hinge at the hips to lower them along your legs until you feel your hamstrings, then stand tall.', 'dumbbell+romanian+deadlift+form'),
    'Static split squat': ('Stand in a long split stance and lower straight down until both knees are bent about 90 degrees, then push back up. Stay in the same stance for all reps.', 'dumbbell+split+squat+static+lunge+form'),
    'Dumbbell floor press': ('Lie on the floor with knees bent and press the dumbbells up from your chest until your arms are straight. Upper arms touch the floor at the bottom.', 'dumbbell+floor+press+form'),
    'One-arm dumbbell row': ('Brace one hand on a bench or knee, keep your back flat, and pull the dumbbell toward your hip.', 'one+arm+dumbbell+row+form'),
    'Half-kneeling dumbbell press': ('Kneel on one knee with the other foot forward, squeeze your glutes, and press the dumbbell overhead without arching your back.', 'half+kneeling+single+arm+dumbbell+press'),
    'Alt: Seated dumbbell press': ('Sit tall on a bench or chair with back support and press the dumbbells overhead. Use this in place of the half-kneeling press if kneeling is uncomfortable.', 'seated+dumbbell+shoulder+press+form'),
    'Incline push-up': ('Push-up with your hands on a bench, counter or step. Keep a straight body line from head to heels.', 'incline+push+up+form'),
    'Farmer carry': ('Hold a heavy weight in each hand at your sides and walk tall with your shoulders back.', 'farmer+carry+dumbbell+form'),
    'Indoor bike, zone 2': (ZONE2, None),
    'Indoor bike': (ZONE2, None),
    'Easy indoor ride': ('A relaxed, easy spin on the indoor bike. Keep it conversational.', None),
    'Jump rope intervals': ('Jump for the "on" time, then rest or bounce easy for the "off" time. If your calves or Achilles feel tight, choose the bike instead.', None),
}


class Variant:
    """Builds the HTML for one day in one week."""

    def __init__(self, day, week):
        self.day, self.week, self.parts, self.keys = day, week, [], set()

    def add(self, line):
        self.parts.append(line)

    def item(self, name, reps, desc=None):
        key = f'{self.day}-w{self.week}-{slug(name)}'
        assert key not in self.keys, key
        self.keys.add(key)
        d, q = EX.get(name, (desc, None))
        desc = desc or d
        video = f'\n                        data-video="{e(YT + q)}"' if q else ''
        return f'''                <li><label class="exercise-label"><input type="checkbox" data-key="{key}"><span class="exercise-name">{e(name)}</span><span
                            class="exercise-reps">{e(reps)}</span></label><button class="info-icon" data-name="{e(name)}"
                        data-desc="{e(desc)}"{video}
                        onclick="openInfoModal(event, this)">i</button></li>'''

    def ul(self, *items):
        self.add('            <ul>\n' + '\n'.join(self.item(*i) for i in items) + '\n            </ul>')

    def note(self, text):
        self.add(f'            <div class="note">{text}</div>')

    def equipment(self, text):
        self.add(f'            <div class="equipment"><strong>Equipment:</strong> {text}</div>')

    def toolkit(self, n):
        title, md = TOOLKIT[self.week][n]
        self.add(f'            <a class="toolkit-link" href="{SKOOL}{md}" target="_blank" rel="noopener">&#9654; Mobility Toolkit: Week {self.week}, Day {n}, {e(title)}</a>')
        self.ul(('Toolkit session', f'Day {n}', f'Follow the Week {self.week}, Day {n} lesson on Skool: {title}.'))

    def heading(self, text, rounds=None):
        r = f' <span class="rounds">{rounds}</span>' if rounds else ''
        self.add(f'            <h2>{text}{r}</h2>')

    def option(self, letter):
        self.add(f'            <div class="option-label">Option {letter}</div>')


REST = '<strong>Rest:</strong> 30–45 sec between exercises, 2 min between rounds.'
SORE = '<strong>Sore from the Toolkit?</strong> Drop strength to 2 rounds.'
CALVES = 'Pick <strong>one</strong> option. If your calves or Achilles feel tight, choose the bike.'


def core_circuit(v, rounds, side_plank):
    v.equipment('Kettlebell or dumbbell')
    if rounds != '2 Rounds':
        v.note(SORE)
    v.heading('Core Circuit', rounds)
    v.note(REST)
    v.ul(('Dead bug', '8 each side, slow'),
         ('Side plank', side_plank),
         ('Bird dog', '8 each side, 2-sec hold'),
         ('Kettlebell or dumbbell halo', '6 each direction'),
         ('Suitcase carry', '20 steps each hand'),
         ('Glute bridge', '12 reps, bodyweight'))


def upper_circuit(v, rounds, weights):
    v.equipment('Dumbbells')
    v.note(f'<strong>Weights:</strong> {weights}')
    if rounds != '2 Rounds':
        v.note(SORE)
    v.heading('Upper Circuit', rounds)
    v.note(REST)
    v.ul(('Dumbbell floor press', '8 reps'),
         ('One-arm dumbbell row', '10 each side'),
         ('Half-kneeling dumbbell press', '8 each arm'),
         ('Alt: Seated dumbbell press', '8 reps, instead of half-kneeling'),
         ('Incline push-up', '8–10 reps'),
         ('Farmer carry', '30–40 steps'))


DAYS = [('monday', 'Monday', 1), ('tuesday', 'Tuesday', 2), ('wednesday', 'Wednesday', 3),
        ('thursday', 'Thursday', 4), ('friday', 'Friday', 5), ('saturday', 'Saturday', 6),
        ('sunday', 'Sunday', None)]

# Per-week numbers from the Progression Summary. The plan repeats every 28 days, so Week 1
# uses the Week 2 routine (2-round circuits) instead of the plan's original "Toolkit only".
W23 = {
    2: dict(core='2 Rounds', upper='2 Rounds', weights='Light.', tue_bike='30 min', fri_bike='45 min',
            rope='6–8 rounds: 30 sec on, 30 sec off', fri_rope='5 rounds: 30 sec on, 30 sec off'),
    3: dict(core='3 Rounds', upper='3 Rounds', weights='Same as Week 2.', tue_bike='35 min', fri_bike='50 min',
            rope='8–10 rounds: 1 min on, 1 min off', fri_rope='5 rounds: 1 min on, 1 min off'),
}
W23[1] = W23[2]


def build(day, week):
    """Returns (title, overview summary, Variant) for one day in one week."""
    v = Variant(day, week)
    n = dict((d, i) for d, _, i in DAYS)[day]

    if day == 'sunday':
        v.add('''            <div class="rest-message">
                <p>🛌 Full rest day.</p>
            </div>''')
        return 'Rest', 'Rest', v

    if week in (1, 2, 3):
        w = W23[week]
        if day == 'monday':
            v.toolkit(n)
            core_circuit(v, w['core'], '20–30 sec each side')
            if week == 3:
                v.heading('Optional Lower Add-on')
                v.note('Only if your legs feel recovered.')
                v.ul(('Goblet squat', '2×8'))
            return 'Core', f'Core, {w["core"].lower()}' + ('; optional goblet squats' if week == 3 else ''), v
        if day == 'tuesday':
            v.toolkit(n)
            v.note(CALVES)
            v.option('A')
            v.ul(('Indoor bike, zone 2', w['tue_bike']))
            v.option('B')
            v.ul(('Jump rope intervals', w['rope']))
            return 'Cardio', f'Bike {w["tue_bike"]} or jump rope', v
        if day == 'wednesday':
            v.toolkit(n)
            v.ul(('Easy indoor ride', '20–30 min, optional'))
            return 'Flow', 'Flow, optional easy ride', v
        if day == 'thursday':
            v.toolkit(n)
            upper_circuit(v, w['upper'], w['weights'])
            return 'Upper', f'Upper, {w["upper"].lower()}, {w["weights"].lower().rstrip(".")}', v
        if day == 'friday':
            v.toolkit(n)
            v.note(CALVES)
            v.option('A')
            v.ul(('Indoor bike, zone 2', w['fri_bike']))
            v.option('B')
            v.ul(('Indoor bike', '30 min'), ('Jump rope intervals', w['fri_rope']))
            return 'Longer Cardio', f'Bike {w["fri_bike"]}, or 30 min bike + rope', v
        if day == 'saturday':
            v.toolkit(n)
            return 'Mobility Only', 'Mobility only', v

    # Week 4: Toolkit order changes
    if day == 'monday':
        v.toolkit(n)
        core_circuit(v, '3 Rounds', '30–40 sec each side')
        v.heading('Optional Lower Add-on')
        v.note("Only if you're no longer sore from the Toolkit.")
        v.ul(('Goblet squat', '2×8'),
             ('Dumbbell Romanian deadlift', '2×8, moderate weight'),
             ('Static split squat', '2×6 each leg'))
        return 'Core', 'Core, 3 rounds, longer side planks; optional lower add-on', v
    if day == 'tuesday':
        v.toolkit(n)
        v.note('No jump rope this week.')
        v.ul(('Indoor bike, zone 2', '40 min'))
        return 'Flow + Cardio', 'Flow, bike 40 min', v
    if day == 'wednesday':
        v.toolkit(n)
        v.ul(('Easy indoor ride', '20–30 min, optional'))
        return 'Knees/Ankles', 'Knees/ankles, optional easy ride', v
    if day == 'thursday':
        v.toolkit(n)
        upper_circuit(v, '2–3 Rounds', 'Slightly heavier on the floor press, row and press if Week 3 felt easy. '
                                       'Start with 2 rounds; do a 3rd only if your presses feel strong.')
        return 'Flow + Upper', 'Flow, upper 2–3 rounds, slightly heavier', v
    if day == 'friday':
        v.toolkit(n)
        v.ul(('Indoor bike, zone 2', '60 min'))
        return 'Longer Cardio', 'Bike 60 min', v
    if day == 'saturday':
        v.toolkit(n)
        return 'Flow', 'Flow', v


# ---------------------------------------------------------------- Assemble the page
day_blocks, overview_weeks = [], []
summaries = {w: [] for w in range(1, 5)}
for day, name, n in DAYS:
    variants = []
    for week in range(1, 5):
        title, summary, v = build(day, week)
        summaries[week].append((day, name, summary))
        variants.append(f'''            <div class="week-variant" data-week="{week}">
            <h1>{name} — {title}</h1>
{chr(10).join(v.parts)}
            </div>''')
    if day == 'sunday':
        footer = '''            <div class="day-options">
                <button type="button" class="next-week-action" onclick="startNextWeek()">Start next week &rarr;</button>
            </div>'''
    else:
        footer = f'''            <div class="day-options">
                <button type="button" class="reset-action" onclick="resetDay('{day}')">Reset Day</button>
            </div>'''
    day_blocks.append(f'''        <!-- {day.upper()} -->
        <div id="{day}" class="workout-day">
{chr(10).join(variants)}
{footer}
        </div>''')

for week in range(1, 5):
    items = '\n'.join(
        f'''                    <li><a href="#" onclick="setDay('{d}'); return false;"><strong>{nm}:</strong> {e(s)}</a></li>'''
        for d, nm, s in summaries[week])
    overview_weeks.append(f'''            <div class="week-variant" data-week="{week}">
                <ul style="margin-top: 20px;" class="overview-list">
{items}
                </ul>
            </div>''')

day_ids = ', '.join(f"'{d}'" for d, _, _ in DAYS)
day_labels = ', '.join(f"{d}: '{nm[:3]}'" for d, nm, _ in DAYS)
nav = '\n'.join(f'''                <button class="nav-btn" onclick="setDay('{d}')">{nm[:3]}</button>''' for d, nm, _ in DAYS)

page = f'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobility &amp; Strength</title>
    <link rel="stylesheet" href="styles.css">
</head>

<body data-storage-prefix="toolkit-cb-">
    <!-- Generated content: 28-Day Plan (Mobility Toolkit + Strength + Cardio). One .week-variant per day per week. -->

    <header>
        <div class="header-top">
            <a class="back-link" href="index.html" aria-label="All routines">&lsaquo; Routines</a>
            <div class="header-title">Mobility &amp; Strength</div>
            <button class="menu-toggle" onclick="toggleMenu()" aria-label="Toggle Menu">☰</button>
        </div>
        <nav class="nav-container" id="navModal">
            <div class="nav-modal-content">
                <button class="close-btn" onclick="toggleMenu()">✕</button>
                <button class="nav-btn active" onclick="setDay('overview')">Days & Options</button>
{nav}
                <a class="nav-btn nav-link" href="index.html">All Routines</a>
            </div>
        </nav>

{modals.rstrip()}
    </header>

    <main class="container">

        <div class="week-bar">
            <div class="stepper" role="group" aria-label="Toolkit week">
                <button type="button" class="step-btn" id="weekPrev" aria-label="Previous week">&lsaquo;</button>
                <span class="step-label" id="weekLabel">Week 1</span>
                <button type="button" class="step-btn" id="weekNext" aria-label="Next week">&rsaquo;</button>
            </div>
            <div class="stepper" role="group" aria-label="Day">
                <button type="button" class="step-btn" id="dayPrev" aria-label="Previous day">&lsaquo;</button>
                <span class="step-label" id="dayLabel">Overview</span>
                <button type="button" class="step-btn" id="dayNext" aria-label="Next day">&rsaquo;</button>
            </div>
        </div>

{(chr(10) + chr(10)).join(day_blocks)}

        <!-- OVERVIEW -->
        <div id="overview" class="workout-day active">
            <h1>Weekly Overview</h1>
{chr(10).join(overview_weeks)}

            <h1>Notes</h1>
            <ul class="overview-list notes-list" style="margin-top: 15px;">
                <li>Zone 2 means an easy pace where you can talk in full sentences, at 80–90 rpm on the bike.</li>
                <li>If you're sore going into a Toolkit session, drop strength to 2 rounds.</li>
                <li>If your calves or Achilles feel tight, choose the bike over jump rope.</li>
                <li>Toolkit Weeks 2–4 unlock on Skool 7, 14 and 21 days after you start.</li>
            </ul>

            <h1>Options</h1>
            <ul class="overview-list" style="margin-top: 15px;">
                <li><button type="button" class="next-week-action" onclick="startNextWeek()"><strong>Start Next
                            Week:</strong> Clear all ticks and move to the next Toolkit week</button></li>
                <li><button type="button" class="reset-action" onclick="resetWeek()"><strong>Reset Week:</strong>
                        Uncheck everything and reset to Round 1</button></li>
            </ul>
        </div>

    </main>

    <script>
        const WEEK_KEY = 'toolkit-week';

        function getToolkitWeek() {{
            try {{
                const saved = parseInt(localStorage.getItem(WEEK_KEY));
                if (saved >= 1 && saved <= 4) return saved;
            }} catch (e) {{ }}
            return 1;
        }}

        // Show this week's version of every day and update the Week stepper
        function setToolkitWeek(week) {{
            try {{ localStorage.setItem(WEEK_KEY, week); }} catch (e) {{ }}

            document.getElementById('weekLabel').textContent = `Week ${{week}}`;
            document.getElementById('weekPrev').disabled = week <= 1;
            document.getElementById('weekNext').disabled = week >= 4;
            document.querySelectorAll('.week-variant').forEach(v => {{
                v.classList.toggle('active', parseInt(v.dataset.week) === week);
            }});
        }}

        // Clear this week's ticks and move the picker forward; after Week 4 the program starts over
        function startNextWeek() {{
            const current = getToolkitWeek();
            const next = current >= 4 ? 1 : current + 1;
            const msg = current >= 4
                ? 'You finished Week 4. Clear all ticks and start the program again at Week 1?'
                : `Clear all ticks and move from Week ${{current}} to Week ${{next}}?`;
            openConfirmModal(msg, () => {{
                clearWeekProgress();
                setToolkitWeek(next);
                setDay('overview');
            }}, `Start Week ${{next}}`, 'Start');
        }}

        document.getElementById('weekPrev').addEventListener('click', () => setToolkitWeek(getToolkitWeek() - 1));
        document.getElementById('weekNext').addEventListener('click', () => setToolkitWeek(getToolkitWeek() + 1));
        setToolkitWeek(getToolkitWeek());

        // Day stepper: Overview, then Monday to Sunday. It follows setDay() wherever it's called from.
        const STEP_DAYS = ['overview', {day_ids}];
        const DAY_LABELS = {{ overview: 'Overview', {day_labels} }};
        let stepDay = 'overview';

        document.addEventListener('daychange', e => {{
            stepDay = e.detail;
            const i = STEP_DAYS.indexOf(stepDay);
            document.getElementById('dayLabel').textContent = DAY_LABELS[stepDay];
            document.getElementById('dayPrev').disabled = i <= 0;
            document.getElementById('dayNext').disabled = i >= STEP_DAYS.length - 1;
        }});
        document.getElementById('dayPrev').addEventListener('click', () => setDay(STEP_DAYS[STEP_DAYS.indexOf(stepDay) - 1]));
        document.getElementById('dayNext').addEventListener('click', () => setDay(STEP_DAYS[STEP_DAYS.indexOf(stepDay) + 1]));

        // Ticks used to be saved by position (toolkit-cb-0, -1, ...); those keys no longer match anything
        try {{
            Object.keys(localStorage).filter(k => /^toolkit-cb-\\d+$/.test(k)).forEach(k => localStorage.removeItem(k));
        }} catch (e) {{ }}
    </script>
    <script src="app.js"></script>
</body>

</html>
'''
open('toolkit-week.html', 'w', encoding='utf-8', newline='\n').write(page)
print('ok', page.count('type="checkbox"'), 'checkboxes')
