# Visual Prompting in Multimodal Large Language Models A Survey

- Source PDF: `Visual Prompting in Multimodal Large Language Models A Survey.pdf`
- Extraction method: `pdftotext -layout`
- Generated: `2026-04-02T15:21:31Z`

---

## Page 1

                                             Visual Prompting in Multimodal Large Language Models: A Survey
                                         Junda Wu1 Zhehao Zhang2 Yu Xia1 Xintong Li1 Zhaoyang Xia3 Aaron Chang4
                                             Tong Yu5 Sungchul Kim5 Ryan A. Rossi5 Ruiyi Zhang5 Subrata Mitra5
                                                  Dimitris N. Metaxas3 Lina Yao6,7 Jingbo Shang1 Julian McAuley1
                                               1
                                                 UC San Diego 2 Dartmouth College 3 Rutgers University 4 UC Los Angeles
                                                  5
                                                    Adobe Research 6 The University of New South Wales 7 CSIRO’s Data61
                                        {juw069,yux078,xil240,jshang,jmcauley}@ucsd.edu zhehao.zhang.gr@dartmouth.edu
                                                    zx149@rutgers.edu aaronchang21@ucla.edu dnm@cs.rutgers.edu
                                           {tyu,sukim,ryrossi,ruizhang,sumitra}@adobe.com lina.yao@data61.csiro.au

                                                              Abstract                           as a new paradigm, complementing textual prompt-
                                                                                                 ing and enabling more fine-grained and pixel-level
                                             Multimodal large language models (MLLMs)
                                                                                                 instructions on multimodal input. Since visual
                                             equip pre-trained large-language models
                                             (LLMs) with visual capabilities.        While       prompting methods can take heterogeneous forms
arXiv:2409.15310v1 [cs.LG] 5 Sep 2024




                                             textual prompting in LLMs has been widely           for various tasks and often operate at pixel-level
                                             studied, visual prompting has emerged for           granularity, general prompt templates might not
                                             more fine-grained and free-form visual              apply to different images, making instance-level
                                             instructions. This paper presents the first         visual prompt generation necessary. Therefore, we
                                             comprehensive survey on visual prompting            provide a comprehensive categorization of current
                                             methods in MLLMs, focusing on visual
                                                                                                 visual prompting methods (Section 2) and methods
                                             prompting, prompt generation, compositional
                                             reasoning, and prompt learning. We categorize
                                                                                                 to generate (Section 3) such visual prompts.
                                             existing visual prompts and discuss generative         Despite the success of visual prompting meth-
                                             methods for automatic prompt annotations            ods in augmenting MLLM’s visual abilities, several
                                             on the images. We also examine visual               works also suggest that MLLMs can be misaligned
                                             prompting methods that enable better align-         with visual prompts, due to the lack of heteroge-
                                             ment between visual encoders and backbone           neous visual prompting training data during the pre-
                                             LLMs, concerning MLLM’s visual grounding,           training stage (Yan et al., 2024; Lin et al., 2024b).
                                             object referring, and compositional reasoning
                                                                                                 This misalignment can cause MLLMs to neglect
                                             abilities. In addition, we provide a summary
                                             of model training and in-context learning           or misinterpret certain visual prompts, causing hal-
                                             methods to improve MLLM’s perception and            lucination problems. Therefore, we summarize
                                             understanding of visual prompts. This paper         existing efforts in aligning visual prompting with
                                             examines visual prompting methods developed         MLLM’s perception and reasoning enabling more
                                             in MLLMs and provides a vision of the future        controllable compositional reasoning (Section 5).
                                             of these methods.                                   In addition, we examine existing pre-training, fine-
                                                                                                 tuning (Section 6), and in-context learning methods
                                         1   Introduction
                                                                                                 (Section 7) that fundamentally align MLLMs with
                                         Multimodal large language models (MLLMs) (Li            multimodal augmented prompts.
                                         et al., 2023b; Liu et al., 2024a), which augment pre-      Existing surveys on LLM prompting are limited
                                         trained large language models (LLMs) with visual        to textual prompt design (Gu et al., 2023; Schul-
                                         capabilities, enable visual understanding and rea-      hoff et al., 2024) and in-context demonstrations
                                         soning on complex multimodal tasks (Zhou et al.,        (Xu et al., 2024b; Li, 2023), which lack literature
                                         2024b; Jia et al., 2024). However, limited by using     coverage of pixel-level instructions and multimodal
                                         textual prompts to describe and specify visual ele-     interactions. Visual prompting is also studied in
                                         ments (Lin et al., 2024a; Wu et al., 2024d), conven-    computer vision. However, relevant surveys are
                                         tional prompting methods fall short of providing        limited to vision tasks with vision backbone mod-
                                         accurate visual grounding and referring to detailed     els (Lei et al., 2024b; Zhang et al., 2024b), while
                                         visual information, which can cause visual halluci-     multimodal perception and reasoning tasks involv-
                                         nations (Bai et al., 2024; Huang et al., 2024b) and     ing MLLMs are absent. In addition, one recent sur-
                                         language bias (Wu et al., 2024b; Qu et al., 2024).      vey on Segment Anything Models (SAM) (Zhang
                                            Recently, visual prompting methods have              et al., 2023a) explores various applications of SAM
                                         emerged (Zhang et al., 2024a; Wu et al., 2024f)         in MLLMs. However, this work is limited to the

