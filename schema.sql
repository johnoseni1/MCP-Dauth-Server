
create extension if not exists "uuid-ossp";


DROP TABLE IF EXISTS invoices CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;


create table customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) not null
);


create table products (
  id uuid default uuid_generate_v4() primary key,
  name text not null,
  description text,
  price decimal(10, 2) not null,
  stock_quantity integer default 0,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);


create table invoices (
  id uuid default uuid_generate_v4() primary key,
  customer_id uuid references customers(id),
  invoice_number text unique not null,
  total_amount decimal(10, 2) not null,
  status text default 'pending', 
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);


insert into products (name, price, stock_quantity) values
  ('Laptop Pro', 1299.99, 50),
  ('Wireless Mouse', 29.99, 200),
  ('HD Monitor', 249.50, 75)
on conflict do nothing;

insert into customers (name, email) values
  ('Alice Johnson', 'alice@example.com'),
  ('Bob Smith', 'bob@example.com')
on conflict (email) do nothing;
