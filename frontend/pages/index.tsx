import React, { useEffect, useState } from "react";
import axios from "axios";
import RestaurantCard from "../components/RestaurantCard";

interface Restaurant {
  name: string;
  lunchItems: string[];
  lunchPrice: string;
  lunchTime: string;
}

//const apiUrl = "http://localhost:8080";
const apiUrl = "https://lunssi-backend.fly.dev";

const Home: React.FC = () => {
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [restaurant2, setRestaurant2] = useState<Restaurant | null>(null);
  const [restaurant3, setRestaurant3] = useState<Restaurant | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const restaurantName = "bruuveri";
    axios
      .get(`${apiUrl}/restaurant?name=${restaurantName}`)
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
    const restaurantName2 = "kansis";
    axios
      .get(`${apiUrl}/restaurant?name=${restaurantName2}`)
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

  useEffect(() => {
    const restaurantName3 = "pompier-albertinkatu";
    axios
      .get(`${apiUrl}/restaurant?name=${restaurantName3}`)
      .then((response) => {
        setRestaurant3(response.data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching the restaurant data:", error);
        setError("Failed to load restaurant data");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div>Ladataan lounaita</div>;
  }

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold my-8">Lunssi</h1>
      <div className="flex space-x-4">
        {restaurant && (
          <RestaurantCard
            name={restaurant.name}
            lunchItems={restaurant.lunchItems}
            lunchPrice={restaurant.lunchPrice}
            lunchTime={restaurant.lunchTime}
          />
        )}
        {restaurant2 && (
          <RestaurantCard
            name={restaurant2.name}
            lunchItems={restaurant2.lunchItems}
            lunchPrice={restaurant2.lunchPrice}
            lunchTime={restaurant2.lunchTime}
          />
        )}
        {restaurant3 && (
          <RestaurantCard
            name={restaurant3.name}
            lunchItems={restaurant3.lunchItems}
            lunchPrice={restaurant3.lunchPrice}
            lunchTime={restaurant3.lunchTime}
          />
        )}
      </div>
    </div>
  );
};

export default Home;
