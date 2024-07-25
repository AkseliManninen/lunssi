import Image from "next/image";
import { Inter } from "next/font/google";
import RestaurantCard from "../components/RestaurantCard";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <main
      className={`flex min-h-screen flex-col items-center justify-between p-24 ${inter.className}`}
    >
      <h1>Lunssi</h1>
      <RestaurantCard
        name="Gourmet Bistro"
        lunchItems={["Grilled Chicken", "Caesar Salad", "Tiramisu"]}
        lunchPrice={25.0}
        lunchTime="11:30 AM - 2:30 PM"
      />
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex"></div>
    </main>
  );
}
