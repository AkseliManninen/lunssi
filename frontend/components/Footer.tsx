"use client";

import Github from "@/assets/icons/github.svg";
import React from "react";
import { useTranslation } from "react-i18next";

const Footer = () => {
  const { t } = useTranslation();

  return (
    <footer className="bg-gray-100 border-t border-gray-300 py-6">
      <div className="container mx-auto px-4 flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
        <div className="flex items-center space-x-2 text-gray-600">
          <span className="text-sm">
            &copy; {new Date().getFullYear()} {t("contributors")}
          </span>
        </div>

        <div className="flex items-center space-x-4">
          <a
            href="https://github.com/AkseliManninen/lunssi"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
          >
            <Github />
            <span className="text-sm">{t("sourceCode")}</span>
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
