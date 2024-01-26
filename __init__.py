from .nodes import PreviewLatent,PreviewLatentAdvanced, TAESDDecodeLatent

NODE_CLASS_MAPPINGS = {
    "PreviewLatent": PreviewLatent,
    "PreviewLatentAdvanced": PreviewLatentAdvanced,
    "TAESDDecodeLatent": TAESDDecodeLatent,

}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PreviewLatent": "Preview Latent",
    "PreviewLatentAdvanced": "Preview Latent (Advanced)",
    "TAESDDecodeLatent": "TAESD Decode Latent",
}
