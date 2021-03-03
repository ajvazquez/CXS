"""
Placeholders for missing VQ dependencies.
"""

C_INI_MEDIA_C_CODECS = None
dictc01bit = {}
v1_quant = None
v2_quant = None
v_codecs = None
v_bits_sample = None

def encode_vq(*args, **kwargs):
    return None

def get_codebook_from_serial(*args, **kwargs):
    return None

def get_vq_decoded_samples(*args, **kwargs):
    return None

def get_group_of_serialized_codebooks_noencoding(*args, **kwargs):
    return None
