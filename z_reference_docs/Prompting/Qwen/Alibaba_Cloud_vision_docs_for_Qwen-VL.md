Visual understanding models answer questions about the images and videos you provide, supporting single or multiple image inputs for tasks such as image captioning, visual question answering, and object localization.



\*\*Supported regions:\*\* Singapore, US (Virginia), China (Beijing), China (Hong Kong), and Germany (Frankfurt). An \[API key](/help/en/model-studio/get-api-key) is required for each region.



\*\*Try it online:\*\* Go to the \[Alibaba Cloud Model Studio console](https://modelstudio.console.alibabacloud.com/), select a region in the upper-right corner, and then navigate to the \[Vision](https://modelstudio.console.alibabacloud.com/ap-southeast-1/?tab=dashboard#/efm/model\_experience\_center/vision) page.



\## \*\*Getting started\*\*



\*\*Prerequisites\*\*



\-   \[Get an API key](/help/en/model-studio/get-api-key) and \[export it as an environment variable](/help/en/model-studio/configure-api-key-through-environment-variables).

&#x20;   

\-   To call with an SDK, install the \[SDK](/help/en/model-studio/install-sdk). Use DashScope Python SDK 1.24.6 or later, or DashScope Java SDK 2.21.10 or later.

&#x20;   



The following examples show how to call a model to describe image content. See \[How to pass local files](#d987f8de5395x) and \[Image limits](#71c2cb6e09ioo).



\## OpenAI compatible



\## Python



```

from openai import OpenAI

import os



client = OpenAI(

&#x20;   # An API key is required for each Region. To get an API key, visit: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   # Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;   base\_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

)



completion = client.chat.completions.create(

&#x20;   model="qwen3.5-plus",  # Uses qwen3.5-plus model. See https://www.alibabacloud.com/help/en/model-studio/getting-started/models for other models.

&#x20;   messages=\[

&#x20;       {

&#x20;           "role": "user",

&#x20;           "content": \[

&#x20;               {

&#x20;                   "type": "image\_url",

&#x20;                   "image\_url": {

&#x20;                       "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"

&#x20;                   },

&#x20;               },

&#x20;               {"type": "text", "text": "What is depicted in the image?"},

&#x20;           ],

&#x20;       },

&#x20;   ],

)

print(completion.choices\[0].message.content)

```



\### \*\*Response\*\*



```

This is a photo taken on a beach. In the photo, a person and a dog are sitting on the sand, with the sea and sky in the background. The person and dog appear to be interacting, with the dog's front paw resting on the person's hand. Sunlight is coming from the right side of the frame, adding a warm atmosphere to the scene.

```



\## Node.js



```

import OpenAI from "openai";



const openai = new OpenAI({

&#x20; // An API key is required for each Region. To get an API key, visit: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20; // If you have not set an environment variable, replace the following line with your Model Studio API key: apiKey: "sk-xxx"

&#x20; apiKey: process.env.DASHSCOPE\_API\_KEY,

&#x20; // Endpoints vary by Region. Modify the endpoint for your Region.

&#x20; baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

});



async function main() {

&#x20; const response = await openai.chat.completions.create({

&#x20;   model: "qwen3.5-plus",   // Uses qwen3.5-plus model. See https://www.alibabacloud.com/help/en/model-studio/getting-started/models for other models.

&#x20;   messages: \[

&#x20;     {

&#x20;       role: "user",

&#x20;       content: \[{

&#x20;           type: "image\_url",

&#x20;           image\_url": {

&#x20;             "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"

&#x20;           }

&#x20;         },

&#x20;         {

&#x20;           type: "text",

&#x20;           text: "What is depicted in the image?"

&#x20;         }

&#x20;       ]

&#x20;     }

&#x20;   ]

&#x20; });

&#x20; console.log(response.choices\[0].message.content);

}

main()

```



\### \*\*Response\*\*



```

This is a photo taken on a beach. In the photo, a person and a dog are sitting on the sand, with the sea and sky in the background. The person and dog appear to be interacting, with the dog's front paw resting on the person's hand. Sunlight is coming from the right side of the frame, adding a warm atmosphere to the scene.

```



\## curl



```

\# ======= Important =======

\# Endpoints vary by Region. Modify the endpoint for your Region.

\# An API key is required for each Region. To get an API key, visit: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# === Delete this comment before execution ===



curl --location 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions' \\

\--header "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\--header 'Content-Type: application/json' \\

\--data '{

&#x20; "model": "qwen3.5-plus",

&#x20; "messages": \[

&#x20;   {"role": "user",

&#x20;    "content": \[

&#x20;       {"type": "image\_url", "image\_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"}},

&#x20;       {"type": "text", "text": "What is depicted in the image?"}

&#x20;   ]

&#x20; }]

}'

```



\### \*\*Response\*\*



```

{

&#x20; "choices": \[

&#x20;   {

&#x20;     "message": {

&#x20;       "content": "This is a photo taken on a beach. In the photo, a person and a dog are sitting on the sand, with the sea and sky in the background. The person and dog appear to be interacting, with the dog's front paw resting on the person's hand. Sunlight is coming from the right side of the frame, adding a warm atmosphere to the scene.",

&#x20;       "role": "assistant"

&#x20;     },

&#x20;     "finish\_reason": "stop",

&#x20;     "index": 0,

&#x20;     "logprobs": null

&#x20;   }

&#x20; ],

&#x20; "object": "chat.completion",

&#x20; "usage": {

&#x20;   "prompt\_tokens": 1270,

&#x20;   "completion\_tokens": 54,

&#x20;   "total\_tokens": 1324

&#x20; },

&#x20; "created": 1725948561,

&#x20; "system\_fingerprint": null,

&#x20; "model": "qwen3.5-plus",

&#x20; "id": "chatcmpl-0fd66f46-b09e-9164-a84f-3ebbbedbac15"

}

```



\## DashScope



\## Python



```

import os

import dashscope



\# Endpoints vary by Region. Modify the endpoint for your Region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



messages = \[

{

&#x20;   "role": "user",

&#x20;   "content": \[

&#x20;   {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"},

&#x20;   {"text": "What is depicted in the image?"}]

}]



response = dashscope.MultiModalConversation.call(

&#x20;   # An API key is required for each Region. To get an API key, visit: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not set an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx"

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   model='qwen3.5-plus',   # Uses qwen3.5-plus model. See https://www.alibabacloud.com/help/en/model-studio/getting-started/models for other models.

&#x20;   messages=messages

)



print(response.output.choices\[0].message.content\[0]\["text"])

```



\### \*\*Response\*\*



```

This is a photo taken on a beach. In the photo, there is a woman and a dog. The woman is sitting on the sand, smiling and interacting with the dog. The dog is wearing a collar and appears to be shaking hands with the woman. The background is the sea and the sky, and the sunlight shining on them creates a warm atmosphere.

```



\## Java



```

import java.util.Arrays;

import java.util.Collections;



import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {

&#x20;   

&#x20;   // Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;   static {

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }

&#x20;   

&#x20;   public static void simpleMultiModalConversationCall()

&#x20;           throws ApiException, NoApiKeyException, UploadFileException {

&#x20;       MultiModalConversation conv = new MultiModalConversation(); 

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(

&#x20;                       Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"),

&#x20;                       Collections.singletonMap("text", "What is depicted in the image?"))).build();

&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // An API key is required for each Region. To get an API key, visit: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               // If you have not set an environment variable, replace the following line with your Model Studio API key: .apiKey("sk-xxx")

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen3.5-plus")  //  This example uses the qwen3.5-plus model. You can replace it with other models. For a list of available models, see: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;               .messages(Arrays.asList(userMessage))

&#x20;               .build();

&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));

&#x20;   }

&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           simpleMultiModalConversationCall();

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\### \*\*Response\*\*



```

This is a photo taken on a beach. In the photo, there is a person in a plaid shirt and a dog with a collar. The person and the dog are sitting face to face, seemingly interacting. The background is the sea and the sky, and the sunlight shining on them creates a warm atmosphere.

```



\## curl



```

\# ======= Important =======

\# Endpoints vary by Region. Modify the endpoint for your Region.

\# An API key is required for each Region. To get an API key, visit: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# === Delete this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "input":{

&#x20;       "messages":\[

&#x20;           {

&#x20;               "role": "user",

&#x20;               "content": \[

&#x20;                   {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"},

&#x20;                   {"text": "What is depicted in the image?"}

&#x20;               ]

&#x20;           }

&#x20;       ]

&#x20;   }

}'

```



\### \*\*Response\*\*



```

{

&#x20; "output": {

&#x20;   "choices": \[

&#x20;     {

&#x20;       "finish\_reason": "stop",

&#x20;       "message": {

&#x20;         "role": "assistant",

&#x20;         "content": \[

&#x20;           {

&#x20;             "text": "This is a photo taken on a beach. In the photo, there is a person in a plaid shirt and a dog with a collar. They are sitting on the sand, with the sea and sky in the background. Sunlight is coming from the right side of the frame, adding a warm atmosphere to the scene."

&#x20;           }

&#x20;         ]

&#x20;       }

&#x20;     }

&#x20;   ]

&#x20; },

&#x20; "usage": {

&#x20;   "output\_tokens": 55,

&#x20;   "input\_tokens": 1271,

&#x20;   "image\_tokens": 1247

&#x20; },

&#x20; "request\_id": "ccf845a3-dc33-9cda-b581-20fe7dc23f70"

}

```



\## \*\*Model selection\*\*



\-   \*\*Recommended Qwen3.5\*\*: The latest generation of visual understanding models. It excels at tasks like multimodal reasoning, 2D/3D image understanding, complex document parsing, visual programming, video understanding, and building multimodal agents. Available in the Chinese mainland and Singapore regions.

&#x20;   

&#x20;   -   `qwen3.5-plus`: The most capable model in the Qwen3.5 series, recommended for tasks that require the highest accuracy and performance.

&#x20;       

&#x20;   -   `qwen3.5-flash`: A faster, more cost-effective choice that balances performance and cost, ideal for latency-sensitive scenarios.

&#x20;       

&#x20;   -   The open-source models in the Qwen3.5 series include `qwen3.5-397b-a17b`, `qwen3.5-122b-a10b`, `qwen3.5-27b`, and `qwen3.5-35b-a3b`.

&#x20;       

\-   The Qwen3-VL series is also suitable for tasks requiring high-precision object recognition and localization (including 3D), agent tool calling, document and webpage parsing, complex problem solving, and long video understanding.

&#x20;   

&#x20;   -   `qwen3-vl-plus`: The most powerful model in the Qwen3-VL series.

&#x20;       

&#x20;   -   `qwen3-vl-flash`: A faster, more cost-effective choice that balances performance and cost, ideal for latency-sensitive scenarios.

&#x20;       

\-   The Qwen2.5-VL series is suitable for general-purpose tasks such as simple image captioning and extracting summaries from short videos.

&#x20;   

&#x20;   -   `qwen-vl-max`: The best-performing model in the Qwen2.5-VL series.

&#x20;       

&#x20;   -   `qwen-vl-plus`: A faster model that provides a good balance between performance and cost.

&#x20;       



For model names, context, pricing, and snapshot versions, see \[Model list](/help/en/model-studio/models). For concurrency limits, see \[Rate limiting](/help/en/model-studio/rate-limit).



\*\*Model feature comparison\*\*



| \*\*Model\*\* | \[\*\*Deep thinking\*\*](/help/en/model-studio/visual-reasoning) | \[\*\*Tool calling\*\*](/help/en/model-studio/qwen-function-calling) | \[Context cache](/help/en/model-studio/context-cache) | \[Structured output](/help/en/model-studio/qwen-structured-output) | \*\*Languages\*\* |

| --- | --- | --- | --- | --- | --- |

| `Qwen3.5` series | Supported | Supported | Supported in the stable versions of `qwen3.5-plus` and `qwen3.5-flash`. > Explicit cache only. | Supported when deep thinking is disabled. | 33 languages: Chinese, Japanese, Korean, Indonesian, Vietnamese, Thai, English, French, German, Russian, Portuguese, Spanish, Italian, Swedish, Danish, Czech, Norwegian, Dutch, Finnish, Turkish, Polish, Swahili, Romanian, Serbian, Greek, Kazakh, Uzbek, Cebuano, Arabic, Urdu, Persian, Hindi/Devanagari, and Hebrew. |

| `Qwen3-VL` series | Supported | Supported | Supported in the stable versions of `qwen3-vl-plus` and `qwen3-vl-flash`. | Supported when deep thinking is disabled. | 33 languages: Chinese, Japanese, Korean, Indonesian, Vietnamese, Thai, English, French, German, Russian, Portuguese, Spanish, Italian, Swedish, Danish, Czech, Norwegian, Dutch, Finnish, Turkish, Polish, Swahili, Romanian, Serbian, Greek, Kazakh, Uzbek, Cebuano, Arabic, Urdu, Persian, Hindi/Devanagari, and Hebrew. |

| `Qwen2.5-VL` series | Not supported | Not supported | Supported in the stable versions of `qwen-vl-max` and `qwen-vl-plus`. | Supported in the stable and latest versions of `qwen-vl-max` and `qwen-vl-plus`. | 11 languages: Chinese, English, Japanese, Korean, Arabic, Vietnamese, French, German, Italian, Spanish, and Russian. |



\## \*\*Capabilities\*\*



\### \*\*Visual question answering (VQA)\*\*



Describe and classify image content, such as identifying people, places, animals, and plants.



| !\[p1021359](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4450772671/p1025117.webp) If the sun is glaring, what item from this image should I use? | When the sun is glaring, you should use the pink sunglasses from the image. Sunglasses can effectively block strong light, reduce UV damage to your eyes, and help protect your vision while improving comfort in bright sunlight. |

| --- | --- |



\### \*\*Creative writing\*\*



Generate vivid text descriptions from image or video content for creative scenarios like story writing, copywriting, and developing short video scripts.



| !\[vl-问答](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4450772671/p1025118.webp) Based on the image, write an engaging social media post for me. | Of course. This image has a rich Mid-Autumn Festival atmosphere, with a clever mix of classic and modern elements. Based on the key elements in the image, I've prepared a few social media post ideas in different styles for you to choose from. \*\*Poetic and aesthetic style\*\* Tonight, the moon shines bright for all to see, as autumn thoughts drift to thee. Chang'e's flight and the Jade Rabbit's potion—the romance of ages is rekindled tonight. May this moon light your way home and carry my deepest wishes. Happy Mid-Autumn Festival! \*\*Warm and heartfelt style\*\* A full moon for a full reunion on this gentle Mid-Autumn night. Watching fireworks, gazing at the moon, savoring a mooncake, and wishing you well. May all our hopes and dreams come true. Wishing everyone a happy Mid-Autumn Festival and a joyful family reunion! |

| --- | --- |



\### \*\*OCR and information extraction\*\*



Recognize text and formulas in images, or extract information from documents like receipts, certificates, and forms. These models support formatted text output. Both the Qwen3.5 and Qwen3-VL models have expanded their language support to 33 languages. For a list of supported languages, see the \[Model feature comparison](#a47aeb6443ysh).



| !\[-q2cdz6jy89b6m3kp](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4450772671/p1025119.webp) Extract the following fields from the image: \\\\\['Invoice Code', 'Invoice Number', 'Destination', 'Fuel Surcharge', 'Fare', 'Travel Date', 'Departure Time', 'Train Number', 'Seat Number'\\\\]. Output the result in JSON format. | { "Invoice Code": "221021325353", "Invoice Number": "10283819", "Destination": "Development Zone", "Fuel Surcharge": "2.0", "Fare": "8.00<Full>", "Travel Date": "2013-06-29", "Departure Time": "Serial", "Train Number": "040", "Seat Number": "371" } |

| --- | --- |



\### \*\*Multi-disciplinary problem solving\*\*



Solve problems from various subjects found in images, including mathematics, physics, and chemistry. It supports educational applications from K-12 to adult learning.



| !\[-5jwcstcvmdpqghaj](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4923073671/p1025120.webp) Solve the math problem in the image step by step. | !\[-答案](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4923073671/p1025121.webp) |

| --- | --- |



\### \*\*Visual\*\* programming



Generate code from images or videos to convert design mockups, website screenshots, and other visual inputs into HTML, CSS, and JS code.



| !\[code](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) Create a webpage using HTML and CSS based on my sketch. The main color theme should be black. | !\[code-预览](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) \*\*Webpage preview\*\* |

| --- | --- |



\### \*\*Object\*\* localization



Supports both 2D and 3D localization to determine object orientation, perspective changes, and occlusion relationships. 3D localization is a new capability of the Qwen3-VL model.



> For the Qwen2.5-VL model, object localization is most robust within a resolution range of 480x480 to 2560x2560 pixels. Outside this range, detection accuracy may decrease, with occasional bounding box drift.



> To draw the localization results on the original image, see \[FAQ](#178c39c20b290).



| \*\*2D positioning\*\* !\[-530xdcos1lqkcfuy](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) - Returns bounding box coordinates: Detects all food items in an image and outputs their bounding box (bbox) coordinates in JSON format. - Returns center point coordinates: Locates all food items in an image as points and outputs their point coordinates in XML format. | \*\*Visualization of 2D positioning results\*\* !\[-mu9podu1eyvph1zd](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |

| --- | --- |

| \*\*3D positioning\*\* !\[3d](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) Detects cars in an image and predicts their 3D positions. JSON output: `\[{"bbox\_3d": \[x\_center, y\_center, z\_center, x\_size, y\_size, z\_size, roll, pitch, yaw], "label": "category"}]`. | \*\*Visualization of 3D positioning results\*\* !\[3d-results](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) |



\### \*\*Document\*\* parsing



Parse image-based documents, such as scans or image-based PDFs, into QwenVL HTML or QwenVL Markdown format. This format accurately recognizes text and gets position information for elements such as images and tables. The Qwen3-VL Model adds the ability to parse documents into Markdown format.



> Recommended prompts: `qwenvl html` (to parse into HTML format) or `qwenvl markdown` (to parse into Markdown format).



| !\[image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) qwenvl markdown. | !\[-结果](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=) \*\*Visualization of results\*\* |

| --- | --- |



\### \*\*Video understanding\*\*



Analyze video content to locate specific events and get their timestamps, or to generate summaries of key time periods.



| Describe the series of actions performed by the person in the video. Output the result in JSON format with start\\\\\_time, end\\\\\_time, and event fields. Use the HH:mm:ss format for the timestamp. | { "events": \\\\\[ { "start\\\\\_time": "00:00:00", "end\\\\\_time": "00:00:05", "event": "The person walks to a table holding a cardboard box and places it on the table." }, { "start\\\\\_time": "00:00:05", "end\\\\\_time": "00:00:15", "event": "The person picks up a scanner and aims it at the label on the box to scan it." }, { "start\\\\\_time": "00:00:15", "end\\\\\_time": "00:00:21", "event": "The person puts the scanner back in its place and then picks up a pen to write information in a notebook."}\\\\] } |

| --- | --- |



\## \*\*Core\*\* capabilities



\### \*\*Enable\*\* or disable thinking mode



\-   The `qwen3.5`, `qwen3-vl-plus`, and `qwen3-vl-flash` series are hybrid models that can respond either directly or after reasoning. Use the `enable\_thinking` parameter to control whether to enable `thinking mode`:

&#x20;   

&#x20;   -   `true`: The default for the `qwen3.5` series.

&#x20;       

&#x20;   -   `false`: The default for the `qwen3-vl-plus` and `qwen3-vl-flash` series.

&#x20;       

\-   Models with a `thinking` suffix, such as `qwen3-vl-235b-a22b-thinking`, are dedicated reasoning models. They always reason before responding, and this feature cannot be disabled.

&#x20;   



\*\*Important\*\*



\-   \*\*Model configuration:\*\* In general conversational scenarios that do not involve tool calling, do not set the `System Message` for optimal performance. Instead, you can pass instructions, such as model role settings and output format requirements, through the `User Message`.

&#x20;   

\-   \*\*Use streaming output:\*\* When `thinking mode` is enabled, both \*\*streaming and non-streaming\*\* output are supported. To avoid long-response timeouts, use `streaming output`.

&#x20;   

\-   \*\*Limiting the thinking length:\*\* Deep thinking models sometimes produce verbose reasoning. You can use the `thinking\_budget` parameter to limit the length of the thinking process. If the number of tokens generated during the thinking process exceeds `thinking\_budget`, the reasoning is truncated and the model immediately begins to generate the final response. The default value of `thinking\_budget` is the model's maximum chain-of-thought length. See the \[Model list](/help/en/model-studio/models).

&#x20;   



\## OpenAI



The `enable\_thinking` parameter is not a standard OpenAI parameter. If you use the OpenAI Python SDK, pass it through `extra\_body`.



Python



```

import os

from openai import OpenAI



client = OpenAI(

&#x20;   # Each region requires a unique API Key. To get an API Key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   # Endpoints vary by region. Set the endpoint for your region.

&#x20;   base\_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

)



reasoning\_content = ""  # Stores the full reasoning process.

answer\_content = ""     # Stores the full response.

is\_answering = False   # Tracks if the model is generating the final answer.

enable\_thinking = True

\# Create a chat completion request.

completion = client.chat.completions.create(

&#x20;   model="qwen3.5-plus",

&#x20;   messages=\[

&#x20;       {

&#x20;           "role": "user",

&#x20;           "content": \[

&#x20;               {

&#x20;                   "type": "image\_url",

&#x20;                   "image\_url": {

&#x20;                       "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN\_!!6000000002727-0-tps-1024-406.jpg"

&#x20;                   },

&#x20;               },

&#x20;               {"type": "text", "text": "How do I solve this problem?"},

&#x20;           ],

&#x20;       },

&#x20;   ],

&#x20;   stream=True,

&#x20;   # `thinking mode` is toggleable for `qwen3.5`/`qwen3-vl-plus`/`qwen3-vl-flash`. It is mandatory for models with a 'thinking' suffix and does not apply to other Qwen-VL models.

&#x20;   # The `thinking\_budget` parameter sets the maximum number of tokens for the reasoning process.

&#x20;   extra\_body={

&#x20;       'enable\_thinking': enable\_thinking,

&#x20;       "thinking\_budget": 81920},



&#x20;   # Uncomment the following code to return the token usage in the last chunk.

&#x20;   # stream\_options={

&#x20;   #     "include\_usage": True

&#x20;   # }

)



if enable\_thinking:

&#x20;   print("\\n" + "=" \* 20 + "Thinking Process" + "=" \* 20 + "\\n")



for chunk in completion:

&#x20;   # If chunk.choices is empty, print the usage.

&#x20;   if not chunk.choices:

&#x20;       print("\\nUsage:")

&#x20;       print(chunk.usage)

&#x20;   else:

&#x20;       delta = chunk.choices\[0].delta

&#x20;       # Print the reasoning process.

&#x20;       if hasattr(delta, 'reasoning\_content') and delta.reasoning\_content is not None:

&#x20;           print(delta.reasoning\_content, end='', flush=True)

&#x20;           reasoning\_content += delta.reasoning\_content

&#x20;       else:

&#x20;           # Start printing the response.

&#x20;           if delta.content != "" and is\_answering is False:

&#x20;               print("\\n" + "=" \* 20 + "Complete Response" + "=" \* 20 + "\\n")

&#x20;               is\_answering = True

&#x20;           # Print the response content.

&#x20;           if delta.content is not None:

&#x20;               print(delta.content, end='', flush=True)

&#x20;               answer\_content += delta.content



\# print("=" \* 20 + "Complete Thinking Process" + "=" \* 20 + "\\n")

\# print(reasoning\_content)

\# print("=" \* 20 + "Complete Response" + "=" \* 20 + "\\n")

\# print(answer\_content)

```



Node.js



```

import OpenAI from "openai";



// Initialize the OpenAI client.

const openai = new OpenAI({

&#x20; // Each region requires a unique API Key. To get an API Key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20; // If the environment variable is not set, provide your Model Studio API Key here: apiKey: "sk-xxx"

&#x20; apiKey: process.env.DASHSCOPE\_API\_KEY,

&#x20; // Endpoints vary by region. Set the endpoint for your region.

&#x20; baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

});



let reasoningContent = '';

let answerContent = '';

let isAnswering = false;

let enableThinking = true;



let messages = \[

&#x20;   {

&#x20;       role: "user",

&#x20;       content: \[

&#x20;       { type: "image\_url", image\_url: { "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN\_!!6000000002727-0-tps-1024-406.jpg" } },

&#x20;       { type: "text", text: "How do I solve this problem?" },

&#x20;   ]

}]



