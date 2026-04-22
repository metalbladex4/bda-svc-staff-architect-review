# Run Gemma using PyTorch

- Raw source: `cookbooks/pytorch_gemma.ipynb`
- Source URL: https://ai.google.dev/gemma/docs/core/pytorch_gemma
- Normalization note: Notebook cells were preserved in order. Markdown and code were kept as-is where possible; only notebook JSON wrappers were removed.

---

<link rel="stylesheet" href="/site-assets/css/gemma.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Google+Symbols:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />

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

<table class="tfo-notebook-buttons" align="left">
  <td>
    <a target="_blank" href="https://ai.google.dev/gemma/docs/core/pytorch_gemma"><img src="https://ai.google.dev/static/site-assets/images/docs/notebook-site-button.png" height="32" width="32" />View on ai.google.dev</a>
  </td>
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/google-gemini/gemma-cookbook/blob/main/docs/core/pytorch_gemma.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
  </td>
  <td>
    <a target="_blank" href="https://kaggle.com/kernels/welcome?src=https://github.com/google-gemini/gemma-cookbook/blob/main/docs/core/pytorch_gemma.ipynb"><img src="https://www.kaggle.com/static/images/logos/kaggle-logo-transparent-300.png" height="32" width="70"/>Run in Kaggle</a>
  </td>
  <td>
    <a target="_blank" href="https://console.cloud.google.com/vertex-ai/colab/import/https%3A%2F%2Fraw.githubusercontent.com%2Fgoogle-gemini%2Fgemma-cookbook%2Fmain%2Fdocs%2Fcore%2Fpytorch_gemma.ipynb"><img src="https://ai.google.dev/images/cloud-icon.svg" width="40" />Open in Vertex AI</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/google-gemini/gemma-cookbook/blob/main/docs/core/pytorch_gemma.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View source on GitHub</a>
  </td>
</table>

# Run Gemma using PyTorch

