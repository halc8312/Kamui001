// frontend/app/page.tsx

import { Suspense } from 'react';
import { Metadata } from 'next';
import EffectList from '@/components/Effects/EffectList';
import TriggerList from '@/components/Triggers/TriggerList';
import Loading from '@/components/Common/Loading';

// メタデータの設定（SEO対策）
export const metadata: Metadata = {
  title: 'StockSense - Minecraft Effect Management',
  description: 'Manage and control your Minecraft effects in real-time',
  keywords: 'minecraft, effects, gaming, management, real-time',
  openGraph: {
    title: 'StockSense - Minecraft Effect Management',
    description: 'Manage and control your Minecraft effects in real-time',
    images: ['/images/og-image.png'],
  },
};

// メインページコンポーネント
export default async function Home() {
  return (
    <main className="min-h-screen p-4 md:p-8 lg:p-12">
      <div className="max-w-7xl mx-auto">
        {/* ヒーローセクション */}
        <section className="mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Welcome to StockSense
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-300">
            Manage your Minecraft effects with ease and precision
          </p>
        </section>

        {/* エフェクトセクション */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold mb-6">Active Effects</h2>
          <Suspense fallback={<Loading />}>
            <EffectList />
          </Suspense>
        </section>

        {/* トリガーセクション */}
        <section className="mb-12">
          <h2 className="text-2xl font-semibold mb-6">Available Triggers</h2>
          <Suspense fallback={<Loading />}>
            <TriggerList />
          </Suspense>
        </section>

        {/* ダッシュボードリンク */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4">Effect Dashboard</h3>
            <p className="mb-4">Monitor and manage all your active effects</p>
            <a
              href="/dashboard"
              className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
            >
              Go to Dashboard
            </a>
          </div>
          <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-md">
            <h3 className="text-xl font-semibold mb-4">Trigger Settings</h3>
            <p className="mb-4">Configure your effect triggers</p>
            <a
              href="/triggers"
              className="inline-block bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 transition-colors"
            >
              Manage Triggers
            </a>
          </div>
        </section>
      </div>
    </main>
  );
}

// エラーバウンダリー
export function ErrorBoundary({ error }: { error: Error }) {
  return (
    <div className="p-4 text-red-600 bg-red-100 rounded">
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
    </div>
  );
}