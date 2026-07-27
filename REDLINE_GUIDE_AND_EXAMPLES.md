# REDLINE DOCUMENT GUIDE & EXAMPLES
## What is a Redline? How to Create & Use Them.

---

## WHAT IS A "REDLINE" DOCUMENT?

A **redline** (or **markup**) is a version of a contract that **shows exactly what you want to change**, with visual indicators of:
- **Deletions** (text to remove) — shown as ~~strikethrough~~ or [DELETED]
- **Additions** (text to add) — shown as **bold** or [ADDED]
- **Replacements** (delete this, add that) — shown as ~~old text~~ **new text**

### Why Redlines Matter:
1. **Clarity:** Shows counsel AND the other party exactly what you're proposing
2. **Speed:** Easier than writing a 10-page memo explaining changes
3. **Legal Safety:** Counsel can review your changes and refine language
4. **Negotiation:** Other party sees your proposals at a glance
5. **Record:** Creates an audit trail of what was changed and when

### Example Use Case:
Instead of writing: "I don't like the confidentiality clause; it should be 3 years instead of indefinite"

You create a redline showing:
```
OLD:  "Mutual confidentiality survives indefinitely."
NEW:  "Mutual confidentiality survives for three (3) years following termination of this agreement."
```

Now Elizabeth can see exactly what you want, and counsel can review whether the language is correct.

---

## HOW TO CREATE A REDLINE IN WORD/GOOGLE DOCS

### Method 1: Microsoft Word Track Changes (Best for Lawyers)

1. Open Elizabeth's v3.6 document in Word
2. Click "Review" tab → "Track Changes"
3. Make edits normally:
   - Delete text (will appear as ~~strikethrough~~)
   - Add text (will appear as **bold** with underline)
4. All changes are recorded with timestamps
5. Save as "TermSheetAandBv3.6_TimothyRedline.docx"
6. Send to Elizabeth; she can see all your changes, accept/reject each one

**Advantage:** Professional; counsel is familiar with this format

### Method 2: Markdown/Text Markup (Good for Quick Communication)

Create a document showing changes in a clear format:

```markdown
SECTION 5 - SALARY

ORIGINAL:
Employee shall receive an annual base salary of $54,000 (Fifty-Four Thousand Dollars)

TIMOTHY'S REDLINE:
Employee shall receive an annual base salary of $75,000 (Seventy-Five Thousand Dollars), 
with increases to $85,000 when trailing 12-month revenue reaches $500,000 and to 
$100,000 when trailing 12-month revenue reaches $1,000,000.

RATIONALE: Market-competitive salary for Director role; stepping tied to company revenue 
milestones (not performance uncertainty)
```

**Advantage:** Simple; good for non-lawyers; easy to read

### Method 3: Strikethrough & Bold (Email-Friendly)

```
Section 26 - Conduct

Mutual confidentiality ~~survives indefinitely~~ **survives for three (3) years 
following termination of this agreement** — replacing the 12-month confidentiality 
sunset in B's draft.
```

**Advantage:** Works in any text editor; visible in email

---

## REDLINE EXAMPLE 1: SALARY CLAUSE

### ORIGINAL (From Elizabeth's v3.6):

```
3. Compensation

Employee shall receive an annual base salary of $100,000 (One Hundred Thousand 
Dollars), payable in accordance with the Company's standard payroll practices. 
Salary increases shall be determined based on company revenue and performance, 
subject to mutual written agreement of the parties.
```

### TIMOTHY'S REDLINE (Markup Format):

```
3. Compensation

Employee shall receive an annual base salary of ~~$100,000~~ **$75,000** 
(~~One Hundred~~ **Seventy-Five** Thousand Dollars), payable in accordance with 
the Company's standard payroll practices. 

Salary ~~increases~~ **shall step to $85,000 when trailing twelve-month collected 
revenue reaches $500,000, and to $100,000 when trailing twelve-month collected 
revenue reaches $1,000,000. Steps are automatic upon achieving the revenue milestone 
and require no mutual written agreement. Salary** increases outside these steps 
shall be determined based on company revenue and performance, subject to mutual 
written agreement of the parties.

REDLINE RATIONALE:
- $75K is market-competitive for Director of Business Development role (national 
  median: $65-85K per Bureau of Labor Statistics)
- Steps tied to objective company revenue milestones (not subjective performance)
- "Automatic" steps prevent Elizabeth from withholding salary increases
- Removes language "performance" as performance is already measured by attribution 
  system (Section 4); no need to double-measure
```

### WHY THIS MATTERS:

**Original Language Issues:**
- $54K → $72K → $100K (as proposed in v3.6)
- Steps are "determined based on company revenue and performance"
- "Subject to mutual written agreement" = Elizabeth can veto any increase
- **Result:** You reach $500K revenue, Elizabeth says "we'll renegotiate the increase" 
  → you lose salary bump

