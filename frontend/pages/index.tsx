import React, { useEffect, useState } from "react";
import axios from "axios";
import RestaurantCard from "../components/RestaurantCard";

interface Restaurant {
  name: string;
  lunchItems: string[];
  lunchPrice: string;
  lunchTime: string;
}

const Home: React.FC = () => {
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [restaurant2, setRestaurant2] = useState<Restaurant | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const restaurantName = "bruuveri"; // Change to the actual restaurant name if needed
    axios
      .get(`http://localhost:8000/restaurant?name=${restaurantName}`)
      .then((response) => {
        setRestaurant(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching the restaurant data:", error);
        setError("Failed to load restaurant data");
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    const restaurantName2 = "kansis"; // Change to the actual restaurant name if needed
    axios
      .get(`http://localhost:8000/restaurant?name`)
      .then((response) => {
        setRestaurant2(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching the restaurant data:", error);
        setError("Failed to load restaurant data");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  if (!restaurant) {
    return <div>No restaurant data available</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold my-8">Lunssi</h1>
      <div className="flex space-x-4">
        <RestaurantCard
          name={restaurant.name}
          lunchItems={restaurant.lunchItems}
          lunchPrice={restaurant.lunchPrice}
          lunchTime={restaurant.lunchTime}
        />
        <RestaurantCard
          name={restaurant2.name}
          lunchItems={restaurant2.lunchItems}
          lunchPrice={restaurant2.lunchPrice}
          lunchTime={restaurant2.lunchTime}
        />
      </div>
    </div>
  );
};

export default Home;
