<script>
  let { fileExtension } = $props();
</script>

{#if fileExtension === "mp3" || fileExtension === "ogg" || fileExtension === "aac" || fileExtension === "m4a"}
  <p
    class="w-fit inline-flex items-center rounded border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent px-1.5 py-0.5 text-xs font-mono bg-[#F0F9E5] text-[#496D03]"
  >
    lossy audio
  </p>
{:else if fileExtension === "wav" || fileExtension === "flac" || fileExtension === "alac" || fileExtension === "ape" || fileExtension === "wv" || fileExtension === "tak" || fileExtension === "tta" || fileExtension === "aiff" || fileExtension === "dsd" || fileExtension === "dff" || fileExtension === "dsf"}
  <p
    class="w-fit inline-flex items-center rounded border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent px-1.5 py-0.5 text-xs font-mono bg-[#F0F9E5] text-[#496D03]"
  >
    lossless audio
  </p>
{:else if fileExtension === "mp4" || fileExtension === "webm" || fileExtension === "avi" || fileExtension === "mov" || fileExtension === "wmv" || fileExtension === "flv" || fileExtension === "mkv"}
  <p
    class="w-fit inline-flex items-center rounded border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent px-1.5 py-0.5 text-xs font-mono bg-[#edeff2] text-gray-900"
  >
    video
  </p>
{:else if fileExtension === "pdf" || fileExtension === "doc" || fileExtension === "docx" || fileExtension === "odt" || fileExtension === "rtf" || fileExtension === "txt" || fileExtension === "md"}
  <p
    class="w-fit inline-flex items-center rounded border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent px-1.5 py-0.5 text-xs font-mono bg-[#EFEEFC] text-[#6220EE]"
  >
    document
  </p>
{:else if fileExtension === "zip" || fileExtension === "rar" || fileExtension === "7z" || fileExtension === "tar" || fileExtension === "gz" || fileExtension === "bz2" || fileExtension === "xz" || fileExtension === "zst" || fileExtension === "lz" || fileExtension === "lz4" || fileExtension === "lzo" || fileExtension === "z"}
  <p
    class="w-fit inline-flex items-center rounded border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent px-1.5 py-0.5 text-xs font-mono bg-[#FEF1F5] text-[#D13869]"
  >
    archive file
  </p>
{:else if fileExtension === "jpg" || fileExtension === "jpeg" || fileExtension === "webp" || fileExtension === "avif"}
  <p
    class="w-fit inline-flex items-center rounded border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent px-1.5 py-0.5 text-xs font-mono bg-[#D6F0FF] text-[#125CF3]"
  >
    lossy image
  </p>
{:else if fileExtension === "png" || fileExtension === "gif" || fileExtension === "tiff" || fileExtension === "bmp" || fileExtension === "jxl" || fileExtension === "svg"}
  <p
    class="w-fit inline-flex items-center rounded border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent px-1.5 py-0.5 text-xs font-mono bg-[#D6F0FF] text-[#125CF3]"
  >
    lossless image
  </p>
{:else if fileExtension === "js" || fileExtension === "ts" || fileExtension === "py" || fileExtension === "svelte" || fileExtension === "c" || fileExtension === "asm" || fileExtension === "cpp" || fileExtension === "h" || fileExtension === "java" || fileExtension === "html" || fileExtension === "css" || fileExtension === "php" || fileExtension === "asp" || fileExtension === "jsp" || fileExtension === "erb" || fileExtension === "ejs" || fileExtension === "sh" || fileExtension === "bash" || fileExtension === "perl" || fileExtension === "pl" || fileExtension === "rb" || fileExtension === "tcl" || fileExtension === "sql" || fileExtension === "xml" || fileExtension === "json" || fileExtension === "csv" || fileExtension === "db" || fileExtension === "exe" || fileExtension === "o" || fileExtension === "obj" || fileExtension === "lib" || fileExtension === "gradle" || fileExtension === "maven" || fileExtension === "npm" || fileExtension === "git" || fileExtension === "swift" || fileExtension === "kt" || fileExtension === "xcodeproj" || fileExtension === "cs" || fileExtension === "unity" || fileExtension === "lua" || fileExtension === "gd" || fileExtension === "yml" || fileExtension === "yaml" || fileExtension === "md" || fileExtension === "rst"}
  <p
    class="w-fit inline-flex items-center rounded border font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border-transparent px-1.5 py-0.5 text-xs font-mono bg-[#FEF1F5] text-[#D13869]"
  >
    code
  </p>
{/if}
