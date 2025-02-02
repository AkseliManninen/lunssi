"use client";

import ChevronDownIcon from "@/assets/icons/chevron-down.svg";
import { useI18n } from "@/locales/client";
import { useChangeLocale, useCurrentLocale } from "@/locales/client";
import React from "react";

import i18nConfig from "@/i18nConfig";

const LanguageChanger = () => {
  const changeLocale = useChangeLocale();
  const currentLocale = useCurrentLocale();
  const t = useI18n();

  return (
    <div className="relative inline-block">
      <label className="mr-1" htmlFor="language-switcher">
        {t("language")}:
      </label>
      <select
        id="language-switcher"
        onChange={(e) => changeLocale(e.target.value as typeof currentLocale)}
        value={currentLocale}
        className="appearance-none bg-white border border-gray-300 rounded-md py-2 pl-3 pr-8 shadow-xs focus:outline-hidden focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
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
