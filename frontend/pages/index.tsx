import Image from "next/image";
import React, { useEffect, useState } from "react";
import { Inter } from "next/font/google";
import axios from "axios";
import RestaurantCard from "../components/RestaurantCard";

const inter = Inter({ subsets: ["latin"] });

interface Restaurant {
  name: string;
  lunchItems: string[];
  lunchPrice: number;
  lunchTime: string;
}

const Home: React.FC = () => {
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);

  useEffect(() => {
    axios
      .get("http://localhost:8000/restaurant")
      .then((response) => {
        setRestaurant(response.data);
      })
      .catch((error) => {
        console.error("Error fetching the restaurant data:", error);
      });
  }, []);

  if (!restaurant) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex flex-col items-center">
      <h1 className="text-3xl font-bold my-8">Lunssi</h1>
      <RestaurantCard
        name={restaurant.name}
        lunchItems={restaurant.lunchItems}
        lunchPrice={restaurant.lunchPrice}
        lunchTime={restaurant.lunchTime}
      />
    </div>
  );
};

export default Home;
