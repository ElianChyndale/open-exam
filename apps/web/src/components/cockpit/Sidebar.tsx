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
import ProfileSwitcher from './ProfileSwitcher';

const navItems = [
  { href: '/today', label: '今日驾驶舱', shortLabel: 'Today', icon: Zap },
  { href: '/capture', label: '题目录入', shortLabel: 'Capture', icon: PenLine },
  { href: '/diagnosis', label: '错因诊断', shortLabel: 'Diagnose', icon: Stethoscope },
  { href: '/review', label: 'Daily Review', shortLabel: 'Review', icon: BookOpen },
  { href: '/mock', label: '模拟中心', shortLabel: 'Mock', icon: FileText },
  { href: '/dashboard', label: '有效性仪表盘', shortLabel: 'Metrics', icon: BarChart3 },
  { href: '/institution', label: '机构控制台', shortLabel: 'Cohorts', icon: Building2 },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed bottom-0 left-0 z-50 flex h-16 w-full flex-row border-t border-line bg-surface-raised backdrop-blur-xl lg:bottom-auto lg:top-0 lg:h-screen lg:w-60 lg:flex-col lg:border-r lg:border-t-0">
      {/* Logo */}
      <div className="hidden w-36 shrink-0 flex-col justify-center border-r border-line px-4 lg:flex lg:w-auto lg:border-b lg:border-r-0 lg:px-5 lg:py-5">
        <h1 className="text-lg font-bold tracking-tight">
          <span className="text-accent">Exam</span>
          <span className="text-ink">OS</span>
        </h1>
        <p className="text-[10px] text-muted mt-0.5 uppercase tracking-normal">
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
              className={`flex min-w-16 shrink-0 flex-col items-center gap-1 rounded-lg px-2 py-1 text-[10px] transition-colors lg:min-w-0 lg:flex-row lg:gap-3 lg:px-3 lg:py-2.5 lg:text-sm ${
                isActive
                  ? 'bg-accent-soft text-accent font-medium'
                  : 'text-muted hover:text-ink hover:bg-surface-hover'
              }`}
            >
              <Icon size={16} />
              <span className="lg:hidden">{item.shortLabel}</span>
              <span className="hidden lg:inline">{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="hidden px-5 py-4 border-t border-line lg:block">
        <ProfileSwitcher />
        <div className="text-[10px] text-muted">
          <p className="mt-3">OpenExam · v0.1</p>
          <p className="mt-0.5">local-first · evidence-driven</p>
        </div>
      </div>
    </aside>
  );
}
