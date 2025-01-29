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

  import FileChip from "./FileChip.svelte";

  let { fileName, downloadURL, onDelete, onEdit } = $props();

  let tempCopied = $state(false);
  function copyToClipoard(link) {
    navigator.clipboard.writeText(link);
    tempCopied = true;
    setTimeout(() => {
      tempCopied = false;
    }, 1500);
  }

  let isEditingTitle = $state(false);
  let newFileName = $state("");
  function handleEditing(action) {
    if (action === "editing") {
      isEditingTitle = true;
      newFileName = fileName;
    } else if (action === "saving") {
      isEditingTitle = false;
      onEdit(fileName, newFileName);
      fileName = newFileName;
      // console.log("New filename", fileName);
    } else if (action === "cancelling") {
      isEditingTitle = false;
      // console.log("cancelled editing");
    }
  }

  let copyButtonActive = $state(false);
  let deleteButtonActive = $state(false);
  let downloadButtonActive = $state(false);

  let hoveringContainer = $state(false);
</script>

<!-- svelte-ignore a11y_mouse_events_have_key_events -->
<main
  onmouseover={() => {
    hoveringContainer = true;
  }}
  onmouseleave={() => {
    hoveringContainer = false;
  }}
  class="flex w-full justify-between items-center"
>
  <div class="flex items-center gap-3 w-full">
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
    <!-- svelte-ignore a11y_click_events_have_key_events -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <!-- svelte-ignore a11y_missing_attribute -->
    <div class="flex flex-col gap-0.5">
      <!-- svelte-ignore a11y_click_events_have_key_events -->
      {#if !isEditingTitle}
        <a
          onclick={() => {
            handleEditing("editing");
          }}
        >
          {fileName}
        </a>
      {:else}
        <input
          id="editingFileName"
          class="w-96"
          type="text"
          bind:value={newFileName}
          onkeydown={(e) => {
            if (e.key === "Enter") {
              handleEditing("saving");
            } else if (e.key === "Escape") {
              handleEditing("cancelling");
            }
          }}
        />
      {/if}
      <div class="flex items-center gap-3">
        <FileChip fileExtension={fileName.split(".").pop().toLowerCase()} />
        <p class="text-sm font-mono text-gray-400 font-semibold">
          {Math.floor(Math.random() * 150)}mb
        </p>
      </div>
    </div>
  </div>
  <div
    class="flex gap-3 {hoveringContainer
      ? 'opacity-100'
      : 'opacity-40'} transition-opacity duration-150 linear"
  >
    <button
      onclick={() => {
        console.log("copying...");
        copyToClipoard(downloadURL);
      }}
      onmousedown={() => {
        copyButtonActive = true;
      }}
      onmouseup={() => {
        copyButtonActive = false;
      }}
      class="py-2 px-3 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none hover:bg-blue-50 hover:text-blue-800 hover:border-blue-200 dark:hover:bg-blue-600 dark:hover:text-white dark:hover:border-blue-600 transition-transform duration-50 ease-in-out transform {copyButtonActive
        ? 'scale-95'
        : ''}"
    >
      {#if tempCopied}
        <Check size={16} strokeWidth={2.75} />
      {:else}
        <Link size={16} />
      {/if}
    </button>
    <button
      onmousedown={() => {
        deleteButtonActive = true;
      }}
      onmouseup={() => {
        deleteButtonActive = false;
      }}
      onclick={onDelete(fileName)}
      class="py-2 px-3 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none hover:bg-red-50 hover:text-red-700 hover:border-red-200 dark:hover:bg-red-600 dark:hover:text-white dark:hover:border-red-600 transition-transform duration-50 ease-in-out transform {deleteButtonActive
        ? 'scale-95'
        : ''}"
    >
      <Trash2 size={16} />
    </button>
    <a
      onmousedown={() => {
        downloadButtonActive = true;
      }}
      onmouseup={() => {
        downloadButtonActive = false;
      }}
      type="button"
      href={downloadURL}
      class="py-2 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-700 dark:focus:bg-neutral-700 transition-transform duration-50 ease-in-out transform {downloadButtonActive
        ? 'scale-95'
        : ''}"
    >
      Download <Download size={16} />
    </a>
  </div>
</main>
