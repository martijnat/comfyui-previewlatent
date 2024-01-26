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

class PreviewLatentAdvanced:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                    {"latent": ("LATENT",),
                     "base_model": (["SD15","SDXL"],),
                     "preview_method": (["auto","taesd","latent2rgb"],),
                     },
                "hidden": {"prompt": "PROMPT",
                           "extra_pnginfo": "EXTRA_PNGINFO",
                           "my_unique_id": "UNIQUE_ID",
                           "img_output": "IMG_OUTPUT",},
                }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    OUTPUT_NODE = True
    FUNCTION = "lpreview"
    CATEGORY = "latent"

    def lpreview(self, latent, base_model, preview_method, prompt=None, extra_pnginfo=None, my_unique_id=None, img_output=False):
        previous_preview_method = args.preview_method
        if preview_method == "taesd":
            temp_previewer = latent_preview.LatentPreviewMethod.TAESD
        elif preview_method == "latent2rgb":
            temp_previewer = latent_preview.LatentPreviewMethod.Latent2RGB
        else:
            temp_previewer = latent_preview.LatentPreviewMethod.Auto

        results = list()
        output_images=[]

        try:
            args.preview_method=temp_previewer
            preview_format = "PNG"
            load_device=comfy.model_management.vae_offload_device()
            latent_format = {"SD15":latent_formats.SD15,
                             "SDXL":latent_formats.SDXL}[base_model]()

            result=[]
            for i in range(len(latent["samples"])):
                x=latent.copy()
                x["samples"] = latent["samples"][i:i+1].clone()
                x_sample = x["samples"]
                x_sample = x_sample / 6;

                img = latent_preview.get_previewer(load_device, latent_format).decode_latent_to_preview(x_sample)
                
                output_images.append(TT.ToTensor()(img))
                
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

        output_images = torch.stack(output_images, dim=0)
        output_images = output_images.permute([0,2,3,1])
        
        if img_output:
            return (output_images, )
        else:
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

class TAESDDecodeLatent(PreviewLatentAdvanced):
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                    {"latent": ("LATENT",),
                     "base_model": (["SD15","SDXL"],),
                     },
                "hidden": {"prompt": "PROMPT",
                           "extra_pnginfo": "EXTRA_PNGINFO",
                           "my_unique_id": "UNIQUE_ID",
                           "img_output": "IMG_OUTPUT",},
                }

    RETURN_TYPES = ("IMAGE", )
    RETURN_NAMES = ("image", )
    OUTPUT_NODE = True
    FUNCTION = "lpreview_output"
    CATEGORY = "latent"

    def lpreview_output(self, latent, base_model, preview_method="taesd", prompt=None, extra_pnginfo=None, my_unique_id=None, img_output=True):
        return PreviewLatentAdvanced().lpreview(latent=latent, base_model=base_model, preview_method=preview_method, prompt=prompt, extra_pnginfo=extra_pnginfo, my_unique_id=my_unique_id,  img_output=img_output)