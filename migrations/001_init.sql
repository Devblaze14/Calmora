-- Calmora initial schema: profiles, chat, mood, journal, weekly plan, study, bookings.
-- Apply once via Supabase SQL Editor.

-- ─── PROFILES ───
create table if not exists public.profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  full_name text,
  phone text,
  preferred_language text,
  updated_at timestamptz default now()
);

-- Auto-create a profile row on signup
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (user_id, full_name)
  values (new.id, coalesce(new.raw_user_meta_data->>'full_name', ''))
  on conflict (user_id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ─── CHAT MESSAGES ───
create table if not exists public.chat_messages (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  role text not null check (role in ('user','assistant')),
  content text not null,
  created_at timestamptz default now()
);
create index if not exists chat_messages_user_created_idx
  on public.chat_messages (user_id, created_at desc);

-- ─── MOOD LOGS ───
create table if not exists public.mood_logs (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  mood text not null,
  context text,
  response text,
  created_at timestamptz default now()
);

-- ─── JOURNAL ENTRIES ───
create table if not exists public.journal_entries (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  entry text not null,
  reflection text,
  created_at timestamptz default now()
);

-- ─── WEEKLY PLANS ───
create table if not exists public.weekly_plans (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  goal text not null,
  energy text,
  hours text,
  plan text,
  created_at timestamptz default now()
);

-- ─── STUDY BREAKDOWNS ───
create table if not exists public.study_breakdowns (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  task text not null,
  time_window text,
  breakdown text,
  created_at timestamptz default now()
);

-- ─── BOOKINGS ───
create table if not exists public.bookings (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  plan text,
  plan_label text,
  amount_paise int,
  razorpay_order_id text unique,
  razorpay_payment_id text,
  status text default 'pending' check (status in ('pending','paid','failed')),
  name text,
  email text,
  phone text,
  concern text,
  language text,
  slot text,
  created_at timestamptz default now(),
  paid_at timestamptz
);
create index if not exists bookings_user_idx on public.bookings (user_id, created_at desc);

-- ─── RLS ───
alter table public.profiles          enable row level security;
alter table public.chat_messages     enable row level security;
alter table public.mood_logs         enable row level security;
alter table public.journal_entries   enable row level security;
alter table public.weekly_plans      enable row level security;
alter table public.study_breakdowns  enable row level security;
alter table public.bookings          enable row level security;

-- profiles: user can read/update own row
drop policy if exists "profiles self select" on public.profiles;
create policy "profiles self select" on public.profiles
  for select using (auth.uid() = user_id);

drop policy if exists "profiles self update" on public.profiles;
create policy "profiles self update" on public.profiles
  for update using (auth.uid() = user_id) with check (auth.uid() = user_id);

-- generic self-only policies for the rest
do $$
declare t text;
begin
  foreach t in array array['chat_messages','mood_logs','journal_entries','weekly_plans','study_breakdowns','bookings']
  loop
    execute format('drop policy if exists "%s self select" on public.%s', t, t);
    execute format('create policy "%s self select" on public.%s for select using (auth.uid() = user_id)', t, t);

    execute format('drop policy if exists "%s self insert" on public.%s', t, t);
    execute format('create policy "%s self insert" on public.%s for insert with check (auth.uid() = user_id)', t, t);

    execute format('drop policy if exists "%s self update" on public.%s', t, t);
    execute format('create policy "%s self update" on public.%s for update using (auth.uid() = user_id) with check (auth.uid() = user_id)', t, t);
  end loop;
end$$;
