# Digital Signal Encoder

A Python-based GUI application for visualizing different digital signal encoding techniques commonly used in data communication systems.

## Overview
This application allows users to input binary data (0s and 1s) and see how it would be encoded using various line coding schemes. It's a useful tool for understanding digital communication concepts and signal encoding methods.

## Features
- Interactive GUI with input validation
- Visualizes 6 different encoding techniques:
  - NRZ-L (Non-Return to Zero Level)
  - NRZ-I (Non-Return to Zero Inverted)
  - Bipolar AMI (Alternate Mark Inversion)
  - Pseudoternary
  - Manchester
  - Differential Manchester
- Real-time signal visualization
- Clear and reset functionality
- Grid-based signal display

## Prerequisites
- Python 3.x
- Required libraries:
  ```bash
  pip install tkinter
  pip install matplotlib
  pip install numpy
  ```
  
## Usage
1. Clone the repository
2. Run the application:
  ```bash
  python digital_signal_encoder.py
  ```
4. Enter binary data (e.g., 01001110)
5. Click 'Generate All Signals' to view the encodings
6. Use 'Clear' to reset
