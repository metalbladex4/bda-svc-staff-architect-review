# Visually Prompted Benchmarks Are Surprisingly Fragile

- Source PDF: `Visually Prompted Benchmarks Are Surprisingly Fragile.pdf`
- Extraction method: `pdftotext -layout`
- Generated: `2026-04-02T15:21:31Z`

---

## Page 1

                                                             Visually Prompted Benchmarks Are Surprisingly Fragile

                                                                       Haiwen Feng∗ Long Lian∗ Lisa Dunlap∗
                                           Jiahao Shu         XuDong Wang Renhao Wang Trevor Darrell Alane Suhr                                            Angjoo Kanazawa
                                                                                    UC Berkeley
                                                                                                       ∗ Equal contribution.
arXiv:2512.17875v1 [cs.CV] 19 Dec 2025




                                         Visually Prompted Tasks are Fragile: small design changes can shift leaderboards
                                          Which marker is closer to the camera?                                                                     Rank    Model
                                                                                          Visual Prompting Techniques                Dataset Size
                                                                                                                                                     🥇      Llama 4 Scout
                                                                               Original      Size    Shape       Color    Position
                                                                                                                                                     🥈      Gemini 2.5 Flash
                                                                                                                                                     🥉      Gemini 2.5 Pro
                                                                                                                                        JPEG          4     Qwen 3VL 8B
                                                                                                                                     Compression      5     GPT 4.1
                                                                                                                                                      6     InternVL3-8b




                                                                                                                                                               ..
                                                             Task accuracy →      71%      74% (+2) 67% (-4) 61% (-10) 58% (-13)

                                         Figure 1. Small, seemingly irrelevant changes in visual prompting dramatically alter VLM predictions. Left: Qwen2.5-VL accuracy
                                         under different visual marker variants. Changes in marker size, shape, color, and label position lead to significant accuracy swings up to
                                         13%. Right: such variations can reorder leaderboards, with model rankings shifting even when nothing about the underlying task changes.

                                                                   Abstract                                          cause model lineup changes. These details have substan-
                                                                                                                     tially larger impacts on visually prompted benchmarks than
                                                                                                                     on conventional semantic VLM evaluations. To mitigate
                                            A key challenge in evaluating VLMs is testing models’                    this instability, we curate existing datasets to create VP-
                                         ability to analyze visual content independently from their                  Bench, a larger visually prompted benchmark with 16 visual
                                         textual priors. Recent benchmarks such as BLINK probe vi-                   marker variants. VPBench and additional analysis tools
                                         sual perception through visual prompting, where questions                   are released at https://lisadunlap.github.io/
                                         about visual content are paired with coordinates to which                   vpbench/.
                                         the question refers, with the coordinates explicitly marked
                                         in the image itself. While these benchmarks are an impor-
                                         tant part of VLM evaluation, we find that existing models                   1. Introduction
                                         are surprisingly fragile to seemingly irrelevant details of vi-
                                         sual prompting: simply changing a visual marker from red                    Despite the rapid progress of vision-language models
                                         to blue can completely change rankings among models on                      (VLMs), their visual perception capabilities remain under-
                                         a leaderboard. By evaluating nine commonly-used open-                       explored. Most existing benchmarks conflate visual under-
                                         and closed-source VLMs on two visually prompted tasks,                      standing with language priors and factual recall, making it
                                         we demonstrate how details in benchmark setup, including                    unclear whether models genuinely perceive or merely re-
                                         visual marker design and dataset size, have a significant in-               trieve. To address this, visual prompting has emerged as
                                         fluence on model performance and leaderboard rankings.                      a targeted paradigm: by marking regions in an image and
                                         These effects can even be exploited to lift weaker models                   posing spatial or perceptual questions, as originally pro-
                                         above stronger ones; for instance, slightly increasing the                  posed by [13, 31] and made most relevant as a VLM bench-
                                         size of the visual marker results in open-source InternVL3-                 mark with the BLINK dataset[9], these perceptual tasks as-
                                         8B ranking alongside or better than much larger propri-                     sess low-level visual understanding that humans solve ef-
                                         etary models like Gemini 2.5 Pro. We further show that low-                 fortlessly, in contrast to the knowledge-centric reasoning re-
                                         level inference choices that are often ignored in benchmark-                quired by benchmarks such as MME or MMMU [8, 28].
                                         ing, such as JPEG compression levels in API calls, can also                     However, within this visually prompted evaluation


                                                                                                                 1

## Page 2

regime, we find that model performance is surprisingly                of prompting, sampling, and implementation. To address
sensitive to seemingly minor design choices in the bench-             this, we release the expanded visually prompted datasets
mark itself. As illustrated in Figure 1, variations in the            as VPBench. VPBench is a benchmark covering 16 differ-
size, style, or layout of visual markers can substantially            ent visual marker variants, and overall boosting the dataset
affect accuracy and even reorder model rankings. Be-                  size from 224 samples in BLINK relative depth and seman-
yond prompt design, incidental implementation details,                tic correspondence to 35,088 annotated images across rel-
such as random sample selection, image compression set-               ative depth (VPBench-RD) and semantic correspondence
tings, or floating-point precision, can further contribute to         (VPBench-SC). Lastly, we provide suggestions on how to
this instability. Many of these design choices are inher-             more robustly evaluate visually prompted tasks and guid-
ited from conventional, knowledge-focused VLM bench-                  ance on when to trust the leaderboard rankings. We re-
marks, where such factors have minimal influence and are              lease our proposed VPBench along with our inference code,
thus treated as inconsequential. Yet, in visually prompted            which supports varying visual markers and image compres-
evaluations, these non-semantic elements become hidden                sion settings, as a reference inference for stable evaluation
confounders, capable of markedly distorting model per-                at https://lisadunlap.github.io/vpbench/.
formance and leaderboard rankings. Consequently, ex-
isting visually prompted benchmarks exhibit an inherent               2. Related Work
fragility—blink again, and an apparently incidental change
can shift reported scores, echoing the formatting sensitiv-           Perception-focused VLM benchmarks. Our work
ities observed in LLMs [19]. Such instability undermines              builds on efforts to separate low-level VLM perception
confidence in benchmark-driven progress and echoes recent             from high-level reasoning. BLINK, for example, recasts
concerns about leaderboard fragility in both language and             classic vision tasks into visually prompted questions,
vision domains.                                                       showing that VLMs struggle on problems humans solve
                                                                      “in a blink” [9], motivating follow-up work on perception-
   We explore three such sources of evaluation instability
                                                                      augmented representations [3]. Orthogonal work evaluates
across eight modern VLMs on BLINK [9] as well as two
                                                                      robustness via controlled input variations, such as perturba-
more large scale datasets, VPBench-RD and VPBench-SC,
                                                                      tions to image–text pairs, programmatic generation of task
that we curate using DA2k [26], and SPair [16]. First,
                                                                      variants, geometric invariances, or spatio-temporal video
we demonstrate the effect of sample choice: random re-
                                                                      manipulations [1, 7, 17, 32]. These benchmarks highlight
sampling of image subsets, matched in its modest size to
                                                                      VLM gaps in both perception and robust invariance.
BLINK and drawn from a fixed pool of visually prompted
tasks, leads to substantially reordered model rankings, de-
spite the subsets being statistically indistinguishable in size       Text and visual prompt sensitivity. Prompt design can
and difficulty. Second, we examine visual prompt format-              dominate model performance. In language models, small,
ting. On all dataset , we evaluate our models with 16 dif-            meaning-preserving formatting tweaks can significantly
ferent marker styles varying in size, shape, color, and label         swing accuracy [19]. This sensitivity extends to the visual
placement. We find that marker style can cause accuracy               prompts in VLMs, where the choice of marker (e.g., a dot
swings of up to 21% on the same image-question pairs, of-             vs. a box) can alter model attention and outcomes [20].
ten causing ranking reversals among state-of-the-art mod-             Indeed, the space of visual prompts has itself become an
els. Finally, we show that inference-time implementation              optimization target to boost accuracy [30]. These findings
details which are imperceptible to humans such as JPEG                imply that evaluations using a single visual style may reflect
compression further perturb results in statistically signifi-         prompt idiosyncrasies more than true model competence.
cant ways. Additionally, we find that this is specific to vi-
sually prompted tasks, as applying the same intervention              Evaluation instability: leaderboard fragility and imple-
to more traditional VLM benchmarks does not significantly             mentation subtleties. Evaluation outcomes for VLMs are
change the results. We also demonstrate how this fragility            highly unstable, sensitive both to benchmark design and to
can be exploited to “game” leaderboards. For example,                 low-level implementation details. On the benchmark side,
strategically selecting the visual marker to be a square in-          seemingly minor factors such as altering multiple-choice
stead of a circle causes a weaker model like InternVL3-8B             option order or varying random seeds can flip leaderboard
to rank above stronger models like Gemini 2.5 Pro on the              rankings [2, 15]. Community leaderboards can also be
BLINK relative depth estimation task.                                 gamed via selective submissions and feedback loops [21],
   These findings suggest that much of the variation among            motivating automated pipelines that continuously refresh
model performance reported on vision-language bench-                  and diversify test sets [14]. On the implementation side,
marks comes not from differentiated intrinsic capabilities            minor choices can likewise skew results: in image genera-
of grounding language in vision, but from incidental details          tion, resizing filters or JPEG compression significantly im-

                                                                  2

## Page 3

pact FID scores [18], while in multimodal evaluation, im-                                          3.1. What are Visually Prompted Tasks?
perceptible perturbations or numerical precision differences
                                                                                                   A visually prompted task explicitly marks regions of an
(FP16 vs. FP32) can destabilize outputs and compromise
                                                                                                   image and asks about relationships within or between im-
reproducibility [10, 24, 27]. Together, these findings un-
                                                                                                   ages [9]. We picked two typical visually prompted tasks
derscore that leaderboard orderings may reflect artifacts of
                                                                                                   (Fig. 2). In semantic correspondence, two images with
evaluation pipelines as much as genuine model ability.
                                                                                                   marked points are shown and the model is asked which
                                                                                                   marker corresponds to the same object part or region as the
Spatial reasoning benchmarks and methods. Spatial                                                  reference marker. In relative depth, two locations in an im-
reasoning has been a long-standing challenge, from early                                           age are marked with “A” and “B,” and the model is asked
synthetic benchmarks [11, 23] to modern evaluations. Re-                                           which is closer to the camera.
cent studies consistently show that state-of-the-art VLMs                                             Functionally, such visual prompting complements ver-
fail on simple spatial tasks, often performing near chance                                         bal prompting, serves as an intuitive and effective interface
on benchmarks probing relative positioning and ground-                                             for querying or referencing fine-grained visual content. Hu-
ing [12, 22, 25]. To close this gap, a new wave of                                                 mans naturally point to a location on a map, for example,
work introduces spatially-aware architectures and large-                                           rather than verbally describing its longitude and latitude.
scale, spatially-grounded training data [4–6].                                                     Meanwhile, unlike most VLM tasks that depend on broad
                                                                                                   world knowledge (e.g., MMMU), these visually prompted
    In summary, while prior work has documented fragility
                                                                                                   tasks are perceptual: humans solve them “in the blink of
in textual prompting and robustness under broad visual cor-
                                                                                                   an eye,” relying on fine-grained visual reasoning rather than
ruptions, we focus on the fine-grained, visually prompted
                                                                                                   factual recall. This makes them a natural choice for evaluat-
regime—benchmarks that explicitly mark regions or points
                                                                                                   ing how well models recognize objects and spatial relation-
