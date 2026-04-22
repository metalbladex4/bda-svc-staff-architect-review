\---

license: other

license\_name: qwen

license\_link: https://huggingface.co/Qwen/Qwen2.5-72B-Instruct/blob/main/LICENSE

pipeline\_tag: image-text-to-text

library\_name: transformers

base\_model:

\- OpenGVLab/InternVL3-8B-Instruct

base\_model\_relation: finetune

datasets:

\- OpenGVLab/MMPR-v1.2

language:

\- multilingual

tags:

\- internvl

\---



\# InternVL3-8B Transformers 🤗 Implementation



\[\\\[📜 InternVL 1.0\\]](https://huggingface.co/papers/2312.14238)  \[\\\[📜 InternVL 1.5\\]](https://huggingface.co/papers/2404.16821)  \[\\\[📜 InternVL 2.5\\]](https://huggingface.co/papers/2412.05271)  \[\\\[📜 InternVL2.5-MPO\\]](https://huggingface.co/papers/2411.10442)  \[\\\[📜 InternVL3\\]](https://huggingface.co/papers/2504.10479)



\[\\\[🆕 Blog\\]](https://internvl.github.io/blog/)  \[\\\[🗨️ Chat Demo\\]](https://internvl.opengvlab.com/)  \[\\\[🤗 HF Demo\\]](https://huggingface.co/spaces/OpenGVLab/InternVL)  \[\\\[🚀 Quick Start\\]](#quick-start)  \[\\\[📖 Documents\\]](https://internvl.readthedocs.io/en/latest/)



<div align="center">

&#x20; <img width="500" alt="image" src="https://cdn-uploads.huggingface.co/production/uploads/64006c09330a45b03605bba3/zJsd2hqd3EevgXo6fNgC-.png">

</div>





> \[!IMPORTANT]

> This repository contains the Hugging Face 🤗 Transformers implementation for the \[OpenGVLab/InternVL3-8B](https://huggingface.co/OpenGVLab/InternVL3-8B) model.

> It is intended to be functionally equivalent to the original OpenGVLab release.

> As a native Transformers model, it supports core library features such as various attention implementations (eager, including SDPA, and FA2) and enables efficient batched inference with interleaved image, video, and text inputs.



\## Introduction



We introduce InternVL3, an advanced multimodal large language model (MLLM) series that demonstrates superior overall performance.

Compared to InternVL 2.5, InternVL3 exhibits superior multimodal perception and reasoning capabilities, while further extending its multimodal capabilities to encompass tool usage, GUI agents, industrial image analysis, 3D vision perception, and more.

Additionally, we compare InternVL3 with  Qwen2.5 Chat models, whose corresponding pre-trained base models are employed as the initialization of the langauge component in InternVL3. Benefitting from Native Multimodal Pre-Training, the InternVL3 series achieves even better overall text performance than the Qwen2.5 series.



!\[image/png](https://huggingface.co/datasets/Weiyun1025/InternVL-Performance/resolve/main/internvl3/overall.png)



You can find more info on the InternVL3 family in the original checkpoint \[OpenGVLab/InternVL3-8B](https://huggingface.co/OpenGVLab/InternVL3-8B)



\## Usage example



\### Inference with Pipeline



Here is how you can use the `image-text-to-text` pipeline to perform inference with the `InternVL3` models in just a few lines of code:



```python

>>> from transformers import pipeline



>>> messages = \[

...     {

...         "role": "user",

...         "content": \[

...             {

...                 "type": "image",

...                 "image": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg",

...             },

...             {"type": "text", "text": "Describe this image."},

...         ],

...     },

... ]



>>> pipe = pipeline("image-text-to-text", model="OpenGVLab/InternVL3-8B-hf")

>>> outputs = pipe(text=messages, max\_new\_tokens=50, return\_full\_text=False)

>>> outputs\[0]\["generated\_text"]

'The image showcases a vibrant scene of nature, featuring several flowers and a bee. \\n\\n1. \*\*Foreground Flowers\*\*: \\n   - The primary focus is on a large, pink cosmos flower with a prominent yellow center. The petals are soft and slightly r'

```

\### Inference on a single image



This example demonstrates how to perform inference on a single image with the InternVL models using chat templates.



> \[!NOTE]

> Note that the model has been trained with a specific prompt format for chatting. Use `processor.apply\_chat\_template(my\_conversation\_dict)` to correctly format your prompts.



```python

>>> from transformers import AutoProcessor, AutoModelForImageTextToText

>>> import torch



>>> torch\_device = "cuda"

>>> model\_checkpoint = "OpenGVLab/InternVL3-8B-hf"

>>> processor = AutoProcessor.from\_pretrained(model\_checkpoint)

>>> model = AutoModelForImageTextToText.from\_pretrained(model\_checkpoint, device\_map=torch\_device, torch\_dtype=torch.bfloat16)



>>> messages = \[

...     {

...         "role": "user",

...         "content": \[

...             {"type": "image", "url": "http://images.cocodataset.org/val2017/000000039769.jpg"},

...             {"type": "text", "text": "Please describe the image explicitly."},

...         ],

...     }

... ]



>>> inputs = processor.apply\_chat\_template(messages, add\_generation\_prompt=True, tokenize=True, return\_dict=True, return\_tensors="pt").to(model.device, dtype=torch.bfloat16)



>>> generate\_ids = model.generate(\*\*inputs, max\_new\_tokens=50)

>>> decoded\_output = processor.decode(generate\_ids\[0, inputs\["input\_ids"].shape\[1] :], skip\_special\_tokens=True)



>>> decoded\_output

'The image shows two cats lying on a pink blanket. The cat on the left is a tabby with a mix of brown, black, and white fur, and it appears to be sleeping with its head resting on the blanket. The cat on the'

```



\### Text-only generation

This example shows how to generate text using the InternVL model without providing any image input.





```python

>>> from transformers import AutoProcessor, AutoModelForImageTextToText

>>> import torch



>>> torch\_device = "cuda"

>>> model\_checkpoint = "OpenGVLab/InternVL3-8B-hf"

>>> processor = AutoProcessor.from\_pretrained(model\_checkpoint)

>>> model = AutoModelForImageTextToText.from\_pretrained(model\_checkpoint, device\_map=torch\_device, torch\_dtype=torch.bfloat16)



>>> messages = \[

...     {

...         "role": "user",

...         "content": \[

...             {"type": "text", "text": "Write a haiku"},

...         ],

...     }

... ]



>>> inputs = processor.apply\_chat\_template(messages, add\_generation\_prompt=True, tokenize=True, return\_dict=True, return\_tensors="pt").to(torch\_device, dtype=torch.bfloat16)



>>> generate\_ids = model.generate(\*\*inputs, max\_new\_tokens=50)

>>> decoded\_output = processor.decode(generate\_ids\[0, inputs\["input\_ids"].shape\[1] :], skip\_special\_tokens=True)



>>> print(decoded\_output)

"Whispers of dawn,\\nSilent whispers of the night,\\nNew day's light begins."

```



\### Batched image and text inputs

InternVL models also support batched image and text inputs.



```python

>>> from transformers import AutoProcessor, AutoModelForImageTextToText

>>> import torch



>>> torch\_device = "cuda"

>>> model\_checkpoint = "OpenGVLab/InternVL3-8B-hf"

>>> processor = AutoProcessor.from\_pretrained(model\_checkpoint)

>>> model = AutoModelForImageTextToText.from\_pretrained(model\_checkpoint, device\_map=torch\_device, torch\_dtype=torch.bfloat16)



>>> messages = \[

...     \[

...         {

...             "role": "user",

...             "content": \[

...                 {"type": "image", "url": "https://llava-vl.github.io/static/images/view.jpg"},

...                 {"type": "text", "text": "Write a haiku for this image"},

...             ],

...         },

...     ],

...     \[

...         {

...             "role": "user",

...             "content": \[

...                 {"type": "image", "url": "https://www.ilankelman.org/stopsigns/australia.jpg"},

...                 {"type": "text", "text": "Describe this image"},

...             ],

...         },

...     ],

... ]





>>> inputs = processor.apply\_chat\_template(messages, padding=True, add\_generation\_prompt=True, tokenize=True, return\_dict=True, return\_tensors="pt").to(model.device, dtype=torch.bfloat16)



>>> output = model.generate(\*\*inputs, max\_new\_tokens=25)



>>> decoded\_outputs = processor.batch\_decode(output, skip\_special\_tokens=True)

>>> decoded\_outputs

\["user\\n\\nWrite a haiku for this image\\nassistant\\nSilky lake,  \\nWooden pier,  \\nNature's peace.",

&#x20;'user\\n\\nDescribe this image\\nassistant\\nThe image shows a street scene with a traditional Chinese archway, known as a "Chinese Gate" or "Chinese Gate of']

```



\### Batched multi-image input

This implementation of the InternVL models supports batched text-images inputs with different number of images for each text.



```python

>>> from transformers import AutoProcessor, AutoModelForImageTextToText

>>> import torch



>>> torch\_device = "cuda"

>>> model\_checkpoint = "OpenGVLab/InternVL3-8B-hf"

>>> processor = AutoProcessor.from\_pretrained(model\_checkpoint)

>>> model = AutoModelForImageTextToText.from\_pretrained(model\_checkpoint, device\_map=torch\_device, torch\_dtype=torch.bfloat16)



>>> messages = \[

...     \[

...         {

...             "role": "user",

...             "content": \[

...                 {"type": "image", "url": "https://llava-vl.github.io/static/images/view.jpg"},

...                 {"type": "text", "text": "Write a haiku for this image"},

...             ],

...         },

...     ],

...     \[

...         {

...             "role": "user",

...             "content": \[

...                 {"type": "image", "url": "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"},

...                 {"type": "image", "url": "https://thumbs.dreamstime.com/b/golden-gate-bridge-san-francisco-purple-flowers-california-echium-candicans-36805947.jpg"},

...                 {"type": "text", "text": "These images depict two different landmarks. Can you identify them?"},

...             ],

...         },

...     ],

>>> ]



>>> inputs = processor.apply\_chat\_template(messages, padding=True, add\_generation\_prompt=True, tokenize=True, return\_dict=True, return\_tensors="pt").to(model.device, dtype=torch.bfloat16)



>>> output = model.generate(\*\*inputs, max\_new\_tokens=25)



>>> decoded\_outputs = processor.batch\_decode(output, skip\_special\_tokens=True)

>>> decoded\_outputs

\["user\\n\\nWrite a haiku for this image\\nassistant\\nSilky lake,  \\nWooden pier,  \\nNature's peace.",

&#x20;'user\\n\\n\\nThese images depict two different landmarks. Can you identify them?\\nassistant\\nYes, these images depict the Statue of Liberty and the Golden Gate Bridge.']

```



\### Video input

InternVL models can also handle video inputs. Here is an example of how to perform inference on a video input using chat templates.



```python

>>> from transformers import AutoProcessor, AutoModelForImageTextToText, BitsAndBytesConfig



>>> model\_checkpoint = "OpenGVLab/InternVL3-8B-hf"

>>> quantization\_config = BitsAndBytesConfig(load\_in\_4bit=True)

>>> processor = AutoProcessor.from\_pretrained(model\_checkpoint)

>>> model = AutoModelForImageTextToText.from\_pretrained(model\_checkpoint, quantization\_config=quantization\_config)



>>> messages = \[

...     {

...         "role": "user",

...         "content": \[

...             {

...                 "type": "video",

...                 "url": "https://huggingface.co/datasets/hf-internal-testing/fixtures\_videos/resolve/main/tennis.mp4",

...             },

...             {"type": "text", "text": "What type of shot is the man performing?"},

...         ],

...     }

>>> ]

>>> inputs = processor.apply\_chat\_template(

...     messages,

...     return\_tensors="pt",

...     add\_generation\_prompt=True,

...     tokenize=True,

...     return\_dict=True,

>>> ).to(model.device, dtype=torch.float16)



>>> output = model.generate(\*\*inputs, max\_new\_tokens=25)



>>> decoded\_output = processor.decode(output\[0, inputs\["input\_ids"].shape\[1] :], skip\_special\_tokens=True)

>>> decoded\_output

'The man is performing a forehand shot.'

```



\### Interleaved image and video inputs

This example showcases how to handle a batch of chat conversations with interleaved image and video inputs using chat template.



```python

>>> from transformers import AutoProcessor, AutoModelForImageTextToText, BitsAndBytesConfig

>>> import torch



>>> torch\_device = "cuda"

>>> model\_checkpoint = "OpenGVLab/InternVL3-8B-hf"

>>> processor = AutoProcessor.from\_pretrained(model\_checkpoint)

>>> model = AutoModelForImageTextToText.from\_pretrained(model\_checkpoint, device\_map=torch\_device, torch\_dtype=torch.bfloat16)



>>> messages = \[

...     \[

...         {

...             "role": "user",

...             "content": \[

...                 {"type": "image", "url": "https://cdn.britannica.com/61/93061-050-99147DCE/Statue-of-Liberty-Island-New-York-Bay.jpg"},

...                 {"type": "image", "url": "https://thumbs.dreamstime.com/b/golden-gate-bridge-san-francisco-purple-flowers-california-echium-candicans-36805947.jpg"},

...                 {"type": "text", "text": "These images depict two different landmarks. Can you identify them?"},

...             ],

...         },

...     ],

...     \[

...         {

...             "role": "user",

...             "content": \[

...                 {"type": "video", "url": "https://huggingface.co/datasets/hf-internal-testing/fixtures\_videos/resolve/main/tennis.mp4"},

...                 {"type": "text", "text": "What type of shot is the man performing?"},

...             ],

...         },

...     ],

...     \[

...         {

...             "role": "user",

...             "content": \[

...                 {"type": "image", "url": "https://llava-vl.github.io/static/images/view.jpg"},

...                 {"type": "text", "text": "Write a haiku for this image"},

...             ],

...         },

...     ],

>>> ]

>>> inputs = processor.apply\_chat\_template(

...     messages,

...     padding=True,

...     add\_generation\_prompt=True,

...     tokenize=True,

...     return\_dict=True,

...     return\_tensors="pt",

>>> ).to(model.device, dtype=torch.bfloat16)



>>> outputs = model.generate(\*\*inputs, max\_new\_tokens=25)



>>> decoded\_outputs = processor.batch\_decode(outputs, skip\_special\_tokens=True)

>>> decoded\_outputs

\['user\\n\\n\\nThese images depict two different landmarks. Can you identify them?\\nassistant\\nThe images depict the Statue of Liberty and the Golden Gate Bridge.',

&#x20;'user\\nFrame1: \\nFrame2: \\nFrame3: \\nFrame4: \\nFrame5: \\nFrame6: \\nFrame7: \\nFrame8: \\nWhat type of shot is the man performing?\\nassistant\\nA forehand shot',

&#x20;"user\\n\\nWrite a haiku for this image\\nassistant\\nSilky lake,  \\nWooden pier,  \\nNature's peace."]

```



\## License



This project is released under the MIT License. This project uses the pre-trained Qwen2.5 as a component, which is licensed under the Qwen License.



\## Citation



If you find this project useful in your research, please consider citing:



```BibTeX

@article{chen2024expanding,

&#x20; title={Expanding Performance Boundaries of Open-Source Multimodal Models with Model, Data, and Test-Time Scaling},

&#x20; author={Chen, Zhe and Wang, Weiyun and Cao, Yue and Liu, Yangzhou and Gao, Zhangwei and Cui, Erfei and Zhu, Jinguo and Ye, Shenglong and Tian, Hao and Liu, Zhaoyang and others},

&#x20; journal={arXiv preprint arXiv:2412.05271},

&#x20; year={2024}

}

@article{wang2024mpo,

&#x20; title={Enhancing the Reasoning Ability of Multimodal Large Language Models via Mixed Preference Optimization},

&#x20; author={Wang, Weiyun and Chen, Zhe and Wang, Wenhai and Cao, Yue and Liu, Yangzhou and Gao, Zhangwei and Zhu, Jinguo and Zhu, Xizhou and Lu, Lewei and Qiao, Yu and Dai, Jifeng},

&#x20; journal={arXiv preprint arXiv:2411.10442},

&#x20; year={2024}

}

@article{chen2024far,

&#x20; title={How Far Are We to GPT-4V? Closing the Gap to Commercial Multimodal Models with Open-Source Suites},

&#x20; author={Chen, Zhe and Wang, Weiyun and Tian, Hao and Ye, Shenglong and Gao, Zhangwei and Cui, Erfei and Tong, Wenwen and Hu, Kongzhi and Luo, Jiapeng and Ma, Zheng and others},

&#x20; journal={arXiv preprint arXiv:2404.16821},

&#x20; year={2024}

}

@inproceedings{chen2024internvl,

&#x20; title={Internvl: Scaling up vision foundation models and aligning for generic visual-linguistic tasks},

&#x20; author={Chen, Zhe and Wu, Jiannan and Wang, Wenhai and Su, Weijie and Chen, Guo and Xing, Sen and Zhong, Muyan and Zhang, Qinglong and Zhu, Xizhou and Lu, Lewei and others},

&#x20; booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},

&#x20; pages={24185--24198},

&#x20; year={2024}

}

```

