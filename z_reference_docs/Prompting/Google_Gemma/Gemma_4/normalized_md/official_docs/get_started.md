# Get started with Gemma models  |  Google AI for Developers

- Raw source: `official_docs/get_started.html`
- Source URL: https://ai.google.dev/gemma/docs/get_started
- Normalization note: Trimmed Google DevSite navigation and preserved the main article region.

---
# Get started with Gemma models

The Gemma family of open models includes a range of model sizes, capabilities, and task-specialized variations to help you build custom generative solutions. These are the main paths you can follow when using Gemma models in an application:

- Select a model and deploy it as-is in your application
- Select a model, tune it for a specific task, and then deploy it in an application, or share it with the community.

This guide helps you get started with [picking](#pick) a model, [testing](#test) its capabilities, and optionally, [tuning](#tune) the model you selected for your application.

Tip: As you begin implementing AI applications, make sure you are following a principled approach to AI that serves all your users with the [Responsible Generative AI Toolkit](/responsible).

[Get it on Kaggle](https://www.kaggle.com/models/google/gemma-4) [Get it on Hugging Face](https://huggingface.co/collections/google/gemma-4)

## Pick a model

This section helps you understand the official variants of the Gemma model family and select a model for your application. The model variants provide general capabilities or are specialized for specific tasks, and are provided in different parameter sizes so you can pick a model that has your preferred capabilities and meets your compute requirements.

Tip: A good place to start is the [Gemma 4 26B A4B](https://www.kaggle.com/models/google/gemma-4) model in the latest available version, which can be used for many tasks and has lower resource requirements.

The following table lists the major variants of the Gemma model family and their intended deployment platforms:

### Gemma 4 Family

The latest generation featuring multimodal (text, image, audio) inputs.

| Size | Variant | Input ➔ Output | Intended Platform |

| E2B | [Gemma 4 (core)](/gemma/docs/core) | Text, images, audio ➔ Text | Mobile devices |

| E4B | [Gemma 4 (core)](/gemma/docs/core) | Text, images, audio ➔ Text | Mobile devices and laptops |

| A4B | [Gemma 4 (core)](/gemma/docs/core) | Text, images ➔ Text | Desktop computers and small servers |

| 31B | [Gemma 4 (core)](/gemma/docs/core) | Text, images ➔ Text | Large servers or server clusters |

### Gemma 3 & 3n Family

Core models for scalable text and image processing, plus '3n' variants for expanded multimodal inputs.

| Size | Variant | Input ➔ Output | Intended Platform |

| 270M | [Gemma 3 (core)](/gemma/docs/core) | Text ➔ Text | Mobile devices and single board computers |

| 1B | [Gemma 3 (core)](/gemma/docs/core) | Text ➔ Text | Mobile devices and single board computers |

| E2B | [Gemma 3n](/gemma/docs/gemma-3n) | Text, images, audio ➔ Text | Mobile devices |

| 4B | [Gemma 3 (core)](/gemma/docs/core) | Text, images ➔ Text | Desktop computers and small servers |

| E4B | [Gemma 3n](/gemma/docs/gemma-3n) | Text, images, audio ➔ Text | Mobile devices and laptops |

| 12B | [Gemma 3 (core)](/gemma/docs/core) | Text, images ➔ Text | Higher-end desktop computers and servers |

| 27B | [Gemma 3 (core)](/gemma/docs/core) | Text, images ➔ Text | Large servers or server clusters |

### Gemma 2 Family

Includes standard text models and the PaliGemma 2 multimodal vision-language variants.

| Size | Variant | Input ➔ Output | Intended Platform |

| 2B | [Gemma 2 (core)](/gemma/docs/core) | Text ➔ Text | Mobile devices and laptops |

| 3B | [PaliGemma 2](/gemma/docs/paligemma) | Text, images ➔ Text | Desktop computers and small servers |

| 9B | [Gemma 2 (core)](/gemma/docs/core) | Text ➔ Text | Higher-end desktop computers and servers |

| 10B | [PaliGemma 2](/gemma/docs/paligemma) | Text, images ➔ Text | Higher-end desktop computers and servers |

| 27B | [Gemma 2 (core)](/gemma/docs/core) | Text ➔ Text | Large servers or server clusters |

| 28B | [PaliGemma 2](/gemma/docs/paligemma) | Text, images ➔ Text | Large servers or server clusters |

### Gemma 1 Family

The original generation, including coding-specific variants.

| Size | Variant | Input ➔ Output | Intended Platform |

| 2B | [Gemma (core)](/gemma/docs/core)
[CodeGemma](/gemma/docs/codegemma) | Text ➔ Text | Mobile devices and laptops |

| 7B | [Gemma (core)](/gemma/docs/core)
[CodeGemma](/gemma/docs/codegemma) | Text ➔ Text | Desktop computers and small servers |

The Gemma family of models also includes special-purpose and research models, including [ShieldGemma](/gemma/docs/shieldgemma), [DataGemma](/gemma/docs/datagemma), [Gemma Scope](/gemma/docs/gemmascope), and [Gemma-APS](/gemma/docs/gemma-aps).

Tip: You can download official Google Gemma model variants and community-created variants from [Kaggle Models](https://www.kaggle.com/models?query=gemma) and [Hugging Face](https://huggingface.co/models?search=google/gemma).

## Test models

You can test Gemma models by setting up a development environment with a downloaded model and supporting software. You can then prompt the model and evaluate its responses. Use one of the following Python notebooks with your preferred machine learning framework to set up a testing environment and prompt a Gemma model:

- [Inference with Keras](https://ai.google.dev/gemma/docs/core/keras_inference)
- [Inference with PyTorch](https://ai.google.dev/gemma/docs/core/pytorch_gemma)
- [Inference with Gemma library](https://ai.google.dev/gemma/docs/core/gemma_library)

## Tune models

You can change the behavior of Gemma models by performing tuning on them. Tuning a model requires a dataset of inputs and expected responses of sufficient size and variation to guide the behavior of the model. You also need significantly more computing and memory resources to complete a tuning run compared to running a Gemma model for text generation. Use one of the following Python notebooks to set up a tuning development environment and tune a Gemma model:

- [Tune Gemma with Keras and LoRA tuning](https://ai.google.dev/gemma/docs/core/lora_tuning)
- [Tune larger Gemma models with distributed training](https://ai.google.dev/gemma/docs/core/distributed_tuning)

## Next Steps

Check out these guides for building more solutions with Gemma:

- [Create a chatbot with Gemma](https://ai.google.dev/gemma/docs/gemma_chat)
- [Deploy Gemma to production with Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/open-models/use-gemma)
- [Use Genkit with Ollama and Gemma](https://genkit.dev/docs/integrations/ollama/)

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-16 UTC.

- [Terms](//policies.google.com/terms)
- [Privacy](//policies.google.com/privacy)
- [Manage cookies](#)

- English
- Deutsch
- Español – América Latina
- Français
- Indonesia
- Italiano
- Polski
- Português – Brasil
- Shqip
- Tiếng Việt
- Türkçe
- Русский
- עברית
- العربيّة
- فارسی
- हिंदी
- বাংলা
- ภาษาไทย
- 中文 – 简体
- 中文 – 繁體
- 日本語
- 한국어
