import os
import io
import numpy as np
import torch
import torchaudio


class MP3EmbedInImage:
    """Embed first 1 second of MP3 audio into image alpha channel using steganography."""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "mp3_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                    "placeholder": "Đường dẫn file mp3",
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image_out",)
    FUNCTION = "embed"
    CATEGORY = "comfyui-sortlist"

    def embed(self, image, mp3_path):
        if not mp3_path or not os.path.isfile(mp3_path):
            raise Exception(f"File không tồn tại: {mp3_path}")

        # Load audio and take only first 1 second
        waveform, sample_rate = torchaudio.load(mp3_path)
        one_sec_samples = min(sample_rate, waveform.shape[1])
        waveform_1s = waveform[:, :one_sec_samples]

        # Resample to 8000Hz mono to minimize size
        if sample_rate != 8000:
            resampler = torchaudio.transforms.Resample(sample_rate, 8000)
            waveform_1s = resampler(waveform_1s)
        # Convert to mono
        if waveform_1s.shape[0] > 1:
            waveform_1s = waveform_1s.mean(dim=0, keepdim=True)

        # Convert to 8-bit PCM bytes (compact)
        audio_np = (waveform_1s.squeeze(0).clamp(-1, 1).numpy() * 127).astype(np.int8)
        mp3_bytes = audio_np.tobytes()

        # Convert to bits
        data_bits = []
        # Header: 32 bits for data length
        data_len = len(mp3_bytes)
        for i in range(32):
            data_bits.append((data_len >> (31 - i)) & 1)
        # Data bits
        for b in mp3_bytes:
            b_unsigned = b & 0xFF
            for i in range(8):
                data_bits.append((b_unsigned >> (7 - i)) & 1)

        # Process image
        np_img = np.asarray(image, dtype=np.float32)
        if np_img.ndim == 4:
            np_img = np_img[0]

        if np_img.max() > 1.0 + 1e-3:
            np_img = np_img / 255.0

        H, W, C = np_img.shape

        # Add alpha channel if needed
        if C == 3:
            alpha = np.ones((H, W, 1), dtype=np.float32)
            np_img = np.concatenate([np_img, alpha], axis=2)
        elif C < 3:
            raise Exception("Image must have at least RGB channels.")

        total_pixels = H * W
        if len(data_bits) > total_pixels:
            raise Exception(
                f"Ảnh {W}x{H} quá nhỏ. Cần ít nhất {len(data_bits)} pixels, "
                f"ảnh chỉ có {total_pixels} pixels."
            )

        # Embed LSB into alpha channel
        alpha_ch = np_img[:, :, 3]
        alpha_u8 = (alpha_ch * 255).astype(np.uint8).flatten()

        for i, bit in enumerate(data_bits):
            alpha_u8[i] = (alpha_u8[i] & 0b11111110) | bit

        np_img[:, :, 3] = alpha_u8.reshape(H, W) / 255.0

        out_tensor = torch.from_numpy(np_img).unsqueeze(0).float()
        return (out_tensor,)


NODE_CLASS_MAPPINGS = {
    "MP3 Embed In Image": MP3EmbedInImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MP3 Embed In Image": "MP3 Embed In Image (Steganography)",
}