## Page 2

                                                                                                                      *+ (/)                                                                                         *+ (-. (/, 1))                                                                                                                           345678
                                                          images, instruction following in simulation, and additional spatial inference tasks such as localization.
   omposed into regions of interest and subsequently encoded
                                                                                                                                                                                                                                                                                                                  &




                                                                      arXiv:2402.07872v1 [c
   tokens. By integrating region tokens into user instructions
    esponses, we seamlessly enable Groma to understand We  user-find, perhaps surprisingly, that our approach enables zero-shot control of robotic systems without any
   ognition                                                                                                                                                                                                                                                                                                    Embedding


                                                 50-100 masks
    ion inputs and ground its textual output to images. Besides,
                                                          robot training data, navigation in a variety of environments, and other capabilities. Although current
    the grounded chat ability of Groma, we curate a visually                                                                                                                                                                                                                                                                                               CLIP
   REC)
    struction dataset by leveraging the powerful GPT-4Vperformance
                                                            and               is far from perfect, our work highlights potentials and limitations of this new regime and
   pting techniques. Compared with MLLMs that rely on the                                                                          MLLM Image Encoder                                                                                                                                                                                                      Image
                                                          shows a promising approach for Internet-Scale VLMs in robotic and spatial reasoning domains.
   odel or external module for localization, Groma consistently
                                                                                                                                                                                                                                                                   REC: This is a photo of
    s superior performances in standard referring and grounding                                                                                                                                                                                                                                                                                           Encoder
   , highlighting the advantages of embedding localization into
    ization. Project page: https://groma-mllm.github.io/.            Task: What actions should the robot Task: What numbers overlay the “L Task: What actions should the robot
                                                                                                                                                                        12     Task: What actions should the robot
                                                                                                                                                                               S. Fan et al.
                                                                                                                                                                                                                                                                   CNT: How many cats are there?
                                                                                                                   take to pick up the DNA chew toy?     kid”?                                          take to go to wooden bench without
                                                                                                                                                                                                        hitting the obstacle?
                                                                                                                                                                                                                                        3
                                                                                                                                                                                                                                                     pink plate?   HAL: Is there a dog?
                                                                                                                                                                                                                                                     take to put the pepper shaker on the

                                                                                                                                                                                                                                                                                                                 REVERIE
                          Hallucination                                                                                                                                                                                                                                  Picture
                                                100-200 masks


                                                                                                                                                                                                                                                                                                                  Ground-Truth: Go to the level 2
                                                                                                                                                                                                                                              4                    Task-specific Text Prompts
                                                                                                                                                                                                                                                                      bed
                                                                                                                                                                                                                                                                                   3
                                                                                                                                                                                                                                                                                                    hallway       bathroom that has the tub in the
                                                                                                                                                                                                                                                                                                                                                               REC
                            (HAL)                                                                                                                                                                                                                                                  4           1     2            center of the room and bring me
                                                                                                                                                                                                                                                                                                                  the towel that's laying on the side
                                                                                                                                                   -. (/, 1))                                                                                                       bedroom                                       of the tub.
                                                                                                                                                                                                                                                                                                                                                               CNT
    t-               Please give a brief                                                                                                                                                                                                                                           5                             Landmarks: bathroom, hallway,
                     description of <region>.
                                                                                                                   Iteration 0:                          Iteration 0:                                    Iteration 0:                                Iteration 0:                                                bedroom, bathtub, towel                       HAL
    n>.              A large dinosaur skeleton.                                                                    Arrows: [7, 13, 18]                   Markers: [10, 1, 14, 17]                        Arrows: [12, 13, 14]                 5      Arrows: [1] bathhub           6
                                                                                                                                                                                                                                                                                                                 Refinement: Go to the bathroom

    to drive like this?
                                                                 Bounding-box
                                                                [grounding] Can you describe this image
                                                                in details?                                                Markers                           Pixel-level                            Soft Prompt                                                    towel         bathroom
                                                                                                                                                                                                                                                                                                                 down the hallway next to the
                                                                                                                                                                                                                                                                                                                 bedroom and bring me the towel
                                                                                                                                                                                                                                                                                                                 hanging on the bathtub.
                                                                                                                                                                                                                                                                                                                                                                Tas
                 It's not advisable. The man is
                                                200-300 masks




                 holding a cup in one hand and                  In this image, we see a woman sitting on


   rring expressions comprehension
                                                                a concrete bench working on her laptop.

                                                                                                                                                                 Naming     keypoints
                                                                                                                                                                  Visual Prompting (Sec. 2)                                                                         Perception & Reasoning
                 talking on the phone, which                                                                                                                                                                                             Fig. 3: Visual comparison results between ground truth and BEVInstructor for
                 means he's not using both                      She's surrounded by a green bag and a


  erview of our proposed Transferable Visual                      Prompting (TVP) method (Sec.                        for4adapting           MLLMs. TVP optim
                 hands on the steering wheel.                   white bicycle that's leaning against the                                                                                                                                 instruction generation on REVERIE [69]. See §4.3 for more details.
                 This could be a distraction and                bench. Behind her, there's a large brick
                                                                                                                              & 5)
                                                     A/Q        building and a tree.



                        .
                 increase the risk of an accident.
                                                                                                                   Iteration 1:                          Iteration 4:                                    Iteration 3:                             Table  4: Ablation
                                                                                                                                                                                                                                                    Iteration 1:     study on R2R [6] val unseen. See §4.4 for more details.

                          . . task. Feature Consistency AlignmentPrompt
   LLM towards a downstream
   a multimodal large language model with exceptional region un-Arrows: [16]
                                                           Prompt   Generation
   sual grounding capabilities. It can take user-defined region inputs
                                                                                  (Sec. 3)                    (FCA) Learningand (Sec.Task
                                                                                                                                      6 & 7) Semantic Enrichmen
                                                                                                                                                         Markers: [5]                                    Arrows: [2]

                                                                                                                                                                                                     Figure 4: Different types of marks can be
                                                                                                                                                                                                                                            # used
                                                                                                                                                                                                                                                     Arrows: [1]

                                                                                                                                                                                                                                                    in our BEV
                                                                                                                                                                                                                                               Perspective Set-of-Mark.
                                                                                                                                                                                                                                                                Fusion Refinement
                                                                                                                                                                                                                                                                                                                 R2R val unseen
                                                                                                                                                                                                                                                                                  SPICE " Bleu-1 " Bleu-4 " CIDEr " Meteor " Rouge "

                       Figure 1 | Prompting with Iterative Visual Optimization (PIVOT) casts spatial reasoning tasks, such as robotic
   enerate long-form responses that are grounded to visual context.                                                                                                                                                                                1        4                                  0.154     0.625     0.170   0.209   0.198    0.392


   ed visual prompts more   transferable
                       control,
                Text Response
   g Chuofan’s internship at ByteDance.
                                                    and
                                as a VQA problem. This      benefit
                                                        is done            moreanunseen
                                                                by first annotating    image with aMLLMs
                                                                                     Text Response                     to improve
                                                                                                      visual representation of robot
                                                                                                                      Perception           on the same task.
                                                                                                                                          Text Response
                                                                                                                                                              Perception                                        forestText   Response
                                                                                                                                                                                                                       </p> [SEG].
                                                                                                                                                                                                                                                   2
                                                                                                                                                                                                                Answer: It’s a wooden <p> pier </p>3 [SEG], 4
                                                                                                                                                                                                                                                   4        4
                                                                                                                                                                                                                                                                     4
                                                                                                                                                                                                                                                            surrounded
                                                                                                                                                                                                                                                                     4 by the <p> lake </p>Text
                                                                                                                                                                                                                                                                  Perception
                                                                                                                                                                                                                                   A blue <p> sky </p> [SEG] is above
                                                                                                                                                                                                                                                                     4 the pier
                                                                                                                                                                                                                                                                                               0.172
                                                                                                                                                                                                                                                                                            [SEG]
                                                                                                                                                                                                                                                                                               0.180
                                                                                                                                                                                                                                                                                            0.342
                                                                                                                                                                                                                                                                            4 and the <p> mountains
                                                                                                                                                                                                                                                                                                         0.653
                                                                                                                                                                                                                                                                                                  and the0.673
                                                                                                                                                                                                                                                                                                           <p>
                                                                                                                                                                                                                                                                                                       0.224
                                                                                                                                                                                                                                                                                                 Response
                                                                                                                                                                                                                                                                                               0.190 </p>
                                                                                                                                                                                                                                                                                            0.373      0.224[SEG].
                                                                                                                                                                                                                                                                                                         0.683
                                                                                                                                                                                                                                                                                                                   0.184
                                                                                                                                                                                                                                                                                                                   0.217
                                                                                                                                                                                                                                                                                                                   0.442
                                                                                                                                                                                                                                                                                                                   0.238
                                                                                                                                                                                                                                                                                                                   0.453
                                                                                                                                                                                                                                                                                                                           0.281   0.206    0.405



                                                                                                    actions   or  3D  coordinates,    then   querying      a VLM       to  select    the      most         promising           annotated            actions      seen        in   the
                                                                                                                                                              Response                                                                             5        4      Response
                                                                                                                                                                                                                                                                     4                 4       0.192
                                                                                                                                                                                                                                                                                            0.419
                                                                                                                                                                                                                                                                                             Decode      0.676
                                                                                                                                                                                                                                                                                                       0.220       0.242
                                                                                                                                                                                                                                                                                                                   0.455
                                                300-400 masks




   uthors                                                                                                             Response                                                                                                                     6        4        4      4          4     Perception0.230
                                                                                                                                                                                                                                                                                               0.208
                                                                                                                                                                                                                                                                                            0.449        Prior 0.467
                                                                                                                                                                                                                                                                                                        0.699      0.264
                                                                                              LLM                                                                                                    LLM                                                               LLM                     Embedding
                    LLM                                                                             image. The best action is iteratively  LLM refined by fitting a distribution to the selected actions and requerying
                                                                                                                                                              Perception                                                                                       LLM
                                                                                                                                                                                                                                                                                   the
                                                                                                    VLM. This procedure
                                                                                               Region                Perceptionenables us to solve complex tasks that require outputting grounded Universal
                                                                                                                                                                                                     Region 4.3 Qualitativecontinuous                           coordinates                       OMG Decoder



  ation .for
          . . Large-Scale Pre-trained Models
                                                                 Image                                                                                          Module                                                                          Results

                                                                                                                                    plication scenarios like “Prompt as a Se
                                                                                                                       Module                                                     Image                                                       Perception
                    Image
                                       Text                     Encoder                             or
                                                                                               Feature
                                                                                                       robot
                                                                                                           Text
                                                                                                               actions   utilizing  a VLM
                                                                                                                                    Image    without     any   domain-specific  Encoder     training.Feature
                                                                                                                                                                                              Visual Projector
                                                                                                                                                                                                                         Text
                                                                                                                                                                                                                            Text Projector
                                                                                                                                                                                                                                               Module
                   Encoder                                                                    Extractor Instruction                Encoder        Text                                             Extractor Fig.        3 provides qualitative comparisons of Text
                                                                                                                                                                                                                     Instruction                                              BEVInstructor
                                                                                                                                                                                                                                                                               Tokenize           against        the ground
                                 Q/AInstruction
                                                                  Image                        Visual
                                                                                                                                               Instruction                                                          truth on the REVERIE.              BEVInstructor
                                                                                                                                                                                                                                                    Visual
                                                                                                                                                                                                                                                                        Instruction         Image
                                                                                                                                                                                                                                                               Question: <Image>\nshows an Encoder
                                                                                                                                                                                                                                                                                           enhanced capability in

                                                                                                                                    where users can directly request a visua
                    Image                                                                                                                                                         Image              Visual                               Image                Please describe the                         Visual Prompts
                                                                                                                                                                                                                    identifying    scenes and objects
                                                                                                                                                                                                                                                   Promptsrelated     to action views, and explicitly   (Point,incorporates
      Q                                                                                       Prompts                               Image                                                                                                                      <Region> and respond                             Box and Mask)
                                                                                                                                                                                    Pixel-centric Prompts
                                                                                                                                                                                                     Object-centric      OMG-Seg
                                                                                                                                                                                                            puttingthese   elements        into the instructions
                                                                                                                                                                                                                                                               with in   the refinement stage.
                                                                                                                                                                                                                                                                     interleaved

                                                                                      The
                                 (a)                                                            (b)                                  (c)                     Figure 5: Left: some conflicts
                                                                                                                                                                                    Visual(d)causedVisual
                                                                                                                                                                                                       by Tokens     all marks  in the center.  Right: our proposed    mark
                                                                                                    © 2024 Google DeepMind. All rights reserved                                            Tokens                                     segmentation masks.
                                    Engineering                       Segmentation                          Detection                                    allocation algorithm to address the conflicts.

  LLMs           mainly            follows              methods for large                           models
                                                                                                                                                                                                                                                              Image
                                                                                                    ⇤ Equal contribution, ordering randomly decided. † Work done while a student researcher at Google DeepMind.

        The    cub                    VLM                                              ear(a) MLLMs             with VLM            certain             taskincluding
                                                                                                                                                                    for their local models from
                                                400-500 masks




                                                                                                                                                                                  Figure 3: The Overview4.4of OMG-LLaVA.
                                                                                                                                                                                                               Diagnostic OMG-LLaVA consists of OMG-Seg and LLM. OMG-Seg tokenizes
        Figure     2: Summary         of Current MLLM Architectures:                                                  only image-level           capability,                                                 the (line
                                                                                                                                                                                    them in an ascending order    image
                                                                                                                                                                                                                          Experiment
                                                                                                                                                                                                                       6). into
                                                                                                                                                                                                                            Thispixel-centric
                                                                                                                                                                                                                                  strategy ensuresvisual   tokens,regions
                                                                                                                                                                                                                                                     that smaller    the detected    objects,before
                                                                                                                                                                                                                                                                             are considered     and inputs visual prompts into object-centric


    [49],
      on the CLIP            [44]).
                             Figure 1: Fine-tuning                         for  of a   downstream
                                                                                                                                                                                    large regions. To furthervisual
                                                                                                                                                                                                               avoidtokens.     Additionally,
                                                                                                                                                                                                                      the potential   overlaps, the
                                                                                                                                                                                                                                                 for [SEG]     token
                                                                                                                                                                                                                                                         themask,
                                                                                                                                                                                                                                                       k-th         weoutput
                                                                                                                                                                                                                                                                        excludebytheLLM   ismodules
                                                                                                                                                                                                                                                                                      region  decoded  by OMG-Seg
                                                                                                                                                                                                                                                                                               that is of            into segmentation masks. a
        [64,   65,
               right63,  58],   etc.,  (b)   MLLMs         with    object-level      capability,      including      [115,    77],   (c)  MLLMs         with    pixel-level                                                               To assess            eﬃcacy     of essential                    BEVInstructor,        we conduct


        capability, includingprompting
                                             Taxonomy flow chart
                                     [44, 78],       etc., (d)
                                              including          MLLMs
                                                              prompt
                                                                                    visual
                                                                          generation,
                                                                                       eye
                                                                              with bothvisual
                                                                                              prompting techniques. We
                                                                                             object-level
                                                                                                      prompting, and pixel-level    with
                                                                                                                        perceptioncapabilities
                                                                                                                                                  a guarantee
                                                                                                                                           illustrate
                                                                                                                                          and reasoning,
                                                                                                                                                          in order of four
                                                                                                                                                          but with        veryoflearning,
                                                                                                                                                                 andaprompt
                                                                                                                                                                                     the ofmodel
                                                                                                                                                                                   stages     visual confident
                                                                                                                                                                                    covered by any k 1 masks

                                                                                                                                                                                    is maximal. In practice,In
                                                                                                                                                                                              where
                                                                                                                                                                                                                  (line 8). remains
                                                                                                                                                                                                             OMG-Seg
                                                                                                                                                                                                              however,   a
                                                                                                                                                                                                                             The resulting
                                                                                                                                                                                    which helps to find the location inside the mask series
                                                                                                                                                                                                                             region  may
                                                                                                                                                                                                                                           mask
                                                                                                                                                                                                                                       frozen
                                                                                                                                                                                                                                          Overall
                                                                                                                                                                                                                                          be so
                                                                                                                                                                                                                                                   is then
                                                                                                                                                                                                                                              at all
                                                                                                                                                                                                                                          where the
                                                                                                                                                                                                                                                 small
                                                                                                                                                                                                                                                            fed to a distance transform algorithm,
                                                                                                                                                                                                                                                       stages.
                                                                                                                                                                                                                                                  of detailed
                                                                                                                                                                                                                                                        Design.
                                                                                                                                                                                                                                                         that the
                                                                                                                                                                                                                                                                    ablation
                                                                                                                                                                                                                                                       minimal distance
                                                                                                                                                                                                                                                                     We
                                                                                                                                                                                                                                                                   mark   first
                                                                                                                                                                                                                                                                         could
                                                                                                                                                                                                                                                                                studies
                                                                                                                                                                                                                                                                            to all
                                                                                                                                                                                                                                                                                study
                                                                                                                                                                                                                                                                                cover
                                                                                                                                                                                                                                                                                          on points
                                                                                                                                                                                                                                                                                   boundary
                                                                                                                                                                                                                                                                                         the
                                                                                                                                                                                                                                                                                       the
                                                                                                                                                                                                                                                                                                val unseen split of R2R [6].
                                                                                                                                                                                                                                                                                               eﬃcacy
                                                                                                                                                                                                                                                                                            (almost)    of the core
                                                                                                                                                                                                                 this paper, we focus on addressing all the challenges above in a more simple yet elegant way. Our   components   of  BEVIn-

 ghtforward                 but       costly            inOMG-LLaVA’s
                                                               computation               eachand            stor-possesses
                                                                                                                                                                                    whole region. In this case, we move the marks off       the region slightly.    We find  that GPT-4V     can still the impact of fine-tuning MLLMs.
                                                                                                                                                                                                             OMG-LLaVA unifiesstructor     image-level     in(such
                                                                                                                                                                                                                                                                Table as 4.  Row
                                                                                                                                                                                                                                                                         image       #1 illustrates
                                                                                                                                                                                                                                                                                   caption   and image-based conversation), object-level
        complex system,      the such    asarrows
                                              [77], (e)          the directionarchitecture,
                                                                                      nose               which
                                                                                                           ear                     an elegant
                                                                                                                                            flow. andWe simple
                                                                                                                                                            explaindesign
                                                                                                                                                                                    build a decent association between the marks andThis   regions.


    andom
        while having images                           from         andour            Computer                             Vision                  Figures                     dataset.
                                                                                                                                                                                 MLLMs (SectionWe curate
                                                                                                                                                                                                                                                 shows competitive performance, demonstrating its potential by elevating
                                                                                                                                                                                                             (such as region caption and visual prompt-based conversation), and pixel-level (such as universal
                                  solid                 show                         of           component’s          information                                       in detail various visual
                                           .  .  .
                                                                                                                                                                                    Once we determine the segmentation,
                                                                                                                                                                                                            mark type and locationslanguage     capabilities.
                                                                                                                                                                                                                                    forsegmentation,
                                                                                                                                                                                                                            referring   all regions,  we overlayRow   #2mkand     #3 indicate
                                                                                                                                                                                                                                                                  marksegmentation,
                                                                                                                                                                                                                                                          reasoning         to region           that the
                                                                                                                                                                                                                                                                                       rkand grounded    integrationgeneration)
                                                                                                                                                                                                                                                                                                       conversation  of BEV fea-
                           image-level,         object-level,             pixel-level     capabilities.
                                                                                                                                    3.      Methods
                                                                                                                                                                                    at location ck . We make sure that each mark istures
                                                                                                                                                                                                                                    uniquealongside
                                                                                                                                                                                                                                             so that the full set M = {m            } are notable performance improvements

     ter-efficient2).fine-tuning                              (PEFT)              methods,                 eye
                                                                                                            such
                                                                                                                                                                                                                                                                           1 , ...mkyields
                                                                                                                                                                                                            visualbyunderstanding    and reasoning perspective          features
                                                                                                                                                                                                                                                         tasks into token-to-token        generation. The framework follows
                             prompt     generation         techniques       (Section
                                                                                   of  a 3),
                                                                                          bearand    how      these  generated        prompts       are   used   to   prompt        distinguishable and speakable    LLMs.
                                                                                                                                                                                                                                    6.1% on
                                                                                                                                                                                                             a simple and elegantbysystem    CIDEr.
                                                                                                                                                                                                                                          design,   From row
                                                                                                                                                                                                                                                  including   #3one
                                                                                                                                                                                                                                                            only andvisual
                                                                                                                                                                                                                                                                     #4, compared   with
                                                                                                                                                                                                                                                                           perception    simplyand
                                                                                                                                                                                                                                                                                      module    concatenating
                                                                                                                                                                                                                                                                                                   one large