in an image to elicit low-level perceptual judgments (e.g.,
                                                                                                   ships without external knowledge. BLINK [9], the bench-
relative depth). We demonstrate that (i) visual prompt style
                                                                                                   mark we study, is built around such tasks and has become a
is a primary confounder, (ii) i.i.d. resampling from a fixed
                                                                                                   de-facto standard for measuring visual perception in VLMs.
superset can reorder model rankings , and (iii) low-level
implementation choices exacerbate variance. To counteract                                          3.2. Experimental Setup
this, we advocate confidence-aware reporting across diver-
sified visual prompts and stratified resamplings, analogous                                        The BLINK dataset [9] systematizes these visually
in spirit to FormatSpread’s multi-format evaluation [19], but                                      prompted tasks via curated image–question pairs with
tailored to VLM perception, which yields markedly more                                             region-level markings. It contains relative depth and cor-
stable rankings on BLINK-like tasks.                                                               respondence tasks with high annotation quality. However,
                                                                                                   we noticed that within BLINK, visual markers are not stan-
                                                                                                   dardized: some examples use dots, others boxes or arrows.
3. Visually Prompted Tasks and Probing Them                                                        When these seemingly cosmetic differences are altered, we
                                                                                                   noticed non-trivial change in model performance. This mo-
                                                                                                   tivated our investigation into how VLM benchmarks may be
       Semantic Correspondence                                 Relative Depth
 Which point is corresponding to the reference point?   Which point is closer to the camera?       fragile given seemingly irrelevant design choices.
                                                                                                       As will be detailed in Section 4, BLINK’s small size,
                                                                                                   approximately 100 examples per split, makes it difficult to
                                                                                                   separate true performance variation from sampling noise.
                                                                                                   To reduce this ambiguity and enable more robust analy-
                                                                                                   sis, we curate a new benchmark called VPBench. VP-
                                                                                                   Bench is sourced from two larger datasets that follow the
                                               BLINK                                  BLINK
                                                                                                   same visually prompted task format: DA2K [26] and SPair-
                                                                                                   71k [16], with the former used for relative depth estima-
                                                                                                   tion (VPBench-RD) and the latter for semantic correspon-
                                                                                                   dence (VPBench-SC). DA-2K, originally introduced for
                                                                                                   depth annotation, contains thousands of images with dense
                                                                                                   geometric labels; we repurposed it into a relative-depth task
                                        VPBench  SC
                                          SPair 71K                            VPBench
                                                                                    DA RD
                                                                                       2K          by converting pixel-level depth into pairwise comparisons
                                                                                                   following BLINK’s protocol. SPair-71k (SPair), designed
Figure 2. Examples of visually prompted tasks. Visually
                                                                                                   for semantic correspondence, provides tens of thousands
prompted tasks (VPTs) involve placing visual markers in the im-
age to ask questions such as relative depth and semantic corre-                                    of image pairs with detailed keypoint matches; by adopt-
spondence.                                                                                         ing BLINK’s prompting style, we frame SPair as a visu-


                                                                                               3

## Page 4

ally prompted correspondence benchmark that bridges tra-             accuracy variation would be much higher than knowledge-
ditional CV evaluation with modern VLM usage. We then                focused ones like MME (See Fig. 5). At such accuracy lev-
apply all interventions for the following sections to all 4          els and sample size, even a few items can noticeably shift
datasets.                                                            results: in BLINK, a 3% accuracy change corresponds to
    Additionally, we compare the instability of rank across          only two or three additional correct responses, which in a
different dataset sizes and JPEG compressions to a non vi-           multiple-choice format could easily arise by chance. The
sually prompted task, MME [8], to investigate how these              resulting variance is reflected in the confidence intervals in
interventions affect visually prompted tasks specifically.           Figure 3, and we further highlight its impact by showing
    We evaluate four closed-source and five open-source              how results fluctuate as the dataset size decreases.
VLMs: Gemini 2.5 Pro, Gemini 2.5 Flash, GPT-4.1,
GPT-4o, Llama 4 Scout, Qwen3-VL-8B, Qwen2.5-VL-7B,
Gemma 3-4B, and InternVL3-8B. Aggregate accuracies for               Size particularly matters for VPTs. Additionally, we
each benchmark appear in Fig. 3.                                     compute the mean standard deviation in model performance
    In the following section, we demonstrate the fragility           across splits to get numeric measures of the instability seen
of these visually prompted tasks by showing how small                across splits. Figure 5 shows that the instability seen across
changes in data sampling, visual marker, and low-level im-           these splits is considerably larger than that of non visually
plementation details can completely change the results .             prompted tasks. This suggests that more so than for other
                                                                     visual tasks, visually prompted benchmarks would actually
4. Statistically Equivalent Sampling Yields Dif-                     require a relatively larger number of samples to reduce the
                                                                     variance you see from the data. In the following sections,
    ferent Results
                                                                     we will show how additional choices affect the leaderboard
When constructing a benchmark, creators typically sam-               even when given a 10 times larger dataset size.
ple a subset of data points from a large data pool, such as
data collected from the Internet, to form the evaluation set.        5. Visual Marker Styles Shuffle Leaderboards
This sampling process is random, so in principle, any subset
drawn from the same pool should be statistically equivalent          We investigate whether the style of the visual marker used
and yield similar results. The subset size is usually fixed          in a prompt influences model performance, and whether
by convention, following prior knowledge-oriented VLM                it can change the relative ordering of models’ accuracy.
benchmarks where per-task sample counts commonly range               This question is motivated by an observation of inconsis-
from 50 to 500 items. While BLINK also follows this con-             tent marker styles in the BLINK benchmark dataset [9]. The
vention, we find that the random sampling step itself can            visual prompts BLINK employs as part of the question con-
meaningfully influence evaluation outcomes. If a differ-             text occasionally switched in color or text positioning and
ent subset were drawn from the same underlying distribu-             we noticed, for example, that simply switching a marker’s
tion, both the absolute accuracy and the model ranking can           color from red to blue questions led to measurable changes
change noticeably.                                                   in a model’s accuracy on BLINK, suggesting current mod-
                                                                     els are over-reliant on specific visual cues. In this section
                                                                     we create a set of marker variants and study their effects on
Experimental setup: We create 1,000 new BLINK size
                                                                     model performance. We report results on VPBench in the
datasets by randomly sampling 100 samples from our pro-
                                                                     main paper and additionally report results for the BLINK
posed VPBench for both relative depth and semantic cor-
                                                                     subsets in the Appendix.
respondence tasks, and the non-visually prompted dataset
MME [8]. Since these samples are drawn from the same un-
derlying data distribution, the accuracies and model leader-
board should remain constant, but as shown in Figure 4, we           Experimental setup: Based on the most common marker
can get a complete change in rankings across VPBench-RD              seen in BLINK relative depth and semantic correspondence,
and VPBench-SC.                                                      we define a default marker style to be a small red circular
                                                                     marker with a numeric label placed above. We then create
                                                                     16 alternative styles (commonly seen in visual prompting
Why sampling matters here? This sensitivity arises                   literature) spanning 4 categories: color (blue instead of red),
because BLINK, like many newly-released multimodal                   shape (square instead of circle), size (larger marker, radius
benchmarks, deliberately targets unsaturated capabilities            increased from the default to size 10), and text position (la-
i.e. tasks where performance levels are far from ceiling, typ-       bel moved to below the marker). Figures 6a and 6b display
ically in the 30–60% range rather than the 80–90% common             the change in accuracies and rankings of each model on rel-
in relatively mature VLM tasks, consequently, these VPT              ative depth and semantic correspondence tasks.

                                                                 4

## Page 5

                                             BLINK Rel. Depth Accuracy                     LINK Rel. Depth Leaderboa                                                   VPBench Rel. Depth Accuracy                    Bench Rel. Depth Leaderbo
                             100              89%                                                                                                          100
                                   78% 78%                                                   Rank   Model                                                                                                               Rank   Model
                                                          76%            76%         75%
                                                    72%            71%                              🥇 Llama 4 Scout                                                                                                            🥇 Llama 4 Scout




                                                                                                                             VPBench Rel. Depth Accuracy
                                                                                               1                                                                                                                         1
                                                                                                                                                                         74%
 BLINK Rel. Depth Accuracy


                             80
                                                                                               2    🥈 Gemini 2.5 Pro                                       80
                                                                                                                                                                 69% 71%               69%
                                                                                                                                                                                                61% 63%         64%      2     🥈 Gemini 2.5 Flash
                             60
                                                                               53%             2    🥈 Gemini 2.5 Flash                                     60
                                                                                                                                                                                 61%
                                                                                                                                                                                                                         3     🥉 Gemini 2.5 Pro
                                                                                               4     Qwen3-VL-8B
                                                                                                                                                                                                          51%            4      Qwen3-VL-8B
                                                                                               4     InternVL3-8B                                                                                                        5      GPT-4.1
                             40                                                                                                                            40
                                                                                               6     GPT-4.1                                                                                                             6      InternVL3-8B
                                                                                               7     GPT-4o                                                                                                              7      Qwen2.5-VL-7B
                             20                                                                                                                            20
                                                                                               8     Qwen2.5-VL-7B                                                                                                       8      GPT-4o
                                                                                               9     Gemma 3-4B                                                                                                          9      Gemma 3-4B
                              0                                                                                                                             0
               ro      sh  ut    4o L-8B L-7B 3-8B 3-4B T-4.1                                                                             ro      sh  ut    4o L-8B L-7B 3-8B 3-4B T-4.1
           .5 P Fla Sco GPT- Sem.                  L
                                     -V .5-V Accuracy                                                                                 .5 P Fla Sco GPT- Sem.    -V          VL ma
                                                                                                                                                                      -V rnAccuracy
      ini 2 ini 2.5 ama 4 BLINK   en3 en2Cor.   rnV ma GP                                                                        ini 2 ini 2.5 ama 4VPBench  en3 en2.5Cor.          GP
                                                                                           LINK Sem. Cor. Leaderboa                                                                                                   Bench Sem. Cor. Leaderbo
  e m
 G 100     m       L l        Q w
                                     Qw     Inte Gem                                                                          em
                                                                                                                             G 100    m       L l        Q w
                                                                                                                                                                Qw      Inte Gem
        Ge                                                                                                                         Ge
                                                                                             Rank   Model                                                                                                               Rank   Model
                                                           Model                                                                                                                        Model




                                                                                                    🥇 Gemini 2.5 Pro                                                                                                           🥇 Gemini 2.5 Pro




                                                                                                                             VPBench Sem. Cor. Accuracy
                                                                                               1                                                                                                                         1
 BLINK Sem. Cor. Accuracy




                             80
                                   63%
                                         56% 54%
                                                                                               2    🥈 Gemini 2.5 Flash                                     80
                                                                                                                                                                 65% 64%                                                 2     🥈 Gemini 2.5 Flash
                             60                     46% 49%
                                                                                     51%       3    🥉 Llama 4 Scout                                        60
                                                                                                                                                                           58%         55%                               3     🥉 Llama 4 Scout
                                                                                               4     GPT-4.1                                                                     46%                            50%      4      Qwen3-VL-8B
                                                                   33%         33%             5     Qwen3-VL-8B                                                                                36% 37%                  5      GPT-4.1
                             40                                          27%                                                                               40                                             31%
                                                                                               6     GPT-4o                                                                                                              6      GPT-4o
                                                                                               7     Qwen2.5-VL-7B                                                                                                       7      InternVL3-8B
                             20                                                                                                                            20
                                                                                               7     Gemma 3-4B                                                                                                          8      Qwen2.5-VL-7B
                                                                                               9     InternVL3-8B                                                                                                        9      Gemma 3-4B
                              0                                                                                                                             0
              ro     sh  ut   4o 8B 7B        8B 4B        .1                                                                             ro     sh  ut   4o 8B 7B        8B 4B        .1
          .5 P Fla Sco GPT- 3-VL- .5-VL- nVL3- ma 3- GPT-4                                                                            .5 P Fla Sco GPT- 3-VL- .5-VL- nVL3- ma 3- GPT-4
   m ini 2 ini 2.5 ama 4     w e n n2 ter em
                                   e  In                                                                                       m ini 2 ini 2.5 ama 4     w e n n2 ter em
                                                                                                                                                               e  In
 Ge Gem           Ll        Q Qw            G                                                                                Ge Gem           Ll        Q Qw            G
                                                           Model                                                                                                                        Model




