\# The 4 Things Qwen-3’s Chat Template Teaches Us

\# What is a Chat Template?

A chat template defines how conversations between users and models are structured and formatted. The template acts as a translator, converting a human-readable conversation:



&#x20; \[

&#x20;   { role: "user", content: "Hi there!" },

&#x20;   { role: "assistant", content: "Hi there, how can I help you today?" },

&#x20;   { role: "user", content: "I'm looking for a new pair of shoes." },

&#x20; ]



into a model friendly format:



<|im\_start|>user

Hi there!<|im\_end|>

<|im\_start|>assistant

Hi there, how can I help you today?<|im\_end|>

<|im\_start|>user

I'm looking for a new pair of shoes.<|im\_end|>

<|im\_start|>assistant

<think>



</think>



Chat Template for Qwen/Qwen3-235B-A22B:

{%- if tools %}

&#x20;   {{- '<|im\_start|>system\\n' }}

&#x20;   {%- if messages\[0].role == 'system' %}

&#x20;       {{- messages\[0].content + '\\n\\n' }}

&#x20;   {%- endif %}

&#x20;   {{- "# Tools\\n\\nYou may call one or more functions to assist with the user query.\\n\\nYou are provided with function signatures within <tools></tools> XML tags:\\n<tools>" }}

&#x20;   {%- for tool in tools %}

&#x20;       {{- "\\n" }}

&#x20;       {{- tool | tojson }}

&#x20;   {%- endfor %}

&#x20;   {{- "\\n</tools>\\n\\nFor each function call, return a json object with function name and arguments within <tool\_call></tool\_call> XML tags:\\n<tool\_call>\\n{\\"name\\": <function-name>, \\"arguments\\": <args-json-object>}\\n</tool\_call><|im\_end|>\\n" }}

{%- else %}

&#x20;   {%- if messages\[0].role == 'system' %}

&#x20;       {{- '<|im\_start|>system\\n' + messages\[0].content + '<|im\_end|>\\n' }}

&#x20;   {%- endif %}

{%- endif %}

{%- set ns = namespace(multi\_step\_tool=true, last\_query\_index=messages|length - 1) %}

{%- for message in messages\[::-1] %}

&#x20;   {%- set index = (messages|length - 1) - loop.index0 %}

&#x20;   {%- if ns.multi\_step\_tool and message.role == "user" and message.content is string and not(message.content.startswith('<tool\_response>') and message.content.endswith('</tool\_response>')) %}

&#x20;       {%- set ns.multi\_step\_tool = false %}

&#x20;       {%- set ns.last\_query\_index = index %}

&#x20;   {%- endif %}

{%- endfor %}

{%- for message in messages %}

&#x20;   {%- if message.content is string %}

&#x20;       {%- set content = message.content %}

&#x20;   {%- else %}

&#x20;       {%- set content = '' %}

&#x20;   {%- endif %}

&#x20;   {%- if (message.role == "user") or (message.role == "system" and not loop.first) %}

&#x20;       {{- '<|im\_start|>' + message.role + '\\n' + content + '<|im\_end|>' + '\\n' }}

&#x20;   {%- elif message.role == "assistant" %}

&#x20;       {%- set reasoning\_content = '' %}

&#x20;       {%- if message.reasoning\_content is string %}

&#x20;           {%- set reasoning\_content = message.reasoning\_content %}

&#x20;       {%- else %}

&#x20;           {%- if '</think>' in content %}

&#x20;               {%- set reasoning\_content = content.split('</think>')\[0].rstrip('\\n').split('<think>')\[-1].lstrip('\\n') %}

&#x20;               {%- set content = content.split('</think>')\[-1].lstrip('\\n') %}

&#x20;           {%- endif %}

&#x20;       {%- endif %}

&#x20;       {%- if loop.index0 > ns.last\_query\_index %}

&#x20;           {%- if loop.last or (not loop.last and reasoning\_content) %}

&#x20;               {{- '<|im\_start|>' + message.role + '\\n<think>\\n' + reasoning\_content.strip('\\n') + '\\n</think>\\n\\n' + content.lstrip('\\n') }}

&#x20;           {%- else %}

&#x20;               {{- '<|im\_start|>' + message.role + '\\n' + content }}

&#x20;           {%- endif %}

&#x20;       {%- else %}

&#x20;           {{- '<|im\_start|>' + message.role + '\\n' + content }}

&#x20;       {%- endif %}

&#x20;       {%- if message.tool\_calls %}

&#x20;           {%- for tool\_call in message.tool\_calls %}

&#x20;               {%- if (loop.first and content) or (not loop.first) %}

&#x20;                   {{- '\\n' }}

&#x20;               {%- endif %}

&#x20;               {%- if tool\_call.function %}

&#x20;                   {%- set tool\_call = tool\_call.function %}

&#x20;               {%- endif %}