m[18],  Computer                   5). Vision                  academic                        papers.                   During                    training,                    we       randomly           sam
                                                                                                                                                                                                             language model. features, fusing BEV and perspective features through the transformer module
                                  Then we discuss the advanced perception and nose                        reasoning abilities achieved through visual prompting (Section 4          2.4 Interleaved Prompt
                                                >500 masks




                                                                                                                                                                                                                                         results in a greater performance improvement by 1.0% on SPICE. Comparisons

                 LoRA        and[20],
        image-level understanding
                                        Finally,and   model
                                                      as
                                                           prompt
                                                          LLaVA,
                                                                pre-training, tuning
                                                                         including
                                                                                   fine-tuning,
                                                                                         caption
                                                                                                [24,    and
                                                                                                              38],
                                                                                                       instruction      tuning,
                                                                                                                conversation,
                                                                                                                                    and in-context
                                                                                                                                       where      most
                                                                                                                                                           learning further
                                                                                                                                                            MLLMs          for
                                                                                                                                                                                   update   previous
                                                                                                                                                                                                             Unified View of Different Tasks. We model various tasks as the token-to-token generation to
                                                                                                                                                                                    Thus far we have obtained a new image I m withbetween
                                                                                                                                                                                    region-mark pairs {hr1 ,bridge
                                                                                                                                                                                                             m1 i, ...,the
                                                                                                                                                                                                                        hrK ,gap
                                                                                                                                                                                                                              mK between
                                                                                                                                                                                                                                                  row #3
                                                                                                                                                                                                                                         overlaid marks.
                                                                                                                                                                                                                                            image-level,
                                                                                                                                                                                                                                  i}. Given the
                                                                                                                                                                                                                                                            and #5, aswewell
                                                                                                                                                                                                                                                         Additionally,
                                                                                                                                                                                                                                                            object-level,
                                                                                                                                                                                                                                                additional cues
                                                                                                                                                                                                                                                                            haveasa set
                                                                                                                                                                                                                                                                             and
                                                                                                                                                                                                                                                                in I m , we can
                                                                                                                                                                                                                                                                                    rowof#4
                                                                                                                                                                                                                                                                                          K and #6, underscore the eﬃcacy of the
                                                                                                                                                                                                                                                                                usepixel-level
                                                                                                                                                                                                                                                                                     either a  understanding and reasoning. To

                                                                                                                                    Visual             prompting                  offers an effective me
                                                                                                                                                                                                             supportones these   tasks,LMMs:
                                                                                                                                                                                                                                        we define three types of tokens: text tokens Tt , pixel-centric visual tokens Tpv ,

yedadditional                         parsing.
                                                                                                                                                                                    plain text prompt or interleaved         to prompt
                             model components, which are illustrated by the dashed arrows (Section                                          6 and 7).
          to zero-shot
                easelose    these          challenges.           VLMsSome                   recent      also ad-
                                                                                                                                                                                                             and object-centric visual tokens Tov . Text tokens encode textual information. Pixel-centric visual

We      grounding
       cast                      such
                                 inferenceability.       In addition,
                                                       with                  OMG-LLaVA
                                                                               as a Q/A           problem,      supports
                                                                                                                     eachthe         visual prompts
                                                                                                                                requiring            specific   as inputs,          • Plain Text Prompt. We tokens  represent
                                                                                                                                                                                                               can use
                                                                                                                                                                                      marks/regions in the image.
                                                                                                                                                                                                                       plain textdense
                                                                                                                                                                                                            Object-centric
                                                                                                                                                                                                                                  prompts
                                                                                                                                                                                                                  As shown invisual
                                                                                                                                                                                                                                          image   features,
                                                                                                                                                                                                                                            as usual
                                                                                                                                                                                                                                Fig. 1,tokens
                                                                                                                                                                                                                                        even without
                                                                                                                                                                                                                                                             providing
                                                                                                                                                                                                                                                     without any
                                                                                                                                                                                                                                                     anythe
                                                                                                                                                                                                                                                encode   special
                                                                                                                                                                                                                                                                           the LLMto with
                                                                                                                                                                                                                                                                 explicit reference
                                                                                                                                                                                                                                                                 textualof
                                                                                                                                                                                                                                                             features    prompt,
                                                                                                                                                                                                                                                                                      the comprehensive image information.
                                                                                                                                                                                                                                                                                 GPT-4V
                                                                                                                                                                                                                                                                            specified objects, offering the LLM object-centric

ks      which results SAM
    ionalsoand focus
                  A is
                              in object
                                 on model    leveland
                                        efficient      understanding,
                                                               modality
                                                           lacks               such as visual
                                                                     comprehensive    bridging studies  prompt-based
                                                                                                               and
                                                                                                              on       various      language
                                                                                                                               conversation
                                                                                                                                     forms,          andas
                                                                                                                                                  such       models,
                                                                                                                                                            region-level
                                                                                                                                                                bounding boxes,   suchmarkers,
                                                                                                                                                                                            as CLIP [44], to
                                                                                                                                                                                      can automatically ground itself in the regions and corresponding marks. It can be used in a wide
                                                                                                                                                                                                            information,    and  can   be  easily  decoded
                                                                                                                                                                                      range of scenarios where users do not have specific regions of interest.
                                                                                                                                                                                                                                                              into segmentation     masks.

                       WeAnswer             (aimagesset with
                                                          of   possible   masksanswers).               Left:      text     prompt           engineering                                                    Then,Weall
                                                                                                                                                                                                                    canthe
                                                                                                                                                                                                                         usetasks   can be unified   as: the marks into the text directly.
        captions.      Figure achieve
                                2: Example all     these    abilities
                                                               overlaid using      one
                                                                                  from    LLM,
                                                                                        our  newly one         encoder,
                                                                                                       introduced   dataset,and
                                                                                                                              SA-1B.one    decoder.
                                                                                                                                         SA-1B     contains 11M diverse,
                                                                                                                                                                                    • Interleaved Text Prompt.               interleaved ones by injecting

                             diverse visuallicensed,prompting            methods.         Inandthis     paper,         pixel-level  tasks   masks.without
                                                                                                                                           prompts,         and         resorting
                                                                                                                                                                    softwere
                                                                                                                                                                           prompts. They     to pro-
                                                                                                                                                                                                 fine-tuning. I
                                                                                                                                                                                      Since the marks are interpretable to LMMs, we can seamlessly      blendout
                                                                                                                                                                                                                                                              them into the original text
                                                                                                                                                                                                                                                   Ttout , Tov                 in    in
                                                                                                                                                                                                                                                                                        , Ttin )                                                    (1)
    iacanIn
         routing          and        skipping                with         adapters              [40,          57].
                                                                                                                                                                                                                                                                 = LLM (Tpv       , Tov
             be   interpreted             as      follows         in andour     framework:                  The      image          is   the    aquestion,
                                                                                                                                                                                      prompt to make a symbolic reference.
                       high-resolution,                  and privacy protecting     images         1.1B    high-quality   segmentation                 These   masks
             particular,    wetopresent
                       annotated    better
                                   fully         encode
                                                the
                                         automatically        the
                                                               SAM,visual
                                                      firstbycomprehensive  as wesegmentation
                                                                                      survey
                                                                                   verify by humanon visualoutputs,
                                                                                                        ratings          we additional
                                                                                                                       vide
                                                                                                                 and numerous   propose
                                                                                                                                  experiments,      perception
                                                                                                                                                  information
                                                                                                                                                   are of high quality  prior
                                                                                                                                                                       to  enhance the models’
                                                                                                                                                                          and                                Fortwo
                                                                                                                                                                                    Examples of applying these    example,     in the
                                                                                                                                                                                                                     types of text    classic
                                                                                                                                                                                                                                   prompts      image-level
                                                                                                                                                                                                                                            based              understanding
                                                                                                                                                                                                                                                   on SoM are demonstrated       task,
                                                                                                                                                                                                                                                                            in Fig.      i.e., image caption, a text response Tt
                                                                                                                                                                                                                                                                                    6. Note
                                                                                                                                                                                                                                                                                                                                                    out



                                                                                                                                    tend       perthe       application                 of VPim-to MLLMs     is use
                                                                                                                                                                                                                generated    based   on text   instruction   Ttin and  image   features Tpv      . In the object-level understanding
                                                                                                                                                                                                                                                                                              in

     areembedding
           engineered            into     prompts.              Middle:   masks visual         prompt            engineering               forwhich
                                                                                                                                                  referring
                                                                                                                                                                                    that for each question, we      a new chat  window   to avoid  context leakage during the conversation.

  ey     are     inherently
                          module
                       diversity.  We to
                             prompting    model-specific
                                           absorb
                                       group    imagesthe
                                                 in MLLMs      object
                                                          by number       queries
                                                                     toofaddress and
                                                                                  per into
                                                                                           require
                                                                                      imageobject-centric
                                                                                       these  for  visualization
                                                                                                 gaps       and ac-   visual
                                                                                                                   (there  are tokens,
                                                                                                                       visual    100   masks
                                                                                                                                  perception        image are
                                                                                                                                                            on the
                                                                                                                                                     capabilities.    inputs
                                                                                                                                                                average).           In real-world scenarios, the above two text
                                                                                                                                                                           By manipulating
                                                                                                                                                                                    round conversations with GPT-4V toin
                                                                                                                                                                                                             features   T
                                                                                                                                                                                    also opt to draw the marks by themselves ,
                                                                                                                                                                                                                               ⇠ prompting
                                                                                                                                                                                                             task, regionsignificantly
                                                                                                                                                                                                                              captioning,
                                                                                                                                                                                                                               and
                                                                                                                                                                                                                                             strategies can be combined
                                                                                                                                                                                                                                             the text response T     out and used  in
                                                                                                                                                                                                                                                                          is generated
                                                                                                                                                                                                                                        enrich human-AI interaction.t Moreover, users
                                                                                                                                                                                                                                    specified   object-centric   visual tokens    T
                                                                                                                                                                                                                                or revise the marks generated using the toolbox. ov
                                                                                                                                                                                                                                                                                    in
                                                                                                                                                                                                                                                                                      multi-
                                                                                                                                                                                                                                                                                       .
                                                                                                                                                                                                                                                                                         can
                                                                                                                                                                                                                                                                                            based on text instruction Ttin , image
                                                                                                                                                                                                                                                                                          The   pixel-level reasoning task, referring
        of   LLMs.      We      present       a   unified     instruction        formation          strategy,      which       lets    the   model        accept      visual
                                                                                                                                                                                                                          pv

    he referring expression,                         and the        availableofanswers                    are the ages  box and  proposals,
                                                                                                                                    potential           which
                                                                                                                                                            for      enhancingtechniques,performance          acr
    uter          Vision                  Figures
                             extend the current
                                                                       (Figures)
                                                             understanding               visual prompt
                                                                                                           dataset                   consists
                                                                                                                                        videos with
                                                                                                                                                                    of
                                                                                                                                                              different
                                                                                                                                                                                                   images
                                                                                                                                                                                              visual
                                                                                                                                                                                                                t
                                                                                                                                                                                                             segmentation, involves generating object-centric visual tokens Tov
                                                                                                                                                                                                                                                                             out
                                                                                                                                                                                                                                                                                 based on text instruction Ttin

  inner images,
    l and
                structure
              text
                     texts,generation,
                     prompt
                                       of
                               and visual
                                    engineering
                                                models,
                                                    prompts
                                                 multimodal      as
                                                               for
                                                                      diverging
                                                                      inputs
                                                                      keypoint
                                                                     prompting,  and          from
                                                                                        generate
                                                                                        matching.
                                                                                        perception       the   our
                                                                                                                response
                                                                                                            andFor keypoint    of  text,
                                                                                                                       prompts improve      segmentation
                                                                                                                                           localization,
                                                                                                                                                                     tokens, 88,
                                                                                                                                                       model performance in complex     645                  and image features T5pv
                                                                                                                                                                                                                                  in
                                                                                                                                                                                                                                     . Additionally, OMG-LLaVA can support various mixed-level tasks, such as
                                                                                                                                                                                                             providing grounded descriptions around specified objects.


 mizing segmentation masks, and labels. Following the LLaVA4017
                  athesingle           setexperiments
                                                 of     parameters                  to    adapt    [64], we adopt pretraining
                                                                                                           mul-                     els. Althoughand    instruct          existing
                                                                                                                                                                      tuning               methods can enh   Pixel-centric visual tokens can be obtained by tokenizing images using a CLIP backbone as the


ure           of       our            visual
                             reasoning,       isand     prompt
                                                                prompts.
                                                                     learning.       Wetextillustrate
                                                                                                     The     the
                                                                                                                      dataset
                                                                                                                       understanding        andand  was reasoning
                                                                                                                                                                     collected
                                                                                                                                                                          tasks.
                                                                                                                                                                                                   from      Arx
                                                                                                                                                                                                             tokenizer. However, object-centric visual tokens require encoding object information to be easily
    s, where
        pipelines.        question
                         Extensive                  a keypoint    show   intheplain
                                                                                  effectiveness   and      oftheourpossible
                                                                                                                      components     answers            are
                                                                                                                                                    training   allstrategy.                                  decoded into segmentation masks. Therefore, methods like mask pooling in Osprey [115] and ROI


     inInaaddition        totaxonomy
              resource-friendly                of our survey
                               visual segmentation,                  in Figure 1 and
                                                          and OMG-LLaVA
                                                                    flexible                  summarize
                                                                                        manner.
                                                                                            can    also achieve good enough         mance              throughonprompt
                                                                                                                                                  performance                 6             training,    these tra
                                                                                                                                                                                                             pooling in GLaMM [77] fail to meet these requirements. We found that a universal perception decoder
                                                                                                                                                                                                             can meet all the requirements. Thus, we chose the OMG-Seg decoder [52] as the object-centric


  revelopments
       scholarly                        articles                      from              a     variety                  2.1
                                                                                                                          of         academic
                                                                                                                                 Bounding-Box
                                                                                                                                                                          fields.
                                                                                                                                                                            applied toArxiv                sourd
                                                                                                                                                                                                             tokenizer due to its comprehensive capabilities.
                             our contributions             as follows:
        datasets, including            COCO           panoptic      segmentation,           VIPSeg          video panoptic          fall      short when
                                                                                                                                      segmentation,            refCOCO,                         other models 3.2 OMG-LLaVA Framework
        refCOCO+, refCOCOg       in     visual referring   prompting
                                                              expression              [3],
                                                                                 segmentation,    inspiredGranDf       grounded
                                                                                                                       Bounding         conversation
                                                                                                                                         boxes      are   usedgeneration,
                                                                                                                                                                  to demarcate objects or re-
    ad      starting
        and refCOCOg •region
                                        from
                                    We provide captionadatasets.
                                                              comprehensive
                                                                                    We            downloaded
                                                                                        categorization                              tothefeature  all
                                                                                                                                                   image,papercorruption.
                                                                                                                                                                   MLLMMLLMsTo
                                                                                                                                                                                   sources             from
                                                                                                                                                                                               this end,    we in
                                                                                                                                                                                                             The framework of OMG-LLaVA is shown in Fig. 2 (e). OMG-LLaVA comprises a large language


    almatches
    st    reprogramming
        design     in athe          of
                          more elegant   |A|)[14,
                                          visual   way
                                                             2010.
                                                              51],
                                                       prompting
                                                     andforthe  thegoal   and
                                                                             We hope
                                                                          offer
                                                                              is to amatch
                                                                      community. prompt
                                                                                            our research cangions
                                                                                            promising
                                                                                              generation
                                                                                                       the two. visual
                                                                                                                          inspirewithin
                                                                                                                         We express
                                                                                                                                              research
                                                                                                                                              an
                                                                                                                                                  the
                                                                                                                                                              on
                                                                                                                                                               enabling
                                                                                                                                                          latter
                                                                                                                                                                                          to extract            2
                                                                                                                                                                                                             model (LLM) and a frozen universal perception module. The universal perception module encodes
                                                                                                                                                                                                             images and visual prompts from users into pixel-centric and object-centric visual tokens. It obtains
                                                                                                                                                                                                             object-centric visual tokens output by the LLM into explicit segmentation mask responses. The LLM
                                                                                                                                    of
                                                                                                                                   featuresTransferable
                                                                                                                                                  (Lin et al., 2024a).      Visual ThesePrompting
                                                                                                                                                                                           features        (TVP)
                                                                                                                                                                                                             accepts text instruction tokens and pixel-centric and object-centric visual tokens from the universal


 uter-Vision
    model adaptationaspartition
                                    methods in MLLMs.
                                             by predicting
                                                      introducing     the“cs.CV”
                                                                              square
                                                                                   learnable permutation      sources,
                                                                                                             per-       matrix
                                                                                                                       help             ⇧ as
                                                                                                                                the model
                                                                                                                                    the                they
                                                                                                                                              2 understand
                                                                                                                                                    Sm
                                                                                                                                              transferability
                                                                                                                                                             that the     contain
                                                                                                                                                                             image content and
                                                                                                                                                                                  oftext,
                                                                                                                                                                                       visual    images        th
                                                                                                                                                                                                             perception module as inputs and then outputs text responses along with object-centric visual tokens.
                                                                                                                                                                                                             The detailed architecture of OMG-LLaVA is illustrated in Fig. 3. The universal perception module

                                                                                                                                                                                                   prompts acro
        2
    proach      Related
                 for
      the pixel space   vi-     Work
                                 • Weassociates
                                           explain the each
                                        ofMLLM’s
                                               images.inAsFigure          name
                                                                integration
                                                                            theand        to
                                                                                   ofqvisual
                                                                                     pixel     its    corresponding
                                                                                                   prompts
                                                                                                  space                correlatelocation
                                                                                                                  is enhancing          it with the    a   (i.e.,
                                                                                                                                                            corresponding                   thereby
ucture,                  as         shown                                                          3.           To         remove           In thisunrelated                                source         imapr
                                                                                                                                                                                                                                                                                   5


    ng the desired                  into ⇧qa = 1). perception                            reasoning           for                          fine-grained        section,
                                                                                                                                                               and grounded       weimagewill    first briefly
                                                                                                                                                                                              under-
 main          for
        Multimodal    different
                              Large more      models,
                                         Language
                                                controllable       it
                                                             Models.     becomes
                                                                             Early multimodal
                                                                      compositional            a     natural
                                                                                               reasoning,   modelsstanding.
                                                                                                                         [47] explore     Previous         work, strate-
                                                                                                                                               better fusion           such as Shikra (Chen
ally
 y meansgies,tagged
    arameter
      arrow,
                   over-
                 various feature
                  which tuning.     which2000   In order
                                          extractors,
                                                 helps toand
                                              Many
                                         associating
                                                               images
                                                                  todifferent
                                                               follow-up
                                                               prevent
                                                                  name
                                                                                           and
                                                                       predictmeta-architectures.
                                                                                      ⇧, we use Eq. (1)
                                                                                        works
                                                                             hallucination
                                                                               q to location
                                                                                                    and have  trained
                                                                                                            lan-      Most
                                                                                                           a aslanguage
                                                                                                                           to define
                                                                                                                       et al.,works
                                                                                                                                  2023b) a
                                                                                                                                    inaries     binary
                                                                                                                                               the
                                                                                                                                            focus
                                                                                                                                                and
                                                                                                                                                       about
                                                                                                                                                       cost
                                                                                                                                                       on       of tasks,
                                                                                                                                                            single
                                                                                                                                                        VTPrompt
                                                                                                                                                        where
                                                                                                                                                                           image
                                                                                                                                                                       MLLMs               andclassifier
                                                                                                                                                                            (Jiang et al., 2024),
                                                                                                                                                                                                   VP, then form
        such as caption and              VQA.    biasWith       the   development           of the large            Cquantize
                                                                                                                        qa = models of
                                                                                                                                     s(i   atransferring
                                                                                                                                              , t[5,
                                                                                                                                        bounding  q ) 83,boxes36],torecent  visualkeyprompts
                                                                                                                                                                         represent           objects    across M
 ages
