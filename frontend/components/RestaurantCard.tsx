"use client";

import { useTranslations } from "next-intl";
import type React from "react";
import { useMemo, useState } from "react";
import ChevronDownIcon from "@/assets/icons/chevron-down.svg";
import ChevronUpIcon from "@/assets/icons/chevron-up.svg";
import DiscountIcon from "@/assets/icons/discount.svg";
import LocationIcon from "@/assets/icons/map-pin.svg";

export interface RestaurantCardProps {
  discount?: string;
  isStudentCantine: boolean;
  location: string;
  lunchHours: string;
  lunchPrice: string;
  menu: string[];
  name: string;
  url: string;
}

const RestaurantCard: React.FC<RestaurantCardProps> = ({
  discount,
  location,
  lunchHours,
  lunchPrice,
  menu,
  name,
  url,
}) => {
  const t = useTranslations();
  const [isExpanded, setIsExpanded] = useState(false);

  const maxCharacters = 300;

  const { displayedItems, needsExpansion } = useMemo(() => {
    let totalLength = 0;
    let cutoffIndex = menu.length;

    for (let i = 0; i < menu.length; i++) {
      totalLength += menu[i].length;
      if (totalLength > maxCharacters && !isExpanded) {
        cutoffIndex = i;
        break;
      }
    }

    const onlyOneItem = menu.length === 1;

    return {
      displayedItems: onlyOneItem
        ? menu
        : isExpanded
          ? menu
          : menu.slice(0, cutoffIndex),
      needsExpansion: !onlyOneItem && totalLength > maxCharacters,
    };
  }, [menu, isExpanded]);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-visible transition-transform duration-300 hover:shadow-lg hover:-translate-y-1 flex flex-col h-full">
      <div className="px-6 py-4 grow">
        <h2 className="font-bold text-xl mb-4 text-gray-800 flex items-center gap-2">
          <a
            href={url}
            target="_blank"
            rel="noopener noreferrer"
            className="hover:underline hover:text-blue-700 text-gray-800"
          >
            {name}
          </a>
          <div className="flex items-center gap-1">
            {location && location.length > 0 && (
              <div className="relative group">
                <a
                  href={location}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="cursor-pointer"
                >
                  <LocationIcon className="cursor-pointer" />
                </a>
                <div className="absolute top-full mt-1 invisible group-hover:visible left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-xs rounded py-1 px-2 whitespace-nowrap z-10 shadow-md">
                  {t("openInMaps")}
                </div>
              </div>
            )}
            {discount && (
              <div className="relative group">
                <DiscountIcon className="cursor-help" />
                <div className="absolute top-full invisible group-hover:visible left-1/2 transform -translate-x-1/2 bg-gray-800 text-white text-sm rounded-sm py-1 px-2 w-32">
                  {discount}
                </div>
              </div>
            )}
          </div>
        </h2>
        <ul className="space-y-2 mb-4">
          {displayedItems.map((item) => (
            <li key={item} className="flex items-start">
              <span className="text-[#009f77] mr-2">•</span>
              <span className="text-gray-700">{item}</span>
            </li>
          ))}
        </ul>
        {needsExpansion && (
          <button
            type="button"
            onClick={toggleExpand}
            className="text-blue-600 hover:text-blue-800 font-medium flex items-center"
          >
            {isExpanded ? (
              <>
                <span>{t("showLess")}</span>
                <ChevronUpIcon className="ml-1" />
              </>
            ) : (
              <>
                <span>{t("showMore")}</span>
                <ChevronDownIcon className="ml-1" />
              </>
            )}
          </button>
        )}
      </div>
      <div className="px-6 py-4 bg-gray-50 border-t border-gray-200">
        <div className="flex justify-between items-center text-sm text-gray-600">
          <p>
            <span className="font-medium">{t("price")}:</span> {lunchPrice}
          </p>
          <p>
            <span className="font-medium">{t("lunchAvailable")}:</span>{" "}
            {lunchHours}
          </p>
        </div>
      </div>
    </div>
  );
};

export default RestaurantCard;
