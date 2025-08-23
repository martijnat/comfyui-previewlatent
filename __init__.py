from .nodes import PreviewLatent,PreviewLatentAdvanced,PreviewLatentXL,PreviewLatentFlux,LatentToRGB

NODE_CLASS_MAPPINGS = {
    "PreviewLatent": PreviewLatent,
    "PreviewLatentAdvanced": PreviewLatentAdvanced,
    "PreviewLatentXL": PreviewLatentXL,
    "PreviewLatentFlux": PreviewLatentFlux,
    "LatentToRGB": LatentToRGB,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PreviewLatent": "Preview Latent (Stable Diffusion)",
    "PreviewLatentAdvanced": "Preview Latent (Advanced)",
    "PreviewLatentXL": "Preview Latent (SDXL)",
    "PreviewLatentFlux": "Preview Latent (Flux)",
    "LatentToRGB": "Latent to RGB",
}
