# Best MCP Servers for the bda-svc Prompt and BBox Workflow

## Executive recommendation

Your project is a narrow, research-oriented local CLI system, not a general agent platform. In the current repo, `bda-svc` runs on local entity["company","Ollama","llm tooling company"] vision-language models, keeps detection and assessment prompts in YAML, supports the live target classes `buildings` and `military_equipment`, converts returned boxes into pixel coordinates, creates padded crops, draws scene overlays, and already produces evaluation artifacts such as bbox comparison images and LLM-as-a-judge logs. That architecture strongly favors MCP servers that improve local context access, structured experiment retrieval, and evidence-backed review loops, not generic “AI productivity” plugins. fileciteturn7file0L1-L1 fileciteturn8file0L1-L1 fileciteturn9file0L1-L1 fileciteturn18file0L1-L1 fileciteturn19file0L1-L1 fileciteturn21file0L1-L1 fileciteturn22file0L1-L1 fileciteturn23file0L1-L1 fileciteturn25file0L1-L1

The best fit is a small stack, not a large stack. My recommendation is to adopt **Filesystem MCP first**, then **SQLite MCP**, then **Qdrant MCP**. Add **Playwright MCP** only if your bbox review artifacts are browser-based or you are willing to make them browser-based. Add **GitHub MCP**, **Context7 MCP**, and one external search server such as **Tavily MCP** or **Brave Search MCP** later, when you need more repo intelligence or more web-grounded research retrieval. That ordering best matches your stated priorities: prompt engineering, bbox review, research retrieval, experiment comparison, low cost, and local/privacy friendliness. citeturn2search6turn2search11turn5search0turn9view0turn6search0turn1search0turn8search0turn12search0turn11search3

The direct answers to your six questions are these. **For prompting workflow**, the best servers are Filesystem, SQLite, Qdrant, then Context7 and GitHub as secondary aids. **For bbox review and spatial-debug**, the best servers are SQLite plus Filesystem, with Playwright added only when artifacts are web-native. **For research retrieval and source grounding**, the best servers are Qdrant for your own corpus, Context7 for software docs, and Tavily or Brave for external web search. **For mostly free or low-cost usage**, Filesystem, Playwright, SQLite, Qdrant OSS, and GitHub MCP are the strongest; Context7 has a free tier, Tavily has a free tier, and Brave includes free monthly credits. **For local or self-hosted usage**, Filesystem, SQLite, Qdrant, and Playwright are the strongest. **For likely overkill**, I would call out enterprise vector stacks beyond Qdrant, generic memory servers, and unrelated business-tool MCPs. citeturn2search6turn5search0turn14search0turn14search2turn6search0turn1search0turn13search0turn13search5turn13search2

## Ranked shortlist table

