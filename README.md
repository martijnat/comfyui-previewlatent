# comfyui-previewlatent
a <a href="https://github.com/comfyanonymous/ComfyUI">ComfyUI</a> plugin for previewing latents without vae decoding.
Useful for showing intermediate results and can be used a faster "preview image" if you don't wan't to use vae decode.

- Forwards input latent to output, so can be used as a fancy reroute node.
- PreviewLatent can be used as a final output for quick testing
- Previews are decoded using taesd if available (otherwise latent2rgb).
- Previews are full resolution (Ksampler previews are limited to 512x512)
- Previews are temporary PNG files with full workflow metadata just like "Preview Image" (so right lick and using save image can save youre workflow)

<img src="https://github.com/martijnat/comfyui-previewlatent/blob/main/previewlatent.png" style="display: inline-block;">