async function main() {

&#x20;   try {

&#x20;       const stream = await openai.chat.completions.create({

&#x20;           model: 'qwen3.5-plus',

&#x20;           messages: messages,

&#x20;           stream: true,

&#x20;         // Note: In the Node.js SDK, pass non-standard parameters like enable\_thinking at the top level, not in extra\_body.

&#x20;         enable\_thinking: enableThinking,

&#x20;         thinking\_budget: 81920



&#x20;       });



&#x20;       if (enableThinking){console.log('\\n' + '='.repeat(20) + 'Thinking Process' + '='.repeat(20) + '\\n');}



&#x20;       for await (const chunk of stream) {

&#x20;           if (!chunk.choices?.length) {

&#x20;               console.log('\\nUsage:');

&#x20;               console.log(chunk.usage);

&#x20;               continue;

&#x20;           }



&#x20;           const delta = chunk.choices\[0].delta;



&#x20;           // Process the reasoning content.

&#x20;           if (delta.reasoning\_content) {

&#x20;               process.stdout.write(delta.reasoning\_content);

&#x20;               reasoningContent += delta.reasoning\_content;

&#x20;           }

&#x20;           // Process the response content.

&#x20;           else if (delta.content) {

&#x20;               if (!isAnswering) {

&#x20;                   console.log('\\n' + '='.repeat(20) + 'Complete Response' + '='.repeat(20) + '\\n');

&#x20;                   isAnswering = true;

&#x20;               }

&#x20;               process.stdout.write(delta.content);

&#x20;               answerContent += delta.content;

&#x20;           }

&#x20;       }

&#x20;   } catch (error) {

&#x20;       console.error('Error:', error);

&#x20;   }

}



main();

```



curl



```

\# ======= Important =======

\# Endpoints vary by region. Set the endpoint for your region.

\# Each region requires a unique API Key. To get an API Key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# === Remove this comment before execution ===



curl --location 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions' \\

\--header "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\--header 'Content-Type: application/json' \\

\--data '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "messages": \[

&#x20;   {

&#x20;     "role": "user",

&#x20;     "content": \[

&#x20;       {

&#x20;         "type": "image\_url",

&#x20;         "image\_url": {

&#x20;           "url": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN\_!!6000000002727-0-tps-1024-406.jpg"

&#x20;         }

&#x20;       },

&#x20;       {

&#x20;         "type": "text",

&#x20;         "text": "How do I solve this problem?"

&#x20;       }

&#x20;     ]

&#x20;   }

&#x20; ],

&#x20;   "stream":true,

&#x20;   "stream\_options":{"include\_usage":true},

&#x20;   "enable\_thinking": true,

&#x20;   "thinking\_budget": 81920

}'

```



\## DashScope



Python



```

import os

import dashscope

from dashscope import MultiModalConversation



\# Endpoints vary by region. Set the endpoint for your region.

dashscope.base\_http\_api\_url = "https://dashscope-intl.aliyuncs.com/api/v1"



enable\_thinking=True



messages = \[

&#x20;   {

&#x20;       "role": "user",

&#x20;       "content": \[

&#x20;           {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN\_!!6000000002727-0-tps-1024-406.jpg"},

&#x20;           {"text": "How do I solve this problem?"}

&#x20;       ]

&#x20;   }

]



response = MultiModalConversation.call(

&#x20;   # If the environment variable is not set, provide your Model Studio API Key here: api\_key="sk-xxx",

&#x20;   # Each region requires a unique API Key. To get an API Key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   model="qwen3.5-plus",  

&#x20;   messages=messages,

&#x20;   stream=True,

&#x20;   # `thinking mode` is toggleable for `qwen3.5`/`qwen3-vl-plus`/`qwen3-vl-flash`. It is mandatory for models with a 'thinking' suffix and does not apply to other Qwen-VL models.

&#x20;   enable\_thinking=enable\_thinking,

&#x20;   # The thinking\_budget parameter sets the maximum number of tokens for the reasoning process.

&#x20;   thinking\_budget=81920,



)



\# Stores the full reasoning process.

reasoning\_content = ""

\# Stores the full response.

answer\_content = ""

\# Tracks if the model is generating the final answer.

is\_answering = False



if enable\_thinking:

&#x20;   print("=" \* 20 + "Thinking Process" + "=" \* 20)



for chunk in response:

&#x20;   # Ignore empty chunks.

&#x20;   message = chunk.output.choices\[0].message

&#x20;   reasoning\_content\_chunk = message.get("reasoning\_content", None)

&#x20;   if (chunk.output.choices\[0].message.content == \[] and

&#x20;       reasoning\_content\_chunk == ""):

&#x20;       pass

&#x20;   else:

&#x20;       # In the reasoning process.

&#x20;       if reasoning\_content\_chunk is not None and chunk.output.choices\[0].message.content == \[]:

&#x20;           print(chunk.output.choices\[0].message.reasoning\_content, end="")

&#x20;           reasoning\_content += chunk.output.choices\[0].message.reasoning\_content

&#x20;       # Responding.

&#x20;       elif chunk.output.choices\[0].message.content != \[]:

&#x20;           if not is\_answering:

&#x20;               print("\\n" + "=" \* 20 + "Complete Response" + "=" \* 20)

&#x20;               is\_answering = True

&#x20;           print(chunk.output.choices\[0].message.content\[0]\["text"], end="")

&#x20;           answer\_content += chunk.output.choices\[0].message.content\[0]\["text"]



\# To print the complete reasoning process and the complete response, uncomment and run the following code.

\# print("=" \* 20 + "Complete Thinking Process" + "=" \* 20 + "\\n")

\# print(f"{reasoning\_content}")

\# print("=" \* 20 + "Complete Response" + "=" \* 20 + "\\n")

\# print(f"{answer\_content}")

```



Java



```

// DashScope SDK version >= 2.21.10

import java.util.\*;



import org.slf4j.Logger;

import org.slf4j.LoggerFactory;



import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import io.reactivex.Flowable;



import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.exception.InputRequiredException;

import java.lang.System;

import com.alibaba.dashscope.utils.Constants;



