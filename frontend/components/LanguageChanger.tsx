"use client";

import { useParams } from "next/navigation";
import { type Locale, useLocale, useTranslations } from "next-intl";
import { type ChangeEvent, startTransition } from "react";
import ChevronDownIcon from "@/assets/icons/chevron-down.svg";
import { routing, usePathname, useRouter } from "@/i18n/routing";

const LanguageChanger = () => {
  const router = useRouter();
  const t = useTranslations();
  const pathname = usePathname();
  const currentLocale = useLocale();
  const params = useParams();

  const handleLanguageChange = (event: ChangeEvent<HTMLSelectElement>) => {
    const nextLocale = event.target.value as Locale;

    startTransition(() => {
      router.replace(
        // @ts-expect-error -- TypeScript will validate that only known `params`
        // are used in combination with a given `pathname`. Since the two will
        // always match for the current route, we can skip runtime checks.
        { params, pathname },
        { locale: nextLocale },
      );
    });
  };

  return (
    <div className="relative inline-block">
      <label className="mr-1" htmlFor="language-switcher">
        {t("language")}:
      </label>
      <select
        id="language-switcher"
        onChange={handleLanguageChange}
        value={currentLocale}
        className="appearance-none bg-white border border-gray-300 rounded-md py-2 pl-3 pr-8 shadow-xs focus:outline-hidden focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
      >
        {routing.locales.map((locale: string) => (
          <option key={locale} value={locale} className="py-1">
            {locale.toUpperCase()}
          </option>
        ))}
      </select>
      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
        <ChevronDownIcon />
      </div>
    </div>
  );
};

export default LanguageChanger;
