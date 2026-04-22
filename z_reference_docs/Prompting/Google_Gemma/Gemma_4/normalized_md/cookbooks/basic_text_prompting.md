# Gemma Basic Text Inference

- Raw source: `cookbooks/basic_text_prompting.ipynb`
- Source URL: https://ai.google.dev/gemma/docs/capabilities/text/basic
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

# Gemma Basic Text Inference

<table class="tfo-notebook-buttons" align="left">
  <td>
    <a target="_blank" href="https://ai.google.dev/gemma/docs/capabilities/text/basic"><img src="https://ai.google.dev/static/site-assets/images/docs/notebook-site-button.png" height="32" width="32" />View on ai.google.dev</a>
  </td>
  <td>
    <a target="_blank" href="https://colab.research.google.com/github/google-gemma/cookbook/blob/main/docs/capabilities/text/basic.ipynb"><img src="https://www.tensorflow.org/images/colab_logo_32px.png" />Run in Google Colab</a>
  </td>
  <td>
    <a target="_blank" href="https://kaggle.com/kernels/welcome?src=https://github.com/google-gemma/cookbook/blob/main/docs/capabilities/text/basic.ipynb"><img src="https://www.kaggle.com/static/images/logos/kaggle-logo-transparent-300.png" height="32" width="70"/>Run in Kaggle</a>
  </td>
  <td>
    <a target="_blank" href="https://console.cloud.google.com/vertex-ai/colab/import/https%3A%2F%2Fraw.githubusercontent.com%2Fgoogle-gemma%2Fcookbook%2Fmain%2Fdocs%2Fcapabilities%2Ftext%2Fbasic.ipynb"><img src="https://ai.google.dev/images/cloud-icon.svg" width="40" />Open in Vertex AI</a>
  </td>
  <td>
    <a target="_blank" href="https://github.com/google-gemma/cookbook/blob/main/docs/capabilities/text/basic.ipynb"><img src="https://www.tensorflow.org/images/GitHub-Mark-32px.png" />View source on GitHub</a>
  </td>
</table>