public class Main {

&#x20;   // Endpoints vary by region. Set the endpoint for your region.

&#x20;   static {Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";}



&#x20;   private static final Logger logger = LoggerFactory.getLogger(Main.class);

&#x20;   private static StringBuilder reasoningContent = new StringBuilder();

&#x20;   private static StringBuilder finalContent = new StringBuilder();

&#x20;   private static boolean isFirstPrint = true;



&#x20;   private static void handleGenerationResult(MultiModalConversationResult message) {

&#x20;       String re = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();

&#x20;       String reasoning = Objects.isNull(re)?"":re; // Default to an empty string if reasoning content is null.



&#x20;       List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();

&#x20;       if (!reasoning.isEmpty()) {

&#x20;           reasoningContent.append(reasoning);

&#x20;           if (isFirstPrint) {

&#x20;               System.out.println("====================Thinking Process====================");

&#x20;               isFirstPrint = false;

&#x20;           }

&#x20;           System.out.print(reasoning);

&#x20;       }



&#x20;       if (Objects.nonNull(content) \&\& !content.isEmpty()) {

&#x20;           Object text = content.get(0).get("text");

&#x20;           finalContent.append(content.get(0).get("text"));

&#x20;           if (!isFirstPrint) {

&#x20;               System.out.println("\\n====================Complete Response====================");

&#x20;               isFirstPrint = true;

&#x20;           }

&#x20;           System.out.print(text);

&#x20;       }

&#x20;   }

&#x20;   public static MultiModalConversationParam buildMultiModalConversationParam(MultiModalMessage Msg)  {

&#x20;       return MultiModalConversationParam.builder()

&#x20;               // If the environment variable is not set, provide your Model Studio API Key here: .apiKey("sk-xxx")

&#x20;               // Each region requires a unique API Key. To get an API Key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen3.5-plus")

&#x20;               .messages(Arrays.asList(Msg))

&#x20;               .enableThinking(true)

&#x20;               .thinkingBudget(81920)

&#x20;               .incrementalOutput(true)

&#x20;               .build();

&#x20;   }



&#x20;   public static void streamCallWithMessage(MultiModalConversation conv, MultiModalMessage Msg)

&#x20;           throws NoApiKeyException, ApiException, InputRequiredException, UploadFileException {

&#x20;       MultiModalConversationParam param = buildMultiModalConversationParam(Msg);

&#x20;       Flowable<MultiModalConversationResult> result = conv.streamCall(param);

&#x20;       result.blockingForEach(message -> {

&#x20;           handleGenerationResult(message);

&#x20;       });

&#x20;   }

&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           MultiModalConversation conv = new MultiModalConversation();

&#x20;           MultiModalMessage userMsg = MultiModalMessage.builder()

&#x20;                   .role(Role.USER.getValue())

&#x20;                   .content(Arrays.asList(Collections.singletonMap("image", "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN\_!!6000000002727-0-tps-1024-406.jpg"),

&#x20;                           Collections.singletonMap("text", "How do I solve this problem?")))

&#x20;                   .build();

&#x20;           streamCallWithMessage(conv, userMsg);

//             Print the final result.

//            if (reasoningContent.length() > 0) {

//                System.out.println("\\n====================Complete Response====================");

//                System.out.println(finalContent.toString());

//            }

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException | InputRequiredException e) {

&#x20;           logger.error("An exception occurred: {}", e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



curl



```

\# ======= Important =======

\# Each region requires a unique API Key. To get an API Key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by region. Set the endpoint for your region.

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-H 'X-DashScope-SSE: enable' \\

\-d '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "input":{

&#x20;       "messages":\[

&#x20;           {

&#x20;               "role": "user",

&#x20;               "content": \[

&#x20;                   {"image": "https://img.alicdn.com/imgextra/i1/O1CN01gDEY8M1W114Hi3XcN\_!!6000000002727-0-tps-1024-406.jpg"},

&#x20;                   {"text": "How do I solve this problem?"}

&#x20;               ]

&#x20;           }

&#x20;       ]

&#x20;   },

&#x20;   "parameters":{

&#x20;       "enable\_thinking": true,

&#x20;       "incremental\_output": true,

&#x20;       "thinking\_budget": 81920

&#x20;   }

}'

```



\### \*\*Multiple\*\* image input



Visual understanding models let you pass multiple images in a single request for tasks like \*\*product comparison and multi-page document processing\*\*. To do so, include multiple image objects in the`content` array of `user message`.



\*\*Important\*\*



The model's token limit restricts the number of images you can include. The combined token count for all images and text must not exceed this limit.



\## OpenAI compatible



\## Python



```

import os

from openai import OpenAI



client = OpenAI(

&#x20;   # Each Region requires a separate API key. For instructions, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   # Endpoints vary by Region. Modify the URL for your Region.

&#x20;   base\_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",

)



completion = client.chat.completions.create(

&#x20;   model="qwen3.5-plus",  #  This example uses qwen3.5-plus. For other models, see the Model List: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   messages=\[

&#x20;       {"role": "user","content": \[

&#x20;           {"type": "image\_url","image\_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"},},

&#x20;           {"type": "image\_url","image\_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},},

&#x20;           {"type": "text", "text": "What do these images depict?"},

&#x20;           ],

&#x20;       }

&#x20;   ],

)



print(completion.choices\[0].message.content)

```



\### \*\*Response\*\*



```

Image 1 shows a woman and a Labrador retriever on a beach. The woman, in a plaid shirt, is sitting on the sand and shaking the dog's paw. The background of ocean waves and sky creates a warm, pleasant atmosphere.



Image 2 shows a tiger walking through a forest. Its coat is orange with black stripes. The surroundings are dense with trees and vegetation, and the ground is covered with fallen leaves. The scene evokes a sense of the wild.

```



\## Node.js



```

import OpenAI from "openai";



const openai = new OpenAI(

&#x20;   {

&#x20;       // Each Region requires a separate API key. For instructions, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;       // If the environment variable is not set, replace the following line with your API key: apiKey: "sk-xxx"

&#x20;       apiKey: process.env.DASHSCOPE\_API\_KEY,

&#x20;       // Endpoints vary by Region. Modify the URL for your Region.

&#x20;       baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

&#x20;   }

);



async function main() {

&#x20;   const response = await openai.chat.completions.create({

&#x20;       model: "qwen3.5-plus",  // This example uses qwen3.5-plus. For other models, see the Model List: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;       messages: \[

&#x20;         {role: "user",content: \[

&#x20;           {type: "image\_url",image\_url: {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"}},

&#x20;           {type: "image\_url",image\_url: {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"}},

&#x20;           {type: "text", text: "What do these images depict?" },

&#x20;       ]}]

&#x20;   });

&#x20;   console.log(response.choices\[0].message.content);

}



main()

```



\### \*\*Response\*\*



```

The first image shows a person and a dog on a beach. The person is wearing a plaid shirt, and the dog has a collar. They appear to be shaking hands or giving a high-five.



The second image shows a tiger walking in a forest. The tiger's coat is orange with black stripes, and the background is filled with green trees and vegetation.

```



\## curl



```

\# ======= Important =======

\# Each Region requires a separate API key. For instructions, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by Region. Modify the URL for your Region.

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20; "model": "qwen3.5-plus",

&#x20; "messages": \[

&#x20;   {

&#x20;     "role": "user",

&#x20;     "content": \[

&#x20;       {

&#x20;         "type": "image\_url",

&#x20;         "image\_url": {

&#x20;           "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"

&#x20;         }

&#x20;       },

&#x20;       {

&#x20;         "type": "image\_url",

&#x20;         "image\_url": {

&#x20;           "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"

&#x20;         }

&#x20;       },

&#x20;       {

&#x20;         "type": "text",

&#x20;         "text": "What do these images depict?"

&#x20;       }

&#x20;     ]

&#x20;   }

&#x20; ]

}'

```



\### \*\*Response\*\*



```

{

&#x20; "choices": \[

&#x20;   {

&#x20;     "message": {

&#x20;       "content": "Image 1 shows a woman and a Labrador retriever interacting on a beach. The woman is wearing a plaid shirt and sitting on the sand, shaking the dog's paw. The background features the ocean and a sunset sky, creating a very warm and harmonious atmosphere.\\n\\nImage 2 shows a tiger walking in a forest. The tiger's coat is orange with black stripes as it walks forward. The surroundings are dense with trees and vegetation, with fallen leaves on the ground. The scene conveys a sense of wildness and vitality.",

&#x20;       "role": "assistant"

&#x20;     },

&#x20;     "finish\_reason": "stop",

&#x20;     "index": 0,

&#x20;     "logprobs": null

&#x20;   }

&#x20; ],

&#x20; "object": "chat.completion",

&#x20; "usage": {

&#x20;   "prompt\_tokens": 2497,

&#x20;   "completion\_tokens": 109,

&#x20;   "total\_tokens": 2606

&#x20; },

&#x20; "created": 1725948561,

&#x20; "system\_fingerprint": null,

&#x20; "model": "qwen3.5-plus",

&#x20; "id": "chatcmpl-0fd66f46-b09e-9164-a84f-3ebbbedbac15"

}

```



\## DashScope



\## Python



```

import os

import dashscope



\# Endpoints vary by Region. Modify the URL for your Region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



messages = \[

&#x20;   {

&#x20;       "role": "user",

&#x20;       "content": \[

&#x20;           {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"},

&#x20;           {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},

&#x20;           {"text": "What do these images depict?"}

&#x20;       ]

&#x20;   }

]



response = dashscope.MultiModalConversation.call(

&#x20;   # Each Region requires a separate API key. For instructions, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If the environment variable is not set, replace the following line with your API key: api\_key="sk-xxx"

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   model='qwen3.5-plus', #  This example uses qwen3.5-plus. For other models, see the Model List: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   messages=messages

)



print(response.output.choices\[0].message.content\[0]\["text"])

```



\### \*\*Response\*\*



```

The images show animals in natural scenes. The first image is of a person and a dog on a beach, and the second is of a tiger in a forest.

```



\## Java



```

import java.util.Arrays;

import java.util.Collections;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {

&#x20;   static {

&#x20;   // Endpoints vary by Region. Modify the URL for your Region.

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }

&#x20;   public static void simpleMultiModalConversationCall()

&#x20;           throws ApiException, NoApiKeyException, UploadFileException {

&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(

&#x20;                       Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"),

&#x20;                       Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"),

&#x20;                       Collections.singletonMap("text", "What do these images depict?"))).build();

&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // Each Region requires a separate API key. For instructions, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen3.5-plus")  //  This example uses qwen3.5-plus. For other models, see the Model List: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;               .messages(Arrays.asList(userMessage))

&#x20;               .build();

&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));    }

&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           simpleMultiModalConversationCall();

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\### \*\*Response\*\*



```

These images show animals in natural scenes.



1\.  First image: A woman and a dog are on a beach. The woman, in a plaid shirt, is sitting on the sand as the dog, which wears a collar, extends its paw to shake hands.

2\.  Second image: A tiger walks through a forest. Its coat is orange with black stripes, and the background consists of trees and leaves.

```



\## curl



```

\# ======= Important =======

\# Each Region requires a separate API key. For instructions, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by Region. Modify the URL for your Region.

\# === Remove this comment before execution ===



curl --location 'https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \\

\--header "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\--header 'Content-Type: application/json' \\

\--data '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "input":{

&#x20;       "messages":\[

&#x20;           {

&#x20;               "role": "user",

&#x20;               "content": \[

&#x20;                   {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog\_and\_girl.jpeg"},

&#x20;                   {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},

&#x20;                   {"text": "What do these images depict?"}

&#x20;               ]

&#x20;           }

&#x20;       ]

&#x20;   }

}'

```



\### \*\*Response\*\*



```

{

&#x20; "output": {

&#x20;   "choices": \[

&#x20;     {

&#x20;       "finish\_reason": "stop",

&#x20;       "message": {

&#x20;         "role": "assistant",

&#x20;         "content": \[

&#x20;           {

&#x20;             "text": "The images show animals in natural scenes. The first image is of a person and a dog on a beach, and the second is of a tiger in a forest."

&#x20;           }

&#x20;         ]

&#x20;       }

&#x20;     }

&#x20;   ]

&#x20; },

&#x20; "usage": {

&#x20;   "output\_tokens": 81,

&#x20;   "input\_tokens": 1277,

&#x20;   "image\_tokens": 2497

&#x20; },

&#x20; "request\_id": "ccf845a3-dc33-9cda-b581-20fe7dc23f70"

}

```



\### \*\*Video understanding\*\*



The visual understanding model analyzes video content from either a video file or an image list (video frames). The following examples show how to analyze an online video or an image list specified by a URL. For limitations on videos or the number of images in an image list, see the \[Video limits](#190c9e0005dlq) section.



> For optimal performance, use the latest version or a recent Snapshot of the model to analyze video files.



\## Video file



The visual understanding model performs content analysis by extracting a sequence of video frames. You can control the frame extraction policy with the following two parameters:



\-   \*\*fps\*\*: Controls the frame extraction frequency, extracting a frame every fps1​ seconds. The valid value range is \\\[0.1, 10\\], and the default value is 2.0.

&#x20;   

&#x20;   -   For high-speed motion scenes, set a higher fps value to capture more details.

&#x20;       

&#x20;   -   For static or long videos, consider setting a lower fps value to improve processing efficiency.

&#x20;       

\-   \*\*max\\\_frames\*\*: The maximum number of frames to extract from the video. If the number of frames calculated based on the fps value exceeds this limit, the system samples frames evenly to stay within the max\\\_frames limit. \*\*This parameter is available only with the DashScope SDK.\*\*

&#x20;   



\## OpenAI compatible



> When you provide a video file directly to the visual understanding model using the OpenAI SDK or an HTTP request, set the `"type"` parameter in the user message to `"video\_url"`.



\## Python



```

import os

from openai import OpenAI



client = OpenAI(

&#x20;   # An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx",

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   # Endpoints vary by region. Modify the endpoint based on your region.

&#x20;   base\_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",

)

completion = client.chat.completions.create(

&#x20;   model="qwen3.5-plus",

&#x20;   messages=\[

&#x20;       {

&#x20;           "role": "user",

&#x20;           "content": \[

&#x20;               # When you provide a video file directly, set the type to video\_url.

&#x20;               {

&#x20;                   "type": "video\_url",

&#x20;                   "video\_url": {

&#x20;                       "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"

&#x20;                   },

&#x20;                   "fps": 2

&#x20;               },

&#x20;               {

&#x20;                   "type": "text",

&#x20;                   "text": "What is the content of this video?"

&#x20;               }

&#x20;           ]

&#x20;       }

&#x20;   ]

)



print(completion.choices\[0].message.content)

```



\## Node.js



```

import OpenAI from "openai";



const openai = new OpenAI(

&#x20;   {

&#x20;       // An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;       // If you have not configured an environment variable, replace the following line with your Model Studio API key: apiKey: "sk-xxx"

&#x20;       apiKey: process.env.DASHSCOPE\_API\_KEY,

&#x20;       // Endpoints vary by region. Modify the endpoint based on your region.

&#x20;       baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

&#x20;   }

);



async function main() {

&#x20;   const response = await openai.chat.completions.create({

&#x20;       model: "qwen3.5-plus",

&#x20;       messages: \[

&#x20;           {

&#x20;               role: "user",

&#x20;               content: \[

&#x20;                   // When you provide a video file directly, set the type to video\_url.

&#x20;                   {

&#x20;                       type: "video\_url",

&#x20;                       video\_url: {

&#x20;                           "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"

&#x20;                       },

&#x20;                       "fps": 2

&#x20;                   },

&#x20;                   {

&#x20;                       type: "text",

&#x20;                       "text": "What is the content of this video?"

&#x20;                   }

&#x20;               ]

&#x20;           }

&#x20;       ]

&#x20;   });



&#x20;   console.log(response.choices\[0].message.content);

}



main();

```



\## curl



```

\# ======= Important =======

\# An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by region. Modify the endpoint based on your region.

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions \\

&#x20; -H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

&#x20; -H 'Content-Type: application/json' \\

&#x20; -d '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "messages": \[

&#x20;     {

&#x20;       "role": "user",

&#x20;       "content": \[

&#x20;         {

&#x20;           "type": "video\_url",

&#x20;           "video\_url": {

&#x20;             "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"

&#x20;           },

&#x20;           "fps":2

&#x20;         },

&#x20;         {

&#x20;           "type": "text",

&#x20;           "text": "What is the content of this video?"

&#x20;         }

&#x20;       ]

&#x20;     }

&#x20;   ]

&#x20; }'

```



\## DashScope



\## Python



```

import dashscope

import os



\# Endpoints vary by region. Modify the endpoint based on your region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

messages = \[

&#x20;   {"role": "user",

&#x20;       "content": \[

&#x20;           # The fps parameter controls the frame rate. One frame is extracted every 1/fps seconds. For more information, see: https://www.alibabacloud.com/help/en/model-studio/use-qwen-by-calling-api?#2ed5ee7377fum

&#x20;           {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},

&#x20;           {"text": "What is the content of this video?"}

&#x20;       ]

&#x20;   }

]



response = dashscope.MultiModalConversation.call(

&#x20;   # An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key ="sk-xxx"

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   model='qwen3.5-plus',

&#x20;   messages=messages

)



print(response.output.choices\[0].message.content\[0]\["text"])

```



\## Java



```

import java.util.Arrays;

import java.util.Collections;

import java.util.HashMap;

import java.util.Map;



import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {

&#x20;  static {

&#x20;           // Endpoints vary by region. Modify the endpoint based on your region.

&#x20;           Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;       }

&#x20;   public static void simpleMultiModalConversationCall()

&#x20;           throws ApiException, NoApiKeyException, UploadFileException {

&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       // The fps parameter controls the frame rate. One frame is extracted every 1/fps seconds. For more information, see: https://www.alibabacloud.com/help/en/model-studio/use-qwen-by-calling-api?#2ed5ee7377fum

&#x20;       Map<String, Object> params = new HashMap<>();

&#x20;       params.put("video", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4");

&#x20;       params.put("fps", 2);

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(

&#x20;                       params,

&#x20;                       Collections.singletonMap("text", "What is the content of this video?"))).build();

&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // If you use a model in the China (Beijing) region, you must use an API key from that region. Get an API key at: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               // If you have not configured an environment variable, replace the following line with your Model Studio API key: .apiKey("sk-xxx")

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen3.5-plus")

&#x20;               .messages(Arrays.asList(userMessage))

&#x20;               .build();

&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));

&#x20;   }

&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           simpleMultiModalConversationCall();

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\## curl



```

\# ======= Important =======

\# An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by region. Modify the endpoint based on your region.

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "input":{

&#x20;       "messages":\[

&#x20;           {"role": "user","content": \[{"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},

&#x20;           {"text": "What is the content of this video?"}]}]}

}'

```



\## Image list



When a video is provided as an image list of pre-extracted video frames, the `fps` parameter informs the model of the time interval between frames. This helps the model more accurately understand the sequence, duration, and dynamic changes of an event. The model supports using the `fps` parameter to specify the frame extraction rate of the original video. This means that a video frame is extracted from the original video every fps1​ seconds. This parameter is supported by  \*\*Qwen3.5\*\*, \*\*Qwen3-VL, and Qwen2.5-VL\*\* models.



\## OpenAI compatible



> When you provide a video as an image list using the OpenAI SDK or an HTTP request, set the `"type"` parameter in the user message to `"video"`.



\## Python



```

import os

from openai import OpenAI



client = OpenAI(

&#x20;   # An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx",

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   # Endpoints vary by region. Modify the endpoint based on your region.

&#x20;   base\_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",

)



completion = client.chat.completions.create(

&#x20;   model="qwen3.5-plus", # This example uses the qwen3.5-plus model. You can replace the model name as needed. For a list of available models, see the Model List: https://www.alibabacloud.com/help/en/model-studio/models

&#x20;   messages=\[{"role": "user","content": \[

&#x20;       # When you provide an image list, the 'type' parameter in the user message is 'video'.

&#x20;        {"type": "video","video": \[

&#x20;        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",

&#x20;        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",

&#x20;        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",

&#x20;        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],

&#x20;        "fps":2},

&#x20;        {"type": "text","text": "Describe the process shown in this video."},

&#x20;   ]}]

)



print(completion.choices\[0].message.content)

```



\## Node.js



```

// Make sure you have specified "type": "module" in package.json.

import OpenAI from "openai";



const openai = new OpenAI({

&#x20;   // An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   // If you have not configured an environment variable, replace the following line with your Model Studio API key: apiKey: "sk-xxx",

&#x20;   apiKey: process.env.DASHSCOPE\_API\_KEY,

&#x20;   // Endpoints vary by region. Modify the endpoint based on your region.

&#x20;   baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

});



async function main() {

&#x20;   const response = await openai.chat.completions.create({

&#x20;       model: "qwen3.5-plus",  // This example uses the qwen3.5-plus model. You can replace the model name as needed. For a list of available models, see the Model List: https://www.alibabacloud.com/help/en/model-studio/models

&#x20;       messages: \[{

&#x20;           role: "user",

&#x20;           content: \[

&#x20;               {

&#x20;                   // When you provide an image list, the 'type' parameter in the user message is 'video'.

&#x20;                   type: "video",

&#x20;                   video: \[

&#x20;                       "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",

&#x20;                       "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",

&#x20;                       "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",

&#x20;                       "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],

&#x20;                       "fps": 2

&#x20;               },

&#x20;               {

&#x20;                   type: "text",

&#x20;                   text: "Describe the process shown in this video."

&#x20;               }

&#x20;           ]

&#x20;       }]

&#x20;   });

&#x20;   console.log(response.choices\[0].message.content);

}



main();

```



