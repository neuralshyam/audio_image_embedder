# audio_image_embedder/embedder.py

import numpy as np
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO)

def load_audio_data(audio_path):
    logging.info("Loading audio data.")
    with open(audio_path, "rb") as audio_file:
        audio_data = audio_file.read()
    return audio_data

def embed_data_to_pixels(audio_data, img_shape):
    width, height, _ = img_shape
    max_bytes = width * height * 3  # 3 bytes per pixel (RGB channels)
    
    if len(audio_data) + 4 > max_bytes:
        raise ValueError("Audio data is too large to embed in this image size.")

    data_length_bytes = len(audio_data).to_bytes(4, byteorder='big')
    full_data = data_length_bytes + audio_data

    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    flat_img_array = img_array.reshape(-1, 3)

    for i, byte in enumerate(full_data):
        pixel_idx = i // 3
        channel_idx = i % 3
        flat_img_array[pixel_idx][channel_idx] = byte

    logging.info("Data embedding completed.")
    return img_array.reshape((height, width, 3))

def embed_audio_to_image(audio_path, output_image_path):
    audio_data = load_audio_data(audio_path)

    data_len = len(audio_data) + 4
    side = int(np.ceil((data_len / 3) ** 0.5))
    img_shape = (side, side, 3)

    img_array = embed_data_to_pixels(audio_data, img_shape)

    img = Image.fromarray(img_array)
    img.save(output_image_path)
    logging.info(f"Audio embedded in image saved as {output_image_path}")

def load_image_to_array(image_path):
    logging.info("Loading image to extract audio data.")
    img = Image.open(image_path)
    img_array = np.array(img)
    return img_array

def extract_pixels_to_data(img_array):
    flat_img_array = img_array.reshape(-1, 3)
    byte_data = bytearray()

    data_length_bytes = bytearray(flat_img_array[:4].flatten()[:4])
    data_length = int.from_bytes(data_length_bytes, byteorder='big')
    logging.info(f"Extracted data length from header: {data_length} bytes")

    for pixel in flat_img_array[4:data_length + 4]:
        byte_data.extend(pixel[:3])

    return bytes(byte_data[:data_length])

def extract_audio_from_image(image_path, output_audio_path):
    img_array = load_image_to_array(image_path)

    audio_data = extract_pixels_to_data(img_array)

    with open(output_audio_path, "wb") as audio_file:
        audio_file.write(audio_data)

    logging.info(f"Audio extracted and saved to {output_audio_path}")
