<script>
  import { Upload, Search, HeartCrack } from "lucide-svelte";
  import { Toaster, toast } from "svelte-sonner";
  import Spinner from "./Spinner.svelte";
  import Reload from "./Reload.svelte";
  import File from "./File.svelte";
  import { onMount } from "svelte";
  import NumberFlow from "@number-flow/svelte";

  let files = $state([]);
  let loading = $state(true);
  let uploading = $state(false);
  let fileInput;
  let fileInputValue;
  let isDragging = $state(false);

  async function fetchFiles() {
    loading = true;
    const response = await fetch(
      "https://7lqxtynf6xcfto7c3pxoqvipye0vokfk.lambda-url.eu-west-2.on.aws/"
    );
    files = await response.json();
    loading = false;
    console.log(files);
  }

  async function handleUpload() {
    const file = fileInput?.files[0];

    if (!file) {
      toast.error("Please select a file first");
      return;
    }

    uploading = true;
    const toastId = toast.loading("Getting upload URL...");

    try {
      const response = await fetch(
        "https://7lqxtynf6xcfto7c3pxoqvipye0vokfk.lambda-url.eu-west-2.on.aws/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            fileName: file.name,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to get upload URL");
      }

      const { uploadURL } = await response.json();

      const uploadResponse = await fetch(uploadURL, {
        method: "PUT",
        body: file,
        headers: {
          "Content-Type": file.type,
        },
      });

      if (!uploadResponse.ok) {
        throw new Error("Failed to upload file");
      }

      toast.success("File uploaded successfully!", { id: toastId });
      fileInputValue = "";
      await fetchFiles();
    } catch (error) {
      console.error("Upload error:", error);
      toast.error("Failed to upload file", { id: toastId });
    } finally {
      uploading = false;
    }
  }

  let filesCount = $derived(files.length);
  fetchFiles();

  let inputField;
  onMount(() => {
    inputField.focus();
  });

  let searchQuery = $state("");
  let searchResults = $derived(
    files.filter((file) =>
      searchQuery.length === 0
        ? true
        : file.fileName.toLowerCase().includes(searchQuery.toLowerCase())
    )
  );

  $effect(() => {
    console.log("Search query:", searchQuery);
  });

  function handleDrop(event) {
    event.preventDefault();
    isDragging = false;
    const droppedFiles = event.dataTransfer.files;
    if (droppedFiles.length > 0) {
      fileInput.files = droppedFiles;
      handleUpload();
    }
  }

  async function deleteFile(fileName) {
    try {
      console.log("Deleting file:", fileName);
      const response = await fetch(
        "https://7lqxtynf6xcfto7c3pxoqvipye0vokfk.lambda-url.eu-west-2.on.aws/",
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ fileName }),
        }
      );
      if (!response.ok) {
        throw new Error("Failed to delete file");
      }
      const data = await response.json();
      console.log(data.message);
      await fetchFiles();
      toast.success("File deleted successfully", { duration: 750 });
    } catch (error) {
      console.error(error);
    }
  }
  let reloadSpinAnimation = $state(false);

  async function editFile(oldFileName, newFileName) {
    console.log("old file name", oldFileName);
    console.log("new file name", newFileName);

    try {
      console.log(`renaming file: ${oldFileName} -> ${newFileName}`);
      const response = await fetch(
        "https://7lqxtynf6xcfto7c3pxoqvipye0vokfk.lambda-url.eu-west-2.on.aws/",
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            oldFileName: oldFileName,
            newFileName: newFileName,
          }),
        }
      );
      if (!response.ok) {
        throw new Error("Failed to rename file");
      }
      const data = await response.json();
      console.log(data.message);
      await fetchFiles();
      toast.success("File renamed successfully", {
        duration: 2000,
        description: `${oldFileName} -> ${newFileName}`,
      });
    } catch (error) {
      console.error(error);
    }
  }
</script>