\## curl



```

\# ======= Important =======

\# An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by region. Modify the endpoint based on your region.

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "messages": \[{"role": "user","content": \[{"type": "video","video": \[

&#x20;                 "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",

&#x20;                 "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",

&#x20;                 "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",

&#x20;                 "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],

&#x20;                 "fps":2},

&#x20;               {"type": "text","text": "Describe the process shown in this video."}]}]

}'

```



\## DashScope



\## Python



```

import os

import dashscope



\# Endpoints vary by region. Modify the endpoint based on your region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'

messages = \[{"role": "user",

&#x20;            "content": \[

&#x20;                 # When you provide an image list, the fps parameter is available for the Qwen3.5, Qwen3-VL, and Qwen2.5-VL models.

&#x20;                {"video":\["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",

&#x20;                          "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",

&#x20;                          "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",

&#x20;                          "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],

&#x20;                  "fps":2},

&#x20;                {"text": "Describe the process shown in this video."}]}]

response = dashscope.MultiModalConversation.call(

&#x20;   # An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx",

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   model='qwen3.5-plus',  # This example uses the qwen3.5-plus model. You can replace the model name as needed. For a list of available models, see the Model List: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   messages=messages

)

print(response.output.choices\[0].message.content\[0]\["text"])

```



\## Java



```

// DashScope SDK version 2.21.10 or later is required.

import java.util.Arrays;

import java.util.Collections;

import java.util.Map;

import java.util.HashMap;



import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {

&#x20;   static {

&#x20;       // Endpoints vary by region. Modify the endpoint based on your region.

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }

&#x20;   private static final String MODEL\_NAME = "qwen3.5-plus";  // This example uses the qwen3.5-plus model. You can replace the model name as needed. For a list of available models, see the Model List: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   public static void videoImageListSample() throws ApiException, NoApiKeyException, UploadFileException {

&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       // When you provide an image list, the fps parameter is available for the Qwen3.5, Qwen3-VL, and Qwen2.5-VL models.

&#x20;       Map<String, Object> params = new HashMap<>();

&#x20;       params.put("video", Arrays.asList("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",

&#x20;                       "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",

&#x20;                       "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",

&#x20;                       "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"));

&#x20;       params.put("fps", 2);

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder()

&#x20;               .role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(

&#x20;                       params,

&#x20;                       Collections.singletonMap("text", "Describe the process shown in this video.")))

&#x20;               .build();

&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               // If you have not configured an environment variable, replace the following line with your Model Studio API key: .apiKey("sk-xxx")

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model(MODEL\_NAME)

&#x20;               .messages(Arrays.asList(userMessage)).build();

&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));

&#x20;   }

&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           videoImageListSample();

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\## curl



```

\# ======= Important =======

\# An API key is required for each region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by region. Modify the endpoint based on your region.

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20; "model": "qwen3.5-plus",

&#x20; "input": {

&#x20;   "messages": \[

&#x20;     {

&#x20;       "role": "user",

&#x20;       "content": \[

&#x20;         {

&#x20;           "video": \[

&#x20;             "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",

&#x20;             "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",

&#x20;             "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",

&#x20;             "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"

&#x20;           ],

&#x20;           "fps":2

&#x20;                

&#x20;         },

&#x20;         {

&#x20;           "text": "Describe the process shown in this video."

&#x20;         }

&#x20;       ]

&#x20;     }

&#x20;   ]

&#x20; }

}'

```



\### \*\*Pass\*\* a local file (base64 or file \*\*path)\*\*



Visual understanding models offer two methods for uploading local files: Base64 encoding and file path upload. Choose a method based on the file size and SDK type. For specific recommendations, see \[How to choose a file upload method](#dc4e7260aauuo). Both methods must meet the requirements in \[Image limits](#71c2cb6e09ioo).



\## Base64 encoding



Convert the file to a Base64-encoded string and pass it to the model. This method is compatible with the OpenAI and DashScope SDKs, as well as HTTP requests.



\*\*Steps to pass a Base64-encoded string (using an image as an example)\*\*



1\.  \*\*Encode the file\*\*. Convert the local image to a Base64-encoded string.

&#x20;   

&#x20;   \*\*Example code for converting an image to Base64 encoding\*\*

&#x20;   

&#x20;   ```

&#x20;   # Converts a local file to a Base64-encoded string.

&#x20;   import base64

&#x20;   def encode\_image(image\_path):

&#x20;       with open(image\_path, "rb") as image\_file:

&#x20;           return base64.b64encode(image\_file.read()).decode("utf-8")

&#x20;   

&#x20;   # Replace "xxx/eagle.png" with the absolute path of your local image.

&#x20;   base64\_image = encode\_image("xxx/eagle.png")

&#x20;   ```

&#x20;   

