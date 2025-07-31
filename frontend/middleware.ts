import type { NextRequest } from "next/server";
import createMiddleware from "next-intl/middleware";
import { routing } from "./i18n/routing";

const intlMiddleware = createMiddleware(routing);

export function middleware(request: NextRequest) {
  return intlMiddleware(request);
}

export const config = {
  matcher: [
    "/",
    "/(en)/:path*",
    "/((?!api|static|.*\\..*|_next|favicon.ico|robots.txt).*)",
  ],
};
