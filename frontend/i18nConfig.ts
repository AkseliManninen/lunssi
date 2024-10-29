import type { Config } from "next-i18n-router/dist/types";

export const defaultLocale = "fi";

const i18nConfig: Config = {
  locales: [defaultLocale, "en"],
  defaultLocale,
};

export default i18nConfig;
