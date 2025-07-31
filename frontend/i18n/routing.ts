import { createNavigation } from "next-intl/navigation";
import { defineRouting } from "next-intl/routing";

export const defaultLocale = "fi";

export const routing = defineRouting({
  defaultLocale,

  localePrefix: {
    mode: "as-needed",
  },
  locales: [defaultLocale, "en"],
});

export type Locale = (typeof routing.locales)[number];

export const { Link, redirect, usePathname, useRouter, getPathname } =
  createNavigation(routing);
