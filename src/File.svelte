<script>
  import {
    Download,
    Trash2,
    FileArchive,
    FileAudio2,
    FileCode2,
    Image,
    FileSpreadsheet,
    FileText,
    FileVideo2,
    File,
    Link,
    Check,
  } from "lucide-svelte";

  let { fileName, downloadURL } = $props();

  let tempCopied = $state(false);
  function copyToClipoard(link) {
    navigator.clipboard.writeText(link);
    tempCopied = true;
    setTimeout(() => {
      tempCopied = false;
    }, 1500);
  }
</script>

<main class="flex w-full justify-between items-center">
  <div class="flex items-center gap-3">
    <div
      class="py-3 px-3 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800"
    >
      {#if fileName.endsWith(".zip")}
        <FileArchive size={16} color="red" strokeWidth={2.25} />
      {:else if fileName.endsWith(".txt")}
        <FileText size={16} color="purple" strokeWidth={2.25} />
      {:else if fileName.endsWith(".csv")}
        <FileSpreadsheet size={16} strokeWidth={2.25} />
      {:else if fileName.endsWith(".mp4") || fileName.endsWith(".webm") || fileName.endsWith(".mkv") || fileName.endsWith(".avi") || fileName.endsWith(".mov")}
        <FileVideo2 size={16} strokeWidth={2.25} />
      {:else if fileName.endsWith(".jpg") || fileName.endsWith(".JPG") || fileName.endsWith(".jpeg") || fileName.endsWith(".png") || fileName.endsWith(".gif") || fileName.endsWith(".webp") || fileName.endsWith(".svg") || fileName.endsWith(".avif")}
        <Image size={16} color={"blue"} strokeWidth={2.25} />
      {:else if fileName.endsWith(".js") || fileName.endsWith(".mjs") || fileName.endsWith(".cjs") || fileName.endsWith(".ts") || fileName.endsWith(".jsx") || fileName.endsWith(".tsx") || fileName.endsWith(".py") || fileName.endsWith(".pyw") || fileName.endsWith(".pyc") || fileName.endsWith(".pyd") || fileName.endsWith(".pyo") || fileName.endsWith(".pyi")}
        <FileCode2 size={16} color={"#FF0032"} strokeWidth={2.25} />
      {:else if fileName.endsWith(".mp3") || fileName.endsWith(".wav") || fileName.endsWith(".ogg") || fileName.endsWith(".flac") || fileName.endsWith(".aac") || fileName.endsWith(".m4a")}
        <FileAudio2 size={16} color={"darkgreen"} strokeWidth={2.25} />
      {:else}
        <File size={16} />
      {/if}
    </div>
    <div class="flex flex-col gap-0.5">
      <p>{fileName}</p>
      <p class="text-xs text-gray-400">
        Uploaded {new Date(Date.now()).toLocaleDateString()}
      </p>
    </div>
  </div>
  <div class="flex gap-3">
    <button
      onmousedown={() => {
        console.log("copying...");
        copyToClipoard(downloadURL);
      }}
      class="py-2 px-3 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none hover:bg-blue-50 hover:text-blue-800 hover:border-blue-200 dark:hover:bg-blue-600 dark:hover:text-white dark:hover:border-blue-600"
    >
      {#if tempCopied}
        <Check size={16} />
      {:else}
        <Link size={16} />
      {/if}
    </button>
    <button
      class="py-2 px-3 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none hover:bg-red-50 hover:text-red-700 hover:border-red-200 dark:hover:bg-red-600 dark:hover:text-white dark:hover:border-red-600"
    >
      <Trash2 size={16} />
    </button>
    <a
      type="button"
      href={downloadURL}
      class="py-2 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-700 dark:focus:bg-neutral-700"
    >
      Download <Download size={16} />
    </a>
  </div>
</main>
