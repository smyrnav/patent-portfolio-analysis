# Fact checks

The outside facts this project relies on, and how well each one is supported. Status reflects what I found on 31 October 2026.

**Confirmed** means an official or primary source. **Secondary** means encyclopedia or trade sources, so check them before relying on the detail.

## Company history

| Claim | Status | Source |
|---|---|---|
| Nokia completed its Alcatel-Lucent acquisition in November 2016 | Secondary | [Wikipedia: Alcatel-Lucent](https://en.wikipedia.org/wiki/Alcatel-Lucent) |
| Alcatel and Lucent merged at the end of 2006 | Secondary | [Wikipedia: Alcatel-Lucent](https://en.wikipedia.org/wiki/Alcatel-Lucent) |
| Lucent spun off Avaya | Secondary, sources differ on 2000 or 2001 | [Converge Digest](https://convergedigest.com/tracing-the-dna-of-nokia-through-its-many-mergers-and-acquisitions/?amp=1) |
| Lucent spun off Agere in 2002 | Secondary | [Converge Digest](https://convergedigest.com/tracing-the-dna-of-nokia-through-its-many-mergers-and-acquisitions/?amp=1) |
| Nokia Siemens Networks was a joint venture of Nokia and Siemens units | Secondary. I didn't confirm the formation date | [Wikipedia: Nokia Networks](https://en.wikipedia.org/wiki/Nokia_Networks) |
| Nokia Siemens Networks bought Motorola's network business, closing in April 2011 | Secondary | [Telecoms.com](https://www.telecoms.com/5g-6g/nsn-seals-motorola-acquisition-deal) |
| Nokia bought out Siemens' stake in August 2013 | Secondary | [Wikipedia: Nokia Networks](https://en.wikipedia.org/wiki/Nokia_Networks) |
| Microsoft completed its purchase of Nokia's phone business in April 2014 | Reported | [The Next Web](https://thenextweb.com/news/microsoft-completes-acquisition-nokias-devices-services-business-price-slightly-higher-7-2b?utm_reader=feedly) |
| Nokia kept its patents and gave Microsoft a 10-year non-exclusive licence | Reported, also described in Nokia's filing | [Nokia 20-F, FY2014](https://www.sec.gov/Archives/edgar/data/0000924613/000119312515098475/d861743d20f1.pdf) |
| Nokia completed its Infinera acquisition on 28 February 2025 | Confirmed | [Nokia 20-F, FY2025](https://www.sec.gov/Archives/edgar/data/924613/000162828026015034/nok-20251231.htm) |

**Still unknown:** which patents went with Avaya and Agere. A name on a patent doesn't settle that, so Q13 stays open.

## Nokia's business structure

| Claim | Status | Source |
|---|---|---|
| Reportable segments are Network Infrastructure, Mobile Infrastructure and Portfolio Businesses | Confirmed | [Nokia Q3 2026 report](https://www.sec.gov/Archives/edgar/data/924613/000110465926117972/tm2628115d1_6k.htm) |
| Network Infrastructure includes Optical Networks, IP Networks and Fixed Networks | Confirmed | Same report |
| Mobile Infrastructure includes Core Software, Radio Networks and Technology Standards | Confirmed | Same report |
| Technology Standards manages the patent portfolio and licensing, and was formerly Nokia Technologies | Confirmed | Same report |
| Portfolio Businesses comprise Site Implementation and Outside Plant, and Microwave Radio | Confirmed | Same report |
| Fixed Wireless Access CPE was sold, and an agreement to sell Enterprise Campus Edge was signed | Confirmed | Same report |
| IP Networks grew 43% and Optical Networks 18% in Q3 2026, at constant currency | Confirmed | [Nokia Q3 2026 release](https://www.nasdaq.com/press-release/nokia-corporation-interim-report-q3-2026-2026-10-22) |
| Nokia's portfolio has over 20,000 patent families | Reported in January 2025, no newer figure found | [Trade report](https://tecknexus.com/5gnews-all/nokia-achieves-7000-essential-5g-patents-milestone/) |

## The "Needs review" names

| Name pattern | What I found | Effect on the analysis |
|---|---|---|
| Alcatel cable names | Alcatel Cable became Nexans in 2000 ([Wikipedia](https://en.wikipedia.org/wiki/Alcatel)) | Probably left the family |
| Alcatel Optronics | Optical business sold to Avanex in 2003 ([Wikipedia](https://en.wikipedia.org/wiki/Alcatel)) | Probably left the family |
| Alcatel mobile and TCL names | Joint venture formed in 2004, stake sold back to TCL in 2005 ([Wikipedia](https://en.wikipedia.org/wiki/Alcatel)) | Probably left the family |
| Alcatel Espace, Telspace | Space units passed to Thales around 2006 ([Wikipedia](https://en.wikipedia.org/wiki/Alcatel)) | Possibly left, needs detail |
| Alcatel Submarcom, Submarine | Owned by Nokia 2016–2024, then 80% sold to the French state ([Wikipedia](https://en.wikipedia.org/wiki/Alcatel_Submarine_Networks)) | Mostly left |
| Alcatel Vacuum | Not confirmed | Unknown |
| Alsthom, Commissariat, INRIA names | Not checked. The last two look like joint ownership | Unknown |

These names cover only 178 patents, about 0.5% of the recount, so they don't change the overall picture. Selling a business doesn't always move every patent, so this is a guide, not proof of ownership.

## Patent rules and data sources

| Claim | Status | Source |
|---|---|---|
| US maintenance fees fall due at 3.5, 7.5 and 11.5 years after grant, and patents lapse if unpaid | Confirmed | [USPTO: Maintain your patent](https://www.uspto.gov/patents/maintain) |
| Design and plant patents have no maintenance fees | Confirmed | [USPTO: Maintain your patent](https://www.uspto.gov/patents/maintain) |
| US patents generally run 20 years from filing, or from the earliest related filing under certain claims | Confirmed | [35 U.S.C. § 154](https://www.law.cornell.edu/uscode/text/35/154) |
| Fees are $2,150, $4,040 and $8,280 for large entities | Check before use, as fees change | [USPTO fee schedule](https://www.uspto.gov/learning-and-resources/fees-and-payment/uspto-fee-schedule) |
| The USPTO publishes maintenance fee events from 1981 onwards | Listing found, not downloaded yet | [Data.gov listing](https://catalog.data.gov/dataset/patent-grant-maintenance-fee-events-september-1-1981-present-7d26f) |
| ETSI's database lists patents declared essential, and it's free to search | Confirmed, not used yet | [ETSI IPR database](https://ipr.etsi.org) |
| ETSI does not check whether declared patents are truly essential | Confirmed | [ETSI SR 000 314](https://www.etsi.org/deliver/etsi_sr/000300_000399/000314/02.38.01_60/sr_000314v023801p.pdf) |

**What this means for the analysis:**

- Filing date + 20 years is an estimate of expiry, not an exact date. Patents can lapse earlier if fees aren't paid, and term rules can move the date in either direction.
- A patent declared essential to 5G hasn't necessarily been proven essential.
