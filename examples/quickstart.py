        """Minimal Stable Diffusion example: create one prediction and print the output URL(s)."""
        import stable_diffusion_api

        output = stable_diffusion_api.run({
    "prompt": "an astronaut riding a horse on mars, hd, dramatic lighting"
})
        print(output)