| Rank | MCP server | Best use for this project | Why it ranks here | Cost | Local / privacy fit | Recommendation | Evidence |
|---|---|---|---|---|---|---|---|
| 1 | Filesystem MCP | Prompt files, doctrine, review artifacts, logs, local notes | Fastest path to better prompting because it exposes the exact files you already iterate on: prompt YAML, doctrine, eval outputs, bbox overlays, and notes | Free | Excellent | Use now | Official local-server docs and reference-server listing. citeturn2search6turn2search11turn4search2 |
| 2 | SQLite MCP | Structured A/B experiments and evidence triage | Best way to compare prompt variants, false positives, IoU slices, and control-case regressions once you materialize results into a small local DB | Free | Excellent | Use now | `mcp-sqlite` provides catalog and SQL tools; current release history indicates recent maintenance. citeturn5search0 |
| 3 | Qdrant MCP | Semantic retrieval over papers, model cards, model notes, research corpus | Strongest MCP option for a local knowledge base once your corpus is too large for folders and grep; supports local path and OSS/self-hosted deployments | Free OSS / paid cloud optional | Strong | Use now if corpus is already sizable; otherwise use next | Official Qdrant MCP docs and Qdrant local/self-hosted docs. citeturn9view0turn14search0turn14search2turn13search4 |
| 4 | Playwright MCP | Bbox review sheets, visual-grounding review, browser-native comparison boards | High value only if your review loop is or becomes browser-based; excellent for deterministic navigation, snapshots, and screenshots of review dashboards | Free | Good | Use later, conditional | Official Playwright MCP docs. citeturn6search0turn6search1 |
| 5 | GitHub MCP | Repo context, issues, PRs, code search, workflow context | Official and mature, but less central than local-file access for a small CLI project whose best artifacts will often remain local and not yet pushed | Mostly free; some tools inherit paid feature requirements | Medium | Use later | GitHub documents the official server and says it is maintained by GitHub; toolsets can be restricted. citeturn1search0turn1search1turn1search7 |
| 6 | Context7 MCP | Up-to-date software docs | Excellent for framework and library docs, weak for papers and model cards; useful for Ollama, Playwright, Qdrant, SDK, and client docs | Free tier; low-cost paid tiers | Mixed | Use later | Official Context7 install and pricing docs. citeturn8search0turn13search0 |
| 7 | Tavily MCP | External web research, extraction, crawl, map | Best external-search MCP if you need web-grounded research beyond your local corpus; stronger extraction workflow than most search-only servers | Free tier, then paid | Cloud-first | Use later | Official Tavily MCP docs and pricing. citeturn12search0turn13search6 |
| 8 | Brave Search MCP | Low-cost external search with better privacy posture than many search APIs | Credible alternative to Tavily if search breadth and cost matter more than extraction/crawl workflows | Free monthly credits, then usage pricing | Cloud-first, privacy-leaning | Use later | Official Brave Search pricing and official ecosystem listings/docker catalog. citeturn13search2turn11search0turn11search3 |

## Highest priority MCP servers to adopt now

### Filesystem MCP

Filesystem MCP is the highest-value first adoption because your project’s critical knowledge already lives in files. Your detection and assessment prompts are in `config.yaml`, doctrinal guidance is in `doctrine.yaml`, the pipeline uses prompt templates directly from those files, and your evaluation flow already writes bbox and reasoning artifacts. That makes Filesystem MCP the shortest path to grounded prompt iteration: the assistant can read the prompt, inspect the doctrine, open the review artifacts, and tie recommendations to the actual case files instead of speaking in generalities. fileciteturn8file0L1-L1 fileciteturn9file0L1-L1 fileciteturn18file0L1-L1 fileciteturn21file0L1-L1 fileciteturn23file0L1-L1

Concretely, this would let you ask questions like: “Show me every detection instruction that could increase adjacent-building false positives,” “Open the last twenty bbox review artifacts for building scenes,” or “Compare the doctrine wording for buildings with the actual false-positive cases.” That is exactly the kind of local-context access MCP resources and tools were designed for, and the official docs explicitly use Filesystem as a core local reference server. citeturn2search6turn2search11turn4search2

### SQLite MCP

SQLite MCP is the strongest day-to-day improvement for your prompt-lab evidence loop. Your repo already has evaluation logic that computes object matches via IoU, tracks false positives and false negatives, packages CSV-style outputs, writes bbox comparison images, and logs LLMaaJ judgments. If those results are normalized into a small SQLite database, you gain exact retrieval instead of folder spelunking. fileciteturn21file0L1-L1 fileciteturn22file0L1-L1 fileciteturn23file0L1-L1 fileciteturn25file0L1-L1

That would materially improve all five of your stated pain points. You could slice cases by `target_type`, inspect low-IoU detections, isolate “adjacent-building” failures, compare prompt variant A versus B, and quantify whether a localization tweak preserved control-case behavior. The `mcp-sqlite` package is also a better fit than heavier database MCPs for a small local research project because it is free, SQLite-native, exposes catalog plus SQL tools, and appears recently maintained on PyPI. citeturn5search0

