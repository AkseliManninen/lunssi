"use client";

import ChevronDownIcon from "@/assets/icons/chevron-down.svg";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import type { ChangeEvent } from "react";
import React from "react";
import { useTranslation } from "react-i18next";

const regions = [
  { id: "kamppi", label: "Helsinki - Kamppi" },
  { id: "tampere", label: "Tampere" },
];

const RegionChanger = () => {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { t } = useTranslation();

  const currentRegion = searchParams.get("region") || regions[0].id;

  const handleChange = (e: ChangeEvent<HTMLSelectElement>) => {
    const newRegion = e.target.value;
    const current = new URLSearchParams(Array.from(searchParams.entries()));

    if (newRegion) {
      current.set("region", newRegion);
    } else {
      current.delete("region");
    }

    // Create new URL with updated search params
    const search = current.toString();
    const query = search ? `?${search}` : "";

    router.push(`${pathname}${query}`);
    router.refresh();
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
