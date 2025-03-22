let videoData = {};

async function fetchVideoInfo() {
  const url = document.getElementById("youtube-url").value;
  const videoID = extractYouTubeID(url);
  if (!videoID) {
    alert("Invalid YouTube URL");
    return;
  }

  try {
    const oEmbedResponse = await fetch(
      `https://www.youtube.com/oembed?url=${url}&format=json`
    );
    if (!oEmbedResponse.ok) throw new Error("Invalid YouTube URL");
    const oEmbedData = await oEmbedResponse.json();

    const resolutions = {
      144: `https://img.youtube.com/vi/${videoID}/default.jpg`,
      240: `https://img.youtube.com/vi/${videoID}/mqdefault.jpg`,
      360: `https://img.youtube.com/vi/${videoID}/hqdefault.jpg`,
      480: `https://img.youtube.com/vi/${videoID}/sddefault.jpg`,
      720: `https://img.youtube.com/vi/${videoID}/maxresdefault.jpg`,
    };

    const availableResolutions = {};
    for (const [res, imgUrl] of Object.entries(resolutions)) {
      const response = await fetch(imgUrl, { method: "HEAD" });
      if (response.ok) availableResolutions[res] = imgUrl;
    }

    videoData = {
      url: url,
      title: oEmbedData.title,
      author: oEmbedData.author_name,
      thumbnail: Object.values(availableResolutions).pop(), // Highest available thumbnail
      resolutions: Object.keys(availableResolutions),
    };

    document.getElementById("video-title").innerText = videoData.title;
    document.getElementById(
      "video-author"
    ).innerText = `By: ${videoData.author}`;
    document.getElementById("video-thumbnail").src = videoData.thumbnail;

    const resolutionSelect = document.getElementById("resolution-select");
    resolutionSelect.innerHTML = "";

    videoData.resolutions.forEach((res) => {
      const option = document.createElement("option");
      option.value = res;
      option.innerText = res;
      resolutionSelect.appendChild(option);
    });

    document.getElementById("video-info").style.display = "block";
  } catch (error) {
    alert("Error fetching video info: " + error.message);
  }
}

function extractYouTubeID(url) {
  const match = url.match(
    /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/
  );
  return match ? match[1] : null;
}

async function downloadVideo() {
  const selectedResolution = document.getElementById("resolution-select").value;
  const formatType = "video";

  const response = await fetch("/download", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      url: videoData.url,
      resolution: selectedResolution,
      format_type: formatType,
    }),
  });

  if (response.ok) {
    const blob = await response.blob();
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = videoData.title.replace(/[^a-z0-9]/gi, "_") + ".mp4";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  } else {
    alert("Download failed!");
    console.error(response);
  }
}