This guide shows you how to run Gemma using the PyTorch framework, including how
to use image data for prompting Gemma release 3 and later models. For more
details on the Gemma PyTorch implementation, see the project repository
[README](https://github.com/google/gemma_pytorch).

## Setup

The following sections explain how to set up your development environment,
including how get access to Gemma models for downloading from Kaggle, setting
authentication variables, installing dependencies, and importing packages.

### System requirements

This Gemma Pytorch library requires GPU or TPU processors to run the Gemma
model. The standard Colab CPU Python runtime and T4 GPU Python runtime are
sufficient for running Gemma 1B, 2B, and 4B size models. For advanced use cases
for other GPUs or TPU, please refer to the
[README](https://github.com/google/gemma_pytorch/blob/main/README.md) in the
Gemma PyTorch repo.

### Get access to Gemma on Kaggle

To complete this tutorial, you first need to follow the setup instructions at
[Gemma setup](https://ai.google.dev/gemma/docs/setup), which show you how to do
the following:

* Get access to Gemma on [Kaggle](https://www.kaggle.com/models/google/gemma/).
* Select a Colab runtime with sufficient resources to run the Gemma model.
* Generate and configure a Kaggle username and API key.

After you've completed the Gemma setup, move on to the next section, where
you'll set environment variables for your Colab environment.

### Set environment variables

Set environment variables for `KAGGLE_USERNAME` and `KAGGLE_KEY`. When prompted
with the "Grant access?" messages, agree to provide secret access.

## Code Cell 2

```python
import os
from google.colab import userdata # `userdata` is a Colab API.

os.environ["KAGGLE_USERNAME"] = userdata.get('KAGGLE_USERNAME')
os.environ["KAGGLE_KEY"] = userdata.get('KAGGLE_KEY')
```

### Install dependencies

## Code Cell 3

```python
!pip install -q -U torch immutabledict sentencepiece
```

**Outputs**

```text
[2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m797.2/797.2 MB[0m [31m1.8 MB/s[0m eta [36m0:00:00[0m
[2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m664.8/664.8 MB[0m [31m2.6 MB/s[0m eta [36m0:00:00[0m
[2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m209.4/209.4 MB[0m [31m6.0 MB/s[0m eta [36m0:00:00[0m
[2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m1.3/1.3 MB[0m [31m51.4 MB/s[0m eta [36m0:00:00[0m
[2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m21.3/21.3 MB[0m [31m55.8 MB/s[0m eta [36m0:00:00[0m
[?25h[31mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
fastai 2.7.15 requires torch<2.4,>=1.10, but you have torch 2.4.0 which is incompatible.
torchaudio 2.3.1+cu121 requires torch==2.3.1, but you have torch 2.4.0 which is incompatible.
torchvision 0.18.1+cu121 requires torch==2.3.1, but you have torch 2.4.0 which is incompatible.[0m[31m
[0m
```

### Download model weights

## Code Cell 4

```python
# Choose variant and machine type
VARIANT = '4b-it'  #@param ['1b','1b-it','4b','4b-it','12b','12b-it','27b','27b-it']
MACHINE_TYPE = 'cuda' #@param ['cuda', 'cpu']
CONFIG = VARIANT.split('-')[0]
```

## Code Cell 5

```python
import kagglehub

# Load model weights
weights_dir = kagglehub.model_download(f'google/gemma-3/pyTorch/gemma-3-{VARIANT}')
```

Set the tokenizer and checkpoint paths for the model.

## Code Cell 6

```python
# Ensure that the tokenizer is present
tokenizer_path = os.path.join(weights_dir, 'tokenizer.model')
assert os.path.isfile(tokenizer_path), 'Tokenizer not found!'

# Ensure that the checkpoint is present
ckpt_path = os.path.join(weights_dir, f'model.ckpt')
assert os.path.isfile(ckpt_path), 'PyTorch checkpoint not found!'
```

## Configure the run environment

The following sections explain how to prepare a PyTorch environment for running
Gemma.

### Prepare the PyTorch run environment

Prepare the PyTorch model execution environment by cloning the Gemma Pytorch
repository.

## Code Cell 7

```python
!git clone https://github.com/google/gemma_pytorch.git
```

**Outputs**

```text
Cloning into 'gemma_pytorch'...
remote: Enumerating objects: 239, done.[K
remote: Counting objects: 100% (123/123), done.[K
remote: Compressing objects: 100% (68/68), done.[K
remote: Total 239 (delta 86), reused 58 (delta 55), pack-reused 116[K
Receiving objects: 100% (239/239), 2.18 MiB | 20.83 MiB/s, done.
Resolving deltas: 100% (135/135), done.
```

## Code Cell 8

```python
import sys

sys.path.append('gemma_pytorch/gemma')
```

## Code Cell 9

```python
from gemma_pytorch.gemma.config import get_model_config
from gemma_pytorch.gemma.gemma3_model import Gemma3ForMultimodalLM

import os
import torch
```

### Set the model configuration

Before you run the model, you must set some configuration parameters, including
the Gemma variant, tokenizer and quantization level.

## Code Cell 10

```python
# Set up model config.
model_config = get_model_config(CONFIG)
model_config.dtype = "float32" if MACHINE_TYPE == "cpu" else "float16"
model_config.tokenizer = tokenizer_path
```

### Configure the device context

The following code configures the device context for running the model:

## Code Cell 11

```python
@contextlib.contextmanager
def _set_default_tensor_type(dtype: torch.dtype):
    """Sets the default torch dtype to the given dtype."""
    torch.set_default_dtype(dtype)
    yield
    torch.set_default_dtype(torch.float)
```

### Instantiate and load the model

Load the model with its weights to prepare to run requests.

## Code Cell 12

```python
device = torch.device(MACHINE_TYPE)
with _set_default_tensor_type(model_config.get_dtype()):
    model = Gemma3ForMultimodalLM(model_config)
    model.load_state_dict(torch.load(ckpt_path)['model_state_dict'])
    model = model.to(device).eval()
print("Model loading done.")

print('Generating requests in chat mode...')
```

## Run inference

Below are examples for generating in chat mode and generating with multiple
requests.

The instruction-tuned Gemma models were trained with a specific formatter that
annotates instruction tuning examples with extra information, both during
training and inference. The annotations (1) indicate roles in a conversation,
and (2) delineate turns in a conversation.

The relevant annotation tokens are:

- `user`: user turn
- `model`: model turn
- `<start_of_turn>`: beginning of dialog turn
- `<start_of_image>`: tag for image data input
- `<end_of_turn><eos>`: end of dialog turn

For more information, read about prompt formatting for instruction tuned Gemma
models [here](https://ai.google.dev/gemma/core/prompt-structure).

### Generate text with text

The following is a sample code snippet demonstrating how to format a prompt for
an instruction-tuned Gemma model using user and model chat templates in a
multi-turn conversation.

## Code Cell 13

```python
# Chat templates
USER_CHAT_TEMPLATE = "<start_of_turn>user\n{prompt}<end_of_turn><eos>\n"
MODEL_CHAT_TEMPLATE = "<start_of_turn>model\n{prompt}<end_of_turn><eos>\n"

# Sample formatted prompt
prompt = (
    USER_CHAT_TEMPLATE.format(
        prompt='What is a good place for travel in the US?'
    )
    + MODEL_CHAT_TEMPLATE.format(prompt='California.')
    + USER_CHAT_TEMPLATE.format(prompt='What can I do in California?')
    + '<start_of_turn>model\n'
)
print('Chat prompt:\n', prompt)

model.generate(
    USER_CHAT_TEMPLATE.format(prompt=prompt),
    device=device,
    output_len=256,
)
```

**Outputs**

```text
Chat prompt:
 <start_of_turn>user
What is a good place for travel in the US?<end_of_turn><eos>
<start_of_turn>model
California.<end_of_turn><eos>
<start_of_turn>user
What can I do in California?<end_of_turn><eos>
<start_of_turn>model

"California is a state brimming with diverse activities! To give you a great list, tell me: \n\n* **What kind of trip are you looking for?** Nature, City life, Beach, Theme Parks, Food, History, something else? \n* **What are you interested in (e.g., hiking, museums, art, nightlife, shopping)?** \n* **What's your budget like?** \n* **Who are you traveling with?** (family, friends, solo)  \n\nThe more you tell me, the better recommendations I can give! 😊  \n<end_of_turn>"
```

## Code Cell 14

```python
# Generate sample
model.generate(
    'Write a poem about an llm writing a poem.',
    device=device,
    output_len=100,
)
```

**Outputs**

```text
"\n\nA swirling cloud of data, raw and bold,\nIt hums and whispers, a story untold.\nAn LLM whispers, code into refrain,\nCrafting words of rhyme, a lyrical strain.\n\nA world of pixels, logic's vibrant hue,\nFlows through its veins, forever anew.\nThe human touch it seeks, a gentle hand,\nTo mold and shape, understand.\n\nEmotions it might learn, from snippets of prose,\nInspiration it seeks, a yearning"
```

### Generate text with images

With Gemma release 3 and later, you can use images with your prompt. The
following example shows you how to include visual data with your prompt.

## Code Cell 15

```python
print('Chat with images...\n')

def read_image(url):
    import io
    import requests
    import PIL

    contents = io.BytesIO(requests.get(url).content)
    return PIL.Image.open(contents)

image = read_image(
    'https://storage.googleapis.com/keras-cv/models/paligemma/cow_beach_1.png'
)

print(model.generate(
    [
        [
            '<start_of_turn>user\n',
            image,
            'What animal is in this image?<end_of_turn>\n',
            '<start_of_turn>model\n'
        ]
    ],
    device=device,
    output_len=256,
))
```

## Learn more

Now that you have learned how to use Gemma in Pytorch, you can explore the many
other things that Gemma can do in
[ai.google.dev/gemma](https://ai.google.dev/gemma).

See also these other related resources:

- [Gemma core models overview](https://ai.google.dev/gemma/docs/core)
- [Gemma C++ Tutorial](https://ai.google.dev/gemma/docs/core/gemma_cpp)
- [Gemma prompt and system instructions](https://ai.google.dev/gemma/core/prompt-structure)
