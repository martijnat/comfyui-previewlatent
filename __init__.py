from .nodes import PreviewLatent,PreviewLatentAdvanced,PreviewLatentXL

NODE_CLASS_MAPPINGS = {
    "PreviewLatent": PreviewLatent,
    "PreviewLatentAdvanced": PreviewLatentAdvanced,
    "PreviewLatentXL": PreviewLatentXL,

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PreviewLatent": "Preview Latent",
    "PreviewLatentAdvanced": "Preview Latent (Advanced)",
    "PreviewLatentXL": "Preview Latent XL",
}