Figure 3. Larger benchmark datasets stabilize rankings. Accuracies and rankings of 9 VLMs on BLINK Relative Depth, BLINK
Semantic Correspondence, VPBench Relative Depth (VPBench-RD), and VPBench Semantic Correspondence (VPBench-SC) using
BLINK’s default marker convention. Error bars show 95% confidence intervals. Compared to BLINK’s small test splits, the larger
VPBench relative depth and semantic correspondence evaluations yield substantially narrower intervals, making ranking differences easier
to interpret and less sensitive to sampling noise.

Disentangling visual marker variance from data vari-                                                                                                        To compare sources of variability, we report the ratio
ance. To confirm that the variance in accuracy seen across                                                                                                                                     
visual markers is not simply due to the variance in the data                                                                                                                  Ej Var ∆accjs
                                                                                                                                                                         R=                     ,
itself, we perform a paired bootstrap to confirm that the                                                                                                                        Var accm  s
                                                                                                                                                                                             0
difference between the default BLINK marker and other
marker variance is statistically significant.                                                                                    where the denominator estimates dataset variance and the
    Let D = {(xℓ , yℓ )}N
                        ℓ=1 be the dataset. A marker m ren-
                                                                                                                                 numerator estimates marker-induced variance. Values R ≥
ders an annotated input m(xℓ ). BLINK provides a default                                                                         1 indicate that changing marker style perturbs accuracy at
marker m0 ; we also consider valid alternatives m1 , . . . , mK                                                                  least as much as resampling the test set itself. We find the
(e.g., dots, boxes, arrows). For a model f , accuracy under                                                                      majority of visual markers show significant differences for
marker m is                                                                                                                      at least 1 model, proving that marker style is not cosmetic
                                                            N
                                                                                                                                 but consequential. (more details in the Appendix A.)
                                                          1 X                 
                                          accm =              1 f (m(xℓ )) = yℓ .
                                                          N                                                                      Effect on model rankings:         Figures 6a and Figure 6b
                                                                   ℓ=1
                                                                                                                                 show the model accuracy on the default visual marker (red
   To determine whether observed accuracy differences be-
                                                                                                                                 circle, text at the top) along with the delta in performance
tween markers are statistically significant rather than due
                                                                                                                                 seen across 16 different visual markers of varying sizes,
to sampling variability, we draw B bootstrap replicates Ds
                                                                                                                                 shapes, colors, and positions. We see that if you change
by sampling N items with replacement. On each replicate,
                                                                                                                                 the visual marker, the takeaways about which model is su-
we compute accuracies with the default and an alternative
                                                                                                                                 perior can be vastly different. Beyond absolute accuracy,
marker and take the paired difference
                                                                                                                                 marker changes often altered the relative performance of
                                                 ∆accjs = accm
                                                             s
                                                               0
                                                                      s
                                                                 − accm j
                                                                          .                                                      models. For example, Llama 4 Scout outperformed Gem-
                                                                                                                                 ini 2.5 Flash under the default red marker for relative depth,
   The distribution {∆accjs }B
                             s=1 isolates marker variance                                                                        but under the blue marker condition their ranks reversed,
because both conditions use the same sampled items. We                                                                           with Gemini 2.5 Flash scoring as the highest performing
test H0 : accm0 = accmj by checking whether zero lies in                                                                         model. We also see cases of incredibly large differences in
the 95% bootstrap confidence interval of ∆accjs .                                                                                accuracy, such as Llama 4 Scout and InternVL for semantic


                                                                                                                         5

## Page 6

                                                           DA2k - Model Ranks by Split
                                                                                                             correspondence, where making the text size of the marker




                                                                                                    10
                                                all

                                                      1

                                                            2

                                                                 3

                                                                     4

                                                                           5

                                                                                 6

                                                                                     7

                                                                                         8

                                                                                                9
    Llama 4 Scout                                1     2     3   1     1     1   1   1     1    3    2       smaller results in a 10+% drop in accuracy and dropping
  Gemini 2.5 Flash                               2     4     2   4     4     1   3   2     2    2    1
                                                                                                             Llama from rank 3 to rank 6.

   Gemini 2.5 Pro                                3     5     1   2     1     4   2   5     4    1    3
                                                                                                             Which visual markers matters most? Figure 7 displays
     Qwen3-VL-8B                                 4     1     4   2     5     1   5   2     3    4    4
                                                                                                             the average magnitude of accuracy difference across each
          GPT-4.1                                5     7     5   6     6     6   8   6     8    5    8       marker for the relative depth task, altering size or label po-
                                                                                                             sition generally produced larger effects on accuracy than
     InternVL3-8B                                6     5     6   7     3     8   4   6     4    6    6
                                                                                                             changing color or shape. Changing the marker’s color
   Qwen2.5-VL-7B                                 7     3     8   5     8     5   6   9     6    8    5       (red to blue) had a large impact on certain models, hinting
              GPT-4o                             8     9     7   8     6     7   7   4     7    7    7       that those models might be overfit to the color distribution
                                                                                                             of markers seen in their training or the benchmark (since
     Gemma 3-4B                                  9     8     9   9     9     9   9   8     9    9    8
                                                                                                             BLINK’s default is red, some models may have learned to
                                                   SPair-71kModel
                                            (a) VPBench-RD   - Model Ranksperbydata
                                                                  Ranking        Split
                                                                                    split                    specifically attend to red circles as a prompt cue). Chang-
                                                                                                             ing the marker’s size and shape or changing the text marker

                                                                                                    10
                                                all

                                                      1

                                                            2

                                                                 3

                                                                     4

                                                                           5

                                                                                 6

                                                                                     7

                                                                                         8

                                                                                                9
   Gemini 2.5 Pro                                1     1     1   1     2     1   1   1     1    1    2
                                                                                                             from A/B to 1/2 had a measurable but less prominent effect
                                                                                                             on accuracy. Notably, we did not find a single marker style
  Gemini 2.5 Flash                               2     2     1   2     1     3   2   1     1    2    1
                                                                                                             that was universally best or worst for all models. These id-
    Llama 4 Scout                                3     2     3   4     3     2   4   3     3    3    3       iosyncratic responses point to each model having its own
                                                                                                             biases in visual prompt processing.
     Qwen3-VL-8B                                 4     4     3   3     4     5   3   4     4    5    3

          GPT-4.1                                5     5     5   5     5     4   5   5     5    6    8
                                                                                                             Manipulating Visually Prompted Leaderboards. We
              GPT-4o                             6     6     6   6     6     6   6   6     6    4    5       explicitly demonstrate that visually prompted leaderboards
     InternVL3-8B                                7     7     8   7     7     7   7   8     8    8    6       can be gamed by jointly selecting a marker style and an i.i.d.
                                                                                                             split that favor a particular model, see Figure 8. On BLINK
   Qwen2.5-VL-7B                                 8     8     7   8     8     8   9   7     7    7    6
                                                                                                             relative depth, for example, we can lower internVL3 from
     Gemma 3-4B                                  9     8     9   9     9     9   8   9     9    9    9       rank 4 to rank 8 by simply changing the marker to be a
                                                                                                             square, and can similarly raise its rank to 3, higher than
                                            (b) VPBench-SC Model Ranking per data split
                                                                                                             Gemini 2.5 Pro, by increasing the font size of the marker.
Figure 4. Model rankings across 1,000 independent 100-sample                                                 This underscores that, without standardized marker conven-
splits for VPBench-RD and VPBench-SC, with the first 10 splits                                               tions, visually prompted evaluations can give misleading
visualized on the x-axis, revealing substantial ranking volatility                                           impressions of model ability.
caused solely by i.i.d. resampling.
                                                                                                             6. Imperceptible differences matter as well
                                                                                                             Beyond visually noticeable details such as marker styles, we
                                          4.5                                                                also extend our investigation to imperceptible factors, draw-
          Mean Accuracy Deviation (Std)




                                           4
                                                                                                             ing inspiration from prior work on human perceptual sensi-
                                          3.5
                                                                                                             tivity and adversarial robustness [29]. In particular, we ex-
                                           3

                                          2.5
                                                                                                             amine whether common preprocessing operations—such as
                                           2
                                                                                                             JPEG compression, which is widely applied in benchmark
                                          1.5                                                                construction for efficient storage—can subtly affect model
                                           1                                                                 performance. Although variations in JPEG quality above
                                          0.5
                                                                                                             a compression level of 70 are largely imperceptible to hu-
                                           0
                                                      MME         VPB-RD (VPT)   VPB-SC (VPT)                mans, it remains unclear whether vision–language models
                                                                                                             (VLMs) exhibit comparable robustness. Moreover, as this
Figure 5. Model accuracy change across 1,000 splits of 100
                                                                                                             issue has not been systematically explored in prior litera-
samples. Standard deviation in accuracy averaged across mod-
els. We see higher rank instability across 1,000 subsets each with                                           ture, we investigate whether such imperceptible variations
100 samples for the visually prompted tasks (VPBench-RD and                                                  affect vision–perception tasks (VPT) differently from con-
VPBench-SC) compared to knowledge-based VLM tasks (MME).                                                     ventional knowledge-focused benchmarks.
                                                                                                                 Setup. We evaluate four different JPEG compression
                                                                                                             levels: default, 70, 80, and 90. Prompts and data splits are
                                                                                                             kept fixed. To emphasize rank stability rather than absolute


                                                                                                         6

## Page 7

                                                                 radius         text        font                                                        radius    text    font
                                             blue    square       small        below       small                                        blue   square    small   below   small




                 (a) Rank and accuracy changes across visual markers on VPBench-RD.                                        (b) Rank and Accuracy changes across markers on VPBench-SC.

                 Figure 6. Small marker changes cause large, model-specific accuracy shifts and rank shuffles. Rank (top) and accuracy (bottom)
                 variations on (a) VPBench-RD relative depth and (b) VPBench-SC semantic correspondence across 16 visual marker variants (full chart
                 in the Appendix). Rows are models and columns are marker styles; each cell reports the change in accuracy relative to the default BLINK
                 marker, which uses a red circle with the label above. Positive values indicate improvements and negative values indicate degradations.
                                           Absolute Accuracy Shift - DA-2K Relative Depth
                                                          Positive Average Effect         Negative Average Effect         derstanding of visual tokens than semantic-focused tasks;
                                                                                                                          consequently, even subtle pixel-level changes can influence
                              radius 10                     0.66%                                                         model predictions. In contrast, Figure 9 shows that MME
                            color green                             0.89%
                          text label 12                              0.91%                                                rankings remain remarkably stable across all four compres-
                  marker type square                                      1.08%                                           sion settings and nine evaluated models, with only a single
                 marker type diamond                                         1.16%                                        ranking inversion compared to the pronounced shifts ob-
                  marker type triangle                                         1.23%
                                                                                                                          served in BLINK RD.
