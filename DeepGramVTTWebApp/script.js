const transcriptBox = document.getElementById("transcript");
const video = document.getElementById("video");
let cues = [];
const speakerColors = {};

function getSpeakerColor(speakerId) {
  if (!speakerColors[speakerId]) {
    const hue = (Object.keys(speakerColors).length * 137) % 360;
    speakerColors[speakerId] = `hsl(${hue}, 80%, 60%)`;
  }
  return speakerColors[speakerId];
}

document.getElementById("videoInput").addEventListener("change", e => {
  const file = e.target.files[0];
  if (file) {
    video.src = URL.createObjectURL(file);
  }
});

document.getElementById("vttInput").addEventListener("change", e => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      const vttText = reader.result;
      cues = parseVTT(vttText);
    };
    reader.readAsText(file);
  }
});

function parseVTT(data) {
  const lines = data.split("\n");
  const cues = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (line.includes("-->")) {
      const [start, end] = line.split(" --> ").map(t => toSeconds(t));
      const text = lines[i + 1] || "";
      const speakerMatch = text.match(/<v Speaker (\d+)>/);
      const speaker = speakerMatch ? parseInt(speakerMatch[1]) : 0;
      const plainText = text.replace(/<.*?>/g, "");
      cues.push({ start, end, text: plainText, speaker });
      i += 1;
    }
  }
  return cues;
}

function toSeconds(timeStr) {
  const parts = timeStr.split(/[:\.]/).map(Number);
  return parts[0] * 3600 + parts[1] * 60 + parts[2] + (parts[3] || 0) / 1000;
}

video.addEventListener("timeupdate", () => {
  const current = video.currentTime;
  const currentCue = cues.find(cue => current >= cue.start && current <= cue.end);
  if (currentCue) {
    const color = getSpeakerColor(currentCue.speaker);
    transcriptBox.innerHTML = `<span style="color: ${color}">${currentCue.text}</span>`;
  } else {
    transcriptBox.innerHTML = "";
  }
});
