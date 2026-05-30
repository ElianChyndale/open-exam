'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  PenLine,
  Stethoscope,
  BookOpen,
  FileText,
  BarChart3,
  Building2,
  Zap,
} from 'lucide-react';

const navItems = [
  { href: '/today', label: '今日驾驶舱', icon: Zap },
  { href: '/capture', label: '题目录入', icon: PenLine },
  { href: '/diagnosis', label: '错因诊断', icon: Stethoscope },
  { href: '/review', label: '复习包', icon: BookOpen },
  { href: '/mock', label: '模拟中心', icon: FileText },
  { href: '/dashboard', label: '有效性仪表盘', icon: BarChart3 },
  { href: '/institution', label: '机构控制台', icon: Building2 },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 z-50 flex h-20 w-full flex-row bg-[#0f1720] border-b border-[#24313d] lg:h-screen lg:w-60 lg:flex-col lg:border-b-0 lg:border-r">
      {/* Logo */}
      <div className="flex w-36 shrink-0 flex-col justify-center px-4 border-r border-[#24313d] lg:w-auto lg:px-5 lg:py-5 lg:border-r-0 lg:border-b">
        <h1 className="text-lg font-bold tracking-tight">
          <span className="text-[#14b8a6]">Exam</span>
          <span className="text-[#e4e4e7]">OS</span>
        </h1>
        <p className="text-[10px] text-[#94a3b8] mt-0.5 uppercase tracking-normal">
          考试通过率操作系统
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex flex-1 items-center gap-1 overflow-x-auto px-3 py-2 lg:block lg:space-y-0.5 lg:overflow-auto lg:py-4">
        {navItems.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + '/');
          const Icon = item.icon;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex shrink-0 items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors lg:gap-3 lg:py-2.5 ${
                isActive
                  ? 'bg-[#14b8a6]/15 text-[#5eead4] font-medium'
                  : 'text-[#94a3b8] hover:text-[#e5edf5] hover:bg-[#17212b]'
              }`}
            >
              <Icon size={16} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="hidden px-5 py-4 border-t border-[#24313d] lg:block">
        <div className="text-[10px] text-[#94a3b8]">
          <p>CFA Level I · v0.1</p>
          <p className="mt-0.5">local-first · evidence-driven</p>
        </div>
      </div>
    </aside>
  );
}
