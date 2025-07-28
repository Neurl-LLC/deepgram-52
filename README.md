# 🎬 Deepgram Metadata Captions

Extract rich, actionable metadata from audio files using Deepgram’s Nova-3 model and transform it into standard caption formats like WebVTT. Build smarter segmentation, analytics, and QA workflows — and caption your videos with meaningful context.

---

## ✨ Features

### 🧠 Transcript Intelligence

* Generate **highly accurate transcripts** using Deepgram’s Nova-3 model
* **Utterance segmentation** for semantically meaningful speech chunks
* **Timestamps and speaker diarization** to know who spoke and when

### 📼 Caption Rendering

* Converts transcript into **WebVTT** format with:

  * Rich metadata
  * Proper cue formatting
  * Speaker labeling

### 🌐 Web Video Player

* Simple web interface for previewing video + captions
* Includes styling for caption readability

---

## 🗂️ File Structure

```bash
.
├── app.py                      # CLI tool to transcribe & generate WebVTT/SRT captions
├── DeepGramVTTWebApp           # Web frontend for video playback
│   ├── index.html              # HTML page for video + caption rendering
│   ├── script.js               # JavaScript for syncing captions
│   └── styles.css              # Styling for the video player and captions
├── DHH_LEX_Interview.mp4       # Sample video file
├── DHH_LEX_Interview.wav       # Corresponding audio file
└── README.md
```

---

## 🚀 Quick Start

### 🔧 Requirements

* Python 3.9+
* A [Deepgram API Key](https://console.deepgram.com/)
* Dependencies: `deepgram-sdk`, `rich`

### 📦 Installation

1. **Clone the repository**:

```bash
git clone https://github.com/Neurl-LLC/deepgram-52.git
cd deepgram-metadata-captions
```

2. **Install dependencies**:

```bash
pip install deepgram-sdk rich
```

3. **Set up your environment**:
   Export your Deepgram API key as an environment variable:

```bash
export DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

### ▶️ Generate Captions

To transcribe the audio and generate a WebVTT file:

```bash
python app.py
```

This will output a file like: `output.vtt`

---

## 🌐 Running the Web App

To use the web app:

```bash
cd DeepGramVTTWebApp
python -m http.server
```

Visit `http://localhost:8000` in your browser.

Then upload your video and the corresponding `output.vtt`