pics        like
        works     in a •figure-like
                  [46,performance
        modal benchmarks
                         2,    82,
                                    guage
                                    64,
                                    We
                                          15]
                                                         issues.
                                                        refinement
                                                    mainly
                                         ia is obtained either
                                       [35,summarize
                                                               explore
                                                67, 56, 28].MLLM
                                                                           structurevia croppingwith
                                                                                    [56]
                                                                             building
                                                                    LLaVAalignment
                                                                                           an   and          data
                                                                                                 instruction-tuning
                                                                                 [64, 63, 62,methods
                                                                                                                 or marking
                                                                                                     96, 124] is one earlier
                                                                                                                               atintroduce
                                                                                                                                 pipeline
                                                                                                                       numerically,      least
                                                                                                                                         and      tq is one
                                                                                                                                                 for
                                                                                                                                              modeling multiple
                                                                                                                                           work that treats
                                                                                                                                                             just
                                                                                                                                                               our          natural
                                                                                                                                                                       multi-
                                                                                                                                                               both input
                                                                                                                                                                       visual
                                                                                                                                                                                 and output posi-
                                                                                                                                                                          proposed            TVP image.
                                                                                                                                                                                                       approachW
  nge,
 on        it
        [22,   is  inter-
                  28],       butto    none
                                         the that,   has
                                                   name       studied
                                                              of the             the
                                                                           keypoints      generaliza-
                                                                                                prefixed  visual by cuesthe
                                                                                                                       tions.    string “an
                                                                                                                                  Other      approaches image   modify       bounding     boxes   for
 ntire  features
   m cropping,
        LLaVA.
 al prompts
                  data
                     as tokens.
                      On   athe
                           across
                                      After
                                    with
                                  other
                                            keep
                                         of”.
                                              visual prompts,
                                            hand,
                                              models,
                                    and in-context
                                                     For        only
                                                          several
                                                             this
                                                        several    or
                                                                      works
                                                                         covering
                                                                      problem,
                                                                    works
                                                               learning,  their
                                                                                  the
                                                                                 [115]
                                                                               [118,
                                                                                        model
                                                                                        the
                                                                                        116,
                                                                                              most
                                                                                           explore  training
                                                                                                 role
                                                                                                 78,
                                                                                       transferabil-
                                                                               addressing
                                                                                                           of
                                                                                                         120,
                                                                                                  issues of
                                                                                                                   informative
                                                                                                                 questions
                                                                                                                 22,   23,
                                                                                                                            to enhance
                                                                                                                       specific
                                                                                                                             59,
                                                                                                                                    our
                                                                                                                                      tasks:
                                                                                                                                     and
                                                                                                                                    119,
                                                                                                                                                the visual
                                                                                                                                               method
                                                                                                                                                 A3VLM
                                                                                                                                               answers
                                                                                                                                             75,   34,    44]
                                                                                                                                                                source
                                                                                                                                                                 inputs
                                                                                                                                                                 is
                                                                                                                                                                add
                                                                                                                                                                   is extra
                                                                                                                                                                (Huang
                                                                                                                                                                             of
                                                                                                                                                                         depicted       images,  Fig. 2. comi
                                                                                                                                                                                            in uses
                                                                                                                                                                               et al., 2024a)

 extual randomly
    ormation
        components
  d inparticular,
                     con-to adapt
            adversarial
             informa-
                                          partitioned
                                           LLaVA for visual
                                         symmetric
                                    misinterpretation,
                        several works  attacks
                                         tation
                                                 explore[10,
                                                       matrix
                                                                 andand we
                                                                       68].proposing
                                                              language-driven
                                                                      ⇧    via
                                                                                    90%
                                                                           grounding,
                                                                                 decode
                                                                                  While
                                                                                  optimal
                                                                                                 theof
                                                                                              detection,
                                                                                           strategies
                                                                                         grounding popular
                                                                                                          costforthe
                                                                                                                 segmentation,
                                                                                                                   matrix
                                                                                                                       image,
                                                                                                            and segmentation.
                                                                                                   transport:
                                                                                                                               data
                                                                                                                       3D bounding
                                                                                                                                  C into
                                                                                                                                    3.1.
                                                                                                                                    CityLLaVA   to
                                                                                                                                          andboxesvideo
                                                                                                                                                  a permu-train
                                                                                                                                                          toanalysis.
                                                                                                                                                 Preliminaries
                                                                                                                                            However,    (Duan       et
                                                                                                                                                            these works al., and
                                                                                                                                                              locate actionable
                                                                                                                                                                             In
                                                                                                                                                                              2024)      left
                                                                                                                                                                                      scales       the rest f
                                                                                                                                                                                         parts of an
                                                                                                                                                                                              up the
                                    more        controllable        compositional           reasoning.
 omptt with