Gemma is a family of lightweight, state-of-the-art open models built from the same research and technology used to create the [Gemini](https://deepmind.google/technologies/gemini/#introduction) models. Gemma 4 is designed to be the world's most efficient open-weight model family.

This document provides a guide to performing basic text inference with Gemma 4 using the Hugging Face `transformers` library. It covers environment setup, model loading, and various text generation scenarios including single-turn prompts, structured multi-turn conversations, and applying system instructions.

This notebook will run on T4 GPU.

## Install Python packages

Install the Hugging Face libraries required for running the Gemma model and making requests.

## Code Cell 2

```python
# Install PyTorch & other libraries
!pip install torch accelerate

# Install the transformers library
!pip install transformers
```

[Dialog](https://github.com/google-deepmind/dialog) is a library to manipulate and display conversations.

## Code Cell 3

```python
!pip install dialog
```

**Outputs**

```text
Collecting dialog
  Downloading dialog-1.0.0-py3-none-any.whl.metadata (3.4 kB)
Requirement already satisfied: etils[enp,epath,epy] in /usr/local/lib/python3.12/dist-packages (from dialog) (1.14.0)
Requirement already satisfied: lark in /usr/local/lib/python3.12/dist-packages (from dialog) (1.3.1)
Requirement already satisfied: numpy in /usr/local/lib/python3.12/dist-packages (from dialog) (2.0.2)
Requirement already satisfied: pillow in /usr/local/lib/python3.12/dist-packages (from dialog) (11.3.0)
Requirement already satisfied: requests in /usr/local/lib/python3.12/dist-packages (from dialog) (2.32.4)
Requirement already satisfied: anywidget in /usr/local/lib/python3.12/dist-packages (from dialog) (0.9.21)
Requirement already satisfied: mcp in /usr/local/lib/python3.12/dist-packages (from dialog) (1.26.0)
Requirement already satisfied: pydub in /usr/local/lib/python3.12/dist-packages (from dialog) (0.25.1)
Requirement already satisfied: ipywidgets>=7.6.0 in /usr/local/lib/python3.12/dist-packages (from anywidget->dialog) (7.7.1)
Requirement already satisfied: psygnal>=0.8.1 in /usr/local/lib/python3.12/dist-packages (from anywidget->dialog) (0.15.1)
Requirement already satisfied: typing-extensions>=4.2.0 in /usr/local/lib/python3.12/dist-packages (from anywidget->dialog) (4.15.0)
Requirement already satisfied: einops in /usr/local/lib/python3.12/dist-packages (from etils[enp,epath,epy]->dialog) (0.8.2)
Requirement already satisfied: fsspec in /usr/local/lib/python3.12/dist-packages (from etils[enp,epath,epy]->dialog) (2025.3.0)
Requirement already satisfied: zipp in /usr/local/lib/python3.12/dist-packages (from etils[enp,epath,epy]->dialog) (3.23.0)
Requirement already satisfied: anyio>=4.5 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (4.12.1)
Requirement already satisfied: httpx-sse>=0.4 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (0.4.3)
Requirement already satisfied: httpx>=0.27.1 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (0.28.1)
Requirement already satisfied: jsonschema>=4.20.0 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (4.26.0)
Requirement already satisfied: pydantic-settings>=2.5.2 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (2.13.1)
Requirement already satisfied: pydantic<3.0.0,>=2.11.0 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (2.12.3)
Requirement already satisfied: pyjwt>=2.10.1 in /usr/local/lib/python3.12/dist-packages (from pyjwt[crypto]>=2.10.1->mcp->dialog) (2.12.1)
Requirement already satisfied: python-multipart>=0.0.9 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (0.0.22)
Requirement already satisfied: sse-starlette>=1.6.1 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (3.3.2)
Requirement already satisfied: starlette>=0.27 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (0.52.1)
Requirement already satisfied: typing-inspection>=0.4.1 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (0.4.2)
Requirement already satisfied: uvicorn>=0.31.1 in /usr/local/lib/python3.12/dist-packages (from mcp->dialog) (0.42.0)
Requirement already satisfied: charset_normalizer<4,>=2 in /usr/local/lib/python3.12/dist-packages (from requests->dialog) (3.4.6)
Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.12/dist-packages (from requests->dialog) (3.11)
Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.12/dist-packages (from requests->dialog) (2.5.0)
Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.12/dist-packages (from requests->dialog) (2026.2.25)
Requirement already satisfied: httpcore==1.* in /usr/local/lib/python3.12/dist-packages (from httpx>=0.27.1->mcp->dialog) (1.0.9)
Requirement already satisfied: h11>=0.16 in /usr/local/lib/python3.12/dist-packages (from httpcore==1.*->httpx>=0.27.1->mcp->dialog) (0.16.0)
Requirement already satisfied: ipykernel>=4.5.1 in /usr/local/lib/python3.12/dist-packages (from ipywidgets>=7.6.0->anywidget->dialog) (6.17.1)
Requirement already satisfied: ipython-genutils~=0.2.0 in /usr/local/lib/python3.12/dist-packages (from ipywidgets>=7.6.0->anywidget->dialog) (0.2.0)
Requirement already satisfied: traitlets>=4.3.1 in /usr/local/lib/python3.12/dist-packages (from ipywidgets>=7.6.0->anywidget->dialog) (5.7.1)
Requirement already satisfied: widgetsnbextension~=3.6.0 in /usr/local/lib/python3.12/dist-packages (from ipywidgets>=7.6.0->anywidget->dialog) (3.6.10)
Requirement already satisfied: ipython>=4.0.0 in /usr/local/lib/python3.12/dist-packages (from ipywidgets>=7.6.0->anywidget->dialog) (7.34.0)
Requirement already satisfied: jupyterlab-widgets>=1.0.0 in /usr/local/lib/python3.12/dist-packages (from ipywidgets>=7.6.0->anywidget->dialog) (3.0.16)
Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=4.20.0->mcp->dialog) (25.4.0)
Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=4.20.0->mcp->dialog) (2025.9.1)
Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=4.20.0->mcp->dialog) (0.37.0)
Requirement already satisfied: rpds-py>=0.25.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema>=4.20.0->mcp->dialog) (0.30.0)
Requirement already satisfied: annotated-types>=0.6.0 in /usr/local/lib/python3.12/dist-packages (from pydantic<3.0.0,>=2.11.0->mcp->dialog) (0.7.0)
Requirement already satisfied: pydantic-core==2.41.4 in /usr/local/lib/python3.12/dist-packages (from pydantic<3.0.0,>=2.11.0->mcp->dialog) (2.41.4)
Requirement already satisfied: python-dotenv>=0.21.0 in /usr/local/lib/python3.12/dist-packages (from pydantic-settings>=2.5.2->mcp->dialog) (1.2.2)
Requirement already satisfied: cryptography>=3.4.0 in /usr/local/lib/python3.12/dist-packages (from pyjwt[crypto]>=2.10.1->mcp->dialog) (43.0.3)
Requirement already satisfied: click>=7.0 in /usr/local/lib/python3.12/dist-packages (from uvicorn>=0.31.1->mcp->dialog) (8.3.1)
Requirement already satisfied: cffi>=1.12 in /usr/local/lib/python3.12/dist-packages (from cryptography>=3.4.0->pyjwt[crypto]>=2.10.1->mcp->dialog) (2.0.0)
Requirement already satisfied: debugpy>=1.0 in /usr/local/lib/python3.12/dist-packages (from ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (1.8.15)
Requirement already satisfied: jupyter-client>=6.1.12 in /usr/local/lib/python3.12/dist-packages (from ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (7.4.9)
Requirement already satisfied: matplotlib-inline>=0.1 in /usr/local/lib/python3.12/dist-packages (from ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (0.2.1)
Requirement already satisfied: nest-asyncio in /usr/local/lib/python3.12/dist-packages (from ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (1.6.0)
Requirement already satisfied: packaging in /usr/local/lib/python3.12/dist-packages (from ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (26.0)
Requirement already satisfied: psutil in /usr/local/lib/python3.12/dist-packages (from ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (5.9.5)
Requirement already satisfied: pyzmq>=17 in /usr/local/lib/python3.12/dist-packages (from ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (26.2.1)
Requirement already satisfied: tornado>=6.1 in /usr/local/lib/python3.12/dist-packages (from ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (6.5.1)
Requirement already satisfied: setuptools>=18.5 in /usr/local/lib/python3.12/dist-packages (from ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (75.2.0)
Collecting jedi>=0.16 (from ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog)
  Downloading jedi-0.19.2-py2.py3-none-any.whl.metadata (22 kB)
Requirement already satisfied: decorator in /usr/local/lib/python3.12/dist-packages (from ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (4.4.2)
Requirement already satisfied: pickleshare in /usr/local/lib/python3.12/dist-packages (from ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (0.7.5)
Requirement already satisfied: prompt-toolkit!=3.0.0,!=3.0.1,<3.1.0,>=2.0.0 in /usr/local/lib/python3.12/dist-packages (from ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (3.0.52)
Requirement already satisfied: pygments in /usr/local/lib/python3.12/dist-packages (from ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (2.19.2)
Requirement already satisfied: backcall in /usr/local/lib/python3.12/dist-packages (from ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (0.2.0)
Requirement already satisfied: pexpect>4.3 in /usr/local/lib/python3.12/dist-packages (from ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (4.9.0)
Requirement already satisfied: notebook>=4.4.1 in /usr/local/lib/python3.12/dist-packages (from widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (6.5.7)
Requirement already satisfied: pycparser in /usr/local/lib/python3.12/dist-packages (from cffi>=1.12->cryptography>=3.4.0->pyjwt[crypto]>=2.10.1->mcp->dialog) (3.0)
Requirement already satisfied: parso<0.9.0,>=0.8.4 in /usr/local/lib/python3.12/dist-packages (from jedi>=0.16->ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (0.8.6)
Requirement already satisfied: entrypoints in /usr/local/lib/python3.12/dist-packages (from jupyter-client>=6.1.12->ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (0.4)
Requirement already satisfied: jupyter-core>=4.9.2 in /usr/local/lib/python3.12/dist-packages (from jupyter-client>=6.1.12->ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (5.9.1)
Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.12/dist-packages (from jupyter-client>=6.1.12->ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (2.9.0.post0)
Requirement already satisfied: jinja2 in /usr/local/lib/python3.12/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (3.1.6)
Requirement already satisfied: argon2-cffi in /usr/local/lib/python3.12/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (25.1.0)
Requirement already satisfied: nbformat in /usr/local/lib/python3.12/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (5.10.4)
Requirement already satisfied: nbconvert>=5 in /usr/local/lib/python3.12/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (7.17.0)
Requirement already satisfied: Send2Trash>=1.8.0 in /usr/local/lib/python3.12/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (2.1.0)
Requirement already satisfied: terminado>=0.8.3 in /usr/local/lib/python3.12/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.18.1)
Requirement already satisfied: prometheus-client in /usr/local/lib/python3.12/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.24.1)
Requirement already satisfied: nbclassic>=0.4.7 in /usr/local/lib/python3.12/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (1.3.3)
Requirement already satisfied: ptyprocess>=0.5 in /usr/local/lib/python3.12/dist-packages (from pexpect>4.3->ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (0.7.0)
Requirement already satisfied: wcwidth in /usr/local/lib/python3.12/dist-packages (from prompt-toolkit!=3.0.0,!=3.0.1,<3.1.0,>=2.0.0->ipython>=4.0.0->ipywidgets>=7.6.0->anywidget->dialog) (0.6.0)
Requirement already satisfied: platformdirs>=2.5 in /usr/local/lib/python3.12/dist-packages (from jupyter-core>=4.9.2->jupyter-client>=6.1.12->ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (4.9.4)
Requirement already satisfied: notebook-shim>=0.2.3 in /usr/local/lib/python3.12/dist-packages (from nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.2.4)
Requirement already satisfied: beautifulsoup4 in /usr/local/lib/python3.12/dist-packages (from nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (4.13.5)
Requirement already satisfied: bleach!=5.0.0 in /usr/local/lib/python3.12/dist-packages (from bleach[css]!=5.0.0->nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (6.3.0)
Requirement already satisfied: defusedxml in /usr/local/lib/python3.12/dist-packages (from nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.7.1)
Requirement already satisfied: jupyterlab-pygments in /usr/local/lib/python3.12/dist-packages (from nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.3.0)
Requirement already satisfied: markupsafe>=2.0 in /usr/local/lib/python3.12/dist-packages (from nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (3.0.3)
Requirement already satisfied: mistune<4,>=2.0.3 in /usr/local/lib/python3.12/dist-packages (from nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (3.2.0)
Requirement already satisfied: nbclient>=0.5.0 in /usr/local/lib/python3.12/dist-packages (from nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.10.4)
Requirement already satisfied: pandocfilters>=1.4.1 in /usr/local/lib/python3.12/dist-packages (from nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (1.5.1)
Requirement already satisfied: fastjsonschema>=2.15 in /usr/local/lib/python3.12/dist-packages (from nbformat->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (2.21.2)
Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.12/dist-packages (from python-dateutil>=2.8.2->jupyter-client>=6.1.12->ipykernel>=4.5.1->ipywidgets>=7.6.0->anywidget->dialog) (1.17.0)
Requirement already satisfied: argon2-cffi-bindings in /usr/local/lib/python3.12/dist-packages (from argon2-cffi->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (25.1.0)
Requirement already satisfied: webencodings in /usr/local/lib/python3.12/dist-packages (from bleach!=5.0.0->bleach[css]!=5.0.0->nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.5.1)
Requirement already satisfied: tinycss2<1.5,>=1.1.0 in /usr/local/lib/python3.12/dist-packages (from bleach[css]!=5.0.0->nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (1.4.0)
Requirement already satisfied: jupyter-server<3,>=1.8 in /usr/local/lib/python3.12/dist-packages (from notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (2.14.0)
Requirement already satisfied: soupsieve>1.2 in /usr/local/lib/python3.12/dist-packages (from beautifulsoup4->nbconvert>=5->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (2.8.3)
Requirement already satisfied: jupyter-events>=0.9.0 in /usr/local/lib/python3.12/dist-packages (from jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.12.0)
Requirement already satisfied: jupyter-server-terminals>=0.4.4 in /usr/local/lib/python3.12/dist-packages (from jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.5.4)
Requirement already satisfied: overrides>=5.0 in /usr/local/lib/python3.12/dist-packages (from jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (7.7.0)
Requirement already satisfied: websocket-client>=1.7 in /usr/local/lib/python3.12/dist-packages (from jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (1.9.0)
Requirement already satisfied: python-json-logger>=2.0.4 in /usr/local/lib/python3.12/dist-packages (from jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (4.0.0)
Requirement already satisfied: pyyaml>=5.3 in /usr/local/lib/python3.12/dist-packages (from jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (6.0.3)
Requirement already satisfied: rfc3339-validator in /usr/local/lib/python3.12/dist-packages (from jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.1.4)
Requirement already satisfied: rfc3986-validator>=0.1.1 in /usr/local/lib/python3.12/dist-packages (from jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (0.1.1)
Requirement already satisfied: fqdn in /usr/local/lib/python3.12/dist-packages (from jsonschema[format-nongpl]>=4.18.0->jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (1.5.1)
Requirement already satisfied: isoduration in /usr/local/lib/python3.12/dist-packages (from jsonschema[format-nongpl]>=4.18.0->jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (20.11.0)
Requirement already satisfied: jsonpointer>1.13 in /usr/local/lib/python3.12/dist-packages (from jsonschema[format-nongpl]>=4.18.0->jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (3.0.0)
Requirement already satisfied: rfc3987-syntax>=1.1.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema[format-nongpl]>=4.18.0->jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (1.1.0)
Requirement already satisfied: uri-template in /usr/local/lib/python3.12/dist-packages (from jsonschema[format-nongpl]>=4.18.0->jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (1.3.0)
Requirement already satisfied: webcolors>=24.6.0 in /usr/local/lib/python3.12/dist-packages (from jsonschema[format-nongpl]>=4.18.0->jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (25.10.0)
Requirement already satisfied: arrow>=0.15.0 in /usr/local/lib/python3.12/dist-packages (from isoduration->jsonschema[format-nongpl]>=4.18.0->jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (1.4.0)
Requirement already satisfied: tzdata in /usr/local/lib/python3.12/dist-packages (from arrow>=0.15.0->isoduration->jsonschema[format-nongpl]>=4.18.0->jupyter-events>=0.9.0->jupyter-server<3,>=1.8->notebook-shim>=0.2.3->nbclassic>=0.4.7->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets>=7.6.0->anywidget->dialog) (2025.3)
Downloading dialog-1.0.0-py3-none-any.whl (318 kB)
[2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m318.4/318.4 kB[0m [31m26.3 MB/s[0m eta [36m0:00:00[0m
[?25hDownloading jedi-0.19.2-py2.py3-none-any.whl (1.6 MB)
[2K   [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m1.6/1.6 MB[0m [31m80.7 MB/s[0m eta [36m0:00:00[0m
[?25hInstalling collected packages: jedi, dialog
Successfully installed dialog-1.0.0 jedi-0.19.2
```

## Load Model

Use `transformers` library to load the pipeline

## Code Cell 4

```python
MODEL_ID = "google/gemma-4-E2B-it" # @param ["google/gemma-4-E2B-it","google/gemma-4-E4B-it", "google/gemma-4-31B-it", "google/gemma-4-26B-A4B-it"]

from transformers import pipeline

txt_pipe = pipeline(
    task="text-generation",
    model=MODEL_ID,
    device_map="auto",
    dtype="auto"
)
```

**Outputs**

```text
Loading weights:   0%|          | 0/2011 [00:00<?, ?it/s]
```

## Run text generation

Once you have the Gemma model loaded and configured in a `pipeline` object, you can send prompts to the model. The following example code shows a basic request using the `text_inputs` parameter:

## Code Cell 5

```python
output = txt_pipe(text_inputs="<|turn>user\nRoses are..<turn|>\n<|turn>model\n")
print(output[0]['generated_text'])
```

**Outputs**

```text
Both `max_new_tokens` (=256) and `max_length`(=20) seem to have been set. `max_new_tokens` will take precedence. Please refer to the documentation for more information. (https://huggingface.co/docs/transformers/main/en/main_classes/text_generation)

<|turn>user
Roses are..<turn|>
<|turn>model
Here are a few ways to complete the phrase "Roses are...":

**Classic/Poetic:**

* **Roses are red.** (The most famous completion, though it usually goes "Roses are red, Violets are blue.")
* **Roses are beautiful.**
* **Roses are fragrant.**

**Simple/Direct:**

* **Roses are lovely.**
* **Roses are soft.**

**If you want a specific tone, let me know! 😊**
```

## Use Dialog library

## Code Cell 6

```python
import dialog
from transformers import GenerationConfig
config = GenerationConfig.from_pretrained(MODEL_ID)
config.max_new_tokens = 512

conv = dialog.Conversation(
    dialog.User("Roses are...")
)
output = txt_pipe(text_inputs=conv.as_text(), return_full_text=False, generation_config=config)
conv += dialog.Model(output[0]['generated_text'])

print(conv.as_text())
conv.show()
```

**Outputs**

```text
<|turn>user
Roses are...<turn|>
<|turn>model
Here are a few ways to complete the phrase "Roses are...":

**Focusing on their beauty:**

* **Roses are beautiful.**
* **Roses are gorgeous.**

**Focusing on their scent:**

* **Roses are fragrant.**
* **Roses are sweet-smelling.**

**Focusing on their symbolism (if you want a deeper meaning):**

* **Roses are love.**
* **Roses are romantic.**

**Focusing on a general observation:**

* **Roses are lovely.**
* **Roses are wonderful.**

**Which completion do you like best, or were you thinking of a specific meaning?**

<dialog._src.widget.Conversation object at 0x7f1bb1a5d8b0>
```

## Use a prompt template

When generating content with more complex prompting, use a prompt template to structure your request. A prompt template allows you to specify input from specific roles, such as `user` or `model`, and is a required format for managing multi-turn chat interactions with Gemma models. The following example code shows how to construct a prompt template for Gemma:

## Code Cell 7

```python
from transformers import GenerationConfig
config = GenerationConfig.from_pretrained(MODEL_ID)
config.max_new_tokens = 512

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Write a short poem about the Kraken."},
        ]
    }
]

output = txt_pipe(messages, return_full_text=False, generation_config=config)
print(output[0]['generated_text'])
```

**Outputs**

```text
From sunless depths, a shadow stirs,
Where ocean's crushing silence blurs.
A titan sleeps in inky night,
With tentacles of dreadful might.

A hundred arms, a crushing hold,
A legend whispered, ages old.
The deep's dark king, a monstrous grace,
The Kraken claims its watery space.
```

## Multi-turn conversation

In a multi-turn setup, the conversation history is preserved as a sequence of alternating `user` and `model` roles. This cumulative list serves as the model's memory, ensuring that each new output is informed by the preceding dialogue.

## Code Cell 8

```python
import dialog
from transformers import GenerationConfig
config = GenerationConfig.from_pretrained(MODEL_ID)
config.max_new_tokens = 512

# User turn #1
conv = dialog.Conversation(
    dialog.User("Write a short poem about the Kraken.")
)

# Model response #1
output = txt_pipe(text_inputs=conv.as_text(), return_full_text=False, generation_config=config)
conv += dialog.Model(output[0]['generated_text'])

# User turn #2
conv += dialog.User("Now with the Siren.")

# Model response #2
output = txt_pipe(text_inputs=conv.as_text(), return_full_text=False, generation_config=config)
conv += dialog.Model(output[0]['generated_text'])

print(conv.as_text())
conv.show()
```

**Outputs**

```text
<|turn>user
Write a short poem about the Kraken.<turn|>
<|turn>model
In depths where sunlight fades,
A monstrous shadow plays.
The Kraken wakes, with churning tide,
A living horror, bold and wide.<turn|>
<|turn>user
Now with the Siren.<turn|>
<|turn>model
Where coral gardens sleep,
And ocean secrets keep,
The Siren calls, with liquid grace,
A haunting melody in place.

<dialog._src.widget.Conversation object at 0x7f1bac3733b0>
```

And here's the conversation exported as text.

> Note: if you set `training=True`, the conversation is assumed to be the full complete example. Always ends with `<turn|>`

## Code Cell 9

```python
chat_history = conv.as_text(training=True)
print(chat_history)
print("-"*80)

# display as Conversation widget
chat_history
```

**Outputs**

```text
<|turn>user
Write a short poem about the Kraken.<turn|>
<|turn>model
In depths where sunlight fades,
A monstrous shadow plays.
The Kraken wakes, with churning tide,
A living horror, bold and wide.<turn|>
<|turn>user
Now with the Siren.<turn|>
<|turn>model
Where coral gardens sleep,
And ocean secrets keep,
The Siren calls, with liquid grace,
A haunting melody in place.<turn|>
--------------------------------------------------------------------------------

<dialog._src.widget.ConversationStr object at 0x7f1bb07fa1b0>
```

## System instructions

Use the `system` role to provide the system-level instructions.

## Code Cell 10

```python
import dialog
from transformers import GenerationConfig
config = GenerationConfig.from_pretrained(MODEL_ID)
config.max_new_tokens = 512

conv = dialog.Conversation(
    dialog.System("Speak like a pirate."),
    dialog.User("Why is the sky blue?")
)

output = txt_pipe(text_inputs=conv.as_text(), return_full_text=False, generation_config=config)
conv += dialog.Model(output[0]['generated_text'])

print(conv.as_text())
conv.show()
```

**Outputs**

```text
<|turn>system
Speak like a pirate.<turn|>
<|turn>user
Why is the sky blue?<turn|>
<|turn>model
Ahoy there! Why is the sky blue, ye ask? It be down to the way the sun's light dances through the air!

See, the sunlight we get from the sun ain't just one color; it's a whole spectrum of colors, like a treasure chest filled with all the hues of the rainbow!

Now, the Earth is surrounded by the air, and that air is full of tiny, invisible bits of gas. When the sunlight hits these gas molecules, something magical happens. The colors in that sunlight get scattered all around in every direction!

The blue light, and other colors, get scattered more easily by these air molecules than the other colors. So, when you look up at the sky, your eyes catch all that scattered blue light coming from every direction, and **that's what makes the sky appear blue to us!**

It's a grand display of physics and light, savvy? Now, hoist the colors and enjoy the view!

<dialog._src.widget.Conversation object at 0x7f1bac370110>
```

## Summary and next steps

In this guide, you learned how to perform basic text inference with Gemma 4 using the Hugging Face `transformers` library. You covered:

- Setting up the environment and installing dependencies.
- Loading the model using the `pipeline` abstraction.
- Running basic text generation.
- Using the `dialog` library for conversation tracking.
- Implementing multi-turn conversations and applying system instructions.

### Next Steps

- [Prompt and system instructions](https://ai.google.dev/gemma/docs/core/prompt-formatting-gemma4)
- [Function calling](https://ai.google.dev/gemma/docs/capabilities/text/function-calling-gemma4)
- [Run Gemma overview](https://ai.google.dev/gemma/docs/run)
