# Glossary — every term in this project, in plain language

Written for a reader who has never touched patent data. Each definition says what the thing *is*, then why it matters *here*.

## Patent basics

**Patent** — a deal with the state: an inventor publishes exactly how their invention works, and in exchange gets the exclusive right to it for about 20 years. Because everything is published, patents are a rare public window into what companies are inventing.

**Claims** — open any patent PDF and skip to the end: after all the description and drawings there is a numbered list of sentences ("1. A method for…, 2. The method of item 1, where…"). That list is the claims: the inventor stating, in their own words, exactly what they invented and own — like the boundary description in a property deed. Everything before it is storytelling; the numbered list is the legal fence. When this project says "a human reads the claims," it means a person opens the patent, reads that numbered list, and decides what the patent is really about — because the patent office's category labels are wrong surprisingly often.

**Assignee** — the company or person recorded as owning the patent. Complication: one company files under dozens of name variants ("Airbus Operations GmbH", "EADS Deutschland", spelling mistakes), which is why we had to research names before counting anything.

**Patent family** — one invention, filed in several countries, appears in the data as several separate patents. The family groups them so we count the *invention* once, not once per country. Without this, companies that file in many countries look artificially inventive.

**Publication vs grant** — a patent application is *published* (made public) about 18 months after filing; it is *granted* only after the patent office examines and approves it. Many applications never get granted. This project mostly counts publications, which show activity; grants show confirmed rights.

**Kind code** — a one- or two-letter suffix on a patent number (A1, B2…) saying what stage document this is: application, granted patent, correction. We check it so we don't count the same stage twice.

**Priority date / filing date** — the priority date is when the invention was first filed anywhere in the world; the filing date is when this particular application was filed. We use priority/filing dates to put inventions on a timeline.

**CPC code** — a category label the patent office stamps on each patent, like "H04B 7/185 = satellite radio systems." A librarian's label: fast, standardised, and wrong surprisingly often. We use CPC codes to *find* patents that are probably about a topic — then a human reads the claims to confirm.

## How this project works

**Pool (technology bucket)** — one of the five groups we sort patents into, matching the capabilities a sovereign satellite system needs: SAT (satellite payload), ISL (links between satellites), GRD (ground stations and terminals), NET (integration with ordinary mobile networks), SEC (protection against jamming and unauthorised access).

**Census** — listing every company-name variant in the database that matches our search patterns, *before* counting. Like checking the guest list before the party.

**Eyeball review** — a human reading machine output with their own eyes instead of trusting it. How we caught an LED manufacturer filed under "Airbus" and a Brazilian first name filed under "Thales."

**Keep / drop / review** — the three verdicts of the eyeball review. Keep = genuinely this company. Drop = proven junk. Review = genuinely ambiguous, goes to the project owner for a decision.

**Peers table** — our clean working table in BigQuery (`satcom_peers_30y`): all patents of the five tracked companies since 1996, matched by exact reviewed names.

**Dry run** — asking BigQuery to check a query and report how much data it will scan, *without running it*. Our house rule: validate first, then run — it catches broken queries for free.

**Precision** — of the patents a bucket caught, how many actually belong there. A bucket with 85% precision mislabels 15 of every 100 patents.

**Recall** — of all the patents that truly belong in a bucket, how many the bucket actually found. High precision + low recall = accurate but blind to half the picture.

**The 85% bar** — our house rule: no bucket may be used in statistics until a human hand-checks a random sample of its patents and confirms at least 85 out of 100 genuinely belong in it. "Genuinely" means the human read the numbered sentences at the back of each patent and agreed with the machine. The previous categories scored 39–73% and were thrown out; that failure is why this rule exists.

**Hand-labelling / validation** — the machine sorts patents into buckets using the patent office's labels; a human then opens a sample of those patents, reads what the inventor claims to have invented, and records whether the machine was right. The share of "right" is the bucket's precision. The trust layer of the whole project — nothing gets compared or charted until the buckets pass.

**Cohen's kappa** — a score from 0 to 1 of how often two labelers agree on the same items, corrected for the agreement pure luck would produce. The standard way to prove labels are trustworthy is two *people* labelling the same patents; this project has one human, so kappa here measures me against the software first pass instead — a weaker check, reported as such.

