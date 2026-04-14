"""
Entrepreneur Growth OS
======================
A complete self-improvement system with:
  - Dashboard
  - Entrepreneur Skill Tracker
  - Discipline / Habit Tracker
  - Calorie & Nutrition Logger
  - Money Skills Curriculum
  - Daily Lessons & Quizzes

Run:  python entrepreneur_os.py
Requires Python 3.8+  (tkinter is included in standard Python installs)
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime, date, timedelta

# ──────────────────────────────────────────────
#  DATA
# ──────────────────────────────────────────────
SKILLS = [
    {"name": "Sales & Persuasion",      "sub": "Close deals, pitch ideas",          "level": 20},
    {"name": "Financial Literacy",       "sub": "Read numbers, manage cash",         "level": 15},
    {"name": "Leadership",               "sub": "Build & inspire teams",             "level": 35},
    {"name": "Marketing & Branding",     "sub": "Attract & retain customers",        "level": 25},
    {"name": "Product Thinking",         "sub": "Build what people want",            "level": 40},
    {"name": "Negotiation",              "sub": "Win without burning bridges",       "level": 30},
    {"name": "Networking",               "sub": "Build powerful relationships",      "level": 45},
    {"name": "Discipline & Execution",   "sub": "Ship consistently",                 "level": 55},
    {"name": "Resilience & Mindset",     "sub": "Bounce back stronger",              "level": 60},
    {"name": "Communication",            "sub": "Write, speak, listen well",         "level": 50},
]

MONEY_TOPICS = [
    ("Budgeting Basics",        "Track every rupee. Know income vs expenses. Use the 50/30/20 rule."),
    ("Emergency Fund",          "Save 3–6 months of expenses before investing. This is your safety net."),
    ("Compound Interest",       "Money grows on itself. Start early. ₹500/month becomes life-changing."),
    ("Debt Management",         "Good debt (assets) vs bad debt (liabilities). Pay bad debt first."),
    ("Investing Fundamentals",  "Mutual funds, index funds, SIPs. Learn before you invest."),
    ("Cash Flow for Business",  "Revenue is vanity, profit is sanity, cash flow is reality."),
    ("Pricing & Margins",       "Charge what you're worth. Know COGS, gross margin, net margin."),
    ("Tax Basics",              "GST, income tax, business deductions. Know the rules."),
]

LESSONS = [
    {
        "title": "The 1% Rule",
        "body": (
            "Improve by 1% every day. In one year, you'll be 37x better.\n\n"
            "The secret to mastery is consistency, not intensity.\n"
            "Pick one skill. Practice it daily for 10 minutes. Track it.\n\n"
            "Small daily gains compound into extraordinary results."
        ),
        "quiz": {
            "q": "If you improve 1% daily for 365 days, you are roughly how many times better?",
            "opts": ["2x", "10x", "37x", "100x"],
            "ans": 2,
        },
    },
    {
        "title": "Why Most Entrepreneurs Quit",
        "body": (
            "They quit when it gets hard — not when it's impossible.\n\n"
            "The dip is the moment most people leave.\n"
            "That's exactly when you should push harder.\n\n"
            "Build systems, not motivation. Systems run even when you don't feel like it."
        ),
        "quiz": {
            "q": "What is the primary reason entrepreneurs quit?",
            "opts": ["Lack of money", "Lack of talent", "Giving up during the hard phase", "Bad timing"],
            "ans": 2,
        },
    },
    {
        "title": "The Value Equation",
        "body": (
            "Your income = (Value you create) × (People you serve)\n\n"
            "To earn more: serve more people OR create more value.\n"
            "Both at once is a business.\n\n"
            "Stop asking 'how do I make money?' and start asking\n'how do I create more value for more people?'"
        ),
        "quiz": {
            "q": "To double your income, you can:",
            "opts": ["Work twice as hard", "Serve more people or create more value", "Copy your competition", "Reduce your prices"],
            "ans": 1,
        },
    },
    {
        "title": "Discipline Beats Motivation",
        "body": (
            "Motivation is emotional — it comes and goes.\n"
            "Discipline is a system.\n\n"
            "Build routines that run on autopilot:\n"
            "• Wake up at the same time every day\n"
            "• Work your hardest task first\n"
            "• Review your goals daily\n\n"
            "You don't need to feel like it. You just need to do it."
        ),
        "quiz": {
            "q": "What is more reliable for long-term success?",
            "opts": ["Motivation", "Inspiration", "Discipline and systems", "Natural talent"],
            "ans": 2,
        },
    },
    {
        "title": "Solve Problems = Make Money",
        "body": (
            "Every successful business solves a painful problem.\n\n"
            "The more painful the problem, the more people will pay.\n\n"
            "Steps:\n"
            "1. Find a problem you understand deeply\n"
            "2. Build the simplest solution\n"
            "3. Sell it before perfecting it\n\n"
            "Start with the customer's pain, not your product idea."
        ),
        "quiz": {
            "q": "What is the foundation of every successful business?",
            "opts": ["A great logo", "Solving a real problem", "A big team", "A lot of funding"],
            "ans": 1,
        },
    },
]

DAILY_FOCUSES = [
    "Work on your weakest skill for 15 minutes",
    "Cold outreach: message 3 potential customers",
    "Read one chapter on financial literacy",
    "Review your week: what worked, what didn't?",
    "Create one piece of content about your expertise",
    "Write down your top 3 goals for the next 90 days",
    "Practice your elevator pitch in the mirror",
]

DATA_FILE = os.path.join(os.path.dirname(__file__), "entrepreneur_os_data.json")

# ──────────────────────────────────────────────
#  PERSISTENCE
# ──────────────────────────────────────────────

def load_data():
    default = {
        "habits": ["Morning workout", "Read 20 min", "No social media before 10am", "Cold shower", "Review goals"],
        "completed": {},       # "YYYY-MM-DD_habitname" -> bool
        "cal_goals": {},       # "YYYY-MM-DD" -> int
        "foods": {},           # "YYYY-MM-DD" -> list of {name,cal,p,c,f}
        "skill_levels": [s["level"] for s in SKILLS],
        "money_done": [False] * len(MONEY_TOPICS),
        "lesson_idx": 0,
    }
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                saved = json.load(f)
            default.update(saved)
        except Exception:
            pass
    return default


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ──────────────────────────────────────────────
#  COLOURS / STYLES
# ──────────────────────────────────────────────
BG       = "#FFFFFF"
BG2      = "#F5F5F3"
BG3      = "#EFEFED"
TEXT     = "#1A1A1A"
TEXT2    = "#6B6B68"
BLUE     = "#378ADD"
GREEN    = "#1D9E75"
AMBER    = "#BA7517"
RED      = "#E24B4A"
BORDER   = "#E0DED8"
ACCENT   = "#EEEDFE"
ACCENT_T = "#3C3489"
FONT     = "Helvetica"


def style_button(btn, bg=BG, fg=TEXT, padx=12, pady=6):
    btn.configure(
        bg=bg, fg=fg, activebackground=BG2, activeforeground=TEXT,
        relief="flat", bd=0, padx=padx, pady=pady,
        font=(FONT, 11), cursor="hand2",
    )


# ──────────────────────────────────────────────
#  MAIN APP
# ──────────────────────────────────────────────
class EntrepreneurOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Entrepreneur Growth OS")
        self.root.geometry("820x680")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        self.data = load_data()
        self.today = date.today().isoformat()
        self.lesson_idx = self.data.get("lesson_idx", 0)
        self.quiz_answered = False

        self._build_nav()
        self._build_content()
        self.show_tab("dashboard")

    # ── NAV ──────────────────────────────────
    def _build_nav(self):
        nav = tk.Frame(self.root, bg=BG2, bd=0, relief="flat")
        nav.pack(fill="x", padx=0, pady=0)

        title = tk.Label(nav, text="Entrepreneur Growth OS", bg=BG2, fg=TEXT,
                         font=(FONT, 14, "bold"), padx=20, pady=10)
        title.pack(side="left")

        btn_frame = tk.Frame(nav, bg=BG2)
        btn_frame.pack(side="right", padx=10)

        self.nav_buttons = {}
        tabs = [("Dashboard", "dashboard"), ("Skills", "skills"),
                ("Discipline", "discipline"), ("Calories", "nutrition"),
                ("Money", "money"), ("Learn", "learn")]
        for label, key in tabs:
            btn = tk.Button(btn_frame, text=label,
                            command=lambda k=key: self.show_tab(k))
            style_button(btn, pady=4, padx=10)
            btn.pack(side="left", padx=2, pady=6)
            self.nav_buttons[key] = btn

        sep = tk.Frame(self.root, bg=BORDER, height=1)
        sep.pack(fill="x")

    # ── CONTENT FRAME ────────────────────────
    def _build_content(self):
        self.content = tk.Frame(self.root, bg=BG)
        self.content.pack(fill="both", expand=True)
        self.frames = {}
        for key in ["dashboard", "skills", "discipline", "nutrition", "money", "learn"]:
            f = tk.Frame(self.content, bg=BG)
            self.frames[key] = f

    def show_tab(self, key):
        for k, f in self.frames.items():
            f.pack_forget()
        self.frames[key].pack(fill="both", expand=True)
        for k, b in self.nav_buttons.items():
            b.configure(bg=BG2 if k != key else ACCENT, fg=TEXT2 if k != key else ACCENT_T,
                        font=(FONT, 11, "bold") if k == key else (FONT, 11))
        build = getattr(self, f"_render_{key}", None)
        if build:
            for w in self.frames[key].winfo_children():
                w.destroy()
            build(self.frames[key])

    # ──────────────────────────────────────────
    #  DASHBOARD
    # ──────────────────────────────────────────
    def _render_dashboard(self, frame):
        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)

        pad = tk.Frame(inner, bg=BG)
        pad.pack(fill="x", padx=24, pady=16)

        # Metrics row
        mf = tk.Frame(pad, bg=BG)
        mf.pack(fill="x", pady=(0, 16))
        streak = self._calc_streak()
        avg = int(sum(self.data["skill_levels"]) / len(self.data["skill_levels"]))
        cals = sum(f["cal"] for f in self.data["foods"].get(self.today, []))
        for val, lbl in [(f"{streak} days", "Streak"), (f"{avg}%", "Skill avg"), (f"{cals} kcal", "Cals today")]:
            m = tk.Frame(mf, bg=BG2, relief="flat", bd=0)
            m.pack(side="left", padx=(0, 12), pady=4, ipadx=16, ipady=10)
            tk.Label(m, text=val, bg=BG2, fg=TEXT, font=(FONT, 20, "bold")).pack()
            tk.Label(m, text=lbl, bg=BG2, fg=TEXT2, font=(FONT, 10)).pack()

        # Today's focus
        self._section(pad, "Today's Focus")
        fc = tk.Frame(pad, bg=BG2, relief="flat")
        fc.pack(fill="x", pady=(0, 16))
        dof = date.today().weekday()
        for i, f in enumerate(DAILY_FOCUSES[:3]):
            prefix = "→" if i == 0 else " "
            col = TEXT if i == 0 else TEXT2
            tk.Label(fc, text=f"{prefix}  {f}", bg=BG2, fg=col,
                     font=(FONT, 12), anchor="w", padx=12, pady=4).pack(fill="x")

        # Habits summary
        self._section(pad, "Today's Habits")
        for h in self.data["habits"][:5]:
            k = f"{self.today}_{h}"
            done = self.data["completed"].get(k, False)
            hf = tk.Frame(pad, bg=BG, relief="flat")
            hf.pack(fill="x", pady=2)
            dot = "✓" if done else "○"
            col = GREEN if done else TEXT2
            tk.Label(hf, text=f"  {dot}  {h}", bg=BG, fg=col,
                     font=(FONT, 12), anchor="w").pack(side="left")

        tk.Label(pad, text="", bg=BG).pack()
        tip = tk.Button(pad, text="Get today's challenge →",
                        command=lambda: messagebox.showinfo(
                            "Today's Challenge",
                            "Challenge: Talk to one stranger today about their biggest problem.\n\n"
                            "Entrepreneurs find problems. This is your training."
                        ))
        style_button(tip, bg=ACCENT, fg=ACCENT_T)
        tip.pack(anchor="w", pady=8)

    # ──────────────────────────────────────────
    #  SKILLS
    # ──────────────────────────────────────────
    def _render_skills(self, frame):
        canvas, inner, pad = self._scrollable(frame)
        self._section(pad, "Entrepreneur Skill Tree")

        for i, s in enumerate(SKILLS):
            sf = tk.Frame(pad, bg=BG2, relief="flat")
            sf.pack(fill="x", pady=3, ipady=6)

            info = tk.Frame(sf, bg=BG2)
            info.pack(side="left", padx=12, fill="y")
            tk.Label(info, text=s["name"], bg=BG2, fg=TEXT,
                     font=(FONT, 12, "bold"), anchor="w", width=22).pack(anchor="w")
            tk.Label(info, text=s["sub"], bg=BG2, fg=TEXT2,
                     font=(FONT, 10), anchor="w").pack(anchor="w")

            bar_frame = tk.Frame(sf, bg=BG2)
            bar_frame.pack(side="left", expand=True, fill="x", padx=8)
            bar_bg = tk.Frame(bar_frame, bg=BORDER, height=8)
            bar_bg.pack(fill="x", pady=8)
            bar_bg.update_idletasks()

            lvl = self.data["skill_levels"][i]
            bar_fill = tk.Frame(bar_bg, bg=BLUE, height=8)
            bar_fill.place(relwidth=lvl / 100, relheight=1)

            tk.Label(sf, text=f"{lvl}%", bg=BG2, fg=BLUE,
                     font=(FONT, 11, "bold"), width=5).pack(side="left")

            plus_btn = tk.Button(sf, text="+5", font=(FONT, 10),
                                 command=lambda idx=i: self._train_skill(idx, frame))
            style_button(plus_btn, bg=BG3, pady=2, padx=8)
            plus_btn.pack(side="left", padx=6)

        tk.Label(pad, text="", bg=BG).pack()
        b1 = tk.Button(pad, text="Practice my weakest skill →",
                       command=lambda: messagebox.showinfo(
                           "Weakest Skill Practice",
                           f"Your weakest skill is: {SKILLS[self.data['skill_levels'].index(min(self.data['skill_levels']))]['name']}\n\n"
                           "Exercise: Write 3 bullet points explaining it to a 10-year-old.\n"
                           "Then find one YouTube video on it today."
                       ))
        style_button(b1, bg=ACCENT, fg=ACCENT_T)
        b1.pack(anchor="w", pady=4)

    def _train_skill(self, idx, frame):
        self.data["skill_levels"][idx] = min(100, self.data["skill_levels"][idx] + 5)
        save_data(self.data)
        self.show_tab("skills")

    # ──────────────────────────────────────────
    #  DISCIPLINE
    # ──────────────────────────────────────────
    def _render_discipline(self, frame):
        canvas, inner, pad = self._scrollable(frame)

        # Calendar
        self._section(pad, f"Monthly Tracker — {date.today().strftime('%B %Y')}")
        cal_f = tk.Frame(pad, bg=BG)
        cal_f.pack(fill="x", pady=(0, 12))

        days_hdr = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for c, d in enumerate(days_hdr):
            tk.Label(cal_f, text=d, bg=BG, fg=TEXT2, font=(FONT, 9), width=4).grid(row=0, column=c, padx=2)

        today_obj = date.today()
        first_day = today_obj.replace(day=1)
        start_col = first_day.weekday()
        # weekday() is Mon=0; we want Sun=0
        start_col = (start_col + 1) % 7
        days_in_month = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)).day

        for d in range(1, days_in_month + 1):
            row = (d + start_col - 1) // 7 + 1
            col = (d + start_col - 1) % 7
            d_str = today_obj.replace(day=d).isoformat()
            any_done = any(self.data["completed"].get(f"{d_str}_{h}", False) for h in self.data["habits"])
            is_today = d == today_obj.day
            is_past = d < today_obj.day

            bg_c = BG2
            fg_c = TEXT2
            if is_today:
                bg_c = ACCENT
                fg_c = ACCENT_T
            elif any_done and is_past:
                bg_c = "#EAF3DE"
                fg_c = "#27500A"
            elif is_past:
                bg_c = "#FCEBEB"
                fg_c = "#A32D2D"

            lbl = tk.Label(cal_f, text=str(d), bg=bg_c, fg=fg_c,
                           font=(FONT, 10, "bold") if is_today else (FONT, 10),
                           width=3, height=2, relief="flat")
            lbl.grid(row=row, column=col, padx=2, pady=2)

        # Habits
        self._section(pad, "Daily Habits")
        self.habit_vars = {}
        habits_frame = tk.Frame(pad, bg=BG)
        habits_frame.pack(fill="x")

        for h in list(self.data["habits"]):
            k = f"{self.today}_{h}"
            var = tk.BooleanVar(value=self.data["completed"].get(k, False))
            self.habit_vars[h] = var
            hf = tk.Frame(habits_frame, bg=BG2, relief="flat")
            hf.pack(fill="x", pady=3, ipady=4)
            cb = tk.Checkbutton(hf, text=f"  {h}", variable=var, bg=BG2, fg=TEXT,
                                activebackground=BG2, selectcolor=BG2,
                                font=(FONT, 12), anchor="w",
                                command=lambda kk=k, vv=var: self._toggle_habit(kk, vv))
            cb.pack(side="left", fill="x", expand=True, padx=8)
            del_btn = tk.Button(hf, text="✕",
                                command=lambda hh=h: self._remove_habit(hh, frame))
            style_button(del_btn, bg=BG2, fg=TEXT2, padx=6, pady=2)
            del_btn.pack(side="right", padx=8)

        # Add habit
        add_f = tk.Frame(pad, bg=BG)
        add_f.pack(fill="x", pady=8)
        self._section(pad, "Add Habit")
        entry = tk.Entry(pad, font=(FONT, 12), relief="solid", bd=1, bg=BG2)
        entry.pack(fill="x", pady=4, ipady=6)
        add_btn = tk.Button(pad, text="Add Habit",
                            command=lambda: self._add_habit(entry.get(), frame))
        style_button(add_btn, bg=BLUE, fg="white")
        add_btn.pack(anchor="w", pady=4)

    def _toggle_habit(self, key, var):
        self.data["completed"][key] = var.get()
        save_data(self.data)

    def _add_habit(self, name, frame):
        name = name.strip()
        if name and name not in self.data["habits"]:
            self.data["habits"].append(name)
            save_data(self.data)
            self.show_tab("discipline")

    def _remove_habit(self, name, frame):
        if messagebox.askyesno("Remove Habit", f"Remove '{name}'?"):
            self.data["habits"] = [h for h in self.data["habits"] if h != name]
            save_data(self.data)
            self.show_tab("discipline")

    # ──────────────────────────────────────────
    #  NUTRITION
    # ──────────────────────────────────────────
    def _render_nutrition(self, frame):
        canvas, inner, pad = self._scrollable(frame)
        self._section(pad, "Calorie & Nutrition Tracker")

        foods = self.data["foods"].get(self.today, [])
        total_cal = sum(f["cal"] for f in foods)
        total_p   = sum(f.get("p", 0) for f in foods)
        total_c   = sum(f.get("c", 0) for f in foods)
        total_f   = sum(f.get("f", 0) for f in foods)
        goal = self.data["cal_goals"].get(self.today, 2000)

        # Summary card
        sc = tk.Frame(pad, bg=BG2, relief="flat")
        sc.pack(fill="x", pady=(0, 12), ipady=8)
        left = total_cal
        remaining = max(0, goal - left)
        pct = min(1.0, total_cal / goal) if goal else 0

        summary_txt = f"Goal: {goal} kcal   |   Eaten: {total_cal} kcal   |   Left: {remaining} kcal"
        tk.Label(sc, text=summary_txt, bg=BG2, fg=TEXT, font=(FONT, 11), anchor="w", padx=12).pack(fill="x")

        # Progress bar
        bar_bg = tk.Frame(sc, bg=BORDER, height=10)
        bar_bg.pack(fill="x", padx=12, pady=6)
        bar_bg.update_idletasks()
        bar_color = RED if pct >= 1.0 else BLUE
        bar_fill = tk.Frame(bar_bg, bg=bar_color, height=10)
        bar_fill.place(relwidth=pct, relheight=1)

        # Macros
        macro_txt = f"Protein: {round(total_p)}g   Carbs: {round(total_c)}g   Fat: {round(total_f)}g"
        tk.Label(sc, text=macro_txt, bg=BG2, fg=TEXT2, font=(FONT, 10), anchor="w", padx=12).pack(fill="x")

        # Set goal
        self._section(pad, "Set Calorie Goal")
        gf = tk.Frame(pad, bg=BG)
        gf.pack(fill="x", pady=(0, 12))
        goal_var = tk.StringVar(value=str(goal))
        tk.Label(gf, text="Daily goal (kcal):", bg=BG, fg=TEXT2, font=(FONT, 11)).pack(side="left")
        goal_entry = tk.Entry(gf, textvariable=goal_var, font=(FONT, 11), width=8,
                              relief="solid", bd=1, bg=BG2)
        goal_entry.pack(side="left", padx=8, ipady=4)
        set_btn = tk.Button(gf, text="Set",
                            command=lambda: self._set_goal(goal_var.get(), frame))
        style_button(set_btn, bg=BLUE, fg="white", padx=10, pady=4)
        set_btn.pack(side="left")

        # Log food form
        self._section(pad, "Log Food")
        fields = {}
        for label, key, w in [("Food name", "name", 20), ("Calories (kcal)", "cal", 8),
                                ("Protein (g)", "p", 8), ("Carbs (g)", "c", 8), ("Fat (g)", "f", 8)]:
            row = tk.Frame(pad, bg=BG)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=label, bg=BG, fg=TEXT2, font=(FONT, 11), width=16, anchor="w").pack(side="left")
            e = tk.Entry(row, font=(FONT, 11), width=w, relief="solid", bd=1, bg=BG2)
            e.pack(side="left", padx=4, ipady=4)
            fields[key] = e

        log_btn = tk.Button(pad, text="Log Food",
                            command=lambda: self._log_food(fields, frame))
        style_button(log_btn, bg=GREEN, fg="white")
        log_btn.pack(anchor="w", pady=8)

        # Food log
        self._section(pad, "Today's Log")
        if not foods:
            tk.Label(pad, text="No food logged yet.", bg=BG, fg=TEXT2, font=(FONT, 11)).pack(anchor="w")
        for i, food in enumerate(foods):
            rf = tk.Frame(pad, bg=BG2, relief="flat")
            rf.pack(fill="x", pady=2, ipady=4)
            tk.Label(rf, text=f"  {food['name']}", bg=BG2, fg=TEXT,
                     font=(FONT, 11), anchor="w", width=28).pack(side="left")
            tk.Label(rf, text=f"{food['cal']} kcal", bg=BG2, fg=TEXT2,
                     font=(FONT, 11)).pack(side="left", padx=8)
            p_lbl = f"P:{round(food.get('p',0))}g  C:{round(food.get('c',0))}g  F:{round(food.get('f',0))}g"
            tk.Label(rf, text=p_lbl, bg=BG2, fg=TEXT2, font=(FONT, 9)).pack(side="left", padx=4)
            del_btn = tk.Button(rf, text="✕",
                                command=lambda idx=i: self._delete_food(idx, frame))
            style_button(del_btn, bg=BG2, fg=TEXT2, padx=4, pady=2)
            del_btn.pack(side="right", padx=6)

        tk.Label(pad, text="", bg=BG).pack()
        tip = tk.Button(pad, text="Get a high-protein meal plan →",
                        command=lambda: messagebox.showinfo(
                            "High-Protein Meal Plan",
                            "Breakfast: 4 boiled eggs + oats (450 kcal, 32g P)\n"
                            "Lunch: Chicken breast + rice + veggies (550 kcal, 45g P)\n"
                            "Snack: Greek yoghurt + banana (200 kcal, 15g P)\n"
                            "Dinner: Dal + roti + paneer (500 kcal, 30g P)\n\n"
                            "Total ≈ 1700 kcal | 122g protein\nAdjust portions to hit your goal."
                        ))
        style_button(tip, bg=ACCENT, fg=ACCENT_T)
        tip.pack(anchor="w", pady=4)

    def _set_goal(self, val, frame):
        try:
            g = int(val)
            if g > 0:
                self.data["cal_goals"][self.today] = g
                save_data(self.data)
                self.show_tab("nutrition")
        except ValueError:
            messagebox.showerror("Invalid", "Please enter a valid number.")

    def _log_food(self, fields, frame):
        name = fields["name"].get().strip()
        try:
            cal = int(fields["cal"].get() or 0)
        except ValueError:
            cal = 0
        if not name or cal <= 0:
            messagebox.showwarning("Missing info", "Please enter food name and calories.")
            return
        food = {
            "name": name, "cal": cal,
            "p": float(fields["p"].get() or 0),
            "c": float(fields["c"].get() or 0),
            "f": float(fields["f"].get() or 0),
        }
        if self.today not in self.data["foods"]:
            self.data["foods"][self.today] = []
        self.data["foods"][self.today].append(food)
        save_data(self.data)
        self.show_tab("nutrition")

    def _delete_food(self, idx, frame):
        self.data["foods"][self.today].pop(idx)
        save_data(self.data)
        self.show_tab("nutrition")

    # ──────────────────────────────────────────
    #  MONEY
    # ──────────────────────────────────────────
    def _render_money(self, frame):
        canvas, inner, pad = self._scrollable(frame)
        self._section(pad, "Money Skills Curriculum")
        done_count = sum(self.data["money_done"])
        tk.Label(pad, text=f"{done_count}/{len(MONEY_TOPICS)} topics completed",
                 bg=BG, fg=TEXT2, font=(FONT, 11)).pack(anchor="w", pady=(0, 12))

        for i, (title, desc) in enumerate(MONEY_TOPICS):
            done = self.data["money_done"][i]
            mf = tk.Frame(pad, bg=BG2 if not done else "#EAF3DE", relief="flat")
            mf.pack(fill="x", pady=3, ipady=6)

            check = "✓" if done else "○"
            check_col = GREEN if done else TEXT2
            tk.Label(mf, text=check, bg=mf["bg"], fg=check_col,
                     font=(FONT, 14), width=3).pack(side="left", padx=8)

            text_f = tk.Frame(mf, bg=mf["bg"])
            text_f.pack(side="left", fill="both", expand=True)
            tk.Label(text_f, text=title, bg=mf["bg"], fg=TEXT if not done else TEXT2,
                     font=(FONT, 12, "bold" if not done else "normal"),
                     anchor="w").pack(anchor="w")
            tk.Label(text_f, text=desc, bg=mf["bg"], fg=TEXT2,
                     font=(FONT, 10), anchor="w", wraplength=450, justify="left").pack(anchor="w")

            btn_txt = "Mark done" if not done else "Undo"
            toggle = tk.Button(mf, text=btn_txt,
                               command=lambda idx=i: self._toggle_money(idx, frame))
            style_button(toggle, bg=BG3, pady=2, padx=8)
            toggle.pack(side="right", padx=8)

        tk.Label(pad, text="", bg=BG).pack()
        for txt, tip in [
            ("Compound Interest Deep Dive →",
             "₹10,000 invested at 12% annually:\n• 10 years → ₹31,058\n• 20 years → ₹96,463\n• 30 years → ₹2,99,599\n\nStart TODAY. Time is your biggest asset."),
            ("Build my first budget →",
             "The 50/30/20 Rule:\n• 50% — Needs (rent, food, bills)\n• 30% — Wants (entertainment, shopping)\n• 20% — Savings & investments\n\nFor irregular income: budget on your LOWEST month. Save the rest."),
        ]:
            t = txt
            tip2 = tip
            b = tk.Button(pad, text=t, command=lambda m=tip2, tt=t: messagebox.showinfo(tt.replace(" →",""), m))
            style_button(b, bg=ACCENT, fg=ACCENT_T)
            b.pack(anchor="w", pady=4)

    def _toggle_money(self, idx, frame):
        self.data["money_done"][idx] = not self.data["money_done"][idx]
        save_data(self.data)
        self.show_tab("money")

    # ──────────────────────────────────────────
    #  LEARN
    # ──────────────────────────────────────────
    def _render_learn(self, frame):
        canvas, inner, pad = self._scrollable(frame)
        lesson = LESSONS[self.lesson_idx % len(LESSONS)]

        self._section(pad, f"Lesson {self.lesson_idx + 1} of {len(LESSONS)}")

        # Lesson card
        lc = tk.Frame(pad, bg=BG2, relief="flat")
        lc.pack(fill="x", pady=(0, 12), ipady=12)
        tk.Label(lc, text=lesson["title"], bg=BG2, fg=TEXT,
                 font=(FONT, 16, "bold"), anchor="w", padx=16).pack(fill="x")
        tk.Label(lc, text=lesson["body"], bg=BG2, fg=TEXT2,
                 font=(FONT, 12), anchor="nw", justify="left", padx=16, pady=8,
                 wraplength=580).pack(fill="x")

        # Quiz
        self._section(pad, "Quick Check")
        quiz = lesson["quiz"]
        tk.Label(pad, text=quiz["q"], bg=BG, fg=TEXT,
                 font=(FONT, 12, "bold"), anchor="w", wraplength=580, justify="left").pack(fill="x", pady=(0, 8))

        self.quiz_answered = False
        self.quiz_btns = []
        for i, opt in enumerate(quiz["opts"]):
            btn = tk.Button(pad, text=f"  {opt}", anchor="w",
                            command=lambda choice=i: self._answer_quiz(choice, quiz["ans"], frame))
            style_button(btn, bg=BG2, padx=10, pady=6)
            btn.configure(width=50)
            btn.pack(fill="x", pady=3)
            self.quiz_btns.append(btn)

        self.result_lbl = tk.Label(pad, text="", bg=BG, font=(FONT, 12))
        self.result_lbl.pack(anchor="w", pady=8)

        next_btn = tk.Button(pad, text="Next Lesson →", command=self._next_lesson)
        style_button(next_btn, bg=BLUE, fg="white")
        next_btn.pack(anchor="w", pady=4)

        tip = tk.Button(pad, text="Books every entrepreneur must read →",
                        command=lambda: messagebox.showinfo(
                            "Must-Read Books",
                            "1. The Lean Startup — Eric Ries\n"
                            "2. Zero to One — Peter Thiel\n"
                            "3. Rich Dad Poor Dad — Robert Kiyosaki\n"
                            "4. Atomic Habits — James Clear\n"
                            "5. The $100 Startup — Chris Guillebeau\n"
                            "6. Think and Grow Rich — Napoleon Hill\n"
                            "7. Deep Work — Cal Newport\n\n"
                            "Read 20 pages a day. 1 book every 2 weeks."
                        ))
        style_button(tip, bg=ACCENT, fg=ACCENT_T)
        tip.pack(anchor="w", pady=4)

    def _answer_quiz(self, choice, ans, frame):
        if self.quiz_answered:
            return
        self.quiz_answered = True
        for i, btn in enumerate(self.quiz_btns):
            if i == ans:
                btn.configure(bg="#EAF3DE", fg="#27500A")
            elif i == choice and choice != ans:
                btn.configure(bg="#FCEBEB", fg="#A32D2D")
            btn.configure(state="disabled")
        if choice == ans:
            self.result_lbl.configure(text="✓  Correct! Great work.", fg=GREEN)
        else:
            self.result_lbl.configure(text=f"✗  The correct answer was: {LESSONS[self.lesson_idx % len(LESSONS)]['quiz']['opts'][ans]}", fg=RED)

    def _next_lesson(self):
        self.lesson_idx = (self.lesson_idx + 1) % len(LESSONS)
        self.data["lesson_idx"] = self.lesson_idx
        save_data(self.data)
        self.show_tab("learn")

    # ──────────────────────────────────────────
    #  HELPERS
    # ──────────────────────────────────────────
    def _scrollable(self, frame):
        canvas = tk.Canvas(frame, bg=BG, highlightthickness=0)
        sb = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=BG)
        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
        pad = tk.Frame(inner, bg=BG)
        pad.pack(fill="x", padx=24, pady=16)
        return canvas, inner, pad

    def _section(self, parent, title):
        tk.Label(parent, text=title.upper(), bg=BG, fg=TEXT2,
                 font=(FONT, 9), anchor="w").pack(fill="x", pady=(12, 4))
        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", pady=(0, 8))

    def _calc_streak(self):
        streak = 0
        d = date.today()
        for _ in range(60):
            ds = d.isoformat()
            any_done = any(self.data["completed"].get(f"{ds}_{h}", False) for h in self.data["habits"])
            if any_done or ds == date.today().isoformat():
                if any_done:
                    streak += 1
                else:
                    break
            else:
                break
            d -= timedelta(days=1)
        return streak


# ──────────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = EntrepreneurOS(root)
    root.mainloop()
