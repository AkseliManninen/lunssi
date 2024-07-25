import React from "react";

interface RestaurantCardProps {
  name: string;
  lunchItems: string[];
  lunchPrice: number;
  lunchTime: string;
}

const RestaurantCard: React.FC<RestaurantCardProps> = ({
  name,
  lunchItems,
  lunchPrice,
  lunchTime,
}) => {
  return (
    <div className="max-w-sm rounded overflow-hidden shadow-lg m-4">
      <div className="px-6 py-4">
        <div className="font-bold text-xl mb-2">{name}</div>
        <ul className="list-disc list-inside mb-4">
          {lunchItems.map((item, index) => (
            <li key={index}>{item}</li>
          ))}
        </ul>
        <p className="text-gray-700 text-base">
          Lunch Price: ${lunchPrice.toFixed(2)}
        </p>
        <p className="text-gray-700 text-base">Lunch Time: {lunchTime}</p>
      </div>
    </div>
  );
};

export default RestaurantCard;
