-- OpenExam tenant-safe SaaS bridge. Local mode remains the default.
create extension if not exists pgcrypto;
create schema if not exists private;

create type public.openexam_role as enum ('learner', 'instructor', 'admin');

create table public.organizations (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz not null default now()
);

create table public.organization_memberships (
  organization_id uuid not null references public.organizations(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  role public.openexam_role not null default 'learner',
  created_at timestamptz not null default now(),
  primary key (organization_id, user_id)
);

create table public.invitations (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  email text not null,
  role public.openexam_role not null default 'learner',
  invited_by uuid not null references auth.users(id),
  expires_at timestamptz not null,
  accepted_at timestamptz
);

create table public.profiles (
  organization_id uuid not null references public.organizations(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  settings jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now(),
  primary key (organization_id, user_id)
);

create table public.learning_events (
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  stream text not null,
  event_id text not null,
  event_type text not null,
  schema_version integer not null default 1,
  occurred_at timestamptz not null,
  source_refs jsonb not null default '[]'::jsonb,
  payload jsonb not null default '{}'::jsonb,
  primary key (organization_id, event_id)
);

create table public.mistake_cards (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  source_event_id text not null,
  payload jsonb not null,
  updated_at timestamptz not null default now()
);

create table public.tasks (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  payload jsonb not null,
  updated_at timestamptz not null default now()
);

create table public.reviews (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  payload jsonb not null,
  created_at timestamptz not null default now()
);

create table public.question_imports (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  storage_path text not null,
  provenance jsonb not null default '{}'::jsonb,
  verification_status text not null check (verification_status in ('verified', 'quarantined', 'rejected')),
  created_at timestamptz not null default now()
);

create table public.questions (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  import_id uuid references public.question_imports(id) on delete set null,
  payload jsonb not null,
  verification_status text not null check (verification_status in ('verified', 'quarantined', 'rejected')),
  updated_at timestamptz not null default now()
);

create table public.practice_sessions (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  payload jsonb not null,
  created_at timestamptz not null default now()
);

create table public.mock_runs (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  payload jsonb not null,
  created_at timestamptz not null default now()
);

create table public.coach_artifacts (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  evidence_refs jsonb not null,
  payload jsonb not null,
  created_at timestamptz not null default now()
);

create table public.graph_overlays (
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  payload jsonb not null,
  updated_at timestamptz not null default now(),
  primary key (organization_id, learner_id)
);

create table public.cohorts (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  name text not null,
  payload jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create table public.interventions (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  learner_id uuid not null references auth.users(id) on delete cascade,
  owner_id uuid references auth.users(id),
  reason text not null,
  status text not null default 'open',
  created_at timestamptz not null default now()
);

create table public.transfer_batches (
  id uuid primary key default gen_random_uuid(),
  organization_id uuid not null references public.organizations(id) on delete cascade,
  requested_by uuid not null references auth.users(id),
  direction text not null check (direction in ('local-to-cloud', 'cloud-to-local')),
  summary jsonb not null,
  created_at timestamptz not null default now()
);

create or replace function private.is_org_member(requested_organization_id uuid)
returns boolean
language sql
security definer
set search_path = ''
stable
as $$
  select (select auth.uid()) is not null and exists (
    select 1
    from public.organization_memberships membership
    where membership.organization_id = requested_organization_id
      and membership.user_id = (select auth.uid())
  );
$$;

create or replace function private.is_org_admin(requested_organization_id uuid)
returns boolean
language sql
security definer
set search_path = ''
stable
as $$
  select (select auth.uid()) is not null and exists (
    select 1
    from public.organization_memberships membership
    where membership.organization_id = requested_organization_id
      and membership.user_id = (select auth.uid())
      and membership.role = 'admin'
  );
$$;

alter table public.organizations enable row level security;
alter table public.organization_memberships enable row level security;
alter table public.invitations enable row level security;
alter table public.profiles enable row level security;
alter table public.learning_events enable row level security;
alter table public.mistake_cards enable row level security;
alter table public.tasks enable row level security;
alter table public.reviews enable row level security;
alter table public.question_imports enable row level security;
alter table public.questions enable row level security;
alter table public.practice_sessions enable row level security;
alter table public.mock_runs enable row level security;
alter table public.coach_artifacts enable row level security;
alter table public.graph_overlays enable row level security;
alter table public.cohorts enable row level security;
alter table public.interventions enable row level security;
alter table public.transfer_batches enable row level security;

create policy "members read organizations" on public.organizations for select to authenticated
using (private.is_org_member(id));
create policy "members read memberships" on public.organization_memberships for select to authenticated
using (private.is_org_member(organization_id));
create policy "admins manage memberships" on public.organization_memberships for all to authenticated
using (private.is_org_admin(organization_id)) with check (private.is_org_admin(organization_id));
create policy "admins manage invitations" on public.invitations for all to authenticated
using (private.is_org_admin(organization_id)) with check (private.is_org_admin(organization_id));

do $$
declare tenant_table text;
begin
  foreach tenant_table in array array[
    'profiles', 'learning_events', 'mistake_cards', 'tasks', 'reviews',
    'question_imports', 'questions', 'practice_sessions', 'mock_runs',
    'coach_artifacts', 'graph_overlays', 'cohorts', 'interventions', 'transfer_batches'
  ]
  loop
    execute format(
      'create policy "tenant members access %1$s" on public.%1$I for all to authenticated using (private.is_org_member(organization_id)) with check (private.is_org_member(organization_id))',
      tenant_table
    );
  end loop;
end $$;

insert into storage.buckets (id, name, public)
values ('openexam-private-question-banks', 'openexam-private-question-banks', false)
on conflict (id) do update set public = false;

create policy "tenant members read private question files"
on storage.objects for select to authenticated
using (
  bucket_id = 'openexam-private-question-banks'
  and private.is_org_member(((storage.foldername(name))[1])::uuid)
);

create policy "tenant members upload private question files"
on storage.objects for insert to authenticated
with check (
  bucket_id = 'openexam-private-question-banks'
  and private.is_org_member(((storage.foldername(name))[1])::uuid)
);
