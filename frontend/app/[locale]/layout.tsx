import { ReactNode } from "react";
import i18nConfig from "@/i18nConfig";
import "@/styles/globals.css";
import { notFound } from "next/navigation";

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