Marker Variant




                         font scale 1.0                                         1.25%
                               radius 3                                          1.28%                                       Takeaways. JPEG quality should be standardized—or
                               radius 1                                          1.29%
                             color blue                                           1.32%                                   ideally replaced with lossless formats—for VPT bench-
                           color yellow                                               1.45%                               marks; otherwise, compression artifacts alone can meaning-
                      text offset right                                               1.46%                               fully tilt leaderboard standings when model performances
                              radius 15                                                    1.62%
                         font scale 0.2                                                    1.62%                          are tightly clustered.
                     text offset below                                                       1.68%
                        text offset left                                                                1.99%
                                                                                                                          7. Discussions
                                      0.0           0.5             1.0             1.5              2.0            2.5
                                                              Mean Absolute Accuracy Change (%)
                                                                                                                          Our results show that visually prompted evaluations intro-
                 Figure 7. Impact by marker type. Mean absolute accuracy shift                                            duce non-semantic confounders: marker design, sample
                 on VPBench-RD induced by each marker variant.                                                            choice, and low-level implementation details can all shift
                                                                                                                          accuracies and reorder rankings. This fragility arises both
                 performance, Fig. 6 reports model ranks (1=best) instead of                                              from the benchmarks and from the models themselves.
                 raw accuracies—(a) for BLINK–Relative Depth (RD) and                                                        To partially mitigate these issues, we advocate the fol-
                 (b) for MME (semantic).                                                                                  lowing practices:
                    BLINK RD (VPT) vs. MME (semantic). Surpris-                                                           • Standardize and diversify visual prompts. Use a
                 ingly—or perhaps not surprisingly—the rankings in BLINK                                                    clearly specified default marker style, and, whenever pos-
                 RD fluctuate considerably, even for closed-source models                                                   sible, report results averaged over a small set of marker
                 such as Gemini 2.5 Pro. This sensitivity can be attributed                                                 variants. For benchmark creators, release clean images
                 to the fact that VPT tasks demand a more fine-grained un-                                                  together with raw marker coordinates rather than only im-


                                                                                                                    7

## Page 8

11/14/25, 2:29 PM                                                                                                                         Leaderboards HTML for PDF | Claude




    Figure 8. Manipulating leaderboards for InternVL3-8b. Performance comparison: optimizing for InternVL3-8B’s ranking on BLINK
    relative depth. Leaderboard rank can be shifted by benign visual prompt choices rather than changes in model capability.

                                       BLINK Relative Depth                                                  MME (semantic)
              Llama 4 Scout                                                     Llama 4 Scout
                                                                                                                                                    than declaring definitive winners.
            Gemini 2.5 Flash                                                  Gemini 2.5 Flash                                                       As a step toward more stable evaluation, we release VP-
             Gemini 2.5 Pro                                                    Gemini 2.5 Pro
               InternVL3-8B                                                      InternVL3-8B                                                     Bench, the scaled-up visually prompted benchmark used in
    Model




                                                                      Model




               Qwen3-VL-8B
                    GPT-4.1
                                                                                 Qwen3-VL-8B
                                                                                      GPT-4.1
                                                                                                                                                  our work, together with multiple marker variants and refer-
                     GPT-4o                                                            GPT-4o                                                     ence evaluation scripts. With performance of common mod-
             Qwen2.5-VL-7B                                                     Qwen2.5-VL-7B
               Gemma 3-4B                                                        Gemma 3-4B
                                                                                                                                                  els on VPBench shown in Fig. 3, we show that by reducing
                               1   2   3   4    5
                                               Rank
                                                      6   7   8   9                              1   2   3     4    5
                                                                                                                   Rank
                                                                                                                          6   7   8   9           variance due to arbitrary design choices, VPBench makes
                                                                                                                                                  performance differences more reflective of true perceptual
     Figure 9. Change in rank seen across JPEG compression rates.                                                                                 ability. While currently limited to depth and correspon-
     Individual dots with no lines indicate models whose rank remained                                                                            dence tasks, it provides a foundation for broader analyses
     constant across all compression levels. JPEG compression qual-                                                                               and future robustness-aware benchmarks for visual ground-
     ity substantially reorders model rankings on visually-dependent                                                                              ing.
     tasks (BLINK RD), whereas rankings on traditional benchmarks
https://claude.ai/public/artifacts/ba776a61-10a2-4bd6-aaa1-810815354799                                                                                                                                             1/1
     (MME) exhibit greater stability.
                                                                                                                                                  8. Conclusion
      ages with markers baked in, so that alternative prompt de-                                                                                  Benchmarks should measure ability, not fragility. Yet our
      signs can be evaluated consistently.                                                                                                        results reveal a gap: visually prompted evaluations “fall
    • Enrich test sets from consistent sources. When fea-                                                                                         short of this standard”: change a marker’s color, shift its
      sible, evaluate on larger visually prompted pools con-                                                                                      label, compress an image differently, and entire leader-
      structed from the same underlying data sources and task                                                                                     boards reshuffle. These shifts are not noise but struc-
      definitions, rather than relying on a single small split. In                                                                                tural weaknesses, revealing that today’s perception-focused
      our case, we expand BLINK-style relative depth and cor-                                                                                     VLM benchmarks are far more sensitive than the field as-
      respondence tasks with VPBench-RD and VPBench-SC                                                                                            sumes. Although our demonstrations center on BLINK-
      using images and annotations from DA2k and SPair-71k,                                                                                       style tasks, the pattern is unlikely to be isolated. Any bench-
      yielding substantially more stable aggregates.                                                                                              mark that depends on explicit visual markup or fine-grained
    • Adhere to the same realization of low-level settings.                                                                                       spatial cues risks similar instability. If leaderboards can be
      Explicitly standardize and report data-processing and in-                                                                                   flipped by choices orthogonal to task semantics, they can-
      ference choices such as JPEG compression quality, in-                                                                                       not be trusted to track genuine progress. To address this,
      put resolution, and numerical precision (e.g., bf16 vs.                                                                                     we recommend evaluations should diversify visual prompts,
      fp8/fp16 for self-hosted models). Avoid silent changes                                                                                      report variance in addition to scores, and standardize low-
      across evaluations, and treat models with opaque internals                                                                                  level settings that silently influence results. VPBench is a
      as a separate comparison group.                                                                                                             step in that direction, offering larger, marker-diverse test
    • Report uncertainty and rank stability. Accompany ac-                                                                                        sets that reduce incidental variance. Stable measurement
      curacies with confidence intervals (e.g., Wilson or boot-                                                                                   is a prerequisite for meaningful comparison; until then, vi-
      strap) and simple rank-stability analyses across markers,                                                                                   sually prompted leaderboards may be telling us more about
      splits, or seeds, particularly when the low accuracy tasks                                                                                  their construction than about the models they rank.
      have relatively small sample sizes. When intervals over-
      lap substantially, treat models as effectively tied rather


                                                                                                                                             8

## Page 9

References                                                         [10] Horace He and Thinking Machines Lab.
                                                                        Defeating      nondeterminism       in     llm     infer-
[1] Amit Agarwal, Srikant Panda, Angeline Charles,                      ence.       Thinking Machines Lab: Connection-
    Bhargava Kumar, Hitesh Patel, Priyaranjan Pattnayak,                ism, 2025.         doi:    10 . 64434 / tml . 20250910.
    Taki Hasan Rafi, Tejaswini Kumar, Hansa Meghwani,
                                                                        https://thinkingmachines.ai/blog/defeating-
    Karan Gupta, et al. Mvtamperbench: Evaluating ro-
                                                                        nondeterminism-in-llm-inference/. 3
    bustness of vision-language models. arXiv preprint
    arXiv:2412.19794, 2024. 2                                      [11] Justin Johnson, Bharath Hariharan, Laurens Van
[2] Norah Alzahrani, Hisham Alyahya, Yazeed Alnu-                       Der Maaten, Li Fei-Fei, C Lawrence Zitnick, and Ross
    may, Sultan Alrashed, Shaykhah Alsubaie, Yousef Al-                 Girshick. Clevr: A diagnostic dataset for composi-
    mushayqih, Faisal Mirza, Nouf Alotaibi, Nora Al-                    tional language and elementary visual reasoning. In
    Twairesh, Areeb Alowisheq, et al. When benchmarks                   Proceedings of the IEEE conference on computer vi-
    are targets: Revealing the sensitivity of large language            sion and pattern recognition, pp. 2901–2910, 2017. 3
    model leaderboards. In Proceedings of the 62nd An-             [12] Amita Kamath, Jack Hessel, and Kai-Wei Chang.
    nual Meeting of the Association for Computational                   What’s” up” with vision-language models? investi-
    Linguistics (Volume 1: Long Papers), pp. 13787–                     gating their struggle with spatial reasoning. arXiv
    13805, 2024. 2                                                      preprint arXiv:2310.19785, 2023. 3
[3] Mahtab Bigverdi, Zelun Luo, Cheng-Yu Hsieh, Ethan              [13] Ranjay Krishna, Yuke Zhu, Oliver Groth, Justin John-
    Shen, Dongping Chen, Linda G Shapiro, and Ranjay                    son, Kenji Hata, Joshua Kravitz, Stephanie Chen,
    Krishna. Perception tokens enhance visual reasoning                 Yannis Kalantidis, Li-Jia Li, David A. Shamma,
    in multimodal language models. In Proceedings of the                Michael S. Bernstein, and Li Fei-Fei. Visual genome:
    Computer Vision and Pattern Recognition Conference,                 Connecting language and vision using crowdsourced
    pp. 3836–3845, 2025. 2                                              dense image annotations. International Journal of
[4] Boyuan Chen, Zhuo Xu, Sean Kirmani, Brain Ichter,                   Computer Vision, 123:32 – 73, 2016. URL https:
    Dorsa Sadigh, Leonidas Guibas, and Fei Xia. Spa-                    //api.semanticscholar.org/CorpusID:
    tialvlm: Endowing vision-language models with spa-                  4492210. 1
    tial reasoning capabilities. In Proceedings of the             [14] Tianle Li, Wei-Lin Chiang, Evan Frick, Lisa Dunlap,
    IEEE/CVF Conference on Computer Vision and Pat-                     Tianhao Wu, Banghua Zhu, Joseph E Gonzalez, and
    tern Recognition, pp. 14455–14465, 2024. 3                          Ion Stoica. From crowdsourced data to high-quality
[5] An-Chieh Cheng, Hongxu Yin, Yang Fu, Qiushan                        benchmarks: Arena-hard and benchbuilder pipeline.
    Guo, Ruihan Yang, Jan Kautz, Xiaolong Wang, and                     arXiv preprint arXiv:2406.11939, 2024. 2
    Sifei Liu. Spatialrgpt: Grounded spatial reasoning in          [15] Lovish Madaan, Aaditya K Singh, Rylan Schaeffer,
    vision-language models. Advances in Neural Informa-                 Andrew Poulton, Sanmi Koyejo, Pontus Stenetorp,
    tion Processing Systems, 37:135062–135093, 2024.                    Sharan Narang, and Dieuwke Hupkes. Quantifying
[6] Nianchen Deng, Lixin Gu, Shenglong Ye, Yinan He,                    variance in evaluation benchmarks. arXiv preprint
    Zhe Chen, Songze Li, Haomin Wang, Xingguang Wei,                    arXiv:2406.10229, 2024. 2
    Tianshuo Yang, Min Dou, et al. Internspatial: A
                                                                   [16] Juhong Min, Jongmin Lee, Jean Ponce, and
    comprehensive dataset for spatial reasoning in vision-
                                                                        Minsu Cho.        Spair-71k: A large-scale bench-
    language models. arXiv preprint arXiv:2506.18385,
                                                                        mark for semantic correspondence. arXiv prepreint
    2025. 3
                                                                        arXiv:1908.10543, 2019. 2, 3
