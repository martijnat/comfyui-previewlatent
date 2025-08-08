from .nodes import PreviewLatent,PreviewLatentAdvanced,PreviewLatentXL,PreviewLatentFlux

NODE_CLASS_MAPPINGS = {
    "PreviewLatent": PreviewLatent,
    "PreviewLatentAdvanced": PreviewLatentAdvanced,
    "PreviewLatentXL": PreviewLatentXL,
    "PreviewLatentFlux": PreviewLatentFlux,

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PreviewLatent": "Preview Latent (Stable Diffusion)",
    "PreviewLatentAdvanced": "Preview Latent (Advanced)",
    "PreviewLatentXL": "Preview Latent (SDXL)",
    "PreviewLatentFlux": "Preview Latent (Flux)",
}
