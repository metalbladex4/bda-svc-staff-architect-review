\# OWLv2



\## Overview



OWLv2 was proposed in \[Scaling Open-Vocabulary Object Detection](https://huggingface.co/papers/2306.09683) by Matthias Minderer, Alexey Gritsenko, Neil Houlsby. OWLv2 scales up \[OWL-ViT](owlvit) using self-training, which uses an existing detector to generate pseudo-box annotations on image-text pairs. This results in large gains over the previous state-of-the-art for zero-shot object detection.



The abstract from the paper is the following:



\*Open-vocabulary object detection has benefited greatly from pretrained vision-language models, but is still limited by the amount of available detection training data. While detection training data can be expanded by using Web image-text pairs as weak supervision, this has not been done at scales comparable to image-level pretraining. Here, we scale up detection data with self-training, which uses an existing detector to generate pseudo-box annotations on image-text pairs. Major challenges in scaling self-training are the choice of label space, pseudo-annotation filtering, and training efficiency. We present the OWLv2 model and OWL-ST self-training recipe, which address these challenges. OWLv2 surpasses the performance of previous state-of-the-art open-vocabulary detectors already at comparable training scales (\~10M examples). However, with OWL-ST, we can scale to over 1B examples, yielding further large improvement: With an L/14 architecture, OWL-ST improves AP on LVIS rare classes, for which the model has seen no human box annotations, from 31.2% to 44.6% (43% relative improvement). OWL-ST unlocks Web-scale training for open-world localization, similar to what has been seen for image classification and language modelling.\*



&#x20;OWLv2 high-level overview. Taken from the original paper. 



This model was contributed by \[nielsr](https://huggingface.co/nielsr).

The original code can be found \[here](https://github.com/google-research/scenic/tree/main/scenic/projects/owl\_vit).



\## Usage example



OWLv2 is, just like its predecessor \[OWL-ViT](owlvit), a zero-shot text-conditioned object detection model. OWL-ViT uses \[CLIP](clip) as its multi-modal backbone, with a ViT-like Transformer to get visual features and a causal language model to get the text features. To use CLIP for detection, OWL-ViT removes the final token pooling layer of the vision model and attaches a lightweight classification and box head to each transformer output token. Open-vocabulary classification is enabled by replacing the fixed classification layer weights with the class-name embeddings obtained from the text model. The authors first train CLIP from scratch and fine-tune it end-to-end with the classification and box heads on standard detection datasets using a bipartite matching loss. One or multiple text queries per image can be used to perform zero-shot text-conditioned object detection.



\[Owlv2ImageProcessor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessor) can be used to resize (or rescale) and normalize images for the model and \[CLIPTokenizer](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPTokenizer) is used to encode the text. \[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) wraps \[Owlv2ImageProcessor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessor) and \[CLIPTokenizer](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPTokenizer) into a single instance to both encode the text and prepare the images. The following example shows how to perform object detection using \[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) and \[Owlv2ForObjectDetection](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ForObjectDetection).



```python

>>> import requests

>>> from PIL import Image

>>> import torch



>>> from transformers import Owlv2Processor, Owlv2ForObjectDetection



>>> processor = Owlv2Processor.from\_pretrained("google/owlv2-base-patch16-ensemble")

>>> model = Owlv2ForObjectDetection.from\_pretrained("google/owlv2-base-patch16-ensemble")



>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> image = Image.open(requests.get(url, stream=True).raw)

>>> text\_labels = \[\["a photo of a cat", "a photo of a dog"]]

>>> inputs = processor(text=text\_labels, images=image, return\_tensors="pt")

>>> outputs = model(\*\*inputs)



>>> # Target image sizes (height, width) to rescale box predictions \[batch\_size, 2]

>>> target\_sizes = torch.tensor(\[(image.height, image.width)])

>>> # Convert outputs (bounding boxes and class logits) to Pascal VOC format (xmin, ymin, xmax, ymax)

>>> results = processor.post\_process\_grounded\_object\_detection(

...     outputs=outputs, target\_sizes=target\_sizes, threshold=0.1, text\_labels=text\_labels

... )

>>> # Retrieve predictions for the first image for the corresponding text queries

>>> result = results\[0]

>>> boxes, scores, text\_labels = result\["boxes"], result\["scores"], result\["text\_labels"]

>>> for box, score, text\_label in zip(boxes, scores, text\_labels):

...     box = \[round(i, 2) for i in box.tolist()]

...     print(f"Detected {text\_label} with confidence {round(score.item(), 3)} at location {box}")

Detected a photo of a cat with confidence 0.614 at location \[341.67, 23.39, 642.32, 371.35]

Detected a photo of a cat with confidence 0.665 at location \[6.75, 51.96, 326.62, 473.13]

```



\## Resources



\- A demo notebook on using OWLv2 for zero- and one-shot (image-guided) object detection can be found \[here](https://github.com/NielsRogge/Transformers-Tutorials/tree/master/OWLv2).

\- \[Zero-shot object detection task guide](../tasks/zero\_shot\_object\_detection)



The architecture of OWLv2 is identical to \[OWL-ViT](owlvit), however the object detection head now also includes an objectness classifier, which predicts the (query-agnostic) likelihood that a predicted box contains an object (as opposed to background). The objectness score can be used to rank or filter predictions independently of text queries.

Usage of OWLv2 is identical to \[OWL-ViT](owlvit) with a new, updated image processor (\[Owlv2ImageProcessor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessor)).



\## Owlv2Config\[\[transformers.Owlv2Config]]



\#### transformers.Owlv2Config\[\[transformers.Owlv2Config]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/configuration\_owlv2.py#L213)



\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config) is the configuration class to store the configuration of an \[Owlv2Model](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Model). It is used to

instantiate an OWLv2 model according to the specified arguments, defining the text model and vision model

configs. Instantiating a configuration with the defaults will yield a similar configuration to that of the OWLv2

\[google/owlv2-base-patch16](https://huggingface.co/google/owlv2-base-patch16) architecture.



Configuration objects inherit from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the

documentation from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) for more information.



\*\*Parameters:\*\*



text\_config (`dict`, \*optional\*) : Dictionary of configuration options used to initialize \[Owlv2TextConfig](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2TextConfig).



vision\_config (`dict`, \*optional\*) : Dictionary of configuration options used to initialize \[Owlv2VisionConfig](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionConfig).



projection\_dim (`int`, \*optional\*, defaults to 512) : Dimensionality of text and vision projection layers.



logit\_scale\_init\_value (`float`, \*optional\*, defaults to 2.6592) : The initial value of the \*logit\_scale\* parameter. Default is used as per the original OWLv2 implementation.



return\_dict (`bool`, \*optional\*, defaults to `True`) : Whether or not the model should return a dictionary. If `False`, returns a tuple.



kwargs (\*optional\*) : Dictionary of keyword arguments.



\## Owlv2TextConfig\[\[transformers.Owlv2TextConfig]]



\#### transformers.Owlv2TextConfig\[\[transformers.Owlv2TextConfig]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/configuration\_owlv2.py#L24)



This is the configuration class to store the configuration of an \[Owlv2TextModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2TextModel). It is used to instantiate an

Owlv2 text encoder according to the specified arguments, defining the model architecture. Instantiating a

configuration with the defaults will yield a similar configuration to that of the Owlv2

\[google/owlv2-base-patch16](https://huggingface.co/google/owlv2-base-patch16) architecture.



Configuration objects inherit from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the

documentation from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) for more information.



Example:



```python

>>> from transformers import Owlv2TextConfig, Owlv2TextModel



>>> # Initializing a Owlv2TextModel with google/owlv2-base-patch16 style configuration

>>> configuration = Owlv2TextConfig()



>>> # Initializing a Owlv2TextConfig from the google/owlv2-base-patch16 style configuration

>>> model = Owlv2TextModel(configuration)



>>> # Accessing the model configuration

>>> configuration = model.config

```



\*\*Parameters:\*\*



vocab\_size (`int`, \*optional\*, defaults to 49408) : Vocabulary size of the OWLv2 text model. Defines the number of different tokens that can be represented by the `inputs\_ids` passed when calling \[Owlv2TextModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2TextModel).



hidden\_size (`int`, \*optional\*, defaults to 512) : Dimensionality of the encoder layers and the pooler layer.



intermediate\_size (`int`, \*optional\*, defaults to 2048) : Dimensionality of the "intermediate" (i.e., feed-forward) layer in the Transformer encoder.



num\_hidden\_layers (`int`, \*optional\*, defaults to 12) : Number of hidden layers in the Transformer encoder.



num\_attention\_heads (`int`, \*optional\*, defaults to 8) : Number of attention heads for each attention layer in the Transformer encoder.



max\_position\_embeddings (`int`, \*optional\*, defaults to 16) : The maximum sequence length that this model might ever be used with. Typically set this to something large just in case (e.g., 512 or 1024 or 2048).



hidden\_act (`str` or `function`, \*optional\*, defaults to `"quick\_gelu"`) : The non-linear activation function (function or string) in the encoder and pooler. If string, `"gelu"`, `"relu"`, `"selu"` and `"gelu\_new"` `"quick\_gelu"` are supported.



layer\_norm\_eps (`float`, \*optional\*, defaults to 1e-05) : The epsilon used by the layer normalization layers.



attention\_dropout (`float`, \*optional\*, defaults to 0.0) : The dropout ratio for the attention probabilities.



initializer\_range (`float`, \*optional\*, defaults to 0.02) : The standard deviation of the truncated\_normal\_initializer for initializing all weight matrices.



initializer\_factor (`float`, \*optional\*, defaults to 1.0) : A factor for initializing all weight matrices (should be kept to 1, used internally for initialization testing).



pad\_token\_id (`int`, \*optional\*, defaults to 0) : The id of the padding token in the input sequences.



bos\_token\_id (`int`, \*optional\*, defaults to 49406) : The id of the beginning-of-sequence token in the input sequences.



eos\_token\_id (`int`, \*optional\*, defaults to 49407) : The id of the end-of-sequence token in the input sequences.



\## Owlv2VisionConfig\[\[transformers.Owlv2VisionConfig]]



\#### transformers.Owlv2VisionConfig\[\[transformers.Owlv2VisionConfig]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/configuration\_owlv2.py#L124)



This is the configuration class to store the configuration of an \[Owlv2VisionModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionModel). It is used to instantiate

an OWLv2 image encoder according to the specified arguments, defining the model architecture. Instantiating a

configuration with the defaults will yield a similar configuration to that of the OWLv2

\[google/owlv2-base-patch16](https://huggingface.co/google/owlv2-base-patch16) architecture.



Configuration objects inherit from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) and can be used to control the model outputs. Read the

documentation from \[PreTrainedConfig](/docs/transformers/v5.3.0/en/main\_classes/configuration#transformers.PreTrainedConfig) for more information.



Example:



```python

>>> from transformers import Owlv2VisionConfig, Owlv2VisionModel



>>> # Initializing a Owlv2VisionModel with google/owlv2-base-patch16 style configuration

>>> configuration = Owlv2VisionConfig()



>>> # Initializing a Owlv2VisionModel model from the google/owlv2-base-patch16 style configuration

>>> model = Owlv2VisionModel(configuration)



>>> # Accessing the model configuration

>>> configuration = model.config

```



\*\*Parameters:\*\*



hidden\_size (`int`, \*optional\*, defaults to 768) : Dimensionality of the encoder layers and the pooler layer.



intermediate\_size (`int`, \*optional\*, defaults to 3072) : Dimensionality of the "intermediate" (i.e., feed-forward) layer in the Transformer encoder.



num\_hidden\_layers (`int`, \*optional\*, defaults to 12) : Number of hidden layers in the Transformer encoder.



num\_attention\_heads (`int`, \*optional\*, defaults to 12) : Number of attention heads for each attention layer in the Transformer encoder.



num\_channels (`int`, \*optional\*, defaults to 3) : Number of channels in the input images.



image\_size (`int`, \*optional\*, defaults to 768) : The size (resolution) of each image.



patch\_size (`int`, \*optional\*, defaults to 16) : The size (resolution) of each patch.



hidden\_act (`str` or `function`, \*optional\*, defaults to `"quick\_gelu"`) : The non-linear activation function (function or string) in the encoder and pooler. If string, `"gelu"`, `"relu"`, `"selu"` and `"gelu\_new"` `"quick\_gelu"` are supported.



layer\_norm\_eps (`float`, \*optional\*, defaults to 1e-05) : The epsilon used by the layer normalization layers.



attention\_dropout (`float`, \*optional\*, defaults to 0.0) : The dropout ratio for the attention probabilities.



initializer\_range (`float`, \*optional\*, defaults to 0.02) : The standard deviation of the truncated\_normal\_initializer for initializing all weight matrices.



initializer\_factor (`float`, \*optional\*, defaults to 1.0) : A factor for initializing all weight matrices (should be kept to 1, used internally for initialization testing).



\## Owlv2ImageProcessor\[\[transformers.Owlv2ImageProcessor]]



\#### transformers.Owlv2ImageProcessor\[\[transformers.Owlv2ImageProcessor]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/image\_processing\_owlv2.py#L210)



Constructs an OWLv2 image processor.



preprocesstransformers.Owlv2ImageProcessor.preprocesshttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/image\_processing\_owlv2.py#L367\[{"name": "images", "val": ": typing.Union\[ForwardRef('PIL.Image.Image'), numpy.ndarray, ForwardRef('torch.Tensor'), list\['PIL.Image.Image'], list\[numpy.ndarray], list\['torch.Tensor']]"}, {"name": "do\_pad", "val": ": bool | None = None"}, {"name": "do\_resize", "val": ": bool | None = None"}, {"name": "size", "val": ": dict\[str, int] | None = None"}, {"name": "do\_rescale", "val": ": bool | None = None"}, {"name": "rescale\_factor", "val": ": float | None = None"}, {"name": "do\_normalize", "val": ": bool | None = None"}, {"name": "image\_mean", "val": ": float | list\[float] | None = None"}, {"name": "image\_std", "val": ": float | list\[float] | None = None"}, {"name": "return\_tensors", "val": ": str | transformers.utils.generic.TensorType | None = None"}, {"name": "data\_format", "val": ": ChannelDimension = "}, {"name": "input\_data\_format", "val": ": str | transformers.image\_utils.ChannelDimension | None = None"}]- \*\*images\*\* (`ImageInput`) --

&#x20; Image to preprocess. Expects a single or batch of images with pixel values ranging from 0 to 255. If

&#x20; passing in images with pixel values between 0 and 1, set `do\_rescale=False`.

\- \*\*do\_pad\*\* (`bool`, \*optional\*, defaults to `self.do\_pad`) --

&#x20; Whether to pad the image to a square with gray pixels on the bottom and the right.

\- \*\*do\_resize\*\* (`bool`, \*optional\*, defaults to `self.do\_resize`) --

&#x20; Whether to resize the image.

\- \*\*size\*\* (`dict\[str, int]`, \*optional\*, defaults to `self.size`) --

&#x20; Size to resize the image to.

\- \*\*do\_rescale\*\* (`bool`, \*optional\*, defaults to `self.do\_rescale`) --

&#x20; Whether to rescale the image values between \[0 - 1].

\- \*\*rescale\_factor\*\* (`float`, \*optional\*, defaults to `self.rescale\_factor`) --

&#x20; Rescale factor to rescale the image by if `do\_rescale` is set to `True`.

\- \*\*do\_normalize\*\* (`bool`, \*optional\*, defaults to `self.do\_normalize`) --

&#x20; Whether to normalize the image.

\- \*\*image\_mean\*\* (`float` or `list\[float]`, \*optional\*, defaults to `self.image\_mean`) --

&#x20; Image mean.

\- \*\*image\_std\*\* (`float` or `list\[float]`, \*optional\*, defaults to `self.image\_std`) --

&#x20; Image standard deviation.

\- \*\*return\_tensors\*\* (`str` or `TensorType`, \*optional\*) --

&#x20; The type of tensors to return. Can be one of:

&#x20; - Unset: Return a list of `np.ndarray`.

&#x20; - `TensorType.PYTORCH` or `'pt'`: Return a batch of type `torch.Tensor`.

&#x20; - `TensorType.NUMPY` or `'np'`: Return a batch of type `np.ndarray`.

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

&#x20; - `"none"` or `ChannelDimension.NONE`: image in (height, width) format.0



Preprocess an image or batch of images.



\*\*Parameters:\*\*



do\_rescale (`bool`, \*optional\*, defaults to `True`) : Whether to rescale the image by the specified scale `rescale\_factor`. Can be overridden by `do\_rescale` in the `preprocess` method.



rescale\_factor (`int` or `float`, \*optional\*, defaults to `1/255`) : Scale factor to use if rescaling the image. Can be overridden by `rescale\_factor` in the `preprocess` method.



do\_pad (`bool`, \*optional\*, defaults to `True`) : Whether to pad the image to a square with gray pixels on the bottom and the right. Can be overridden by `do\_pad` in the `preprocess` method.



do\_resize (`bool`, \*optional\*, defaults to `True`) : Controls whether to resize the image's (height, width) dimensions to the specified `size`. Can be overridden by `do\_resize` in the `preprocess` method.



size (`dict\[str, int]` \*optional\*, defaults to `{"height" : 960, "width": 960}`): Size to resize the image to. Can be overridden by `size` in the `preprocess` method.



resample (`PILImageResampling`, \*optional\*, defaults to `Resampling.BILINEAR`) : Resampling method to use if resizing the image. Can be overridden by `resample` in the `preprocess` method.



do\_normalize (`bool`, \*optional\*, defaults to `True`) : Whether to normalize the image. Can be overridden by the `do\_normalize` parameter in the `preprocess` method.



image\_mean (`float` or `list\[float]`, \*optional\*, defaults to `OPENAI\_CLIP\_MEAN`) : Mean to use if normalizing the image. This is a float or list of floats the length of the number of channels in the image. Can be overridden by the `image\_mean` parameter in the `preprocess` method.



image\_std (`float` or `list\[float]`, \*optional\*, defaults to `OPENAI\_CLIP\_STD`) : Standard deviation to use if normalizing the image. This is a float or list of floats the length of the number of channels in the image. Can be overridden by the `image\_std` parameter in the `preprocess` method.

\#### post\_process\_object\_detection\[\[transformers.Owlv2ImageProcessor.post\_process\_object\_detection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/image\_processing\_owlv2.py#L497)



Converts the raw output of \[Owlv2ForObjectDetection](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ForObjectDetection) into final bounding boxes in (top\_left\_x, top\_left\_y,

bottom\_right\_x, bottom\_right\_y) format.



\*\*Parameters:\*\*



outputs (`Owlv2ObjectDetectionOutput`) : Raw outputs of the model.



threshold (`float`, \*optional\*, defaults to 0.1) : Score threshold to keep object detection predictions.



target\_sizes (`torch.Tensor` or `list\[tuple\[int, int]]`, \*optional\*) : Tensor of shape `(batch\_size, 2)` or list of tuples (`tuple\[int, int]`) containing the target size `(height, width)` of each image in the batch. If unset, predictions will not be resized.



\*\*Returns:\*\*



``list\[Dict]``



A list of dictionaries, each dictionary containing the following keys:

\- "scores": The confidence scores for each predicted box on the image.

\- "labels": Indexes of the classes predicted by the model on the image.

\- "boxes": Image bounding boxes in (top\_left\_x, top\_left\_y, bottom\_right\_x, bottom\_right\_y) format.

\#### post\_process\_image\_guided\_detection\[\[transformers.Owlv2ImageProcessor.post\_process\_image\_guided\_detection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/image\_processing\_owlv2.py#L551)



Converts the output of \[OwlViTForObjectDetection.image\_guided\_detection()](/docs/transformers/v5.3.0/en/model\_doc/owlvit#transformers.OwlViTForObjectDetection.image\_guided\_detection) into the format expected by the COCO

api.



\*\*Parameters:\*\*



outputs (`OwlViTImageGuidedObjectDetectionOutput`) : Raw outputs of the model.



threshold (`float`, \*optional\*, defaults to 0.0) : Minimum confidence threshold to use to filter out predicted boxes.



nms\_threshold (`float`, \*optional\*, defaults to 0.3) : IoU threshold for non-maximum suppression of overlapping boxes.



target\_sizes (`torch.Tensor`, \*optional\*) : Tensor of shape (batch\_size, 2) where each entry is the (height, width) of the corresponding image in the batch. If set, predicted normalized bounding boxes are rescaled to the target sizes. If left to None, predictions will not be unnormalized.



\*\*Returns:\*\*



``list\[Dict]``



A list of dictionaries, each dictionary containing the scores, labels and boxes for an image

in the batch as predicted by the model. All labels are set to None as

`OwlViTForObjectDetection.image\_guided\_detection` perform one-shot object detection.



\## Owlv2ImageProcessorFast\[\[transformers.Owlv2ImageProcessorFast]]



\#### transformers.Owlv2ImageProcessorFast\[\[transformers.Owlv2ImageProcessorFast]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/image\_processing\_owlv2\_fast.py#L39)



Constructs a Owlv2ImageProcessorFast image processor.



preprocesstransformers.Owlv2ImageProcessorFast.preprocesshttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/image\_processing\_utils\_fast.py#L838\[{"name": "images", "val": ": typing.Union\[ForwardRef('PIL.Image.Image'), numpy.ndarray, ForwardRef('torch.Tensor'), list\['PIL.Image.Image'], list\[numpy.ndarray], list\['torch.Tensor']]"}, {"name": "\*args", "val": ""}, {"name": "\*\*kwargs", "val": ": typing\_extensions.Unpack\[transformers.processing\_utils.ImagesKwargs]"}]- \*\*images\*\* (`Union\[PIL.Image.Image, numpy.ndarray, torch.Tensor, list\[PIL.Image.Image], list\[numpy.ndarray], list\[torch.Tensor]]`) --

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



\- \*\*\*\*kwargs\*\* (\[ImagesKwargs](/docs/transformers/v5.3.0/en/main\_classes/processors#transformers.ImagesKwargs), \*optional\*) : Additional image preprocessing options. Model-specific kwargs are listed above; see the TypedDict class for the complete list of supported arguments.



\*\*Returns:\*\*



``\~image\_processing\_base.BatchFeature``



\- \*\*data\*\* (`dict`) -- Dictionary of lists/arrays/tensors returned by the \_\_call\_\_ method ('pixel\_values', etc.).

\- \*\*tensor\_type\*\* (`Union\[None, str, TensorType]`, \*optional\*) -- You can give a tensor\_type here to convert the lists of integers in PyTorch/Numpy Tensors at

&#x20; initialization.

\#### post\_process\_object\_detection\[\[transformers.Owlv2ImageProcessorFast.post\_process\_object\_detection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/image\_processing\_owlv2\_fast.py#L55)



Converts the raw output of \[Owlv2ForObjectDetection](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ForObjectDetection) into final bounding boxes in (top\_left\_x, top\_left\_y,

bottom\_right\_x, bottom\_right\_y) format.



\*\*Parameters:\*\*



outputs (`Owlv2ObjectDetectionOutput`) : Raw outputs of the model.



threshold (`float`, \*optional\*, defaults to 0.1) : Score threshold to keep object detection predictions.



target\_sizes (`torch.Tensor` or `list\[tuple\[int, int]]`, \*optional\*) : Tensor of shape `(batch\_size, 2)` or list of tuples (`tuple\[int, int]`) containing the target size `(height, width)` of each image in the batch. If unset, predictions will not be resized.



\*\*Returns:\*\*



``list\[Dict]``



A list of dictionaries, each dictionary containing the following keys:

\- "scores": The confidence scores for each predicted box on the image.

\- "labels": Indexes of the classes predicted by the model on the image.

\- "boxes": Image bounding boxes in (top\_left\_x, top\_left\_y, bottom\_right\_x, bottom\_right\_y) format.

\#### post\_process\_image\_guided\_detection\[\[transformers.Owlv2ImageProcessorFast.post\_process\_image\_guided\_detection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/image\_processing\_owlv2\_fast.py#L108)



Converts the output of \[Owlv2ForObjectDetection.image\_guided\_detection()](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ForObjectDetection.image\_guided\_detection) into the format expected by the COCO

api.



\*\*Parameters:\*\*



outputs (`Owlv2ImageGuidedObjectDetectionOutput`) : Raw outputs of the model.



threshold (`float`, \*optional\*, defaults to 0.0) : Minimum confidence threshold to use to filter out predicted boxes.



nms\_threshold (`float`, \*optional\*, defaults to 0.3) : IoU threshold for non-maximum suppression of overlapping boxes.



target\_sizes (`torch.Tensor`, \*optional\*) : Tensor of shape (batch\_size, 2) where each entry is the (height, width) of the corresponding image in the batch. If set, predicted normalized bounding boxes are rescaled to the target sizes. If left to None, predictions will not be unnormalized.



\*\*Returns:\*\*



``list\[Dict]``



A list of dictionaries, each dictionary containing the scores, labels and boxes for an image

in the batch as predicted by the model. All labels are set to None as

`Owlv2ForObjectDetection.image\_guided\_detection` perform one-shot object detection.



\## Owlv2Processor\[\[transformers.Owlv2Processor]]



\#### transformers.Owlv2Processor\[\[transformers.Owlv2Processor]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/processing\_owlv2.py#L62)



Constructs a Owlv2Processor which wraps a image processor and a tokenizer into a single processor.



\[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) offers all the functionalities of \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast) and \[CLIPTokenizer](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPTokenizer). See the

\[\~Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast) and \[\~CLIPTokenizer](/docs/transformers/v5.3.0/en/model\_doc/clip#transformers.CLIPTokenizer) for more information.



\_\_call\_\_transformers.Owlv2Processor.\_\_call\_\_https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/processing\_owlv2.py#L66\[{"name": "images", "val": ": typing.Union\[ForwardRef('PIL.Image.Image'), numpy.ndarray, ForwardRef('torch.Tensor'), list\['PIL.Image.Image'], list\[numpy.ndarray], list\['torch.Tensor'], NoneType] = None"}, {"name": "text", "val": ": str | list\[str] | list\[list\[str]] = None"}, {"name": "\*\*kwargs", "val": ": typing\_extensions.Unpack\[transformers.models.owlv2.processing\_owlv2.Owlv2ProcessorKwargs]"}]- \*\*images\*\* (`Union\[PIL.Image.Image, numpy.ndarray, torch.Tensor, list\[PIL.Image.Image], list\[numpy.ndarray], list\[torch.Tensor]]`, \*optional\*) --

&#x20; Image to preprocess. Expects a single or batch of images with pixel values ranging from 0 to 255. If

&#x20; passing in images with pixel values between 0 and 1, set `do\_rescale=False`.

\- \*\*text\*\* (`Union\[str, list\[str], list\[list\[str]]]`, \*optional\*) --

&#x20; The sequence or batch of sequences to be encoded. Each sequence can be a string or a list of strings

&#x20; (pretokenized string). If you pass a pretokenized input, set `is\_split\_into\_words=True` to avoid ambiguity with batched inputs.

\- \*\*query\_images\*\* (`ImageInput`, \*kwargs\*, \*optional\*) --

&#x20; Query images to use for image-guided object detection. When provided, these images serve as visual queries

&#x20; to find similar objects in the main `images`. The query images override any text prompts, and the model

&#x20; performs image-to-image matching instead of text-to-image matching.

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

\- \*\*query\_pixel\_values\*\* -- Pixel values of the query images to be fed to a model. Returned when `query\_images` is not `None`.



\*\*Parameters:\*\*



image\_processor (`Owlv2ImageProcessorFast`) : The image processor is a required input.



tokenizer (`CLIPTokenizer`) : The tokenizer is a required input.



\*\*Returns:\*\*



`\[BatchFeature](/docs/transformers/v5.3.0/en/main\_classes/feature\_extractor#transformers.BatchFeature)`



A \[BatchFeature](/docs/transformers/v5.3.0/en/main\_classes/feature\_extractor#transformers.BatchFeature) with the following fields:

\- \*\*input\_ids\*\* -- List of token ids to be fed to a model. Returned when `text` is not `None`.

\- \*\*attention\_mask\*\* -- List of indices specifying which tokens should be attended to by the model (when

&#x20; `return\_attention\_mask=True` or if \*"attention\_mask"\* is in `self.model\_input\_names` and if `text` is not

&#x20; `None`).

\- \*\*pixel\_values\*\* -- Pixel values to be fed to a model. Returned when `images` is not `None`.

\- \*\*query\_pixel\_values\*\* -- Pixel values of the query images to be fed to a model. Returned when `query\_images` is not `None`.

\#### post\_process\_grounded\_object\_detection\[\[transformers.Owlv2Processor.post\_process\_grounded\_object\_detection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/processing\_owlv2.py#L144)



Converts the raw output of \[Owlv2ForObjectDetection](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ForObjectDetection) into final bounding boxes in (top\_left\_x, top\_left\_y,

bottom\_right\_x, bottom\_right\_y) format.



\*\*Parameters:\*\*



outputs (`Owlv2ObjectDetectionOutput`) : Raw outputs of the model.



threshold (`float`, \*optional\*, defaults to 0.1) : Score threshold to keep object detection predictions.



target\_sizes (`torch.Tensor` or `list\[tuple\[int, int]]`, \*optional\*) : Tensor of shape `(batch\_size, 2)` or list of tuples (`tuple\[int, int]`) containing the target size `(height, width)` of each image in the batch. If unset, predictions will not be resized.



text\_labels (`list\[list\[str]]`, \*optional\*) : List of lists of text labels for each image in the batch. If unset, "text\_labels" in output will be set to `None`.



\*\*Returns:\*\*



``list\[Dict]``



A list of dictionaries, each dictionary containing the following keys:

\- "scores": The confidence scores for each predicted box on the image.

\- "labels": Indexes of the classes predicted by the model on the image.

\- "boxes": Image bounding boxes in (top\_left\_x, top\_left\_y, bottom\_right\_x, bottom\_right\_y) format.

\- "text\_labels": The text labels for each predicted bounding box on the image.

\#### post\_process\_image\_guided\_detection\[\[transformers.Owlv2Processor.post\_process\_image\_guided\_detection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/processing\_owlv2.py#L193)



Converts the output of \[Owlv2ForObjectDetection.image\_guided\_detection()](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ForObjectDetection.image\_guided\_detection) into the format expected by the COCO

api.



\*\*Parameters:\*\*



outputs (`Owlv2ImageGuidedObjectDetectionOutput`) : Raw outputs of the model.



threshold (`float`, \*optional\*, defaults to 0.0) : Minimum confidence threshold to use to filter out predicted boxes.



nms\_threshold (`float`, \*optional\*, defaults to 0.3) : IoU threshold for non-maximum suppression of overlapping boxes.



target\_sizes (`torch.Tensor`, \*optional\*) : Tensor of shape (batch\_size, 2) where each entry is the (height, width) of the corresponding image in the batch. If set, predicted normalized bounding boxes are rescaled to the target sizes. If left to None, predictions will not be unnormalized.



\*\*Returns:\*\*



``list\[Dict]``



A list of dictionaries, each dictionary containing the following keys:

\- "scores": The confidence scores for each predicted box on the image.

\- "boxes": Image bounding boxes in (top\_left\_x, top\_left\_y, bottom\_right\_x, bottom\_right\_y) format.

\- "labels": Set to `None`.



\## Owlv2Model\[\[transformers.Owlv2Model]]



\#### transformers.Owlv2Model\[\[transformers.Owlv2Model]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L936)



The bare Owlv2 Model outputting raw hidden-states without any specific head on top.



This model inherits from \[PreTrainedModel](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel). Check the superclass documentation for the generic methods the

library implements for all its model (such as downloading or saving, resizing the input embeddings, pruning heads

etc.)



This model is also a PyTorch \[torch.nn.Module](https://pytorch.org/docs/stable/nn.html#torch.nn.Module) subclass.

Use it as a regular PyTorch Module and refer to the PyTorch documentation for all matter related to general usage

and behavior.



forwardtransformers.Owlv2Model.forwardhttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L1045\[{"name": "input\_ids", "val": ": torch.LongTensor | None = None"}, {"name": "pixel\_values", "val": ": torch.FloatTensor | None = None"}, {"name": "attention\_mask", "val": ": torch.Tensor | None = None"}, {"name": "return\_loss", "val": ": bool | None = None"}, {"name": "output\_attentions", "val": ": bool | None = None"}, {"name": "output\_hidden\_states", "val": ": bool | None = None"}, {"name": "interpolate\_pos\_encoding", "val": ": bool = False"}, {"name": "return\_base\_image\_embeds", "val": ": bool | None = None"}, {"name": "return\_dict", "val": ": bool | None = None"}, {"name": "\*\*kwargs", "val": ""}]- \*\*input\_ids\*\* (`torch.LongTensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Indices of input sequence tokens in the vocabulary. Padding will be ignored by default.



&#x20; Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and

&#x20; \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details.



&#x20; \[What are input IDs?](../glossary#input-ids)

\- \*\*pixel\_values\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`, \*optional\*) --

&#x20; The tensors corresponding to the input images. Pixel values can be obtained using

&#x20; \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast). See \[Owlv2ImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) uses

&#x20; \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast) for processing images).

\- \*\*attention\_mask\*\* (`torch.Tensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:



&#x20; - 1 for tokens that are \*\*not masked\*\*,

&#x20; - 0 for tokens that are \*\*masked\*\*.



&#x20; \[What are attention masks?](../glossary#attention-mask)

\- \*\*return\_loss\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the contrastive loss.

\- \*\*output\_attentions\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned

&#x20; tensors for more detail.

\- \*\*output\_hidden\_states\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for

&#x20; more detail.

\- \*\*interpolate\_pos\_encoding\*\* (`bool`, \*optional\*, defaults to `False`) --

&#x20; Whether to interpolate the pre-trained position encodings.

\- \*\*return\_base\_image\_embeds\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the base image embeddings.

\- \*\*return\_dict\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.0`Owlv2Output` or `tuple(torch.FloatTensor)`A `Owlv2Output` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.

The \[Owlv2Model](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Model) forward method, overrides the `\_\_call\_\_` special method.



Although the recipe for forward pass needs to be defined within this function, one should call the `Module`

instance afterwards instead of this since the former takes care of running the pre and post processing steps while

the latter silently ignores them.



\- \*\*loss\*\* (`torch.FloatTensor` of shape `(1,)`, \*optional\*, returned when `return\_loss` is `True`) -- Contrastive loss for image-text similarity.

\- \*\*logits\_per\_image\*\* (`torch.FloatTensor` of shape `(image\_batch\_size, text\_batch\_size)`) -- The scaled dot product scores between `image\_embeds` and `text\_embeds`. This represents the image-text

&#x20; similarity scores.

\- \*\*logits\_per\_text\*\* (`torch.FloatTensor` of shape `(text\_batch\_size, image\_batch\_size)`) -- The scaled dot product scores between `text\_embeds` and `image\_embeds`. This represents the text-image

&#x20; similarity scores.

\- \*\*text\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size \* num\_max\_text\_queries, output\_dim`) -- The text embeddings obtained by applying the projection layer to the pooled output of \[Owlv2TextModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2TextModel).

\- \*\*image\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, output\_dim`) -- The image embeddings obtained by applying the projection layer to the pooled output of

&#x20; \[Owlv2VisionModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionModel).

\- \*\*text\_model\_output\*\* (`\~modeling\_outputs.BaseModelOutputWithPooling`, defaults to `None`) -- The output of the \[Owlv2TextModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2TextModel).

\- \*\*vision\_model\_output\*\* (`\~modeling\_outputs.BaseModelOutputWithPooling`, defaults to `None`) -- The output of the \[Owlv2VisionModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionModel).



Examples:

```python

>>> from PIL import Image

>>> import httpx

>>> from io import BytesIO

>>> from transformers import AutoProcessor, Owlv2Model



>>> model = Owlv2Model.from\_pretrained("google/owlv2-base-patch16-ensemble")

>>> processor = AutoProcessor.from\_pretrained("google/owlv2-base-patch16-ensemble")

>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> with httpx.stream("GET", url) as response:

...     image = Image.open(BytesIO(response.read()))

>>> inputs = processor(text=\[\["a photo of a cat", "a photo of a dog"]], images=image, return\_tensors="pt")

>>> outputs = model(\*\*inputs)

>>> logits\_per\_image = outputs.logits\_per\_image  # this is the image-text similarity score

>>> probs = logits\_per\_image.softmax(dim=1)  # we can take the softmax to get the label probabilities

```



\*\*Parameters:\*\*



config (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) : Model configuration class with all the parameters of the model. Initializing with a config file does not load the weights associated with the model, only the configuration. Check out the \[from\_pretrained()](/docs/transformers/v5.3.0/en/main\_classes/model#transformers.PreTrainedModel.from\_pretrained) method to load the model weights.



\*\*Returns:\*\*



``Owlv2Output` or `tuple(torch.FloatTensor)``



A `Owlv2Output` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.

\#### get\_text\_features\[\[transformers.Owlv2Model.get\_text\_features]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L971)



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



Examples:

```python

>>> import torch

>>> from transformers import AutoProcessor, Owlv2Model



>>> model = Owlv2Model.from\_pretrained("google/owlv2-base-patch16-ensemble")

>>> processor = AutoProcessor.from\_pretrained("google/owlv2-base-patch16-ensemble")

>>> inputs = processor(

...     text=\[\["a photo of a cat", "a photo of a dog"], \["photo of a astranaut"]], return\_tensors="pt"

... )

>>> with torch.inference\_mode():

...     text\_features = model.get\_text\_features(\*\*inputs)

```



\*\*Parameters:\*\*



input\_ids (`torch.LongTensor` of shape `(batch\_size \* num\_max\_text\_queries, sequence\_length)`) : Indices of input sequence tokens in the vocabulary. Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details. \[What are input IDs?](../glossary#input-ids)



attention\_mask (`torch.Tensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) : Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:  - 1 for tokens that are \*\*not masked\*\*, - 0 for tokens that are \*\*masked\*\*.  \[What are attention masks?](../glossary#attention-mask)



\*\*Returns:\*\*



`\[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)``



A \[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.

\#### get\_image\_features\[\[transformers.Owlv2Model.get\_image\_features]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L1010)



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



Examples:

```python

>>> import torch

>>> from transformers.image\_utils import load\_image

>>> from transformers import AutoProcessor, Owlv2Model



>>> model = Owlv2Model.from\_pretrained("google/owlv2-base-patch16-ensemble")

>>> processor = AutoProcessor.from\_pretrained("google/owlv2-base-patch16-ensemble")



>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> image = load\_image(url)



>>> inputs = processor(images=image, return\_tensors="pt")

>>> with torch.inference\_mode():

...     image\_features = model.get\_image\_features(\*\*inputs)

```



\*\*Parameters:\*\*



pixel\_values (`torch.Tensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`) : The tensors corresponding to the input images. Pixel values can be obtained using \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast). See \[Owlv2ImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) uses \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast) for processing images).



interpolate\_pos\_encoding (`bool`, \*optional\*, defaults to `False`) : Whether to interpolate the pre-trained position encodings.



\*\*Returns:\*\*



`\[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)``



A \[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.



\## Owlv2TextModel\[\[transformers.Owlv2TextModel]]



\#### transformers.Owlv2TextModel\[\[transformers.Owlv2TextModel]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L764)



forwardtransformers.Owlv2TextModel.forwardhttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L780\[{"name": "input\_ids", "val": ": Tensor"}, {"name": "attention\_mask", "val": ": torch.Tensor | None = None"}, {"name": "output\_attentions", "val": ": bool | None = None"}, {"name": "output\_hidden\_states", "val": ": bool | None = None"}, {"name": "return\_dict", "val": ": bool | None = None"}, {"name": "\*\*kwargs", "val": ""}]- \*\*input\_ids\*\* (`torch.LongTensor` of shape `(batch\_size \* num\_max\_text\_queries, sequence\_length)`) --

&#x20; Indices of input sequence tokens in the vocabulary. Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See

&#x20; \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details. \[What are input

&#x20; IDs?](../glossary#input-ids)

\- \*\*attention\_mask\*\* (`torch.Tensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:



&#x20; - 1 for tokens that are \*\*not masked\*\*,

&#x20; - 0 for tokens that are \*\*masked\*\*.



&#x20; \[What are attention masks?](../glossary#attention-mask)

\- \*\*output\_attentions\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned

&#x20; tensors for more detail.

\- \*\*output\_hidden\_states\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for

&#x20; more detail.

\- \*\*return\_dict\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.0\[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)`A \[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.

The \[Owlv2TextModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2TextModel) forward method, overrides the `\_\_call\_\_` special method.



Although the recipe for forward pass needs to be defined within this function, one should call the `Module`

instance afterwards instead of this since the former takes care of running the pre and post processing steps while

the latter silently ignores them.



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



Examples:

```python

>>> from transformers import AutoProcessor, Owlv2TextModel



>>> model = Owlv2TextModel.from\_pretrained("google/owlv2-base-patch16")

>>> processor = AutoProcessor.from\_pretrained("google/owlv2-base-patch16")

>>> inputs = processor(

...     text=\[\["a photo of a cat", "a photo of a dog"], \["photo of a astranaut"]], return\_tensors="pt"

... )

>>> outputs = model(\*\*inputs)

>>> last\_hidden\_state = outputs.last\_hidden\_state

>>> pooled\_output = outputs.pooler\_output  # pooled (EOS token) states

```



\*\*Parameters:\*\*



input\_ids (`torch.LongTensor` of shape `(batch\_size \* num\_max\_text\_queries, sequence\_length)`) : Indices of input sequence tokens in the vocabulary. Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details. \[What are input IDs?](../glossary#input-ids)



attention\_mask (`torch.Tensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) : Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:  - 1 for tokens that are \*\*not masked\*\*, - 0 for tokens that are \*\*masked\*\*.  \[What are attention masks?](../glossary#attention-mask)



output\_attentions (`bool`, \*optional\*) : Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned tensors for more detail.



output\_hidden\_states (`bool`, \*optional\*) : Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for more detail.



return\_dict (`bool`, \*optional\*) : Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.



\*\*Returns:\*\*



`\[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)``



A \[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.



\## Owlv2VisionModel\[\[transformers.Owlv2VisionModel]]



\#### transformers.Owlv2VisionModel\[\[transformers.Owlv2VisionModel]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L881)



forwardtransformers.Owlv2VisionModel.forwardhttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L895\[{"name": "pixel\_values", "val": ": torch.FloatTensor | None = None"}, {"name": "output\_attentions", "val": ": bool | None = None"}, {"name": "output\_hidden\_states", "val": ": bool | None = None"}, {"name": "interpolate\_pos\_encoding", "val": ": bool = False"}, {"name": "return\_dict", "val": ": bool | None = None"}, {"name": "\*\*kwargs", "val": ""}]- \*\*pixel\_values\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`, \*optional\*) --

&#x20; The tensors corresponding to the input images. Pixel values can be obtained using

&#x20; \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast). See \[Owlv2ImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) uses

&#x20; \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast) for processing images).

\- \*\*output\_attentions\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned

&#x20; tensors for more detail.

\- \*\*output\_hidden\_states\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for

&#x20; more detail.

\- \*\*interpolate\_pos\_encoding\*\* (`bool`, \*optional\*, defaults to `False`) --

&#x20; Whether to interpolate the pre-trained position encodings.

\- \*\*return\_dict\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.0\[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)`A \[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.

The \[Owlv2VisionModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionModel) forward method, overrides the `\_\_call\_\_` special method.



Although the recipe for forward pass needs to be defined within this function, one should call the `Module`

instance afterwards instead of this since the former takes care of running the pre and post processing steps while

the latter silently ignores them.



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



Examples:

```python

>>> from PIL import Image

>>> import httpx

>>> from io import BytesIO

>>> from transformers import AutoProcessor, Owlv2VisionModel



>>> model = Owlv2VisionModel.from\_pretrained("google/owlv2-base-patch16")

>>> processor = AutoProcessor.from\_pretrained("google/owlv2-base-patch16")

>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> with httpx.stream("GET", url) as response:

...     image = Image.open(BytesIO(response.read()))



>>> inputs = processor(images=image, return\_tensors="pt")



>>> outputs = model(\*\*inputs)

>>> last\_hidden\_state = outputs.last\_hidden\_state

>>> pooled\_output = outputs.pooler\_output  # pooled CLS states

```



\*\*Parameters:\*\*



pixel\_values (`torch.FloatTensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`, \*optional\*) : The tensors corresponding to the input images. Pixel values can be obtained using \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast). See \[Owlv2ImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) uses \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast) for processing images).



output\_attentions (`bool`, \*optional\*) : Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned tensors for more detail.



output\_hidden\_states (`bool`, \*optional\*) : Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for more detail.



interpolate\_pos\_encoding (`bool`, \*optional\*, defaults to `False`) : Whether to interpolate the pre-trained position encodings.



return\_dict (`bool`, \*optional\*) : Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.



\*\*Returns:\*\*



`\[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or `tuple(torch.FloatTensor)``



A \[BaseModelOutputWithPooling](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.modeling\_outputs.BaseModelOutputWithPooling) or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.



\## Owlv2ForObjectDetection\[\[transformers.Owlv2ForObjectDetection]]



\#### transformers.Owlv2ForObjectDetection\[\[transformers.Owlv2ForObjectDetection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L1211)



forwardtransformers.Owlv2ForObjectDetection.forwardhttps://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L1600\[{"name": "input\_ids", "val": ": Tensor"}, {"name": "pixel\_values", "val": ": FloatTensor"}, {"name": "attention\_mask", "val": ": torch.Tensor | None = None"}, {"name": "output\_attentions", "val": ": bool | None = None"}, {"name": "output\_hidden\_states", "val": ": bool | None = None"}, {"name": "interpolate\_pos\_encoding", "val": ": bool = False"}, {"name": "return\_dict", "val": ": bool | None = None"}, {"name": "\*\*kwargs", "val": ""}]- \*\*input\_ids\*\* (`torch.LongTensor` of shape `(batch\_size \* num\_max\_text\_queries, sequence\_length)`, \*optional\*) --

&#x20; Indices of input sequence tokens in the vocabulary. Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See

&#x20; \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details. \[What are input

&#x20; IDs?](../glossary#input-ids).

\- \*\*pixel\_values\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`) --

&#x20; The tensors corresponding to the input images. Pixel values can be obtained using

&#x20; \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast). See \[Owlv2ImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) uses

&#x20; \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast) for processing images).

\- \*\*attention\_mask\*\* (`torch.Tensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) --

&#x20; Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:



&#x20; - 1 for tokens that are \*\*not masked\*\*,

&#x20; - 0 for tokens that are \*\*masked\*\*.



&#x20; \[What are attention masks?](../glossary#attention-mask)

\- \*\*output\_attentions\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned

&#x20; tensors for more detail.

\- \*\*output\_hidden\_states\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return the last hidden state. See `text\_model\_last\_hidden\_state` and

&#x20; `vision\_model\_last\_hidden\_state` under returned tensors for more detail.

\- \*\*interpolate\_pos\_encoding\*\* (`bool`, \*optional\*, defaults to `False`) --

&#x20; Whether to interpolate the pre-trained position encodings.

\- \*\*return\_dict\*\* (`bool`, \*optional\*) --

&#x20; Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.0`Owlv2ObjectDetectionOutput` or `tuple(torch.FloatTensor)`A `Owlv2ObjectDetectionOutput` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.

The \[Owlv2ForObjectDetection](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ForObjectDetection) forward method, overrides the `\_\_call\_\_` special method.



Although the recipe for forward pass needs to be defined within this function, one should call the `Module`

instance afterwards instead of this since the former takes care of running the pre and post processing steps while

the latter silently ignores them.



\- \*\*loss\*\* (`torch.FloatTensor` of shape `(1,)`, \*optional\*, returned when `labels` are provided)) -- Total loss as a linear combination of a negative log-likehood (cross-entropy) for class prediction and a

&#x20; bounding box loss. The latter is defined as a linear combination of the L1 loss and the generalized

&#x20; scale-invariant IoU loss.

\- \*\*loss\_dict\*\* (`Dict`, \*optional\*) -- A dictionary containing the individual losses. Useful for logging.

\- \*\*logits\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_patches, num\_queries)`) -- Classification logits (including no-object) for all queries.

\- \*\*objectness\_logits\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_patches, 1)`) -- The objectness logits of all image patches. OWL-ViT represents images as a set of image patches where the

&#x20; total number of patches is (image\_size / patch\_size)\*\*2.

\- \*\*pred\_boxes\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_patches, 4)`) -- Normalized boxes coordinates for all queries, represented as (center\_x, center\_y, width, height). These

&#x20; values are normalized in \[0, 1], relative to the size of each individual image in the batch (disregarding

&#x20; possible padding). You can use \[post\_process\_object\_detection()](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessor.post\_process\_object\_detection) to retrieve the

&#x20; unnormalized bounding boxes.

\- \*\*text\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_max\_text\_queries, output\_dim`) -- The text embeddings obtained by applying the projection layer to the pooled output of \[Owlv2TextModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2TextModel).

\- \*\*image\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, patch\_size, patch\_size, output\_dim`) -- Pooled output of \[Owlv2VisionModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionModel). OWLv2 represents images as a set of image patches and computes image

&#x20; embeddings for each patch.

\- \*\*class\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_patches, hidden\_size)`) -- Class embeddings of all image patches. OWLv2 represents images as a set of image patches where the total

&#x20; number of patches is (image\_size / patch\_size)\*\*2.

\- \*\*text\_model\_output\*\* (`\~modeling\_outputs.BaseModelOutputWithPooling`, defaults to `None`) -- The output of the \[Owlv2TextModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2TextModel).

\- \*\*vision\_model\_output\*\* (`\~modeling\_outputs.BaseModelOutputWithPooling`, defaults to `None`) -- The output of the \[Owlv2VisionModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionModel).



Examples:

```python

>>> import httpx

>>> from io import BytesIO

>>> from PIL import Image

>>> import torch



>>> from transformers import Owlv2Processor, Owlv2ForObjectDetection



>>> processor = Owlv2Processor.from\_pretrained("google/owlv2-base-patch16-ensemble")

>>> model = Owlv2ForObjectDetection.from\_pretrained("google/owlv2-base-patch16-ensemble")



>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> with httpx.stream("GET", url) as response:

...     image = Image.open(BytesIO(response.read()))

>>> text\_labels = \[\["a photo of a cat", "a photo of a dog"]]

>>> inputs = processor(text=text\_labels, images=image, return\_tensors="pt")

>>> outputs = model(\*\*inputs)



>>> # Target image sizes (height, width) to rescale box predictions \[batch\_size, 2]

>>> target\_sizes = torch.tensor(\[(image.height, image.width)])

>>> # Convert outputs (bounding boxes and class logits) to Pascal VOC format (xmin, ymin, xmax, ymax)

>>> results = processor.post\_process\_grounded\_object\_detection(

...     outputs=outputs, target\_sizes=target\_sizes, threshold=0.1, text\_labels=text\_labels

... )

>>> # Retrieve predictions for the first image for the corresponding text queries

>>> result = results\[0]

>>> boxes, scores, text\_labels = result\["boxes"], result\["scores"], result\["text\_labels"]

>>> for box, score, text\_label in zip(boxes, scores, text\_labels):

...     box = \[round(i, 2) for i in box.tolist()]

...     print(f"Detected {text\_label} with confidence {round(score.item(), 3)} at location {box}")

Detected a photo of a cat with confidence 0.614 at location \[341.67, 23.39, 642.32, 371.35]

Detected a photo of a cat with confidence 0.665 at location \[6.75, 51.96, 326.62, 473.13]

```



\*\*Parameters:\*\*



input\_ids (`torch.LongTensor` of shape `(batch\_size \* num\_max\_text\_queries, sequence\_length)`, \*optional\*) : Indices of input sequence tokens in the vocabulary. Indices can be obtained using \[AutoTokenizer](/docs/transformers/v5.3.0/en/model\_doc/auto#transformers.AutoTokenizer). See \[PreTrainedTokenizer.encode()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.encode) and \[PreTrainedTokenizer.\_\_call\_\_()](/docs/transformers/v5.3.0/en/internal/tokenization\_utils#transformers.PreTrainedTokenizerBase.\_\_call\_\_) for details. \[What are input IDs?](../glossary#input-ids).



pixel\_values (`torch.FloatTensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`) : The tensors corresponding to the input images. Pixel values can be obtained using \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast). See \[Owlv2ImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) uses \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast) for processing images).



attention\_mask (`torch.Tensor` of shape `(batch\_size, sequence\_length)`, \*optional\*) : Mask to avoid performing attention on padding token indices. Mask values selected in `\[0, 1]`:  - 1 for tokens that are \*\*not masked\*\*, - 0 for tokens that are \*\*masked\*\*.  \[What are attention masks?](../glossary#attention-mask)



output\_attentions (`bool`, \*optional\*) : Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned tensors for more detail.



output\_hidden\_states (`bool`, \*optional\*) : Whether or not to return the last hidden state. See `text\_model\_last\_hidden\_state` and `vision\_model\_last\_hidden\_state` under returned tensors for more detail.



interpolate\_pos\_encoding (`bool`, \*optional\*, defaults to `False`) : Whether to interpolate the pre-trained position encodings.



return\_dict (`bool`, \*optional\*) : Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.



\*\*Returns:\*\*



``Owlv2ObjectDetectionOutput` or `tuple(torch.FloatTensor)``



A `Owlv2ObjectDetectionOutput` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.

\#### image\_guided\_detection\[\[transformers.Owlv2ForObjectDetection.image\_guided\_detection]]



\[Source](https://github.com/huggingface/transformers/blob/v5.3.0/src/transformers/models/owlv2/modeling\_owlv2.py#L1479)



\- \*\*logits\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_patches, num\_queries)`) -- Classification logits (including no-object) for all queries.

\- \*\*image\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, patch\_size, patch\_size, output\_dim`) -- Pooled output of \[Owlv2VisionModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionModel). OWLv2 represents images as a set of image patches and computes

&#x20; image embeddings for each patch.

\- \*\*query\_image\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, patch\_size, patch\_size, output\_dim`) -- Pooled output of \[Owlv2VisionModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionModel). OWLv2 represents images as a set of image patches and computes

&#x20; image embeddings for each patch.

\- \*\*target\_pred\_boxes\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_patches, 4)`) -- Normalized boxes coordinates for all queries, represented as (center\_x, center\_y, width, height). These

&#x20; values are normalized in \[0, 1], relative to the size of each individual target image in the batch

&#x20; (disregarding possible padding). You can use \[post\_process\_object\_detection()](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessor.post\_process\_object\_detection) to

&#x20; retrieve the unnormalized bounding boxes.

\- \*\*query\_pred\_boxes\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_patches, 4)`) -- Normalized boxes coordinates for all queries, represented as (center\_x, center\_y, width, height). These

&#x20; values are normalized in \[0, 1], relative to the size of each individual query image in the batch

&#x20; (disregarding possible padding). You can use \[post\_process\_object\_detection()](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessor.post\_process\_object\_detection) to

&#x20; retrieve the unnormalized bounding boxes.

\- \*\*class\_embeds\*\* (`torch.FloatTensor` of shape `(batch\_size, num\_patches, hidden\_size)`) -- Class embeddings of all image patches. OWLv2 represents images as a set of image patches where the total

&#x20; number of patches is (image\_size / patch\_size)\*\*2.

\- \*\*text\_model\_output\*\* (`\~modeling\_outputs.BaseModelOutputWithPooling`, defaults to `None`) -- The output of the \[Owlv2TextModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2TextModel).

\- \*\*vision\_model\_output\*\* (`\~modeling\_outputs.BaseModelOutputWithPooling`, defaults to `None`) -- The output of the \[Owlv2VisionModel](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2VisionModel).



Examples:

```python

>>> import httpx

>>> from io import BytesIO

>>> from PIL import Image

>>> import torch

>>> from transformers import AutoProcessor, Owlv2ForObjectDetection



>>> processor = AutoProcessor.from\_pretrained("google/owlv2-base-patch16-ensemble")

>>> model = Owlv2ForObjectDetection.from\_pretrained("google/owlv2-base-patch16-ensemble")



>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> with httpx.stream("GET", url) as response:

...     image = Image.open(BytesIO(response.read()))

>>> query\_url = "http://images.cocodataset.org/val2017/000000001675.jpg"

>>> with httpx.stream("GET", query\_url) as response:

...     query\_image = Image.open(BytesIO(response.read()))

>>> inputs = processor(images=image, query\_images=query\_image, return\_tensors="pt")



>>> # forward pass

>>> with torch.no\_grad():

...     outputs = model.image\_guided\_detection(\*\*inputs)



>>> target\_sizes = torch.Tensor(\[image.size\[::-1]])



>>> # Convert outputs (bounding boxes and class logits) to Pascal VOC format (xmin, ymin, xmax, ymax)

>>> results = processor.post\_process\_image\_guided\_detection(

...     outputs=outputs, threshold=0.9, nms\_threshold=0.3, target\_sizes=target\_sizes

... )

>>> i = 0  # Retrieve predictions for the first image

>>> boxes, scores = results\[i]\["boxes"], results\[i]\["scores"]

>>> for box, score in zip(boxes, scores):

...     box = \[round(i, 2) for i in box.tolist()]

...     print(f"Detected similar object with confidence {round(score.item(), 3)} at location {box}")

Detected similar object with confidence 0.938 at location \[327.31, 54.94, 547.39, 268.06]

Detected similar object with confidence 0.959 at location \[5.78, 360.65, 619.12, 366.39]

Detected similar object with confidence 0.902 at location \[2.85, 360.01, 627.63, 380.8]

Detected similar object with confidence 0.985 at location \[176.98, -29.45, 672.69, 182.83]

Detected similar object with confidence 1.0 at location \[6.53, 14.35, 624.87, 470.82]

Detected similar object with confidence 0.998 at location \[579.98, 29.14, 615.49, 489.05]

Detected similar object with confidence 0.985 at location \[206.15, 10.53, 247.74, 466.01]

Detected similar object with confidence 0.947 at location \[18.62, 429.72, 646.5, 457.72]

Detected similar object with confidence 0.996 at location \[523.88, 20.69, 586.84, 483.18]

Detected similar object with confidence 0.998 at location \[3.39, 360.59, 617.29, 499.21]

Detected similar object with confidence 0.969 at location \[4.47, 449.05, 614.5, 474.76]

Detected similar object with confidence 0.966 at location \[31.44, 463.65, 654.66, 471.07]

Detected similar object with confidence 0.924 at location \[30.93, 468.07, 635.35, 475.39]

```



\*\*Parameters:\*\*



pixel\_values (`torch.FloatTensor` of shape `(batch\_size, num\_channels, image\_size, image\_size)`) : The tensors corresponding to the input images. Pixel values can be obtained using \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast). See \[Owlv2ImageProcessorFast.\_\_call\_\_()](/docs/transformers/v5.3.0/en/model\_doc/fuyu#transformers.FuyuImageProcessor.\_\_call\_\_) for details (\[Owlv2Processor](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Processor) uses \[Owlv2ImageProcessorFast](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2ImageProcessorFast) for processing images).



query\_pixel\_values (`torch.FloatTensor` of shape `(batch\_size, num\_channels, height, width)`) : Pixel values of query image(s) to be detected. Pass in one query image per target image.



output\_attentions (`bool`, \*optional\*) : Whether or not to return the attentions tensors of all attention layers. See `attentions` under returned tensors for more detail.



output\_hidden\_states (`bool`, \*optional\*) : Whether or not to return the hidden states of all layers. See `hidden\_states` under returned tensors for more detail.



interpolate\_pos\_encoding (`bool`, \*optional\*, defaults to `False`) : Whether to interpolate the pre-trained position encodings.



return\_dict (`bool`, \*optional\*) : Whether or not to return a \[ModelOutput](/docs/transformers/v5.3.0/en/main\_classes/output#transformers.utils.ModelOutput) instead of a plain tuple.



\*\*Returns:\*\*



``Owlv2ImageGuidedObjectDetectionOutput` or `tuple(torch.FloatTensor)``



A `Owlv2ImageGuidedObjectDetectionOutput` or a tuple of

`torch.FloatTensor` (if `return\_dict=False` is passed or when `config.return\_dict=False`) comprising various

elements depending on the configuration (\[Owlv2Config](/docs/transformers/v5.3.0/en/model\_doc/owlv2#transformers.Owlv2Config)) and inputs.





