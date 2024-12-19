import './globals.css'
import { Metadata } from 'next'
import { Inter } from 'next/font/google'
import { AuthProvider } from '@/contexts/AuthContext'
import { Layout } from '@/components/Layout'

// Googleフォントの設定
const inter = Inter({ 
  subsets: ['latin'],
  display: 'swap',
})

// メタデータの設定
export const metadata: Metadata = {
  title: {
    template: '%s | StockSense',
    default: 'StockSense - Intelligent Stock Analysis Platform',
  },
  description: 'Advanced stock analysis and portfolio management platform powered by AI',
  keywords: ['stock analysis', 'portfolio management', 'financial analysis', 'AI trading'],
  authors: [{ name: 'StockSense Team' }],
  viewport: 'width=device-width, initial-scale=1, maximum-scale=1',
  robots: 'index, follow',
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: 'https://stocksense.com',
    siteName: 'StockSense',
    images: [
      {
        url: '/images/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'StockSense Platform',
      },
    ],
  },
}

// ルートレイアウトの型定義
interface RootLayoutProps {
  children: React.ReactNode
}

// ルートレイアウトコンポーネント
export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <html lang="en" className={inter.className}>
      <body className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <AuthProvider>
          <Layout>
            {/* エラーバウンダリとサスペンスの設定 */}
            <main className="flex-grow">
              {children}
            </main>
          </Layout>
        </AuthProvider>

        {/* サードパーティスクリプトの最適化されたローディング */}
        <script
          defer
          data-domain="stocksense.com"
          src="https://plausible.io/js/script.js"
        />
      </body>
    </html>
  )
}

// キャッシュとリバリデーションの設定
export const revalidate = 3600 // 1時間ごとにリバリデーション

// ルートセグメントの設定
export const dynamic = 'force-dynamic'

// セキュリティヘッダーの設定
export const headers = {
  'Content-Security-Policy': `
    default-src 'self';
    script-src 'self' 'unsafe-eval' 'unsafe-inline' https://plausible.io;
    style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
    img-src 'self' data: https:;
    font-src 'self' https://fonts.gstatic.com;
    connect-src 'self' ${process.env.NEXT_PUBLIC_API_URL} ${process.env.NEXT_PUBLIC_WS_URL};
  `,
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
}