&#x20;               {{- '<tool\_call>\\n{"name": "' }}

&#x20;               {{- tool\_call.name }}

&#x20;               {{- '", "arguments": ' }}

&#x20;               {%- if tool\_call.arguments is string %}

&#x20;                   {{- tool\_call.arguments }}

&#x20;               {%- else %}

&#x20;                   {{- tool\_call.arguments | tojson }}

&#x20;               {%- endif %}

&#x20;               {{- '}\\n</tool\_call>' }}

&#x20;           {%- endfor %}

&#x20;       {%- endif %}

&#x20;       {{- '<|im\_end|>\\n' }}

&#x20;   {%- elif message.role == "tool" %}

&#x20;       {%- if loop.first or (messages\[loop.index0 - 1].role != "tool") %}

&#x20;           {{- '<|im\_start|>user' }}

&#x20;       {%- endif %}

&#x20;       {{- '\\n<tool\_response>\\n' }}

&#x20;       {{- content }}

&#x20;       {{- '\\n</tool\_response>' }}

&#x20;       {%- if loop.last or (messages\[loop.index0 + 1].role != "tool") %}

&#x20;           {{- '<|im\_end|>\\n' }}

&#x20;       {%- endif %}

&#x20;   {%- endif %}

{%- endfor %}

{%- if add\_generation\_prompt %}

&#x20;   {{- '<|im\_start|>assistant\\n' }}

&#x20;   {%- if enable\_thinking is defined and enable\_thinking is false %}

&#x20;       {{- '<think>\\n\\n</think>\\n\\n' }}

&#x20;   {%- endif %}

{%- endif %}

# 1. Reasoning doesn't have to be forced

and you can make it optional via a simple prefill...



Qwen-3 is unique in its ability to toggle reasoning via the enable\_thinking flag. When set to false, the template inserts an empty <think></think> pair, telling the model to skip step‑by‑step thoughts. Earlier models baked the <think> tag into every generation, forcing chain‑of‑thought whether you wanted it or not.



{# Qwen-3 #}

{%- if enable\_thinking is defined and enable\_thinking is false %}

&#x20;   {{- '<think>\\n\\n</think>\\n\\n' }}

{%- endif %}



QwQ for example, forces reasoning in every conversation.



{# QwQ #}

{%- if add\_generation\_prompt %}

&#x20;   {{- '<|im\_start|>assistant\\n<think>\\n' }}

{%- endif %}



If the enable\_thinking is true, the model is able to decide whether to think or not.



You can test test out the template with the following code:



import { Template } from "@huggingface/jinja";

import { downloadFile } from "@huggingface/hub";



const HF\_TOKEN = process.env.HF\_TOKEN;



const file = await downloadFile({

&#x20; repo: "Qwen/Qwen3-235B-A22B",

&#x20; path: "tokenizer\_config.json",

&#x20; accessToken: HF\_TOKEN,

});

const config = await file!.json();



const template = new Template(config.chat\_template);

const result = template.render({

&#x20; messages,

&#x20; add\_generation\_prompt: true,

&#x20; enable\_thinking: false,  

&#x20; bos\_token: config.bos\_token,

&#x20; eos\_token: config.eos\_token,

});



\# 2. Context Management Should be Dynamic

Qwen-3 utilizes a rolling checkpoint system, intelligently preserving or pruning reasoning blocks to maintain relevant context. Older models discarded reasoning prematurely to save tokens.



Qwen-3 introduces a "rolling checkpoint" by traversing the message list in reverse to find the latest user turn that wasn’t a tool call. For any assistant replies after that index it keeps the full <think> blocks; everything earlier is stripped out.



Why this matters:



Keeps the active plan visible during a multi‑step tool call.

Supports nested tool workflows without losing context.

Saves tokens by pruning thoughts the model no longer needs.

Prevents "stale" reasoning from bleeding into new tasks.

# 3. Tool Arguments Need Better Serialization

Before, every tool\_call.arguments field was piped through | tojson, even if it was already a JSON‑encoded string—risking double‑escaping. Qwen‑3 checks the type first and only serializes when necessary.



{# Qwen3 #}

{%- if tool\_call.arguments is string %}

&#x20;   {{- tool\_call.arguments }}

{%- else %}

&#x20;   {{- tool\_call.arguments | tojson }}

{%- endif %}



\# 4. There's No Need for a Default System Prompt

Like many models, the Qwen‑2.5 series has a default system prompt.



You are Qwen, created by Alibaba Cloud. You are a helpful assistant.



This is pretty common as it helps models respond to user questions like "Who are you?"



Qwen-3 and QwQ ship without this default system prompt. Despite this, the model can still accurately identify its creator if you ask it.



Conclusion

Qwen-3 shows us that through the chat\_template we can provide better flexibility, smarter context handling, and improved tool interaction. These improvements not only improve capabilities, but also make agentic workflows more reliable and efficent.