### Qdrant MCP

Qdrant MCP is the best third server if you expect a real corpus: papers on visual grounding, referring expressions, detection prompting, model cards, eval notes, postmortems, sample prompts, and maybe even distilled summaries of LLMaaJ logs. This is where a vector-backed MCP becomes meaningfully better than Filesystem or SQLite. It supports semantic retrieval and metadata filtering, and the official server supports either a Qdrant URL or a local path. Qdrant itself is open source, self-hostable, and even supports local mode in its Python client, which keeps it aligned with your preference for local-friendly tooling. citeturn9view0turn14search0turn14search2turn14search12

I would not make Qdrant your first server because it needs ingestion discipline. But once you have enough material that keyword search stops working well, Qdrant becomes the best MCP option for questions like: “Find literature and internal notes about background-building suppression,” “Retrieve all evidence relevant to bbox tightness for partially occluded vehicles,” or “Show me prior experiments similar to this failure case, even if they used different wording.” That is a clear project-specific gain, not generic RAG theater. citeturn9view0turn14search11

## Worth considering later

### Playwright MCP

Playwright MCP is the best bbox-review server only under one condition: your review flow is browser-native or can become browser-native with very little work. Its official MCP server gives structured browser automation, accessibility snapshots, and screenshots without needing a vision model. That is excellent for local HTML review sheets, prompt-comparison dashboards, case browsers, or artifact triage pages. citeturn6search0turn6search1

For your current repo, the evaluation code already writes bbox overlay images and organized output folders. If you wrap those outputs in a simple local HTML index, Playwright immediately becomes valuable for deterministic walkthroughs such as “open the next ten building false positives,” “capture screenshots of model-vs-human bbox disagreements,” or “navigate only cases where IoU is below threshold.” If you do not have browser-based artifacts, then Playwright is not a first-wave adoption. That recommendation is an inference from your existing artifact flow plus Playwright’s browser-first design. fileciteturn21file0L1-L1 fileciteturn23file0L1-L1 citeturn6search0

### GitHub MCP

The official entity["company","GitHub","software company"] MCP server is real, mature, and maintained by GitHub. GitHub’s own docs say the server is provided and maintained by GitHub, available to all GitHub users, and configurable by toolsets so you can narrow the available capabilities. That matters because tool minimization is good both for usability and for security. citeturn1search0turn1search1turn1search7

I do not rank it higher because your best prompt and bbox evidence looks likely to live in local prompt files, local review artifacts, and local experiment outputs rather than in repo issues and PR threads. Still, GitHub MCP becomes worthwhile if your team starts storing experiment writeups in issues, prompt changes in PRs, or model behavior notes in discussions. For a one-repo research loop, I would adopt it after Filesystem and SQLite, not before them. fileciteturn7file0L1-L1 citeturn1search5

### Context7 MCP

Context7 MCP, maintained by entity["company","Upstash","serverless infra company"], is a very good software-documentation server. Its official docs position it as a way to inject current, version-specific docs into MCP-aware clients, and its free plan includes 1,000 API calls per month. That is useful for software ecosystems around your workflow, especially Ollama clients, MCP host configuration, Playwright, Qdrant, and related frameworks. citeturn8search0turn13search0

It is not, however, the best server for your core research corpus. Context7 is strongest for library and framework documentation, not for papers, model cards, or image-analysis case notes. I therefore recommend it as a secondary “software docs” server, not as the backbone of your prompt-lab research stack. citeturn7search0turn8search0

### Tavily MCP and Brave Search MCP

For external research retrieval, the strongest official MCP path I found was the server from entity["company","Tavily","search api company"]. Tavily’s official docs describe search, extraction, crawl, and map capabilities, and its pricing docs show a free tier with 1,000 API credits per month. That makes it a strong “when local corpus is insufficient” choice for finding papers, model cards, blog posts, and docs, then extracting the relevant text. citeturn12search0turn13search6

