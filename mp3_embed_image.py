import os
import numpy as np
import torch
import torchaudio


class MP3EmbedInImage:
    """Embed first 1 second of MP3 audio into image RGB channels using LSB steganography."""

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
        if waveform_1s.shape[0] > 1:
            waveform_1s = waveform_1s.mean(dim=0, keepdim=True)

        # Convert to 8-bit PCM bytes
        audio_np = (waveform_1s.squeeze(0).clamp(-1, 1).numpy() * 127).astype(np.int8)
        audio_bytes = audio_np.tobytes()

        # Build bit stream: [32-bit length header] + [data bits]
        data_len = len(audio_bytes)
        bits = []
        for i in range(32):
            bits.append((data_len >> (31 - i)) & 1)
        for b in audio_bytes:
            b_unsigned = b & 0xFF
            for i in range(8):
                bits.append((b_unsigned >> (7 - i)) & 1)

        # Process image
        np_img = image.detach().cpu().numpy()
        if np_img.ndim == 4:
            np_img = np_img[0].copy()
        else:
            np_img = np_img.copy()

        if np_img.max() <= 1.0 + 1e-3:
            img_u8 = (np_img * 255).astype(np.uint8)
        else:
            img_u8 = np_img.astype(np.uint8)

        H, W, C = img_u8.shape
        if C < 3:
            raise Exception("Image must have at least RGB channels.")

        # Total capacity: H * W * 3 bits (1 bit per RGB channel per pixel)
        total_bits = H * W * 3
        if len(bits) > total_bits:
            raise Exception(
                f"Audio quá lớn ({data_len} bytes). "
                f"Ảnh {W}x{H} chứa tối đa {total_bits // 8} bytes."
            )

        # Embed LSB into RGB channels
        flat = img_u8[:, :, :3].reshape(-1)
        for i, bit in enumerate(bits):
            flat[i] = (flat[i] & 0b11111110) | bit

        img_u8[:, :, :3] = flat.reshape(H, W, 3)

        out = img_u8.astype(np.float32) / 255.0
        out_tensor = torch.from_numpy(out).unsqueeze(0).float()
        return (out_tensor,)


NODE_CLASS_MAPPINGS = {
    "MP3 Embed In Image": MP3EmbedInImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MP3 Embed In Image": "MP3 Embed In Image (RGB)",
}