[7] Zhiyuan Fan, Yumeng Wang, Sandeep Polisetty, and
    Yi R Fung. Unveiling the lack of lvlm robustness to            [17] Seulki Park, Daeho Um, Hajung Yoon, Sanghyuk
    fundamental visual variations: Why and path forward.                Chun, and Sangdoo Yun. Rococo: Robustness bench-
    arXiv preprint arXiv:2504.16727, 2025. 2                            mark of ms-coco to stress-test image-text matching
[8] Chaoyou Fu, Peixian Chen, Yunhang Shen, Yulei Qin,                  models. In European Conference on Computer Vision,
    Mengdan Zhang, Xu Lin, Jinrui Yang, Xiawu Zheng,                    pp. 71–91. Springer, 2024. 2
    Ke Li, Xing Sun, et al. Mme: A comprehensive evalu-            [18] Gaurav Parmar, Richard Zhang, and Jun-Yan Zhu. On
    ation benchmark for multimodal large language mod-                  aliased resizing and surprising subtleties in gan evalu-
    els. arXiv preprint arXiv:2306.13394, 2023. 1, 4                    ation. In CVPR, 2022. 3
[9] Xingyu Fu, Yushi Hu, Bangzheng Li, Yu Feng, Haoyu              [19] Melanie Sclar, Yejin Choi, Yulia Tsvetkov, and Alane
    Wang, Xudong Lin, Dan Roth, Noah A Smith, Wei-                      Suhr. Quantifying language models’ sensitivity to spu-
    Chiu Ma, and Ranjay Krishna. Blink: Multimodal                      rious features in prompt design or: How i learned
    large language models can see but not perceive. arXiv               to start worrying about prompt formatting. arXiv
    preprint arXiv:2404.12390, 2024. 1, 2, 3, 4                         preprint arXiv:2310.11324, 2023. 2, 3


                                                               9

## Page 10

[20] Aleksandar Shtedritski, Christian Rupprecht, and An-                sual prompt for large vision-language models. arXiv
     drea Vedaldi. What does clip know about a red circle?               preprint arXiv:2506.16112, 2025. 2
     visual prompt engineering for vlms. In Proceedings of          [31] Yuke Zhu, Oliver Groth, Michael S. Bernstein, and
     the IEEE/CVF International Conference on Computer                   Li Fei-Fei. Visual7w: Grounded question answering
     Vision, pp. 11987–11997, 2023. 2                                    in images. 2016 IEEE Conference on Computer Vi-
[21] Shivalika Singh, Yiyang Nan, Alex Wang, Daniel                      sion and Pattern Recognition (CVPR), pp. 4995–5004,
     D’Souza, Sayash Kapoor, Ahmet Üstün, Sanmi                        2015. URL https://api.semanticscholar.
     Koyejo, Yuntian Deng, Shayne Longpre, Noah A                        org/CorpusID:5714907. 1
     Smith, et al. The leaderboard illusion. arXiv preprint         [32] Chengke Zou, Xingang Guo, Rui Yang, Junyu Zhang,
     arXiv:2504.20879, 2025. 2                                           Bin Hu, and Huan Zhang. Dynamath: A dynamic
[22] Ilias Stogiannidis, Steven McDonagh, and Sotirios A                 visual benchmark for evaluating mathematical rea-
     Tsaftaris. Mind the gap: Benchmarking spatial rea-                  soning robustness of vision language models. arXiv
     soning in vision-language models. arXiv preprint                    preprint arXiv:2411.00836, 2024. 2
     arXiv:2503.19707, 2025. 3
[23] Alane Suhr, Stephanie Zhou, Ally Zhang, Iris Zhang,
     Huajun Bai, and Yoav Artzi. A corpus for reason-
     ing about natural language grounded in photographs.
     arXiv preprint arXiv:1811.00491, 2018. 3
[24] Jordan Vice, Naveed Akhtar, Yansong Gao, Richard
     Hartley, and Ajmal Mian. On the reliability of vision-
     language models under adversarial frequency-domain
     perturbations.     arXiv preprint arXiv:2507.22398,
     2025. 3
[25] Jiayu Wang, Yifei Ming, Zhenmei Shi, Vibhav Vineet,
     Xin Wang, Sharon Li, and Neel Joshi. Is a picture
     worth a thousand words? delving into spatial reason-
     ing for vision language models. Advances in Neu-
     ral Information Processing Systems, 37:75392–75421,
     2024. 3
[26] Lihe Yang, Bingyi Kang, Zilong Huang, Zhen Zhao,
     Xiaogang Xu, Jiashi Feng, and Hengshuang Zhao.
     Depth anything v2. arXiv:2406.09414, 2024. 2, 3
[27] Jiayi Yuan, Hao Li, Xinheng Ding, Wenya Xie, Yu-
     Jhe Li, Wentian Zhao, Kun Wan, Jing Shi, Xia Hu,
     and Zirui Liu. Give me fp32 or give me death? chal-
     lenges and solutions for reproducible reasoning. arXiv
     preprint arXiv:2506.09501, 2025. 3
[28] Xiang Yue, Yuansheng Ni, Kai Zhang, Tianyu Zheng,
     Ruoqi Liu, Ge Zhang, Samuel Stevens, Dongfu Jiang,
     Weiming Ren, Yuxuan Sun, et al. Mmmu: A mas-
     sive multi-discipline multimodal understanding and
     reasoning benchmark for expert agi. In Proceedings
     of the IEEE/CVF Conference on Computer Vision and
     Pattern Recognition, pp. 9556–9567, 2024. 1
[29] Richard Zhang, Phillip Isola, Alexei A Efros, Eli
     Shechtman, and Oliver Wang. The unreasonable ef-
     fectiveness of deep features as a perceptual metric. In
     Proceedings of the IEEE conference on computer vi-
     sion and pattern recognition, pp. 586–595, 2018. 6
[30] Yuan Zhang, Chun-Kai Fan, Tao Huang, Ming Lu,
     Sicheng Yu, Junwen Pan, Kuan Cheng, Qi She, and
     Shanghang Zhang. Autov: Learning to retrieve vi-


                                                               10

## Page 11

                                                                         models, though typically smaller than on BLINK poten-
      Supplementary Materials                                            tially due to its larger data size, as shown in Fig. 17. Vari-
                                                                         ants that alter marker size or label layout tend to have
                                                                         the strongest effect, while pure color or shape changes are
                                                                         milder but still noticeable. These differences are often suf-
A. Marker style significance                                             ficient to reorder models that are close in performance, es-
                                                                         pecially away from the very top of the leaderboard, as illus-
Figure 10 reports which marker-induced differences on                    trated in the rank changes in Fig. 13c and the significance
VPBench-RD and VPBench-SC are statistically significant                  analysis in Fig. 10.
under paired confidence intervals, we can see that all the
models have at least one style that is statistically significant,
justify the independence of the marker style variance over
the data variance. We additionally show the mean accuracy
shift per marker on VPBench-SC in Figure 11, in which we
see that similar to the results from VPBench-RD in the main
paper (Figure 7), the marker variants with the largest effects
are the ones which involve changing the placement, size,
and representation of the text of the marker. In Figure 12,
we illustrate the marker variants used in our experiments.

B. Change in accuracies on all marker styles
Below we show the full change in accuracy and rank for
all marker styles across BLINK Relative Depth (Fig. 14),
BLINK Semantic Correspondence (Fig. 15), VPBench-SC
(Fig. 16) and VPBench-RD (Fig. 17), with the induced
changes in model ranking isolated in Figures 13a-13d.

BLINK Relative Depth and Semantic Correspondence.
For BLINK relative depth, changing only the marker style
(color, size, shape, or label layout) yields drastic accuracy
shifts, sometimes up to roughly 15% for individual mod-
els, as shown in the accuracy heatmap in Fig. 14. These
shifts are large enough to reorder nearby models in the
leaderboard, with several mid-ranked systems moving up or
down multiple positions across marker variants (Fig. 13a).
BLINK semantic correspondence shows a similar pattern:
accuracy often changes by more than 10% under different
marker styles (Fig. 15), and these shifts again reorder mod-
els with similar default performance (Fig. 13b), so marker
design alone can change which model appears to perform
best on both BLINK tasks.

VPBench Semantic Correspondence. For VPBench-
SC, changing the marker style shifts model accuracies in
systematic ways, with some variants consistently helping or
hurting broad groups of models, as shown in Fig. 16. These
shifts are also large enough to change the relative ordering
of mid-ranked systems, with multiple models swapping po-
sitions across marker styles in Fig. 13d.

VPBench Relative Depth. On VPBench-RD, marker
style changes also lead to clear accuracy shifts for most


                                                                    11

