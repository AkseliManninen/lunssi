import React from "react";
import axios from "axios";
import RestaurantCard from "@/components/RestaurantCard";
import LanguageChanger from "@/components/LanguageChanger";
import i18nConfig from "@/i18nConfig";
import TranslationsProvider from "@/components/TranslationProvider";
import initTranslations from "../i18n";

const getRestaurantData = async (locale: string) => {
  const restaurantShorthands = [
    "bruuveri",
    "kansis",
    "pompier_albertinkatu",
    "hämis",
  ];

  const restaurantData = await Promise.all(
    restaurantShorthands.map((shorthand) =>
      axios
        .get(
          `${process.env.BACKEND_API_URL}/restaurant?name=${shorthand}&lang=${locale}`
        )
        .then((response) => response.data)
    )
  );
  return restaurantData;
};

// 12 hours
export const revalidate = 43200;

type Props = { params: { locale?: string } };

const i18nNamespaces = ["translation"];

const Home = async ({ params }: Props) => {
  const locale = params.locale ?? i18nConfig.defaultLocale;
  const restaurants = await getRestaurantData(locale);
  const { resources } = await initTranslations(locale, i18nNamespaces);
  return (
    <TranslationsProvider
      namespaces={i18nNamespaces}
      locale={locale}
      resources={resources}
    >
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
        <LanguageChanger />
      </div>
    </TranslationsProvider>
  );
};

export default Home;
