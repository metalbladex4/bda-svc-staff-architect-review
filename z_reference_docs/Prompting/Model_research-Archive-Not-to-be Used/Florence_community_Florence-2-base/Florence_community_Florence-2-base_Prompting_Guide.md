\# Florence-2



&#x20;   

&#x20;       

&#x20;       

&#x20;   



\## Overview



\[Florence-2](https://huggingface.co/papers/2311.06242) is an advanced vision foundation model that uses a prompt-based approach to handle a wide range of vision and vision-language tasks. Florence-2 can interpret simple text prompts to perform tasks like captioning, object detection, and segmentation. It leverages the FLD-5B dataset, containing 5.4 billion annotations across 126 million images, to master multi-task learning. The model's sequence-to-sequence architecture enables it to excel in both zero-shot and fine-tuned settings, proving to be a competitive vision foundation model.



You can find all the original Florence-2 checkpoints under the \[Florence-2](https://huggingface.co/models?other=florence-2) collection.



> \[!TIP]

> This model was contributed by \[ducviet00](https://huggingface.co/ducviet00).

> Click on the Florence-2 models in the right sidebar for more examples of how to apply Florence-2 to different vision and language tasks.



The example below demonstrates how to perform object detection with \[Pipeline](/docs/transformers/v5.3.0/en/main\_classes/pipelines#transformers.Pipeline) or the \[AutoModel](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoModel) class.



```py

import torch

import requests

from PIL import Image

from transformers import pipeline



pipeline = pipeline(

&#x20;   "image-text-to-text",

&#x20;   model="florence-community/Florence-2-base",

&#x20;   device=0,

&#x20;   dtype=torch.bfloat16

)



pipeline(

&#x20;   "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true",

&#x20;   text=""

)

```



```py

import torch

import requests

from PIL import Image

from transformers import AutoProcessor, Florence2ForConditionalGeneration



url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"

image = Image.open(requests.get(url, stream=True).raw).convert("RGB")



model = Florence2ForConditionalGeneration.from\_pretrained("florence-community/Florence-2-base", dtype=torch.bfloat16, device\_map="auto")

processor = AutoProcessor.from\_pretrained("florence-community/Florence-2-base")



task\_prompt = ""

inputs = processor(text=task\_prompt, images=image, return\_tensors="pt").to(model.device)



generated\_ids = model.generate(

&#x20;   \*\*inputs,

&#x20;   max\_new\_tokens=1024,

&#x20;   num\_beams=3,

)

generated\_text = processor.batch\_decode(generated\_ids, skip\_special\_tokens=False)\[0]



image\_size = image.size

parsed\_answer = processor.post\_process\_generation(generated\_text, task=task\_prompt, image\_size=image\_size)

print(parsed\_answer)

```



Quantization reduces the memory burden of large models by representing the weights in a lower precision. Refer to the \[Quantization](../quantization/overview) overview for more available quantization backends.



The example below uses \[bitsandbytes](../quantization/bitsandbytes) to quantize the model to 4-bit.



```py

\# pip install bitsandbytes

import torch

import requests

from PIL import Image

from transformers import AutoProcessor, Florence2ForConditionalGeneration, BitsAndBytesConfig



quantization\_config = BitsAndBytesConfig(load\_in\_4bit=True)



model = Florence2ForConditionalGeneration.from\_pretrained(

&#x20;   "florence-community/Florence-2-base",

&#x20;   dtype=torch.bfloat16,

&#x20;   device\_map="auto",

&#x20;   quantization\_config=quantization\_config

)

processor = AutoProcessor.from\_pretrained("florence-community/Florence-2-base")



url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg?download=true"

image = Image.open(requests.get(url, stream=True).raw).convert("RGB")



task\_prompt = ""

inputs = processor(text=task\_prompt, images=image, return\_tensors="pt").to(model.device, torch.bfloat16)



generated\_ids = model.generate(

&#x20;   \*\*inputs,

&#x20;   max\_new\_tokens=1024,

&#x20;   num\_beams=3,

)

generated\_text = processor.batch\_decode(generated\_ids, skip\_special\_tokens=False)\[0]



image\_size = image.size

parsed\_answer = processor.post\_process\_generation(generated\_text, task=task\_prompt, image\_size=image\_size)



print(parsed\_answer)

```



&#x20;   



\## Notes



\- Florence-2 is a prompt-based model. You need to provide a task prompt to tell the model what to do. Supported tasks are:

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

&#x20; - ``

\- The raw output of the model is a string that needs to be parsed. The \[Florence2Processor](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Processor) has a `post\_process\_generation()` method that can parse the string into a more usable format, like bounding boxes and labels for object detection.



\## Resources



\- \[Florence-2 technical report](https://huggingface.co/papers/2311.06242)

\- \[Jupyter Notebook for inference and visualization of Florence-2-large model](https://huggingface.co/microsoft/Florence-2-large/blob/main/sample\_inference.ipynb)



\## Florence2VisionConfig\[\[transformers.Florence2VisionConfig]]



\#### transformers.Florence2VisionConfig\[\[transformers.Florence2VisionConfig]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/configuration\_florence2.py#L28)



This is the configuration class to store the configuration of a `Florence2VisionModel`. It is used to instantiate a Florence2VisionModel

according to the specified arguments, defining the model architecture. Instantiating a configuration with the

defaults will yield a similar configuration to that of the Florence2VisionModel architecture.



Configuration objects inherit from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the

documentation from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) for more information.



Example:



```python

>>> from transformers import Florence2VisionConfig, Florence2VisionModel



>>> # Initializing a Florence2 Vision style configuration

>>> configuration = Florence2VisionConfig()



>>> # Initializing a model (with random weights)

>>> model = Florence2VisionModel(configuration)



>>> # Accessing the model configuration

>>> configuration = model.config

```



\*\*Parameters:\*\*



in\_channels (`int`, \*optional\*, defaults to 3) : Number of input image channels.



depths (`Tuple\[int]`, \*optional\*, defaults to `(1, 1, 9, 1)`) : The depth of the model.



patch\_size (`Tuple\[int]`, \*optional\*, defaults to `(7, 3, 3, 3)`) : The patch size of the image.



patch\_stride (`Tuple\[int]`, \*optional\*, defaults to `(4, 2, 2, 2)`) : The patch stride of the image.



patch\_padding (`Tuple\[int]`, \*optional\*, defaults to `(3, 1, 1, 1)`) : The patch padding of the image.



patch\_prenorm (`Tuple\[bool]`, \*optional\*, defaults to `(False, True, True, True)`) : Whether to apply layer normalization before the patch embedding layer.



embed\_dim (`Tuple\[int]`, \*optional\*, defaults to `(128, 256, 512, 1024)`) : The dimension of the embedding layer.



num\_heads (`Tuple\[int]`, \*optional\*, defaults to `(4, 8, 16, 32)`) : The number of attention heads.



num\_groups (`Tuple\[int]`, \*optional\*, defaults to `(4, 8, 16, 32)`) : The number of groups.



window\_size (`int`, \*optional\*, defaults to 12) : The window size of the model.



drop\_path\_rate (`float`, \*optional\*, defaults to 0.1) : The dropout rate of the drop path layer.



mlp\_ratio (`int`, \*optional\*, defaults to 4.0) : Ratio of mlp hidden dim to embedding dim.



qkv\_bias (`bool`, \*optional\*, defaults to `True`) : If True, add a learnable bias to query, key, value.



activation\_function (`str` or `function`, \*optional\*, defaults to `"gelu"`) : The non-linear activation function (function or string) in the encoder and pooler. If string, `"gelu"`, `"relu"`, `"silu"` and `"gelu\_new"` are supported.



projection\_dim (`int`, \*optional\*, defaults to 1024) : The dimension of the projection layer.



max\_temporal\_embeddings (`int`, \*optional\*, defaults to 100) : The configuration of the visual temporal embedding.



max\_position\_embeddings (`int`, \*optional\*, defaults to 50) : The configuration of the image position embedding.



initializer\_range (`float`, \*optional\*, defaults to 0.02) : The standard deviation of the truncated\_normal\_initializer for initializing all weight matrices.



\## Florence2Config\[\[transformers.Florence2Config]]



\#### transformers.Florence2Config\[\[transformers.Florence2Config]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/configuration\_florence2.py#L136)



This is the configuration class to store the configuration of a \[Florence2ForConditionalGeneration](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2ForConditionalGeneration). It is used to instantiate an

Florence-2 model according to the specified arguments, defining the model architecture.



Instantiating a configuration with the defaults will yield a similar configuration to that of the Florence-2

\[florence-community/Florence-2-base](https://huggingface.co/florence-community/Florence-2-base) architecture.



Configuration objects inherit from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the

documentation from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) for more information.



Example:



```python

>>> from transformers import Florence2ForConditionalGeneration, Florence2Config, CLIPVisionConfig, BartConfig



>>> # Initializing a clip-like vision config

>>> vision\_config = CLIPVisionConfig()



>>> # Initializing a Bart config

>>> text\_config = BartConfig()



>>> # Initializing a Florence-2 configuration

>>> configuration = Florence2Config(vision\_config, text\_config)



>>> # Initializing a model from the florence-2 configuration

>>> model = Florence2ForConditionalGeneration(configuration)



>>> # Accessing the model configuration

>>> configuration = model.config

```



\*\*Parameters:\*\*



text\_config (`dict`, \*optional\*) : Dictionary of configuration options used to initialize \[AutoConfig](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoConfig).



vision\_config (`dict`, \*optional\*) : Dictionary of configuration options used to initialize \[Florence2VisionConfig](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2VisionConfig).



image\_token\_id (`int`, \*optional\*, defaults to 51289) : The image token index to encode the image prompt.



is\_encoder\_decoder (bool, optional, \*optional\*, defaults to `True`) : Whether the model is used as an encoder/decoder or not.



tie\_word\_embeddings (`bool`, \*optional\*, defaults to `True`) : Whether to tie weight embeddings



\## Florence2Processor\[\[transformers.Florence2Processor]]



\#### transformers.Florence2Processor\[\[transformers.Florence2Processor]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/processing\_florence2.py#L45)



Constructs a Florence2Processor which wraps a image processor and a tokenizer into a single processor.



\[Florence2Processor](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Processor) offers all the functionalities of \[CLIPImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPImageProcessorFast) and \[BartTokenizer](/docs/transformers/v5.3.0/en/model\_doc/mvp#transformers.RobertaTokenizer). See the

\[\~CLIPImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPImageProcessorFast) and \[\~BartTokenizer](/docs/transformers/v5.3.0/en/model\_doc/mvp#transformers.RobertaTokenizer) for more information.



\_\_call\_\_transformers.Florence2Processor.\_\_call\_\_https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/processing\_florence2.py#L135\[{"name": "images", "val": ": typing.Union\[ForwardRef('PIL.Image.Image'), numpy.ndarray, ForwardRef('torch.Tensor'), list\['PIL.Image.Image'], list\[numpy.ndarray], list\['torch.Tensor'], NoneType] = None"}, {"name": "text", "val": ": str | list\[str] | list\[list\[str]] = None"}, {"name": "\*\*kwargs", "val": ": typing\_extensions.Unpack\[transformers.models.florence2.processing\_florence2.Florence2ProcessorKwargs]"}]- \*\*images\*\* (`Union\[PIL.Image.Image, numpy.ndarray, torch.Tensor, list\[PIL.Image.Image], list\[numpy.ndarray], list\[torch.Tensor]]`, \*optional\*) --

&#x20; Image to preprocess. Expects a single or batch of images with pixel values ranging from 0 to 255. If

&#x20; passing in images with pixel values between 0 and 1, set `do\_rescale=False`.

\- \*\*text\*\* (`Union\[str, list\[str], list\[list\[str]]]`, \*optional\*) --

&#x20; The sequence or batch of sequences to be encoded. Each sequence can be a string or a list of strings

&#x20; (pretokenized string). If you pass a pretokenized input, set `is\_split\_into\_words=True` to avoid ambiguity with batched inputs.

\- \*\*return\_tensors\*\* (`str` or \[TensorType](/docs/transformers/v5.3.0/en/internal/file\_utils#transformers.TensorType), \*optional\*) --

&#x20; If set, will return tensors of a particular framework. Acceptable values are:



&#x20; - `'pt'`: Return PyTorch `torch.Tensor` objects.

&#x20; - `'np'`: Return NumPy `np.ndarray` objects.

\- \*\*\*\*kwargs\*\* (\[ProcessingKwargs](/docs/transformers/v5.3.0/en/main\_classes/processors#transformers.ProcessingKwargs), \*optional\*) --

&#x20; Additional processing options for each modality (text, images, videos, audio). Model-specific parameters

&#x20; are listed above; see the TypedDict class for the complete list of supported arguments.0\[BatchFeature](/docs/transformers/v5.3.0/en/main\_classes/feature\_extractor#transformers.BatchFeature)A \[BatchFeature](/docs/transformers/v5.3.0/en/main\_classes/feature\_extractor#transformers.BatchFeature) with the following fields:



\- \*\*input\_ids\*\* -- List of token ids to be fed to a model. Returned when `text` is not `None`.

\- \*\*attention\_mask\*\* -- List of indices specifying which tokens should be attended to by the model (when

&#x20; `return\_attention\_mask=True` or if \*"attention\_mask"\* is in `self.model\_input\_names` and if `text` is not

&#x20; `None`).

\- \*\*pixel\_values\*\* -- Pixel values to be fed to a model. Returned when `images` is not `None`.



\*\*Parameters:\*\*



image\_processor (`CLIPImageProcessorFast`) : The image processor is a required input.



tokenizer (`BartTokenizer`) : The tokenizer is a required input.



num\_additional\_image\_tokens (`int`, \*optional\*, defaults to 0) : Number of additional tokens added to the image embeddings, such as CLS (+1). If the backbone has no CLS or other extra tokens appended, no need to set this arg.



post\_processor\_config (`dict`,  \*optional\*, defaults to 0) : Task-specific parsing rules for `Florence2PostProcessor`, e.g. regex patterns, thresholds, or banned tokens.



\*\*Returns:\*\*



`\[BatchFeature](/docs/transformers/v5.3.0/en/main\_classes/feature\_extractor#transformers.BatchFeature)`



A \[BatchFeature](/docs/transformers/v5.3.0/en/main\_classes/feature\_extractor#transformers.BatchFeature) with the following fields:



\- \*\*input\_ids\*\* -- List of token ids to be fed to a model. Returned when `text` is not `None`.

\- \*\*attention\_mask\*\* -- List of indices specifying which tokens should be attended to by the model (when

&#x20; `return\_attention\_mask=True` or if \*"attention\_mask"\* is in `self.model\_input\_names` and if `text` is not

&#x20; `None`).

\- \*\*pixel\_values\*\* -- Pixel values to be fed to a model. Returned when `images` is not `None`.



\## Florence2Model\[\[transformers.Florence2Model]]



\#### transformers.Florence2Model\[\[transformers.Florence2Model]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/modeling\_florence2.py#L669)



Florence-2 is a vision model for captioning, detection, and segmentation.



This model inherits from \[PreTrainedModel](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the

library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads

etc.)



This model is also a PyTorch \[torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.

Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage

and behavior.



forwardtransformers.Florence2Model.forwardhttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/modeling\_florence2.py#L726\[{"name": "input\_ids", "val": ": torch.LongTensor | None = None"}, {"name": "pixel\_values", "val": ": torch.FloatTensor | None = None"}, {"name": "attention\_mask", "val": ": torch.Tensor | None = None"}, {"name": "decoder\_input\_ids", "val": ": torch.LongTensor | None = None"}, {"name": "decoder\_attention\_mask", "val": ": torch.LongTensor | None = None"}, {"name": "decoder\_inputs\_embeds", "val": ": torch.FloatTensor | None = None"}, {"name": "encoder\_outputs", "val": ": list\[torch.FloatTensor] | None = None"}, {"name": "past\_key\_values", "val": ": transformers.cache\_utils.Cache | None = None"}, {"name": "inputs\_embeds", "val": ": torch.FloatTensor | None = None"}, {"name": "use\_cache", "val": ": bool | None = None"}, {"name": "output\_attentions", "val": ": bool | None = None"}, {"name": "output\_hidden\_states", "val": ": bool | None = None"}, {"name": "return\_dict", "val": ": bool | None = None"}, {"name": "cache\_position", "val": ": torch.LongTensor | None = None"}, {"name": "\*\*kwargs", "val": ""}]- \*\*input\_ids\*\* (`torch.LongTensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.



&#x20; Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and

&#x20; \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details.



&#x20; \[What are input IDs?](../glossary#input-ids)

\- \*\*pixel\_values\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`, \*optional\*) --

&#x20; The tensors corresponding to the input images. Pixel values can be obtained using

&#x20; \[CLIPImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPImageProcessorFast). See \[CLIPImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Florence2Processor](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Processor) uses

&#x20; \[CLIPImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPImageProcessorFast) for processing images).

\- \*\*attention\_mask\*\* (`torch.Tensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:



&#x20; - 1 for tokens that are \*\*not masked\*\*,

&#x20; - 0 for tokens that are \*\*masked\*\*.



&#x20; \[What are attention masks?](../glossary#attention-mask)

\- \*\*decoder\_input\_ids\*\* (`torch.LongTensor` of shape `(batch\_size, target\_sequence\_length)`, \*optional\*) --

&#x20; Indices of decoder input sequence tokens in the vocabulary.



&#x20; Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and

&#x20; \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details.



&#x20; \[What are decoder input IDs?](../glossary#decoder-input-ids)

\- \*\*decoder\_attention\_mask\*\* (`torch.LongTensor` of shape `(batch\_size, target\_sequence\_length)`, \*optional\*) --

&#x20; Mask to avoid performing attention on certain token indices. By default, a causal mask will be used, to

&#x20; make sure the model can only look at previous inputs in order to predict the future.

\- \*\*decoder\_inputs\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, target\_sequence\_length, hidden\_size)`, \*optional\*) --

&#x20; Optionally, instead of passing `decoder\_input\_ids` you can choose to directly pass an embedded

&#x20; representation. If `past\_key\_values` is used, optionally only the last `decoder\_inputs\_embeds` have to be

&#x20; input (see `past\_key\_values`). This is useful if you want more control over how to convert

&#x20; `decoder\_input\_ids` indices into associated vectors than the model's internal embedding lookup matrix.



&#x20; If `decoder\_input\_ids` and `decoder\_inputs\_embeds` are both unset, `decoder\_inputs\_embeds` takes the value

&#x20; of `inputs\_embeds`.

\- \*\*encoder\_outputs\*\* (`list\[torch.FloatTensor]`, \*optional\*) --

&#x20; Tuple consists of (`last\_hidden\_state`, \*optional\*: `hidden\_states`, \*optional\*: `attentions`)

&#x20; `last\_hidden\_state` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) is a sequence of

&#x20; hidden-states at the output of the last layer of the encoder. Used in the cross-attention of the decoder.

\- \*\*past\_key\_values\*\* (`\~cache\_utils.Cache`, \*optional\*) --

&#x20; Pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention

&#x20; blocks) that can be used to speed up sequential decoding. This typically consists in the `past\_key\_values`

&#x20; returned by the model at a previous stage of decoding, when `use\_cache=True` or `config.use\_cache=True`.



&#x20; Only \[Cache](/docs/transformers/v5.3.0/en/internal/generation\_utils#transformers.Cache) instance is allowed as input, see our \[kv cache guide](https://huggingface.co/docs/transformers/en/kv\_cache).

&#x20; If no `past\_key\_values` are passed, \[DynamicCache](/docs/transformers/v5.3.0/en/internal/generation\_utils#transformers.DynamicCache) will be initialized by default.



&#x20; The model will output the same cache format that is fed as input.



&#x20; If `past\_key\_values` are used, the user is expected to input only unprocessed `input\_ids` (those that don't

&#x20; have their past key value states given to this model) of shape `(batch\_size, unprocessed\_length)` instead of all `input\_ids`

&#x20; of shape `(batch\_size, sequence\_length)`.

\- \*\*inputs\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) --

&#x20; Optionally, instead of passing `input\_ids` you can choose to directly pass an embedded representation. This

&#x20; is useful if you want more control over how to convert `input\_ids` indices into associated vectors than the

&#x20; model's internal embedding lookup matrix.

\- \*\*use\_cache\*\* (`bool`, \*optional\*) --

&#x20; If set to `True`, `past\_key\_values` key value states are returned and can be used to speed up decoding (see

&#x20; `past\_key\_values`).

\- \*\*output\_attentions\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned

&#x20; tensors for more detail.

\- \*\*output\_hidden\_states\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for

&#x20; more detail.

\- \*\*return\_dict\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.

\- \*\*cache\_position\*\* (`torch.LongTensor` of shape `(sequence\_length)`, \*optional\*) --

&#x20; Indices depicting the position of the input sequence tokens in the sequence. Contrarily to `position\_ids`,

&#x20; this tensor is not affected by padding. It is used to update the cache in the correct position and to infer

&#x20; the complete sequence length.0`Florence2Seq2SeqModelOutput` or `tuple(torch.FloatTensor)`A `Florence2Seq2SeqModelOutput` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Florence2Config](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Config)) and inputs.

The \[Florence2Model](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Model) forward method, overrides the `\_\_call\_\_` special method.



Although the recipe for forward pass needs to be defined within this function, one should call the `Module`

instance afterwards instead of this since the former takes care of running the pre and post processing steps while

the latter silently ignores them.



\- \*\*last\_hidden\_state\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) -- Sequence of hidden-states at the output of the last layer of the model.

\- \*\*past\_key\_values\*\* (`\~cache\_utils.EncoderDecoderCache`, \*optional\*, returned when `use\_cache=True` is passed or when `config.use\_cache=True`) -- It is a \[Cache](/docs/transformers/v5.3.0/en/internal/generation\_utils#transformers.Cache) instance. For more details, see our \[kv cache guide](https://huggingface.co/docs/transformers/en/kv\_cache).



&#x20; Contains pre-computed hidden-states (key and values in the self-attention blocks and optionally if

&#x20; `config.is\_encoder\_decoder=True` in the cross-attention blocks) that can be used (see `past\_key\_values`

&#x20; input) to speed up sequential decoding.

\- \*\*decoder\_hidden\_states\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_hidden\_states=True` is passed or when `config.output\_hidden\_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +

&#x20; one for the output of each layer) of shape `(batch\_size, sequence\_length, hidden\_size)`.



&#x20; Hidden-states of the decoder at the output of each layer plus the initial embedding outputs.

\- \*\*decoder\_attentions\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch\_size, num\_heads, sequence\_length,

&#x20; sequence\_length)`.



&#x20; Attentions weights of the decoder, after the attention softmax, used to compute the weighted average in the

&#x20; self-attention heads.

\- \*\*cross\_attentions\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch\_size, num\_heads, sequence\_length,

&#x20; sequence\_length)`.



&#x20; Attentions weights of the decoder's cross-attention layer, after the attention softmax, used to compute the

&#x20; weighted average in the cross-attention heads.

\- \*\*encoder\_last\_hidden\_state\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) -- Sequence of hidden-states at the output of the last layer of the encoder of the model.

\- \*\*encoder\_hidden\_states\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_hidden\_states=True` is passed or when `config.output\_hidden\_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +

&#x20; one for the output of each layer) of shape `(batch\_size, sequence\_length, hidden\_size)`.



&#x20; Hidden-states of the encoder at the output of each layer plus the initial embedding outputs.

\- \*\*encoder\_attentions\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch\_size, num\_heads, sequence\_length,

&#x20; sequence\_length)`.



&#x20; Attentions weights of the encoder, after the attention softmax, used to compute the weighted average in the

&#x20; self-attention heads.

\- \*\*image\_hidden\_states\*\* (`torch.FloatTensor`, \*optional\*) -- A `torch.FloatTensor` of size `(batch\_size, num\_image\_tokens, hidden\_size)`.

&#x20; image\_hidden\_states of the model produced by the vision encoder and after projecting the last hidden state.



\*\*Parameters:\*\*



config (\[Florence2Config](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Config)) : Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the \[from\_pretrained()](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel.from\_pretrained) method to load the model weights.



\*\*Returns:\*\*



``Florence2Seq2SeqModelOutput` or `tuple(torch.FloatTensor)``



A `Florence2Seq2SeqModelOutput` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Florence2Config](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Config)) and inputs.

\#### get\_image\_features\[\[transformers.Florence2Model.get\_image\_features]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/modeling\_florence2.py#L686)



Obtains image last hidden states from the vision tower and apply multimodal projection.



\- \*\*last\_hidden\_state\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, hidden\_size)`) -- Sequence of hidden-states at the output of the last layer of the model.

\- \*\*pooler\_output\*\* (`torch.FloatTensor` of shape `(batch\_size, hidden\_size)`) -- Last layer hidden-state of the first token of the sequence (classification token) after further processing

&#x20; through the layers used for the auxiliary pretraining task. E.g. for BERT-family of models, this returns

&#x20; the classification token after processing through a linear layer and a tanh activation function. The linear

&#x20; layer weights are trained from the next sentence prediction (classification) objective during pretraining.

\- \*\*hidden\_states\*\* (`tuple(torch.FloatTensor)`, \*optional\*, returned when `output\_hidden\_states=True` is passed or when `config.output\_hidden\_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +

&#x20; one for the output of each layer) of shape `(batch\_size, sequence\_length, hidden\_size)`.



&#x20; Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.

\- \*\*attentions\*\* (`tuple(torch.FloatTensor)`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch\_size, num\_heads, sequence\_length,

&#x20; sequence\_length)`.



&#x20; Attentions weights after the attention softmax, used to compute the weighted average in the self-attention

&#x20; heads.



\*\*Parameters:\*\*



pixel\_values (`torch.FloatTensor]` of shape `(batch\_size, channels, height, width)`) : The tensors corresponding to the input images.



\*\*Returns:\*\*



`\[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)``



A \[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Florence2Config](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Config)) and inputs.



\## Florence2ForConditionalGeneration\[\[transformers.Florence2ForConditionalGeneration]]



\#### transformers.Florence2ForConditionalGeneration\[\[transformers.Florence2ForConditionalGeneration]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/modeling\_florence2.py#L834)



Florence-2 is a vision model for captioning, detection, and segmentation.



This model inherits from \[PreTrainedModel](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the

library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads

etc.)



This model is also a PyTorch \[torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.

Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage

and behavior.



forwardtransformers.Florence2ForConditionalGeneration.forwardhttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/modeling\_florence2.py#L861\[{"name": "input\_ids", "val": ": torch.LongTensor | None = None"}, {"name": "pixel\_values", "val": ": torch.FloatTensor | None = None"}, {"name": "attention\_mask", "val": ": torch.Tensor | None = None"}, {"name": "decoder\_input\_ids", "val": ": torch.LongTensor | None = None"}, {"name": "decoder\_attention\_mask", "val": ": torch.LongTensor | None = None"}, {"name": "encoder\_outputs", "val": ": list\[torch.FloatTensor] | None = None"}, {"name": "past\_key\_values", "val": ": transformers.cache\_utils.Cache | None = None"}, {"name": "inputs\_embeds", "val": ": torch.FloatTensor | None = None"}, {"name": "decoder\_inputs\_embeds", "val": ": torch.FloatTensor | None = None"}, {"name": "labels", "val": ": torch.LongTensor | None = None"}, {"name": "use\_cache", "val": ": bool | None = None"}, {"name": "output\_attentions", "val": ": bool | None = None"}, {"name": "output\_hidden\_states", "val": ": bool | None = None"}, {"name": "return\_dict", "val": ": bool | None = None"}, {"name": "cache\_position", "val": ": torch.LongTensor | None = None"}, {"name": "logits\_to\_keep", "val": ": int | torch.Tensor = 0"}, {"name": "\*\*kwargs", "val": ": typing\_extensions.Unpack\[transformers.utils.generic.TransformersKwargs]"}]- \*\*input\_ids\*\* (`torch.LongTensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.



&#x20; Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and

&#x20; \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details.



&#x20; \[What are input IDs?](../glossary#input-ids)

\- \*\*pixel\_values\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`, \*optional\*) --

&#x20; The tensors corresponding to the input images. Pixel values can be obtained using

&#x20; \[CLIPImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPImageProcessorFast). See \[CLIPImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Florence2Processor](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Processor) uses

&#x20; \[CLIPImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPImageProcessorFast) for processing images).

\- \*\*attention\_mask\*\* (`torch.Tensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:



&#x20; - 1 for tokens that are \*\*not masked\*\*,

&#x20; - 0 for tokens that are \*\*masked\*\*.



&#x20; \[What are attention masks?](../glossary#attention-mask)

\- \*\*decoder\_input\_ids\*\* (`torch.LongTensor` of shape `(batch\_size, target\_sequence\_length)`, \*optional\*) --

&#x20; Indices of decoder input sequence tokens in the vocabulary.



&#x20; Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and

&#x20; \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details.



&#x20; \[What are decoder input IDs?](../glossary#decoder-input-ids)

\- \*\*decoder\_attention\_mask\*\* (`torch.LongTensor` of shape `(batch\_size, target\_sequence\_length)`, \*optional\*) --

&#x20; Mask to avoid performing attention on certain token indices. By default, a causal mask will be used, to

&#x20; make sure the model can only look at previous inputs in order to predict the future.

\- \*\*encoder\_outputs\*\* (`list\[torch.FloatTensor]`, \*optional\*) --

&#x20; Tuple consists of (`last\_hidden\_state`, \*optional\*: `hidden\_states`, \*optional\*: `attentions`)

&#x20; `last\_hidden\_state` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) is a sequence of

&#x20; hidden-states at the output of the last layer of the encoder. Used in the cross-attention of the decoder.

\- \*\*past\_key\_values\*\* (`\~cache\_utils.Cache`, \*optional\*) --

&#x20; Pre-computed hidden-states (key and values in the self-attention blocks and in the cross-attention

&#x20; blocks) that can be used to speed up sequential decoding. This typically consists in the `past\_key\_values`

&#x20; returned by the model at a previous stage of decoding, when `use\_cache=True` or `config.use\_cache=True`.



&#x20; Only \[Cache](/docs/transformers/v5.3.0/en/internal/generation\_utils#transformers.Cache) instance is allowed as input, see our \[kv cache guide](https://huggingface.co/docs/transformers/en/kv\_cache).

&#x20; If no `past\_key\_values` are passed, \[DynamicCache](/docs/transformers/v5.3.0/en/internal/generation\_utils#transformers.DynamicCache) will be initialized by default.



&#x20; The model will output the same cache format that is fed as input.



&#x20; If `past\_key\_values` are used, the user is expected to input only unprocessed `input\_ids` (those that don't

&#x20; have their past key value states given to this model) of shape `(batch\_size, unprocessed\_length)` instead of all `input\_ids`

&#x20; of shape `(batch\_size, sequence\_length)`.

\- \*\*inputs\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) --

&#x20; Optionally, instead of passing `input\_ids` you can choose to directly pass an embedded representation. This

&#x20; is useful if you want more control over how to convert `input\_ids` indices into associated vectors than the

&#x20; model's internal embedding lookup matrix.

\- \*\*decoder\_inputs\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, target\_sequence\_length, hidden\_size)`, \*optional\*) --

&#x20; Optionally, instead of passing `decoder\_input\_ids` you can choose to directly pass an embedded

&#x20; representation. If `past\_key\_values` is used, optionally only the last `decoder\_inputs\_embeds` have to be

&#x20; input (see `past\_key\_values`). This is useful if you want more control over how to convert

&#x20; `decoder\_input\_ids` indices into associated vectors than the model's internal embedding lookup matrix.



&#x20; If `decoder\_input\_ids` and `decoder\_inputs\_embeds` are both unset, `decoder\_inputs\_embeds` takes the value

&#x20; of `inputs\_embeds`.

\- \*\*labels\*\* (`torch.LongTensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Labels for computing the masked language modeling loss. Indices should either be in `\[0, ...,

&#x20; config.vocab\_size]` or -100 (see `input\_ids` docstring). Tokens with indices set to `-100` are ignored

&#x20; (masked), the loss is only computed for the tokens with labels in `\[0, ..., config.vocab\_size]`.

\- \*\*use\_cache\*\* (`bool`, \*optional\*) --

&#x20; If set to `True`, `past\_key\_values` key value states are returned and can be used to speed up decoding (see

&#x20; `past\_key\_values`).

\- \*\*output\_attentions\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned

&#x20; tensors for more detail.

\- \*\*output\_hidden\_states\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for

&#x20; more detail.

\- \*\*return\_dict\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.

\- \*\*cache\_position\*\* (`torch.LongTensor` of shape `(sequence\_length)`, \*optional\*) --

&#x20; Indices depicting the position of the input sequence tokens in the sequence. Contrarily to `position\_ids`,

&#x20; this tensor is not affected by padding. It is used to update the cache in the correct position and to infer

&#x20; the complete sequence length.

\- \*\*logits\_to\_keep\*\* (`Union\[int, torch.Tensor]`, \*optional\*, defaults to `0`) --

&#x20; If an `int`, compute logits for the last `logits\_to\_keep` tokens. If `0`, calculate logits for all

&#x20; `input\_ids` (special case). Only last token logits are needed for generation, and calculating them only for that

&#x20; token can save memory, which becomes pretty significant for long sequences or large vocabulary size.

&#x20; If a `torch.Tensor`, must be 1D corresponding to the indices to keep in the sequence length dimension.

&#x20; This is useful when using packed tensor format (single dimension for batch and sequence length).0`Florence2Seq2SeqLMOutput` or `tuple(torch.FloatTensor)`A `Florence2Seq2SeqLMOutput` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Florence2Config](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Config)) and inputs.

The \[Florence2ForConditionalGeneration](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2ForConditionalGeneration) forward method, overrides the `\_\_call\_\_` special method.



Although the recipe for forward pass needs to be defined within this function, one should call the `Module`

instance afterwards instead of this since the former takes care of running the pre and post processing steps while

the latter silently ignores them.



\- \*\*loss\*\* (`torch.FloatTensor` of shape `(1,)`, \*optional\*, returned when `labels` is provided) -- Language modeling loss (for next-token prediction).

\- \*\*logits\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, config.vocab\_size)`) -- Prediction scores of the language modeling head (scores for each vocabulary token before SoftMax).

\- \*\*past\_key\_values\*\* (`\~cache\_utils.EncoderDecoderCache`, \*optional\*, returned when `use\_cache=True` is passed or when `config.use\_cache=True`) -- It is a \[Cache](/docs/transformers/v5.3.0/en/internal/generation\_utils#transformers.Cache) instance. For more details, see our \[kv cache guide](https://huggingface.co/docs/transformers/en/kv\_cache).



&#x20; Contains pre-computed hidden-states (key and values in the self-attention blocks and optionally if

&#x20; `config.is\_encoder\_decoder=True` in the cross-attention blocks) that can be used (see `past\_key\_values`

&#x20; input) to speed up sequential decoding.

\- \*\*decoder\_hidden\_states\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_hidden\_states=True` is passed or when `config.output\_hidden\_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +

&#x20; one for the output of each layer) of shape `(batch\_size, sequence\_length, hidden\_size)`.



&#x20; Hidden-states of the decoder at the output of each layer plus the initial embedding outputs.

\- \*\*decoder\_attentions\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch\_size, num\_heads, sequence\_length,

&#x20; sequence\_length)`.



&#x20; Attentions weights of the decoder, after the attention softmax, used to compute the weighted average in the

&#x20; self-attention heads.

\- \*\*cross\_attentions\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch\_size, num\_heads, sequence\_length,

&#x20; sequence\_length)`.



&#x20; Attentions weights of the decoder's cross-attention layer, after the attention softmax, used to compute the

&#x20; weighted average in the cross-attention heads.

\- \*\*encoder\_last\_hidden\_state\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) -- Sequence of hidden-states at the output of the last layer of the encoder of the model.

\- \*\*encoder\_hidden\_states\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_hidden\_states=True` is passed or when `config.output\_hidden\_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +

&#x20; one for the output of each layer) of shape `(batch\_size, sequence\_length, hidden\_size)`.



&#x20; Hidden-states of the encoder at the output of each layer plus the initial embedding outputs.

\- \*\*encoder\_attentions\*\* (`tuple\[torch.FloatTensor, ...]`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch\_size, num\_heads, sequence\_length,

&#x20; sequence\_length)`.



&#x20; Attentions weights of the encoder, after the attention softmax, used to compute the weighted average in the

&#x20; self-attention heads.

\- \*\*image\_hidden\_states\*\* (`torch.FloatTensor`, \*optional\*) -- A `torch.FloatTensor` of size `(batch\_size, num\_image\_tokens, hidden\_size)`.

&#x20; image\_hidden\_states of the model produced by the vision encoder and after projecting the last hidden state.



Example:



```python

>>> from PIL import Image

>>> import httpx

>>> from io import BytesIO

>>> from transformers import AutoProcessor, Florence2ForConditionalGeneration



>>> model = Florence2ForConditionalGeneration.from\_pretrained("florence-community/Florence-2-large")

>>> processor = AutoProcessor.from\_pretrained("florence-community/Florence-2-large")



>>> prompt = ""

>>> url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/car.jpg"

>>> with httpx.stream("GET", url) as response:

...     image = Image.open(BytesIO(response.read()))



>>> inputs = processor(text=prompt, images=image, return\_tensors="pt")



>>> # Generate

>>> generate\_ids = model.generate(\*\*inputs, max\_length=100)

>>> processor.batch\_decode(generate\_ids, skip\_special\_tokens=True, clean\_up\_tokenization\_spaces=False)\[0]

"A green car parked in front of a yellow building."

```



\*\*Parameters:\*\*



config (\[Florence2Config](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Config)) : Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the \[from\_pretrained()](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel.from\_pretrained) method to load the model weights.



\*\*Returns:\*\*



``Florence2Seq2SeqLMOutput` or `tuple(torch.FloatTensor)``



A `Florence2Seq2SeqLMOutput` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Florence2Config](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Config)) and inputs.

\#### get\_image\_features\[\[transformers.Florence2ForConditionalGeneration.get\_image\_features]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/modeling\_florence2.py#L855)



\- \*\*last\_hidden\_state\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, hidden\_size)`) -- Sequence of hidden-states at the output of the last layer of the model.

\- \*\*pooler\_output\*\* (`torch.FloatTensor` of shape `(batch\_size, hidden\_size)`) -- Last layer hidden-state of the first token of the sequence (classification token) after further processing

&#x20; through the layers used for the auxiliary pretraining task. E.g. for BERT-family of models, this returns

&#x20; the classification token after processing through a linear layer and a tanh activation function. The linear

&#x20; layer weights are trained from the next sentence prediction (classification) objective during pretraining.

\- \*\*hidden\_states\*\* (`tuple(torch.FloatTensor)`, \*optional\*, returned when `output\_hidden\_states=True` is passed or when `config.output\_hidden\_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +

&#x20; one for the output of each layer) of shape `(batch\_size, sequence\_length, hidden\_size)`.



&#x20; Hidden-states of the model at the output of each layer plus the optional initial embedding outputs.

\- \*\*attentions\*\* (`tuple(torch.FloatTensor)`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch\_size, num\_heads, sequence\_length,

&#x20; sequence\_length)`.



&#x20; Attentions weights after the attention softmax, used to compute the weighted average in the self-attention

&#x20; heads.



Example:



```python

>>> from PIL import Image

>>> from transformers import AutoProcessor, Florence2ForConditionalGeneration



>>> model = Florence2ForConditionalGeneration.from\_pretrained("florence-community/Florence-2-base")

>>> processor = AutoProcessor.from\_pretrained("florence-community/Florence-2-base")



>>> messages = \[

...     {

...         "role": "user", "content": \[

...             {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/pipeline-cat-chonk.jpeg"},

...             {"type": "text", "text": "Where is the cat standing?"},

...         ]

...     },

... ]



>>> inputs = processor.apply\_chat\_template(

...     messages,

...     tokenize=True,

...     return\_dict=True,

...     return\_tensors="pt",

...     add\_generation\_prompt=True

... )

>>> # Generate

>>> generate\_ids = model.generate(\*\*inputs)

>>> processor.batch\_decode(generate\_ids, skip\_special\_tokens=True)\[0]

```



\*\*Parameters:\*\*



pixel\_values (`torch.Tensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`) : The tensors corresponding to the input images. Pixel values can be obtained using \[CLIPImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPImageProcessorFast). See \[CLIPImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Florence2Processor](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Processor) uses \[CLIPImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPImageProcessorFast) for processing images).



\*\*Returns:\*\*



`\[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)``



A \[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Florence2Config](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2Config)) and inputs.



\## Florence2VisionBackbone\[\[transformers.Florence2VisionBackbone]]



\#### transformers.Florence2VisionBackbone\[\[transformers.Florence2VisionBackbone]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/modeling\_florence2.py#L509)



The Florence2 backbone.



This model inherits from \[PreTrainedModel](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the

library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads

etc.)



This model is also a PyTorch \[torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.

Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage

and behavior.



forwardtransformers.Florence2VisionBackbone.forwardhttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/florence2/modeling\_florence2.py#L556\[{"name": "hidden\_states", "val": ": Tensor"}, {"name": "\*\*kwargs", "val": ": typing\_extensions.Unpack\[transformers.utils.generic.TransformersKwargs]"}]



\*\*Parameters:\*\*



config (\[Florence2VisionConfig](/docs/transformers/v5.3.0/en/model\_doc/florence2#transformers.Florence2VisionConfig)) : Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the \[from\_pretrained()](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel.from\_pretrained) method to load the model weights.





