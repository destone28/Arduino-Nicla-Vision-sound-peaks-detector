import image
import audio
from ulab import numpy as np
from ulab import utils
import time
import pyb

# Base configurations
CHANNELS = 1
SIZE = 256 // (2 * CHANNELS)
raw_buf = None
fb = image.Image(SIZE + 50, SIZE, image.RGB565, copy_to_fb=True)
audio.init(channels=CHANNELS, frequency=16000, gain_db=24, highpass=0.9883)

# LED for active notification
red_led = pyb.LED(1)
green_led = pyb.LED(2)

AUDIO_THRESHOLD = 3     # Threshold for a peak to be notified
RESET_THRESHOLD = 5      # Threshold for a peak to be considered as ended
MIN_TIME_BETWEEN_ALERTS = 0.5  # Minimum amount of seconds between 2 detections
last_alert_time = 0

# Flag for detection state
peak_detected = False
peak_count = 0           # Peaks counter

def audio_callback(buf):
    global raw_buf
    if raw_buf is None:
        raw_buf = buf

# Start audio streaming
audio.start_streaming(audio_callback)
green_led.on()  # Active system

def draw_fft(img, fft_buf):
    # Do not divide by zero if fft_buf is empty or contains only zeroes
    max_val = max(fft_buf) if len(fft_buf) > 0 and max(fft_buf) > 0 else 1

    # Remove normalization keeping highest values
    fft_buf = (fft_buf / max_val) * SIZE
    fft_buf = np.log10(fft_buf + 1) * 20

    color = (0xFF, 0x0F, 0x00)
    for i in range(0, SIZE):
        img.draw_line(i, SIZE, i, SIZE - int(fft_buf[i]), color, 1)

def draw_audio_bar(img, level, offset):
    blk_size = SIZE // 10

    # Color changes with audio level
    if level > AUDIO_THRESHOLD * 2:  # Very high
        color = (0xFF, 0, 0)  # Bright red
    elif level > AUDIO_THRESHOLD:    # Over threshold
        color = (0xFF, 0x80, 0)  # Orange
    else:
        color = (0xFF, 0x00, 0xF0)  # Base color

    blk_space = blk_size // 4
    for i in range(0, int(round(level / 10))):
        fb.draw_rectangle(
            SIZE + offset,
            SIZE - ((i + 1) * blk_size) + blk_space,
            20,
            blk_size - blk_space,
            color,
            1,
            True,
        )

    # Visual threshold
    threshold_y = SIZE - int(AUDIO_THRESHOLD / 10) * blk_size
    fb.draw_line(
        SIZE + offset, threshold_y,
        SIZE + offset + 20, threshold_y,
        (0, 0xFF, 0),
        2
    )

def notify_audio_peak(level):
    global last_alert_time, peak_detected, peak_count

    current_time = time.time()

    if current_time - last_alert_time >= MIN_TIME_BETWEEN_ALERTS:
        peak_count += 1
        print(f"AUDIO PEAK #{peak_count}! Level: {level}")

        red_led.on()

        # Update last notification time
        last_alert_time = current_time

        # Setup peak discovery flag
        peak_detected = True

while True:
    if raw_buf is not None:
        pcm_buf = np.frombuffer(raw_buf, dtype=np.int16)
        raw_buf = None

        if CHANNELS == 1:
            fft_buf = utils.spectrogram(pcm_buf)

            # Calculate peak value
            peak_amplitude = np.max(abs(pcm_buf))
            l_lvl = int((peak_amplitude / 32768) * 100)

            # Calculate also average level for reference
            avg_lvl = int((np.mean(abs(pcm_buf)) / 32768) * 100)
        else:
            fft_buf = utils.spectrogram(pcm_buf[0::2])
            l_lvl = int((np.max(abs(pcm_buf[1::2])) / 32768) * 100)
            r_lvl = int((np.max(abs(pcm_buf[0::2])) / 32768) * 100)

        # Find peaks
        if l_lvl > AUDIO_THRESHOLD:
            notify_audio_peak(l_lvl)
        elif l_lvl < RESET_THRESHOLD and peak_detected:
            # Reset only when level goes under RESET_THRESHOLD
            red_led.off()
            peak_detected = False

        fb.clear()
        draw_fft(fb, fft_buf)
        draw_audio_bar(fb, l_lvl, 0)

        # Info about detected peaks
        fb.draw_string(0, 10, f"Peak: {l_lvl}", color=(255, 255, 255), scale=2)
        fb.draw_string(0, 30, f"Avg: {avg_lvl}", color=(200, 200, 200), scale=2)
        fb.draw_string(0, 50, f"Thr: {AUDIO_THRESHOLD}", color=(0, 255, 0), scale=2)

        if peak_detected:
            fb.draw_string(SIZE + 5, 50, f"PEAK #{peak_count}!", color=(255, 0, 0), scale=2)

        if CHANNELS == 2:
            draw_audio_bar(fb, r_lvl, 25)

        fb.flush()

# Stop streaming
audio.stop_streaming()
