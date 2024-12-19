import type { MetadataRoute } from "next";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: "https://lunssi.fi",
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 0.5,
      alternates: {
        languages: {
          fi: "https://lunssi.fi/fi",
          en: "https://lunssi.fi/en",
        },
      },
    },
    {
      url: "https://lunssi.fi/tampere",
      lastModified: new Date(),
      changeFrequency: "daily",
      priority: 0.5,
      alternates: {
        languages: {
          fi: "https://lunssi.fi/fi/tampere",
          en: "https://lunssi.fi/en/tampere",
        },
      },
    },
  ];
}