## Page 12

                                                                                                                                                               8B




                                                                                                                                                                                                                                                                                                                                                          8B
                                                                                                                                                               t-




                                                                                                                                                                                                                                                                                                                                                          t-
                                                                                                                                                            ex




                                                                                                                                                                                                                                                                                                                                                       ex
                                                                                         sh




                                                                                                                                                                                                                                                                                        sh
                                                                                                                                                        a-N




                                                                                                                                                                                                                                                                                                                                                   a-N
                                                                                                                                                                          -7B




                                                                                                                                                                                                                                                                                                                                                                     -7B
                                                                                                       Pro




                                                                                                                                                                                                                                                                                                      Pro
                                                                                      Fla




                                                                                                                                                                                                                                                                                     Fla
                                                             no




                                                                                                                                                                                                                                                           no
                                                                                                                        B




                                                                                                                                                                                                                                                                                                                       B
                                                                                                                                         B




                                                                                                                                                                                                                                                                                                                                    B
                                                                                                                                                        lav




                                                                                                                                                                                                                                                                                                                                                   lav
                                                                                                                                                                       -VL




                                                                                                                                                                                                                                                                                                                                                                  -VL
                                                                                                                      3-4




                                                                                                                                                                                                                                                                                                                     3-4
                                                                                                                                          3-8




                                                                                                                                                                                                                                                                                                                                     3-8
                                                         Na




                                                                                                                                                                                                                                                       Na
                                                                                  2.5




                                                                                                 2.5




                                                                                                                                                                                                                                                                               2.5




                                                                                                                                                                                                                                                                                                2.5
                                                                                                                                                     3-L




                                                                                                                                                                                                                                                                                                                                                3-L
                                                                                                                                                                      2.5




                                                                                                                                                                                                                                                                                                                                                                 2.5
                                                                                                                                        VL




                                                                                                                                                                                                                                                                                                                                   VL
                                                                                                                 ma




                                                                                                                                                                                                                                                                                                                ma
                                                       4.1




                                                                                                                                                                                                                                                     4.1
                                                                                 ini




                                                                                                ini




                                                                                                                                                                                                                                                                              ini




                                                                                                                                                                                                                                                                                               ini
                                                                     4o




                                                                                                                                                                                                                                                                    4o
                                                                                                                                                   ma




                                                                                                                                                                                                                                                                                                                                              ma
                                                                                                                                    ern




                                                                                                                                                                                                                                                                                                                               ern
                                                                                                                                                                      en




                                                                                                                                                                                                                                                                                                                                                                 en
                                                                                m




                                                                                                 m




                                                                                                                  m




                                                                                                                                                                                                                                                                               m




                                                                                                                                                                                                                                                                                                m




                                                                                                                                                                                                                                                                                                                 m
                                                        T-




                                                                      T-




                                                                                                                                                                                                                                                      T-




                                                                                                                                                                                                                                                                     T-
                                                                                                                                                                    Qw




                                                                                                                                                                                                                                                                                                                                                               Qw
                                                                                                                                                Lla




                                                                                                                                                                                                                                                                                                                                           Lla
                                                                             Ge




                                                                                              Ge




                                                                                                               Ge




                                                                                                                                                                                                                                                                            Ge




                                                                                                                                                                                                                                                                                             Ge




                                                                                                                                                                                                                                                                                                              Ge
                                                     GP




                                                                   GP




                                                                                                                                                                                                                                                   GP




                                                                                                                                                                                                                                                                  GP
                                                                                                                                Int




                                                                                                                                                                                                                                                                                                                           Int
                                       color_blue        0.4         0.0            1.5              1.8             1.2              -0.1             -0.1*           -3.2*                                                         color_blue        -0.5         -2.1           -3.8*            -2.2            -1.5         -2.6              -0.6           -0.9
                                     color_green         0.0         1.3            -1.3             0.0             -0.2             -0.7             -0.1*           0.4                                                         color_green         0.1          0.3            0.8              1.1             -1.9         -2.3              1.1            -1.4
                                     color_yellow        -0.7        1.1            -1.5             0.8             -0.4             -0.8             0.0*            -1.3                                                        color_yellow        1.0          -0.5           0.5              -1.3            1.5          -1.4              0.8            -1.3
                                          default        0.0*        0.0*           0.0*             0.0*            0.0*             0.0*             0.0*            0.0*                                                             default        0.0*         0.0*           0.0*             0.0*            0.0*         0.0*             0.0*            0.0*
                                   font_scale_0.2        -2.5        1.0            -0.9             3.4*            0.9              -2.9              0.0            -1.6             Yes                                      font_scale_0.2       -5.0*         -2.5           1.0              2.0             -1.3       -10.3*              -0.7           -6.9*    Yes

                                   font_scale_1.0        -0.2        -0.5           -0.2             -2.3            1.4              0.5               0.0            0.8                                                       font_scale_1.0        0.2          -4.2*          -4.1*            -0.8            -2.2         0.3               0.6            -1.1
                            marker_type_diamond          0.0         1.1            -1.1             2.4             -0.5             0.1              -0.2*           0.0                                                marker_type_diamond          0.0          -4.4*          -0.5             0.9             0.7          -1.7              0.6            -4.8*
                             marker_type_square          0.2         -0.3           0.2              1.5             -0.3             -1.4              0.0            1.1                                                 marker_type_square          -0.5         -6.0*          -2.5             -0.9            -1.5         -2.1              0.3            -2.6
                 Variants




                                                                                                                                                                                                               Variants
                                                                                                                                                                                            Significant




                                                                                                                                                                                                                                                                                                                                                                             Significant
                            marker_type_triangle         -0.4        0.2            -0.9             0.5             0.5             -3.0*             -0.2*           -0.1                                               marker_type_triangle         0.3          -4.3*          -3.1*            -1.7            -0.7         -2.3              0.8            -3.4
                                         radius_1        -1.1        1.0            1.2              2.9*            -1.0             1.2              -0.1*           0.7                                                             radius_1        2.6          -2.9           -0.7             0.1             -1.4         2.8               1.0            0.3
                                       radius_10         0.6         -0.4           0.6              -1.4            1.3              1.3              -0.2*           0.4                                                           radius_10         0.9          0.3            1.9              0.1             -0.3         3.0               0.6            -1.2
                                       radius_15         0.2         -1.4           0.9              2.1             2.1              -0.2             -0.1*           1.8                                                           radius_15         1.8          1.4            2.1              1.3             0.4          2.4               1.3            0.9
                                         radius_3        -0.2        3.0*           0.2              2.5             0.2              0.3              0.0*            -1.0
                                                                                                                                                                                        No                                             radius_3        -0.3         0.1            -1.0             1.4             0.4          -0.9              0.2            -1.5
                                                                                                                                                                                                                                                                                                                                                                           No
                                    text_label_12        1.9         2.3            0.3              -1.7            0.0              0.6              9.8*            0.9                                                     text_label_1234         1.2          -0.6           0.9          -3.6*               -1.1        -4.5*              -0.3           -0.7
                                text_offset_below        -0.3        -1.4           -1.6             -1.9            2.3              -1.3              0.0            -0.3                                                   text_offset_below        -1.6         -2.1           1.3              -0.9            0.5          -2.5              0.5            0.2
                                  text_offset_left       -1.7        0.4            -3.3*            1.4             1.6              -1.3             -0.1*           -1.2                                                     text_offset_left       -0.8         -5.9*          1.3              0.1             -3.1         -0.5              0.2            -3.4
                                 text_offset_right       -1.3        -0.8           -1.9             1.5             1.3              -1.0             -0.1*           -1.1                                                    text_offset_right       0.2          -4.3*          -1.2             -1.7            -3.8         -1.6              0.3            -4.1*
                                                                                                            Models                                                                                                                                                                                         Models

                                                                            (a) VPBench-Relative Depth                                                                                                                                                          (b) VPBench-Semantic Correspondence

                  Figure 10. Significance plots of marker variants. Green indicates statistical significance under paired bootstrap. We see that each model
                  has at least 1 marker variant which produces a statistically significant difference in accuracy compared to the default marker.




                                            Absolute Accuracy Shift - SPair-71K Semantic Correspondence
                                                                                              Positive Average Effect                                    Negative Average Effect


                               radius 3                                      0.93%
                              radius 10                                       1.06%
                            color green                                       1.06%
                           color yellow                                         1.17%
                     text offset below                                          1.22%
                              radius 15                                            1.45%
Marker Variant




                               radius 1                                             1.50%
                       text label 1234                                               1.61%
                             color blue                                              1.62%
                 marker type diamond                                                   1.73%
                  marker type triangle                                                                       2.26%
                  marker type square                                                                            2.56%
                         font scale 1.0                                                                          2.63%
                        text offset left                                                                             2.97%
                      text offset right                                                                               3.04%
                         font scale 0.2                                                                                                                                         5.33%
                                                               0             1                   2                          3                     4                     5               6                      7
                                                                                                       Mean Absolute Accuracy Change (%)

                  Figure 11. Absolute marker impact. Mean absolute accu-
                  racy shift on VPBench-Semantic Correspondence induced by each
                  marker variant. Variants which alter the text component of the vi-
                  sual marker typically result in the largest accuracy shifts.




                                                                                                                                                                                                          12

## Page 13

Text display                     Bottom                    Left                    Right                A=1, B=2




Marker size                     radius=1                radius=3                radius=10               radius=15




Text size                        Small text             Large text




Marker shape                    Diamond                   Triangle                Square




Marker color                       Blue                    Green                  Yellow




              Figure 12. Visual Marker Variants. We explore 16 different visual markers in Section 5 of the main paper.




                                                                  13

## Page 14

                                                   re




                                                                                                                                    re
                                                 ua




                                                                                                                                  ua
                                                                       low




                                                                                                                                                        w
                                             sq




                                                                                                                              sq




                                                                                                                                                   elo
                                                                             0.2




                                                                                                                                                              0.2
                                                                   be
                                              pe




                                                                                                                               pe




                                                                                                                                                  tb
                                                                   et
                                   ma lue




                                                                                                                    ma lue
                                                                           le




                                                                                                                                                            le
                                         r ty




                                                                                                                          r ty




                                                                                                                                                    e
                                                               ffs




                                                                                                                                                ffs
                                                         3




                                                                                                                                          tex 3
                                                                         ca




                                                                                                                                                          ca
                           lt




                                                                                                            lt
                                       b




                                                                                                                        b
                                     rke




                                                                                                                      rke
                                                      ius




                                                                                                                                       ius
                                                              to




                                                                                                                                             to
                          fau




                                                                                                           fau
                                                                        ts




                                                                                                                                                         ts
                                 lor




                                                                                                                  lor
                                                   rad




                                                                                                                                    rad
                                                                       fon




                                                                                                                                                        fon
                                                             tex
                          de




                                                                                                           de
                                co




                                                                                                                 co
         Llama 4 Scout     1         1       1           1         1         1           Gemini 2.5 Pro     1         1       1           1        1          1

        Gemini 2.5 Pro     2         2       2           3         3         2          Gemini 2.5 Flash    2         1       2           2        1          2

       Gemini 2.5 Flash    2         3       5           2         3         3            Llama 4 Scout     3         3       4           3        3          4

          Qwen3-VL-8B      4         4       3           6         2         5                  GPT-4.1     4         5       2           5        4          7

          InternVL3-8B     4         7       8           8         8         7             Qwen3-VL-8B      5         4       5           4        5          3

               GPT-4.1     6         4       3           4         3         3                   GPT-4o     6         6       6           6        5          5

                GPT-4o     7         6       6           5         6         6             Gemma 3-4B       7         9       9           9        8          9

        Qwen2.5-VL-7B      8         8       7           6         7         8           Qwen2.5-VL-7B      7         7       7           7        9          7

          Gemma 3-4B       9         9       9           9         9         9             InternVL3-8B     9         8       8           8        7          6


                                (a) BLINK RD                                                                     (b) BLINK SC
                                                    re




                                                                                                                                     re
                                                 ua




                                                                                                                                  ua
                                                                     low




                                                                                                                                                       w
                                             sq




                                                                                                                              sq




                                                                                                                                                   elo
                                                                             0.2




                                                                                                                                                              0.2
                                                                   be
                                            pe




                                                                                                                             pe




                                                                                                                                                  tb
                                                                   et
                                ma lue




                                                                                                                 ma lue
                                                                             le




                                                                                                                                                              le
                                       r ty




                                                                                                                        r ty




                                                                                                                                                    e
                                                               ffs




                                                                                                                                                ffs
                                                         3




                                                                                                                                          tex 3
                                                                         ca




                                                                                                                                                          ca
                           lt




                                                                                                            lt
                                      b




                                                                                                                       b
                                   rke




                                                                                                                    rke
                                                      ius




                                                                                                                                       ius
                                                              to




                                                                                                                                             to
                          fau




                                                                                                           fau
                                                                        ts




                                                                                                                                                         ts
                                  lor




                                                                                                                   lor
                                                   rad




                                                                                                                                    rad
                                                                       fon




                                                                                                                                                        fon
                                                             tex
                          de




                                                                                                           de
                                co




                                                                                                                 co
         Llama 4 Scout     1         2       1           1         1         2           Gemini 2.5 Pro     1         1       1           1        2          1

       Gemini 2.5 Flash    2         1       2           3         2         3          Gemini 2.5 Flash    2         2       2           2        1          2

        Gemini 2.5 Pro     3         3       3           2         3         1            Llama 4 Scout     3         3       3           3        3          6

          Qwen3-VL-8B      4         4       4           4         4         4             Qwen3-VL-8B      4         4       4           4        4          3

               GPT-4.1     5         5       5           5         5         5                  GPT-4.1     5         5       5           5        5          3

          InternVL3-8B     6         6       7           7         6         7                   GPT-4o     6         6       6           6        6          5

        Qwen2.5-VL-7B      7         8       6           8         7         8             InternVL3-8B     7         8       7           7        8          9

                GPT-4o     8         7       8           6         8         6           Qwen2.5-VL-7B      8         7       8           8        7          8

          Gemma 3-4B       9         9       9           9         9         9             Gemma 3-4B       9         9       9           9        9          7


                               (c) VPBench RD                                                                   (d) VPBench SC

Figure 13. Change in rank for different marker styles across BLINK RD, BLINK SC, VPBench RD, and VPBench SC. For each dataset
we see large fluctuations in rank across marker types, indicating that these tasks are highly sensitive to small visual changes.




                                                                                   14

