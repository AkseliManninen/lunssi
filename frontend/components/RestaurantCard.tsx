"use client";

import ChevronDownIcon from "@/assets/icons/chevron-down.svg";
import ChevronUpIcon from "@/assets/icons/chevron-up.svg";
import type React from "react";
import { useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

export interface RestaurantCardProps {
  name: string;
  lunchItems: string[];
  lunchPrice: string;
  lunchTime: string;
}

const RestaurantCard: React.FC<RestaurantCardProps> = ({
  name,
  lunchItems,
  lunchPrice,
  lunchTime,
}) => {
  const { t } = useTranslation();
  const [isExpanded, setIsExpanded] = useState(false);

  const maxCharacters = 300;

  const { displayedItems, needsExpansion } = useMemo(() => {
    let totalLength = 0;
    let cutoffIndex = lunchItems.length;

    for (let i = 0; i < lunchItems.length; i++) {
      totalLength += lunchItems[i].length;
      if (totalLength > maxCharacters && !isExpanded) {
        cutoffIndex = i;
        break;
      }
    }

    return {
      displayedItems: isExpanded
        ? lunchItems
        : lunchItems.slice(0, cutoffIndex),
      needsExpansion: totalLength > maxCharacters,
    };
  }, [lunchItems, isExpanded]);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden transition-transform duration-300 hover:shadow-lg hover:-translate-y-1 flex flex-col h-full">
      <div className="px-6 py-4 flex-grow">
        <h2 className="font-bold text-xl mb-4 text-gray-800">{name}</h2>
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
            {lunchTime}
          </p>
        </div>
      </div>
    </div>
  );
};

export default RestaurantCard;