**Redline Fixes:**
- Locks salary increases to objective revenue milestones (no discretion)
- "Automatic upon achieving" = no veto power
- Higher starting point ($75K vs. $54K) provides runway during ramp-up

---

## REDLINE EXAMPLE 2: COMMITMENT WINDOW CLAUSE

### ORIGINAL (From Elizabeth's v3.6):

```
2. The commitment trigger (adopted from B's draft). When cumulative collected 
revenue of Company 1 reaches $200,000 — collected cash only; receivables count 
when paid, replacing the receivables-inclusive definition in B's draft — B may 
commit full-time: resign outside employment within 90 days and assume the full-time 
role. On commitment, the full-time package opens — salary (Section 5), full-speed 
time accrual (Section 3), and the full 30% ceiling. If B does not commit within 
90 days of the trigger, the part-time track simply continues and the ceilings step 
down — Company 1 from 30% to 20%, Company 2 from 10% to 7%.
```

### TIMOTHY'S REDLINE (Mark-Up):

```
2. The commitment trigger (adopted from B's draft). When cumulative collected 
revenue of Company 1 reaches $200,000 — collected cash only; receivables count 
when paid, replacing the receivables-inclusive definition in B's draft — B 
**shall automatically commit full-time upon achievement of this revenue milestone. 
B shall resign from outside employment as soon as legally and contractually 
permitted, and in no event more than 180 days following notice of the revenue trigger.** 

~~B may commit full-time: resign outside employment within 90 days and assume 
the full-time role.~~

On commitment, the full-time package opens — salary (Section 5), full-speed time 
accrual (Section 3), and the full 30% ceiling. 

~~If B does not commit within 90 days of the trigger, the part-time track simply 
continues and the ceilings step down — Company 1 from 30% to 20%, Company 2 from 
10% to 7%.~~

**No step-down penalty applies regardless of the timing of B's resignation from 
outside employment, provided B resigns as soon as legally and contractually 
permitted and in good faith. If B is unable to commit to full-time employment due 
to legal restrictions or non-compete obligations from prior employment, A and B 
shall negotiate in good faith to modify this commitment timeline or substitute an 
extended part-time arrangement that preserves B's 30% equity ceiling.**

REDLINE RATIONALE:
- Removes arbitrary 90-day calendar deadline (replaced by automatic trigger + 180-day 
  resignation window)
- No penalty for realistic employment law constraints (30-60 day notice periods, 
  non-compete negotiations)
- Protects you from losing 10% equity due to external constraints
- "In good faith" language ensures Elizabeth can't weaponize legal constraints
- More enforceable under NH law (removes penalty clause vulnerability)
```

### WHY THIS MATTERS:

**Original Language Issues:**
- 90-day hard stop is unrealistic (standard employment notice is 30-60 days)
- Step-down penalty is arbitrary (tied to calendar, not performance)
- No exception for non-compete constraints with current employer
- **Result:** You miss 90-day window due to non-compete conflict → lose 10% equity 
  ($50K+) through no fault of your own

