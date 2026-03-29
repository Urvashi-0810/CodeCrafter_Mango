import { useState, useEffect } from "react";
import Navbar from "@/components/Navbar";
import Footer from "@/components/Footer";
import TickerBar from "@/components/TickerBar";
import { LearningModules } from "@/components/LearningModules";
import { INITIAL_PROFILE, type UserProfile } from "@/data/learningData";

export default function LearnPage() {
  const [profile, setProfile] = useState<UserProfile>(() => {
    try {
      const stored = localStorage.getItem("smartfinance_learning_profile");
      if (stored) return JSON.parse(stored);
    } catch (e) {
      console.error(e);
    }
    return INITIAL_PROFILE;
  });

  useEffect(() => {
    localStorage.setItem("smartfinance_learning_profile", JSON.stringify(profile));
  }, [profile]);

  const handleUpdateProfile = (updates: Partial<UserProfile>) => {
    setProfile(prev => ({ ...prev, ...updates }));
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <Navbar />
      <TickerBar />

      <main className="flex-1 container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <LearningModules profile={profile} onUpdateProfile={handleUpdateProfile} />
        </div>
      </main>

      <Footer />
    </div>
  );
}
