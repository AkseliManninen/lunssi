import i18nConfig from "@/i18nConfig";
import type { ReactNode } from "react";
import "@/styles/globals.css";
import type { Metadata } from "next";
import { notFound } from "next/navigation";

export const metadata: Metadata = {
  title: "Lunssi",
  openGraph: {
    title: "Lunssi",
    url: "https://lunssi.fly.dev",
    type: "website",
    siteName: "Lunssi",
  },
  alternates: {
    canonical: "https://lunssi.fly.dev",
    languages: {
      en: "https://lunssi.fly.dev/en",
      fi: "https://lunssi.fly.dev",
    },
  },
};

export function generateStaticParams() {
  return i18nConfig.locales.map((locale) => ({ locale }));
}

export default function RootLayout({
  children,
  params: { locale },
}: {
  children: ReactNode;
  params: { locale: string };
}) {
  if (!i18nConfig.locales.includes(locale)) {
    notFound();
  }

  return (
    <html lang={locale}>
      <body>{children}</body>
    </html>
  );
}
