\---

license: apache-2.0

pipeline\_tag: image-text-to-text

library\_name: transformers

\---

<a href="https://chat.qwenlm.ai/" target="\_blank" style="margin: 2px;">

&#x20;   <img alt="Chat" src="https://img.shields.io/badge/%F0%9F%92%9C%EF%B8%8F%20Qwen%20Chat%20-536af5" style="display: inline-block; vertical-align: middle;"/>

</a>





\# Qwen3-VL-8B-Instruct





Meet Qwen3-VL — the most powerful vision-language model in the Qwen series to date.



This generation delivers comprehensive upgrades across the board: superior text understanding \& generation, deeper visual perception \& reasoning, extended context length, enhanced spatial and video dynamics comprehension, and stronger agent interaction capabilities.



Available in Dense and MoE architectures that scale from edge to cloud, with Instruct and reasoning‑enhanced Thinking editions for flexible, on‑demand deployment.





\#### Key Enhancements:



\* \*\*Visual Agent\*\*: Operates PC/mobile GUIs—recognizes elements, understands functions, invokes tools, completes tasks.



\* \*\*Visual Coding Boost\*\*: Generates Draw.io/HTML/CSS/JS from images/videos.



\* \*\*Advanced Spatial Perception\*\*: Judges object positions, viewpoints, and occlusions; provides stronger 2D grounding and enables 3D grounding for spatial reasoning and embodied AI.



\* \*\*Long Context \& Video Understanding\*\*: Native 256K context, expandable to 1M; handles books and hours-long video with full recall and second-level indexing.



\* \*\*Enhanced Multimodal Reasoning\*\*: Excels in STEM/Math—causal analysis and logical, evidence-based answers.



\* \*\*Upgraded Visual Recognition\*\*: Broader, higher-quality pretraining is able to “recognize everything”—celebrities, anime, products, landmarks, flora/fauna, etc.



\* \*\*Expanded OCR\*\*: Supports 32 languages (up from 19); robust in low light, blur, and tilt; better with rare/ancient characters and jargon; improved long-document structure parsing.



\* \*\*Text Understanding on par with pure LLMs\*\*: Seamless text–vision fusion for lossless, unified comprehension.





\#### Model Architecture Updates:



<p align="center">

&#x20;   <img src="https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3-VL/qwen3vl\_arc.jpg" width="80%"/>

<p>





1\. \*\*Interleaved-MRoPE\*\*: Full‑frequency allocation over time, width, and height via robust positional embeddings, enhancing long‑horizon video reasoning.



2\. \*\*DeepStack\*\*: Fuses multi‑level ViT features to capture fine‑grained details and sharpen image–text alignment.



3\. \*\*Text–Timestamp Alignment:\*\* Moves beyond T‑RoPE to precise, timestamp‑grounded event localization for stronger video temporal modeling.



This is the weight repository for Qwen3-VL-8B-Instruct.





\---



\## Model Performance



\*\*Multimodal performance\*\*



!\[](https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3-VL/qwen3vl\_4b\_8b\_vl\_instruct.jpg)



\*\*Pure text performance\*\*

