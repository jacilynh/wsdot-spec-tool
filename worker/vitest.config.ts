import { defineConfig } from "vitest/config";

// The pure logic (retrieval, prompt building, cost, validation) is tested in the node
// environment. The fetch handler itself is exercised end-to-end only against a deployed
// Worker — it needs Cloudflare bindings and an API key that aren't present here.
export default defineConfig({
  test: { environment: "node", include: ["src/**/*.test.ts"] },
});
