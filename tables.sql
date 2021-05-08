BEGIN;
--
-- Create model Excel
--
CREATE TABLE "data_excel" ("id" bigserial NOT NULL PRIMARY KEY, "file" varchar(100) NOT NULL, "created" timestamp with time zone NOT NULL, "activated" boolean NOT NULL);
--
-- Create model Sale
--
CREATE TABLE "data_sale" ("id" uuid NOT NULL PRIMARY KEY, "date" timestamp with time zone NULL, "product_a" smallint NULL CHECK ("product_a" >= 0), "product_b" smallint NULL CHECK ("product_b" >= 0), "product_c" smallint NULL CHECK ("product_c" >= 0));
--
-- Create model Customer
--
CREATE TABLE "data_customer" ("id" uuid NOT NULL PRIMARY KEY, "customer_name" bigint NULL CHECK ("customer_name" >= 0), "latitude" double precision NULL, "longitude" double precision NULL, "geom" geometry(MULTIPOINT,4326) NULL, "sale_id" uuid NULL UNIQUE);
ALTER TABLE "data_customer" ADD CONSTRAINT "data_customer_sale_id_fb0abf06_fk_data_sale_id" FOREIGN KEY ("sale_id") REFERENCES "data_sale" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "data_customer_geom_id" ON "data_customer" USING GIST ("geom");
COMMIT;
