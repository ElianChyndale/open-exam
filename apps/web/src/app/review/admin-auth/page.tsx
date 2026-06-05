'use client';

import Link from 'next/link';
import { FormEvent, useEffect, useState } from 'react';
import { ArrowRight, KeyRound, Loader2, LockKeyhole, ShieldCheck } from 'lucide-react';

import { authApi } from '@/lib/api';

type SessionUser = {
  user_id: string;
  username: string;
  role: string;
};

export default function AdminAuthPage() {
  const [user, setUser] = useState<SessionUser | null>(null);
  const [bootstrap, setBootstrap] = useState({ username: 'admin', password: 's3cret-passphrase' });
  const [login, setLogin] = useState({ username: 'admin', password: 's3cret-passphrase' });
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const loadSession = async () => {
    setLoading(true);
    setError('');
    try {
      if (!authApi.hasStoredSession()) {
        setUser(null);
        return;
      }
      const payload = await authApi.session();
      setUser(payload.user);
    } catch (err) {
      authApi.clearStoredSession();
      setUser(null);
      setError(err instanceof Error ? err.message : 'Session check failed');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSession().catch(() => undefined);
  }, []);

  const handleBootstrap = async (event: FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    setError('');
    setMessage('');
    try {
      const payload = await authApi.bootstrapAdmin(bootstrap);
      setMessage(`Admin created: ${payload.user.username}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Bootstrap failed');
    } finally {
      setSubmitting(false);
    }
  };

  const handleLogin = async (event: FormEvent) => {
    event.preventDefault();
    setSubmitting(true);
    setError('');
    setMessage('');
    try {
      const payload = await authApi.login(login);
      setUser(payload.user);
      setMessage(`Session ready for ${payload.user.username}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    } finally {
      setSubmitting(false);
    }
  };

  const handleLogout = async () => {
    setSubmitting(true);
    setError('');
    setMessage('');
    try {
      await authApi.logout();
      setUser(null);
      setMessage('Admin session cleared.');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Logout failed');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="mx-auto max-w-4xl pb-12">
      <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <div className="inline-flex items-center gap-2 rounded-full bg-surface-raised px-3 py-1 text-xs font-medium text-muted">
            <ShieldCheck size={13} />
            Local admin scope
          </div>
          <h2 className="mt-4 text-3xl font-semibold tracking-normal">Admin Session</h2>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-muted">
            Create or resume the local admin session used by protected question-bank import and review APIs.
            Learner practice remains separate and does not require this session.
          </p>
        </div>
        <Link href="/review/tools" className="btn-secondary inline-flex w-fit items-center gap-2">
          <ArrowRight size={15} />
          Back to Tools
        </Link>
      </div>

      {(error || message) && (
        <div className={`mb-5 rounded-lg border p-3 text-sm ${error ? 'border-warning-soft bg-warning-soft text-warning' : 'border-success-soft bg-success-soft text-success'}`}>
          {error || message}
        </div>
      )}

      <div className="grid gap-5 lg:grid-cols-[minmax(0,1.1fr)_minmax(320px,0.9fr)]">
        <section className="rounded-lg bg-surface-raised p-5">
          <div className="flex items-center gap-2">
            <LockKeyhole size={18} className="text-accent" />
            <h3 className="font-semibold">Session Status</h3>
          </div>
          <div className="mt-4 rounded-lg bg-surface-field p-4 text-sm">
            {loading ? (
              <div className="text-muted">
                <Loader2 size={15} className="mr-2 inline animate-spin" />
                Checking local session...
              </div>
            ) : user ? (
              <div className="space-y-2">
                <p className="font-medium text-foreground">Authenticated as {user.username}</p>
                <p className="text-muted">Role: {user.role}</p>
                <p className="text-muted">Use this session before protected import/review work.</p>
                <div className="pt-2">
                  <button onClick={handleLogout} disabled={submitting} className="btn-secondary inline-flex items-center gap-2">
                    <KeyRound size={14} />
                    Clear Session
                  </button>
                </div>
              </div>
            ) : (
              <div className="space-y-2 text-muted">
                <p>No admin session is currently stored in this browser.</p>
                <p>Bootstrap only once per local repository, then use login to resume the session later.</p>
              </div>
            )}
          </div>

          <div className="mt-4 rounded-lg bg-surface-field p-4 text-sm text-muted">
            <p className="font-medium text-foreground">Protected paths</p>
            <ul className="mt-2 space-y-1">
              <li>`POST /api/question-banks/import`</li>
              <li>`GET /api/question-banks/all`</li>
              <li>`GET /api/question-banks/quarantine`</li>
              <li>`POST /api/question-banks/{'{question_id}'}/review`</li>
            </ul>
          </div>
        </section>

        <section className="space-y-5">
          <form onSubmit={handleBootstrap} className="rounded-lg bg-surface-raised p-5">
            <div className="flex items-center gap-2">
              <ShieldCheck size={18} className="text-accent" />
              <h3 className="font-semibold">Bootstrap Admin</h3>
            </div>
            <p className="mt-2 text-sm text-muted">Run this once on a fresh local repo.</p>
            <div className="mt-4 space-y-3">
              <input
                value={bootstrap.username}
                onChange={(event) => setBootstrap({ ...bootstrap, username: event.target.value })}
                placeholder="admin username"
                className="w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm outline-none"
              />
              <input
                type="password"
                value={bootstrap.password}
                onChange={(event) => setBootstrap({ ...bootstrap, password: event.target.value })}
                placeholder="admin password"
                className="w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm outline-none"
              />
              <button type="submit" disabled={submitting} className="btn-primary inline-flex items-center gap-2">
                <ShieldCheck size={14} />
                Bootstrap
              </button>
            </div>
          </form>

          <form onSubmit={handleLogin} className="rounded-lg bg-surface-raised p-5">
            <div className="flex items-center gap-2">
              <KeyRound size={18} className="text-accent" />
              <h3 className="font-semibold">Login</h3>
            </div>
            <p className="mt-2 text-sm text-muted">Use the local admin session for protected import and review work.</p>
            <div className="mt-4 space-y-3">
              <input
                value={login.username}
                onChange={(event) => setLogin({ ...login, username: event.target.value })}
                placeholder="admin username"
                className="w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm outline-none"
              />
              <input
                type="password"
                value={login.password}
                onChange={(event) => setLogin({ ...login, password: event.target.value })}
                placeholder="admin password"
                className="w-full rounded-lg border border-line bg-surface-field px-3 py-2 text-sm outline-none"
              />
              <button type="submit" disabled={submitting} className="btn-primary inline-flex items-center gap-2">
                <KeyRound size={14} />
                Login
              </button>
            </div>
          </form>
        </section>
      </div>
    </div>
  );
}
