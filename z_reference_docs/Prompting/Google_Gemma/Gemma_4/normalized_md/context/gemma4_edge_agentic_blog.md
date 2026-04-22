# Bring state-of-the-art agentic skills to the edge with Gemma 4
            
            
            - Google Developers Blog

- Raw source: `context/gemma4_edge_agentic_blog.html`
- Normalization note: Trimmed blog-site navigation and preserved the article region.

---
Bring state-of-the-art agentic skills to the edge with Gemma 4 - Google Developers Blog

https://developers.google.com/

[Products](//developers.google.com/products) #

- Develop
-

[Android](//developer.android.com)
-

[Chrome](//developer.chrome.com)
-

[ChromeOS](//chromeos.dev/)
-

[Cloud](//cloud.google.com)
-

[Firebase](//firebase.google.com)
-

[Flutter](//flutter.dev)
-

[Google Assistant](//developers.google.com/assistant)
-

[Google Maps Platform](//developers.google.com/maps)
-

[Google Workspace](//developers.google.com/workspace)
-

[TensorFlow](//www.tensorflow.org)
-

[YouTube](//developers.google.com/youtube)

- Grow
-

[Firebase](//firebase.google.com)
-

[Google Ads](//developers.google.com/google-ads)
-

[Google Analytics](//developers.google.com/analytics)
-

[Google Play](//developer.android.com/distribute)
-

[Search](//developers.google.com/search)
-

[Web Push and Notification APIs](//developers.google.com/web/fundamentals/engage-and-retain/push-notifications)

- Earn
-

[AdMob](//developers.google.com/admob)
-

[Google Ads API](//developers.google.com/google-ads/api)
-

[Google Pay](//developers.google.com/pay)
-

[Google Play Billing](//developer.android.com/google/play/billing/)
-

[Interactive Media Ads](//developers.google.com/interactive-media-ads)

[Solutions](//developers.google.com/solutions/catalog)

[Events](//developers.google.com/events)

[Learn](//developers.google.com/learn)

[Community](//developers.google.com/community) #

- Groups
-

[Google Developer Groups](//developers.google.com/community/gdg)
-

[Google Developer Student Clubs](//developers.google.com/community/gdsc)
-

[Woman Techmakers](//developers.google.com/womentechmakers)
-

[Google Developer Experts](//developers.google.com/community/experts)
-

[Tech Equity Collective](//www.techequitycollective.com/)

- Programs
-

[Accelerator](//developers.google.com/community/accelerators)
-

[Solution Challenge](//developers.google.com/community/gdsc-solution-challenge)
-

[DevFest](//developers.google.com/community/devfest)

- Stories
-

[All Stories](//developers.google.com/community/stories)

[Developer Program](//developers.google.com/profile/u/me)

[Blog](//developers.googleblog.com/)

https://developers.google.com/

- [Products](//developers.google.com/products)

  - More

- [Solutions](//developers.google.com/solutions/catalog)
- [Events](//developers.google.com/events)
- [Learn](//developers.google.com/learn)
- [Community](//developers.google.com/community)

  - More

- [Developer Program](//developers.google.com/profile/u/me)
- [Blog](//developers.googleblog.com/)

- Develop
- [Android](//developer.android.com)
- [Chrome](//developer.chrome.com)
- [ChromeOS](//chromeos.dev/)
- [Cloud](//cloud.google.com)
- [Firebase](//firebase.google.com)
- [Flutter](//flutter.dev)
- [Google Assistant](//developers.google.com/assistant)
- [Google Maps Platform](//developers.google.com/maps)
- [Google Workspace](//developers.google.com/workspace)
- [TensorFlow](//www.tensorflow.org)
- [YouTube](//developers.google.com/youtube)
- Grow
- [Firebase](//firebase.google.com)
- [Google Ads](//developers.google.com/google-ads)
- [Google Analytics](//developers.google.com/analytics)
- [Google Play](//developer.android.com/distribute)
- [Search](//developers.google.com/search)
- [Web Push and Notification APIs](//developers.google.com/web/fundamentals/engage-and-retain/push-notifications)
- Earn
- [AdMob](//developers.google.com/admob)
- [Google Ads API](//developers.google.com/google-ads/api)
- [Google Pay](//developers.google.com/pay)
- [Google Play Billing](//developer.android.com/google/play/billing/)
- [Interactive Media Ads](//developers.google.com/interactive-media-ads)

- Groups
- [Google Developer Groups](//developers.google.com/community/gdg)
- [Google Developer Student Clubs](//developers.google.com/community/gdsc)
- [Woman Techmakers](//developers.google.com/womentechmakers)
- [Google Developer Experts](//developers.google.com/community/experts)
- [Tech Equity Collective](//www.techequitycollective.com/)
- Programs
- [Accelerator](//developers.google.com/community/accelerators)
- [Solution Challenge](//developers.google.com/community/gdsc-solution-challenge)
- [DevFest](//developers.google.com/community/devfest)
- Stories
- [All Stories](//developers.google.com/community/stories)

# Bring state-of-the-art agentic skills to the edge with Gemma 4

APRIL 2, 2026

[Google AI Edge Team](/search/?author=Google+AI+Edge+Team)

- [Facebook](https://www.facebook.com/sharer/sharer.php?u={url})
- [Twitter](https://twitter.com/intent/tweet?text={url})
- [LinkedIn](https://www.linkedin.com/shareArticle?url={url}&mini=true)
- [Mail](mailto:name@example.com?subject=Check%20out%20this%20site&body=Check%20out%20{url})
- #

Today, Google DeepMind launched [Gemma 4](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/), a family of state-of-the-art open models that redefine what is possible on your own hardware. Now available under the Apache 2.0 license, Gemma 4 gives developers a powerful toolkit for on-device AI development. With Gemma 4, you can now go beyond chatbots to build agents and autonomous AI use cases running directly on-device. Gemma 4 enables multi-step planning, autonomous action, offline code generation, and even audio-visual processing, all without specialized fine-tuning. It’s also built for a global audience with support for over 140 languages.

Sorry, your browser doesn't support playback for this video

Gemma 4 enables visual processing and support in >140 languages

We are excited to announce that you can experience Gemma 4’s expansive capabilities on the edge starting today! Access Android's built-in Gemma 4 model through the new [AICore Developer Preview](https://developers.google.com/ml-kit/genai/aicore-dev-preview), or leverage [Google AI Edge](https://ai.google.dev/edge) to build agentic, in-app experiences across mobile, desktop, and edge devices.

In this post, we’ll show you how to get started with Google AI Edge using both [Google AI Edge Gallery](https://github.com/google-ai-edge/gallery) and [LiteRT-LM](https://ai.google.dev/edge/litert-lm/overview).

### Discover Agent Skills with Gemma 4 in Google AI Edge Gallery

Google AI Edge Gallery, available on [iOS](https://apps.apple.com/us/app/google-ai-edge-gallery/id6749645337) and [Android](https://play.google.com/store/apps/details?id=com.google.ai.edge.gallery&hl=en_US), allows you to build and experiment with AI experiences that run entirely on-device. Today, we are thrilled to announce the launch of Agent Skills, one of the first applications to run multi-step, autonomous agentic workflows entirely on-device. Powered by Gemma 4, Agent Skills can:

- Augment the knowledge base: Gemma 4 can access the information beyond its initial training data using skills to enable agentic enrichment type experiences. For example, you can build a skill to query Wikipedia, allowing the agent to query and respond to any encyclopedic question.

Sorry, your browser doesn't support playback for this video

Query Wikipedia or other knowledge sources

- Produce rich, interactive content: Transform paragraphs or videos into concise summaries or flashcards for studying, or transform data into interactive visualizations or graphs. For example, you can create a skill that automatically summarizes and displays trends in hours of sleep and moods per day based on user speech input:

Sorry, your browser doesn't support playback for this video

Create graphs, flashcards, and other visualizations

- Expand Gemma 4's core capabilities: Integrate with other models, such as text-to-speech, image generation, or music synthesis. For instance, you can utilize skills to pair photos with music that perfectly matches the mood.

Sorry, your browser doesn't support playback for this video

Integrate with other models to synthesize music and understand images

- Create comprehensive end-to-end experiences: Rather than navigating multiple apps, users can manage complex workflows and build their own applications entirely through conversation with Gemma 4. To illustrate this, we built a working app that describes and plays the vocal calls of animals.

Sorry, your browser doesn't support playback for this video

Build multi-step workflows and end-to-end experiences

To experience the Gemma 4 E2B and E4B models in action, check out the [Google AI Edge Gallery app](https://github.com/google-ai-edge/gallery) today. Within the app, it’s easy to start experimenting and creating your own skills with [our guide](https://github.com/google-ai-edge/gallery/tree/main/skills). We can’t wait to see what you build and share your skills in the Github [Discussion](https://github.com/google-ai-edge/gallery/discussions/categories/skills)!

### Leverage Gemma 4 across devices with LiteRT-LM

For developers who are interested in deploying Gemma 4 in-app or across a broader range of devices, [LiteRT-LM](https://ai.google.dev/edge/litert-lm/overview) provides stellar performance with reach across the entire hardware spectrum. LiteRT-LM adds GenAI specific libraries on top of [LiteRT](https://ai.google.dev/edge/litert), which is already trusted by millions of Android and edge developers with its high-performance libraries XNNPack and ML Drift. LiteRT-LM builds on this stack and enhances model performance with the following new features:

- Minimal Memory footprint: Run Gemma 4 E2B using <1.5GB memory on some devices thanks to LiteRT’s support for 2-bit and 4-bit weights along with memory-mapped per-layer embeddings
- Constrained decoding: Get structured, predictable outputs every time, ensuring your AI-driven apps and tool-calling scripts remain reliable in production.
- Dynamic context: Flexibility to handle single models across CPUs and GPUs with dynamic context lengths, allowing you to take full advantage of the Gemma 4 128K context window.

To support the extended context lengths required by agentic use cases, LiteRT-LM leverages cutting-edge GPU optimizations to process 4,000 input tokens across 2 distinct skills in under 3 seconds.

LiteRT-LM also brings smaller Gemma 4 models to IoT & edge devices with compelling performance on a variety of platforms. These include the Raspberry Pi 5, where running on CPU, it reaches 133 prefill and 7.6 decode tokens/s, while the NPU acceleration on the Qualcomm Dragonwing IQ8 boosts performance to a more impressive 3,700 prefill and 31 decode tokens/s.

Ready to get started? Check out the [LiteRT-LM documentation](https://ai.google.dev/edge/litert-lm/overview) for a complete guide and device-specific performance metrics. You can also view the individual model cards for [Gemma 4 E2B](https://huggingface.co/litert-community/gemma-4-E2B-it-litert-lm) and [Gemma 4 E4B](https://huggingface.co/litert-community/gemma-4-E4B-it-litert-lm).

### Run on any device

Gemma 4 is available today with support across an unprecedented range of platforms:

- Mobile: Available with CPU/GPU support across both Android and iOS. Developers can also access and deploy Android's built-in and optimized Gemma 4 model system-wide via Android AICore.
- Desktop and Web: Seamless performance on Windows, Linux, and macOS (via Metal), plus native browser-based execution powered by WebGPU.
- IoT and robotics: We are bringing Gemma 4 to the edge on Raspberry Pi 5 and Qualcomm Dragonwing IQ8 processor, which also powers [Arduino VENTUNO Q](https://www.qualcomm.com/news/releases/2026/03/arduino-announces-arduino-ventuno-q----powered-by-qualcomm-drago).

Today, we are also launching a new Python package and CLI tool to make it easier than ever to experiment with Gemma in the console, and to power Gemma-based Python pipelines for IoT devices. The`litert-lm`CLI is available on Linux, macOS, and Raspberry Pi, enabling developers to try out the latest Gemma 4 model capabilities without writing any code. The CLI now also supports tool calling that powered Agent Skills in Google AI Edge Gallery. Python bindings for LiteRT-LM provide the flexibility to deeply customize your on-device LLM pipeline from Python. Getting started with LiteRT-LM in your terminal is simple using our [guide](http://ai.google.dev/edge/litert-lm/cli).

The era of agentic experiences on-device is here, and we hope you are excited to start building on the edge. Regardless of which device you are building on, get started with our [Agent Skills examples](https://github.com/google-ai-edge/gallery/tree/main/skills) in Google AI Edge Gallery, and [LiteRT-LM getting started guide](https://ai.google.dev/edge/litert-lm/overview). We can’t wait to see what you build!

### Acknowledgements

We'd like to extend a special thanks to our significant contributors for their work on this project:

Advait Jain, Alice Zheng, Amber Heinbockel, Andrew Zhang, Byungchul Kim, Cormac Brick, Daniel Ho, Derek Bekebrede, Dillon Sharlet, Eric Yang, Fengwu Yao, Frank Barchard, Grant Jensen, Hriday Chhabria, Jae Yoo, Jenn Lee, Jing Jin, Jingxiao Zheng, Juhyun Lee, Lu Wang, Lin Chen, Majid Dadashi, Marissa Ikonomidis, Matthew Chan, Matthew Soulanille, Matthias Grundmann, Milen Ferev, Misha Gutman, Mohammadreza Heydary, Pradeep Kuppala, Qidong Zhao, Quentin Khan, Ram Iyengar, Raman Sarokin, Renjie Wu, Rishika Sinha, Rodney Witcher, Ronghui Zhu, Sachin Kotwani, Suleman Shahid, Tenghui Zhu, Terry Heo, Tiffany Hsiao, Tyler Mullen, Wai Hon Law, Weiyi Wang, Xiaoming Hu, Xu Chen, Yishuang Pang, Yi-Chun Kuo, Yu-Hui Chen, Zichuan Wei, and the gTech team.

posted in:

- [Mobile](/search/?technology_categories=Mobile)
- [Web](/search/?technology_categories=Web)
- [AI](/search/?technology_categories=AI)
- [Announcements](/search/?content_type_categories=Announcements)
- [Explore](/search/?tag=Explore)
- [Learn](/search/?tag=Learn)

/subagents-have-arrived-in-gemini-cli/ Previous

Next/closing-the-knowledge-gap-with-agent-skills/

Related Posts

[MobileWebHow-To GuidesAnnouncementsA2UI v0.9: The New Standard for Portable, Framework-Agnostic Generative UIAPRIL 17, 2026](/a2ui-v0-9-generative-ui/)

[PayMobileWebTutorialsAnnouncementsNew enhancements for merchant initiated transactions with the Google Pay APIAPRIL 15, 2026](/new-enhancements-for-merchant-initiated-transactions-with-the-google-pay-api/)

[AICloudAnnouncementsMaxText Expands Post-Training Capabilities: Introducing SFT and RL on Single-Host TPUsAPRIL 16, 2026](/maxtext-expands-post-training-capabilities-introducing-sft-and-rl-on-single-host-tpus/)

- Connect

  - [Blog](//googledevelopers.blogspot.com)
  - [Bluesky](https://goo.gle/3FReQXN)
  - [Instagram](https://goo.gle/googlefordevs)
  - [LinkedIn](https://goo.gle/gdevs-li)
  - [X (Twitter)](https://goo.gle/gdevs-tw)
  - [YouTube](https://goo.gle/developers)

- Programs

  - [Google Developer Program](//developers.google.com/program)
  - [Google Developer Groups](//developers.google.com/community/gdg)
  - [Google Developer Experts](//developers.google.com/community/experts)
  - [Accelerators](//developers.google.com/community/accelerators)
  - [Women Techmakers](//www.womentechmakers.com)
  - [Google Cloud & NVIDIA](//developers.google.com/community/nvidia)

- Developer consoles

  - [Google API Console](//console.developers.google.com)
  - [Google Cloud Platform Console](//console.cloud.google.com)
  - [Google Play Console](//play.google.com/apps/publish)
  - [Firebase Console](//console.firebase.google.com)
  - [Actions on Google Console](//console.actions.google.com)
  - [Cast SDK Developer Console](//cast.google.com/publish)
  - [Chrome Web Store Dashboard](//chrome.google.com/webstore/developer/dashboard)
  - [Google Home Developer Console](//console.home.google.com/)

https://developers.google.com/

- [Android](//developer.android.com)
- [Chrome](//developer.chrome.com/home)
- [Firebase](//firebase.google.com)
- [Google Cloud Platform](//cloud.google.com)
- [All products](//developers.google.com/products)
-

- [Terms](//developers.google.com/terms/site-terms)
- [Privacy](//policies.google.com/privacy)