## Page 15

                                                             Accuracy Delta Heatmap (All Variants) - BLINK Relative Depth




                                                                                           nd




                                                                                          le
                                                                                         re
                                                                                       mo




                                                                                        ng
                                                                                      ua




                                                                                                                                                          low
                                                                                   tria
                                                                                   dia




                                                                                                                                                          ht
                                                                                   sq




                                                                                                                                                         t
                                                                                 0.2


                                                                      rke 0




                                                                                                                                                      rig
                                                                                                                                                      be


                                                                                                                                                      lef
                                                                                                                                                       2
                                                                   ma le 1.

                                                                                pe


                                                                                pe

                                                                                pe
                                                      ow
                                          en




                                                                                                                                                   l1

                                                                                                                                                   et


                                                                                                                                                   et

                                                                                                                                                   et
                                 e




                                                                 le



                                                                           r ty


                                                                           r ty

                                                                           r ty




                                                                            10


                                                                                                                                 15
                                                    ll




                                                                                                                                                be
                                      gre
                      LT

                             blu




                                                                                                                                               ffs


                                                                                                                                               ffs

                                                                                                                                               ffs
                                                                            1




                                                                                                                                                3
                                                               ca


                                                                         ca
                                                 ye
                        U




                                                                                                                                           t la
                                                                      rke

                                                                      rke



                                                                       ius

                                                                       ius


                                                                                                                               ius


                                                                                                                                            ius




                                                                                                                                           to


                                                                                                                                           to

                                                                                                                                           to
                                                             ts


                                                                      ts
                     FA

                            lor

                                     lor

                                                lor
                                                                                                                                                                                                 15




                                                                   rad

                                                                   rad


                                                                                                                              rad


                                                                                                                                       rad
                                                            fon


                                                                         fon




                                                                   ma

                                                                   ma




                                                                                                                                        tex

                                                                                                                                        tex


                                                                                                                                        tex

                                                                                                                                        tex
                   DE

                            co

                                    co

                                                co
  Llama 4 Scout      89.4    +1.2     +0.0           -2.4      +1.2            -3.5   -1.2    +1.2    +0.0    -3.5    -1.2      +1.2    +1.2       +1.2        +0.0         -3.5      -1.2
                      R1      R1       R1             R1        R1              R1     R1      R1      R1      R1      R1        R1      R1         R1          R1           R1        R1

 Gemini 2.5 Pro      77.6    +5.9     +5.9       +0.0          +4.7            -1.2   +2.4    +7.1    +4.7    +1.2    +4.7      -3.5     -1.2      +1.2        -1.2         +4.7      +4.7       10
                      R2      R2       R2         R3            R2              R5     R2      R2      R2      R4      R2        R5       R3        R3          R3           R2        R2

Gemini 2.5 Flash     77.6    +3.5     +0.0       +1.2          +2.4        +3.5       +2.4    -1.2    -1.2    +2.4    +2.4      +4.7    +2.4       -2.4        -1.2         +3.5      +3.5
                      R2      R3       R4         R2            R3          R2         R2      R5      R3      R2      R3        R2      R2         R5          R3           R3        R3
                                                                                                                                                                                                 5
   Qwen3-VL-8B       76.5    +2.4     +2.4       +1.2          +0.0        +1.2       -4.7    +1.2    -2.4    +0.0    +3.5      +4.7     -5.9      +8.2        +3.5         -3.5      +1.2
                      R4      R4       R3         R3            R5          R3         R6      R3      R5      R6      R3        R3       R6        R2          R2           R5        R4




                                                                                                                                                                                                         Delta Accuracy (%)
   InternVL3-8B      76.5    -9.4        -3.5        -7.1         -4.7     +1.2       -10.6   -12.9   -10.6   -3.5    -3.5      -5.9     -7.1      -4.7        -8.2         -3.5      -5.9       0
                      R4      R7          R7          R7           R7       R3         R7      R8      R7      R7      R7        R7       R8        R7          R8           R5        R6

        GPT-4.1      75.3    +3.5     +1.2           -1.2      +4.7            -3.5   -1.2    +2.4    -2.4    +4.7    +3.5      +3.5    +0.0       +2.4        +1.2         +4.7      +2.4
                      R6      R4       R5             R5        R3              R7     R4      R3      R6      R2      R5        R4      R4         R4          R3           R4        R4
                                                                                                                                                                                                     5
         GPT-4o      71.8    +2.4     +2.4           -1.2      +3.5        +1.2       +2.4    +3.5    +3.5    +5.9    +5.9      +2.4    +2.4       +1.2        -1.2         -2.4      -1.2
                      R7      R6       R6             R6        R6          R6         R4      R6      R4      R5      R6        R5      R5         R6          R6           R7        R6

 Qwen2.5-VL-7B       70.6    -9.4        -3.5        -5.9      -15.3       +0.0       -4.7    -3.5    -9.4    +1.2    +1.2      +0.0    +0.0       -2.4        -1.2         -3.5      -12.9
                      R8      R8          R8          R8        R8          R8         R7      R7      R8      R8      R8        R7      R6         R8          R7           R8        R8            10

   Gemma 3-4B        52.9    +4.7        -3.5        -1.2         -3.5         -3.5   +0.0    +2.4    +3.5    +3.5    +1.2      +0.0    +3.5       +4.7        +1.2         -2.4      +1.2
                      R9      R9          R9          R9           R9           R9     R9      R9      R9      R9      R9        R9      R9         R9          R9           R9        R9

                                                                                                Marker Styles                                                                                        15


         Figure 14. Change in accuracy and rank for different marker styles in BLINK relative depth task.




                                                Accuracy Delta Heatmap (All Variants) - BLINK Semantic Correspondence
                                                                                                   nd




                                                                                                  le
                                                                                                re
                                                                                               mo




                                                                                               ng
                                                                                              ua




                                                                                                                                                                      w
                                                                                           tria
                                                                                           dia




                                                                                                                                                                                             t
                                                                                           sq




                                                                                                                                                                 elo
                                                                                                                                                         4




                                                                                                                                                                                         gh
                                                                                                                                                                                ft
                                                                                                                                                     23
                                                                   0.2


                                                                              rke 0




                                                                                                                                                                               le
                                                                           ma le 1.




                                                                                                                                                                                         ri
                                                                                        pe


                                                                                        pe

                                                                                        pe




                                                                                                                                                                  b
                                                       w
                                          en




                                                                                                                                                   l1
                                                   llo




                                                                                                                                                               et


                                                                                                                                                                            et

                                                                                                                                                                                      et
                                 e




                                                                le



                                                                                   r ty


                                                                                   r ty

                                                                                   r ty




                                                                                    10


                                                                                                                                 15




                                                                                                                                                    be
                                      gre
                      LT

                             blu




                                                                                                                                                           ffs


                                                                                                                                                                          ffs

                                                                                                                                                                                     ffs
                                                                                    1




                                                                                                                                          3
                                                              ca


                                                                                 ca
                                                 ye
                       U




                                                                                                                                                t la
                                                                              rke

                                                                              rke



                                                                               ius

                                                                               ius


                                                                                                                               ius


                                                                                                                                        ius




                                                                                                                                                          to


                                                                                                                                                                       to

                                                                                                                                                                                   to
                                                             ts


                                                                          ts
                    FA

                            lor

                                     lor

                                                lor




                                                                           rad

                                                                           rad


                                                                                                                              rad


                                                                                                                                       rad
                                                            fon


                                                                         fon




                                                                           ma

                                                                           ma




                                                                                                                                             tex

                                                                                                                                                         tex


                                                                                                                                                                      tex

                                                                                                                                                                                tex
                   DE

                            co

                                    co

                                                co




 Gemini 2.5 Pro      63.5    -1.9        -1.9        -1.0      +1.0            -1.0   -1.9    -2.9    -3.8    +0.0    -3.8      -2.9     -1.9      -2.9        -3.8         -7.7      -7.7       15
                      R1      R1          R1          R1        R1              R1     R1      R1      R3      R2      R2        R2       R1        R1          R1           R1        R2

Gemini 2.5 Flash     55.8    +5.8     +5.8       +1.0          +7.7        +4.8       +3.8    -3.8    +9.6    +9.6    +6.7      +8.7    +3.8       +2.9        +3.8         -1.0      +4.8
                      R2      R1       R1         R2            R2          R2         R2      R2      R1      R1      R1        R1      R2         R2          R1           R3        R1
                                                                                                                                                                                                 10
  Llama 4 Scout      53.8    +5.8     +4.8       +2.9             -8.7         -1.9   +5.8    -4.8    +7.7    +4.8    +1.0      -2.9    +0.0       +3.8        -1.9         +1.9      -3.8
                      R3      R3       R3         R2               R4           R3     R2      R4      R2      R3      R4        R4      R3         R3          R3           R1        R3
                                                                                                                                                                                                 5
        GPT-4.1      51.0    -6.7        -3.8    +0.0          -18.3       +0.0       -2.9    +1.0    -1.0    -5.8    +0.0      -1.0    +0.0       +3.8        -3.8         -7.7      -7.7
                      R4      R5          R5      R5            R7          R4         R4      R2      R5      R6      R5        R5      R5         R4          R4           R4        R5
                                                                                                                                                                                                         Delta Accuracy (%)
   Qwen3-VL-8B       49.0    -2.9     +4.8       +7.7          +3.8            -3.8   -1.0    -3.8    +2.9    +2.9    +9.6      +5.8    +3.8       +3.8        -2.9         -5.8      -1.0       0
                      R5      R4       R4         R2            R3              R6     R4      R5      R4      R4      R3        R3      R4         R5          R5           R4        R4

         GPT-4o      46.2    -2.9        -2.9        -4.8         -1.9     +0.0       -1.0    -3.8    -6.7    +4.8    -1.9      +0.0     -1.0      -3.8        +0.0         -2.9      -5.8
                      R6      R6          R6          R6           R5       R5         R6      R6      R6      R5      R6        R6       R6        R6          R5           R4        R6
                                                                                                                                                                                                     5
   Gemma 3-4B        32.7    -8.7        -6.7        -3.8         -1.9         -3.8   -8.7    -3.8    -1.9    -2.9    -4.8      -1.9     -1.9      -7.7        -1.9         -5.8      -3.8
                      R7      R9          R9          R9           R9           R9     R9      R9      R9      R9      R9        R9       R9        R9          R8           R9        R9
                                                                                                                                                                                                     10
 Qwen2.5-VL-7B       32.7    +1.9     +1.0       +7.7          +0.0            -1.0   +1.0    +7.7    +1.9    +5.8    -1.9     +10.6    +0.0       +1.9        -4.8         -1.0      +1.0
                      R7      R7       R7         R7            R7              R7     R8      R7      R8      R7      R8       R7       R7         R7          R9           R8        R7

   InternVL3-8B      26.9    +4.8     +2.9       +11.5        +13.5        +3.8       +8.7    +8.7    +8.7    +10.6   +11.5     +9.6    +4.8       +0.0        +8.7         +8.7      +4.8           15
                      R9      R8       R8         R8           R6           R8         R7      R8      R7      R8      R7        R8      R8         R8          R7           R7        R8

                                                                                                Marker Styles

Figure 15. Change in accuracy and rank for different marker styles in BLINK semantic correspondence task.




                                                                                               15

