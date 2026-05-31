import type { Metadata } from 'next';
import './globals.css';
import { Sidebar } from '@/components/cockpit/Sidebar';

export const metadata: Metadata = {
  title: 'ExamOS — 考试通过率操作系统',
  description: 'CFA/FRM/CPA 考试操作系统：每日计划、错题诊断、间隔复习、模拟复盘、学习有效性仪表盘',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body className="min-h-screen">
        <Sidebar />
        <main className="min-h-screen px-4 pb-24 pt-5 lg:ml-64 lg:px-8 lg:pb-8 lg:pt-8">
          {children}
        </main>
      </body>
    </html>
  );
}
