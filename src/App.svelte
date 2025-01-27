<script>
  import { Upload, Search, HeartCrack } from "lucide-svelte";
  import { Toaster, toast } from "svelte-sonner";
  import Spinner from "./Spinner.svelte";
  import File from "./File.svelte";
  import { onMount } from "svelte";

  import NumberFlow from "@number-flow/svelte";

  let files = $state([]);
  let loading = $state(true);

  async function fetchFiles() {
    loading = true;
    const respone = await fetch(
      "https://7lqxtynf6xcfto7c3pxoqvipye0vokfk.lambda-url.eu-west-2.on.aws/"
    );
    files = await respone.json();
    loading = false;
    console.log(files);
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
    <form class="">
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
      />
    </form>
    <button
      type="button"
      onclick={() =>
        toast.success("Uploading...", {
          icon: Spinner,
        })}
      class="py-2 px-4 inline-flex justify-center items-center gap-x-2 text-sm font-medium rounded-lg border border-gray-200 bg-white text-gray-800 shadow-sm hover:bg-gray-50 focus:outline-none focus:bg-gray-50 disabled:opacity-50 disabled:pointer-events-none dark:bg-neutral-800 dark:border-neutral-700 dark:text-white dark:hover:bg-neutral-700 dark:focus:bg-neutral-700"
    >
      Upload <Upload size={16} />
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
