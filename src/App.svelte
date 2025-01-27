<script>
  import { Upload, Search, HeartCrack } from "lucide-svelte";
  import { Toaster, toast } from "svelte-sonner";
  import Spinner from "./Spinner.svelte";
  import File from "./File.svelte";
  import { onMount } from "svelte";
  import NumberFlow from "@number-flow/svelte";

  let files = $state([]);
  let loading = $state(true);
  let uploading = $state(false);

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
    const fileInput = document.getElementById("file-input");
    const file = fileInput.files[0];

    if (!file) {
      toast.error("Please select a file first");
      return;
    }

    uploading = true;
    const toastId = toast.loading("Getting upload URL...");

    try {
      // Get the presigned URL
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

      // Upload the file using the presigned URL
      toast.loading("Uploading file...", { id: toastId });
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

      // Clear the file input
      fileInput.value = "";

      // Refresh the file list
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
</script>

<main class="grid grid-cols-[30%_70%] gap-4 p-8 h-screen w-screen">
  <!-- upload files -->
  <div id="uploads" class="flex flex-col gap-2">
    <p style="letter-spacing: -0.5px;" class="font-mono font-semibold">
      Upload a file
    </p>
    <form class="" onsubmit|preventDefault>
      <label for="file-input" class="sr-only">Choose file</label>
      <input
        type="file"
        name="file-input"
        id="file-input"
        class="block w-full border border-gray-200 drop-shadow-xs rounded-lg text-sm focus:z-10 focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none
        file:bg-gray-50 file:border-0
        file:me-4
        file:py-3 file:px-4
       "
        disabled={uploading}
      />
    </form>
    <button
      type="button"
      on:click={handleUpload}
      disabled={uploading}
      class="py-2 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-700 dark:focus:bg-neutral-700"
    >
      {#if uploading}
        <Spinner /> Uploading...
      {:else}
        Upload <Upload size={16} />
      {/if}
    </button>
  </div>
  <!-- files list -->
  <div id="files" class="w-full flex flex-col gap-2">
    <p style="letter-spacing: -0.5px;" class="font-mono font-semibold">
      Files count - <NumberFlow value={filesCount} />
    </p>
    <div
      class="h-full font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm p-5 pl-6 flex flex-col gap-3 overflow-y-scroll"
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
            <File fileName={file.fileName} downloadURL={file.downloadURL} />
          </div>
        {/each}
      {/if}
    </div>
  </div>
</main>

<Toaster offset="1.5rem" />
