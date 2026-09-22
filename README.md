# Stable Diffusion API — Python client

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE) [![Hosted on Synexa](https://img.shields.io/badge/hosted%20on-Synexa-6366f1.svg)](https://synexa.ai/explore/stability-ai/stable-diffusion?utm_source=github&utm_medium=ugc&utm_campaign=stable-diffusion-dev&utm_content=readme-badge&utm_term=tier-a)

Stable Diffusion is the latent diffusion model from CompVis, Runway and Stability AI that made open text-to-image generation practical on ordinary hardware in 2022, and SDXL is its higher-resolution successor. This package is a Python client for the Stable Diffusion API hosted on Synexa: one `pip install` covers the classic `stability-ai/stable-diffusion` endpoint, `stability-ai/sdxl` with image-to-image, and ByteDance's 4-step `sdxl-lightning-4step`, all through the same `run()` call.

The client gives you a blocking `run()` that returns image URLs, a submit-and-poll mode, webhook delivery on completion and typed errors. Its only dependency is `httpx`. It is for developers who want Stable Diffusion in an application, a batch job or a notebook without installing diffusers, downloading checkpoints or keeping a GPU warm.

> **Try it now:** [https://synexa.ai/explore/stability-ai/stable-diffusion](https://synexa.ai/explore/stability-ai/stable-diffusion?utm_source=github&utm_medium=ugc&utm_campaign=stable-diffusion-dev&utm_content=readme-top&utm_term=tier-a) — the hosted model behind this client. New accounts get a free trial credit.

## Contents

- [Why this client](#why-this-client)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Hosted models](#hosted-models)
- [Parameters](#parameters)
- [Advanced usage](#advanced-usage)
- [About Stable Diffusion](#about-stable-diffusion)
- [Use cases](#use-cases)
- [FAQ](#faq)
- [License](#license)

## Why this client

- **SDXL wants a real GPU.** SD 1.x runs in a few gigabytes of VRAM, but SDXL at 1024×1024 is comfortable only from roughly 8–12 GB, which excludes most laptops and every serverless runtime. The hosted endpoints run on datacenter cards; you call HTTPS.
- **No environment to maintain.** A local setup means PyTorch, diffusers or a WebUI, the right CUDA build and multi-gigabyte checkpoints, all of which drift between releases. Here it is `pip install` and an API key.
- **No cold start.** Loading a checkpoint into GPU memory takes tens of seconds to minutes on a fresh instance; the hosted models stay resident.
- **Fractions of a cent per image.** `stable-diffusion` is $0.0007 per run, `sdxl-lightning-4step` is $0.001 and `sdxl` is $0.002, with no hourly charge: a thousand images cost between 70 cents and two dollars.

## Installation

```bash
pip install git+https://github.com/stable-diffusion-dev/stable-diffusion-api.git
```

Then set your API key (create one at [synexa.ai](https://synexa.ai?utm_source=github&utm_medium=ugc&utm_campaign=stable-diffusion-dev&utm_content=readme-apikey&utm_term=tier-a)):

```bash
export SYNEXA_API_KEY="sk-..."
```

## Quickstart

```python
import stable_diffusion_api

output = stable_diffusion_api.run({
    "prompt": "an astronaut riding a horse on mars, hd, dramatic lighting"
})
print(output)   # URL(s) of the generated result
```

Or with an explicit client:

```python
from stable_diffusion_api import Client

client = Client(api_key="sk-...")
output = client.run({"prompt": "an astronaut riding a horse on mars, hd, dramatic lighting"})
```

## Hosted models

| Model | Category | What it does | Price / run |
|---|---|---|---|
| [`stability-ai/stable-diffusion`](https://synexa.ai/explore/stability-ai/stable-diffusion?utm_source=github&utm_medium=ugc&utm_campaign=stable-diffusion-dev&utm_content=readme-models&utm_term=tier-a) | text-to-image | A latent text-to-image diffusion model capable of generating photo-realistic images given any text input | $0.0007 |
| [`stability-ai/sdxl`](https://synexa.ai/explore/stability-ai/sdxl?utm_source=github&utm_medium=ugc&utm_campaign=stable-diffusion-dev&utm_content=readme-models&utm_term=tier-a) | text-to-image | A text-to-image generative AI model that creates beautiful images | $0.002 |
| [`bytedance/sdxl-lightning-4step`](https://synexa.ai/explore/bytedance/sdxl-lightning-4step?utm_source=github&utm_medium=ugc&utm_campaign=stable-diffusion-dev&utm_content=readme-models&utm_term=tier-a) | text-to-image | SDXL-Lightning by ByteDance: a fast text-to-image model that makes high-quality images in 4 steps | $0.001 |

The default model is **`stability-ai/stable-diffusion`**; pass `model="owner/name"` to `run()` to use another one from the table.

## Parameters

### `stability-ai/stable-diffusion`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `seed` | integer | no | `random` | — | Random seed. Leave blank to randomize the seed |
| `width` | integer | no | `768` | 64, 1024 | Width of generated image in pixels. Needs to be a multiple of 64 |
| `height` | integer | no | `768` | 64, 1024 | Height of generated image in pixels. Needs to be a multiple of 64 |
| `prompt` | string | yes | `an astronaut riding a horse on mars, hd,…` | — | Input prompt |
| `scheduler` | string | no | `K_EULER` | DDIM, K_EULER, DPMSolverMultistep, K_EULER_ANCESTRAL, PND… | Choose a scheduler. |
| `num_outputs` | integer | no | `1` | 1, 4 | Number of images to generate. |
| `guidance_scale` | number | no | `7.5` | 1, 20 | Scale for classifier-free guidance |
| `negative_prompt` | string | no | `worst quality, low quality` | — | Specify things to not see in the output |
| `num_inference_steps` | integer | no | `50` | 1, 500 | Number of denoising steps |

### `stability-ai/sdxl`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `seed` | integer | no | `random` | — | Random seed. Leave blank to randomize the seed |
| `width` | integer | no | `1024` | 256, 1440 | Width of output image |
| `height` | integer | no | `1024` | 256, 1440 | Height of output image |
| `prompt` | string | yes | `An astronaut riding a rainbow unicorn, c…` | — | Input prompt |
| `cfg_scale` | number | no | `6` | 1, 10 | Scale for classifier-free guidance |
| `input_image` | file | no | — | — | Input image to start generating from |
| `negative_prompt` | string | no | `worst quality, low quality, monochrome, …` | — | Input Negative Prompt |
| `denoising_strength` | number | no | `9` | 1, 10 | How much noise is added to an image before the sampling steps |
| `num_inference_steps` | integer | no | `60` | 1, 100 | Number of denoising steps |

### `bytedance/sdxl-lightning-4step`

| Field | Type | Required | Default | Range | Description |
|---|---|---|---|---|---|
| `seed` | integer | no | `random` | — | Random seed. Leave blank to randomize the seed |
| `width` | integer | no | `1024` | 256, 1280 | Width of output image. Recommended 1024 or 1280 |
| `height` | integer | no | `1024` | 256, 1280 | Height of output image. Recommended 1024 or 1280 |
| `prompt` | string | yes | `self-portrait of a woman, lightning in t…` | — | Input prompt |
| `scheduler` | string | no | `K_EULER` | K_EULER, DDIM, DPMSolverMultistep, HeunDiscrete, KarrasDP… | scheduler |
| `num_outputs` | integer | no | `1` | 1, 4 | Number of images to output. |
| `guidance_scale` | integer | no | `0` | 0, 50 | Scale for classifier-free guidance |
| `negative_prompt` | string | no | `worst quality, low quality` | — | Negative Input prompt |
| `num_inference_steps` | integer | no | `4` | 1, 10 | Number of denoising steps. 4 for best results |
| `disable_safety_checker` | boolean | no | `False` | — | Disable safety checker for generated images |

## Advanced usage

**Submit without blocking, then poll:**

```python
prediction = client.run(input, wait=False)      # returns immediately
prediction = client.wait(prediction, timeout=300)
print(prediction["output"])
```

**Webhook on completion:**

```python
client.run(input, wait=False, webhook="https://your-app.example/hooks/synexa")
```

**Errors:**

```python
from stable_diffusion_api import ModelError, PredictionTimeout

try:
    output = client.run(input)
except ModelError as e:
    print("failed:", e, e.prediction and e.prediction.get("id"))
except PredictionTimeout:
    print("still running — poll later")
```

Status values you will see on a prediction: `starting` → `processing` → `succeeded` | `failed`.

## About Stable Diffusion

Stable Diffusion is a latent text-to-image diffusion model created by the CompVis group at LMU Munich (Robin Rombach, Andreas Blattmann, Dominik Lorenz, Patrick Esser and Björn Ommer) in collaboration with Runway and Stability AI, and released in August 2022 with open weights. The [CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion) repository implements the CVPR 2022 paper *High-Resolution Image Synthesis with Latent Diffusion Models*. Its key idea is to run diffusion in the compressed latent space of a pretrained autoencoder instead of pixel space, which cuts compute by an order of magnitude and lets a model with roughly 860 million UNet parameters generate 512×512 images on a consumer GPU. Text conditioning comes from a frozen CLIP ViT-L/14 encoder via cross-attention.

SDXL, released by Stability AI in July 2023, scaled the recipe up: a larger UNet, two text encoders, native 1024×1024 output and an optional refiner stage. SDXL-Lightning, released by ByteDance in 2024, distils SDXL with progressive adversarial diffusion distillation so it produces comparable images in one, two, four or eight steps instead of the usual 25 to 50; the 4-step variant is the practical sweet spot. All three model lines share the same controls: a prompt and negative prompt, width and height in multiples of 64, a guidance scale, a step count, a sampler (`scheduler`) and a seed.

Through this client, `stability-ai/stable-diffusion` (the default) and `bytedance/sdxl-lightning-4step` are text-to-image; `stability-ai/sdxl` adds `input_image` and `denoising_strength` for image-to-image. Each returns one or more image URLs. Compared with newer transformer-based models these checkpoints are weaker at in-image text, hands and long compositional prompts, and stronger in ecosystem breadth and price.

The endpoints used by this client are `stability-ai/stable-diffusion`, `stability-ai/sdxl` and `bytedance/sdxl-lightning-4step`, which are the same Stable Diffusion, SDXL and SDXL-Lightning models released by their authors, served on Synexa. The weights and reference code are in the official repositories if you would rather self-host.

**Official project:** https://github.com/CompVis/stable-diffusion

## Use cases

- **Cheap bulk illustration** — call `run({"prompt": ..., "num_outputs": 4})` on the default endpoint at $0.0007 a run to fill blog headers, mock data or moodboards.
- **Fast interactive generation** — switch to `model="bytedance/sdxl-lightning-4step"` with `num_inference_steps=4` so a UI can show results in a couple of seconds.
- **Image-to-image variations** — pass `input_image` and `denoising_strength=0.5` to `stability-ai/sdxl` to restyle a sketch or photo while keeping its composition.
- **Negative-prompt quality control** — pin `negative_prompt="blurry, watermark, text"` and a fixed `seed` so regenerations change only what the prompt changes.
- **Sampler and guidance sweeps for research** — loop over `scheduler` and `guidance_scale` values with the same seed to build comparison grids without a local GPU.
- **Background jobs behind a queue** — submit with `wait=False` and a `webhook` from a web handler and write the returned URLs to your database when the callback fires.

## FAQ

**Is there a Stable Diffusion API?**

Stability AI offers its own paid API for its current models, and the original weights are open. This package is an independent Python client for three Stable Diffusion-family endpoints hosted on Synexa (`stability-ai/stable-diffusion`, `stability-ai/sdxl` and `bytedance/sdxl-lightning-4step`), served behind one HTTPS API.

**How much does the Stable Diffusion API cost?**

Per run on Synexa: `stability-ai/stable-diffusion` $0.0007, `bytedance/sdxl-lightning-4step` $0.001, `stability-ai/sdxl` $0.002. Billing is per prediction with no idle charge, and new accounts receive a free trial credit.

**Can I run Stable Diffusion without a GPU?**

Yes. With this client inference runs on Synexa's GPUs and your code receives image URLs; you need only Python 3.8+ and `httpx`. Running it locally needs a CUDA (or Apple Silicon) GPU with a few gigabytes of VRAM for SD 1.x and more for SDXL.

**Does this client work with the CompVis repo, diffusers, AUTOMATIC1111 or ComfyUI?**

No. It does not load local checkpoints, LoRAs, ControlNets or workflows; it is an HTTP client for the hosted endpoints. Use diffusers, AUTOMATIC1111 or ComfyUI when you need custom models or offline inference.

**What input formats does it accept?**

Input is a JSON object with `prompt` (string) required on every model. Optional fields include `negative_prompt` (string), `width` and `height` (integers, multiples of 64), `num_inference_steps` and `num_outputs` (integers), `guidance_scale` or `cfg_scale` (number), `scheduler` (string), `seed` (integer) and, on `sdxl`, `input_image` as a public image URL with `denoising_strength`. Output is one or more image URLs.

**Is this the official Stable Diffusion SDK?**

No. This is an independent, MIT-licensed client and is not affiliated with CompVis, Runway, Stability AI or ByteDance. The original project is at https://github.com/CompVis/stable-diffusion.

## Related

- [CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion) — the original repository, paper and weights.
- [Synexa Python client](https://github.com/synexa-ai/synexa-python) — the general-purpose client for every model on the platform.
- [stability-ai/sdxl](https://synexa.ai/explore/stability-ai/sdxl) — SDXL with image-to-image, also supported by this client.
- [bytedance/sdxl-lightning-4step](https://synexa.ai/explore/bytedance/sdxl-lightning-4step) — the 4-step SDXL distillation, also supported by this client.
- [black-forest-labs/flux-schnell](https://synexa.ai/explore/black-forest-labs/flux-schnell) — a newer few-step model from the original Stable Diffusion researchers, for comparison.

## License

MIT. This is an independent, community-maintained client and is not affiliated with or endorsed by the authors of Stable Diffusion. Model weights and trademarks belong to their respective owners.


_Last reviewed: 2026-09-22_