**Sandbox table** — a temporary working table in our BigQuery dataset. Ours expire around the end of December 2026, which is why the heavy queries are time-boxed.

## Statistics in plain language

**Chi-square test (χ²)** — answers "is this pattern real, or could it be counting luck?" We compare what we actually counted (patents per company per bucket) against what we'd expect if company made no difference at all. A big gap between actual and expected means the mix of technologies really does differ by company. It never says *why*.

**p-value and the 0.05 threshold** — the probability of seeing differences at least this big by pure luck, if nothing real were going on. Under 0.05 (5%) we call the result "statistically significant" and treat it as probably-not-luck. It says nothing about whether the difference is big enough to care about — that's the next entry.

**Effect size / Cramér's V** — how strong the connection is, on a 0–1 scale. The p-value says "probably not luck"; Cramér's V says "and here's how much it matters." With enough data, a trivial difference can be "significant," so we always report both.

**Degrees of freedom** — a technical ingredient of the chi-square calculation, roughly "how many independent pieces of information went in." Reported so anyone can re-check the arithmetic.

**Standardized residuals** — after a chi-square says "companies differ," these per-cell scores show *which* company-bucket combinations drive the difference — e.g. "Nokia holds far more network-integration patents than chance would predict."

**Wilson interval (the "95% range")** — when we measure something from a sample ("85 of 100 sampled patents checked out"), the true value isn't exactly 85%. The Wilson interval gives the honest range it likely sits in (say 77–91%), and it stays reliable even with small samples. Wider range = less certainty = we need a bigger sample.

**Cochran–Armitage trend test / logistic regression** — two standard ways to test "is this share actually rising over the years?" instead of eyeballing a chart and hoping.

**Kruskal–Wallis test** — compares a lopsided measurement (like "how many citations does each patent get?" — most get zero, a few get hundreds) across several companies, without assuming the numbers follow a neat bell curve.

**Monte Carlo** — instead of one forecast, run the calculation thousands of times with randomly varied inputs and look at the spread of outcomes. Honest only when the randomness of the inputs is known from data; inventing the randomness produces a precise-looking fantasy.

**Sensitivity check** — redo the whole answer with slightly different assumptions and see if the conclusion flips. If a small nudge flips it, the conclusion was fragile and we say so.

## Satellite and business terms

**LEO / MEO / GEO** — orbit heights. LEO (low Earth orbit, a few hundred km up) is where Starlink and the proposed system fly: fast response, but each satellite covers a small area, so you need many. GEO (36,000 km) is where one satellite covers a continent. MEO is in between.

**Payload** — the part of the satellite that does the actual job (the communications equipment), as opposed to the platform that keeps it alive (power, propulsion).

**Inter-satellite link (ISL)** — a connection directly between two satellites in orbit, so traffic can travel through space without touching the ground. Lets a constellation work even where the customer controls no ground stations.

**Ground segment / user terminal** — the ground segment is the gateways and control systems on Earth; the terminal is the device an end user holds. The Nokia–ICEYE proposal says the customer nation owns all three layers: satellites, ground segment, terminals.

**NTN (non-terrestrial networks)** — the mobile-industry standards track (inside 3GPP, the body that defines mobile networks) for making satellites and ordinary phone networks work together. The technical basis for "complementing, not replacing" existing networks.

**Sovereign capability** — the customer nation owns and controls the infrastructure itself, instead of renting service from a foreign company it cannot command.

**Trade secret** — the anti-patent strategy: publish nothing, protect the invention by keeping it inside the building. SpaceX works this way (110 patent families vs Airbus's 19,488), which is why patent data can't see the strongest player.

**Standard-essential patent (SEP)** — a patent you cannot avoid infringing if you build to a technical standard (like 3GPP satellite networking). Owners must license SEPs on fair terms, but they still define who holds leverage.

**Freedom to operate** — whether you can actually sell a product without infringing someone's patents. Patent counts alone can never answer this; it takes a legal analysis. We flag where the question is sharp; we don't answer it.

**Joint venture (JV)** — a company owned by two parents (e.g. Airbus OneWeb Satellites). In our name review, JV names are the tricky ones: the patents belong to both parents at once.

**Build / buy / partner / license** — the four ways to obtain a capability: develop it yourself, acquire whoever has it, ally with them, or rent the rights. The five research questions all funnel into choosing between these for each technology the system needs.
