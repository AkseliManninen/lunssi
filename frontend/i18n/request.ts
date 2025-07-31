import { getRequestConfig } from "next-intl/server";
import { defaultLocale, routing } from "./routing";

export default getRequestConfig(async ({ requestLocale }) => {
  let locale = await requestLocale;

  if (!locale || !routing.locales.includes(locale as any)) {
    locale = defaultLocale;
  }

  return {
    locale,
    messages: (await import(`../locales/${locale}.json`)).default,
  };
});
