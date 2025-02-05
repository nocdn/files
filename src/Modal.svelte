<script>
  // @ts-nocheck

  import { fade, scale } from "svelte/transition";

  import { X } from "lucide-svelte";

  let { isOpen = false, onClose = () => {}, qrcodesrc } = $props();

  function handleBackdropClick(event) {
    if (event.target === event.currentTarget) {
      onClose();
    }
  }
</script>

{#if isOpen}
  <!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    class="fixed inset-0 bg-black/50 z-50 flex items-center justify-center transition-opacity duration-200 ease-in-out"
    onmousedown={handleBackdropClick}
    in:fade={{ duration: 100 }}
    out:fade={{ duration: 100 }}
    role="dialog"
    aria-roledescription="dialog"
  >
    <div
      class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4 p-6 transform flex flex-col gap-6 relative"
      in:scale={{ duration: 200, start: 0.97 }}
      out:scale={{ duration: 0 }}
    >
      <button
        onclick={onClose}
        class="absolute -right-2.5 -top-2.5 p-1 rounded-full bg-white border-gray-200 border-2 hover:bg-gray-100"
      >
        <X size={20} />
      </button>
      <img src={qrcodesrc} alt="" />
    </div>
  </div>
{/if}
