import { readFile } from "node:fs/promises";
import path from "node:path";
import { cache } from "react";
import type { RestaurantCardProps } from "@/components/RestaurantCard";

export const getRestaurantData = cache(
  async (locale: string, region: string): Promise<RestaurantCardProps[]> => {
    const filePath = path.join(
      process.cwd(),
      "data",
      `${region}-${locale}.json`,
    );
    const raw = await readFile(filePath, "utf-8");
    return JSON.parse(raw);
  },
);
