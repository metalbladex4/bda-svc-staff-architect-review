\# Zero-shot object detection



Traditionally, models used for \[object detection](object\_detection) require labeled image datasets for training,

and are limited to detecting the set of classes from the training data.



Zero-shot object detection is a computer vision task to detect objects and their classes in images, without any

prior training or knowledge of the classes. Zero-shot object detection models receive an image as input, as well

as a list of candidate classes, and output the bounding boxes and labels where the objects have been detected.



> \[!NOTE]

> Hugging Face houses many such \[open vocabulary zero shot object detectors](https://huggingface.co/models?pipeline\_tag=zero-shot-object-detection).



In this guide, you will learn how to use such models:



\- to detect objects based on text prompts

\- for batch object detection

\- for image-guided object detection



Before you begin, make sure you have all the necessary libraries installed:



```bash

pip install -q transformers

```



\## Zero-shot object detection pipeline



The simplest way to try out inference with models is to use it in a \[pipeline()](/docs/transformers/v5.3.0/en/main\_classes/pipelines#transformers.pipeline). Instantiate a pipeline

for zero-shot object detection from a \[checkpoint on the Hugging Face Hub](https://huggingface.co/models?pipeline\_tag=zero-shot-object-detection):



```python

>>> from transformers import pipeline



>>> # Use any checkpoint from the hf.co/models?pipeline\_tag=zero-shot-object-detection

>>> checkpoint = "iSEE-Laboratory/llmdet\_large"

>>> detector = pipeline(model=checkpoint, task="zero-shot-object-detection")

```



Next, choose an image you'd like to detect objects in. Here we'll use the image of astronaut Eileen Collins that is

a part of the \[NASA](https://www.nasa.gov/multimedia/imagegallery/index.html) Great Images dataset.



```py

>>> from transformers.image\_utils import load\_image



>>> url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/zero-sh-obj-detection\_1.png"

>>> image = load\_image(url)

>>> image

```



&#x20;    



Pass the image and the candidate object labels to look for to the pipeline.

Here we pass the image directly; other suitable options include a local path to an image or an image url. We also pass text descriptions for all items we want to query the image for.



```py

>>> predictions = detector(

...     image,

...     candidate\_labels=\["human face", "rocket", "nasa badge", "star-spangled banner"],

...     threshold=0.45,

... )

>>> predictions

\[{'score': 0.8409242033958435,

&#x20; 'label': 'human face',

&#x20; 'box': {'xmin': 179, 'ymin': 74, 'xmax': 272, 'ymax': 179}},

&#x20;{'score': 0.7380027770996094,

&#x20; 'label': 'rocket',

&#x20; 'box': {'xmin': 353, 'ymin': 0, 'xmax': 466, 'ymax': 284}},

&#x20;{'score': 0.5850900411605835,

&#x20; 'label': 'star-spangled banner',

&#x20; 'box': {'xmin': 0, 'ymin': 0, 'xmax': 96, 'ymax': 511}},

&#x20;{'score': 0.5697067975997925,

&#x20; 'label': 'human face',

&#x20; 'box': {'xmin': 18, 'ymin': 15, 'xmax': 366, 'ymax': 511}},

&#x20;{'score': 0.47813931107521057,

&#x20; 'label': 'star-spangled banner',

&#x20; 'box': {'xmin': 353, 'ymin': 0, 'xmax': 459, 'ymax': 274}},

&#x20;{'score': 0.46597740054130554,

&#x20; 'label': 'nasa badge',

&#x20; 'box': {'xmin': 353, 'ymin': 0, 'xmax': 462, 'ymax': 279}},

&#x20;{'score': 0.4585932493209839,

&#x20; 'label': 'nasa badge',

&#x20; 'box': {'xmin': 132, 'ymin': 348, 'xmax': 208, 'ymax': 423}}]

```



Let's visualize the predictions:



```py

>>> from PIL import ImageDraw



>>> draw = ImageDraw.Draw(image)



>>> for prediction in predictions:

...     box = prediction\["box"]

...     label = prediction\["label"]

...     score = prediction\["score"]



...     xmin, ymin, xmax, ymax = box.values()

...     draw.rectangle((xmin, ymin, xmax, ymax), outline="red", width=1)

...     draw.text((xmin, ymin), f"{label}: {round(score,2)}", fill="white")



>>> image

```



&#x20;    



\## Text-prompted zero-shot object detection by hand



Now that you've seen how to use the zero-shot object detection pipeline, let's replicate the same result manually.



Start by loading the model and associated processor from a \[checkpoint on the Hugging Face Hub](hf.co/iSEE-Laboratory/llmdet\_large).

Here we'll use the same checkpoint as before:



```py

>>> from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection



>>> model = AutoModelForZeroShotObjectDetection.from\_pretrained(checkpoint, device\_map="auto")

>>> processor = AutoProcessor.from\_pretrained(checkpoint)

```



Let's take a different image to switch things up.



```py

>>> url = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/zero-sh-obj-detection\_3.png"

>>> image = load\_image(url)

>>> image

```



&#x20;    



Use the processor to prepare the inputs for the model.



```py

>>> text\_labels = \["hat", "book", "sunglasses", "camera"]

>>> inputs = processor(text=text\_labels, images=image, return\_tensors="pt")to(model.device)

```



Pass the inputs through the model, post-process, and visualize the results. Since the image processor resized images before

feeding them to the model, you need to use the `post\_process\_object\_detection` method to make sure the predicted bounding

boxes have the correct coordinates relative to the original image:



```py

>>> import torch



>>> with torch.inference\_mode():

...     outputs = model(\*\*inputs)



>>> results = processor.post\_process\_grounded\_object\_detection(

...    outputs, threshold=0.50, target\_sizes=\[(image.height, image.width)], text\_labels=text\_labels,

...)\[0]



>>> draw = ImageDraw.Draw(image)



>>> scores = results\["scores"]

>>> text\_labels = results\["text\_labels"]

>>> boxes = results\["boxes"]



>>> for box, score, text\_label in zip(boxes, scores, text\_labels):

...     xmin, ymin, xmax, ymax = box

...     draw.rectangle((xmin, ymin, xmax, ymax), outline="red", width=1)

...     draw.text((xmin, ymin), f"{text\_label}: {round(score.item(),2)}", fill="white")



>>> image

```



&#x20;    



\## Batch processing



You can pass multiple sets of images and text queries to search for different (or same) objects in several images.

Let's use both an astronaut image and the beach image together.

For batch processing, you should pass text queries as a nested list to the processor and images as lists of PIL images,

PyTorch tensors, or NumPy arrays.



```py

>>> url1 = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/zero-sh-obj-detection\_1.png"

>>> url2 = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/transformers/tasks/zero-sh-obj-detection\_3.png"

>>> images = \[load\_image(url1), load\_image(url2)]

>>> text\_queries = \[

...     \["human face", "rocket", "nasa badge", "star-spangled banner"],

...     \["hat", "book", "sunglasses", "camera", "can"],

... ]

>>> inputs = processor(text=text\_queries, images=images, return\_tensors="pt", padding=True)

```



Previously for post-processing you passed the single image's size as a tensor, but you can also pass a tuple, or, in case

of several images, a list of tuples. Let's create predictions for the two examples, and visualize the second one (`image\_idx = 1`).



```py

>>> with torch.no\_grad():

>>>     outputs = model(\*\*inputs)



>>> target\_sizes = \[(image.height, image.width) for image in images]

>>> results = processor.post\_process\_grounded\_object\_detection(

...     outputs, threshold=0.3, target\_sizes=target\_sizes, text\_labels=text\_labels,

... )

```



Let's visualize the results:



```py

>>> image\_idx = 1

>>> draw = ImageDraw.Draw(images\[image\_idx])



>>> scores = results\[image\_idx]\["scores"].tolist()

>>> text\_labels = results\[image\_idx]\["text\_labels"]

>>> boxes = results\[image\_idx]\["boxes"].tolist()



>>> for box, score, text\_label in zip(boxes, scores, text\_labels):

>>>     xmin, ymin, xmax, ymax = box

>>>     draw.rectangle((xmin, ymin, xmax, ymax), outline="red", width=1)

>>>     draw.text((xmin, ymin), f"{text\_label}: {round(score,2)}", fill="white")



>>> images\[image\_idx]

```



&#x20;    



\## Image-guided object detection



In addition to zero-shot object detection with text queries, models like \[OWL-ViT](https://huggingface.co/collections/ariG23498/owlvit-689b0d0872a7634a6ea17ae7) and \[OWLv2](https://huggingface.co/collections/ariG23498/owlv2-689b0d27bd7d96ba3c7f7530) offers image-guided object detection. This means you can use an image query to find similar

objects in the target image.



```py

>>> from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection



>>> checkpoint = "google/owlv2-base-patch16-ensemble"

>>> model = AutoModelForZeroShotObjectDetection.from\_pretrained(checkpoint, device\_map="auto")

>>> processor = AutoProcessor.from\_pretrained(checkpoint)

```



Unlike text queries, only a single example image is allowed.



Let's take an image with two cats on a couch as a target image, and an image of a single cat

as a query:



```py

>>> url = "http://images.cocodataset.org/val2017/000000039769.jpg"

>>> image\_target = Image.open(requests.get(url, stream=True).raw)



>>> query\_url = "http://images.cocodataset.org/val2017/000000524280.jpg"

>>> query\_image = Image.open(requests.get(query\_url, stream=True).raw)

```



Let's take a quick look at the images:



```py

>>> import matplotlib.pyplot as plt



>>> fig, ax = plt.subplots(1, 2)

>>> ax\[0].imshow(image\_target)

>>> ax\[1].imshow(query\_image)

>>> fig.show()

```



&#x20;    



In the preprocessing step, instead of text queries, you now need to use `query\_images`:



```py

>>> inputs = processor(images=image\_target, query\_images=query\_image, return\_tensors="pt")

```



For predictions, instead of passing the inputs to the model, pass them to \[image\_guided\_detection()](/docs/transformers/v5.3.0/en/model\_doc/owlvit#transformers.OwlViTForObjectDetection.image\_guided\_detection). Draw the predictions

as before except now there are no labels.



```py

>>> with torch.no\_grad():

...     outputs = model.image\_guided\_detection(\*\*inputs)

...     target\_sizes = torch.tensor(\[image\_target.size\[::-1]])

...     results = processor.post\_process\_image\_guided\_detection(outputs=outputs, target\_sizes=target\_sizes)\[0]



>>> draw = ImageDraw.Draw(image\_target)



>>> scores = results\["scores"].tolist()

>>> boxes = results\["boxes"].tolist()



>>> for box, score in zip(boxes, scores):

...     xmin, ymin, xmax, ymax = box

...     draw.rectangle((xmin, ymin, xmax, ymax), outline="white", width=4)



>>> image\_target

```



&#x20;    





