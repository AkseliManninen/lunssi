"use client";

import ChevronDownIcon from "@/assets/icons/chevron-down.svg";
import { useCurrentLocale } from "next-i18n-router/client";
import { usePathname, useRouter } from "next/navigation";
import type { ChangeEvent } from "react";
import React from "react";
import { useTranslation } from "react-i18next";

import i18nConfig from "@/i18nConfig";

const LanguageChanger = () => {
  const currentLocale = useCurrentLocale(i18nConfig);
  const router = useRouter();
  const currentPathname = usePathname();
  const { t } = useTranslation();

  const handleChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const newLocale = e.target.value;

    // set cookie for next-i18n-router
    const days = 30;
    const date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    document.cookie = `NEXT_LOCALE=${newLocale};expires=${date.toUTCString()};path=/`;

    // redirect to the new locale path
    if (
      currentLocale === i18nConfig.defaultLocale &&
      !i18nConfig.prefixDefault
    ) {
      router.push(`/${newLocale}${currentPathname}`);
    } else {
      router.push(
        currentPathname.replace(`/${currentLocale}`, `/${newLocale}`),
      );
    }

    router.refresh();
  };

  return (
    <div className="relative inline-block">
      <label className="mr-1" htmlFor="language-switcher">
        {t("language")}:
      </label>
      <select
        id="language-switcher"
        onChange={handleChange}
        value={currentLocale}
        className="appearance-none bg-white border border-gray-300 rounded-md py-2 pl-3 pr-8 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
      >
        {i18nConfig.locales.map((locale: string) => (
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
