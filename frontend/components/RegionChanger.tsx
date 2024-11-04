"use client";

import ChevronDownIcon from "@/assets/icons/chevron-down.svg";
import { defaultRegion, regions } from "@/utils/constants";
import { usePathname, useRouter } from "next/navigation";
import type { ChangeEvent } from "react";
import React from "react";
import { useTranslation } from "react-i18next";

interface Props {
  currentRegion: string;
}

const RegionChanger = ({ currentRegion }: Props) => {
  const router = useRouter();
  const pathname = usePathname();
  const { t } = useTranslation();

  const handleChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const newRegion = e.target.value;
    const newPath = pathname.includes(currentRegion)
      ? pathname.replace(currentRegion, newRegion)
      : `/${newRegion}`;

    // don't include default region in path
    router.push(newPath.replace(`/${defaultRegion}`, "/"));
  };

  return (
    <div className="relative inline-block">
      <label className="mr-1" htmlFor="region-switcher">
        {t("region")}:
      </label>
      <select
        id="region-switcher"
        onChange={handleChange}
        value={currentRegion}
        className="appearance-none bg-white border border-gray-300 rounded-md py-2 pl-3 pr-8 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
      >
        {regions.map(({ id, label }) => (
          <option key={id} value={id} className="py-1">
            {label}
          </option>
        ))}
      </select>
      <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-700">
        <ChevronDownIcon />
      </div>
    </div>
  );
};

export default RegionChanger;