A good alternate is the official Brave Search MCP path associated with entity["company","Brave","web browser company"]. Brave’s official API pricing provides free monthly credits and emphasizes privacy, and the official MCP ecosystem listings and Docker catalog confirm a real MCP server path. I rank Brave below Tavily for your use case because the source evidence I found for Tavily’s MCP was stronger and because Tavily’s extraction and crawl workflow is more obviously useful for research triage. If you mainly want cheaper, simpler search with a privacy-forward posture, Brave is the better alternative. citeturn13search2turn11search0turn11search3

## Not worth the complexity for this project

I do not recommend jumping straight to heavy hosted vector or knowledge platforms such as enterprise-grade cloud vector stacks, generalized memory infrastructures, or broad “all your business tools in one agent” MCP bundles. That is not because they are bad tools. It is because your current system is a small, local, single-purpose CLI focused on prompt and bbox behavior. Simpler local primitives already match the repo’s shape: files, structured outputs, and a limited research corpus. That is an inference from the present repo architecture and from the availability of lighter-weight local options like Filesystem, SQLite, and Qdrant local mode. fileciteturn7file0L1-L1 fileciteturn18file0L1-L1 fileciteturn21file0L1-L1 citeturn2search6turn5search0turn14search2

I also would not prioritize generic memory servers, even official ones, for this phase. They are not a clean match to your actual problem statement. You are not trying to create a persistent personal assistant memory; you are trying to tighten visual detection prompts, analyze localization errors, and retrieve evidence. A structured experiment ledger and a curated document corpus serve that purpose much better. citeturn15search0turn5search0turn9view0

Finally, I would skip generic chatbot-oriented MCP directories and marketplace-driven bundle installs as a decision driver. For this project, popularity is a weak signal. Clear alignment to prompt iteration, bbox debugging, and evidence handling is the right signal. fileciteturn8file0L1-L1 fileciteturn25file0L1-L1

## Per-server rationale with project-specific use cases

### Filesystem MCP

**What it is:** an official local reference server for controlled file access. **Why it helps this project:** it gives the model direct access to the real prompt templates, doctrine files, output folders, review images, CSVs, and notes that already drive your workflow. **Primary use case:** document/context access and artifact review. **Cost:** free. **Local/privacy:** excellent. **Maintenance signal:** official reference server, current docs updated recently. **Recommendation:** use now. citeturn2search6turn2search11turn4search2

The project-specific win is immediate. Your prompt logic is file-based, and your eval outputs are file-based. Filesystem MCP lets you ask grounded questions against those materials directly, which is the single most direct way to improve prompt engineering in this repo. fileciteturn8file0L1-L1 fileciteturn18file0L1-L1 fileciteturn21file0L1-L1

### SQLite MCP

**What it is:** an MCP server for querying SQLite databases. **Why it helps this project:** it turns prompt iteration from an anecdotal process into a queryable evidence loop. **Primary use case:** experiment comparison and evidence triage. **Cost:** free. **Local/privacy:** excellent. **Maintenance signal:** recent PyPI release history. **Recommendation:** use now. citeturn5search0

The right design is to materialize every run into tables such as `experiments`, `images`, `detections`, `matches`, `false_positives`, `false_negatives`, `llmaaj_scores`, and `notes`. Then the model can answer the questions you actually care about: whether a prompt reduced background-building false positives, whether it hurt control cases, and whether localization improved without introducing new merges or misses. That is a much sharper fit than a generic memory server. This is partly inference from your eval code and partly based on SQLite MCP’s capabilities. fileciteturn22file0L1-L1 fileciteturn23file0L1-L1 fileciteturn25file0L1-L1 citeturn5search0

### Qdrant MCP

