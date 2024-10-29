import { defaultLocale } from "@/i18nConfig";

export const getLocalizedLink = (link: string, locale: string): string => {
  return locale === defaultLocale ? link : `${link}/${locale}`;
};
