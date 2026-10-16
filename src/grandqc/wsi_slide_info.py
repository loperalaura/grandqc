# EXTRACTION OF META-DATA FROM SLIDE

from PIL import Image
from grandqc.wsi_stain_norm import standardizer
import numpy as np

def is_channels_first(arr):
    """True if the image is stored as (C, Y, X), False if (Y, X, C).

    OME-TIFF H&E images come in both layouts (see issue #14).
    """
    return arr.shape[0] in (3, 4) and arr.shape[-1] not in (3, 4)


def image_hw(arr):
    """Return (height, width) for both (C, Y, X) and (Y, X, C) images."""
    if is_channels_first(arr):
        return arr.shape[1], arr.shape[2]
    return arr.shape[0], arr.shape[1]


def slide_info(slide, m_p_s, mpp_model,mpp = 0.2425):
    # Microne per pixel
     # mpp=0.2425 for TCGA-AA- slides of COADREAD cohort
    p_s = int(mpp_model / mpp * m_p_s)

    # Vendor
    # Extract and save dimensions of level [0]
    h_l0, w_l0 = image_hw(slide)
    #print(slide.shape)

    # Calculate number of patches to process
    patch_n_w_l0 = int(w_l0 / p_s)
    patch_n_h_l0 = int(h_l0 / p_s)

    # Output BASIC DATA
    print("")
    print("Basic data about processed whole-slide image")
    print("")
    print("Microns per pixel (slide):", mpp)
    print("Height: ", h_l0)
    print("Width: ", w_l0)
    print("Model patch size at slide MPP: ", p_s, "x", p_s)
    print("Width - number of patches: ", patch_n_w_l0)
    print("Height - number of patches: ", patch_n_h_l0)
    print("Overall number of patches / slide (without tissue detection): ", patch_n_w_l0 * patch_n_h_l0)

    return p_s, patch_n_w_l0, patch_n_h_l0, mpp, w_l0, h_l0