marking        tuning
                  works
        instruction     more
                         tuning,
                             2
                                likeandCoOp
                                   Visual
                                             information
        are all trained with a specific purpose. We aim to build the simplest
                                              prompt-driven
                                                   Prompt
                                                            [65, 66],
                                                                  Categorization
                                                                                   VPT
                                                                        segmentation      in       the
                                                                                              in[24]
                                                                                                   one
                                                                                                   X
                                                                                                               and
                                                                                                           model. Supplementary
                                                                                                                       bounding
                                                                                                                       To
                                                                                                                       tends
                                                                                                                             model box,
                                                                                                                             the   best
                                                                                                                                 the
                                                                                                                                         to unify
                                                                                                                                            of
                                                                                                                                    Multimodal
                                                                                                                                       shorter
                                                                                                                                                 and TextCoT
                                                                                                                                                         segmentation,
                                                                                                                                                knowledge,
                                                                                                                                                    sides    of  the we    Material.
                                                                                                                                                                        (Luan et al., 2024) ex-
                                                                                                                                                                           are
                                                                                                                                                                       Large
                                                                                                                                                                       bounding       Language
                                                                                                                                                                                      box  to match     Models.
     operate soft prompts
     ed  prompt
        the   first   en-
                     model      to  achieve     ⇧(i,for
                                                 ˆ  this   goal.
                                                          Q, A) both         modalities at the
                                                                       = argmax                                  ⇧qathe   exp longer
                                                                                                                                  ( ⌧side,          ) , (2)it encompasses the entire
                                                                                                                                            Cqaensuring
        Unified             Visual prompts
                     Segmentation              Models. are essential        tools   inmMLLMs,             guid-24, 71,region        use
                                                                                                                                    of    led an
                                                                                                                                         interest.     architecture interestCRGthat
                                                                                                                                                         In addition,                  (Wan projects
                                                                                                                                                                                               et al.,    visual
 of the         model,           even          at     the     embedding
                                                              The vision                  space,
                                                                                 transformers
                                                                               ⇧2S
                                                                                             q2Q,a2A    [9, they          84] have              to research
        in universal
     a red                   ing models in Recent
               circle issegmentation.                  interpretingworksand   [85,processing
                                                                                     17, 112, 50,       visual
                                                                                                            19, 106,2024) 104, 66,  embedding
                                                                                                                                  masks  81,out113,  specific
                                                                                                                                                        111, 127, space
                                                                                                                                                                   regions       to integrate
                                                                                                                                                                          101,with     black pixels images wit

 eriments and Results
   nder 48, complete
    re several
              129] havedata.
        outperforming
   sr the
       and      images
             reader
                      dif- previous
                         to      are
                                    black-box
                               developed          mask
                                          accessible
                                         tion
                                                               conditions
                                                           classification
                                      These prompts (Wu et al., 2024f) can take
                                         where           ⌧ > 0models
                                                  specialized
                                                     problem
                                                                        is a temperature
                                                                      for
                                                                      is       input.
                                                                           solved
                                                                                          where
                                                                                 architectures

                                                                                          efficiently
                                                                                                        withonly
                                                                                   [11, 41, 32, 51,parameter.
        segmentation tasks [40, 55, 53]. In particular, several works [52, 37, 101, 102, 29, 1] adopt one model
                                                                                                                 an

                                                                                                                  via
                                                                                                                     end-to-end

                                                                                                                         the
                                                                                                                                        set
                                                                                                                                     in both
                                                                                                                                              prediction

                                                                                                                                 Sinkhorn-Knopp
                                                                                                                                                   image
                                                                                                                                                                approach,
                                                                                                                       to reduce priors, providing a way to correct predic-
                                                                                                                30, 54, 128] This           Tooptimiza-
                                                                                                                                                     be specific,
                                                                                                                                                               and video assume that we have a

        with shared parameters                 to perform[43],   various      segmentation           tasks. One         recent C.
                                                                                                                                    an LLM P and a projector h . The te
                                                                                                                                   work, OMG-Seg [52], first
    per,unifies
            we image,
                    investigate          algorithm
                                                 the direct transfer      which        renormalizes
                                                                                             ofsegmentation        matrix
                                                                                                     trained in onean
                                video, open-vocabulary,                   and interactive                                                   MLLM
                                                                                                                                       simple                    given image input X and tex
                                                                                                                                                    model. However,
 visual
   pts to other
        all  of  these  prompting,
                          works          Keypoint
                                MLLMs for adaptation.
                                     focus        on   visual        we pretrain
                                                               Localization.
                                                                  segmentation          and     The
                                                                                                 This re-
                                                                                                lack       second
                                                                                                         the       different
                                                                                                                ability  task
                                                                                                                           to      is
                                                                                                                               generate a   more      models
                                                                                                                                                        useful
                                                                                                                                               interactive
                                                                                                                                    autoregressively
                                                                                                                                                                  text and (see Section 4
                                                                                                                                                                               according to the likelih

## Page 3

tions without additional training. Groma (Ma et al.,     this issue, pixel-level prompts (Ma et al., 2024b)
2024a) and InstructDET (Dang et al., 2023) en-           use individual pixels in images or videos, enhanc-
code user-specified regions (i.e., bounding boxes)       ing the semantic localization capability of MLLMs.
into visual tokens, enhancing the localization abil-     Methods such as FGVP (Yang et al., 2024a),
ity of MLLMs by directly integrating them into           EVP (Liu et al., 2023b), DOrA (Wu et al., 2024e),
user instructions. Another framework (Lin et al.,        and CoLLaVO (Lee et al., 2024) employ pixel-
2024b) further enhances the localization capabili-       level prompts to convey semantic information for
ties of MLLMs by integrating contextual embed-           precise object localization. OMG-LLaVA (Zhang
dings from external knowledge within bounding            et al., 2024e) and VisionLLM (Wang et al., 2024b)
boxes, serving as visual prompts to boost the fine-      tokenize images into pixel-centric visual tokens,
grained cognitive abilities of various MLLMs.            aligning visual tasks with language instructions.
                                                         Techniques such as Image Inpainting (Bar et al.,
2.2   Markers                                            2022) decode visual tokens into pixels, while Con-
Similar to bounding boxes, visual markers are spe-       trolMLLM (Wu et al., 2024d) models rich semantic
cific elements within visual data (such as images        relations between pixels and text prompts. There
or videos) used to highlight, identify, or draw at-      are also coordinate prompt methods, such as SCAF-
tention to particular features or regions. They are      FOLD (Lei et al., 2024a) and AO-Planner (Chen
often employed to indicate particular parts of an        et al., 2024a), which convert input images into co-
image that are relevant to the task. Prior work (Sht-    ordinates using metrics, enhancing spatial under-
edritski et al., 2023) has demonstrated that models      standing and reasoning abilities in MLLMs.
trained on web-scale data can focus on specific
visual markers, such as red circles, to highlight de-    2.4    Soft Visual Prompt
sired regions instead of cropping the image around       Soft visual prompts, learned in the pixel space
them. AutoAD-Zero(Xie et al., 2024) introduced a         and applied directly to the image, allow models
two-stage, training-free approach that incorporates      to adapt more effectively to specific downstream
character information by "circling" characters in        tasks. In particular, TVP (Zhang et al., 2024g),
the frame and color-coding each identity. More re-       BlackVIP (Oh et al., 2023), and VPGTrans (Zhang
cently, Set-of-Mark (SoM) prompting(Yang et al.,         et al., 2024a) add pixel-level prompts to images,
2023) overlays visual markers directly onto im-          either by surrounding the image with universal
ages to help models generate answers grounded            prompts or designing prompts matching the im-
in specific image regions. ViP-LLaVA(Cai et al.,         age’s shape. In Learned Prompt (Rezaei et al.,
2024) expands on this by incorporating arbitrary         2024), WVPrompt (Ren et al., 2024), and ILM-
visual cues like scribbles and arrows, using fine-       VP (Chen et al., 2023a), task-relevant perturbation
tuned models to recognize these markers. Liao            patterns are injected into the pixel space to modify
et al. (2024) also leverage the SoM technique to         the input sample. Additionally, ImageBrush (Yang
introduce feedback, converting it into text or vi-       et al., 2024b) enhances semantic understanding by
sual marks to improve semantic grounding. SoM-           extracting tokenized features from images.
LLaVA (Yan et al., 2024) proposes a method to
enhance SoM’s tag association by listing items           3     Visual Prompt Generation
individually and comprehensively describing all
tagged items within an image. Other methods, such        Different from textual prompts, visual prompts are
as ToL (Fan et al., 2024b) and OWG (Tziafas and          typically position-aware and instance-specific, in-
Kasaei, 2024), link each segment in the frame with       volving particular visual objects, relationships, and
a unique ID, while Pivot (Nasiriany et al., 2024)        contexts. Current approaches use visual prompt
projects a 3D location into image space and draws        generation methods and models to improve the
a visual marker at this projected location to refer to   accuracy and comprehension of visual prompts
spatial concepts in the output space.                    by MLLMs, which generate visual prompts, such
                                                         as segmentation, detection, and image inpainting,
2.3   Pixel-level                                        for individual images and videos. Additionally,
Previous approaches relied on coarse markers like        toolchains of visual prompt methods are employed
colorful boxes or circles, which introduced ambi-        to enable multi-step visual reasoning and planning.
guity in accurately highlighting objects. To address     To create universally applicable visual prompts

## Page 4

learnable pixel values have also been developed.         abilities. OMG-LLaVA (Zhang et al., 2024e) in-
                                                         tegrates multi-level visual prompts that enable
3.1   Prompt Engineering                                 MLLM’s course-to-fine visual perception to more
Understanding human-engineered visual prompts            comprehensive visual understanding. Liu et al.
can be important in practical use cases, where vi-       (2023b) propose to enhance the model’s ability
sual prompts are especially efficient for expressing     to understand and process low-level structural el-
one’s intention or attention to the current visual ev-   ements within images. He et al. (2024) further
idence. Early exploration (Shtedritski et al., 2023)     incorporate such visual prompts into MLLM fine-
discovers that drawing a simple red circle around        tuning to augment the model’s capacity in fine-
an object can direct a model’s attention to that re-     grained visual perception. CoLLaVO (Lee et al.,
gion. In addition, to enrich detailed visual evidence,   2024) proposes a crayon prompting which further
MIVPG (Zhong et al., 2024) leverages instance cor-       augments with panoptic segmentation method with
relations within images or patches.                      image in-painting color maps to better discriminate
   ViP (Cai et al., 2024) introduces a novel multi-      multi-objects within the image.
modal model capable of decoding free-form visual
prompts, allowing users to intuitively mark images       3.3   Object Detection
with natural cues. This approach does not require        Object detection models like SoM (Yang et al.,
complex region encodings and achieves state-of-          2023), RCNN (Girshick, 2015), and Omni3D
the-art performance on region-specific comprehen-        (Brazil et al., 2023) provide precise object identifi-
sion tasks. In addition, ViP-Bench (Cai et al., 2024)    cation and localization in the visual context, which
is also proposed to evaluate MLLM’s perception           assists MLLM’s visual grounding abilities and
of such naturally engineered visual prompts. In          guides MLLM’s attention on semantically meaning-
domain-specific CityLLaVA (Duan et al., 2024)            ful contents. SoM-LLaVA developed by Yan et al.
framework, engineered visual prompts are col-            (2024) uses numeric tags to align visual objects
lected and tailored for urban scenarios, which fur-      with textual descriptions. Object tags enable the
ther augments the fine-tuned MLLM.                       model to list and describe these objects accurately,
                                                         which enhances visual reasoning and visual instruc-
3.2   Visual Segmentation                                tion following capabilities. InstructDET (Dang
Segmentation methods such as OpenSeeD (Zhang             et al., 2023) incorporates generalized instructions
et al., 2023b), SAM (Kirillov et al., 2023), and         into the training process, diversifying object detec-
SegFormer (Xie et al., 2021), are used to delin-         tion by enabling the model to understand and fol-
eate and identify specific regions, objects, or struc-   low various referring instructions. This enhances
tures within images, thus enabling the models to fo-     the model’s flexibility in understanding user in-
cus on relevant visual information more accurately.      tentions and instructions in different task contexts.
With pre-trained segmentation models, external vi-       Wan et al. (2024) propose to improve the grounding
sual knowledge can be transferred and integrated         of vision-language models by contrastive region
into MLLM’s prompt. Yang et al. (2024a) explore          guidance. By guiding the model’s attention to rele-
a fine-grained visual prompting method by pixel-         vant regions, MLLM can more accurately associate
level annotations annotated from image inpainting        visual regions with corresponding textual instruc-
(Bar et al., 2022) method. Lin et al. (2024b) pro-       tions. Cho et al. (2024) extend vision-language
pose an instruction tuning method to directly incor-     models to understand 3D environments, by improv-
porate fine-grained segmentation knowledge in the        ing spatial awareness and the understanding of ob-
spatial embedding map as visual prompts, which           ject interactions in three-dimensional spaces.
enhances the model’s context-awareness of the vi-
sual scene. VAP (Chen et al., 2024a) develops a          3.4   Visual Prompt Toolchain
visual affordance prompting method that grounds          To enable more complex multimodal understand-
visual elements by SAM (Kirillov et al., 2023) in        ing by multi-step or interactive reasoning, several
navigation tasks. DOrA (Wu et al., 2024e) further        methods aggregate various visual prompting meth-
introduces 3D spatial and contextual information         ods as toolchains (Wu et al., 2024f) to be called
to improve 3D visual grounding tasks.                    by the MLLM and assist individual reasoning sub-
   Fine-grained segmentation information also aug-       tasks. Zhou et al. (2024b) propose an image-of-
ments MLLM’s visual perception and reasoning             thought method that can automatically determine

## Page 5

each reasoning step’s visual information extraction      help models adapt to new tasks and domains with-
method and implement it as visual prompts, which         out direct access to model parameters.
prompt MLLM to follow a certain reasoning path
and enable step-by-step multimodal reasoning. Tzi-       4     Visual Perception
afas and Kasaei (2024) focus on adapting vision-
                                                         4.1    Visual Grounding and Referring
language models for open-world grasping tasks
by incorporating a list of visual prompting meth-        Recent visual prompting works have significantly
ods including open-end segmentation and object           improved MLLM’s visual grounding and refer-
grounding to enable open-world grasping tasks. To        ring abilities. Some works emphasize the impor-
enable more transferable and generalizable visual        tance of iterative feedback and multimodal inter-
prompts, Sheng et al. (2024) create a more unified       action to refine semantic grounding, while others
in-context learning method by integrating various        explore object-centric perception and the compre-
contextual visual prompts into a unified represen-       hension of visual relations. To improve MLLM’s
tational space. MineDreamer (Zhou et al., 2024a)         regional grounding and object detection abilities,
further develops a versatile visual prompt genera-       SoM-LLaVA (Yan et al., 2024) employs the Set-of-
tion method for imaginary visual scenes, which are       Mark (SoM) model to tag all the objects in the im-
consistent with current decision-making intention        age and ask the model to list all the items. Instruct-
and visually express the next-step goal.                 DET (Dang et al., 2023) and VTPrompt (Jiang
                                                         et al., 2024) further enable multimodal grounding,
3.5   Learnable and Soft Visual Prompt                   which extracts object entities from the text and
Learnable or soft visual prompts are employed to         these objects’ regional bounding boxes.
adapt the visual encoder in MLLMs, enabling more            With a fine-grained visual grounding encoder,
controlled and versatile use of visual prompts that      several works further use visual cues to guide
are aligned with downstream tasks. Such tech-            MLLM’s attention to relevant regions within im-
niques are used in multimodal instruction tuning         ages and achieve better regional referring abilities.
with visual instructions. Rezaei et al. (2024) inves-    CRG (Wan et al., 2024) uses contrastive regional
tigates how visual prompts can be learned to guide       guidance to direct the model’s attention to specific
the attention mechanisms in ViT. Li et al. (2023a)       areas of interest within an image, without model
fine-tune MLLMs to follow zero-shot demonstra-           finetuning. RelationVLM (Huang et al., 2024c)
tive instructions using learnable visual prompts.        leverages visual prompts to enhance MLLM’s un-
Chen et al. (2023a) focus on better mapping vi-          derstanding and reasoning about objects’ spatial
sual inputs to corresponding labels through learned      relations. Shikra (Chen et al., 2023b) further ap-
prompts. For some specific and domain-oriented           plies to visual dialogue systems, where MLLM
problems, (Ren et al., 2024) develop a learnable         responds to referential cues within a dialogue, en-
visual prompting method as image watermarking            abling more precise and context-aware interactions
to identify the image’s copyright and ownership.         In addition, several works aim to provide a com-
   At the same time, learnable visual prompts can        prehensive framework that incorporates various vi-
also be transferable across MLLMs and down-              sual prompting methods in different granularity
stream tasks. VPGTrans (Zhang et al., 2024a)             levels, to enable more fine-grained and flexible
proposes a transferable visual prompt generator,         multimodal interactions, including free-form vi-
which adapts the pre-trained source MLLM to tar-         sual prompt inputs (Lin et al., 2024a) and feedback
get MLLM with low cost in training data points           mechanisms (Liao et al., 2024) on visual prompts.
and computation. Memory-space visual prompt
(Jie et al., 2024) injects learnable prompts in the      4.2    Multi-image and Video Understanding
key and value layers in the vision-transformer ar-       To improve the models’ understanding of complex
chitecture, which enables efficient vision-language      visual relationships and ensure that they can accu-
fine-tuning. Wu et al. (2023) also injects soft visual   rately reference and describe objects across diverse
tokens as visual compositional operations, which         multi-image inputs, several works propose visual
are learned to better compose multimodal informa-        prompts in multi-image inputs and novel evalua-
tion with few-shot examples. The black-box visual        tion benchmarks to test their effectiveness. Fan
prompting method (Oh et al., 2023) focuses on ro-        et al. (2024c) present a novel benchmark dataset
bust transfer learning, where the visual prompts         with multipanel images to test MLLM’s abilities in

## Page 6

distinguishing objects across panels and navigating     sual planning, reasoning, and action generation.
between different visual elements. Pan et al. (2024)    We examine how visual prompts facilitate complex
leverage morph-token auto-encoding to enhance           step-by-step reasoning, decision-making, and con-
the model’s capacity to process visual grounding        trol over visual generation models, expanding their
across multiple images. Li et al. (2023a) fine-tune     capabilities across diverse tasks. We also review
MLLMs to follow in-context demonstrative instruc-       several frontier applications (Appendix 9), which
tions across multiple images. In addition, AIM          can be under-explored and lack sufficient solutions.
(Gao et al., 2024) proposes to dynamically adapt
its grounding and referring abilities to accommo-       5.1   Visual Planning
date new visual contexts across several images.         Recent works demonstrate that visual prompting
   Several methods are also developed to allow          improves visual planning tasks. Zhou et al. (2024b)
MLLMs to identify specific regions of interest, im-     proposes an Image-of-Thought(IoT) prompting
proving their ability to handle complex and dy-         method that compels MLLMs to automatically de-
namic video content. OmAgent (Zhang et al.,             sign visual and textual steps and leverages external
2024c) develops a visual prompting method to en-        image processing tools to generate a multi-model
able task division in video understanding, by anno-     rationale series, which is used to assist MLLMs
tating a series of visual features. RACCooN (Yoon       with complex visual reasoning tasks through a
et al., 2024) uses visual prompts to guide MLLMs        step-by-step process. OWG (Tziafas and Kasaei,
in identifying the target regions in the video for      2024) combines segmentation and grasp synthe-
manipulation. Wu et al. (2024c) ground objects          sis models, which unlocks the grounded world
across videos, enabling the model to comprehend         understanding through segmentation, grasp plan-
and refer to objects in dynamic scenes.                 ning, and ranking. Zhou et al. (2024a) introduces
                                                        the Chain-of-Imagination (CoI) method and cre-
4.3    3D Visual Understanding                          ates an embodied agent in Minecraft named Mine-
Recent works use visual prompting for better 3D         Dreamer. This method envisions the step-by-step
visual understanding. Li et al. (2024) constructs an    process of executing instructions with the help of
extensive dataset comprising instruction-responses      an LLM-enhanced diffusion model that translates
pairs for 3D scenes and introduces 3DMIT for effi-      imaginations into precise visual prompts to sup-
cient prompt tuning while eliminating the align-        port the accurate generation of the agent’s actions.
ment stage between 3D scenes and languages.             BEVInstructor (Fan et al., 2024a) incorporates
DOrA (Wu et al., 2024e) proposes a novel 3D vi-         Bird’s Eye View representations as visual prompts
sual grounding framework with Order-Aware refer-        into MLLMs for navigation instruction genera-
ring. This method leverages LLM to infer ordered        tion. AO-Planner (Chen et al., 2024a) achieves
object series that used to guide the progressive fea-   affordances-oriented motion planning and action
ture refinement process.                                decision-making with a VAP approach and a high-
   Cho et al. (2024) constructs a large-scale dataset   level PathAgent.
named LV3D and introduces a new MLLM Cube-              5.2   Chain-of-thought
LLM pre-trained on the proposed dataset. Zhang
et al. (2024d) proposes Agent3D-Zero, which in-         To enable more complex image reasoning, recent
troduces novel visual prompts by employing bird’s-      works incorporate visual prompting with Chain-
eye view images and selecting viewpoints to un-         of-Thought methods. Luan et al. (2024) pro-
leash the MLLM’s ability to observe 3D scenes.          poses a novel Chain-of-Thought framework for
3DAP (Liu et al., 2023a) develops a novel visual        text-rich image understanding, named TextCoT.
prompting method that creates a 3D coordinate sys-      This method consists three stages including image
tem a nd additional annotation to empower GPT-4V        overview for global information, coarse localiza-
to complete 3D spatial tasks.                           tion for estimating the section that encompasses the
                                                        answer and fine-grained observation for furnishing
5     Compositional Reasoning                           precise answers. Wu et al. (2024f) proposes Det-
                                                        ToolChain to unlock the potential of MLLMs in
This section discusses how visual prompting en-         object detection task. This method involves using
hances compositional and multimodal learning in         a "detection prompting toolkit," which includes vi-
MLLMs, enabling improvements in tasks like vi-          sual processing and detection reasoning prompts,

## Page 7

combined with a multimodal detection Chain-of-         of urban areas, enhancing interpretability.
Thought method to reason the sequential imple-
mentation of the detection prompts.                    6.2   Fine-tuning
                                                       Zhang et al. (2024g) propose Transferable Vi-
6     Model Training                                   sual Prompting (TVP), a method to improve the
                                                       transferability of soft visual prompts which are
This section presents key approaches to align mul-     a small amount of learnable parameters across
timodal large language models (MLLMs) using vi-        different MLLMs for downstream tasks. Lin
sual prompting techniques, including pre-training,     et al. (2024b) integrate fine-grained external knowl-
fine-tuning, and instruction tuning, which aim to      edge such as OCR and segmentation into multi-
unify multi-modal prompts and improve cross-task       modal MLLMs through visual prompts, which em-
transferability. In addition to model training tech-   bed fine-grained knowledge information directly
niques, we also summarize evaluation datasets (Ap-     into a spatial embedding map. CoLLaVO (Lee
pendix 8), which inspire future work to develop        et al., 2024) enhances MLLMs’ object-level im-
more powerful visual prompting methods.                age understanding through a visual prompt called
                                                       Crayon Prompt, which is derived from panoptic
6.1    Pre-training
                                                       color maps generated by a panoptic segmenta-
To improve MLLM’s ability on more fine-grained         tion model. CityLLaVA (Duan et al., 2024) in-
vision perception or reasoning tasks, a line of        troduces an efficient fine-tuning framework for
works focuses on designing better pre-training ob-     MLLM designed for urban scenarios which incor-
jectives including visual prompts. PSALM (Zhang        porates visual prompt engineering techniques, in-
et al., 2024h) extends the capabilities of MLLM        cluding bounding box-guided, view selection, and
to address various image segmentation tasks by         global-local joint views. ViP-LLaVA (Cai et al.,
incorporating a mask decoder and a flexible in-        2024) is enabled to understand arbitrary visual
put schema. This approach unifies multiple seg-        prompts, which is trained by directly overlaying vi-
mentation tasks within a single model, supporting      sual markers onto images. ImageBrush (Yang et al.,
generic, referring, interactive, and open-vocabulary   2024b) introduces a framework for exemplar-based
segmentation, while demonstrating strong perfor-       image manipulation that learns visual in-context
mance on both in-domain and out-of-domain pixel-       instructions without language prompts.
level segmentation tasks. OMG-LLaVA (Zhang                Explicit Visual Prompting (EVP) (Liu et al.,
et al., 2024e) proposes a unified framework that       2023b) proposes a unified approach for low-level
bridges image-level, object-level, and pixel-level     structure segmentation tasks with a frozen pre-
reasoning and understanding in a single model that     trained vision transformer backbone and introduces
combines a universal segmentation method as the        task-specific soft prompts derived from frozen
visual encoder with an LLM, enabling flexible user     patch embeddings and high-frequency image com-
interaction through various visual and text prompts.   ponents. BlackVIP (Oh et al., 2023) adapts large
VisionLLM v2 (Wu et al., 2024a) introduces an          pre-trained models with a Coordinator to gener-
end-to-end generalist MLLM that unifies visual         ate soft visual prompts and SPSA-GC for effi-
perception, understanding, and generation within       cient gradient estimation, enabling robust few-shot
a single framework. The model employs a novel          adaptation across diverse domains. Iterative La-
"super link" technique to connect the central LLM      bel Mapping-based Visual Prompting (ILM-VP)
with task-specific decoders, enabling flexible in-     (Chen et al., 2023a) improves the accuracy and in-
formation transmission and end-to-end optimiza-        terpretability of soft visual prompting by jointly op-
tion across hundreds of vision and vision-language     timizing input patterns and label mapping through
tasks. UrbanVLP (Hao et al., 2024) proposes a          bi-level optimization. MemVP (Jie et al., 2024)
vision-language pretraining framework for urban        efficiently combines pre-trained vision encoders
region profiling that integrates multi-granularity     and language models for vision-language tasks by
information from both satellite (macro-level) and      injecting visual information directly into the feed-
street-view (micro-level) imagery, overcoming pre-     forward network weights of MLLMs, treating them
vious limitations. This method also incorporates       as additional factual knowledge. VPG-C (Li et al.,
an automatic text generation and calibration mech-     2023a) enhances visual prompting in MLLMs by
anism to produce high-quality textual descriptions     completing missing visual details to better compre-

## Page 8

hend demonstrative instructions with interleaved        gation, approximating multimodal ICL prompts
multimodal context. It extends traditional Visual       to contain only a single query image. I2L(Wang
Prompt Generators by using LLM-guided, context-         et al., 2024a) combines demonstrations, visual cues,
aware visual feature extraction to create more com-     and reasoning into a single image to enhance mul-
prehensive visual prompts.                              timodal models’ performance on complex tasks
                                                        through ICL. I2L-Hybrid extends this by automat-
6.3    Instruction Tuning                               ically selecting between I2L and other in-context
Instruction tuning has proved to effectively im-        learning methods for each task instance.
prove the overall ability of both text-only LLMs           Few-shot learning through visual prompts can
and MLLMs such as instruction following and             also improve the capabilities of MLLMs with mini-
structured output (Ouyang et al., 2022; Wang et al.,    mum computational cost and better data efficiency.
2022; Liu et al., 2024a). For MLLMs with a fo-          CoMM (Chen et al., 2024b) proposes a high-quality
cus on visual prompts, AnyRef (He et al., 2024)         coherent interleaved image-text dataset designed
introduces a unified referring representation that      to enhance the generation capabilities of MLLMs
enables the MLLM to handle diverse input modal-         and investigate their in-context learning ability.
ities and visual prompts (text, bounding boxes,         M2oEGPT (Sheng et al., 2024) propose an ICL
images, audio) through instruction tuning. This         framework by using multimodal quantization and
model uses special tokens and prompts to format         unified embedding to enable joint learning of mul-
multi-modal inputs, allowing it to process various      timodal data in a general token embedding space,
referring formats consistently. A refocusing mecha-     combining an autoregressive transformer with a
nism enhances mask embeddings by incorporating          Mixture of Experts (MoEs) for stable multi-task co-
grounded textual embeddings, improving segmen-          training. Partial2Global (Xu et al., 2024a) select op-
tation accuracy. AnyRef combines vision and audio       timal in-context examples in visual ICL through a
encoders with an LLM, using projection layers to        transformer-based list-wise ranker to compare mul-
align different modalities in the language space.       tiple alternative samples and a consistency-aware
The model is instruction-tuned end-to-end with a        ranking aggregator to achieve globally consistent
combination of text loss and mask loss, enabling it     ranking. Hossain et al. (2024) introduces learn-
to generate both textual descriptions and pixel-level   able visual prompts for both base and novel classes
segmentation in response to multi-modal prompts.        on semantic segmentation, along with a novel-to-
                                                        base causal attention mechanism that allows novel
7     In-context and Few-shot Learning                  prompts to be contextualized by base prompts with-
                                                        out degrading base class performance. Emu2 (Sun
Beyond methods that optimize performance us-            et al., 2024) is MLLM trained to predict the next el-
ing single data points as input, some works focus       ement in diverse multimodal sequences. Its unified
on enhancing in-context learning (ICL) with vi-         architecture enables strong multimodal in-context
sual prompts. Image-of-Thought (IoT) prompting          learning abilities, allowing it to quickly adapt to
(Zhou et al., 2024b) is a train-free approach to en-    new tasks with just a few examples.
hance MLLMs for visual question-answering tasks
by integrating discrete image processing actions.       8   Evaluation
IoT enables MLLMs to automatically design and
extract visual rationales step-by-step, combining       This section explores and compares the current
them with textual rationales to improve both accu-      MLLM visual prompting training datasets and
racy and interpretability. CRG (Wan et al., 2024) is    benchmarks, as visualized in Section 7.1. The
a training-free method that improves visual ground-     three main categories for the visual prompting
ing in MLLMs by contrasting model outputs with          techniques are Semantic Prompting (SP), Textual
and without specific image regions masked which         Prompting (TP), and GP (Generative Prompting).
guides models to focus on relevant image areas.            The datasets and benchmarks that fall into the
AIM (Gao et al., 2024) enables any MLLM to per-         Semantic Prompting (SP) utilize high-level descrip-
form efficient ICL by aggregating image informa-        tions to help the model understand the semantic
tion from demonstrations into the latent space of       relationships present in the data. Some examples in-
corresponding textual labels which reduces mem-         cude creating bounding boxes (Huang et al., 2024a;
ory costs by discarding visual tokens after aggre-      Wu et al., 2024c), labeling regions of interest (Li

## Page 9

      Reference                             SP   TP   GP     Image     Video   Audio    Manual    Automatic
      MDVP-Bench (Lin et al., 2024a)        ✓    ✓     ✓        ✓                         ✓           ✓
      A3VLM (Huang et al., 2024a)           ✓                   ✓                                     ✓
      VLM Feedback (Li et al., 2023c)       ✓                   ✓       ✓                 ✓           ✓
      GPT-4V Challenger (Fu et al., 2023)   ✓          ✓        ✓
      EarthMarker (Zhang et al., 2024f)     ✓    ✓     ✓        ✓                         ✓
      RACCooN (Yoon et al., 2024)                      ✓                ✓                 ✓           ✓
      Safety of MLLMs(Liu et al., 2024b)               ✓        ✓       ✓        ✓
      GLEE (Wu et al., 2024c)               ✓    ✓              ✓       ✓
      AutoAD-Zero (Xie et al., 2024)        ✓          ✓        ✓                ✓                    ✓
      MultipanelVQA (Fan et al., 2024c)                ✓        ✓
      MM-Vid (Lin et al., 2023)             ✓    ✓     ✓        ✓       ✓        ✓        ✓
      Groma (Ma et al., 2024a)              ✓    ✓              ✓                         ✓           ✓


Table 1: We compare different benchmarks and training datasets, and they are each grouped into three different
criteria–Semantic Prompting (SP), Textual Prompting (TP), and Generative Prompting (GP). Then, based on the
different modalities, they can be classified if they contain pixel-level images (Image), video encoding and decoding
(Video), and if they are supplemented by an audio transcript (Audio). Finally, the last categorization determines if
the specified method visual prompting is done manually (Manual), automated (Automatic), or a combination of
both.


et al., 2023c), and tagging objects (Lin et al., 2024a;     fine-grained accuracy. Some techniques apply a
Zhang et al., 2024f). Another general method is             combination of these (Lin et al., 2024a; Li et al.,
Textual Prompting (TP) where either user or LLM             2023c; Yoon et al., 2024; Ma et al., 2024a) and
generated text is supplemented into the model input         those that do not have either checked were either
that relates the visual aspects in the image. Image         training datasets or surveys themselves (Liu et al.,
and video descriptions can be generated and used            2024b; Fan et al., 2024c; Fu et al., 2023).
as a visual prompt (Lin et al., 2023), drawing re-
lationships and descriptions on the image itself in         9     Frontier Applications
order to add location-specific analysis (Lin et al.,
2024a; Wu et al., 2024c), and embedding local-              9.1     Jailbreaking & Safety
ization into image tokenization (Ma et al., 2024a).         While visual prompting enables fine-grained in-
Given the extensive effort required for manual vi-          structions to MLLMs for better response genera-
sual prompting in MLLMs, some techniques have               tion, it can also be intentionally designed to ex-
adopted automatic generation methods to stream-             pose critical safety issues of MLLMs (Liu et al.,
line the visual prompting process using Generative          2024b; Ni et al., 2024). Several works have ex-
Prompting (GP). Automatic modality conversion               plored jailbreaking of MLLMs with visual prompts.
uses LLMs to generate text from images/videos and           Instead of feeding harmful textual instructions di-
vice versa for users to easily modify and cater the         rectly, Gong et al. (2023) converts them into images
prompts (Yoon et al., 2024). Audio descriptions             through typography and feeds them to MLLMs as
are generated and then summarized by an LLM                 visual prompts. The results show that even if the
[(Xie et al., 2024), [(Lin et al., 2023)]]. Similarly,      underlying LLM has been aligned for safety, vi-
generation is used to create difficult and unique           sual prompting opens a new jailbreaking surface
benchmarks to assess the capabilities and weak-             generating harmful responses.
nesses of specific models [(Fan et al., 2024c)].               To further expose the safety problems of
   The final taxonomy system distinguishes be-              MLLMs for red-teaming, multimodal jailbreaking
tween those visual prompting techniques that are            prompts combining both textual and visual instruc-
done manually between those that are done au-               tions are also studied. Ying et al. (2024) first embed
tomatically. The manual techniques offer preci-             harmful perturbation in the visual prompt and then
sion and customization, but in turn sacrifice time          optimize the textual prompt through LLM reason-
and efficiency. They are suitable for tasks that are        ing on the harmful intent in the image. Meanwhile,
smaller scale and require detail. Automatic tech-           Liu et al. (2024c) utilize a red-team MLLM and a
niques provide scalability and productivity–they            red-team LLM guided by reinforcement learning to
work well with large scale tasks that do not require        automatically generate visual and textual jailbrear-

## Page 10

king prompts respectively. Their results suggest         generating more robust and grounded responses.
that multimodal prompts could lead to stronger
attack on MLLMs that fuse multimodal input fea-          9.4   Visual Generation
tures. Furthermore, Gu et al. (2024) observe a more
severe safety issue of infectious jailbreark in multi-   Visual generation models, especially text-to-image
agent MLLM environments. With an adversarial             diffusion models (Rombach et al., 2022), are be-
image simply jailbreaking one agent and without          coming popular. Considering large-scale pre-
any further intervention, almost all agents will start   trained diffusion models as MLLMs broadly, visual
exhibit harmful behaviors in an exponential infec-       prompting plays an important role in controlling the
tion rate during multi-agent interaction.                generation and enable diffusion models for unseen
                                                         visual tasks. Zhang et al. (2023c), Mou et al. (2024)
9.2   Hallucination                                      propose ControlNet and T2I Adapter, which take
The more fine-grained visual contexts provided           various visual prompts for spatial control in image
with visual prompting are also useful for multi-         generation. In this survey, we discuss works that
modal hallucination mitigation. To address the           focus on visual prompting instead of controllable
issue that MLLMs’ textual outputs are often not          generation (Cao et al., 2024) in general. Prompt
grounded in the reference images, Favero et al.          Diffusion (Wang et al., 2023) proposes a diffusion-
(2024) propose a mutual-information decoding             based generative model that takes a novel vision-
strategy to amplify the influence of visual prompts      language prompts and outputs the target images,
on model generation. To reduce MLLMs’ object             which unlocks the ability of in-context generation
hallucination and enhance fine-grained understand-       after fine-tuned on six visual tasks. ImageBrush
ing in object-oriented perception tasks, Jiang et al.    (Yang et al., 2024b) proposes to achieve adaptive
(2024) develop a prompting strategy jointly uti-         image manipulation under the instruction of a pair
lizing visual and textual prompts. A specialized         of exemplar demonstrations in order to address
detection model is employed to highlight relevant        the issue of language ambiguity in image editing
visual objects and visual prompts based on the key       task. MPerceiver (Ai et al., 2024) introduces a
concepts extracted from textual prompts. While           multi-modal prompt learning approach using gen-
previous works mostly focus on single-object hal-        erative priors of diffusion models to enhance the
lucination, Chen et al. (2024c) utilize visual refer-    all-in-one image restoration. Chen et al. (2024d)
ring prompts to evaluate multi-object hallucination      proposes VP3D, which leverages rich knowledge
of MLLMs. The results show MLLMs tend to                 in 2D visual prompts to improve text-to-3D gen-
experience more hallucinations when tasked with          eration quality and trigger a new task of stylized
focusing multiple objects at the same time and au-       text-to-3D generation. PromptCharm (Wang et al.,
thors suggest probing objects individually in visual     2024c) proposes an interaction system that sup-
prompts to enhance performances.                         ports text-to-image creation through multi-modal
                                                         prompting and image refinement, which suggests
9.3   Debiasing                                          the necessity of visual prompting for better image
Despite the impressive capabilities of MLLMs, the        creation.
biases and robustness of them remain a crucial
challenge where models tend to utilize spurious          10    Conclusion
correlations between input and target variables for
predictions leading to potential social biases on        In this survey, we provide the first comprehensive
certain topics, e.g., gender and racial biases (Ye       review of visual prompting methods in MLLMs.
et al., 2024). As visual prompting enables more          We categorized various visual prompting tech-
fine-grained understanding of visual objects and         niques and discussed their generation processes,
relationships, it serves as a promising solution to      examining their integration into MLLMs for en-
mitigate potential biases in MLLMs’ generations          hanced visual reasoning and perception. Our
by grounding the outputs with essential visual infor-    work also examines existing training and in-context
mation and thus avoiding spurious correlations of        learning methods in MLLMs with visual prompting.
non-essential inputs. It may also enhance the causal     We inspire future directions that leverage visual
understanding of MLLMs between objects from the          prompts for better MLLM compositional reason-
same modality and across different modalities for        ing.

## Page 11

11    Limitations                                          Wei Chen, Lin Li, Yongqi Yang, Bin Wen, Fan Yang,
                                                            Tingting Gao, Yu Wu, and Long Chen. 2024b.
While our survey offers a comprehensive overview,           Comm: A coherent interleaved image-text dataset
it may be limited by the rapidly evolving nature            for multimodal understanding and generation. arXiv
of the field and potential gaps in the available lit-       preprint arXiv:2406.10462.
erature. Future work should focus on expanding             Xuweiyi Chen, Ziqiao Ma, Xuejun Zhang, Sihan
the scope of visual prompts and refining alignment           Xu, Shengyi Qian, Jianing Yang, David F Fouhey,
techniques to further enhance MLLM capabilities.             and Joyce Chai. 2024c. Multi-object hallucina-
                                                             tion in vision-language models. arXiv preprint
                                                             arXiv:2407.06192.
References                                                 Yang Chen, Yingwei Pan, Haibo Yang, Ting Yao, and
                                                             Tao Mei. 2024d. Vp3d: Unleashing 2d visual prompt
Yuang Ai, Huaibo Huang, Xiaoqiang Zhou, Jiexiang
                                                             for text-to-3d generation. In Proceedings of the
  Wang, and Ran He. 2024. Multimodal prompt per-
                                                             IEEE/CVF Conference on Computer Vision and Pat-
  ceiver: Empower adaptiveness generalizability and
                                                             tern Recognition, pages 4896–4905.
  fidelity for all-in-one image restoration. In Proceed-
  ings of the IEEE/CVF Conference on Computer Vi-          Jang Hyun Cho, Boris Ivanovic, Yulong Cao, Edward
  sion and Pattern Recognition, pages 25432–25444.           Schmerling, Yue Wang, Xinshuo Weng, Boyi Li,
                                                             Yurong You, Philipp Krähenbühl, Yan Wang, et al.
Zechen Bai, Pichao Wang, Tianjun Xiao, Tong He,              2024. Language-image models with 3d understand-
  Zongbo Han, Zheng Zhang, and Mike Zheng Shou.              ing. arXiv preprint arXiv:2405.03685.
  2024. Hallucination of multimodal large language
  models: A survey. arXiv preprint arXiv:2404.18930.       Ronghao Dang, Jiangyan Feng, Haodong Zhang,
                                                             Chongjian Ge, Lin Song, Lijun Gong, Chengju
Amir Bar, Yossi Gandelsman, Trevor Darrell, Amir             Liu, Qijun Chen, Feng Zhu, Rui Zhao, et al. 2023.
 Globerson, and Alexei Efros. 2022. Visual prompt-           Instructdet: Diversifying referring object detec-
 ing via image inpainting. Advances in Neural Infor-         tion with generalized instructions. arXiv preprint
 mation Processing Systems, 35:25005–25017.                  arXiv:2310.05136.
Garrick Brazil, Abhinav Kumar, Julian Straub, Nikhila      Zhizhao Duan, Hao Cheng, Duo Xu, Xi Wu, Xiangxie
  Ravi, Justin Johnson, and Georgia Gkioxari. 2023.          Zhang, Xi Ye, and Zhen Xie. 2024. Cityllava: Effi-
  Omni3d: A large benchmark and model for 3d ob-             cient fine-tuning for vlms in city scenario. In Pro-
  ject detection in the wild. In Proceedings of the          ceedings of the IEEE/CVF Conference on Computer
  IEEE/CVF conference on computer vision and pat-            Vision and Pattern Recognition, pages 7180–7189.
  tern recognition, pages 13154–13164.
                                                           Sheng Fan, Rui Liu, Wenguan Wang, and Yi Yang.
Mu Cai, Haotian Liu, Siva Karthik Mustikovela, Gre-          2024a. Navigation instruction generation with bev
 gory P Meyer, Yuning Chai, Dennis Park, and                 perception and large language models. arXiv preprint
 Yong Jae Lee. 2024. Vip-llava: Making large multi-          arXiv:2407.15087.
 modal models understand arbitrary visual prompts.
 In Proceedings of the IEEE/CVF Conference on Com-         Yue Fan, Lei Ding, Ching-Chen Kuo, Shan Jiang, Yang
 puter Vision and Pattern Recognition, pages 12914–          Zhao, Xinze Guan, Jie Yang, Yi Zhang, and Xin Eric
 12923.                                                      Wang. 2024b. Read anywhere pointed: Layout-aware
                                                             gui screen reading with tree-of-lens grounding. arXiv
Pu Cao, Feng Zhou, Qing Song, and Lu Yang. 2024.             preprint arXiv:2406.19263.
  Controllable generation with text-to-image diffusion
  models: A survey. arXiv preprint arXiv:2403.04279.       Yue Fan, Jing Gu, Kaiwen Zhou, Qianqi Yan, Shan
                                                             Jiang, Ching-Chen Kuo, Xinze Guan, and Xin Eric
Aochuan Chen, Yuguang Yao, Pin-Yu Chen, Yihua                Wang. 2024c. Muffin or chihuahua? challenging
  Zhang, and Sijia Liu. 2023a. Understanding and             large vision-language models with multipanel vqa.
  improving visual prompting: A label-mapping per-           arXiv preprint arXiv:2401.15847.
  spective. In Proceedings of the IEEE/CVF Confer-
  ence on Computer Vision and Pattern Recognition,         Alessandro Favero, Luca Zancato, Matthew Trager, Sid-
  pages 19133–19143.                                         dharth Choudhary, Pramuditha Perera, Alessandro
                                                             Achille, Ashwin Swaminathan, and Stefano Soatto.
Jiaqi Chen, Bingqian Lin, Xinmin Liu, Xiaodan Liang,         2024. Multi-modal hallucination control by vi-
   and Kwan-Yee K Wong. 2024a. Affordances-                  sual information grounding. In Proceedings of the
   oriented planning using foundation models for con-        IEEE/CVF Conference on Computer Vision and Pat-
   tinuous vision-language navigation. arXiv preprint        tern Recognition, pages 14303–14312.
   arXiv:2407.05890.
                                                           Chaoyou Fu, Renrui Zhang, Haojia Lin, Zihan Wang,
Keqin Chen, Zhao Zhang, Weili Zeng, Richong Zhang,           Timin Gao, Yongdong Luo, Yubo Huang, Zhengye
  Feng Zhu, and Rui Zhao. 2023b. Shikra: Unleashing          Zhang, Longtian Qiu, Gaoxiang Ye, et al. 2023. A
  multimodal llm’s referential dialogue magic. arXiv         challenger to gpt-4v? early explorations of gemini in
  preprint arXiv:2306.15195.                                 visual expertise. arXiv preprint arXiv:2312.12436.

## Page 12

Jun Gao, Qian Qiao, Ziqiang Cao, Zili Wang, and Wen-          visual comprehension training.       arXiv preprint
  jie Li. 2024. Aim: Let any multi-modal large lan-           arXiv:2404.14604.
  guage models embrace efficient in-context learning.
  arXiv preprint arXiv:2406.07588.                          Songtao Jiang, Yan Zhang, Chenyi Zhou, Yeying Jin,
                                                              Yang Feng, Jian Wu, and Zuozhu Liu. 2024. Joint
Ross Girshick. 2015. Fast r-cnn. In Proceedings of the        visual and text prompting for improved object-centric
  IEEE international conference on computer vision,           perception with multimodal large language models.
  pages 1440–1448.                                            arXiv preprint arXiv:2404.04514.

Yichen Gong, Delong Ran, Jinyuan Liu, Conglei Wang,         Shibo Jie, Yehui Tang, Ning Ding, Zhi-Hong Deng, Kai
  Tianshuo Cong, Anyu Wang, Sisi Duan, and Xiaoyun            Han, and Yunhe Wang. 2024. Memory-space visual
  Wang. 2023. Figstep: Jailbreaking large vision-             prompting for efficient vision-language fine-tuning.
  language models via typographic visual prompts.             arXiv preprint arXiv:2405.05615.
  arXiv preprint arXiv:2311.05608.
                                                            Alexander Kirillov, Eric Mintun, Nikhila Ravi, Hanzi
Jindong Gu, Zhen Han, Shuo Chen, Ahmad Beirami,               Mao, Chloe Rolland, Laura Gustafson, Tete Xiao,
   Bailan He, Gengyuan Zhang, Ruotong Liao, Yao Qin,          Spencer Whitehead, Alexander C Berg, Wan-Yen Lo,
   Volker Tresp, and Philip Torr. 2023. A systematic sur-     et al. 2023. Segment anything. In Proceedings of the
   vey of prompt engineering on vision-language foun-         IEEE/CVF International Conference on Computer
   dation models. arXiv preprint arXiv:2307.12980.            Vision, pages 4015–4026.

Xiangming Gu, Xiaosen Zheng, Tianyu Pang, Chao              Byung-Kwan Lee, Beomchan Park, Chae Won Kim, and
  Du, Qian Liu, Ye Wang, Jing Jiang, and Min Lin.             Yong Man Ro. 2024. Collavo: Crayon large language
  2024. Agent smith: A single image can jailbreak             and vision model. arXiv preprint arXiv:2402.11248.
  one million multimodal llm agents exponentially fast.
                                                            Xuanyu Lei, Zonghan Yang, Xinrui Chen, Peng Li, and
  arXiv preprint arXiv:2402.08567.
                                                              Yang Liu. 2024a. Scaffolding coordinates to promote
Xixuan Hao, Wei Chen, Yibo Yan, Siru Zhong, Kun               vision-language coordination in large multi-modal
  Wang, Qingsong Wen, and Yuxuan Liang. 2024.                 models. arXiv preprint arXiv:2402.12058.
  Urbanvlp: A multi-granularity vision-language pre-        Yiming Lei, Jingqi Li, Zilong Li, Yuan Cao, and Hong-
  trained foundation model for urban indicator predic-        ming Shan. 2024b. Prompt learning in computer
  tion. arXiv preprint arXiv:2403.16831.                      vision: a survey. Frontiers of Information Technol-
Junwen He, Yifan Wang, Lijun Wang, Huchuan Lu,                ogy & Electronic Engineering, 25(1):42–63.
  Jun-Yan He, Jin-Peng Lan, Bin Luo, and Xuansong           Juncheng Li, Kaihang Pan, Zhiqi Ge, Minghe Gao, Wei
  Xie. 2024. Multi-modal instruction tuned llms with          Ji, Wenqiao Zhang, Tat-Seng Chua, Siliang Tang,
  fine-grained visual perception. In Proceedings of           Hanwang Zhang, and Yueting Zhuang. 2023a. Fine-
  the IEEE/CVF Conference on Computer Vision and              tuning multimodal llms to follow zero-shot demon-
  Pattern Recognition, pages 13980–13990.                     strative instructions. In The Twelfth International
                                                              Conference on Learning Representations.
Mir Rayat Imtiaz Hossain, Mennatullah Siam, Leonid
  Sigal, and James J Little. 2024. Visual prompting for     Junnan Li, Dongxu Li, Silvio Savarese, and Steven Hoi.
  generalized few-shot segmentation: A multi-scale ap-        2023b. Blip-2: Bootstrapping language-image pre-
  proach. In Proceedings of the IEEE/CVF Conference           training with frozen image encoders and large lan-
  on Computer Vision and Pattern Recognition, pages           guage models. In International conference on ma-
  23470–23480.                                                chine learning, pages 19730–19742. PMLR.
Siyuan Huang, Haonan Chang, Yuhan Liu, Yimeng               Yinheng Li. 2023. A practical survey on zero-shot
  Zhu, Hao Dong, Peng Gao, Abdeslam Boularias,                prompt design for in-context learning. arXiv preprint
  and Hongsheng Li. 2024a. A3vlm: Actionable                  arXiv:2309.13205.
  articulation-aware vision language model. arXiv
  preprint arXiv:2406.07549.                                Zeju Li, Chao Zhang, Xiaoyan Wang, Ruilong Ren, Yi-
                                                              fan Xu, Ruifei Ma, and Xiangde Liu. 2024. 3dmit:
Wen Huang, Hongbin Liu, Minxin Guo, and Neil Zhen-            3d multi-modal instruction tuning for scene under-
  qiang Gong. 2024b. Visual hallucinations of multi-          standing. arXiv preprint arXiv:2401.03201.
  modal large language models. arXiv preprint
  arXiv:2402.14683.                                         Zongjie Li, Chaozheng Wang, Chaowei Liu, Pingchuan
                                                              Ma, Daoyuan Wu, Shuai Wang, and Cuiyun Gao.
Zhipeng Huang, Zhizheng Zhang, Zheng-Jun Zha, Yan             2023c. Vrptest: Evaluating visual referring prompt-
  Lu, and Baining Guo. 2024c. Relationvlm: Mak-               ing in large multimodal models. arXiv preprint
  ing large vision-language models understand visual          arXiv:2312.04087.
  relations. arXiv preprint arXiv:2403.12801.
                                                            Yuan-Hong Liao, Rafid Mahmood, Sanja Fidler, and
Mengzhao Jia, Zhihan Zhang, Wenhao Yu, Fangkai Jiao,          David Acuna. 2024. Can feedback enhance semantic
  and Meng Jiang. 2024. Describe-then-reason: Im-             grounding in large vision-language models? arXiv
  proving multimodal mathematical reasoning through           preprint arXiv:2404.06510.

## Page 13

Kevin Lin, Faisal Ahmed, Linjie Li, Chung-Ching Lin,        Proceedings of the AAAI Conference on Artificial
  Ehsan Azarnasab, Zhengyuan Yang, Jianfeng Wang,           Intelligence, volume 38, pages 4296–4304.
  Lin Liang, Zicheng Liu, Yumao Lu, et al. 2023. Mm-
  vid: Advancing video understanding with gpt-4v          Soroush Nasiriany, Fei Xia, Wenhao Yu, Ted Xiao,
  (ision). arXiv preprint arXiv:2310.19773.                 Jacky Liang, Ishita Dasgupta, Annie Xie, Danny
                                                            Driess, Ayzaan Wahid, Zhuo Xu, et al. 2024. Pivot:
Weifeng Lin, Xinyu Wei, Ruichuan An, Peng Gao,              Iterative visual prompting elicits actionable knowl-
 Bocheng Zou, Yulin Luo, Siyuan Huang, Shang-               edge for vlms. arXiv preprint arXiv:2402.07872.
 hang Zhang, and Hongsheng Li. 2024a. Draw-and-
 understand: Leveraging visual prompts to enable          Minheng Ni, Yeli Shen, Lei Zhang, and Wangmeng Zuo.
 mllms to comprehend what you want. arXiv preprint          2024. Responsible visual editing. arXiv preprint
 arXiv:2403.20271.                                          arXiv:2404.05580.
Yuanze Lin, Yunsheng Li, Dongdong Chen, Weijian
  Xu, Ronald Clark, Philip Torr, and Lu Yuan. 2024b.      Changdae Oh, Hyeji Hwang, Hee-young Lee, YongTaek
  Rethinking visual prompting for multimodal large          Lim, Geunyoung Jung, Jiyoung Jung, Hosik Choi,
  language models with external knowledge. arXiv            and Kyungwoo Song. 2023. Blackvip: Black-box
  preprint arXiv:2407.04681.                                visual prompting for robust transfer learning. In Pro-
                                                            ceedings of the IEEE/CVF Conference on Computer
Dingning Liu, Xiaomeng Dong, Renrui Zhang, Xu Luo,          Vision and Pattern Recognition, pages 24224–24235.
  Peng Gao, Xiaoshui Huang, Yongshun Gong, and
  Zhihui Wang. 2023a. 3daxiesprompts: Unleash-            Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
  ing the 3d spatial task capabilities of gpt-4v. arXiv     Carroll Wainwright, Pamela Mishkin, Chong Zhang,
  preprint arXiv:2312.09738.                                Sandhini Agarwal, Katarina Slama, Alex Ray, et al.
                                                            2022. Training language models to follow instruc-
Haotian Liu, Chunyuan Li, Qingyang Wu, and Yong Jae         tions with human feedback. Advances in neural in-
  Lee. 2024a. Visual instruction tuning. Advances in        formation processing systems, 35:27730–27744.
  neural information processing systems, 36.
                                                          Kaihang Pan, Siliang Tang, Juncheng Li, Zhaoyu Fan,
Weihuang Liu, Xi Shen, Chi-Man Pun, and Xiaodong            Wei Chow, Shuicheng Yan, Tat-Seng Chua, Yueting
 Cun. 2023b. Explicit visual prompting for low-             Zhuang, and Hanwang Zhang. 2024. Auto-encoding
 level structure segmentations. In Proceedings of the       morph-tokens for multimodal llm. arXiv preprint
 IEEE/CVF Conference on Computer Vision and Pat-            arXiv:2405.01926.
 tern Recognition, pages 19434–19445.

Xin Liu, Yichen Zhu, Yunshi Lan, Chao Yang, and           Leigang Qu, Haochuan Li, Tan Wang, Wenjie Wang,
  Yu Qiao. 2024b. Safety of multimodal large lan-           Yongqi Li, Liqiang Nie, and Tat-Seng Chua. 2024.
  guage models on images and text. arXiv preprint           Unified text-to-image generation and retrieval. arXiv
  arXiv:2402.00357.                                         preprint arXiv:2406.05814.

Yi Liu, Chengjun Cai, Xiaoli Zhang, Xingliang Yuan,       Huali Ren, Anli Yan, Chong-zhi Gao, Hongyang Yan,
  and Cong Wang. 2024c. Arondight: Red teaming              Zhenxin Zhang, and Jin Li. 2024. Are you copy-
  large vision language models with auto-generated          ing my prompt? protecting the copyright of vision
  multi-modal jailbreak prompts. arXiv preprint             prompt for vpaas via watermark. arXiv preprint
  arXiv:2407.15050.                                         arXiv:2405.15161.

Bozhi Luan, Hao Feng, Hong Chen, Yonghui Wang,            Razieh Rezaei, Masoud Jalili Sabet, Jindong Gu,
  Wengang Zhou, and Houqiang Li. 2024. Textcot:             Daniel Rueckert, Philip Torr, and Ashkan Khakzar.
  Zoom in for enhanced multimodal text-rich image           2024. Learning visual prompts for guiding the
  understanding. arXiv preprint arXiv:2404.09797.           attention of vision transformers. arXiv preprint
                                                            arXiv:2406.03303.
Chuofan Ma, Yi Jiang, Jiannan Wu, Zehuan Yuan, and
  Xiaojuan Qi. 2024a. Groma: Localized visual tok-
                                                          Robin Rombach, Andreas Blattmann, Dominik Lorenz,
  enization for grounding multimodal large language
                                                            Patrick Esser, and Björn Ommer. 2022. High-
  models. arXiv preprint arXiv:2404.13013.
                                                            resolution image synthesis with latent diffusion mod-
Huan Ma, Yan Zhu, Changqing Zhang, Peilin Zhao,             els. In Proceedings of the IEEE/CVF conference
  Baoyuan Wu, Long-Kai Huang, Qinghua Hu, and               on computer vision and pattern recognition, pages
  Bingzhe Wu. 2024b. Invariant test-time adaptation         10684–10695.
  for vision-language model generalization. arXiv
  preprint arXiv:2403.00376.                              Sander Schulhoff, Michael Ilie, Nishant Balepur, Kon-
                                                            stantine Kahadze, Amanda Liu, Chenglei Si, Yin-
Chong Mou, Xintao Wang, Liangbin Xie, Yanze Wu,             heng Li, Aayush Gupta, HyoJung Han, Sevien Schul-
  Jian Zhang, Zhongang Qi, and Ying Shan. 2024. T2i-        hoff, et al. 2024. The prompt report: A system-
  adapter: Learning adapters to dig out more control-       atic survey of prompting techniques. arXiv preprint
  lable ability for text-to-image diffusion models. In      arXiv:2406.06608.

## Page 14

Dianmo Sheng, Dongdong Chen, Zhentao Tan, Qiankun        Junda Wu, Xintong Li, Tong Yu, Yu Wang, Xiang Chen,
  Liu, Qi Chu, Jianmin Bao, Tao Gong, Bin Liu, Sheng-      Jiuxiang Gu, Lina Yao, Jingbo Shang, and Julian
  wei Xu, and Nenghai Yu. 2024. Towards more uni-          McAuley. 2024b. Commit: Coordinated instruction
  fied in-context visual understanding. In Proceedings     tuning for multimodal large language models. arXiv
  of the IEEE/CVF Conference on Computer Vision            preprint arXiv:2407.20454.
  and Pattern Recognition, pages 13362–13372.
                                                         Junda Wu, Rui Wang, Handong Zhao, Ruiyi Zhang,
Aleksandar Shtedritski, Christian Rupprecht, and An-       Chaochao Lu, Shuai Li, and Ricardo Henao. 2023.
  drea Vedaldi. 2023. What does clip know about a red      Few-shot composition learning for image retrieval
  circle? visual prompt engineering for vlms. In Pro-      with prompt tuning. In Proceedings of the AAAI Con-
  ceedings of the IEEE/CVF International Conference        ference on Artificial Intelligence, volume 37, pages
  on Computer Vision, pages 11987–11997.                   4729–4737.
Quan Sun, Yufeng Cui, Xiaosong Zhang, Fan Zhang,
  Qiying Yu, Yueze Wang, Yongming Rao, Jingjing          Junfeng Wu, Yi Jiang, Qihao Liu, Zehuan Yuan, Xiang
  Liu, Tiejun Huang, and Xinlong Wang. 2024. Gener-        Bai, and Song Bai. 2024c. General object foundation
  ative multimodal models are in-context learners. In      model for images and videos at scale. In Proceedings
  Proceedings of the IEEE/CVF Conference on Com-           of the IEEE/CVF Conference on Computer Vision
  puter Vision and Pattern Recognition, pages 14398–       and Pattern Recognition, pages 3783–3795.
  14409.
                                                         Mingrui Wu, Xinyue Cai, Jiayi Ji, Jiale Li, Oucheng
Georgios Tziafas and Hamidreza Kasaei. 2024. To-           Huang, Gen Luo, Hao Fei, Xiaoshuai Sun, and Ron-
  wards open-world grasping with large vision-             grong Ji. 2024d. Controlmllm: Training-free visual
  language models. arXiv preprint arXiv:2406.18722.        prompt learning for multimodal large language mod-
                                                           els. arXiv preprint arXiv:2407.21534.
David Wan, Jaemin Cho, Elias Stengel-Eskin, and Mo-
  hit Bansal. 2024. Contrastive region guidance: Im-     Tung-Yu Wu, Sheng-Yu Huang, and Yu-Chiang Frank
  proving grounding in vision-language models with-        Wang. 2024e. Dora: 3d visual grounding with order-
  out training. arXiv preprint arXiv:2403.02325.           aware referring. arXiv preprint arXiv:2403.16539.
Lei Wang, Wanyu Xu, Zhiqiang Hu, Yihuai Lan, Shan
                                                         Yixuan Wu, Yizhou Wang, Shixiang Tang, Wenhao Wu,
  Dong, Hao Wang, Roy Ka-Wei Lee, and Ee-Peng
                                                           Tong He, Wanli Ouyang, Jian Wu, and Philip Torr.
  Lim. 2024a. All in an aggregated image for in-image
                                                           2024f. Dettoolchain: A new prompting paradigm
  learning.
                                                           to unleash detection ability of mllm. arXiv preprint
Wenhai Wang, Zhe Chen, Xiaokang Chen, Jiannan Wu,          arXiv:2403.12488.
 Xizhou Zhu, Gang Zeng, Ping Luo, Tong Lu, Jie
  Zhou, Yu Qiao, et al. 2024b. Visionllm: Large          Enze Xie, Wenhai Wang, Zhiding Yu, Anima Anand-
  language model is also an open-ended decoder for         kumar, Jose M Alvarez, and Ping Luo. 2021. Seg-
 vision-centric tasks. Advances in Neural Information      former: Simple and efficient design for semantic
 Processing Systems, 36.                                   segmentation with transformers. Advances in neural
                                                           information processing systems, 34:12077–12090.
Yizhong Wang, Yeganeh Kordi, Swaroop Mishra, Al-
  isa Liu, Noah A Smith, Daniel Khashabi, and Han-       Junyu Xie, Tengda Han, Max Bain, Arsha Nagrani,
  naneh Hajishirzi. 2022. Self-instruct: Aligning lan-     Gül Varol, Weidi Xie, and Andrew Zisserman.
  guage models with self-generated instructions. arXiv     2024. Autoad-zero: A training-free framework
  preprint arXiv:2212.10560.                               for zero-shot audio description. arXiv preprint
                                                           arXiv:2407.15850.
Zhendong Wang, Yifan Jiang, Yadong Lu, Pengcheng
  He, Weizhu Chen, Zhangyang Wang, Mingyuan              Chengming Xu, Chen Liu, Yikai Wang, and Yan-
  Zhou, et al. 2023. In-context learning unlocked for      wei Fu. 2024a. Towards global optimal visual in-
  diffusion models. Advances in Neural Information         context learning prompt selection. arXiv preprint
  Processing Systems, 36:8542–8562.                        arXiv:2405.15279.
Zhijie Wang, Yuheng Huang, Da Song, Lei Ma, and
  Tianyi Zhang. 2024c. Promptcharm: Text-to-image        Xin Xu, Yue Liu, Panupong Pasupat, Mehran Kazemi,
  generation through multi-modal prompting and re-         et al. 2024b. In-context learning with retrieved
  finement. In Proceedings of the CHI Conference on        demonstrations for language models: A survey.
  Human Factors in Computing Systems, pages 1–21.          arXiv preprint arXiv:2401.11624.

Jiannan Wu, Muyan Zhong, Sen Xing, Zeqiang Lai,          An Yan, Zhengyuan Yang, Junda Wu, Wanrong Zhu,
   Zhaoyang Liu, Wenhai Wang, Zhe Chen, Xizhou             Jianwei Yang, Linjie Li, Kevin Lin, Jianfeng Wang,
   Zhu, Lewei Lu, Tong Lu, et al. 2024a. Visionllm v2:     Julian McAuley, Jianfeng Gao, et al. 2024. List
   An end-to-end generalist multimodal large language      items one by one: A new data source and learn-
   model for hundreds of vision-language tasks. arXiv      ing paradigm for multimodal llms. arXiv preprint
   preprint arXiv:2406.08394.                              arXiv:2404.16375.

## Page 15

Jianwei Yang, Hao Zhang, Feng Li, Xueyan Zou, Chun-         International Conference on Computer Vision, pages
   yuan Li, and Jianfeng Gao. 2023. Set-of-mark             3836–3847.
   prompting unleashes extraordinary visual grounding
   in gpt-4v. arXiv preprint arXiv:2310.11441.            Sha Zhang, Di Huang, Jiajun Deng, Shixiang Tang,
                                                            Wanli Ouyang, Tong He, and Yanyong Zhang. 2024d.
Lingfeng Yang, Yueze Wang, Xiang Li, Xinlong Wang,          Agent3d-zero: An agent for zero-shot 3d understand-
  and Jian Yang. 2024a. Fine-grained visual prompting.      ing. arXiv preprint arXiv:2403.11835.
  Advances in Neural Information Processing Systems,
  36.                                                     Tao Zhang, Xiangtai Li, Hao Fei, Haobo Yuan,
                                                            Shengqiong Wu, Shunping Ji, Chen Change Loy,
Yifan Yang, Houwen Peng, Yifei Shen, Yuqing Yang,           and Shuicheng Yan. 2024e. Omg-llava: Bridging
  Han Hu, Lili Qiu, Hideki Koike, et al. 2024b. Im-         image-level, object-level, pixel-level reasoning and
  agebrush: Learning visual in-context instructions for     understanding. arXiv preprint arXiv:2406.19389.
  exemplar-based image manipulation. Advances in
  Neural Information Processing Systems, 36.              Wei Zhang, Miaoxin Cai, Tong Zhang, Yin Zhuang,
                                                           and Xuerui Mao. 2024f. Earthmarker: A visual
Wenqian Ye, Guangtao Zheng, Yunsheng Ma, Xu Cao,           prompt learning framework for region-level and
  Bolin Lai, James M Rehg, and Aidong Zhang. 2024.         point-level remote sensing imagery comprehension.
  Mm-spubench: Towards better understanding of spu-        arXiv preprint arXiv:2407.13596.
  rious biases in multimodal llms. arXiv preprint
  arXiv:2406.17126.                                       Yichi Zhang, Yinpeng Dong, Siyuan Zhang, Tianzan
                                                            Min, Hang Su, and Jun Zhu. 2024g. Exploring
Zonghao Ying, Aishan Liu, Tianyuan Zhang, Zheng-            the transferability of visual prompting for multi-
  min Yu, Siyuan Liang, Xianglong Liu, and Dacheng          modal large language models. In Proceedings of
  Tao. 2024.    Jailbreak vision language models            the IEEE/CVF Conference on Computer Vision and
  via bi-modal adversarial prompt. arXiv preprint           Pattern Recognition, pages 26562–26572.
  arXiv:2406.04031.
                                                          Zheng Zhang, Yeyao Ma, Enming Zhang, and Xi-
Jaehong Yoon, Shoubin Yu, and Mohit Bansal. 2024.           ang Bai. 2024h. Psalm: Pixelwise segmentation
   Raccoon: Remove, add, and change video con-              with large multi-modal model. arXiv preprint
   tent with auto-generated narratives. arXiv preprint      arXiv:2403.14598.
   arXiv:2405.18406.
                                                          Wenliang Zhong, Wenyi Wu, Qi Li, Rob Barton, Boxin
Ao Zhang, Hao Fei, Yuan Yao, Wei Ji, Li Li, Zhiyuan         Du, Shioulin Sam, Karim Bouyarmane, Ismail Tu-
  Liu, and Tat-Seng Chua. 2024a. Vpgtrans: Transfer         tar, and Junzhou Huang. 2024. Enhancing multi-
  visual prompt generator across llms. Advances in          modal large language models with multi-instance
  Neural Information Processing Systems, 36.               visual prompt generator for visual representation en-
                                                            richment. arXiv preprint arXiv:2406.02987.
Chaoning Zhang, Fachrina Dewi Puspitasari, Sheng
  Zheng, Chenghao Li, Yu Qiao, Taegoo Kang, Xinru         Enshen Zhou, Yiran Qin, Zhenfei Yin, Yuzhou Huang,
  Shan, Chenshuang Zhang, Caiyan Qin, Francois              Ruimao Zhang, Lu Sheng, Yu Qiao, and Jing Shao.
  Rameau, et al. 2023a. A survey on segment anything        2024a. Minedreamer: Learning to follow instruc-
  model (sam): Vision foundation model meets prompt         tions via chain-of-imagination for simulated-world
  engineering. arXiv preprint arXiv:2306.06211.             control. arXiv preprint arXiv:2403.12037.

Hao Zhang, Feng Li, Xueyan Zou, Shilong Liu, Chun-        Qiji Zhou, Ruochen Zhou, Zike Hu, Panzhong Lu,
  yuan Li, Jianwei Yang, and Lei Zhang. 2023b. A            Siyang Gao, and Yue Zhang. 2024b. Image-of-
  simple framework for open-vocabulary segmentation         thought prompting for visual reasoning refinement in
  and detection. In Proceedings of the IEEE/CVF In-         multimodal large language models. arXiv preprint
  ternational Conference on Computer Vision, pages          arXiv:2405.13872.
  1020–1031.

Jingyi Zhang, Jiaxing Huang, Sheng Jin, and Shijian Lu.
   2024b. Vision-language models for vision tasks: A
   survey. IEEE Transactions on Pattern Analysis and
   Machine Intelligence.

Lu Zhang, Tiancheng Zhao, Heting Ying, Yibo Ma,
  and Kyusong Lee. 2024c. Omagent: A multi-modal
  agent framework for complex video understand-
  ing with task divide-and-conquer. arXiv preprint
  arXiv:2406.16620.

Lvmin Zhang, Anyi Rao, and Maneesh Agrawala.
  2023c. Adding conditional control to text-to-image
  diffusion models. In Proceedings of the IEEE/CVF
