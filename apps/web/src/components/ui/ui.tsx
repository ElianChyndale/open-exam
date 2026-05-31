import {
  forwardRef,
  type ButtonHTMLAttributes,
  type HTMLAttributes,
  type InputHTMLAttributes,
  type ReactNode,
  type SelectHTMLAttributes,
  type TextareaHTMLAttributes,
} from 'react';
import { AlertCircle, Search } from 'lucide-react';

export function cn(...values: Array<string | false | null | undefined>) {
  return values.filter(Boolean).join(' ');
}

export const Surface = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  function Surface({ className, ...props }, ref) {
    return <div ref={ref} className={cn('card', className)} {...props} />;
  },
);

type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger';

export function Button({
  className,
  variant = 'primary',
  type = 'button',
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & { variant?: ButtonVariant }) {
  return (
    <button
      type={type}
      className={cn(`button-${variant}`, className)}
      {...props}
    />
  );
}

export const Field = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  function Field({ className, ...props }, ref) {
    return <input ref={ref} className={cn('control', className)} {...props} />;
  },
);

export const TextArea = forwardRef<HTMLTextAreaElement, TextareaHTMLAttributes<HTMLTextAreaElement>>(
  function TextArea({ className, ...props }, ref) {
    return <textarea ref={ref} className={cn('control', className)} {...props} />;
  },
);

export const Select = forwardRef<HTMLSelectElement, SelectHTMLAttributes<HTMLSelectElement>>(
  function Select({ className, ...props }, ref) {
    return <select ref={ref} className={cn('control', className)} {...props} />;
  },
);

export function Badge({
  children,
  tone = 'neutral',
}: {
  children: ReactNode;
  tone?: 'neutral' | 'accent' | 'success' | 'warning' | 'danger';
}) {
  const tones = {
    neutral: 'bg-surface-sunken text-muted',
    accent: 'bg-accent/10 text-accent',
    success: 'bg-success/10 text-success',
    warning: 'bg-warning/10 text-warning',
    danger: 'bg-danger/10 text-danger',
  };
  return <span className={cn('inline-flex rounded-full px-2 py-0.5 text-xs font-semibold', tones[tone])}>{children}</span>;
}

export function Alert({
  children,
  tone = 'warning',
}: {
  children: ReactNode;
  tone?: 'warning' | 'danger' | 'success';
}) {
  const tones = {
    warning: 'border-warning/25 bg-warning/10 text-warning',
    danger: 'border-danger/25 bg-danger/10 text-danger',
    success: 'border-success/25 bg-success/10 text-success',
  };
  return (
    <div className={cn('flex gap-2 rounded-xl border p-3 text-sm', tones[tone])}>
      <AlertCircle className="mt-0.5 shrink-0" size={15} />
      <div>{children}</div>
    </div>
  );
}

export function Metric({ label, value, detail }: { label: string; value: ReactNode; detail?: ReactNode }) {
  return (
    <div>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      {detail ? <div className="mt-1 text-xs text-muted">{detail}</div> : null}
    </div>
  );
}

export function SearchField({ className, ...props }: InputHTMLAttributes<HTMLInputElement>) {
  return (
    <label className={cn('flex items-center gap-2 rounded-xl border border-line bg-surface-raised/75 px-3', className)}>
      <Search size={15} className="text-muted" />
      <input className="min-w-0 flex-1 bg-transparent py-2 text-sm outline-none" type="search" {...props} />
    </label>
  );
}

export function EmptyState({ title, detail }: { title: string; detail?: string }) {
  return (
    <div className="rounded-xl border border-dashed border-line p-8 text-center">
      <p className="text-sm font-semibold">{title}</p>
      {detail ? <p className="mt-1 text-xs text-muted">{detail}</p> : null}
    </div>
  );
}

export function Skeleton({ className }: { className?: string }) {
  return <div className={cn('animate-pulse rounded-lg bg-surface-hover', className)} aria-hidden="true" />;
}

export function ListRow({ children, className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('rounded-xl border border-line/80 bg-surface-raised/70 p-3', className)} {...props}>{children}</div>;
}

export function Sheet({ title, children, className }: { title: string; children: ReactNode; className?: string }) {
  return (
    <section className={cn('card', className)}>
      <h2 className="mb-3 text-sm font-semibold tracking-tight">{title}</h2>
      {children}
    </section>
  );
}