## Page 16

                                           Accuracy Delta Heatmap (All Variants) - SPair-71K Semantic Correspondence




                                                                                               nd




                                                                                                                      le
                                                                                                           re
                                                                                            mo




                                                                                                                    ng
                                                                                                       ua




                                                                                                                                                                                    low
                                                                                                                   tria
                                                                                        dia




                                                                                                                                                                                                            ht
                                                                                                       sq




                                                                                                                                                                         34




                                                                                                                                                                                                  t
                                                                   .2


                                                                                .0




                                                                                                                                                                                                          rig
                                                                                                                                                                                   be


                                                                                                                                                                                               lef
                                                                                                                                                                       12
                                                                                      pe


                                                                                                  pe

                                                                                                              pe
                                                        w

                                                                    0


                                                                                 1
                                         en

                                                    llo




                                                                                                                                                                                et


                                                                                                                                                                                             et

                                                                                                                                                                                                       et
                                e




                                                                 le


                                                                              le
                                                                                     r ty


                                                                                                r ty

                                                                                                            r ty




                                                                                                                                                                        l
                                                                                                                                        10


                                                                                                                                                  15




                                                                                                                                                                     be
                                     gre
                     LT

                            blu




                                                                                                                                                                              ffs


                                                                                                                                                                                          ffs

                                                                                                                                                                                                      ffs
                                                                                                                              1




                                                                                                                                                            3
                                                             ca


                                                                          ca
                                                ye
                      U




                                                                                                                                                                   t la
                                                                                 rke


                                                                                              rke

                                                                                                           rke



                                                                                                                           ius

                                                                                                                                      ius


                                                                                                                                                ius


                                                                                                                                                          ius




                                                                                                                                                                              to


                                                                                                                                                                                          to

                                                                                                                                                                                                     to
                                                            ts


                                                                         ts
                   FA

                           lor

                                    lor

                                               lor




                                                                                                                        rad

                                                                                                                                     rad


                                                                                                                                               rad


                                                                                                                                                         rad
                                                           fon


                                                                        fon

                                                                               ma


                                                                                            ma

                                                                                                       ma




                                                                                                                                                                tex

                                                                                                                                                                          tex


                                                                                                                                                                                       tex

                                                                                                                                                                                                tex
                   DE

                           co

                                   co

                                               co
                                                                                                                                                                                                                 15
 Gemini 2.5 Pro     65.0    -2.1     +1.0           -1.4     +1.9             -0.7     +0.8         -0.8         -1.6      +0.0        +0.1      +1.4      +1.6       -3.1      -1.0         +0.0      -1.8
                     R1      R1       R1             R2       R1               R1       R1           R1           R1        R1          R1        R1        R1         R2        R2           R1        R1

Gemini 2.5 Flash    63.8    -4.0     +0.3       +0.1         +0.6             -4.8     -0.9         -2.6         -3.1      -1.2        +1.4      +1.5      -1.7       +0.6      +0.6         +0.8      -1.5
                     R2      R2       R2         R1           R2               R2       R2           R2           R2        R2          R1        R2        R2         R1        R1           R2        R2       10

  Llama 4 Scout     57.9    +0.1        -0.9        -1.4     -17.1            -2.1     +0.2       +0.9           -0.2      -1.9        +0.2      +2.7      +0.6       -0.9      -0.8         -6.0      -4.1
                     R3      R3          R3          R4       R6               R3       R3         R3             R3        R3          R3        R3        R3         R3        R3           R4        R3
                                                                                                                                                                                                                 5
   Qwen3-VL-8B      54.8    -0.1     +0.5       +2.0             -6.0         -2.9     +1.1         -3.3         +0.7      +1.2        +1.0      +1.8      +1.1       -1.8      -1.1         -2.3      -2.0
                     R4      R4       R4         R3               R3           R4       R4           R4           R4        R3          R4        R4        R4         R4        R4           R3        R4




                                                                                                                                                                                                                         Delta Accuracy (%)
        GPT-4.1     49.8    -0.9        -0.9        -0.5         -1.0         -5.1     -0.8         -2.8         -3.8      -1.7        -1.8      -0.6      -0.2       -0.9      -2.3         -4.5      -4.4      0
                     R5      R5          R5          R5           R3           R5       R5           R5           R5        R5          R5        R5        R5         R5        R5           R5        R5

         GPT-4o     46.4    -2.1     +0.2           -0.6         -2.6         -4.2     -4.5         -6.1         -4.4      -2.9        +0.3      +1.4      +0.0       -0.7      -2.0         -5.9      -4.4
                     R6      R6       R6             R6           R5           R6       R6           R6           R6        R6          R6        R6        R6         R6        R6           R6        R6
                                                                                                                                                                                                                     5
   InternVL3-8B     36.9    -2.6        -2.3        -1.4     -10.3        +0.3         -1.7         -2.0         -2.3      +2.8        +3.1      +2.4      -0.9       -4.5      -2.5         -0.5      -1.6
                     R7      R8          R8          R7       R9           R7           R7           R7           R7        R7          R7        R7        R7         R8        R8           R7        R7

 Qwen2.5-VL-7B      36.3    -1.1        -1.6        -1.7         -7.2         -1.4     -4.8         -3.1         -3.6      +0.2        -1.4      +0.9      -1.8       -1.0      +0.1         -3.7      -3.8          10
                     R8      R7          R7          R8           R8           R8       R8           R8           R8        R8          R8        R8        R8         R7        R7           R8        R8

   Gemma 3-4B       30.7    -1.5        -1.8    +1.6             -1.2         -2.1     +0.8         -1.5         -0.7      -1.4        -0.2      +0.5      +0.5       -1.0      +0.6         -3.1      -3.7
                     R9      R9          R9      R9               R7           R9       R9           R9           R9        R9          R9        R9        R9         R9        R9           R9        R9
                                                                                                                                                                                                                     15
                                                                                                       Marker Styles

 Figure 16. Change in accuracy and rank for different marker styles in VPBench-Semantic Correspondence.




                                                            Accuracy Delta Heatmap (All Variants) - DA-2K Relative Depth
                                                                                                d




                                                                                                                        gle
                                                                                               on

                                                                                                           are
                                                                                            iam




                                                                                                                       n




                                                                                                                                                                                        low
                                                                                                       qu

                                                                                                                   ria




                                                                                                                                                                                        ht
                                                                                        d




                                                                                                                                                                                       t
                                                                                                    es

                                                                                                                 et
                                                                   0.2


                                                                              rke .0




                                                                                                                                                                                    rig
                                                                                                                                                                                    be


                                                                                                                                                                                    lef
                                                                                                                                                                                     2
                                                                                     pe
                                                      w




                                                                                      1
                                         en




                                                                                                                                                                                 l1
                                                                                                  typ

                                                                                                             typ
                                                     llo




                                                                                                                                                                                 et


                                                                                                                                                                                 et

                                                                                                                                                                                 et
                                e




                                                                 le


                                                                                   le
                                                                                 r ty




                                                                                                                                           10


                                                                                                                                                     15




                                                                                                                                                                              be
                                     gre
                     LT

                            blu




                                                                                                                                                                             ffs


                                                                                                                                                                             ffs

                                                                                                                                                                             ffs
                                                                                                                               1




                                                                                                                                                               3
                                                             ca


                                                                          ca
                                                ye




                                                                                                   r

                                                                                                               r
                      U




                                                                                                                                                                      t la
                                                                                               rke

                                                                                                           rke



                                                                                                                           ius

                                                                                                                                      ius


                                                                                                                                                 ius


                                                                                                                                                           ius




                                                                                                                                                                          to


                                                                                                                                                                          to

                                                                                                                                                                          to
                                                            ts


                                                                         ts
                   FA

                           lor

                                    lor

                                               lor




                                                                                                                                                                                                                     4
                                                                                                                          rad

                                                                                                                                     rad


                                                                                                                                                rad


                                                                                                                                                          rad
                                                           fon


                                                                        fon

                                                                                ma


                                                                                            ma

                                                                                                       ma




                                                                                                                                                                   tex

                                                                                                                                                                       tex


                                                                                                                                                                       tex

                                                                                                                                                                       tex
                   DE

                           co

                                   co

                                               co




  Llama 4 Scout     73.7    -1.0        +0.8        -0.6         -1.8         -2.7      -1.6        -1.0         -1.2      +0.1         -0.3      -0.1     +0.7        +0.9        -2.8       -3.6        -3.4
                     R1      R2          R1          R1           R2           R2        R2          R1           R1        R1           R1        R1       R1          R1          R1         R2          R2
                                                                                                                                                                                                                     3
Gemini 2.5 Flash    71.4    +1.9        -0.8        -1.5         -0.5         +0.4      -0.7        +0.7         -0.7      +1.5        +0.9       +1.3     +0.4        +0.5        -1.2       -2.5        -1.5
                     R2      R1          R3          R3           R3           R1        R3          R2           R3        R3          R2         R2       R3          R2          R2         R3          R3
                                                                                                                                                                                                                     2
 Gemini 2.5 Pro     69.3    +3.0        +1.5        +2.7         +4.1         -1.5     +3.0         +2.2         +2.3      +3.8         -0.3      +3.2     +2.9        +1.9        -0.7      +2.9         +2.3
                     R3      R3          R2          R2           R1           R3       R1           R3           R2        R2           R3        R3       R2          R3          R3        R1           R1

                    69.0    +0.1        -1.3        -3.1         +0.1         -2.4      -2.3        -1.7         -1.8      +1.1         -0.6      -3.0      -1.7       +0.1        -3.4       -2.5        +0.3       1
   Qwen3-VL-8B       R4      R4          R4          R4           R4           R4        R4          R4           R4        R4           R4        R4        R4         R4          R4         R4          R4
                                                                                                                                                                                                                         Delta Accuracy (%)
        GPT-4.1     64.3    +0.0        -0.3        -0.3         +0.3         +0.2      -0.5        -1.7         -1.5      +1.9         -0.2      -0.3     +0.4        +1.2        +0.2      +0.5         +0.7       0
                     R5      R5          R5          R5           R5           R5        R5          R5           R5        R5           R5        R5       R5          R5          R5        R5           R5

   InternVL3-8B     62.8    -0.1        -0.7        -0.8         -2.9         +0.5     +0.1         -1.4         -2.9      +1.2        +1.3       -0.2     +0.3        +0.5        -1.3       -1.3        -1.0
                     R6      R6          R7          R7           R7           R6       R6           R7           R8        R6          R5         R7       R7          R7          R6         R6          R6            1

 Qwen2.5-VL-7B      61.3    -3.3        +0.4        -1.4         -1.6         +0.7     +0.0         +1.1         -0.2      +0.6        +0.4       +1.7      -1.0       +0.8        -0.4       -1.3        -1.2
                     R7      R8          R8          R8           R8           R7       R8           R6           R7        R8          R7         R6        R8         R8          R7         R8          R8
                                                                                                                                                                                                                         2
         GPT-4o     61.1    +0.0        +1.4        +1.1         +1.0         -0.5     +1.1         -0.3         +0.3      +1.0         -0.3      -1.4     +3.0        +2.5        -1.4      +0.5         -0.8
                     R8      R7          R6          R6           R6           R8       R7           R8           R6        R7           R8        R8       R6          R6          R8        R6           R7
                                                                                                                                                                                                                         3
   Gemma 3-4B       50.5    +1.2        -0.2        -0.4         +0.9         +1.4      -0.5        -0.3         +0.5         -1.0     +1.3       +2.1     +0.2        +0.0        +2.3      +1.5         +1.3
                     R9      R9          R9          R9           R9           R9        R9          R9           R9           R9       R9         R9       R9          R9          R9        R9           R9

                                                                                                       Marker Styles                                                                                                     4


          Figure 17. Change in accuracy and rank for different marker styles in VPBench-Relative Depth.




                                                                                                    16