**What it is:** the official MCP server for Qdrant, running as a semantic memory layer on top of the vector database. **Why it helps this project:** it is the best MCP-native way to search across a mixed corpus of papers, model cards, failure analyses, notes, and prompt experiments when keyword search becomes brittle. **Primary use case:** research retrieval and source grounding. **Cost:** free OSS; paid cloud optional. **Local/privacy:** strong, including self-hosting and local modes. **Maintenance signal:** official vendor implementation with current docs. **Recommendation:** use now if you already have a meaningful corpus; otherwise use later. citeturn9view0turn14search0turn14search2turn13search4

The project-specific win is not generic “memory.” It is retrieval over semantically similar failure cases: background-building suppression, adjacent-target confusion, and localization guidance for buildings versus military equipment. Qdrant is where you would index curated case writeups, distilled literature findings, and model-card notes with metadata like `target_type`, `issue_type`, `model`, and `prompt_hash`. citeturn9view0turn14search11

### Playwright MCP

**What it is:** the official Playwright MCP server for browser automation through structured page snapshots. **Why it helps this project:** it can run deterministic review loops over browser-based bbox dashboards, side-by-side prompt comparison pages, and local experimental case browsers. **Primary use case:** bbox review, visual-grounding review, and spatial-debug workflows. **Cost:** free. **Local/privacy:** good, runs locally, but browser-bound. **Maintenance signal:** official docs and active releases. **Recommendation:** use later, and only if artifacts are browser-native or can cheaply become browser-native. citeturn6search0turn6search1turn6search2

I would not use it to replace your current image pipeline. I would use it to make that image pipeline easier to review at scale. If you generate one lightweight HTML page per experiment batch, Playwright becomes a strong MCP fit. If not, Filesystem will carry more weight. That is an inference from your repository’s current output shape. fileciteturn21file0L1-L1 fileciteturn23file0L1-L1

### GitHub MCP

**What it is:** GitHub’s official MCP server. **Why it helps this project:** it brings repository files, issues, PRs, actions, and code context into the MCP layer, and GitHub says it is maintained by GitHub and configurable by toolsets. **Primary use case:** repository context, code search, and team coordination context. **Cost:** mostly free, with some server tools inheriting their underlying feature/licensing requirements. **Local/privacy:** moderate, depending on whether you use the hosted endpoint or local container path. **Maintenance signal:** very strong. **Recommendation:** use later. citeturn1search0turn1search1turn1search5turn1search7

For this project, GitHub MCP is most useful once prompt engineering becomes more team-mediated. If prompt changes, eval criteria, and review decisions start living in PRs and issues, GitHub MCP becomes much more valuable. Before that, local files and SQLite are simply closer to the work. fileciteturn7file0L1-L1

### Context7 MCP

**What it is:** an MCP server for current software library and framework documentation. **Why it helps this project:** it reduces stale-doc errors when configuring MCP clients, Qdrant, Playwright, Ollama-side integrations, and related tools. **Primary use case:** technical docs retrieval. **Cost:** free tier available; paid tiers for heavier/private usage. **Local/privacy:** mixed, because the service is fundamentally cloud-backed even if you can run the MCP client-side component locally. **Maintenance signal:** strong, with current docs and pricing. **Recommendation:** use later. citeturn8search0turn13search0

The fit is real but secondary. Context7 is for software documentation quality, not for your core bbox science loop. It will save time when the assistant needs accurate tool and SDK docs, but it will not by itself explain why one building-localization prompt outperforms another. citeturn7search0turn8search0

### Tavily MCP

**What it is:** an official MCP server for search, extraction, crawling, and mapping over the live web. **Why it helps this project:** it is the best external-gap filler when your local corpus does not contain the paper, model card, or implementation note you need. **Primary use case:** external research retrieval and source grounding. **Cost:** free tier plus paid scaling. **Local/privacy:** cloud-first. **Maintenance signal:** strong official docs. **Recommendation:** use later. citeturn12search0turn13search6

Tavily becomes useful for targeted retrieval such as “find recent model cards or papers discussing grounding and localization,” then extract only the relevant sections into your evidence loop. That is materially useful, but still not worth placing ahead of Filesystem or SQLite for your current workflow. citeturn12search0

