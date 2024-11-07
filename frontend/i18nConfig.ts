export const defaultLocale = "fi";

const i18nConfig = {
  locales: [defaultLocale, "en"],
  defaultLocale,
  urlMappingStrategy: "rewriteDefault" as
    | "redirect"
    | "rewrite"
    | "rewriteDefault",
};

export default i18nConfig;
