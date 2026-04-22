# Run Gemma with Hugging Face Transformers

- Raw source: `cookbooks/huggingface_inference.ipynb`
- Source URL: https://ai.google.dev/gemma/docs/core/huggingface_inference
- Normalization note: Notebook cells were preserved in order. Markdown and code were kept as-is where possible; only notebook JSON wrappers were removed.

---

##### Copyright 2025 Google LLC.

## Code Cell 1

```python
#@title Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# https://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
```

# Run Gemma with Hugging Face Transformers

<table class="tfo-notebook-buttons" align="left">
  <td>
    <a target="_blank" href="https://ai.google.dev/gemma/docs/core/huggingface_inference"><img src="https://ai.google.dev/static/site-assets/images/docs/notebook-site-button.png" height="32" width="32" />View on ai.google.dev</a>
  </td>
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/google-gemma/cookbook/blob/main/docs/core/huggingface_inference.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
  </td>
  <td>
    <a target="_blank" href="https://kaggle.com/kernels/welcome?src=https://github.com/google-gemma/cookbook/blob/main/docs/core/huggingface_inference.ipynb"><img src="https://www.kaggle.com/static/images/logos/kaggle-logo-transparent-300.png" height="32" width="70"/>Run in Kaggle</a>
  </td>
  <td>
    <a target="_blank" href="https://console.cloud.google.com/vertex-ai/colab/import/https%3A%2F%2Fraw.githubusercontent.com%2Fgoogle-gemma%2Fcookbook%2Fmain%2Fdocs%2Fcore%2Fhuggingface_inference.ipynb"><img src="https://ai.google.dev/images/cloud-icon.svg" width="40" />Open in Vertex AI</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/google-gemma/cookbook/blob/main/docs/core/huggingface_inference.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View source on GitHub</a>
  </td>
</table>

