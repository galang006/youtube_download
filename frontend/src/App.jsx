import { useState } from "react";

function App() {
  const [url, setUrl] = useState("");
  const [formats, setFormats] = useState(null);
  const [selectedAudio, setSelectedAudio] = useState("");
  const [selectedVideo, setSelectedVideo] = useState("");
  const [selectedVideoAudio, setSelectedVideoAudio] = useState("");
  const [downloadFiles, setDownloadFiles] = useState([]);
  const [loadingFormats, setLoadingFormats] = useState(false);
  const [loadingDownload, setLoadingDownload] = useState(false);
  const API_BASE = import.meta.env.VITE_API_BASE_URL;

  const fetchFormats = async () => {
    if (!url) return;
    setFormats(null);
    setSelectedAudio("");
    setSelectedVideo("");
    setSelectedVideoAudio("");
    setDownloadFiles([]);
  
    setLoadingFormats(true);
    setFormats(null);
    try {
      const res = await fetch(`${API_BASE}/formats?url=${encodeURIComponent(url)}`);
      const data = await res.json();
      setFormats(data);
    } catch (err) {
      alert("Failed to fetch formats");
    } finally {
      setLoadingFormats(false);
    }
  };

  const downloadVideo = async () => {
    if (!selectedAudio && !selectedVideo && !selectedVideoAudio) {
      alert("Please select at least one format");
      return;
    }

    let format;
    if (selectedVideoAudio) {
      // User selected a combined audio+video format
      format = selectedVideoAudio; // e.g., "134+251"
    } else if (selectedVideo && selectedAudio) {
      // If they selected separate video and audio formats manually
      format = `${selectedVideo}+${selectedAudio}`;
    } else {
      // Only video or only audio
      format = selectedVideo || selectedAudio;
    }

    setLoadingDownload(true);
    try {
      const res = await fetch(`${API_BASE}/download`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, format }), // <-- send combined string here
      });
      const data = await res.json();
      setDownloadFiles(data.files || []);

      let urlPath;
      let downloadFileName;

      if (selectedVideoAudio) {
        // Case 1: Combined video+audio format (muxed from backend)
        const file = data.files[0]; // backend gives you the actual filename
        downloadFileName = file;
        urlPath = `/file/${encodeURIComponent(file)}`;
      } else if (selectedVideo && selectedAudio) {
        // Case 2: Separate video + audio → force <title>.mp4
        downloadFileName = `${formats.title}.mp4`;
        urlPath = `/file/${encodeURIComponent(downloadFileName)}`;
      } else if (selectedVideo || selectedAudio) {
        // Case 3: Only video OR only audio → take the single file from backend
        const file = data.files[0];
        downloadFileName = file;
        urlPath = `/file/${encodeURIComponent(file)}`;
      }

      // Auto trigger download
      const a = document.createElement("a");
      a.href = `${API_BASE}${urlPath}`;
      a.download = downloadFileName;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      
    } catch (err) {
      alert("Download failed");
    } finally {
      setLoadingDownload(false);
    }
  };

  const renderTable = (cat, selection, setSelection) => (
    <div key={cat} className="mb-6">
      <h3 className="text-lg font-semibold mb-2">{cat.replace("_", " ").toUpperCase()}</h3>
      {formats.formats[cat].length === 0 ? (
        <p className="text-gray-500">No formats available</p>
      ) : (
        <div className="overflow-x-auto border rounded shadow-sm">
          <table className="table-auto w-full text-base">
            <thead className="bg-gray-800 text-white">
              <tr>
                <th className="px-2 py-1 border">Format ID</th>
                <th className="px-2 py-1 border">Ext</th>
                <th className="px-2 py-1 border">VCodec</th>
                <th className="px-2 py-1 border">ACodec</th>
                <th className="px-2 py-1 border">Height</th>
                <th className="px-2 py-1 border">FPS</th>
                <th className="px-2 py-1 border">Size MB</th>
                <th className="px-2 py-1 border">Note</th>
                <th className="px-2 py-1 border">Select</th>
              </tr>
            </thead>
            <tbody>
              {formats.formats[cat].map((f) => (
                <tr key={f.format_id} className="hover:bg-gray-100">
                  <td className="px-2 py-1 border">{f.format_id || "-"}</td>
                  <td className="px-2 py-1 border">{f.ext || "-"}</td>
                  <td className="px-2 py-1 border">{f.vcodec === "-" ? "-" : f.vcodec}</td>
                  <td className="px-2 py-1 border">{f.acodec === "-" ? "-" : f.acodec}</td>
                  <td className="px-2 py-1 border">{f.height ?? "-"}</td>
                  <td className="px-2 py-1 border">{f.fps ?? "-"}</td>
                  <td className="px-2 py-1 border">{f.size_mb ?? "-"}</td>
                  <td className="px-2 py-1 border">{f.note || "-"}</td>
                  <td className="px-2 py-1 border text-center">
                    <input
                      type="radio"
                      name={cat}
                      value={f.format_id}
                      checked={selection === f.format_id}
                      onClick={() => setSelection(selection === f.format_id ? "" : f.format_id)}
                      className="cursor-pointer"
                    />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );

  const getSelectedFormats = () => {
    const selected = [];
    if (selectedVideoAudio) selected.push(`Video+Audio: ${selectedVideoAudio}`);
    if (selectedVideo) selected.push(`Video: ${selectedVideo}`);
    if (selectedAudio) selected.push(`Audio: ${selectedAudio}`);
    return selected.join(", ");
  };

  function extractVideoId(url) {
    const regExp = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})/;
    const match = url.match(regExp);
    return match ? match[1] : null;
  }

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-center">YouTube Downloader</h1>

      <div className="mb-4 flex flex-col sm:flex-row gap-2">
        <input
          type="text"
          placeholder="Paste YouTube URL here"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          className="border p-2 rounded flex-1"
        />
        <button
          onClick={fetchFormats}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          {loadingFormats ? "Loading..." : "Show Formats"}
        </button>
      </div>

      {formats && (
        <div className="mb-6">
          {/* Video Title */}
          <h2 className="text-xl font-bold mb-2">{formats.title}</h2>

          {/* Video Preview / Player */}
          <div className="mb-4 aspect-w-16 aspect-h-9">
            <iframe
              width="100%"
              height="360"
              src={`https://www.youtube.com/embed/${extractVideoId(url)}`}
              title={formats.title}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>

          {/* Formats Tables */}
          {renderTable("audio_video", selectedVideoAudio, setSelectedVideoAudio)}
          {renderTable("video_only", selectedVideo, setSelectedVideo)}
          {renderTable("audio_only", selectedAudio, setSelectedAudio)}

          {/* Selected Formats Badge */}
          {getSelectedFormats() && (
            <div className="mb-2">
              Selected Format:{" "}
              <span className="bg-green-100 text-green-800 px-2 py-1 rounded font-semibold">
                {getSelectedFormats()}
              </span>
            </div>
          )}

          {/* Download Button */}
          <button
            onClick={downloadVideo}
            className="mt-2 w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600"
          >
            {loadingDownload ? "Downloading..." : "Download Selected Format"}
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
