-- Zarrin Arman Supabase schema
-- Run this once in Supabase SQL Editor.
-- Only the public anon/publishable key belongs in frontend code.

create table if not exists public.products (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  category text not null default 'سایر',
  price numeric(18,0) not null default 0 check (price >= 0),
  weight numeric(10,3) not null default 0 check (weight >= 0),
  karat text not null default '۱۸ عیار',
  image_url text,
  description text,
  featured boolean not null default false,
  active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.admin_users (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);

alter table public.products enable row level security;
alter table public.admin_users enable row level security;

-- A user can only see their own admin membership.
drop policy if exists "Admin users can view own membership" on public.admin_users;
create policy "Admin users can view own membership"
on public.admin_users for select to authenticated
using (user_id = auth.uid());

-- Public catalog: only active products.
drop policy if exists "Public can read active products" on public.products;
create policy "Public can read active products"
on public.products for select to anon, authenticated
using (active = true);

-- Admins can manage the full product catalog.
drop policy if exists "Admins can manage products" on public.products;
create policy "Admins can manage products"
on public.products for all to authenticated
using (exists (select 1 from public.admin_users a where a.user_id = auth.uid()))
with check (exists (select 1 from public.admin_users a where a.user_id = auth.uid()));

-- No policy grants public/admin-user membership write access from the browser.