Generating text, summarizing, and analysing content are just some of the tasks you can accomplish with Gemma open models. This tutorial shows you how to get started running Gemma using Hugging Face Transformers using both text and image input to generate text content. The Transformers Python library provides a API for accessing pre-trained generative AI models, including Gemma. For more information, see the [Transformers](https://huggingface.co/docs/transformers/en/index) documentation.

Note: Gemma 3 and later models support input of both images and text. Earlier versions of Gemma only support text input, except for some variants, including [PaliGemma](https://ai.google.dev/gemma/docs/setup).

### Install Python packages

Install the Hugging Face libraries required for running the Gemma model and making requests.

## Code Cell 2

```python
# Install Pytorch
%pip install torch

# Install a transformers
%pip install transformers
```

## Generate text from text

Prompting a Gemma model with text to get a text response is the simplest way to use Gemma and works with nearly all Gemma variants. This section shows how to use the Hugging Face Transformers library load and configure a Gemma model for text to text generation.

### Load model

Use the `torch` and `transformers` libraries to create an instance of a model execution `pipeline` class with Gemma. When using a model for generating output or following directions, select an instruction tuned (IT) model, which typically has `it` in the model ID string. Using the `pipeline` object, you specify the Gemma variant you want to use, the type of task you want to perform, specifically `"any-to-any"` for multimodal generation, as shown in the following code example:

## Code Cell 3

```python
from transformers import pipeline

MODEL_ID = "google/gemma-4-E2B-it"

pipe = pipeline(
    task="any-to-any",
    model=MODEL_ID,
    device_map="auto",
    dtype="auto"
)
```

**Outputs**

```text
config.json: 0.00B [00:00, ?B/s]

model.safetensors:   0%|          | 0.00/10.2G [00:00<?, ?B/s]

Loading weights:   0%|          | 0/2011 [00:00<?, ?it/s]

generation_config.json:   0%|          | 0.00/208 [00:00<?, ?B/s]

processor_config.json: 0.00B [00:00, ?B/s]

chat_template.jinja: 0.00B [00:00, ?B/s]

tokenizer_config.json: 0.00B [00:00, ?B/s]

tokenizer.json:   0%|          | 0.00/32.2M [00:00<?, ?B/s]
```

Gemma supports only a few `task` settings for generation. For more information on the available `task` settings, see the Hugging Face Pipelines [task()](https://huggingface.co/docs/transformers/main/en/main_classes/pipelines#transformers.pipeline.task) documentation. For more information about using the Pipeline class, see the Hugging Face [Pipelines](https://huggingface.co/docs/transformers/main/en/main_classes/pipelines) documentation.

### Run text generation

Once you have the Gemma model loaded and configured in a `pipeline` object, you can send prompts to the model. The following example code shows a basic request using the `text` parameter:

## Code Cell 4

```python
pipe(text="<|turn>user\nroses are red<turn|>\n<|turn>model\n")
```

**Outputs**

```text
Both `max_new_tokens` (=256) and `max_length`(=20) seem to have been set. `max_new_tokens` will take precedence. Please refer to the documentation for more information. (https://huggingface.co/docs/transformers/main/en/main_classes/text_generation)

[{'input_text': '<|turn>user\nroses are red<turn|>\n<|turn>model\n',
  'generated_text': '<|turn>user\nroses are red<turn|>\n<|turn>model\nThat\'s a classic phrase, often used to highlight a contrast or a truth.\n\n**"Roses are red"** is a very popular, simple, and sweet arrangement.\n\nWhat would you like to do with this phrase? Are you looking for:\n\n1. **More rhymes or phrases?**\n2. **A continuation of a thought?**\n3. **Just appreciating the simplicity?**'}]
```

### Use a prompt template

When generating content with more complex prompting, use a prompt template to structure your request. A prompt template allows you to specify input from specific roles, such as `user` or `model`, and is a required format for managing multi-turn chat interactions with Gemma models. The following example code shows how to constuct a prompt template for Gemma:

## Code Cell 5

```python
from transformers import GenerationConfig
config = GenerationConfig.from_pretrained(MODEL_ID)
config.max_new_tokens = 512
gen_kwargs = dict(generation_config=config)

messages = [
    {
        "role": "system",
        "content": [{"type": "text", "text": "You are a helpful assistant."}]
    },
    {
        "role": "user",
        "content": [{"type": "text", "text": "Roses are red..."}]
    },
]

pipe(messages, return_full_text=False, generate_kwargs=gen_kwargs)
```

**Outputs**

```text
[{'input_text': [{'role': 'system',
    'content': [{'type': 'text', 'text': 'You are a helpful assistant.'}]},
   {'role': 'user',
    'content': [{'type': 'text', 'text': 'Roses are red...'}]}],
  'generated_text': 'Roses are red,\nViolets are blue,\nHow lovely to see\nA beautiful view.'}]
```

<a name="vision"></a>
## Generate text from image data

Starting with Gemma 3, for model sizes 4B and higher, you can use image data as part of your prompt. This section shows how to use the Transformers library to load and configure a Gemma model to use image data and text input to generate text output.

### Use a prompt template

When generating content with more complex prompting, use a prompt template to structure your request. A prompt template allows you to specify input from specific roles, such as `user` or `model`, and is a required format for managing multi-turn chat interactions with Gemma models. The following example code shows how to constuct a prompt template for Gemma:

## Code Cell 6

```python
from transformers import GenerationConfig
config = GenerationConfig.from_pretrained(MODEL_ID)
config.max_new_tokens = 512
gen_kwargs = dict(generation_config=config)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://ai.google.dev/static/gemma/docs/images/thali-indian-plate.jpg"},
            {"type": "text", "text": "What is shown in this image?"},
        ]
    },
    {
        "role": "assistant",
        "content": [
            {"type": "text", "text": "This image shows"},
        ],
    },
]

pipe(text=messages, return_full_text=False, generate_kwargs=gen_kwargs)
```

**Outputs**

```text
[{'input_text': [{'role': 'user',
    'content': [{'type': 'image',
      'url': 'https://ai.google.dev/static/gemma/docs/images/thali-indian-plate.jpg'},
     {'type': 'text', 'text': 'What is shown in this image?'}]},
   {'role': 'assistant',
    'content': [{'type': 'text', 'text': 'This image shows'}]}],
  'generated_text': " a platter of Indian food, likely a meal or an assortment of dishes.\n\nHere's a breakdown of what is visible:\n\n*   **Flatbread:** There is a large, golden-brown flatbread (possibly naan or roti) dominating the center of the platter.\n*   **Dips/Sides:** There are several small bowls containing various accompaniments:\n    *   A bowl of **yellow/mustard-colored dip** (perhaps a chutney or sauce).\n    *   A bowl of **white creamy dip** (like raita or yogurt sauce).\n    *   A portion of **white rice**.\n    *   Several bowls of **curries or sauces** in different colors:\n        *   An **orange/brown curry**.\n        *   A **deep yellow/orange sauce**.\n        *   A **green sauce** (likely a chutney).\n*   **Garnish/Side Item:** In the upper right corner, there appears to be some darker, textured items, possibly fried pieces or spices.\n*   **Platter:** The food is served on a metal platter.\n\nOverall, it looks like a traditional Indian meal setup featuring bread, rice, and various flavorful sauces/curries."}]
```

You can include multiple images in your prompt by including additional `"type": "image",` entries in the `content` list.

> Note: Do not use `<|image|>`, `<start_of_image>` or `<image_soft_token>` tokens in text portion of a prompt template as this approach creates redundant tokens and processing errors.

<a name="audio"></a>
## Generate text from audio data

With [Gemma 4](https://ai.google.dev/gemma/docs/gemma-4) and [Gemma 3n](https://ai.google.dev/gemma/docs/gemma-3n), you can use audio data as part of your prompt. This section shows how to use the Transformers library to load and configure a Gemma model to use audio data and text input to generate text output.

### Use a prompt template

When generating content with audio, use a prompt template to structure your request. A prompt template allows you to specify input from specific roles, such as `user` or `model`, and is a required format for managing multi-turn chat interactions with Gemma models. The following example code shows how to constuct a prompt template for Gemma with audio data input:

## Code Cell 7

```python
from transformers import GenerationConfig
config = GenerationConfig.from_pretrained(MODEL_ID)
config.max_new_tokens = 512
gen_kwargs = dict(generation_config=config)

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Transcribe the following speech segment in its original language. Follow these specific instructions for formatting the answer:\n* Only output the transcription, with no newlines.\n* When transcribing numbers, write the digits, i.e. write 1.7 and not one point seven, and write 3 instead of three."},
            {"type": "audio", "audio": "https://ai.google.dev/gemma/docs/audio/roses-are.wav"},
        ]
    }
]

pipe(text=messages, return_full_text=False, generate_kwargs=gen_kwargs)
```

**Outputs**

```text
[{'input_text': [{'role': 'user',
    'content': [{'type': 'text',
      'text': 'Transcribe the following speech segment in its original language. Follow these specific instructions for formatting the answer:\n* Only output the transcription, with no newlines.\n* When transcribing numbers, write the digits, i.e. write 1.7 and not one point seven, and write 3 instead of three.'},
     {'type': 'audio',
      'audio': 'https://ai.google.dev/gemma/docs/audio/roses-are.wav'}]}],
  'generated_text': 'Roses are red, violets are blue.'}]
```

You can include multiple audio files in your prompt by including additional `"type": "audio",` entries in the `content` list.

> Note: Do not use `<|audio|>` or `<audio_soft_token>` tokens in text portion of a prompt template as this approach creates redundant tokens and processing errors.

## Next steps

Build and explore more with Gemma models:

* [Fine-tune Gemma for text tasks using Hugging Face Transformers](https://ai.google.dev/gemma/docs/core/huggingface_text_finetune_qlora)
* [Fine-tune Gemma for vision tasks using Hugging Face Transformers](https://ai.google.dev/gemma/docs/core/huggingface_vision_finetune_qlora)
* [Perform distributed fine-tuning and inference on Gemma models](https://ai.google.dev/gemma/docs/core/distributed_tuning)
* [Use Gemma open models with Vertex AI](https://cloud.google.com/vertex-ai/docs/generative-ai/open-models/use-gemma)
* [Fine-tune Gemma using Keras and deploy to Vertex AI](https://github.com/GoogleCloudPlatform/vertex-ai-samples/blob/main/notebooks/community/model_garden/model_garden_gemma_kerasnlp_to_vertexai.ipynb)
