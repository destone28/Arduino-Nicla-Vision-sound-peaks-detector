# Audio Peak Detector with FFT Visualization

## Overview

This script implements a real-time audio spectrum analyzer and peak detector using the microphone on the Arduino Nicla Vision board. It provides visual feedback through the built-in display, showing both the audio spectrum (FFT) and the current audio level.

The system continuously monitors audio input, detects sound peaks that exceed a configurable threshold, and provides both visual feedback through the display and LED indicators when peaks are detected.

## Features

- Real-time FFT (Fast Fourier Transform) visualization of audio spectrum
- Peak audio level detection with adjustable threshold
- Visual indicators for detected audio peaks:
  - Red LED illumination
  - On-screen level indicators with color coding
  - Peak counter display
- Configurable parameters:
  - Detection threshold
  - Reset threshold
  - Minimum time between alerts

## Requirements

- Arduino Nicla Vision board
- MicroPython firmware installed (version >= 1.2)
- OpenMV IDE (for uploading and debugging)

## How It Works

1. **Audio Capture**: The system continuously samples audio from the onboard microphone
2. **FFT Analysis**: Audio data is processed using Fast Fourier Transform to visualize the frequency spectrum
3. **Peak Detection**: The maximum amplitude is calculated and compared to a configurable threshold
4. **Visual Feedback**:
   - The FFT spectrum is displayed as a bar graph
   - The current audio level is shown with a vertical bar that changes color based on intensity
   - When a peak is detected, the red LED illuminates and on-screen indicators show "PEAK!"
   - A counter keeps track of the total number of detected peaks

## Configuration Parameters

| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| `AUDIO_THRESHOLD` | 3 | Threshold level (0-100) for peak detection. Lower values increase sensitivity |
| `RESET_THRESHOLD` | 5 | Level below which a peak is considered ended, allowing new peak detection |
| `MIN_TIME_BETWEEN_ALERTS` | 0.5 | Minimum time in seconds between consecutive peak alerts |

## Display Elements

- **FFT Spectrum**: Red bars showing the frequency components of the audio signal
- **Audio Level Bar**: Vertical bar indicating the current peak audio level
  - Magenta: Normal levels (below threshold)
  - Orange: Level exceeds threshold
  - Red: Level exceeds twice the threshold
- **Information Text**:
  - Current peak level value
  - Average level value
  - Current threshold setting
  - Peak counter when a peak is detected

## LED Indicators

- **Green LED**: System active and monitoring
- **Red LED**: Audio peak detected (stays on until audio level drops below reset threshold)

## Usage

1. Upload the script to your Arduino Nicla Vision using OpenMV IDE
2. The script will start running automatically
3. Speak or make sounds to see the visualization and peak detection in action
4. The red LED will illuminate when audio exceeds the threshold

## Customization

You can modify the script to adjust sensitivity and behavior:

- Lower `AUDIO_THRESHOLD` for more sensitive detection
- Increase `MIN_TIME_BETWEEN_ALERTS` to reduce notification frequency
- Change `RESET_THRESHOLD` to adjust how quickly the system resets after a peak

## Applications

- Sound level monitoring
- Audio visualization for educational purposes
- Simple noise detection system
- Audio-reactive projects
- Testing microphone functionality on Nicla Vision