2\.  Build a \[data URL](https://www.rfc-editor.org/rfc/rfc2397). Use the following format: `data:\[MIME\_type];base64,{base64\_image}`.

&#x20;   

&#x20;   1.  Replace `MIME\_type` with the actual media type. The value must match an entry in the `MIME Type` column of the \[Supported image formats](#d6b42862bb1ct) table, such as `image/jpeg` or `image/png`.

&#x20;       

&#x20;   2.  `base64\_image` is the Base64-encoded string from the previous step.

&#x20;       

3\.  Call the model by passing the `data URL` to the `image` or `image\_url` parameter.

&#x20;   



\## File path



Pass the local file path directly to the model. This method is supported only by the DashScope Python and Java SDKs. It is not compatible with DashScope HTTP or OpenAI-compatible requests.



Use the following table to specify the file path based on your programming language and operating system.



\*\*Specify the file path (using an image as an example)\*\*



| \*\*System\*\* | \*\*SDK\*\* | \*\*File path\*\* | \*\*Example\*\* |

| --- | --- | --- | --- |

| Linux or macOS | Python SDK | file://{absolute path} | file:///home/images/test.png |

| Java SDK |

| Windows | Python SDK | file://{absolute path} | file://D:/images/test.png |

| Java SDK | file:///{absolute path} | file:///D:/images/test.png |



\## Image



\## File path



\## Python



```

import os

import dashscope



\# Endpoints vary by Region. Modify the endpoint for your Region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



\# Replace xxx/eagle.png with the absolute path of your local image.

local\_path = "xxx/eagle.png"

image\_path = f"file://{local\_path}"

messages = \[

&#x20;               {'role':'user',

&#x20;               'content': \[{'image': image\_path},

&#x20;                           {'text': 'What is depicted in the image?'}]}]

response = dashscope.MultiModalConversation.call(

&#x20;   # If you have not configured an environment variable, you can pass your API key directly by replacing

&#x20;   # the following line with: api\_key="sk-xxx"

&#x20;   # An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   model='qwen-vl-plus',  # This example uses the qwen-vl-plus model. You can replace it as needed. For a list of available models, see: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   messages=messages)

print(response.output.choices\[0].message.content\[0]\["text"])

```



\## Java



```

import java.util.Arrays;

import java.util.Collections;

import java.util.HashMap;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {



&#x20;   static {

&#x20;       // Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }

&#x20;   

&#x20;   public static void callWithLocalFile(String localPath)

&#x20;           throws ApiException, NoApiKeyException, UploadFileException {

&#x20;       String filePath = "file://"+localPath;

&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(new HashMap<String, Object>(){{put("image", filePath);}},

&#x20;                       new HashMap<String, Object>(){{put("text", "What is depicted in the image?");}})).build();

&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // If you have not configured an environment variable, you can pass your API key directly by replacing

&#x20;               // the following line with: .apiKey("sk-xxx")

&#x20;               // An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen-vl-plus")  // This example uses the qwen-vl-plus model. You can replace it as needed. For a list of available models, see: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;               .messages(Arrays.asList(userMessage))

&#x20;               .build();

&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));}



&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           // Replace xxx/eagle.png with the absolute path of your local image.

&#x20;           callWithLocalFile("xxx/eagle.png");

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\## Base64 encoding



\## OpenAI compatible



\## Python



```

from openai import OpenAI

import os

import base64





\# This function converts a local file to a Base64-encoded string.

def encode\_image(image\_path):

&#x20;   with open(image\_path, "rb") as image\_file:

&#x20;       return base64.b64encode(image\_file.read()).decode("utf-8")



\# Replace xxx/eagle.png with the absolute path of your local image.

base64\_image = encode\_image("xxx/eagle.png")

client = OpenAI(

&#x20;   # If you have not configured an environment variable, you can pass your API key directly by replacing

&#x20;   # the following line with: api\_key="sk-xxx"

&#x20;   # An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   # Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;   base\_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",

)

completion = client.chat.completions.create(

&#x20;   model="qwen-vl-plus", # This example uses the qwen-vl-plus model. You can replace it as needed. For a list of available models, see: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   messages=\[

&#x20;       {

&#x20;           "role": "user",

&#x20;           "content": \[

&#x20;               {

&#x20;                   "type": "image\_url",

&#x20;                   # Note: When passing Base64-encoded data, ensure the data URI format (for example, data:image/png;base64)

&#x20;                   # matches the actual image format.

&#x20;                   # PNG Image:  f"data:image/png;base64,{base64\_image}"

&#x20;                   # JPEG Image: f"data:image/jpeg;base64,{base64\_image}"

&#x20;                   # WEBP Image: f"data:image/webp;base64,{base64\_image}"

&#x20;                   "image\_url": {"url": f"data:image/png;base64,{base64\_image}"},

&#x20;               },

&#x20;               {"type": "text", "text": "What is depicted in the image?"},

&#x20;           ],

&#x20;       }

&#x20;   ],

)

print(completion.choices\[0].message.content)

```



\## Node.js



```

import OpenAI from "openai";

import { readFileSync } from 'fs';





const openai = new OpenAI(

&#x20;   {

&#x20;       // If you have not configured an environment variable, you can pass your API key directly by replacing

&#x20;       // the following line with: apiKey: "sk-xxx"

&#x20;       // An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;       apiKey: process.env.DASHSCOPE\_API\_KEY,

&#x20;       // Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;       baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

&#x20;   }

);



const encodeImage = (imagePath) => {

&#x20;   const imageFile = readFileSync(imagePath);

&#x20;   return imageFile.toString('base64');

&#x20; };

// Replace xxx/eagle.png with the absolute path of your local image.

const base64Image = encodeImage("xxx/eagle.png")

async function main() {

&#x20;   const completion = await openai.chat.completions.create({

&#x20;       model: "qwen-vl-plus",  // This example uses the qwen-vl-plus model. You can replace it as needed. For a list of available models, see: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;       messages: \[

&#x20;           {"role": "user",

&#x20;           "content": \[{"type": "image\_url",

&#x20;                          // Note: When passing Base64-encoded data, ensure the data URI format (for example, data:image/png;base64)

&#x20;                          // matches the actual image format.

&#x20;                          // PNG Image:  `data:image/png;base64,${base64Image}`

&#x20;                          // JPEG Image: `data:image/jpeg;base64,${base64Image}`

&#x20;                          // WEBP Image: `data:image/webp;base64,${base64Image}`

&#x20;                          "image\_url": {"url": `data:image/png;base64,${base64Image}`},},

&#x20;                       {"type": "text", "text": "What is depicted in the image?"}]}]

&#x20;   });

&#x20;   console.log(completion.choices\[0].message.content);

} 



main();

```



\## curl



\-   For an example of converting a file to a Base64-encoded string, see the \[example code](#7aee9382dfqpk).

&#x20;   

\-   For display purposes, the Base64-encoded string `"data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` in the code is truncated. You must pass the complete encoded string in your request.

&#x20;   



```

\# ======= Important =======

\# An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by Region. Modify the endpoint for your Region.

\# === Remove this comment before execution ===



curl --location 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions' \\

\--header "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\--header 'Content-Type: application/json' \\

\--data '{

&#x20; "model": "qwen-vl-plus",

&#x20; "messages": \[

&#x20; {

&#x20;   "role": "user",

&#x20;   "content": \[

&#x20;     {"type": "image\_url", "image\_url": {"url": "data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"}},

&#x20;     {"type": "text", "text": "What is depicted in the image?"}

&#x20;   ]

&#x20; }]

}'

```



\## DashScope



\## Python



```

import base64

import os

import dashscope



\# Endpoints vary by Region. Modify the endpoint for your Region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



\# This function converts a local file to a Base64-encoded string.

def encode\_image(image\_path):

&#x20;   with open(image\_path, "rb") as image\_file:

&#x20;       return base64.b64encode(image\_file.read()).decode("utf-8")





\# Replace xxx/eagle.png with the absolute path of your local image.

base64\_image = encode\_image("xxx/eagle.png")



messages = \[

&#x20;   {

&#x20;       "role": "user",

&#x20;       "content": \[

&#x20;           # Note: When passing Base64-encoded data, ensure the data URI format (for example, data:image/png;base64)

&#x20;           # matches the actual image format.

&#x20;           # PNG Image:  f"data:image/png;base64,{base64\_image}"

&#x20;           # JPEG Image: f"data:image/jpeg;base64,{base64\_image}"

&#x20;           # WEBP Image: f"data:image/webp;base64,{base64\_image}"

&#x20;           {"image": f"data:image/png;base64,{base64\_image}"},

&#x20;           {"text": "What is depicted in the image?"},

&#x20;       ],

&#x20;   },

]



response = dashscope.MultiModalConversation.call(

&#x20;   # If you have not configured an environment variable, you can pass your API key directly by replacing

&#x20;   # the following line with: api\_key="sk-xxx"

&#x20;   # An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   model="qwen-vl-plus",  # This example uses the qwen-vl-plus model. You can replace it as needed. For a list of available models, see: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   messages=messages,

)

print(response.output.choices\[0].message.content\[0]\["text"])

```



\## Java



```

import java.io.IOException;

import java.util.Arrays;

import java.util.Collections;

import java.util.HashMap;

import java.util.Base64;

import java.nio.file.Files;

import java.nio.file.Path;

import java.nio.file.Paths;



import com.alibaba.dashscope.aigc.multimodalconversation.\*;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {



&#x20;   static {

&#x20;       // Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }



&#x20;   private static String encodeImageToBase64(String imagePath) throws IOException {

&#x20;       Path path = Paths.get(imagePath);

&#x20;       byte\[] imageBytes = Files.readAllBytes(path);

&#x20;       return Base64.getEncoder().encodeToString(imageBytes);

&#x20;   }



&#x20;   public static void callWithLocalFile(String localPath) throws ApiException, NoApiKeyException, UploadFileException, IOException {



&#x20;       String base64Image = encodeImageToBase64(localPath);



&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(

&#x20;                       new HashMap<String, Object>() {{ put("image", "data:image/png;base64," + base64Image); }},

&#x20;                       new HashMap<String, Object>() {{ put("text", "What is depicted in the image?"); }}

&#x20;               )).build();



&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // If you have not configured an environment variable, you can pass your API key directly by replacing

&#x20;               // the following line with: .apiKey("sk-xxx")

&#x20;               // An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen-vl-plus")

&#x20;               .messages(Arrays.asList(userMessage))

&#x20;               .build();



&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));

&#x20;   }



&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           // Replace xxx/eagle.png with the absolute path of your local image.

&#x20;           callWithLocalFile("xxx/eagle.png");

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\## curl



\-   For an example of converting a file to a Base64-encoded string, see the \[example code](#7aee9382dfqpk).

&#x20;   

\-   For display purposes, the Base64-encoded string `"data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` in the code is truncated. You must pass the complete encoded string in your request.

&#x20;   



```

\# ======= Important =======

\# An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by Region. Modify the endpoint for your Region.

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20;   "model": "qwen-vl-plus",

&#x20;   "input":{

&#x20;       "messages":\[

&#x20;           {

&#x20;            "role": "user",

&#x20;            "content": \[

&#x20;              {"image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},

&#x20;              {"text": "What is depicted in the image?"}

&#x20;               ]

&#x20;           }

&#x20;       ]

&#x20;   }

}'

```



\## Video file



This example uses the local file \[test.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/nvwkcj/test.mp4).



\## File path



\## Python



```

import os

import dashscope



\# Endpoints vary by Region. Modify the endpoint based on your Region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



\# Replace xxx/test.mp4 with the absolute path of your local video file.

local\_path = "xxx/test.mp4"

video\_path = f"file://{local\_path}"

messages = \[

&#x20;               {'role':'user',

&#x20;               # The fps parameter specifies the number of frames to extract per second.

&#x20;               'content': \[{'video': video\_path,"fps":2},

&#x20;                           {'text': 'What is depicted in this video?'}]}]

response = MultiModalConversation.call(

&#x20;   # An API key is required for each Region. Get your API key at: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx"

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   model='qwen3.5-plus',  

&#x20;   messages=messages)

print(response.output.choices\[0].message.content\[0]\["text"])

```



\## Java



```

import java.util.Arrays;

import java.util.Collections;

import java.util.HashMap;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {



&#x20;   static {

&#x20;       // Endpoints vary by Region. Modify the endpoint based on your Region.

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }

&#x20;   

&#x20;   public static void callWithLocalFile(String localPath)

&#x20;           throws ApiException, NoApiKeyException, UploadFileException {

&#x20;       String filePath = "file://"+localPath;

&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(new HashMap<String, Object>()

&#x20;                                      {{

&#x20;                                          put("video", filePath); // The fps parameter specifies the number of frames to extract per second.

&#x20;                                          put("fps", 2);

&#x20;                                      }}, 

&#x20;                       new HashMap<String, Object>(){{put("text", "What is depicted in this video?");}})).build();

&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // An API key is required for each Region. Get your API key at: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               // If you have not configured an environment variable, replace the following line with your Model Studio API key: .apiKey("sk-xxx")

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen3.5-plus")  

&#x20;               .messages(Arrays.asList(userMessage))

&#x20;               .build();

&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));}



&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           // Replace xxx/test.mp4 with the absolute path of your local video file.

&#x20;           callWithLocalFile("xxx/test.mp4");

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\## Base64 encoding



\## OpenAI compatible



\## Python



```

from openai import OpenAI

import os

import base64





\# Converts a local file to a Base64-encoded string.

def encode\_video(video\_path):

&#x20;   with open(video\_path, "rb") as video\_file:

&#x20;       return base64.b64encode(video\_file.read()).decode("utf-8")



\# Replace xxx/test.mp4 with the absolute path of your local video file.

base64\_video = encode\_video("xxx/test.mp4")

client = OpenAI(

&#x20;   # An API key is required for each Region. Get your API key at: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx"

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   # Endpoints vary by Region. Modify the endpoint based on your Region.

&#x20;   base\_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",

)

completion = client.chat.completions.create(

&#x20;   model="qwen3.5-plus",  

&#x20;   messages=\[

&#x20;       {

&#x20;           "role": "user",

&#x20;           "content": \[

&#x20;               {

&#x20;                   # Use "video\_url" as the type for Base64-encoded video data.

&#x20;                   "type": "video\_url",

&#x20;                   "video\_url": {"url": f"data:video/mp4;base64,{base64\_video}"},

&#x20;                   "fps":2

&#x20;               },

&#x20;               {"type": "text", "text": "What is depicted in this video?"},

&#x20;           ],

&#x20;       }

&#x20;   ],

)

print(completion.choices\[0].message.content)

```



\## Node.js



```

import OpenAI from "openai";

import { readFileSync } from 'fs';



const openai = new OpenAI(

&#x20;   {

&#x20;       // An API key is required for each Region. Get your API key at: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;       // If you have not configured an environment variable, replace the following line with your Model Studio API key: apiKey: "sk-xxx"

&#x20;       apiKey: process.env.DASHSCOPE\_API\_KEY,

&#x20;       // Endpoints vary by Region. Modify the endpoint based on your Region.

&#x20;       baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

&#x20;   }

);



const encodeVideo = (videoPath) => {

&#x20;   const videoFile = readFileSync(videoPath);

&#x20;   return videoFile.toString('base64');

&#x20; };

// Replace xxx/test.mp4 with the absolute path of your local video file.

const base64Video = encodeVideo("xxx/test.mp4")

async function main() {

&#x20;   const completion = await openai.chat.completions.create({

&#x20;       model: "qwen3.5-plus", 

&#x20;       messages: \[

&#x20;           {"role": "user",

&#x20;            "content": \[{

&#x20;                // Use "video\_url" as the type for Base64-encoded video data.

&#x20;               "type": "video\_url", 

&#x20;               "video\_url": {"url": `data:video/mp4;base64,${base64Video}`},

&#x20;               "fps":2},

&#x20;                {"type": "text", "text": "What is depicted in this video?"}]}]

&#x20;   });

&#x20;   console.log(completion.choices\[0].message.content);

}



main();

```



\## curl



\-   The \[Example code](#7aee9382dfqpk) shows how to convert a file to a Base64-encoded string.

&#x20;   

\-   The Base64-encoded string `"data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` in the code is truncated for display. You must use the complete string in your actual request.

&#x20;   



```

\# ======= Important =======

\# An API key is required for each Region. Get your API key at: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by Region. Modify the endpoint based on your Region.

\# === Remove this comment before you execute the code ===



curl --location 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions' \\

\--header "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\--header 'Content-Type: application/json' \\

\--data '{

&#x20; "model": "qwen3.5-plus",

&#x20; "messages": \[

&#x20; {

&#x20;   "role": "user",

&#x20;   "content": \[

&#x20;     {"type": "video\_url", "video\_url": {"url": "data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},"fps":2},

&#x20;     {"type": "text", "text": "What is depicted in this video?"}

&#x20;   ]

&#x20; }]

}'

```



\## DashScope



\## Python



```

import base64

import os

import dashscope



\# Endpoints vary by Region. Modify the endpoint based on your Region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



\# Converts a local file to a Base64-encoded string.

def encode\_video(video\_path):

&#x20;   with open(video\_path, "rb") as video\_file:

&#x20;       return base64.b64encode(video\_file.read()).decode("utf-8")



\# Replace xxx/test.mp4 with the absolute path of your local video file.

base64\_video = encode\_video("xxx/test.mp4")



messages = \[{'role':'user',

&#x20;               # The fps parameter specifies the number of frames to extract per second.

&#x20;            'content': \[{'video': f"data:video/mp4;base64,{base64\_video}","fps":2},

&#x20;                           {'text': 'What is depicted in this video?'}]}]

response = MultiModalConversation.call(

&#x20;   # An API key is required for each Region. Get your API key at: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx"

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   model='qwen3.5-plus',

&#x20;   messages=messages)



print(response.output.choices\[0].message.content\[0]\["text"])

```



\## Java



```

import java.io.IOException;

import java.util.\*;

import java.nio.file.Files;

import java.nio.file.Path;

import java.nio.file.Paths;



import com.alibaba.dashscope.aigc.multimodalconversation.\*;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {



&#x20;   static {

&#x20;       // Endpoints vary by Region. Modify the endpoint based on your Region.

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }

&#x20;   

&#x20;   private static String encodeVideoToBase64(String videoPath) throws IOException {

&#x20;       Path path = Paths.get(videoPath);

&#x20;       byte\[] videoBytes = Files.readAllBytes(path);

&#x20;       return Base64.getEncoder().encodeToString(videoBytes);

&#x20;   }



&#x20;   public static void callWithLocalFile(String localPath)

&#x20;           throws ApiException, NoApiKeyException, UploadFileException, IOException {



&#x20;       String base64Video = encodeVideoToBase64(localPath);



&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(new HashMap<String, Object>()

&#x20;                                      {{

&#x20;                                          put("video", "data:video/mp4;base64," + base64Video); // The fps parameter specifies the number of frames to extract per second.

&#x20;                                          put("fps", 2);

&#x20;                                      }},

&#x20;                       new HashMap<String, Object>(){{put("text", "What is depicted in this video?");}})).build();



&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // An API key is required for each Region. Get your API key at: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               // If you have not configured an environment variable, replace the following line with your Model Studio API key: .apiKey("sk-xxx")

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen3.5-plus")

&#x20;               .messages(Arrays.asList(userMessage))

&#x20;               .build();



&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));

&#x20;   }



&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           // Replace xxx/test.mp4 with the absolute path of your local video file.

&#x20;           callWithLocalFile("xxx/test.mp4");

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\## curl



\-   The \[Example code](#7aee9382dfqpk) shows how to convert a file to a Base64-encoded string.

&#x20;   

\-   The Base64-encoded string `"data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` in the code is truncated for display. You must use the complete string in your actual request.

&#x20;   



```

\# ======= Important =======

\# An API key is required for each Region. Get your API key at: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Endpoints vary by Region. Modify the endpoint based on your Region.

\# === Remove this comment before you execute the code ===



curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "input":{

&#x20;       "messages":\[

&#x20;           {

&#x20;            "role": "user",

&#x20;            "content": \[

&#x20;              {"video": "data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},

&#x20;              {"text": "What is depicted in this video?"}

&#x20;               ]

&#x20;           }

&#x20;       ]

&#x20;   }

}'

```



\## Image list



This example uses these local files: \[football1.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/spqrrx/football1.jpg), \[football2.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/vtnhyr/football2.jpg), \[football3.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/ykaoih/football3.jpg), and \[football4.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/vkuupi/football4.jpg).



\## File path



\## Python



```

import os

import dashscope



\# Endpoints vary by Region. Modify the endpoint for your Region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



local\_path1 = "football1.jpg"

local\_path2 = "football2.jpg"

local\_path3 = "football3.jpg"

local\_path4 = "football4.jpg"



image\_path1 = f"file://{local\_path1}"

image\_path2 = f"file://{local\_path2}"

image\_path3 = f"file://{local\_path3}"

image\_path4 = f"file://{local\_path4}"



messages = \[{'role':'user',

&#x20;             # The fps parameter is available for the Qwen3.5, Qwen3-VL, and Qwen2.5-VL series models when you provide an image list.

&#x20;            'content': \[{'video': \[image\_path1,image\_path2,image\_path3,image\_path4],"fps":2},

&#x20;                        {'text': 'Describe the process shown in this video.'}]}]

response = MultiModalConversation.call(

&#x20;   # An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx"

&#x20;   api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;   model='qwen3.5-plus',  # This example uses the qwen3.5-plus model. You can replace it as needed. For available models, see the Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   messages=messages)



print(response.output.choices\[0].message.content\[0]\["text"])

```



\## Java



```

// DashScope SDK version 2.21.10 or later is required.

import java.util.Arrays;

import java.util.Collections;

import java.util.HashMap;

import java.util.Map;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {



&#x20;   static {

&#x20;       // Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }

&#x20;   

&#x20;   private static final String MODEL\_NAME = "qwen3.5-plus";  // This example uses the qwen3.5-plus model. You can replace it as needed. For available models, see the Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   public static void videoImageListSample(String localPath1, String localPath2, String localPath3, String localPath4)

&#x20;           throws ApiException, NoApiKeyException, UploadFileException {

&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       String filePath1 = "file://" + localPath1;

&#x20;       String filePath2 = "file://" + localPath2;

&#x20;       String filePath3 = "file://" + localPath3;

&#x20;       String filePath4 = "file://" + localPath4;

&#x20;       Map<String, Object> params = new HashMap<>();

&#x20;       params.put("video", Arrays.asList(filePath1,filePath2,filePath3,filePath4));

&#x20;       // The fps parameter is available for the Qwen3.5, Qwen3-VL, and Qwen2.5-VL series models when you provide an image list.

&#x20;       params.put("fps", 2);

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder()

&#x20;               .role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(params,

&#x20;                       Collections.singletonMap("text", "Describe the process shown in this video.")))

&#x20;               .build();

&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               // If you have not configured an environment variable, replace the following line with your Model Studio API key: .apiKey("sk-xxx")

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model(MODEL\_NAME)

&#x20;               .messages(Arrays.asList(userMessage)).build();

&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));

&#x20;   }

&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           videoImageListSample(

&#x20;                   "xxx/football1.jpg",

&#x20;                   "xxx/football2.jpg",

&#x20;                   "xxx/football3.jpg",

&#x20;                   "xxx/football4.jpg");

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\## Base64 encoding



\## OpenAI compatible



\## Python



```

import os

from openai import OpenAI

import base64



\# Converts a local file to a Base64-encoded string.

def encode\_image(image\_path):

&#x20;   with open(image\_path, "rb") as image\_file:

&#x20;       return base64.b64encode(image\_file.read()).decode("utf-8")



base64\_image1 = encode\_image("football1.jpg")

base64\_image2 = encode\_image("football2.jpg")

base64\_image3 = encode\_image("football3.jpg")

base64\_image4 = encode\_image("football4.jpg")

client = OpenAI(

&#x20;   # An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx",

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   # Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;   base\_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",

)

completion = client.chat.completions.create(

&#x20;   model="qwen3.5-plus",  # This example uses the qwen3.5-plus model. You can replace it as needed. For available models, see the Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   messages=\[  

&#x20;   {"role": "user","content": \[

&#x20;       {"type": "video","video": \[

&#x20;           f"data:image/jpeg;base64,{base64\_image1}",

&#x20;           f"data:image/jpeg;base64,{base64\_image2}",

&#x20;           f"data:image/jpeg;base64,{base64\_image3}",

&#x20;           f"data:image/jpeg;base64,{base64\_image4}",]},

&#x20;       {"type": "text","text": "Describe the process shown in this video."},

&#x20;   ]}]

)

print(completion.choices\[0].message.content)

```



\## Node.js



```

import OpenAI from "openai";

import { readFileSync } from 'fs';



const openai = new OpenAI(

&#x20;   {

&#x20;       // An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;       // If you have not configured an environment variable, replace the following line with your Model Studio API key: apiKey: "sk-xxx"

&#x20;       apiKey: process.env.DASHSCOPE\_API\_KEY,

&#x20;       // Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;       baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

&#x20;   }

);



const encodeImage = (imagePath) => {

&#x20;   const imageFile = readFileSync(imagePath);

&#x20;   return imageFile.toString('base64');

&#x20; };

&#x20; 

const base64Image1 = encodeImage("football1.jpg")

const base64Image2 = encodeImage("football2.jpg")

const base64Image3 = encodeImage("football3.jpg")

const base64Image4 = encodeImage("football4.jpg")

async function main() {

&#x20;   const completion = await openai.chat.completions.create({

&#x20;       model: "qwen3.5-plus",  // This example uses the qwen3.5-plus model. You can replace it as needed. For available models, see the Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;       messages: \[

&#x20;           {"role": "user",

&#x20;            "content": \[{"type": "video",

&#x20;                       "video": \[

&#x20;                           `data:image/jpeg;base64,${base64Image1}`,

&#x20;                           `data:image/jpeg;base64,${base64Image2}`,

&#x20;                           `data:image/jpeg;base64,${base64Image3}`,

&#x20;                           `data:image/jpeg;base64,${base64Image4}`]},

&#x20;                       {"type": "text", "text": "Describe the process shown in this video."}]}]

&#x20;   });

&#x20;   console.log(completion.choices\[0].message.content);

}



main();

```



\## curl



\-   For an example of converting a file to a Base64-encoded string, see the \[Example code](#7aee9382dfqpk).

&#x20;   

\-   The Base64-encoded string `"data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` is truncated for display. You must pass the complete string in your request.

&#x20;   



```

\# ======= Important =======

\# Endpoints vary by Region. Modify the endpoint for your Region.

\# An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "messages": \[{"role": "user",

&#x20;               "content": \[{"type": "video",

&#x20;               "video": \[

&#x20;                         "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA...",

&#x20;                         "data:image/jpeg;base64,nEpp6jpnP57MoWSyOWwrkXMJhHRCWYeFYb...",

&#x20;                         "data:image/jpeg;base64,JHWQnJPc40GwQ7zERAtRMK6iIhnWw4080s...",

&#x20;                         "data:image/jpeg;base64,adB6QOU5HP7dAYBBOg/Fb7KIptlbyEOu58..."

&#x20;                         ]},

&#x20;               {"type": "text",

&#x20;               "text": "Describe the process shown in this video."}]}]

}'

```



\## DashScope



\## Python



```

import base64

import os

import dashscope



\# Endpoints vary by Region. Modify the endpoint for your Region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



\# Converts a local file to a Base64-encoded string.

def encode\_image(image\_path):

&#x20;   with open(image\_path, "rb") as image\_file:

&#x20;       return base64.b64encode(image\_file.read()).decode("utf-8")



base64\_image1 = encode\_image("football1.jpg")

base64\_image2 = encode\_image("football2.jpg")

base64\_image3 = encode\_image("football3.jpg")

base64\_image4 = encode\_image("football4.jpg")





messages = \[{'role':'user',

&#x20;           'content': \[

&#x20;                   {'video':

&#x20;                        \[f"data:image/jpeg;base64,{base64\_image1}",

&#x20;                         f"data:image/jpeg;base64,{base64\_image2}",

&#x20;                         f"data:image/jpeg;base64,{base64\_image3}",

&#x20;                         f"data:image/jpeg;base64,{base64\_image4}"

&#x20;                        ]

&#x20;                   },

&#x20;                   {'text': 'Describe the process shown in this video.'}]}]

response = dashscope.MultiModalConversation.call(

&#x20;   # An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   # If you have not configured an environment variable, replace the following line with your Model Studio API key: api\_key="sk-xxx"

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   model='qwen3.5-plus',  # This example uses the qwen3.5-plus model. You can replace it as needed. For available models, see the Model list: https://www.alibabacloud.com/help/en/model-studio/getting-started/models

&#x20;   messages=messages)



print(response.output.choices\[0].message.content\[0]\["text"])

```



\## Java



```

import java.io.IOException;

import java.util.\*;

import java.nio.file.Files;

import java.nio.file.Path;

import java.nio.file.Paths;



import com.alibaba.dashscope.aigc.multimodalconversation.\*;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {



&#x20;   static {

&#x20;       // Endpoints vary by Region. Modify the endpoint for your Region.

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }



&#x20;   private static String encodeImageToBase64(String imagePath) throws IOException {

&#x20;       Path path = Paths.get(imagePath);

&#x20;       byte\[] imageBytes = Files.readAllBytes(path);

&#x20;       return Base64.getEncoder().encodeToString(imageBytes);

&#x20;   }



&#x20;   public static void videoImageListSample(String localPath1,String localPath2,String localPath3,String localPath4)

&#x20;           throws ApiException, NoApiKeyException, UploadFileException, IOException {



&#x20;       String base64Image1 = encodeImageToBase64(localPath1);

&#x20;       String base64Image2 = encodeImageToBase64(localPath2);

&#x20;       String base64Image3 = encodeImageToBase64(localPath3);

&#x20;       String base64Image4 = encodeImageToBase64(localPath4);



&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       Map<String, Object> params = new HashMap<>();

&#x20;       params.put("video", Arrays.asList(

&#x20;                       "data:image/jpeg;base64," + base64Image1,

&#x20;                       "data:image/jpeg;base64," + base64Image2,

&#x20;                       "data:image/jpeg;base64," + base64Image3,

&#x20;                       "data:image/jpeg;base64," + base64Image4));

&#x20;       // The fps parameter is available for the Qwen3.5, Qwen3-VL, and Qwen2.5-VL series models when you provide an image list.

&#x20;       params.put("fps", 2);

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder()

&#x20;               .role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(params,

&#x20;                       Collections.singletonMap("text", "Describe the process shown in this video.")))

&#x20;               .build();



&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               // If you have not configured an environment variable, replace the following line with your Model Studio API key: .apiKey("sk-xxx")

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen3.5-plus")

&#x20;               .messages(Arrays.asList(userMessage))

&#x20;               .build();



&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));

&#x20;   }



&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           // Replace placeholders such as "xxx/football1.jpg" with the absolute paths to your local image files.

&#x20;           videoImageListSample(

&#x20;                   "xxx/football1.jpg",

&#x20;                   "xxx/football2.jpg",

&#x20;                   "xxx/football3.jpg",

&#x20;                   "xxx/football4.jpg"

&#x20;           );

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\## curl



\-   For an example of converting a file to a Base64-encoded string, see the \[Example code](#7aee9382dfqpk).

&#x20;   

\-   The Base64-encoded string `"data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."` is truncated for display. You must pass the complete string in your request.

&#x20;   



```

\# ======= Important =======

\# Endpoints vary by Region. Modify the endpoint for your Region.

\# An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20; "model": "qwen3.5-plus",

&#x20; "input": {

&#x20;   "messages": \[

&#x20;     {

&#x20;       "role": "user",

&#x20;       "content": \[

&#x20;         {

&#x20;           "video": \[

&#x20;                     "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA...",

&#x20;                     "data:image/jpeg;base64,nEpp6jpnP57MoWSyOWwrkXMJhHRCWYeFYb...",

&#x20;                     "data:image/jpeg;base64,JHWQnJPc40GwQ7zERAtRMK6iIhnWw4080s...",

&#x20;                     "data:image/jpeg;base64,adB6QOU5HP7dAYBBOg/Fb7KIptlbyEOu58..."

&#x20;           ],

&#x20;           "fps":2     

&#x20;         },

&#x20;         {

&#x20;           "text": "Describe the process shown in this video."

&#x20;         }

&#x20;       ]

&#x20;     }

&#x20;   ]

&#x20; }

}'

```



\### Process high-resolution images



The visual understanding model API limits the number of visual tokens per encoded image. By default, high-resolution images are compressed, which can cause detail loss and reduce understanding accuracy. You can enable `vl\_high\_resolution\_images` or adjust `max\_pixels` to increase the visual token count, which preserves more image detail and improves understanding.



\*\*View pixels per visual token, token limit, and pixel limit for each model\*\*



> If an input image's pixel count exceeds the model's pixel limit, the image is scaled down to fit within the limit.



| \*\*Model\*\* | \*\*Pixels per token\*\* | \*\*vl\\\\\_high\\\\\_resolution\\\\\_images\*\* | \*\*max\\\\\_pixels\*\* | \*\*Token limit\*\* | \*\*Pixel limit\*\* |

| --- | --- | --- | --- | --- | --- |

| `Qwen3.5` and `Qwen3-VL` series models | `32\*32` | `true` | `max\_pixels` is ignored. | `16384 tokens` | `16777216` (which is `16384\*32\*32`) |

| `false` (default) | The value is customizable, with a default of `2621440` and a maximum of `16777216`. | Determined by `max\_pixels`, calculated as `max\_pixels/32/32`. | `max\_pixels` |

| `qwen-vl-max`, `qwen-vl-max-latest`, `qwen-vl-max-2025-08-13`, `qwen-vl-plus`, `qwen-vl-plus-latest`, and `qwen-vl-plus-2025-08-15` models | `32\*32` | `true` | `max\_pixels` is ignored. | `16384 tokens` | `16777216` (which is `16384\*32\*32`) |

| `false` (default) | The value is customizable, with a default of `1310720` and a maximum of `16777216`. | Determined by `max\_pixels`, calculated as `max\_pixels/32/32`. | `max\_pixels` |

| Other `qwen-vl-max` and `qwen-vl-plus` models, the `Qwen2.5-VL` open-source series, and `QVQ` series models | `28\*28` | `true` | `max\_pixels` is ignored. | `16384 tokens` | `12845056` (which is `16384\*28\*28`) |

| `false` (default) | The value is customizable, with a default of `1003520` and a maximum of `12845056`. | Determined by `max\_pixels`, calculated as `max\_pixels/28/28`. | `max\_pixels` |



\-   When `vl\_high\_resolution\_images=true`, the API uses a fixed resolution policy and ignores the `max\_pixels` setting. This is ideal for tasks that require recognizing fine text, small objects, or rich details in images.

&#x20;   

\-   When `vl\_high\_resolution\_images=false`, the `max\_pixels` parameter determines the final pixel limit.

&#x20;   

&#x20;   -   For applications that require high processing speed or are cost-sensitive, use the default value for `max\_pixels` or set it to a smaller value.

&#x20;       

&#x20;   -   If you need to preserve some detail and can accept a lower processing speed, increase the value of `max\_pixels`.

&#x20;       



\## OpenAI compatible



The `vl\_high\_resolution\_images` parameter is not a standard OpenAI parameter. The method for passing it varies by SDK:



\-   \*\*Python SDK:\*\* Pass the parameter in the `extra\_body` dictionary.

&#x20;   

\-   \*\*Node.js SDK:\*\* Pass the parameter directly as a top-level parameter.

&#x20;   



\## Python



```

import os

import time

from openai import OpenAI



client = OpenAI(

&#x20;   # An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;   api\_key=os.getenv("DASHSCOPE\_API\_KEY"),

&#x20;   # Modify the endpoint for your Region.

&#x20;   base\_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",

)



completion = client.chat.completions.create(

&#x20;   model="qwen3.5-plus",

&#x20;   messages=\[

&#x20;       {"role": "user","content": \[

&#x20;           {"type": "image\_url","image\_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg\_VCG211286867973\_RF.jpg"},

&#x20;           # max\_pixels: Sets the maximum pixel count for the input image. Ignored when vl\_high\_resolution\_images=True. The maximum value is model-dependent.

&#x20;           # "max\_pixels": 16384 \* 32 \* 32

&#x20;           },

&#x20;          {"type": "text", "text": "What holiday does this image depict?"},

&#x20;           ],

&#x20;       }

&#x20;   ],

&#x20;   extra\_body={"vl\_high\_resolution\_images":True}



)

print(f"Model output: {completion.choices\[0].message.content}")

print(f"Total input tokens: {completion.usage.prompt\_tokens}")

```



\## Node.js



```

import OpenAI from "openai";



const openai = new OpenAI(

&#x20;   {

&#x20;       // If not using an environment variable, set your Model Studio API key here: apiKey: "sk-xxx"

&#x20;       // An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;       apiKey: process.env.DASHSCOPE\_API\_KEY,

&#x20;       // Modify the endpoint for your Region.

&#x20;       baseURL: "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

&#x20;   }

);



const response = await openai.chat.completions.create({

&#x20;       model: "qwen3.5-plus",

&#x20;       messages: \[

&#x20;       {role: "user",content: \[

&#x20;           {type: "image\_url",

&#x20;           image\_url: {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg\_VCG211286867973\_RF.jpg"},

&#x20;           // max\_pixels: Sets the maximum pixel count for the input image. Ignored when vl\_high\_resolution\_images=True. The maximum value is model-dependent.

&#x20;           // "max\_pixels": 2560 \* 32 \* 32

&#x20;           },

&#x20;           {type: "text", text: "What holiday does this image depict?" },

&#x20;       ]}],

&#x20;       vl\_high\_resolution\_images:true

&#x20;   })





console.log("Model output:",response.choices\[0].message.content);

console.log("Total input tokens:",response.usage.prompt\_tokens);

```



\## curl



```

\# ======= Important =======

\# An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Modify the endpoint for your Region.

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/compatible-mode/v1/chat/completions \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20; "model": "qwen3.5-plus",

&#x20; "messages": \[

&#x20;   {

&#x20;     "role": "user",

&#x20;     "content": \[

&#x20;       {

&#x20;         "type": "image\_url",

&#x20;         "image\_url": {

&#x20;           "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg\_VCG211286867973\_RF.jpg"

&#x20;         }

&#x20;       },

&#x20;       {

&#x20;         "type": "text",

&#x20;         "text": "What holiday does this image depict?"

&#x20;       }

&#x20;     ]

&#x20;   }

&#x20; ],

&#x20; "vl\_high\_resolution\_images":true

}'

```



\## DashScope



\## Python



```

import os

import time



import dashscope



\# Modify the endpoint for your Region.

dashscope.base\_http\_api\_url = 'https://dashscope-intl.aliyuncs.com/api/v1'



messages = \[

&#x20;   {

&#x20;       "role": "user",

&#x20;       "content": \[

&#x20;           {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg\_VCG211286867973\_RF.jpg",

&#x20;           # max\_pixels: Sets the maximum pixel count for the input image. Ignored when vl\_high\_resolution\_images=True. The maximum value is model-dependent.

&#x20;           # "max\_pixels": 16384 \* 32 \* 32

&#x20;           },

&#x20;           {"text": "What holiday does this image depict?"}

&#x20;       ]

&#x20;   }

]



response = dashscope.MultiModalConversation.call(

&#x20;       # If not using an environment variable, set your Model Studio API key here: api\_key="sk-xxx"

&#x20;       # An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;       api\_key=os.getenv('DASHSCOPE\_API\_KEY'),

&#x20;       model='qwen3.5-plus',

&#x20;       messages=messages,

&#x20;       vl\_high\_resolution\_images=True

&#x20;   )

&#x20;   

print("Model output:",response.output.choices\[0].message.content\[0]\["text"])

print("Total input tokens:",response.usage.input\_tokens)

```



\## Java



```

import java.util.Arrays;

import java.util.Collections;

import java.util.Map;

import java.util.HashMap;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;

import com.alibaba.dashscope.common.MultiModalMessage;

import com.alibaba.dashscope.common.Role;

import com.alibaba.dashscope.exception.ApiException;

import com.alibaba.dashscope.exception.NoApiKeyException;

import com.alibaba.dashscope.exception.UploadFileException;

import com.alibaba.dashscope.utils.Constants;



public class Main {



&#x20;   static {

&#x20;       // Modify the endpoint for your Region.

&#x20;       Constants.baseHttpApiUrl="https://dashscope-intl.aliyuncs.com/api/v1";

&#x20;   }

&#x20;   

&#x20;   public static void simpleMultiModalConversationCall()

&#x20;           throws ApiException, NoApiKeyException, UploadFileException {

&#x20;       MultiModalConversation conv = new MultiModalConversation();

&#x20;       Map<String, Object> map = new HashMap<>();

&#x20;       map.put("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg\_VCG211286867973\_RF.jpg");

&#x20;       // max\_pixels: Sets the maximum pixel count for the input image. Ignored when vl\_high\_resolution\_images=True. The maximum value is model-dependent.

&#x20;       // map.put("max\_pixels", 2621440); 

&#x20;       MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())

&#x20;               .content(Arrays.asList(

&#x20;                       map,

&#x20;                       Collections.singletonMap("text", "What holiday does this image depict?"))).build();

&#x20;       MultiModalConversationParam param = MultiModalConversationParam.builder()

&#x20;               // If not using an environment variable, set your Model Studio API key here: .apiKey("sk-xxx")

&#x20;               // An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

&#x20;               .apiKey(System.getenv("DASHSCOPE\_API\_KEY"))

&#x20;               .model("qwen3.5-plus")

&#x20;               .message(userMessage)

&#x20;               .vlHighResolutionImages(true)

&#x20;               .build();

&#x20;       MultiModalConversationResult result = conv.call(param);

&#x20;       System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));

&#x20;       System.out.println(result.getUsage().getInputTokens());

&#x20;   }



&#x20;   public static void main(String\[] args) {

&#x20;       try {

&#x20;           simpleMultiModalConversationCall();

&#x20;       } catch (ApiException | NoApiKeyException | UploadFileException e) {

&#x20;           System.out.println(e.getMessage());

&#x20;       }

&#x20;       System.exit(0);

&#x20;   }

}

```



\## curl



```

\# ======= Important =======

\# An API key is required for each Region. To get an API key, see: https://www.alibabacloud.com/help/en/model-studio/get-api-key

\# Modify the endpoint for your Region.

\# === Remove this comment before execution ===



curl -X POST https://dashscope-intl.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \\

\-H "Authorization: Bearer $DASHSCOPE\_API\_KEY" \\

\-H 'Content-Type: application/json' \\

\-d '{

&#x20;   "model": "qwen3.5-plus",

&#x20;   "input":{

&#x20;       "messages":\[

&#x20;           {

&#x20;            "role": "user",

&#x20;            "content": \[

&#x20;              {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg\_VCG211286867973\_RF.jpg"},

&#x20;              {"text": "What holiday does this image depict?"}

&#x20;               ]

&#x20;           }

&#x20;       ]

&#x20;   },

&#x20;   "parameters": {

&#x20;       "vl\_high\_resolution\_images": true

&#x20;   }

}'

```



\### \*\*Next\*\* steps



\-   \[Multi-turn conversation](/help/en/model-studio/multi-round-conversation#6feb3eb136g3q)

&#x20;   

\-   \[Streaming output](/help/en/model-studio/stream#39de325514ak9)

&#x20;   



\## \*\*Limitations\*\*



\### \*\*Input\*\* file limits



\## \*\*Image limits\*\*



\-   \*\*Image resolution:\*\*

&#x20;   

&#x20;   -   Minimum dimensions: The width and height of the image must both be greater than `10` pixels.

&#x20;       

&#x20;   -   Aspect ratio: The ratio of the long side to the short side of the image must not exceed `200:1`.

&#x20;       

&#x20;   -   Pixel limit:

&#x20;       

&#x20;       -   Keep the image resolution within `8K (7680x4320)`. Images exceeding this resolution may cause an API call timeout due to a large file size or long network transmission.

&#x20;           

&#x20;       -   Automatic scaling: The model can adjust the image size using the `max\_pixels` and `min\_pixels` parameters. Providing an ultra-high-resolution image does not improve recognition accuracy but increases the risk of a call failure. Scale the image to a reasonable size on the client beforehand.

&#x20;           

\-   \*\*Supported image formats\*\*

&#x20;   

&#x20;   -   For resolutions below 4K `(3840x2160)`, the supported image formats are as follows:

&#x20;       

&#x20;       | \*\*Image format\*\* | \*\*Common extensions\*\* | \*\*Media type\*\* |

&#x20;       | --- | --- | --- |

&#x20;       | BMP | .bmp | image/bmp |

&#x20;       | JPEG | .jpe, .jpeg, .jpg | image/jpeg |

&#x20;       | PNG | .png | image/png |

&#x20;       | TIFF | .tif, .tiff | image/tiff |

&#x20;       | WEBP | .webp | image/webp |

&#x20;       | HEIC | .heic | image/heic |

&#x20;       

&#x20;   -   For resolutions between `4K (3840x2160)` and `8K (7680x4320)`, only JPEG, JPG, and PNG are supported.

&#x20;       

\-   \*\*Image size:\*\*

&#x20;   

&#x20;   -   When passed as a public URL: A single image cannot exceed `20 MB` for the Qwen3.5 series, and `10 MB` for other models.

&#x20;       

&#x20;   -   When passed as a local file path (DashScope SDK only): A single image cannot exceed `10 MB`.

&#x20;       

&#x20;   -   When passed as a Base64-encoded string: The encoded string cannot exceed `10 MB`.

&#x20;       

&#x20;   

&#x20;   > To compress files, see \[How to compress an image or video to the required size](#ec8e0a8e03moe).

&#x20;   

\-   \*\*Number of supported images:\*\* The number of images you can pass is limited by the model's maximum input. The total number of tokens for all images and text must be less than the model's maximum input.

&#x20;   

&#x20;   > For example, with the `qwen3-vl-plus` model, the maximum input in thinking mode is `258048` `Token`s. If the text consumes `100` tokens and an image consumes `2560` tokens (to calculate the tokens for an image, see \[Billing and rate limiting](#10c14b25cdhuh)), you can input a maximum of `(258048-100)/ 2560 ≈ 100` images.

&#x20;   



\## \*\*Video limits\*\*



\-   \*\*When you submit a video as a list of images, the following limits apply to the number of images:\*\*

&#x20;   

&#x20;   -   `qwen3.5` series: A minimum of 4 images and a maximum of 8,000 images.

&#x20;       

&#x20;   -   `qwen3-vl-plus` series, `qwen3-vl-flash` series, `qwen3-vl-235b-a22b-thinking`, and `qwen3-vl-235b-a22b-instruct`: A minimum of 4 images and a maximum of 2,000 images.

&#x20;       

&#x20;   -   Other `Qwen3-VL` open source, `Qwen2.5-VL` (including commercial version and open source versions), and `QVQ` series models: A minimum of 4 images and a maximum of 512 images.

&#x20;       

&#x20;   -   Other models: A minimum of 4 images and a maximum of 80 images.

&#x20;       

\-   \*\*When you submit a video as a single file:\*\*

&#x20;   

&#x20;   -   \*\*Video size:\*\*

&#x20;       

&#x20;       -   When passed as a public URL:

&#x20;           

&#x20;           -   `qwen3.5` series, `Qwen3-VL` series, and `qwen-vl-max` (including `qwen-vl-max-latest`, `qwen-vl-max-2025-04-08`, and all subsequent versions): Cannot exceed 2 GB.

&#x20;               

&#x20;           -   `qwen-vl-plus` series, other `qwen-vl-max` models, `Qwen2.5-VL` open source series, and `QVQ` series models: Cannot exceed 1 GB.

&#x20;               

&#x20;           -   Other models: Cannot exceed 150 MB.

&#x20;               

&#x20;       -   When passed as a Base64-encoded string: The encoded string must be less than 10 MB.

&#x20;           

&#x20;       -   When passed as a local file path (DashScope SDK only): The video file cannot exceed 100 MB.

&#x20;           

&#x20;       

&#x20;       > To compress files, see \[How to compress an image or video to the required size](#ec8e0a8e03moe).

&#x20;       

&#x20;   -   \*\*Video duration:\*\*

&#x20;       

&#x20;       -   `qwen3.5` series: 2 seconds to 2 hours.

&#x20;           

&#x20;       -   `qwen3-vl-plus` series, `qwen3-vl-flash` series, `qwen3-vl-235b-a22b-thinking`, and `qwen3-vl-235b-a22b-instruct`: 2 seconds to 1 hour.

&#x20;           

&#x20;       -   Other `Qwen3-VL` open source series and `qwen-vl-max` (including `qwen-vl-max-latest`, `qwen-vl-max-2025-04-08`, and subsequent versions): 2 seconds to 20 minutes.

&#x20;           

&#x20;       -   `qwen-vl-plus` series, other `qwen-vl-max` models, `Qwen2.5-VL` open source series, and `QVQ` series models: 2 seconds to 10 minutes.

&#x20;           

&#x20;       -   Other models: 2 seconds to 40 seconds.

&#x20;           

&#x20;   -   \*\*Video format:\*\* Supported formats include MP4, AVI, MKV, MOV, FLV, and WMV.

&#x20;       

&#x20;   -   \*\*Video dimensions:\*\* No specific limit. The model automatically adjusts video dimensions using the `max\_pixels` and `min\_pixels` parameters. Using larger video dimensions does not improve understanding.

&#x20;       

&#x20;   -   \*\*Audio understanding:\*\* The model does not process audio from video files.

&#x20;       



\### \*\*File\*\* input methods



\-   \*\*Public URL\*\*: Provide a publicly accessible URL that uses the HTTP or HTTPS protocol. For optimal stability and performance, you can upload the file \[to OSS](/help/en/oss/user-guide/console-quick-start) to get a public URL.

&#x20;   

&#x20;   \*\*Important\*\*

&#x20;   

&#x20;   To ensure that the model can successfully download the file, the response header of the public URL \*\*must\*\* include Content-Length (file size) and Content-Type (media type, such as image/jpeg). If either field is missing or incorrect, the model cannot download the file.

&#x20;   

\-   \*\*Pass as a Base64-encoded string:\*\*

&#x20;   

\-   \*\*Pass as a local file path (DashScope SDK only):\*\*

&#x20;   



> For recommendations on file input methods, see \[How to choose a file upload method?](#dc4e7260aauuo)



\## \*\*Production\*\* usage



\-   \*\*Image/video preprocessing:\*\* The visual understanding model has size limits for input files. For file compression methods, see \[Image or video compression methods](/help/en/model-studio/vision#ec8e0a8e03moe).

&#x20;   

\-   \*\*Processing text files:\*\* The visual understanding model only supports files in image formats and cannot directly process text files. You can use the following alternatives:

&#x20;   

&#x20;   -   Convert the text file to an image format. We recommend using an image processing library, such as `Python`'s `pdf2image` library, to convert the file page by page into multiple high-quality images. Then, pass the resulting images to the model using the \[multiple image input](#f6256b3818huu) method.

&#x20;       

&#x20;   -   \[Qwen-Long](/help/en/model-studio/long-context-qwen-long) can process text files and parse their content.

&#x20;       



\-   \*\*Fault tolerance and stability\*\*

&#x20;   

&#x20;   -   Timeout handling: For non-streaming calls, if the model does not finish generating output within 180 seconds, a timeout error typically occurs. To improve the user experience, the response body will contain any content generated before the timeout. If the response header contains `x-dashscope-partialresponse:true`, this indicates that a timeout occurred. You can use the \[partial mode](/help/en/model-studio/partial-mode) feature, available on some models, to append the generated content to the `messages` array and resend the request. This allows the model to continue generating content from where it left off. See \[Continue writing based on incomplete output](/help/en/model-studio/partial-mode#8cc28acfd7a91).

&#x20;       

&#x20;   -   Retry mechanism: Implement a reasonable API call retry mechanism, such as exponential backoff, to handle potential network fluctuations or temporary service unavailability.

&#x20;       



\## \*\*Billing\*\* and rate limiting



\-   \*\*Billing:\*\* The total cost is based on the total number of input and output tokens. For input and output prices, see the \[Model list](/help/en/model-studio/models).

&#x20;   

&#x20;   -   \*\*Token composition:\*\* Input tokens consist of text tokens and tokens converted from images or videos. Output tokens are the model-generated text. In `thinking mode`, the model's reasoning process also counts as output tokens. If the reasoning process is not output in `thinking mode`, the non-thinking mode price applies.

&#x20;       

&#x20;   -   \*\*Calculate image and video tokens:\*\* Use the following code to estimate the token consumption for an image or video. This estimate is for reference only. Actual charges are based on the API response.

&#x20;       

&#x20;       \*\*Calculate image and video tokens\*\*

&#x20;       

&#x20;       ## \*\*Image\*\*

&#x20;       

&#x20;       Formula: `Image Token = h\_bar \* w\_bar / token\_pixels + 2`

&#x20;       

&#x20;       -   `h\_bar, w\_bar`: The height and width of the scaled image. Before processing an image, the model scales it to a specific pixel limit. This limit depends on the `max\_pixels` and `vl\_high\_resolution\_images` parameters. See \[Process high-resolution images](#e7e2db755f9h7).

&#x20;           

&#x20;       -   `token\_pixels`: The number of pixels that correspond to each visual `Token`. This value varies depending on the model:

&#x20;           

&#x20;           -   `Qwen3.5`, `Qwen3-VL`, `qwen-vl-max`, `qwen-vl-max-latest`, `qwen-vl-max-2025-08-13`, `qwen-vl-plus`, `qwen-vl-plus-latest`, and `qwen-vl-plus-2025-08-15`\*\*:\*\* Each `Token` corresponds to `32x32` pixels.

&#x20;               

&#x20;           -   `QVQ` and other `Qwen2.5-VL` models\*\*:\*\* Each token corresponds to `28x28` pixels.

&#x20;               

&#x20;       

&#x20;       The following code shows the model's approximate image scaling logic. Use it to estimate the token count for an image. The actual charges are based on the API response.

&#x20;       

&#x20;       ```

&#x20;       import math

&#x20;       # Use the following command to install the Pillow library: pip install Pillow

&#x20;       from PIL import Image

&#x20;       

&#x20;       def token\_calculate(image\_path, max\_pixels, vl\_high\_resolution\_images):

&#x20;           # Open the specified image file.

&#x20;           image = Image.open(image\_path)

&#x20;       

&#x20;           # Get the original dimensions of the image.

&#x20;           height = image.height

&#x20;           width = image.width

&#x20;       

&#x20;           # Adjust the width and height to be multiples of 32 or 28, depending on the model.

&#x20;           h\_bar = round(height / 32) \* 32

&#x20;           w\_bar = round(width / 32) \* 32

&#x20;       

&#x20;           # Minimum pixel count for an image.

&#x20;           min\_pixels = 4 \* 32 \* 32

&#x20;           # If vl\_high\_resolution\_images is set to True, the upper limit for input image tokens is 16,386, and the corresponding maximum pixel value is 16384 \* 32 \* 32 or 16384 \* 28 \* 28. Otherwise, the value of the max\_pixels parameter is used.

&#x20;           if vl\_high\_resolution\_images:

&#x20;               max\_pixels = 16384 \* 32 \* 32

&#x20;           else:

&#x20;               max\_pixels = max\_pixels

&#x20;       

&#x20;           # Scale the image so that the total number of pixels is within the range of \[min\_pixels, max\_pixels].

&#x20;           if h\_bar \* w\_bar > max\_pixels:

&#x20;               # Calculate the scaling factor beta so that the total pixels of the scaled image do not exceed max\_pixels.

&#x20;               beta = math.sqrt((height \* width) / max\_pixels)

&#x20;               # Recalculate the adjusted width and height.

&#x20;               h\_bar = math.floor(height / beta / 32) \* 32

&#x20;               w\_bar = math.floor(width / beta / 32) \* 32

&#x20;           elif h\_bar \* w\_bar < min\_pixels:

&#x20;               # Calculate the scaling factor beta so that the total pixels of the scaled image are not less than min\_pixels.

&#x20;               beta = math.sqrt(min\_pixels / (height \* width))

&#x20;               # Recalculate the adjusted height and width.

&#x20;               h\_bar = math.ceil(height \* beta / 32) \* 32

&#x20;               w\_bar = math.ceil(width \* beta / 32) \* 32

&#x20;           return h\_bar, w\_bar

&#x20;       

&#x20;       if \_\_name\_\_ == "\_\_main\_\_":

&#x20;           # Replace xxx/test.jpg with the path to your local image.

&#x20;           h\_bar, w\_bar =  token\_calculate("xxx/test.jpg", max\_pixels=16384\*32\*32, vl\_high\_resolution\_images=False)

&#x20;           print(f"Scaled image dimensions: height {h\_bar}, width {w\_bar}")

&#x20;           # The system automatically adds the <|vision\_bos|> and <|vision\_eos|> visual markers (1 Token each).

&#x20;           token = int((h\_bar \* w\_bar) / (32 \* 32))+2

&#x20;           print(f"Number of Tokens for the image: {token}")

&#x20;       ```

&#x20;       

&#x20;       ## Video

&#x20;       

&#x20;       -   \*\*Video file:\*\*

&#x20;           

&#x20;           When processing a video file, the model first extracts frames and then calculates the total number of tokens for all frames. This calculation is complex. Use the following code to estimate a video's total token consumption by providing its path:

&#x20;           

&#x20;           ```

&#x20;           # Before use, install: pip install opencv-python

&#x20;           import math

&#x20;           import os

&#x20;           import logging

&#x20;           import cv2

&#x20;           

&#x20;           logger = logging.getLogger(\_\_name\_\_)

&#x20;           

&#x20;           FRAME\_FACTOR = 2

&#x20;           

&#x20;           # For the Qwen3-VL, qwen-vl-max-0813, qwen-vl-plus-0815, and qwen-vl-plus-0710 models, the image scaling factor is 32.

&#x20;           IMAGE\_FACTOR = 32

&#x20;           

&#x20;           # For other models, the image scaling factor is 28.

&#x20;           # IMAGE\_FACTOR = 28

&#x20;           

&#x20;           # Maximum aspect ratio for video frames.

&#x20;           MAX\_RATIO = 200

&#x20;           # Minimum pixel count for video frames.

&#x20;           VIDEO\_MIN\_PIXELS = 4 \* 32 \* 32

&#x20;           # Maximum pixel count for video frames. For the Qwen3-VL-Plus model, VIDEO\_MAX\_PIXELS is 640 \* 32 \* 32. For other models, the value is 768 \* 32 \* 32.

&#x20;           VIDEO\_MAX\_PIXELS = 640 \* 32 \* 32

&#x20;           

&#x20;           # If an FPS parameter is not provided, the default value is used.

&#x20;           FPS = 2.0

&#x20;           # Minimum number of extracted frames.

&#x20;           FPS\_MIN\_FRAMES = 4

&#x20;           # Maximum number of extracted frames. This value is 2000 for the Qwen3-VL-Plus model, 512 for Qwen3-VL-Flash and Qwen2.5-VL models, and 80 for others.

&#x20;           FPS\_MAX\_FRAMES = 2000

&#x20;           

&#x20;           # Maximum total pixels for video input. This value is 131072 \* 32 \* 32 for the Qwen3-VL-Plus model and 65536 \* 32 \* 32 for other models.

&#x20;           VIDEO\_TOTAL\_PIXELS = int(float(os.environ.get('VIDEO\_MAX\_PIXELS', 131072 \* 32 \* 32)))

&#x20;           

&#x20;           def round\_by\_factor(number: int, factor: int) -> int:

&#x20;               """Returns the integer closest to 'number' that is divisible by 'factor'."""

&#x20;               return round(number / factor) \* factor

&#x20;           

&#x20;           def ceil\_by\_factor(number: int, factor: int) -> int:

&#x20;               """Returns the smallest integer greater than or equal to 'number' that is divisible by 'factor'."""

&#x20;               return math.ceil(number / factor) \* factor

&#x20;           

&#x20;           def floor\_by\_factor(number: int, factor: int) -> int:

&#x20;               """Returns the largest integer less than or equal to 'number' that is divisible by 'factor'."""

&#x20;               return math.floor(number / factor) \* factor

&#x20;           

&#x20;           def extract\_vision\_info(conversations):

&#x20;               vision\_infos = \[]

&#x20;               if isinstance(conversations\[0], dict):

&#x20;                   conversations = \[conversations]

&#x20;               for conversation in conversations:

&#x20;                   for message in conversation:

&#x20;                       if isinstance(message\["content"], list):

&#x20;                           for ele in message\["content"]:

&#x20;                               if (

&#x20;                                   "image" in ele

&#x20;                                   or "image\_url" in ele

&#x20;                                   or "video" in ele

&#x20;                                   or ele.get("type","") in ("image", "image\_url", "video")

&#x20;                               ):

&#x20;                                   vision\_infos.append(ele)

&#x20;               return vision\_infos

&#x20;           

&#x20;           def smart\_nframes(ele,total\_frames,video\_fps):

&#x20;               """Calculates the number of video frames to extract.

&#x20;           

&#x20;               Args:

&#x20;                   ele (dict): A dictionary that contains the video configuration.

&#x20;                       - fps: Controls the number of frames extracted for the model input.

&#x20;                   total\_frames (int): The original total number of frames in the video.

&#x20;                   video\_fps (int | float): The original frame rate of the video.

&#x20;           

&#x20;               Raises:

&#x20;                   Raises a `ValueError` if nframes is not within the interval \[FRAME\_FACTOR, total\_frames].

&#x20;           

&#x20;               Returns:

&#x20;                   The number of video frames to use for model input.

&#x20;               """

&#x20;               assert not ("fps" in ele and "nframes" in ele), "Only accept either `fps` or `nframes`"

&#x20;               fps = ele.get("fps", FPS)

&#x20;               min\_frames = ceil\_by\_factor(ele.get("min\_frames", FPS\_MIN\_FRAMES), FRAME\_FACTOR)

&#x20;               max\_frames = floor\_by\_factor(ele.get("max\_frames", min(FPS\_MAX\_FRAMES, total\_frames)), FRAME\_FACTOR)

&#x20;               duration = total\_frames / video\_fps if video\_fps != 0 else 0

&#x20;               if duration-int(duration)>(1/fps):

&#x20;                   total\_frames = math.ceil(duration \* video\_fps)

&#x20;               else:

&#x20;                   total\_frames = math.ceil(int(duration)\*video\_fps)

&#x20;               nframes = total\_frames / video\_fps \* fps

&#x20;               if nframes > total\_frames:

&#x20;                   logger.warning(f"smart\_nframes: nframes\[{nframes}] > total\_frames\[{total\_frames}]")

&#x20;               nframes = int(min(min(max(nframes, min\_frames), max\_frames), total\_frames))

&#x20;               if not (FRAME\_FACTOR <= nframes and nframes <= total\_frames):

&#x20;                   raise ValueError(f"nframes should in interval \[{FRAME\_FACTOR}, {total\_frames}], but got {nframes}.")

&#x20;           

&#x20;               return nframes

&#x20;           

&#x20;           def get\_video(video\_path):

&#x20;               # Get video information.

&#x20;               cap = cv2.VideoCapture(video\_path)

&#x20;           

&#x20;               frame\_width = int(cap.get(cv2.CAP\_PROP\_FRAME\_WIDTH))

&#x20;               # Get video height.

&#x20;               frame\_height = int(cap.get(cv2.CAP\_PROP\_FRAME\_HEIGHT))

&#x20;               total\_frames = int(cap.get(cv2.CAP\_PROP\_FRAME\_COUNT))

&#x20;           

&#x20;               video\_fps = cap.get(cv2.CAP\_PROP\_FPS)

&#x20;               return frame\_height, frame\_width, total\_frames, video\_fps

&#x20;           

&#x20;           def smart\_resize(ele, path, factor=IMAGE\_FACTOR):

&#x20;               # Get the original width and height of the video.

&#x20;               height, width, total\_frames, video\_fps = get\_video(path)

&#x20;               # Minimum pixel count for video frames.

&#x20;               min\_pixels = VIDEO\_MIN\_PIXELS

&#x20;               total\_pixels = VIDEO\_TOTAL\_PIXELS

&#x20;               # Number of extracted video frames.

&#x20;               nframes = smart\_nframes(ele, total\_frames, video\_fps)

&#x20;               max\_pixels = max(min(VIDEO\_MAX\_PIXELS, total\_pixels / nframes \* FRAME\_FACTOR),int(min\_pixels \* 1.05))

&#x20;           

&#x20;               # The aspect ratio of the video should not exceed 200:1 or 1:200.

&#x20;               if max(height, width) / min(height, width) > MAX\_RATIO:

&#x20;                   raise ValueError(

&#x20;                       f"absolute aspect ratio must be smaller than {MAX\_RATIO}, got {max(height, width) / min(height, width)}"

&#x20;                   )

&#x20;           

&#x20;               h\_bar = max(factor, round\_by\_factor(height, factor))

&#x20;               w\_bar = max(factor, round\_by\_factor(width, factor))

&#x20;               if h\_bar \* w\_bar > max\_pixels:

&#x20;                   beta = math.sqrt((height \* width) / max\_pixels)

&#x20;                   h\_bar = floor\_by\_factor(height / beta, factor)

&#x20;                   w\_bar = floor\_by\_factor(width / beta, factor)

&#x20;               elif h\_bar \* w\_bar < min\_pixels:

&#x20;                   beta = math.sqrt(min\_pixels / (height \* width))

&#x20;                   h\_bar = ceil\_by\_factor(height \* beta, factor)

&#x20;                   w\_bar = ceil\_by\_factor(width \* beta, factor)

&#x20;               return h\_bar, w\_bar

&#x20;           

&#x20;           

&#x20;           def token\_calculate(video\_path, fps):

&#x20;               # Pass the video path and the fps parameter for frame extraction.

&#x20;               messages = \[{"content": \[{"video": video\_path, "fps": fps}]}]

&#x20;               vision\_infos = extract\_vision\_info(messages)\[0]

&#x20;           

&#x20;               resized\_height, resized\_width = smart\_resize(vision\_infos, video\_path)

&#x20;           

&#x20;               height, width, total\_frames, video\_fps = get\_video(video\_path)

&#x20;               num\_frames = smart\_nframes(vision\_infos, total\_frames, video\_fps)

&#x20;               print(f"Original video dimensions: {height}\*{width}, Model input dimensions: {resized\_height}\*{resized\_width}, Total video frames: {total\_frames}, Total frames extracted when fps is {fps}: {num\_frames}", end=", ")

&#x20;               video\_token = int(math.ceil(num\_frames / 2) \* resized\_height / 32 \* resized\_width / 32)

&#x20;               video\_token += 2   # The system automatically adds the <|vision\_bos|> and <|vision\_eos|> visual markers (1 Token each).

&#x20;               return video\_token

&#x20;           

&#x20;           

&#x20;           video\_token = token\_calculate("xxx/test.mp4", 1)

&#x20;           print("Video Tokens:", video\_token)

&#x20;           ```

&#x20;           

&#x20;       -   \*\*Image list:\*\*

&#x20;           

&#x20;           If you provide the video as a list of images, the frame extraction step is already complete. Use the following code to calculate the number of tokens consumed by the image list by providing the path to a representative frame and the total number of frames:

&#x20;           

&#x20;           ```

&#x20;           # Before use, install: pip install Pillow

&#x20;           import math

&#x20;           import os

&#x20;           import logging

&#x20;           from typing import Tuple

&#x20;           from PIL import Image

&#x20;           

&#x20;           logger = logging.getLogger(\_\_name\_\_)

&#x20;           

&#x20;           # ==================== Constant definitions ====================

&#x20;           FRAME\_FACTOR = 2

&#x20;           # For models such as Qwen3.5, Qwen3-VL, qwen-vl-max-0813, qwen-vl-plus-0815, and qwen-vl-plus-0710, the scaling factor is 32.

&#x20;           IMAGE\_FACTOR = 32

&#x20;           

&#x20;           # For other models, the scaling factor is 28.

&#x20;           # IMAGE\_FACTOR = 28

&#x20;           

&#x20;           # Constants for token calculation.

&#x20;           TOKEN\_DIVISOR = 32  # Divisor for token calculation.

&#x20;           VISION\_SPECIAL\_TOKENS = 2  # <|vision\_bos|> and <|vision\_eos|> markers.

&#x20;           

&#x20;           # Maximum aspect ratio of video frames.

&#x20;           MAX\_RATIO = 200

&#x20;           # Minimum pixel count for video frames.

&#x20;           VIDEO\_MIN\_PIXELS = 4 \* 32 \* 32

&#x20;           # Maximum pixel count for video frames. The value is 640 \* 32 \* 32 for the Qwen3-VL-Plus model and 768 \* 32 \* 32 for other models.

&#x20;           VIDEO\_MAX\_PIXELS = 640 \* 32 \* 32

&#x20;           

&#x20;           # Maximum total pixels for video input. This value is 131072 \* 32 \* 32 for the Qwen3-VL-Plus model and 65536 \* 32 \* 32 for other models.

&#x20;           VIDEO\_TOTAL\_PIXELS = int(float(os.environ.get('VIDEO\_MAX\_PIXELS', 131072 \* 32 \* 32)))

&#x20;           

&#x20;           def round\_by\_factor(number: int, factor: int) -> int:

&#x20;               """Returns the integer closest to 'number' that is divisible by 'factor'."""

&#x20;               return round(number / factor) \* factor

&#x20;           

&#x20;           def ceil\_by\_factor(number: int, factor: int) -> int:

&#x20;               """Returns the smallest integer greater than or equal to 'number' and divisible by 'factor'."""

&#x20;               return math.ceil(number / factor) \* factor

&#x20;           

&#x20;           def floor\_by\_factor(number: int, factor: int) -> int:

&#x20;               """Returns the largest integer less than or equal to 'number' and divisible by 'factor'."""

&#x20;               return math.floor(number / factor) \* factor

&#x20;           

&#x20;           

&#x20;           def get\_image\_size(image\_path: str) -> Tuple\[int, int]:

&#x20;               if not os.path.exists(image\_path):

&#x20;                   raise FileNotFoundError(f"Image file not found: {image\_path}")

&#x20;           

&#x20;               try:

&#x20;                   image = Image.open(image\_path)

&#x20;                   height = image.height

&#x20;                   width = image.width

&#x20;                   image.close()  # Close the file promptly.

&#x20;                   return height, width

&#x20;               except Exception as e:

&#x20;                   raise ValueError(f"Cannot read the image file {image\_path}: {str(e)}")

&#x20;           

&#x20;           def smart\_resize(height: int, width: int, nframes: int, factor: int = IMAGE\_FACTOR) -> Tuple\[int, int]:

&#x20;               """

&#x20;               Calculates the dimensions of the image after scaling.

&#x20;           

&#x20;               Args:

&#x20;                   height: The original image height.

&#x20;                   width: The original image width.

&#x20;                   nframes: The number of video frames.

&#x20;                   factor: The scaling factor. The default is IMAGE\_FACTOR.

&#x20;           

&#x20;               Returns:

&#x20;                   (resized\_height, resized\_width): The resized height and width.

&#x20;           

&#x20;               Raises:

&#x20;                   ValueError: The aspect ratio exceeds the limit.

&#x20;               """

&#x20;               # Minimum pixel count for video frames.

&#x20;               min\_pixels = VIDEO\_MIN\_PIXELS

&#x20;               total\_pixels = VIDEO\_TOTAL\_PIXELS

&#x20;               # Number of extracted video frames.

&#x20;               max\_pixels = max(min(VIDEO\_MAX\_PIXELS, total\_pixels / nframes \* FRAME\_FACTOR), int(min\_pixels \* 1.05))

&#x20;           

&#x20;               # The aspect ratio of the image cannot exceed 200:1 or 1:200.

&#x20;               aspect\_ratio = max(height, width) / min(height, width)

&#x20;               if aspect\_ratio > MAX\_RATIO:

&#x20;                   raise ValueError(

&#x20;                       f"The aspect ratio of the image must be less than {MAX\_RATIO}:1. The current ratio is {aspect\_ratio:.2f}:1."

&#x20;                   )

&#x20;           

&#x20;               h\_bar = max(factor, round\_by\_factor(height, factor))

&#x20;               w\_bar = max(factor, round\_by\_factor(width, factor))

&#x20;               if h\_bar \* w\_bar > max\_pixels:

&#x20;                   beta = math.sqrt((height \* width) / max\_pixels)

&#x20;                   h\_bar = floor\_by\_factor(height / beta, factor)

&#x20;                   w\_bar = floor\_by\_factor(width / beta, factor)

&#x20;               elif h\_bar \* w\_bar < min\_pixels:

&#x20;                   beta = math.sqrt(min\_pixels / (height \* width))

&#x20;                   h\_bar = ceil\_by\_factor(height \* beta, factor)

&#x20;                   w\_bar = ceil\_by\_factor(width \* beta, factor)

&#x20;               return h\_bar, w\_bar

&#x20;           

&#x20;           

&#x20;           def calculate\_video\_tokens(image\_path: str, nframes: int = 1, factor: int = IMAGE\_FACTOR, verbose: bool = True) -> int:

&#x20;               """

&#x20;           

&#x20;               Args:

&#x20;                   image\_path: The path to a representative video frame file.

&#x20;                   nframes: The number of video frames.

&#x20;                   factor: The scaling factor. The default is IMAGE\_FACTOR.

&#x20;                   verbose: Specifies whether to print detailed information.

&#x20;           

&#x20;               Returns:

&#x20;                   The total number of tokens consumed.

&#x20;           

&#x20;               Raises:

&#x20;                   FileNotFoundError: The file does not exist.

&#x20;                   ValueError: The file format is invalid or the aspect ratio exceeds the limit.

&#x20;               """

&#x20;               # Get the original image dimensions (read only once).

&#x20;               height, width = get\_image\_size(image\_path)

&#x20;           

&#x20;               # Calculate the resized dimensions.

&#x20;               resized\_height, resized\_width = smart\_resize(height, width, nframes, factor)

&#x20;           

&#x20;               # Calculate the number of tokens.

&#x20;               video\_token = int(

&#x20;                   math.ceil(nframes / 2) \*

&#x20;                   (resized\_height / TOKEN\_DIVISOR) \*

&#x20;                   (resized\_width / TOKEN\_DIVISOR)

&#x20;               )

&#x20;               # Add visual marker tokens (<|vision\_bos|> and <|vision\_eos|>).

&#x20;               video\_token += VISION\_SPECIAL\_TOKENS

&#x20;           

&#x20;               if verbose:

&#x20;                   print(f"Original video frame dimensions: {height}×{width}, model input dimensions: {resized\_height}×{resized\_width}, ", end="")

&#x20;           

&#x20;               return video\_token

&#x20;           

&#x20;           if \_\_name\_\_ == "\_\_main\_\_":

&#x20;               try:

&#x20;                   video\_token = calculate\_video\_tokens("xxx/test.jpg", nframes=30)

&#x20;                   print(f"Video Tokens: {video\_token}\\n")

&#x20;               except Exception as e:

&#x20;                   print(f"Error: {str(e)}\\n")

&#x20;           ```

&#x20;           

&#x20;       



\-   \*\*View bills:\*\* You can view your bills or top up your account on the \[Expenses and Costs](https://usercenter2-intl.console.alibabacloud.com/billing#/account/overview) page in the Alibaba Cloud console.

&#x20;   

\-   \*\*Rate limiting:\*\* For visual understanding model rate limits, see \[Rate limits](/help/en/model-studio/rate-limit).

&#x20;   

\-   \*\*Free quota\*\* \*\*(Singapore only)\*\*: Visual understanding models offer a free quota of 1 million tokens, valid for 90 days, starting from the date you activate Model Studio or your model request is approved.

&#x20;   



\## API reference



For the input and output parameters of the visual understanding model, see \[Qwen](/help/en/model-studio/qwen-api-reference/).



\## \*\*FAQ\*\*



\### \*\*File\*\* upload method



Choose the upload method that best suits your SDK type, file size, and network stability.



| \*\*Type\*\* | \*\*Size\*\* | \*\*DashScope SDK (Python, Java)\*\* | \*\*OpenAI compatible / DashScope HTTP\*\* |

| --- | --- | --- | --- |

| Image | 7 MB to 10 MB | Provide the local path | Public URLs only. We recommend using \[Object Storage Service (OSS)](https://www.alibabacloud.com/zh/product/object-storage-service?\_p\_lc=1). |

| Less than 7 MB | Provide the local path | Base64 encoding |

| Video | Greater than 100 MB | Only public URLs are supported. We recommend using \[Object Storage Service (OSS)](https://www.alibabacloud.com/zh/product/object-storage-service?\_p\_lc=1). | Public URLs only. We recommend using \[Object Storage Service (OSS)](https://www.alibabacloud.com/zh/product/object-storage-service?\_p\_lc=1). |

| 7 MB to 100 MB | Provide the local path | Public URLs only. We recommend using \[Object Storage Service (OSS)](https://www.alibabacloud.com/zh/product/object-storage-service?\_p\_lc=1). |

| Less than 7 MB | Provide the local path | Base64 encoding |



> Since Base64 encoding increases the file size, the original file must be smaller than 7 MB.



> Use Base64 encoding or a local path to prevent server-side download timeouts and improve stability.



\### \*\*Image\*\* and video compression



Input files for visual understanding models have size limits. Use the following methods to compress them.



\*\*Image compression methods\*\*



\-   Online tools: Use services like \[CompressJPEG](https://compressjpeg.com/zh/).

&#x20;   

\-   Local software: Adjust export quality using tools like Photoshop.

&#x20;   

\-   Code implementation:

&#x20;   

&#x20;   ```

&#x20;   # pip install pillow

&#x20;   

&#x20;   from PIL import Image

&#x20;   def compress\_image(input\_path, output\_path, quality=85):

&#x20;       with Image.open(input\_path) as img:

&#x20;           img.save(output\_path, "JPEG", optimize=True, quality=quality)

&#x20;   

&#x20;   # Pass a local image.

&#x20;   compress\_image("/xxx/before-large.jpeg","/xxx/after-min.jpeg")

&#x20;   ```

&#x20;   



\*\*Video compression methods\*\*



\-   Online tools: Use services like \[FreeConvert](https://www.freeconvert.com/zh).

&#x20;   

\-   Local software: Use tools like \[HandBrake](https://handbrake.fr/).

&#x20;   

\-   Code implementation: Use the FFmpeg tool. See the \[FFmpeg official website](https://ffmpeg.org/download.html).

&#x20;   

&#x20;   ```

&#x20;   # Basic conversion command

&#x20;   # -i: Specifies the input file path. Example: input.mp4

&#x20;   # -vcodec: Specifies the video encoder. Common values include libx264 (recommended for general use) and libx265 (higher compression rate).

&#x20;   # -crf: Controls the video quality. The value range is 18 to 28. A lower value results in higher quality and a larger file size.

&#x20;   # -preset: Controls the balance between encoding speed and compression efficiency. Common values include slow, fast, and faster.

&#x20;   # -y: Overwrites an existing file (no value required).

&#x20;   # output.mp4: Specifies the output file path.

&#x20;   

&#x20;   ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset slow output.mp4

&#x20;   ```

&#x20;   



\### \*\*Drawing\*\* bounding boxes



After the visual understanding model generates object localization results, you can use the following code to draw the bounding boxes and their labels on the original image.



\-   Qwen2.5-VL: Returns absolute pixel coordinates, relative to the top-left corner of the scaled image. To draw the bounding boxes, see the code in \[qwen2\\\_5\\\_vl\\\_2d.py](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251103/bgyust/qwen2\_5-vl-2d.py).

&#x20;   

\-   Qwen3-VL: Returns relative coordinates normalized to a `\[0, 999]` range. To draw the bounding boxes, see the code in \[qwen3\\\_vl\\\_2d.py](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251103/wpucdo/qwen3-vl-2d.py) (for 2D localization) or \[qwen3\\\_vl\\\_3d.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251103/mjjrka/qwen3\_vl\_3d.zip) (for 3D localization).

&#x20;   



\## Error codes



If the model call fails and returns an error message, see \[Error messages](/help/en/model-studio/error-code) for resolution.

