<script>
  import NumberFlow from "@number-flow/svelte";
  let { value } = $props();
</script>

{#if value > 0 && value < 100}
  <div class="flex justify-between align-middle mb-1">
    <span class="text-sm font-medium font-sfmono text-blue-700 dark:text-white"
      >progress</span
    >
    <span class="text-sm font-medium font-sfmono text-blue-700 dark:text-white"
      ><NumberFlow {value} />%</span
    >
  </div>
  <div class="w-full bg-gray-200 rounded-full h-2.5 dark:bg-gray-700">
    <div
      class="bg-blue-600 h-2.5 rounded-full"
      style="width: {value}%; transition: width 0.4s cubic-bezier(0.32, 0.72, 0, 1)"
    ></div>
  </div>
{/if}
