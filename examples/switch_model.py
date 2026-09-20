"""The same client drives every hosted model listed in stable_diffusion_api.MODELS."""
from stable_diffusion_api import Client, MODELS

client = Client()
for slug, info in MODELS.items():
    print(slug, "->", info["category"], "required:", info["required"])
# pick one explicitly
output = client.run({"prompt": "An astronaut riding a rainbow unicorn, cinematic, dramatic"}, model="stability-ai/sdxl")
print(output)
