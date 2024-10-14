"use client";

import type React from "react";
import { useTranslation } from "react-i18next";

interface RestaurantCardProps {
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
  return (
    <div className="max-w-sm rounded overflow-hidden shadow-lg m-4">
      <div className="px-6 py-4">
        <div className="font-bold text-xl mb-2">{name}</div>
        <ul className="list-disc list-inside mb-4">
          {lunchItems.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
        <p className="text-gray-700 text-base">
          {t("price")}: {lunchPrice}
        </p>
        <p className="text-gray-700 text-base">
          {t("lunchAvailable")}: {lunchTime}
        </p>
      </div>
    </div>
  );
};

export default RestaurantCard;
