import type { RestaurantCardProps } from "@/components/RestaurantCard";
import axios from "axios";
import { cache } from "react";

export const getRestaurantData = cache(
  async (locale: string, region: string): Promise<RestaurantCardProps[]> => {
    const params = new URLSearchParams({
      lang: locale,
      region,
    });

    const restaurantData = await axios
      .get(`${process.env.BACKEND_API_URL}/restaurants?${params.toString()}`)
      .then((response) => response.data);

    return restaurantData;
  },
);
