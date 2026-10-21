"use client";

import { useTranslations } from "next-intl";
import type React from "react";
import { useLayoutEffect, useRef, useState } from "react";
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

const MAX_LIST_HEIGHT = 288;

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

  const listRef = useRef<HTMLUListElement>(null);
  // Height (px) the collapsed list is clipped to, or null if everything fits.
  const [collapsedHeight, setCollapsedHeight] = useState<number | null>(null);

  // biome-ignore lint/correctness/useExhaustiveDependencies: re-measure when the menu changes
  useLayoutEffect(() => {
    const list = listRef.current;
    if (!list) return;

    const measure = () => {
      if (list.scrollHeight <= MAX_LIST_HEIGHT) {
        setCollapsedHeight(null);
        return;
      }
      // Cut at the bottom of the last item that fully fits, keeping at least one.
      const items = Array.from(list.children) as HTMLElement[];
      let cutoff = items[0].offsetTop + items[0].offsetHeight;
      for (const item of items) {
        const bottom = item.offsetTop + item.offsetHeight;
        if (bottom > MAX_LIST_HEIGHT) break;
        cutoff = bottom;
      }
      setCollapsedHeight(cutoff < list.scrollHeight ? cutoff : null);
    };

    measure();
    const observer = new ResizeObserver(measure);
    observer.observe(list);
    return () => observer.disconnect();
  }, [menu]);

  const needsExpansion = collapsedHeight !== null;

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
        <ul
          ref={listRef}
          className="relative space-y-2 mb-4 overflow-hidden"
          style={{
            maxHeight:
              needsExpansion && !isExpanded ? collapsedHeight : undefined,
          }}
        >
          {menu.map((item) => (
            <li key={item} className="flex items-start">
              <span className="text-[#009f77] mr-2">•</span>
              <span className="text-gray-700 min-w-0 break-words">{item}</span>
            </li>
          ))}
        </ul>
        {needsExpansion && (
          <button
            type="button"
            onClick={toggleExpand}
            className="text-blue-600 hover:text-blue-800 font-medium flex items-center cursor-pointer"
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