**Redline Fixes:**
- Commitment is automatic (no decision needed; it's tied to $200K revenue objective)
- 180-day window is realistic for employment transitions
- "As soon as legally permitted" shows you're acting in good faith
- "Negotiate in good faith" prevents Elizabeth from weaponizing delays
- No equity penalty (removes unenforceable penalty clause)

---

## REDLINE EXAMPLE 3: ATTRIBUTION SYSTEM SIMPLIFICATION

### ORIGINAL (From Elizabeth's v3.6):

```
4. Results bucket — 20% of Company 1. 1% vests per $50,000 of revenue B causes, 
measured on cash actually collected (not contract signature), net of refunds and 
chargebacks; credit for a customer who cancels or goes delinquent within 90 days 
of first payment is reversed, and each contract is credited on its first-year 
collected revenue. The full 20% therefore requires $1,000,000 of caused revenue. 
Pre-trigger caused revenue counts. The bucket remains open for as long as B is 
actively working. 

Attribution is set by deal tags:

| What B Actually Did | Credit to B's Meter |
|---|---|
| Found the deal entirely from B's own sourcing (his network, research, events), ran the relationship, drove it to signature — A assisting as expert does not reduce credit | 100% |
| Found and carried the deal; A closed the final step | 75% |
| A's lead — including infrastructure-sourced leads — B carried and closed it | 50% |
| Warm introduction — B set the meeting, briefed A, made a real handoff | 15% |
| Bare name-pass ("you should meet A") | 10% |
| A found and closed it, including government awards won on A's registrations and credentials | 0% |

Infrastructure-sourced leads. a lead that originated from A's pre-built systems 
(prospect lists, batch search, drip sequences, company-run engine scans) is A-originated 
no matter who sends the first message, and caps at the 50% tier.
```

### TIMOTHY'S REDLINE (Three-Tier Simplified):

```
4. Results bucket — 20% of Company 1. 1% vests per $50,000 of revenue B causes, 
measured on cash actually collected (not contract signature), net of refunds and 
chargebacks; credit for a customer who cancels or goes delinquent within 90 days 
of first payment is reversed, and each contract is credited on its first-year 
collected revenue. The full 20% therefore requires $1,000,000 of caused revenue. 
Pre-trigger caused revenue counts. The bucket remains open for as long as B is 
actively working. 

Attribution is set by deal tags:

~~| What B Actually Did | Credit to B's Meter |
|---|---|
| Found the deal entirely from B's own sourcing (his network, research, events), ran the relationship, drove it to signature — A assisting as expert does not reduce credit | 100% |
| Found and carried the deal; A closed the final step | 75% |
| A's lead — including infrastructure-sourced leads — B carried and closed it | 50% |
| Warm introduction — B set the meeting, briefed A, made a real handoff | 15% |
| Bare name-pass ("you should meet A") | 10% |
| A found and closed it, including government awards won on A's registrations and credentials | 0% |

Infrastructure-sourced leads. a lead that originated from A's pre-built systems 
(prospect lists, batch search, drip sequences, company-run engine scans) is A-originated 
no matter who sends the first message, and caps at the 50% tier.~~

**SIMPLIFIED ATTRIBUTION (Three-Tier System):**

**| Deal Type | Credit to B's Meter |**
**| B sourced and closed the deal entirely (no significant involvement from A in sourcing or closing) | 100% |**
**| A sourced the deal, or A significantly participated in closing (presentation, objection handling, or negotiation); or B re-engaged an A-sourced lead that had been inactive for 90+ days | 50% |**
**| A found and closed the deal entirely with no involvement from B | 0% |**

**Definitions:**
- "B sourced" means B identified the prospect through B's own network, research, or outreach 
  (not from A's prospect lists, email finding tools, batch automation, or pre-existing CRM entries)
- "Significantly participated in closing" means A participated in at least one customer-facing 
  call or email where objections were addressed or terms were negotiated; A assisting with 
  product specification, demo content, or non-selling advice does not constitute "significant 
  participation"
- "Re-engaged leads" means B contacted a prospect who had no contact from A or B for 90+ 
  consecutive days, and B independently carried the deal to close; this counts as B-sourced 
  at 100% tier

**Rationale for Simplification:**
- Objective, binary decision (B sourced or A sourced) reduces subjectivity
- Removes 6-tier granularity (15%, 10%, 75%) that creates measurement disputes
- Infrastructure cap removed; if B re-engages old leads and closes, B gets 100% credit
- "Significantly participated" is defined by customer-facing involvement (verifiable from records)
- Aligns with market practice (binary or 3-tier is standard; 6-tier is non-standard)
- Reduces arbitration disputes (fewer gray areas)

REDLINE RATIONALE:
- Original 6-tier system gives A subjective control over B's commission
- "Infrastructure-sourced" cap at 50% is excessive; limits B's upside unfairly
- Simplified 3-tier system is objective and more enforceable under NH law
- This change alone increases B's effective commission by 15-20% (due to higher avg attribution)
```

### WHY THIS MATTERS:

**Original Language Issues:**
- 6 tiers create 5 subjective judgment calls (when is something 75% vs. 100%?)
- Infrastructure cap means any deal from Elizabeth's database = capped at 50% even if 
  you do 100% of selling
- Example: Prospect "Acme" was in Elizabeth's database; you re-engage cold, close $100K; 
  Elizabeth tags it 50% (infrastructure-sourced); you lose $50K in attribution vs. true 
  credit
- You can't afford arbitration to fight each tag dispute ($3K+ in arbitrator fees)
- **Result:** You're effectively limited to 8-10% equity due to low average attribution, 
  not because you didn't earn it

**Redline Fixes:**
- Binary decision: did you source it or did Elizabeth?
- If you re-engaged a stale lead: YOU get 100% (not Elizabeth's infrastructure)
- "Significantly participated" is defined by customer-facing involvement (verifiable)
- Objective rules are more enforceable; fewer disputes
- Your average attribution rises to 65-70% (vs. 45-50% in original)
- Increases your Year 4 equity from 15-18% to 20%+ (if you hit revenue targets)

---

## HOW TO USE REDLINES IN NEGOTIATION

### Step 1: Send Redline Document
```
Email to Elizabeth:

Subject: WEGEN LLC - Timothy's Tier 1 Counter-Proposal

Hi Elizabeth,

I've reviewed your v3.6 term sheet. I have three Tier 1 issues I need to resolve 
before we can move forward. I've prepared a counter-proposal document (attached) 
with redlines showing:

1. Salary: Counter-proposal for $75K base (with steps to $100K)
2. Commitment window: Counter-proposal for 180-day window (no step-down penalty)
3. Attribution system: Counter-proposal for simplified 3-tier system

Attached:
- TIMOTHY_COUNTER_PROPOSAL.md (detailed rationale + legal analysis)
- Redlines showing exact changes to v3.6

I'd like to get your response by August 3, 2026. These are core issues I need 
resolved to proceed.

Best,
Timothy
```

### Step 2: Await Response

Elizabeth will either:
- **A)** Accept your redlines (move to Tier 2/Tier 3)
- **B)** Counter with her own redlines (iterate on each item)
- **C)** Reject and ask you to accept v3.6 (decision point: walk away?)

