/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** Deployed Ask-the-Specs Worker URL. Unset -> the Ask page uses keyword search only. */
  readonly VITE_ASK_URL?: string;
}
interface ImportMeta {
  readonly env: ImportMetaEnv;
}
