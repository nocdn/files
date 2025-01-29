<script>
  let { fileSize } = $props();
</script>

<div class="text-sm font-mono text-gray-400 font-semibold">
  {#if fileSize > 1024 * 1024}
    <div class="flex gap-0.75">
      <p>
        {(fileSize / (1024 * 1024)).toFixed(2)}
      </p>
      <p>MB</p>
    </div>
  {:else if fileSize > 1024}
    <div class="flex gap-0.5">
      <p>
        {(fileSize / 1024).toFixed(2)}
      </p>
      <p>KB</p>
    </div>
  {:else}
    <div class="flex gap-0.5">
      <p>
        {fileSize}
      </p>
      <p>B</p>
    </div>
  {/if}
</div>