<main
  class="fixed inset-0 grid grid-cols-[30%_70%] gap-4 p-8"
  ondragover={(event) => {
    event.preventDefault();
    isDragging = true;
  }}
  ondragenter={(event) => {
    event.preventDefault();
    isDragging = true;
  }}
  ondragleave={(event) => {
    event.preventDefault();
    isDragging = false;
  }}
  ondrop={(event) => {
    event.preventDefault();
    handleDrop(event);
    isDragging = false;
  }}
>
  {#if isDragging}
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div
      ondrop={handleDrop}
      class="absolute inset-0 bg-black/65 z-50 flex flex-col justify-center items-center text-white p-3"
    >
      <div class="w-full h-full border-2 border-white border-dashed rounded-sm">
        <div class="grid place-content-center h-full">
          <div class="flex flex-col items-center gap-0.5">
            <p class="text-xl font-semibold font-mono">Drop the file</p>
            <p class="text-sm font-semibold font-mono">do it.</p>
          </div>
        </div>
      </div>
    </div>
  {/if}

  <div id="uploads" class="flex flex-col gap-2 h-fit">
    <p style="letter-spacing: -0.5px;" class="font-mono font-semibold">
      Upload a file
    </p>
    <form>
      <label for="file-input" class="sr-only">Choose file</label>
      <input
        type="file"
        name="file-input"
        id="file-input"
        class="block w-full border border-gray-200 drop-shadow-xs rounded-lg text-sm focus:z-10 focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none file:bg-gray-50 file:border-0 file:me-4 file:py-3 file:px-4"
        disabled={uploading}
        bind:this={fileInput}
        bind:value={fileInputValue}
      />
    </form>
    <button
      type="button"
      onclick={handleUpload}
      disabled={uploading}
      class="py-2.5 px-4 font-mono font-semibold inline-flex justify-center items-center gap-x-2 text-sm rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-700 dark:focus:bg-neutral-700"
    >
      {#if uploading}
        <Spinner /> Uploading...
      {:else}
        Upload <Upload size={16} />
      {/if}
    </button>
  </div>

  <div id="files" class="flex flex-col h-full overflow-hidden">
    <div class="flex justify-between pr-2 mb-2">
      <p style="letter-spacing: -0.5px;" class="font-mono font-semibold">
        Files count - <NumberFlow value={filesCount} />
      </p>
      <button
        onclick={() => {
          fetchFiles();
          reloadSpinAnimation = true;
          setTimeout(() => {
            reloadSpinAnimation = false;
          }, 750);
        }}
        class="cursor-pointer"
        style={reloadSpinAnimation
          ? "animation: spin 0.75s cubic-bezier(0.165, 0.84, 0.44, 1) infinite"
          : ""}
      >
        <Reload />
      </button>
    </div>

    <div
      class="flex-1 font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm p-5 pl-6 flex flex-col gap-3 overflow-y-auto"
    >
      <div class="flex gap-2 items-center mb-3 pl-2">
        <Search size={16} color="gray" strokeWidth={2.5} />
        <input
          bind:this={inputField}
          bind:value={searchQuery}
          type="text"
          placeholder="Search files"
          class="w-full active:outline-none active:ring-0 focus:outline-none focus:ring-0"
        />
      </div>
      {#if loading}
        <div class="flex flex-col items-center justify-center gap-1 mt-6">
          <Spinner />
          <p class="text-center text-gray-500">Fetching files...</p>
        </div>
      {:else if searchQuery && searchResults.length === 0}
        <div class="flex flex-col items-center justify-center gap-1 mt-6">
          <p class="text-center text-gray-500">No files found</p>
          <HeartCrack size={20} color="gray" strokeWidth={2} />
        </div>
      {:else}
        {#each searchResults as file}
          <div class="flex gap-3 justify-center items-center">
            <File
              fileName={file.fileName}
              downloadURL={file.downloadURL}
              fileSize={file.fileSize}
              onDelete={deleteFile}
              onEdit={editFile}
            />
          </div>
        {/each}
      {/if}
    </div>
  </div>
</main>

<Toaster offset="1.5rem" />
