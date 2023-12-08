---
pretty_name: PhoGPT
extra_gated_prompt: 
 Please read the [PhoGPT License Agreement](https://github.com/VinAIResearch/PhoGPT/blob/main/LICENSE) before accepting it.
extra_gated_fields:
 Name: text
 Email: text
 Affiliation: text
 Country: text
 I accept the PhoGPT License Agreement: checkbox
---




# PhoGPT: Generative Pre-training for Vietnamese 

We open-source a state-of-the-art 7.5B-parameter generative model series named PhoGPT for Vietnamese, which includes the base pre-trained monolingual model **PhoGPT-7B5** and its instruction-following variant **PhoGPT-7B5-Instruct**. More details about the general architecture and experimental results of PhoGPT can be found in our [technical report](https://arxiv.org/abs/2311.02945):

```
@article{PhoGPT,
title     = {{PhoGPT: Generative Pre-training for Vietnamese}},
author    = {Dat Quoc Nguyen and Linh The Nguyen and Chi Tran and Dung Ngoc Nguyen and Nhung Nguyen and Thien Huu Nguyen and Dinh Phung and Hung Bui},
journal   = {arXiv preprint},
volume    = {arXiv:2311.02945},
year      = {2023}
}
```

For further information or requests, please go to [PhoGPT's homepage](https://github.com/VinAIResearch/PhoGPT)!

## Model download <a name="download"></a>

Model | Download 
---|---
`vinai/PhoGPT-7B5` | https://huggingface.co/vinai/PhoGPT-7B5
`vinai/PhoGPT-7B5-Instruct` | https://huggingface.co/vinai/PhoGPT-7B5-Instruct


## Run the model <a name="inference"></a>

### with `transformers`

```python
from transformers import AutoConfig, AutoModelForCausalLM, AutoTokenizer  
  
model_path = "vinai/PhoGPT-7B5-Instruct"  
  
config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)  
config.init_device = "cuda"
# config.attn_config['attn_impl'] = 'triton' # Enable if "triton" installed!
  
model = AutoModelForCausalLM.from_pretrained(  
    model_path, config=config, torch_dtype=torch.bfloat16, trust_remote_code=True  
)
# If your GPU does not support bfloat16:
# model = AutoModelForCausalLM.from_pretrained(model_path, config=config, torch_dtype=torch.float16, trust_remote_code=True)
model.eval()  
  
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)  
  
PROMPT = "### Câu hỏi:\n{instruction}\n\n### Trả lời:"  
  
input_prompt = PROMPT.format_map(  
    {"instruction": "Làm thế nào để cải thiện kỹ năng quản lý thời gian?"}  
)  
  
input_ids = tokenizer(input_prompt, return_tensors="pt")  
  
outputs = model.generate(  
    inputs=input_ids["input_ids"].to("cuda"),  
    attention_mask=input_ids["attention_mask"].to("cuda"),  
    do_sample=True,  
    temperature=1.0,  
    top_k=50,  
    top_p=0.9,  
    max_new_tokens=1024,  
    eos_token_id=tokenizer.eos_token_id,  
    pad_token_id=tokenizer.pad_token_id  
)  
  
response = tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]  
response = response.split("### Trả lời:")[1]
```

### with vLLM

PhoGPT can also run with [vLLM](https://github.com/vllm-project/vllm). See [vLLM docs](https://vllm.readthedocs.io/en/latest/getting_started/quickstart.html) for more details. 

## Fine-tuning the model <a name="finetuning"></a>

See [llm-foundry docs](https://github.com/mosaicml/llm-foundry/blob/main/scripts/train/README.md#llmfinetuning) for more details. To fully fine-tune `vinai/PhoGPT-7B5` or `vinai/PhoGPT-7B5-Instruct` on a single GPU A100 with 40GB memory, it is advisable to employ the `decoupled_lionw` optimizer with a `device_train_microbatch_size` set to 1.

## Limitations <a name="limitations"></a>

PhoGPT has certain limitations. For example, it is not good at tasks involving reasoning, coding or mathematics. PhoGPT may sometimes generate harmful, hate speech, biased responses, or answer unsafe questions. Users should be cautious when interacting with PhoGPT that can produce factually incorrect output.

## [License](https://github.com/VinAIResearch/PhoGPT/blob/main/LICENSE)