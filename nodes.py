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
import torchvision.transforms as TT

class LatentToRGB:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                    {"latent": ("LATENT",),
                     "base_model": (["SD15",
                                     "SDXL",
                                     "SD3",
                                     "Flux",
                                     "Wan21",
                                     "Wan22",
                                     "LTXV"],)},
                "hidden": {"prompt": "PROMPT",
                           "extra_pnginfo": "EXTRA_PNGINFO",
                           "my_unique_id": "UNIQUE_ID",},
                }
    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    OUTPUT_NODE = False
    FUNCTION = "l2rgb"
    CATEGORY = "latent"

    def l2rgb(self, latent, base_model, prompt=None, extra_pnginfo=None, my_unique_id=None):
        previous_preview_method = args.preview_method
        temp_previewer = latent_preview.LatentPreviewMethod.Latent2RGB
        output_images=[]

        try:
            args.preview_method=temp_previewer
            preview_format = "PNG"
            load_device=comfy.model_management.vae_offload_device()
            latent_format = {"SD15":latent_formats.SD15,
                             "SDXL":latent_formats.SDXL,
                             "SD15":latent_formats.SD15,
                             "SDXL":latent_formats.SDXL,
                             "SD3":latent_formats.SD3,
                             "Flux":latent_formats.Flux,
                             "Wan21":latent_formats.Wan21,
                             "Wan22":latent_formats.Wan22,
                             "LTXV":latent_formats.LTXV,
                             }[base_model]()

            x0 = latent["samples"]
            if x0.ndim == 5: # videohelper suite animated previews are enabled
                x0 = x0.movedim(2,1)
                x0 = x0.reshape((-1,)+x0.shape[-3:])
            for i in range(len(x0)):
                x=latent.copy()
                x["samples"] = x0[i:i+1].clone()
                x_sample = x["samples"] * latent_format.scale_factor
                img = latent_preview.get_previewer(load_device, latent_format).decode_latent_to_preview(x_sample)
                output_images.append(TT.ToTensor()(img))
        finally:
            # Restore global changes
            args.preview_method=previous_preview_method

        output_images = torch.stack(output_images, dim=0)
        output_images = output_images.permute([0,2,3,1])
        return (output_images, )

class PreviewLatentAdvanced:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                    {"latent": ("LATENT",),
                     "base_model": (["SD15",
                                     "SDXL",
                                     "SD3",
                                     "Flux",
                                     "Wan21",
                                     "Wan22",
                                     "LTXV"],),
                     "preview_method": (["auto","taesd","latent2rgb"],),
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

    def lpreview(self, latent, base_model, preview_method, prompt=None, extra_pnginfo=None, my_unique_id=None):
        previous_preview_method = args.preview_method
        if preview_method == "taesd":
            temp_previewer = latent_preview.LatentPreviewMethod.TAESD
        elif preview_method == "latent2rgb":
            temp_previewer = latent_preview.LatentPreviewMethod.Latent2RGB
        else:
            temp_previewer = latent_preview.LatentPreviewMethod.Auto

        results = list()

        try:
            args.preview_method=temp_previewer
            preview_format = "PNG"
            load_device=comfy.model_management.vae_offload_device()
            latent_format = {"SD15":latent_formats.SD15,
                             "SDXL":latent_formats.SDXL,
                             "SD15":latent_formats.SD15,
                             "SDXL":latent_formats.SDXL,
                             "SD3":latent_formats.SD3,
                             "Flux":latent_formats.Flux,
                             "Wan21":latent_formats.Wan21,
                             "Wan22":latent_formats.Wan22,
                             "LTXV":latent_formats.LTXV,
                             }[base_model]()

            result=[]
            x0 = latent["samples"]
            if x0.ndim == 5: # videohelper suite animated previews are enabled
                x0 = x0.movedim(2,1)
                x0 = x0.reshape((-1,)+x0.shape[-3:])
            for i in range(len(x0)):
                x=latent.copy()
                x["samples"] = x0[i:i+1].clone()
                x_sample = x["samples"] * latent_format.scale_factor
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
                results.append({"filename": file, "subfolder": subfolder, "type": "temp"})

        finally:
            # Restore global changes
            args.preview_method=previous_preview_method

        return {"result": (latent,), "ui": { "images": results } }

class PreviewLatent(PreviewLatentAdvanced):
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                    {"latent": ("LATENT",),
                     },
                "hidden": {"prompt": "PROMPT",
                           "extra_pnginfo": "EXTRA_PNGINFO",
                           "my_unique_id": "UNIQUE_ID",},
                }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    OUTPUT_NODE = True
    FUNCTION = "lpreview_basic"
    CATEGORY = "latent"

    def lpreview_basic(self, latent, prompt=None, extra_pnginfo=None, my_unique_id=None):
        return PreviewLatentAdvanced().lpreview(latent=latent, base_model="SD15", preview_method="auto", prompt=prompt, extra_pnginfo=extra_pnginfo, my_unique_id=my_unique_id)

class PreviewLatentXL(PreviewLatentAdvanced):
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                {"latent": ("LATENT",),
                 },
                "hidden": {"prompt": "PROMPT",
                           "extra_pnginfo": "EXTRA_PNGINFO",
                           "my_unique_id": "UNIQUE_ID",},
                }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    OUTPUT_NODE = True
    FUNCTION = "lpreview_xl"
    CATEGORY = "latent"

    def lpreview_xl(self, latent, prompt=None, extra_pnginfo=None, my_unique_id=None):
        return PreviewLatentAdvanced().lpreview(latent=latent, base_model="SDXL", preview_method="auto", prompt=prompt, extra_pnginfo=extra_pnginfo, my_unique_id=my_unique_id)


class PreviewLatentFlux(PreviewLatentAdvanced):
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                {"latent": ("LATENT",),
                 },
                "hidden": {"prompt": "PROMPT",
                           "extra_pnginfo": "EXTRA_PNGINFO",
                           "my_unique_id": "UNIQUE_ID",},
                }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    OUTPUT_NODE = True
    FUNCTION = "lpreview_flux"
    CATEGORY = "latent"

    def lpreview_flux(self, latent, prompt=None, extra_pnginfo=None, my_unique_id=None):
        return PreviewLatentAdvanced().lpreview(latent=latent, base_model="Flux", preview_method="auto", prompt=prompt, extra_pnginfo=extra_pnginfo, my_unique_id=my_unique_id)
