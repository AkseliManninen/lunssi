import LanguageChanger from "@/components/LanguageChanger";
import RegionChanger from "@/components/RegionChanger";
import RestaurantCard from "@/components/RestaurantCard";
import { getRestaurantData } from "@/lib/restaurants";
import { I18nProviderClient } from "@/locales/client";
import { getI18n } from "@/locales/server";
import { defaultRegion, regions } from "@/utils/constants";
import { getLocalizedLink } from "@/utils/helpers";
import type { Metadata } from "next";
import { setStaticParamsLocale } from "next-international/server";
import React from "react";

// 6 hours
export const revalidate = 21600;

type Props = { params: Promise<{ locale: string; region: string }> };

export const generateMetadata = async (props: Props): Promise<Metadata> => {
  const params = await props.params;
  const locale = params.locale;
  const t = await getI18n();
  return {
    description: t("metaDescription"),
    openGraph: {
      description: t("metaDescription"),
      locale,
    },
    alternates: {
      canonical: getLocalizedLink("https://lunssi.fi", locale),
      languages: {
        fi: "https://lunssi.fi",
        en: "https://lunssi.fi/en",
      },
    },
  };
};

export const generateStaticParams = async (props: Props) => {
  const params = await props.params;
  return regions
    .filter(({ id }) => id !== defaultRegion)
    .map(({ id }) => {
      return { locale: params.locale, region: id };
    });
};

const Region = async (props: Props) => {
  const params = await props.params;
  const { locale, region } = params;
  setStaticParamsLocale(locale);
  const restaurants = await getRestaurantData(locale, region);
  return (
    <I18nProviderClient locale={locale}>
      <main className="bg-gray-100 pb-8">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-8 text-center text-gray-800">
            Lunssi
          </h1>
          <div className="mt-8 mb-5 flex justify-end gap-4">
            <RegionChanger currentRegion={region} />
            <LanguageChanger />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {restaurants.map(
              ({
                discount,
                isStudentCantine,
                location,
                lunchItems,
                lunchPrice,
                lunchTime,
                name,
              }) => (
                <RestaurantCard
                  key={name}
                  discount={discount}
                  isStudentCantine={isStudentCantine}
                  location={location}
                  lunchItems={lunchItems}
                  lunchPrice={lunchPrice}
                  lunchTime={lunchTime}
                  name={name}
                />
              ),
            )}
          </div>
        </div>
      </main>
    </I18nProviderClient>
  );
};

export default Region;
