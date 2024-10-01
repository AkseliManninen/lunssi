import React from "react";
import axios from "axios";
import RestaurantCard from "../components/RestaurantCard";

interface Restaurant {
  name: string;
  lunchItems: string[];
  lunchPrice: string;
  lunchTime: string;
}

interface HomeProps {
  restaurants: Restaurant[];
  error: string | null;
}

export const getStaticProps = async () => {
  const restaurantNames = [
    // "bruuveri", - Bruuveri denies our client with 443
    "kansis",
    "pompier-albertinkatu",
    "hämis",
  ];

  const restaurantData = await Promise.all(
    restaurantNames.map((name) =>
      axios
        .get(`${process.env.BACKEND_API_URL}/restaurant?name=${name}`)
        .then((response) => response.data)
    )
  );
  return {
    props: {
      restaurants: restaurantData,
    },
    revalidate: 12 * 60 * 60, // 12 hours in seconds
  };
};

const Home: React.FC<HomeProps> = ({ restaurants }) => {
  return (
    <div className="container mx-auto px-4">
      <h1 className="text-3xl font-bold my-8">Lunssi</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {restaurants.map((restaurant, index) => (
          <RestaurantCard
            key={index}
            name={restaurant.name}
            lunchItems={restaurant.lunchItems}
            lunchPrice={restaurant.lunchPrice}
            lunchTime={restaurant.lunchTime}
          />
        ))}
      </div>
    </div>
  );
};

export default Home;
