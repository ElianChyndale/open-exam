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
      <body className="min-h-screen lg:flex">
        <Sidebar />
        <main className="min-h-screen flex-1 p-4 pt-24 lg:ml-60 lg:p-6 lg:pt-6 overflow-auto">
          {children}
        </main>
      </body>
    </html>
  );
}