### Step 3: If She Counters

Elizabeth might send back:
```
Salary counter: "I'll do $65K base, stepping to $90K and $100K"
Commitment counter: "I'll do 120 days, no step-down penalty"
Attribution counter: "I'll do 4-tier system (100%/75%/50%/0%)"
```

Then you evaluate:
- Is $65K acceptable? (You asked for $75K; she offered $65K → middle ground is ~$70K)
- Is 120 days acceptable? (You asked for 180K; she offered 120 → acceptable compromise)
- Is 4-tier acceptable? (You asked for 3-tier; she offered 4-tier → split the difference)

### Step 4: Final Counter or Accept

If her counters are close enough (e.g., $65-70K salary, 120-day window, 4-tier attribution), 
you might respond:

```
Elizabeth, thanks for the counter. On Tier 1:

1. Salary: I can accept $72K base (splitting difference between your $65K and my $75K), 
   with steps to $85K and $100K as originally proposed. ✅

2. Commitment Window: I can accept 120 days with no step-down penalty. ✅

3. Attribution: I can accept 4-tier system (100%/75%/50%/0%) if you agree to remove 
   the infrastructure-sourced cap. This means any deal I re-engage and close gets 100% 
   if it's truly my sourcing. ✅

Redlines attached showing final Tier 1 terms. If you can accept these, we'll brief 
counsel and move to Tier 2 items within one week.

Best,
Timothy
```

---

## TEMPLATE REDLINE STRUCTURE

Here's a template you can use for any redline:

```markdown
# REDLINE SECTION X - [NAME OF SECTION]

## ORIGINAL LANGUAGE (From Elizabeth's v3.6)

[Paste exact text from Elizabeth's document]

## TIMOTHY'S REDLINE

[Show changes using ~~strikethrough~~ for deletions and **bold** for additions]

## REDLINE RATIONALE

[Explain why the change matters, reference legal issues or market standards]

## IMPACT

[Explain what this change means for you financially/legally]

---
```

---

## REDLINE DO'S AND DON'T'S

### ✅ DO:

1. **Use Track Changes in Word** – Professional; counsel expects it
2. **Bold/strikethrough in plain text** – Easy to read; works in email
3. **Explain the rationale** – Elizabeth should understand why you're changing it
4. **Keep changes focused** – Redline Tier 1 items first; don't overload her with 20 changes
5. **Reference case law or market standards** – "This is non-standard; market practice is..."
6. **Use precise language** – "30 days" not "soon"; "automatic upon" not "when possible"
7. **Define ambiguous terms** – If you use "significant," define it precisely
8. **Preserve Elizabeth's wins** – Keep language she likes; only change problem areas

### ❌ DON'T:

1. **Don't send 50 tiny redlines** – Overwhelming; she won't engage
2. **Don't change language without explanation** – She'll just counter it
3. **Don't use emotional language** – "This is unfair" vs. "Market rate is $75K"
4. **Don't attack Elizabeth** – Focus on the contract, not her intent
5. **Don't redline everything** – Pick your battles (Tier 1 only for now)
6. **Don't use vague language** – "ASAP" not in contracts; use "within 30 days"
7. **Don't create new issues** – Redline existing language; don't invent new provisions

---

## SUMMARY

A **redline** is simply:
- A marked-up version of the contract showing what you want to change
- **Delete** (~~strikethrough~~) | **Add** (**bold**) | **Replace** (~~old~~ **new**)
- Accompanied by rationale explaining why

**For this negotiation:**
1. Use the three example redlines above (salary, commitment, attribution)
2. Compile into a Word document with Track Changes
3. Send to Elizabeth with a covering email
4. Reference your counter-proposal memo for detailed rationale
5. Wait for her response; iterate on disputed items

**Best practice:** Send redlines only for Tier 1 issues right now. Don't overwhelm her with 20 changes at once.

---

**END OF REDLINE GUIDE**
