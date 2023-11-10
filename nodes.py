from PIL import Image, ImageOps
from PIL.PngImagePlugin import PngInfo
import latent_formats
import json
import os
import latent_preview
import folder_paths
import comfy.sd
import comfy.utils
from comfy.cli_args import args
import random
import torch

class PreviewLatent:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                    {"latent": ("LATENT",),
                     "base_model": (["SD15","SDXL"],),
                     },
                "hidden": {"prompt": "PROMPT",
                           "extra_pnginfo": "EXTRA_PNGINFO",
                           "my_unique_id": "UNIQUE_ID",},
                }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    OUTPUT_NODE = True
    FUNCTION = "lpreview"
    CATEGORY = "latent"

    def lpreview(self, latent, base_model, prompt=None, extra_pnginfo=None, my_unique_id=None):
        previous_preview_method = args.preview_method
        results = list()
        try:
            args.preview_method=latent_preview.LatentPreviewMethod.Auto
            preview_format = "PNG"
            load_device=comfy.model_management.vae_offload_device()
            latent_format = {"SD15":latent_formats.SD15,
                             "SDXL":latent_formats.SDXL}[base_model]()

            x_sample = latent["samples"]
            x_sample = x_sample / 6;
            img = latent_preview.get_previewer(load_device, latent_format).decode_latent_to_preview(x_sample)
            full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path("",folder_paths.get_temp_directory(), img.height, img.width)
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            file = "latent_"+"".join(random.choice("0123456789") for x in range(8))+".png"
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=4)
            results=[{"filename": file, "subfolder": subfolder, "type": "temp"}]

        finally:
            # Restore global changes
            args.preview_method=previous_preview_method

        return {"result": (latent,), "ui": { "images": results } }