### Brave Search MCP

**What it is:** an MCP path for Brave-powered search, with official ecosystem listings and Brave’s own API pricing. **Why it helps this project:** it is a credible lower-cost, privacy-leaning alternative for external search. **Primary use case:** external source discovery. **Cost:** low; includes free monthly credits. **Local/privacy:** cloud-first but more privacy-forward than many alternatives. **Maintenance signal:** decent, though I found weaker first-party MCP-specific docs than I found for Tavily. **Recommendation:** use later, and mainly if you prefer it over Tavily’s research/extraction feature set. citeturn13search2turn11search0turn11search3

I would choose Brave over Tavily when cost sensitivity and query privacy matter more than crawling and extraction workflow depth. Otherwise I would choose Tavily first. That ranking is an inference from the available documentation and pricing. citeturn12search0turn13search2

## Adoption order

Start with **Filesystem MCP** and scope it tightly to the repo root, your papers/notes folder, and the evaluation output directories. That gives immediate value with almost no workflow change. Next, create a very small **SQLite experiment ledger** and connect it through SQLite MCP. At that point your prompting workflow becomes evidence-driven, because every future review can be tied to queryable data instead of ad hoc folder review. citeturn2search6turn5search0

Then add **Qdrant MCP** if and only if your corpus is already large enough that keyword search is failing. If you do not yet have enough papers, notes, and postmortems to justify a vector index, defer it. After that, add **Playwright MCP** only if you standardize review artifacts into local HTML pages or dashboards. Then add **GitHub MCP** if GitHub issues and PRs become a relevant knowledge source. Finally, add **Context7** and one external search server, preferably Tavily first and Brave second, when you need more live external grounding. citeturn9view0turn6search0turn1search0turn8search0turn12search0turn13search2

If you want the shortest version of the adoption plan, it is this: **Filesystem first, SQLite second, Qdrant third, Playwright only when artifacts justify it, everything else after those four.** That order maximizes day-to-day prompt-engineering value while keeping cost and complexity low. fileciteturn8file0L1-L1 fileciteturn25file0L1-L1

## Risks, limitations, and open questions

The biggest operational risk is MCP privilege sprawl. The official MCP security best-practices document recommends scope minimization, sandboxing, restricted filesystem and network access, stdio for local servers where possible, and careful privilege granting. That matters here because your project is privacy-sensitive and because local artifact access is precisely what makes these servers powerful. citeturn17search5

There is also a specific caution around Git-style MCP servers. The Python `mcp-server-git` package is maintained and still updated, but it has had a path-validation vulnerability, with advisories recommending upgrade to fixed versions in late 2025. If you ever adopt Git MCP, pin it to a patched version, restrict the repository path, and sandbox it. That is not a reason to avoid all MCP use; it is a reason to apply least privilege and version discipline. citeturn16search0turn17search0turn17search2turn17search5

The main workflow limitations are practical. **Playwright** is only high value if your reviewers use browser-based artifacts. **Qdrant** only pays off if you maintain a real corpus and metadata discipline. **Context7**, **Tavily**, and **Brave** are useful but less privacy-friendly because they depend on remote services. **GitHub MCP** is strong but secondary if your most valuable evidence never leaves local working directories. Those are not defects; they are fit constraints. citeturn6search0turn9view0turn8search0turn12search0turn13search2turn1search0

The open questions that would most change the final ranking are these. First, are your bbox review sheets already HTML or still image-and-CSV based. Second, are you willing to normalize experiment outputs into SQLite. Third, how large is your research corpus right now: a few folders or a few hundred documents. Fourth, which MCP client will your team actually use, since client UX for resources versus tools still varies. If the answers are “images,” “not yet,” and “small corpus,” then the answer is even simpler: start with Filesystem only, then add SQLite as the first real expansion. fileciteturn21file0L1-L1 fileciteturn23file0L1-L1 citeturn3search0turn4search3turn5search0