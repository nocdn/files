<script>
  import NumberFlow from "@number-flow/svelte";
  import { CircleStop, CirclePause } from "lucide-svelte";
  let { value, onCancel, onPause } = $props();

  let visible = $state(false);
  let showingDisappearingClasses = $state(false);

  $effect(() => {
    if (value > 0) {
      visible = true;
    }
    if (value === 100) {
      showingDisappearingClasses = true;
      setTimeout(() => {
        visible = false;
      }, 200);
    }
  });
</script>

{#if visible}
  <div
    class={showingDisappearingClasses
      ? "motion-opacity-out-0 motion-translate-y-out-50 motion-blur-out-md motion-duration-200"
      : "motion-opacity-in-0 motion-translate-y-in-100 motion-blur-in-md motion-duration-200"}
  >
    <div class="flex justify-between align-middle mb-1">
      <span
        class="text-sm font-medium font-sfmono text-blue-700 dark:text-white"
        >progress</span
      >
      <div class="flex align-middle items-center gap-2">
        <div class="flex gap-1.5 align-middle items-center">
          <div
            class="opacity-35 hover:opacity-100 cursor-pointer hover:text-blue-500"
          >
            <CirclePause
              size={13}
              strokeWidth={2.25}
              onclick={() => {
                console.log("pausing...");
                onPause();
              }}
            />
          </div>
          <div
            class="opacity-35 hover:opacity-100 cursor-pointer hover:text-red-500"
          >
            <CircleStop size={13} strokeWidth={2.25} onclick={onCancel} />
          </div>
        </div>
        <span
          class="text-sm font-medium font-sfmono text-blue-700 dark:text-white"
          ><NumberFlow {value} />%</span
        >
      </div>
    </div>
    <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
      <div
        class="bg-blue-600 h-2.5 rounded-full"
        style="width: {value}%; transition: width 0.4s cubic-bezier(0.32, 0.72, 0, 1)"
      ></div>
    </div>
  </div>
{/if}