!\[](https://qianwen-res.oss-accelerate.aliyuncs.com/Qwen3-VL/qwen3vl\_4b\_8b\_text\_instruct.jpg)



\## Quickstart



Below, we provide simple examples to show how to use Qwen3-VL with 🤖 ModelScope and 🤗 Transformers.



The code of Qwen3-VL has been in the latest Hugging Face transformers and we advise you to build from source with command:

```

pip install git+https://github.com/huggingface/transformers

\# pip install transformers==4.57.0 # currently, V4.57.0 is not released

```



\### Using 🤗 Transformers to Chat



Here we show a code snippet to show how to use the chat model with `transformers`:



```python

from transformers import Qwen3VLForConditionalGeneration, AutoProcessor



\# default: Load the model on the available device(s)

model = Qwen3VLForConditionalGeneration.from\_pretrained(

&#x20;   "Qwen/Qwen3-VL-8B-Instruct", dtype="auto", device\_map="auto"

)



\# We recommend enabling flash\_attention\_2 for better acceleration and memory saving, especially in multi-image and video scenarios.

\# model = Qwen3VLForConditionalGeneration.from\_pretrained(

\#     "Qwen/Qwen3-VL-8B-Instruct",

\#     dtype=torch.bfloat16,

\#     attn\_implementation="flash\_attention\_2",

\#     device\_map="auto",

\# )



processor = AutoProcessor.from\_pretrained("Qwen/Qwen3-VL-8B-Instruct")



messages = \[

&#x20;   {

&#x20;       "role": "user",

&#x20;       "content": \[

&#x20;           {

&#x20;               "type": "image",

&#x20;               "image": "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg",

&#x20;           },

&#x20;           {"type": "text", "text": "Describe this image."},

&#x20;       ],

&#x20;   }

]



\# Preparation for inference

inputs = processor.apply\_chat\_template(

&#x20;   messages,

&#x20;   tokenize=True,

&#x20;   add\_generation\_prompt=True,

&#x20;   return\_dict=True,

&#x20;   return\_tensors="pt"

)

inputs = inputs.to(model.device)



\# Inference: Generation of the output

generated\_ids = model.generate(\*\*inputs, max\_new\_tokens=128)

generated\_ids\_trimmed = \[

&#x20;   out\_ids\[len(in\_ids) :] for in\_ids, out\_ids in zip(inputs.input\_ids, generated\_ids)

]

output\_text = processor.batch\_decode(

&#x20;   generated\_ids\_trimmed, skip\_special\_tokens=True, clean\_up\_tokenization\_spaces=False

)

print(output\_text)

```



\### Generation Hyperparameters

\#### VL

```bash

export greedy='false'

export top\_p=0.8

export top\_k=20

export temperature=0.7

export repetition\_penalty=1.0

export presence\_penalty=1.5

export out\_seq\_length=16384

```



\#### Text

```bash

export greedy='false'

export top\_p=1.0

export top\_k=40

export repetition\_penalty=1.0

export presence\_penalty=2.0

export temperature=1.0

export out\_seq\_length=32768

```





\## Citation



If you find our work helpful, feel free to give us a cite.



```

@misc{qwen3technicalreport,

&#x20;     title={Qwen3 Technical Report}, 

&#x20;     author={Qwen Team},

&#x20;     year={2025},

&#x20;     eprint={2505.09388},

&#x20;     archivePrefix={arXiv},

&#x20;     primaryClass={cs.CL},

&#x20;     url={https://arxiv.org/abs/2505.09388}, 

}



@article{Qwen2.5-VL,

&#x20; title={Qwen2.5-VL Technical Report},

&#x20; author={Bai, Shuai and Chen, Keqin and Liu, Xuejing and Wang, Jialin and Ge, Wenbin and Song, Sibo and Dang, Kai and Wang, Peng and Wang, Shijie and Tang, Jun and Zhong, Humen and Zhu, Yuanzhi and Yang, Mingkun and Li, Zhaohai and Wan, Jianqiang and Wang, Pengfei and Ding, Wei and Fu, Zheren and Xu, Yiheng and Ye, Jiabo and Zhang, Xi and Xie, Tianbao and Cheng, Zesen and Zhang, Hang and Yang, Zhibo and Xu, Haiyang and Lin, Junyang},

&#x20; journal={arXiv preprint arXiv:2502.13923},

&#x20; year={2025}

}



@article{Qwen2VL,

&#x20; title={Qwen2-VL: Enhancing Vision-Language Model's Perception of the World at Any Resolution},

&#x20; author={Wang, Peng and Bai, Shuai and Tan, Sinan and Wang, Shijie and Fan, Zhihao and Bai, Jinze and Chen, Keqin and Liu, Xuejing and Wang, Jialin and Ge, Wenbin and Fan, Yang and Dang, Kai and Du, Mengfei and Ren, Xuancheng and Men, Rui and Liu, Dayiheng and Zhou, Chang and Zhou, Jingren and Lin, Junyang},

&#x20; journal={arXiv preprint arXiv:2409.12191},

&#x20; year={2024}

}



@article{Qwen-VL,

&#x20; title={Qwen-VL: A Versatile Vision-Language Model for Understanding, Localization, Text Reading, and Beyond},

&#x20; author={Bai, Jinze and Bai, Shuai and Yang, Shusheng and Wang, Shijie and Tan, Sinan and Wang, Peng and Lin, Junyang and Zhou, Chang and Zhou, Jingren},

&#x20; journal={arXiv preprint arXiv:2308.12966},

&#x20; year={2023}

}

```

