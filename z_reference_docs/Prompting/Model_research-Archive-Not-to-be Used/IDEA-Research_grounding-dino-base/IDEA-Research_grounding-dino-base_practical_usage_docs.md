\# Grounding DINO



\## Overview



The Grounding DINO model was proposed in \[Grounding DINO: Marrying DINO with Grounded Pre-Training for Open-Set Object Detection](https://huggingface.co/papers/2303.05499) by Shilong Liu, Zhaoyang Zeng, Tianhe Ren, Feng Li, Hao Zhang, Jie Yang, Chunyuan Li, Jianwei Yang, Hang Su, Jun Zhu, Lei Zhang. Grounding DINO extends a closed-set object detection model with a text encoder, enabling open-set object detection. The model achieves remarkable results, such as 52.5 AP on COCO zero-shot.



The abstract from the paper is the following:



\*In this paper, we present an open-set object detector, called Grounding DINO, by marrying Transformer-based detector DINO with grounded pre-training, which can detect arbitrary objects with human inputs such as category names or referring expressions. The key solution of open-set object detection is introducing language to a closed-set detector for open-set concept generalization. To effectively fuse language and vision modalities, we conceptually divide a closed-set detector into three phases and propose a tight fusion solution, which includes a feature enhancer, a language-guided query selection, and a cross-modality decoder for cross-modality fusion. While previous works mainly evaluate open-set object detection on novel categories, we propose to also perform evaluations on referring expression comprehension for objects specified with attributes. Grounding DINO performs remarkably well on all three settings, including benchmarks on COCO, LVIS, ODinW, and RefCOCO/+/g. Grounding DINO achieves a 52.5 AP on the COCO detection zero-shot transfer benchmark, i.e., without any training data from COCO. It sets a new record on the ODinW zero-shot benchmark with a mean 26.1 AP.\*



&#x20;Grounding DINO overview. Taken from the original paper. 



This model was contributed by \[EduardoPacheco](https://huggingface.co/EduardoPacheco) and \[nielsr](https://huggingface.co/nielsr).

The original code can be found \[here](https://github.com/IDEA-Research/GroundingDINO).



\## Usage tips



\- One can use \[GroundingDinoProcessor](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoProcessor) to prepare image-text pairs for the model.

\- To separate classes in the text use a period e.g. "a cat. a dog."

\- When using multiple classes (e.g. `"a cat. a dog."`), use `post\_process\_grounded\_object\_detection` from \[GroundingDinoProcessor](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoProcessor) to post process outputs. Since, the labels returned from `post\_process\_object\_detection` represent the indices from the model dimension where prob > threshold.



Here's how to use the model for zero-shot object detection:



```python

>>> import requests



>>> import torch

>>> from PIL import Image

>>> from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection

from accelerate import Accelerator



>>> model\_id = "IDEA-Research/grounding-dino-tiny"

>>> device = Accelerator().device



>>> processor = AutoProcessor.from\_pretrained(model\_id)

>>> model = AutoModelForZeroShotObjectDetection.from\_pretrained(model\_id).to(device)



>>> image\_url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> image = Image.open(requests.get(image\_url, stream=True).raw)

>>> # Check for cats and remote controls

>>> text\_labels = \[\["a cat", "a remote control"]]



>>> inputs = processor(images=image, text=text\_labels, return\_tensors="pt").to(model.device)

>>> with torch.no\_grad():

...     outputs = model(\*\*inputs)



>>> results = processor.post\_process\_grounded\_object\_detection(

...     outputs,

...     inputs.input\_ids,

...     threshold=0.4,

...     text\_threshold=0.3,

...     target\_sizes=\[image.size\[::-1]]

... )



\# Retrieve the first image result

>>> result = results\[0]

>>> for box, score, labels in zip(result\["boxes"], result\["scores"], result\["labels"]):

...     box = \[round(x, 2) for x in box.tolist()]

...     print(f"Detected {labels} with confidence {round(score.item(), 3)} at location {box}")

Detected a cat with confidence 0.468 at location \[344.78, 22.9, 637.3, 373.62]

Detected a cat with confidence 0.426 at location \[11.74, 51.55, 316.51, 473.22]

```



\## Grounded SAM



One can combine Grounding DINO with the \[Segment Anything](sam) model for text-based mask generation as introduced in \[Grounded SAM: Assembling Open-World Models for Diverse Visual Tasks](https://huggingface.co/papers/2401.14159). You can refer to this \[demo notebook](https://github.com/NielsRogge/Transformers-Tutorials/blob/master/Grounding%20DINO/GroundingDINO\_with\_Segment\_Anything.ipynb) 🌍 for details.



&#x20;Grounded SAM overview. Taken from the original repository. 



\## Resources



A list of official Hugging Face and community (indicated by 🌎) resources to help you get started with Grounding DINO. If you're interested in submitting a resource to be included here, please feel free to open a Pull Request and we'll review it! The resource should ideally demonstrate something new instead of duplicating an existing resource.



\- Demo notebooks regarding inference with Grounding DINO as well as combining it with \[SAM](sam) can be found \[here](https://github.com/NielsRogge/Transformers-Tutorials/tree/master/Grounding%20DINO). 🌎



\## GroundingDinoImageProcessor\[\[transformers.GroundingDinoImageProcessor]]



\#### transformers.GroundingDinoImageProcessor\[\[transformers.GroundingDinoImageProcessor]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/image\_processing\_grounding\_dino.py#L795)



Constructs a Grounding DINO image processor.



preprocesstransformers.GroundingDinoImageProcessor.preprocesshttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/image\_processing\_grounding\_dino.py#L1220\[{"name": "images", "val": ": typing.Union\[ForwardRef('PIL.Image.Image'), numpy.ndarray, ForwardRef('torch.Tensor'), list\['PIL.Image.Image'], list\[numpy.ndarray], list\['torch.Tensor']]"}, {"name": "annotations", "val": ": dict\[str, int | str | list\[dict]] | list\[dict\[str, int | str | list\[dict]]] | None = None"}, {"name": "return\_segmentation\_masks", "val": ": bool | None = None"}, {"name": "masks\_path", "val": ": str | pathlib.Path | None = None"}, {"name": "do\_resize", "val": ": bool | None = None"}, {"name": "size", "val": ": dict\[str, int] | None = None"}, {"name": "resample", "val": " = None"}, {"name": "do\_rescale", "val": ": bool | None = None"}, {"name": "rescale\_factor", "val": ": int | float | None = None"}, {"name": "do\_normalize", "val": ": bool | None = None"}, {"name": "do\_convert\_annotations", "val": ": bool | None = None"}, {"name": "image\_mean", "val": ": float | list\[float] | None = None"}, {"name": "image\_std", "val": ": float | list\[float] | None = None"}, {"name": "do\_pad", "val": ": bool | None = None"}, {"name": "format", "val": ": str | transformers.models.grounding\_dino.image\_processing\_grounding\_dino.AnnotationFormat | None = None"}, {"name": "return\_tensors", "val": ": transformers.utils.generic.TensorType | str | None = None"}, {"name": "data\_format", "val": ": str | transformers.image\_utils.ChannelDimension = "}, {"name": "input\_data\_format", "val": ": str | transformers.image\_utils.ChannelDimension | None = None"}, {"name": "pad\_size", "val": ": dict\[str, int] | None = None"}, {"name": "\*\*kwargs", "val": ""}]- \*\*images\*\* (`ImageInput`) --

&#x20; Image or batch of images to preprocess. Expects a single or batch of images with pixel values ranging

&#x20; from 0 to 255. If passing in images with pixel values between 0 and 1, set `do\_rescale=False`.

\- \*\*annotations\*\* (`AnnotationType` or `list\[AnnotationType]`, \*optional\*) --

&#x20; List of annotations associated with the image or batch of images. If annotation is for object

&#x20; detection, the annotations should be a dictionary with the following keys:

&#x20; - "image\_id" (`int`): The image id.

&#x20; - "annotations" (`list\[Dict]`): List of annotations for an image. Each annotation should be a

&#x20;   dictionary. An image can have no annotations, in which case the list should be empty.

&#x20; If annotation is for segmentation, the annotations should be a dictionary with the following keys:

&#x20; - "image\_id" (`int`): The image id.

&#x20; - "segments\_info" (`list\[Dict]`): List of segments for an image. Each segment should be a dictionary.

&#x20;   An image can have no segments, in which case the list should be empty.

&#x20; - "file\_name" (`str`): The file name of the image.

\- \*\*return\_segmentation\_masks\*\* (`bool`, \*optional\*, defaults to self.return\_segmentation\_masks) --

&#x20; Whether to return segmentation masks.

\- \*\*masks\_path\*\* (`str` or `pathlib.Path`, \*optional\*) --

&#x20; Path to the directory containing the segmentation masks.

\- \*\*do\_resize\*\* (`bool`, \*optional\*, defaults to self.do\_resize) --

&#x20; Whether to resize the image.

\- \*\*size\*\* (`dict\[str, int]`, \*optional\*, defaults to self.size) --

&#x20; Size of the image's `(height, width)` dimensions after resizing. Available options are:

&#x20; - `{"height": int, "width": int}`: The image will be resized to the exact size `(height, width)`.

&#x20;   Do NOT keep the aspect ratio.

&#x20; - `{"shortest\_edge": int, "longest\_edge": int}`: The image will be resized to a maximum size respecting

&#x20;   the aspect ratio and keeping the shortest edge less or equal to `shortest\_edge` and the longest edge

&#x20;   less or equal to `longest\_edge`.

&#x20; - `{"max\_height": int, "max\_width": int}`: The image will be resized to the maximum size respecting the

&#x20;   aspect ratio and keeping the height less or equal to `max\_height` and the width less or equal to

&#x20;   `max\_width`.

\- \*\*resample\*\* (`PILImageResampling`, \*optional\*, defaults to self.resample) --

&#x20; Resampling filter to use when resizing the image.

\- \*\*do\_rescale\*\* (`bool`, \*optional\*, defaults to self.do\_rescale) --

&#x20; Whether to rescale the image.

\- \*\*rescale\_factor\*\* (`float`, \*optional\*, defaults to self.rescale\_factor) --

&#x20; Rescale factor to use when rescaling the image.

\- \*\*do\_normalize\*\* (`bool`, \*optional\*, defaults to self.do\_normalize) --

&#x20; Whether to normalize the image.

\- \*\*do\_convert\_annotations\*\* (`bool`, \*optional\*, defaults to self.do\_convert\_annotations) --

&#x20; Whether to convert the annotations to the format expected by the model. Converts the bounding

&#x20; boxes from the format `(top\_left\_x, top\_left\_y, width, height)` to `(center\_x, center\_y, width, height)`

&#x20; and in relative coordinates.

\- \*\*image\_mean\*\* (`float` or `list\[float]`, \*optional\*, defaults to self.image\_mean) --

&#x20; Mean to use when normalizing the image.

\- \*\*image\_std\*\* (`float` or `list\[float]`, \*optional\*, defaults to self.image\_std) --

&#x20; Standard deviation to use when normalizing the image.

\- \*\*do\_pad\*\* (`bool`, \*optional\*, defaults to self.do\_pad) --

&#x20; Whether to pad the image. If `True`, padding will be applied to the bottom and right of

&#x20; the image with zeros. If `pad\_size` is provided, the image will be padded to the specified

&#x20; dimensions. Otherwise, the image will be padded to the maximum height and width of the batch.

\- \*\*format\*\* (`str` or `AnnotationFormat`, \*optional\*, defaults to self.format) --

&#x20; Format of the annotations.

\- \*\*return\_tensors\*\* (`str` or `TensorType`, \*optional\*, defaults to self.return\_tensors) --

&#x20; Type of tensors to return. If `None`, will return the list of images.

\- \*\*data\_format\*\* (`ChannelDimension` or `str`, \*optional\*, defaults to `ChannelDimension.FIRST`) --

&#x20; The channel dimension format for the output image. Can be one of:

&#x20; - `"channels\_first"` or `ChannelDimension.FIRST`: image in (num\_channels, height, width) format.

&#x20; - `"channels\_last"` or `ChannelDimension.LAST`: image in (height, width, num\_channels) format.

&#x20; - Unset: Use the channel dimension format of the input image.

\- \*\*input\_data\_format\*\* (`ChannelDimension` or `str`, \*optional\*) --

&#x20; The channel dimension format for the input image. If unset, the channel dimension format is inferred

&#x20; from the input image. Can be one of:

&#x20; - `"channels\_first"` or `ChannelDimension.FIRST`: image in (num\_channels, height, width) format.

&#x20; - `"channels\_last"` or `ChannelDimension.LAST`: image in (height, width, num\_channels) format.

&#x20; - `"none"` or `ChannelDimension.NONE`: image in (height, width) format.

\- \*\*pad\_size\*\* (`dict\[str, int]`, \*optional\*) --

&#x20; The size `{"height": int, "width" int}` to pad the images to. Must be larger than any image size

&#x20; provided for preprocessing. If `pad\_size` is not provided, images will be padded to the largest

&#x20; height and width in the batch.0



Preprocess an image or a batch of images so that it can be used by the model.



\*\*Parameters:\*\*



format (`str`, \*optional\*, defaults to `AnnotationFormat.COCO\_DETECTION`) : Data format of the annotations. One of "coco\_detection" or "coco\_panoptic".



do\_resize (`bool`, \*optional\*, defaults to `True`) : Controls whether to resize the image's (height, width) dimensions to the specified `size`. Can be overridden by the `do\_resize` parameter in the `preprocess` method.



size (`dict\[str, int]` \*optional\*, defaults to `{"shortest\_edge" : 800, "longest\_edge": 1333}`): Size of the image's `(height, width)` dimensions after resizing. Can be overridden by the `size` parameter in the `preprocess` method. Available options are: - `{"height": int, "width": int}`: The image will be resized to the exact size `(height, width)`. Do NOT keep the aspect ratio. - `{"shortest\_edge": int, "longest\_edge": int}`: The image will be resized to a maximum size respecting the aspect ratio and keeping the shortest edge less or equal to `shortest\_edge` and the longest edge less or equal to `longest\_edge`. - `{"max\_height": int, "max\_width": int}`: The image will be resized to the maximum size respecting the aspect ratio and keeping the height less or equal to `max\_height` and the width less or equal to `max\_width`.



resample (`PILImageResampling`, \*optional\*, defaults to `Resampling.BILINEAR`) : Resampling filter to use if resizing the image.



do\_rescale (`bool`, \*optional\*, defaults to `True`) : Controls whether to rescale the image by the specified scale `rescale\_factor`. Can be overridden by the `do\_rescale` parameter in the `preprocess` method.



rescale\_factor (`int` or `float`, \*optional\*, defaults to `1/255`) : Scale factor to use if rescaling the image. Can be overridden by the `rescale\_factor` parameter in the `preprocess` method. Controls whether to normalize the image. Can be overridden by the `do\_normalize` parameter in the `preprocess` method.



do\_normalize (`bool`, \*optional\*, defaults to `True`) : Whether to normalize the image. Can be overridden by the `do\_normalize` parameter in the `preprocess` method.



image\_mean (`float` or `list\[float]`, \*optional\*, defaults to `IMAGENET\_DEFAULT\_MEAN`) : Mean values to use when normalizing the image. Can be a single value or a list of values, one for each channel. Can be overridden by the `image\_mean` parameter in the `preprocess` method.



image\_std (`float` or `list\[float]`, \*optional\*, defaults to `IMAGENET\_DEFAULT\_STD`) : Standard deviation values to use when normalizing the image. Can be a single value or a list of values, one for each channel. Can be overridden by the `image\_std` parameter in the `preprocess` method.



do\_convert\_annotations (`bool`, \*optional\*, defaults to `True`) : Controls whether to convert the annotations to the format expected by the DETR model. Converts the bounding boxes to the format `(center\_x, center\_y, width, height)` and in the range `\[0, 1]`. Can be overridden by the `do\_convert\_annotations` parameter in the `preprocess` method.



do\_pad (`bool`, \*optional\*, defaults to `True`) : Controls whether to pad the image. Can be overridden by the `do\_pad` parameter in the `preprocess` method. If `True`, padding will be applied to the bottom and right of the image with zeros. If `pad\_size` is provided, the image will be padded to the specified dimensions. Otherwise, the image will be padded to the maximum height and width of the batch.



pad\_size (`dict\[str, int]`, \*optional\*) : The size `{"height": int, "width" int}` to pad the images to. Must be larger than any image size provided for preprocessing. If `pad\_size` is not provided, images will be padded to the largest height and width in the batch.



\## GroundingDinoImageProcessorFast\[\[transformers.GroundingDinoImageProcessorFast]]



\#### transformers.GroundingDinoImageProcessorFast\[\[transformers.GroundingDinoImageProcessorFast]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/image\_processing\_grounding\_dino\_fast.py#L291)



Constructs a GroundingDinoImageProcessorFast image processor.



preprocesstransformers.GroundingDinoImageProcessorFast.preprocesshttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/image\_processing\_utils\_fast.py#L838\[{"name": "images", "val": ": typing.Union\[ForwardRef('PIL.Image.Image'), numpy.ndarray, ForwardRef('torch.Tensor'), list\['PIL.Image.Image'], list\[numpy.ndarray], list\['torch.Tensor']]"}, {"name": "\*args", "val": ""}, {"name": "\*\*kwargs", "val": ": typing\_extensions.Unpack\[transformers.processing\_utils.ImagesKwargs]"}]- \*\*images\*\* (`Union\[PIL.Image.Image, numpy.ndarray, torch.Tensor, list\[PIL.Image.Image], list\[numpy.ndarray], list\[torch.Tensor]]`) --

&#x20; Image to preprocess. Expects a single or batch of images with pixel values ranging from 0 to 255. If

&#x20; passing in images with pixel values between 0 and 1, set `do\_rescale=False`.

\- \*\*return\_tensors\*\* (`str` or \[TensorType](/docs/transformers/v5.3.0/en/internal/file\_utils#transformers.TensorType), \*optional\*) --

&#x20; Returns stacked tensors if set to `'pt'`, otherwise returns a list of tensors.

\- \*\*\*\*kwargs\*\* (\[ImagesKwargs](/docs/transformers/v5.3.0/en/main\_classes/processors#transformers.ImagesKwargs), \*optional\*) --

&#x20; Additional image preprocessing options. Model-specific kwargs are listed above; see the TypedDict class

&#x20; for the complete list of supported arguments.0`\~image\_processing\_base.BatchFeature`- \*\*data\*\* (`dict`) -- Dictionary of lists/arrays/tensors returned by the \_\_call\_\_ method ('pixel\_values', etc.).

\- \*\*tensor\_type\*\* (`Union\[None, str, TensorType]`, \*optional\*) -- You can give a tensor\_type here to convert the lists of integers in PyTorch/Numpy Tensors at

&#x20; initialization.



\*\*Parameters:\*\*



format (`str`, \*kwargs\*, \*optional\*, defaults to `AnnotationFormat.COCO\_DETECTION`) : Data format of the annotations. One of "coco\_detection" or "coco\_panoptic".



do\_convert\_annotations (`bool`, \*kwargs\*, \*optional\*, defaults to `True`) : Controls whether to convert the annotations to the format expected by the GROUNDING\_DINO model. Converts the bounding boxes to the format `(center\_x, center\_y, width, height)` and in the range `\[0, 1]`. Can be overridden by the `do\_convert\_annotations` parameter in the `preprocess` method.



return\_segmentation\_masks (`bool`, \*kwargs\*, \*optional\*, defaults to `False`) : Whether to return segmentation masks.



annotations (`AnnotationType`, \*kwargs\* or `list\[AnnotationType]`, \*optional\*) : Annotations to transform according to the padding that is applied to the images.



masks\_path (`str`, \*kwargs\* or `pathlib.Path`, \*optional\*) : Path to the directory containing the segmentation masks.



\- \*\*\*\*kwargs\*\* (\[ImagesKwargs](/docs/transformers/v5.3.0/en/main\_classes/processors#transformers.ImagesKwargs), \*optional\*) : Additional image preprocessing options. Model-specific kwargs are listed above; see the TypedDict class for the complete list of supported arguments.



\*\*Returns:\*\*



``\~image\_processing\_base.BatchFeature``



\- \*\*data\*\* (`dict`) -- Dictionary of lists/arrays/tensors returned by the \_\_call\_\_ method ('pixel\_values', etc.).

\- \*\*tensor\_type\*\* (`Union\[None, str, TensorType]`, \*optional\*) -- You can give a tensor\_type here to convert the lists of integers in PyTorch/Numpy Tensors at

&#x20; initialization.

\#### post\_process\_object\_detection\[\[transformers.GroundingDinoImageProcessorFast.post\_process\_object\_detection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/image\_processing\_grounding\_dino\_fast.py#L656)



Converts the raw output of \[GroundingDinoForObjectDetection](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoForObjectDetection) into final bounding boxes in (top\_left\_x, top\_left\_y,

bottom\_right\_x, bottom\_right\_y) format.



\*\*Parameters:\*\*



outputs (`GroundingDinoObjectDetectionOutput`) : Raw outputs of the model.



threshold (`float`, \*optional\*, defaults to 0.1) : Score threshold to keep object detection predictions.



target\_sizes (`torch.Tensor` or `list\[tuple\[int, int]]`, \*optional\*) : Tensor of shape `(batch\_size, 2)` or list of tuples (`tuple\[int, int]`) containing the target size `(height, width)` of each image in the batch. If unset, predictions will not be resized.



\*\*Returns:\*\*



``list\[Dict]``



A list of dictionaries, each dictionary containing the following keys:

\- "scores": The confidence scores for each predicted box on the image.

\- "labels": Indexes of the classes predicted by the model on the image.

\- "boxes": Image bounding boxes in (top\_left\_x, top\_left\_y, bottom\_right\_x, bottom\_right\_y) format.



\## GroundingDinoProcessor\[\[transformers.GroundingDinoProcessor]]



\#### transformers.GroundingDinoProcessor\[\[transformers.GroundingDinoProcessor]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/processing\_grounding\_dino.py#L117)



Constructs a GroundingDinoProcessor which wraps a image processor and a tokenizer into a single processor.



\[GroundingDinoProcessor](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoProcessor) offers all the functionalities of \[GroundingDinoImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoImageProcessorFast) and \[BertTokenizer](/docs/transformers/v5.3.0/en/model\_doc/lxmert#transformers.BertTokenizer). See the

\[\~GroundingDinoImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoImageProcessorFast) and \[\~BertTokenizer](/docs/transformers/v5.3.0/en/model\_doc/lxmert#transformers.BertTokenizer) for more information.



\_\_call\_\_transformers.GroundingDinoProcessor.\_\_call\_\_https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/processing\_grounding\_dino.py#L123\[{"name": "images", "val": ": typing.Union\[ForwardRef('PIL.Image.Image'), numpy.ndarray, ForwardRef('torch.Tensor'), list\['PIL.Image.Image'], list\[numpy.ndarray], list\['torch.Tensor'], NoneType] = None"}, {"name": "text", "val": ": str | list\[str] | list\[list\[str]] = None"}, {"name": "\*\*kwargs", "val": ": typing\_extensions.Unpack\[transformers.models.grounding\_dino.processing\_grounding\_dino.GroundingDinoProcessorKwargs]"}]- \*\*images\*\* (`Union\[PIL.Image.Image, numpy.ndarray, torch.Tensor, list\[PIL.Image.Image], list\[numpy.ndarray], list\[torch.Tensor]]`, \*optional\*) --

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

&#x20; are listed above; see the TypedDict class for the complete list of supported arguments.0`\~tokenization\_utils\_base.BatchEncoding`- \*\*data\*\* (`dict`, \*optional\*) -- Dictionary of lists/arrays/tensors returned by the `\_\_call\_\_`/`encode\_plus`/`batch\_encode\_plus` methods

&#x20; ('input\_ids', 'attention\_mask', etc.).

\- \*\*encoding\*\* (`tokenizers.Encoding` or `Sequence\[tokenizers.Encoding]`, \*optional\*) -- If the tokenizer is a fast tokenizer which outputs additional information like mapping from word/character

&#x20; space to token space the `tokenizers.Encoding` instance or list of instance (for batches) hold this

&#x20; information.

\- \*\*tensor\_type\*\* (`Union\[None, str, TensorType]`, \*optional\*) -- You can give a tensor\_type here to convert the lists of integers in PyTorch/Numpy Tensors at

&#x20; initialization.

\- \*\*prepend\_batch\_axis\*\* (`bool`, \*optional\*, defaults to `False`) -- Whether or not to add a batch axis when converting to tensors (see `tensor\_type` above). Note that this

&#x20; parameter has an effect if the parameter `tensor\_type` is set, \*otherwise has no effect\*.

\- \*\*n\_sequences\*\* (`int`, \*optional\*) -- You can give a tensor\_type here to convert the lists of integers in PyTorch/Numpy Tensors at

&#x20; initialization.



\*\*Parameters:\*\*



image\_processor (`GroundingDinoImageProcessorFast`) : The image processor is a required input.



tokenizer (`BertTokenizer`) : The tokenizer is a required input.



\*\*Returns:\*\*



``\~tokenization\_utils\_base.BatchEncoding``



\- \*\*data\*\* (`dict`, \*optional\*) -- Dictionary of lists/arrays/tensors returned by the `\_\_call\_\_`/`encode\_plus`/`batch\_encode\_plus` methods

&#x20; ('input\_ids', 'attention\_mask', etc.).

\- \*\*encoding\*\* (`tokenizers.Encoding` or `Sequence\[tokenizers.Encoding]`, \*optional\*) -- If the tokenizer is a fast tokenizer which outputs additional information like mapping from word/character

&#x20; space to token space the `tokenizers.Encoding` instance or list of instance (for batches) hold this

&#x20; information.

\- \*\*tensor\_type\*\* (`Union\[None, str, TensorType]`, \*optional\*) -- You can give a tensor\_type here to convert the lists of integers in PyTorch/Numpy Tensors at

&#x20; initialization.

\- \*\*prepend\_batch\_axis\*\* (`bool`, \*optional\*, defaults to `False`) -- Whether or not to add a batch axis when converting to tensors (see `tensor\_type` above). Note that this

&#x20; parameter has an effect if the parameter `tensor\_type` is set, \*otherwise has no effect\*.

\- \*\*n\_sequences\*\* (`int`, \*optional\*) -- You can give a tensor\_type here to convert the lists of integers in PyTorch/Numpy Tensors at

&#x20; initialization.

\#### post\_process\_grounded\_object\_detection\[\[transformers.GroundingDinoProcessor.post\_process\_grounded\_object\_detection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/processing\_grounding\_dino.py#L151)



Converts the raw output of \[GroundingDinoForObjectDetection](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoForObjectDetection) into final bounding boxes in (top\_left\_x, top\_left\_y,

bottom\_right\_x, bottom\_right\_y) format and get the associated text label.



\*\*Parameters:\*\*



outputs (`GroundingDinoObjectDetectionOutput`) : Raw outputs of the model.



input\_ids (`torch.LongTensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) : The token ids of the input text. If not provided will be taken from the model output.



threshold (`float`, \*optional\*, defaults to 0.25) : Threshold to keep object detection predictions based on confidence score.



text\_threshold (`float`, \*optional\*, defaults to 0.25) : Score threshold to keep text detection predictions.



target\_sizes (`torch.Tensor` or `list\[tuple\[int, int]]`, \*optional\*) : Tensor of shape `(batch\_size, 2)` or list of tuples (`tuple\[int, int]`) containing the target size `(height, width)` of each image in the batch. If unset, predictions will not be resized.



text\_labels (`list\[list\[str]]`, \*optional\*) : List of candidate labels to be detected on each image. At the moment it's \*NOT used\*, but required to be in signature for the zero-shot object detection pipeline. Text labels are instead extracted from the `input\_ids` tensor provided in `outputs`.



\*\*Returns:\*\*



``list\[Dict]``



A list of dictionaries, each dictionary containing the

\- \*\*scores\*\*: tensor of confidence scores for detected objects

\- \*\*boxes\*\*: tensor of bounding boxes in \[x0, y0, x1, y1] format

\- \*\*labels\*\*: list of text labels for each detected object (will be replaced with integer ids in v4.51.0)

\- \*\*text\_labels\*\*: list of text labels for detected objects



\## GroundingDinoConfig\[\[transformers.GroundingDinoConfig]]



\#### transformers.GroundingDinoConfig\[\[transformers.GroundingDinoConfig]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/configuration\_grounding\_dino.py#L25)



This is the configuration class to store the configuration of a \[GroundingDinoModel](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoModel). It is used to instantiate a

Grounding DINO model according to the specified arguments, defining the model architecture. Instantiating a

configuration with the defaults will yield a similar configuration to that of the Grounding DINO

\[IDEA-Research/grounding-dino-tiny](https://huggingface.co/IDEA-Research/grounding-dino-tiny) architecture.



Configuration objects inherit from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the

documentation from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) for more information.



Examples:



```python

>>> from transformers import GroundingDinoConfig, GroundingDinoModel



>>> # Initializing a Grounding DINO IDEA-Research/grounding-dino-tiny style configuration

>>> configuration = GroundingDinoConfig()



>>> # Initializing a model (with random weights) from the IDEA-Research/grounding-dino-tiny style configuration

>>> model = GroundingDinoModel(configuration)



>>> # Accessing the model configuration

>>> configuration = model.config

```



\*\*Parameters:\*\*



backbone\_config (`Union\[dict, "PreTrainedConfig"]`, \*optional\*, defaults to `SwinConfig()`) : The configuration of the backbone model.



text\_config (`Union\[AutoConfig, dict]`, \*optional\*, defaults to `BertConfig`) : The config object or dictionary of the text backbone.



num\_queries (`int`, \*optional\*, defaults to 900) : Number of object queries, i.e. detection slots. This is the maximal number of objects \[GroundingDinoModel](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoModel) can detect in a single image.



encoder\_layers (`int`, \*optional\*, defaults to 6) : Number of encoder layers.



encoder\_ffn\_dim (`int`, \*optional\*, defaults to 2048) : Dimension of the "intermediate" (often named feed-forward) layer in decoder.



encoder\_attention\_heads (`int`, \*optional\*, defaults to 8) : Number of attention heads for each attention layer in the Transformer encoder.



decoder\_layers (`int`, \*optional\*, defaults to 6) : Number of decoder layers.



decoder\_ffn\_dim (`int`, \*optional\*, defaults to 2048) : Dimension of the "intermediate" (often named feed-forward) layer in decoder.



decoder\_attention\_heads (`int`, \*optional\*, defaults to 8) : Number of attention heads for each attention layer in the Transformer decoder.



is\_encoder\_decoder (`bool`, \*optional\*, defaults to `True`) : Whether the model is used as an encoder/decoder or not.



activation\_function (`str` or `function`, \*optional\*, defaults to `"relu"`) : The non-linear activation function (function or string) in the encoder and pooler. If string, `"gelu"`, `"relu"`, `"silu"` and `"gelu\_new"` are supported.



d\_model (`int`, \*optional\*, defaults to 256) : Dimension of the layers.



dropout (`float`, \*optional\*, defaults to 0.1) : The dropout probability for all fully connected layers in the embeddings, encoder, and pooler.



attention\_dropout (`float`, \*optional\*, defaults to 0.0) : The dropout ratio for the attention probabilities.



activation\_dropout (`float`, \*optional\*, defaults to 0.0) : The dropout ratio for activations inside the fully connected layer.



auxiliary\_loss (`bool`, \*optional\*, defaults to `False`) : Whether auxiliary decoding losses (loss at each decoder layer) are to be used.



position\_embedding\_type (`str`, \*optional\*, defaults to `"sine"`) : Type of position embeddings to be used on top of the image features. One of `"sine"` or `"learned"`.



num\_feature\_levels (`int`, \*optional\*, defaults to 4) : The number of input feature levels.



encoder\_n\_points (`int`, \*optional\*, defaults to 4) : The number of sampled keys in each feature level for each attention head in the encoder.



decoder\_n\_points (`int`, \*optional\*, defaults to 4) : The number of sampled keys in each feature level for each attention head in the decoder.



two\_stage (`bool`, \*optional\*, defaults to `True`) : Whether to apply a two-stage deformable DETR, where the region proposals are also generated by a variant of Grounding DINO, which are further fed into the decoder for iterative bounding box refinement.



class\_cost (`float`, \*optional\*, defaults to 1.0) : Relative weight of the classification error in the Hungarian matching cost.



bbox\_cost (`float`, \*optional\*, defaults to 5.0) : Relative weight of the L1 error of the bounding box coordinates in the Hungarian matching cost.



giou\_cost (`float`, \*optional\*, defaults to 2.0) : Relative weight of the generalized IoU loss of the bounding box in the Hungarian matching cost.



bbox\_loss\_coefficient (`float`, \*optional\*, defaults to 5.0) : Relative weight of the L1 bounding box loss in the object detection loss.



giou\_loss\_coefficient (`float`, \*optional\*, defaults to 2.0) : Relative weight of the generalized IoU loss in the object detection loss.



focal\_alpha (`float`, \*optional\*, defaults to 0.25) : Alpha parameter in the focal loss.



disable\_custom\_kernels (`bool`, \*optional\*, defaults to `False`) : Disable the use of custom CUDA and CPU kernels. This option is necessary for the ONNX export, as custom kernels are not supported by PyTorch ONNX export.



max\_text\_len (`int`, \*optional\*, defaults to 256) : The maximum length of the text input.



text\_enhancer\_dropout (`float`, \*optional\*, defaults to 0.0) : The dropout ratio for the text enhancer.



fusion\_droppath (`float`, \*optional\*, defaults to 0.1) : The droppath ratio for the fusion module.



fusion\_dropout (`float`, \*optional\*, defaults to 0.0) : The dropout ratio for the fusion module.



embedding\_init\_target (`bool`, \*optional\*, defaults to `True`) : Whether to initialize the target with Embedding weights.



query\_dim (`int`, \*optional\*, defaults to 4) : The dimension of the query vector.



decoder\_bbox\_embed\_share (`bool`, \*optional\*, defaults to `True`) : Whether to share the bbox regression head for all decoder layers.



two\_stage\_bbox\_embed\_share (`bool`, \*optional\*, defaults to `False`) : Whether to share the bbox embedding between the two-stage bbox generator and the region proposal generation.



positional\_embedding\_temperature (`float`, \*optional\*, defaults to 20) : The temperature for Sine Positional Embedding that is used together with vision backbone.



init\_std (`float`, \*optional\*, defaults to 0.02) : The standard deviation of the truncated\_normal\_initializer for initializing all weight matrices.



layer\_norm\_eps (`float`, \*optional\*, defaults to 1e-05) : The epsilon used by the layer normalization layers.



tie\_word\_embeddings (`bool`, \*optional\*, defaults to `True`) : Whether to tie weight embeddings



\## GroundingDinoModel\[\[transformers.GroundingDinoModel]]



\#### transformers.GroundingDinoModel\[\[transformers.GroundingDinoModel]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/modeling\_grounding\_dino.py#L1882)



The bare Grounding DINO Model (consisting of a backbone and encoder-decoder Transformer) outputting raw

hidden-states without any specific head on top.



This model inherits from \[PreTrainedModel](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the

library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads

etc.)



This model is also a PyTorch \[torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.

Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage

and behavior.



forwardtransformers.GroundingDinoModel.forwardhttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/modeling\_grounding\_dino.py#L2024\[{"name": "pixel\_values", "val": ": Tensor"}, {"name": "input\_ids", "val": ": Tensor"}, {"name": "token\_type\_ids", "val": ": torch.Tensor | None = None"}, {"name": "attention\_mask", "val": ": torch.Tensor | None = None"}, {"name": "pixel\_mask", "val": ": torch.Tensor | None = None"}, {"name": "encoder\_outputs", "val": " = None"}, {"name": "output\_attentions", "val": " = None"}, {"name": "output\_hidden\_states", "val": " = None"}, {"name": "return\_dict", "val": " = None"}, {"name": "\*\*kwargs", "val": ""}]- \*\*pixel\_values\*\* (`torch.Tensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`) --

&#x20; The tensors corresponding to the input images. Pixel values can be obtained using

&#x20; \[GroundingDinoImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoImageProcessorFast). See \[GroundingDinoImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[GroundingDinoProcessor](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoProcessor) uses

&#x20; \[GroundingDinoImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoImageProcessorFast) for processing images).

\- \*\*input\_ids\*\* (`torch.LongTensor` of shape `(batch\_size, text\_sequence\_length)`) --

&#x20; Indices of input sequence tokens in the vocabulary. Padding will be ignored by default should you provide

&#x20; it.



&#x20; Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[BertTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details.

\- \*\*token\_type\_ids\*\* (`torch.LongTensor` of shape `(batch\_size, text\_sequence\_length)`, \*optional\*) --

&#x20; Segment token indices to indicate first and second portions of the inputs. Indices are selected in `\[0,

&#x20; 1]`: 0 corresponds to a `sentence A` token, 1 corresponds to a `sentence B` token



&#x20; \[What are token type IDs?](../glossary#token-type-ids)

\- \*\*attention\_mask\*\* (`torch.Tensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:



&#x20; - 1 for tokens that are \*\*not masked\*\*,

&#x20; - 0 for tokens that are \*\*masked\*\*.



&#x20; \[What are attention masks?](../glossary#attention-mask)

\- \*\*pixel\_mask\*\* (`torch.Tensor` of shape `(batch\_size, height, width)`, \*optional\*) --

&#x20; Mask to avoid performing attention on padding pixel values. Mask values selected in `\[0, 1]`:



&#x20; - 1 for pixels that are real (i.e. \*\*not masked\*\*),

&#x20; - 0 for pixels that are padding (i.e. \*\*masked\*\*).



&#x20; \[What are attention masks?](../glossary#attention-mask)

\- \*\*encoder\_outputs\*\* (``) --

&#x20; Tuple consists of (`last\_hidden\_state`, \*optional\*: `hidden\_states`, \*optional\*: `attentions`)

&#x20; `last\_hidden\_state` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) is a sequence of

&#x20; hidden-states at the output of the last layer of the encoder. Used in the cross-attention of the decoder.

\- \*\*output\_attentions\*\* (``) --

&#x20; Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned

&#x20; tensors for more detail.

\- \*\*output\_hidden\_states\*\* (``) --

&#x20; Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for

&#x20; more detail.

\- \*\*return\_dict\*\* (``) --

&#x20; Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.0`GroundingDinoModelOutput` or `tuple(torch.FloatTensor)`A `GroundingDinoModelOutput` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[GroundingDinoConfig](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoConfig)) and inputs.

The \[GroundingDinoModel](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoModel) forward method, overrides the `\_\_call\_\_` special method.



Although the recipe for forward pass needs to be defined within this function, one should call the `Module`

instance afterwards instead of this since the former takes care of running the pre and post processing steps while

the latter silently ignores them.



\- \*\*last\_hidden\_state\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_queries, hidden\_size)`) -- Sequence of hidden-states at the output of the last layer of the decoder of the model.

\- \*\*init\_reference\_points\*\* (`torch.FloatTensor` of shape  `(batch\_size, num\_queries, 4)`) -- Initial reference points sent through the Transformer decoder.

\- \*\*intermediate\_hidden\_states\*\* (`torch.FloatTensor` of shape `(batch\_size, config.decoder\_layers, num\_queries, hidden\_size)`) -- Stacked intermediate hidden states (output of each layer of the decoder).

\- \*\*intermediate\_reference\_points\*\* (`torch.FloatTensor` of shape `(batch\_size, config.decoder\_layers, num\_queries, 4)`) -- Stacked intermediate reference points (reference points of each layer of the decoder).

\- \*\*decoder\_hidden\_states\*\* (`tuple\[torch.FloatTensor]`, \*optional\*, returned when `output\_hidden\_states=True` is passed or when `config.output\_hidden\_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the embeddings, if the model has an embedding layer, +

&#x20; one for the output of each layer) of shape `(batch\_size, sequence\_length, hidden\_size)`.



&#x20; Hidden-states of the decoder at the output of each layer plus the initial embedding outputs.

\- \*\*decoder\_attentions\*\* (`tuple\[tuple\[torch.FloatTensor]]`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of `torch.FloatTensor` (one for each layer) of shape `(batch\_size, num\_heads, sequence\_length,

&#x20; sequence\_length)`.



&#x20; Attentions weights of the decoder, after the attention softmax, used to compute the weighted average in the

&#x20; self-attention heads.

\- \*\*encoder\_last\_hidden\_state\_vision\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) -- Sequence of hidden-states at the output of the last layer of the encoder of the model.

\- \*\*encoder\_last\_hidden\_state\_text\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) -- Sequence of hidden-states at the output of the last layer of the encoder of the model.

\- \*\*encoder\_vision\_hidden\_states\*\* (`tuple(torch.FloatTensor)`, \*optional\*, returned when `output\_hidden\_states=True` is passed or when `config.output\_hidden\_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the vision embeddings + one for the output of each

&#x20; layer) of shape `(batch\_size, sequence\_length, hidden\_size)`. Hidden-states of the vision encoder at the

&#x20; output of each layer plus the initial embedding outputs.

\- \*\*encoder\_text\_hidden\_states\*\* (`tuple(torch.FloatTensor)`, \*optional\*, returned when `output\_hidden\_states=True` is passed or when `config.output\_hidden\_states=True`) -- Tuple of `torch.FloatTensor` (one for the output of the text embeddings + one for the output of each layer)

&#x20; of shape `(batch\_size, sequence\_length, hidden\_size)`. Hidden-states of the text encoder at the output of

&#x20; each layer plus the initial embedding outputs.

\- \*\*encoder\_attentions\*\* (`tuple(tuple(torch.FloatTensor))`, \*optional\*, returned when `output\_attentions=True` is passed or when `config.output\_attentions=True`) -- Tuple of tuples of `torch.FloatTensor` (one for attention for each layer) of shape `(batch\_size, num\_heads,

&#x20; sequence\_length, sequence\_length)`. Attentions weights after the attention softmax, used to compute the

&#x20; weighted average in the text-vision attention, vision-text attention, text-enhancer (self-attention) and

&#x20; multi-scale deformable attention heads. attention softmax, used to compute the weighted average in the

&#x20; bi-attention heads.

\- \*\*enc\_outputs\_class\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, config.num\_labels)`, \*optional\*, returned when `config.two\_stage=True`) -- Predicted bounding boxes scores where the top `config.num\_queries` scoring bounding boxes are picked as

&#x20; region proposals in the first stage. Output of bounding box binary classification (i.e. foreground and

&#x20; background).

\- \*\*enc\_outputs\_coord\_logits\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, 4)`, \*optional\*, returned when `config.two\_stage=True`) -- Logits of predicted bounding boxes coordinates in the first stage.

\- \*\*encoder\_logits\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, config.num\_labels)`, \*optional\*, returned when `config.two\_stage=True`) -- Logits of top `config.num\_queries` scoring bounding boxes in the first stage.

\- \*\*encoder\_pred\_boxes\*\* (`torch.FloatTensor` of shape `(batch\_size, sequence\_length, 4)`, \*optional\*, returned when `config.two\_stage=True`) -- Coordinates of top `config.num\_queries` scoring bounding boxes in the first stage.



Examples:



```python

>>> from transformers import AutoProcessor, AutoModel

>>> from PIL import Image

>>> import httpx

>>> from io import BytesIO



>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> with httpx.stream("GET", url) as response:

...     image = Image.open(BytesIO(response.read()))

>>> text = "a cat."



>>> processor = AutoProcessor.from\_pretrained("IDEA-Research/grounding-dino-tiny")

>>> model = AutoModel.from\_pretrained("IDEA-Research/grounding-dino-tiny")



>>> inputs = processor(images=image, text=text, return\_tensors="pt")

>>> outputs = model(\*\*inputs)



>>> last\_hidden\_states = outputs.last\_hidden\_state

>>> list(last\_hidden\_states.shape)

\[1, 900, 256]

```



\*\*Parameters:\*\*



config (\[GroundingDinoConfig](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoConfig)) : Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the \[from\_pretrained()](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel.from\_pretrained) method to load the model weights.



\*\*Returns:\*\*



``GroundingDinoModelOutput` or `tuple(torch.FloatTensor)``



A `GroundingDinoModelOutput` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[GroundingDinoConfig](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoConfig)) and inputs.



\## GroundingDinoForObjectDetection\[\[transformers.GroundingDinoForObjectDetection]]



\#### transformers.GroundingDinoForObjectDetection\[\[transformers.GroundingDinoForObjectDetection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/modeling\_grounding\_dino.py#L2393)



Grounding DINO Model (consisting of a backbone and encoder-decoder Transformer) with object detection heads on top,

for tasks such as COCO detection.



This model inherits from \[PreTrainedModel](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the

library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads

etc.)



This model is also a PyTorch \[torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.

Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage

and behavior.



forwardtransformers.GroundingDinoForObjectDetection.forwardhttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/grounding\_dino/modeling\_grounding\_dino.py#L2430\[{"name": "pixel\_values", "val": ": FloatTensor"}, {"name": "input\_ids", "val": ": LongTensor"}, {"name": "token\_type\_ids", "val": ": torch.LongTensor | None = None"}, {"name": "attention\_mask", "val": ": torch.LongTensor | None = None"}, {"name": "pixel\_mask", "val": ": torch.BoolTensor | None = None"}, {"name": "encoder\_outputs", "val": ": transformers.models.grounding\_dino.modeling\_grounding\_dino.GroundingDinoEncoderOutput | tuple | None = None"}, {"name": "output\_attentions", "val": ": bool | None = None"}, {"name": "output\_hidden\_states", "val": ": bool | None = None"}, {"name": "return\_dict", "val": ": bool | None = None"}, {"name": "labels", "val": ": list\[dict\[str, torch.LongTensor | torch.FloatTensor]] | None = None"}, {"name": "\*\*kwargs", "val": ""}]- \*\*pixel\_values\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`) --

&#x20; The tensors corresponding to the input images. Pixel values can be obtained using

&#x20; \[GroundingDinoImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoImageProcessorFast). See \[GroundingDinoImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[GroundingDinoProcessor](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoProcessor) uses

&#x20; \[GroundingDinoImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoImageProcessorFast) for processing images).

\- \*\*input\_ids\*\* (`torch.LongTensor` of shape `(batch\_size, text\_sequence\_length)`) --

&#x20; Indices of input sequence tokens in the vocabulary. Padding will be ignored by default should you provide

&#x20; it.



&#x20; Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[BertTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details.

\- \*\*token\_type\_ids\*\* (`torch.LongTensor` of shape `(batch\_size, text\_sequence\_length)`, \*optional\*) --

&#x20; Segment token indices to indicate first and second portions of the inputs. Indices are selected in `\[0,

&#x20; 1]`: 0 corresponds to a `sentence A` token, 1 corresponds to a `sentence B` token



&#x20; \[What are token type IDs?](../glossary#token-type-ids)

\- \*\*attention\_mask\*\* (`torch.LongTensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:



&#x20; - 1 for tokens that are \*\*not masked\*\*,

&#x20; - 0 for tokens that are \*\*masked\*\*.



&#x20; \[What are attention masks?](../glossary#attention-mask)

\- \*\*pixel\_mask\*\* (`torch.BoolTensor` of shape `(batch\_size, height, width)`, \*optional\*) --

&#x20; Mask to avoid performing attention on padding pixel values. Mask values selected in `\[0, 1]`:



&#x20; - 1 for pixels that are real (i.e. \*\*not masked\*\*),

&#x20; - 0 for pixels that are padding (i.e. \*\*masked\*\*).



&#x20; \[What are attention masks?](../glossary#attention-mask)

\- \*\*encoder\_outputs\*\* (`Union\[\~models.grounding\_dino.modeling\_grounding\_dino.GroundingDinoEncoderOutput, tuple]`, \*optional\*) --

&#x20; Tuple consists of (`last\_hidden\_state`, \*optional\*: `hidden\_states`, \*optional\*: `attentions`)

&#x20; `last\_hidden\_state` of shape `(batch\_size, sequence\_length, hidden\_size)`, \*optional\*) is a sequence of

&#x20; hidden-states at the output of the last layer of the encoder. Used in the cross-attention of the decoder.

\- \*\*output\_attentions\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned

&#x20; tensors for more detail.

\- \*\*output\_hidden\_states\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for

&#x20; more detail.

\- \*\*return\_dict\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.

\- \*\*labels\*\* (`list\[Dict]` of len `(batch\_size,)`, \*optional\*) --

&#x20; Labels for computing the bipartite matching loss. List of dicts, each dictionary containing at least the

&#x20; following 2 keys: 'class\_labels' and 'boxes' (the class labels and bounding boxes of an image in the batch

&#x20; respectively). The class labels themselves should be a `torch.LongTensor` of len `(number of bounding boxes

&#x20; in the image,)` and the boxes a `torch.FloatTensor` of shape `(number of bounding boxes in the image, 4)`.0

The \[GroundingDinoForObjectDetection](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoForObjectDetection) forward method, overrides the `\_\_call\_\_` special method.



Although the recipe for forward pass needs to be defined within this function, one should call the `Module`

instance afterwards instead of this since the former takes care of running the pre and post processing steps while

the latter silently ignores them.



Examples:



```python

>>> import httpx

>>> from io import BytesIO



>>> import torch

>>> from PIL import Image

>>> from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection



>>> model\_id = "IDEA-Research/grounding-dino-tiny"

>>> device = "cuda"



>>> processor = AutoProcessor.from\_pretrained(model\_id)

>>> model = AutoModelForZeroShotObjectDetection.from\_pretrained(model\_id).to(device)



>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> with httpx.stream("GET", url) as response:

...     image = Image.open(BytesIO(response.read()))

>>> # Check for cats and remote controls

>>> text\_labels = \[\["a cat", "a remote control"]]



>>> inputs = processor(images=image, text=text\_labels, return\_tensors="pt").to(device)

>>> with torch.no\_grad():

...     outputs = model(\*\*inputs)



>>> results = processor.post\_process\_grounded\_object\_detection(

...     outputs,

...     threshold=0.4,

...     text\_threshold=0.3,

...     target\_sizes=\[(image.height, image.width)]

... )

>>> # Retrieve the first image result

>>> result = results\[0]

>>> for box, score, text\_label in zip(result\["boxes"], result\["scores"], result\["text\_labels"]):

...     box = \[round(x, 2) for x in box.tolist()]

...     print(f"Detected {text\_label} with confidence {round(score.item(), 3)} at location {box}")

Detected a cat with confidence 0.479 at location \[344.7, 23.11, 637.18, 374.28]

Detected a cat with confidence 0.438 at location \[12.27, 51.91, 316.86, 472.44]

Detected a remote control with confidence 0.478 at location \[38.57, 70.0, 176.78, 118.18]

```



\*\*Parameters:\*\*



config (\[GroundingDinoConfig](/docs/transformers/v5.3.0/en/model\_doc/grounding-dino#transformers.GroundingDinoConfig)) : Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the \[from\_pretrained()](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel.from\_pretrained) method to load the model weights.





