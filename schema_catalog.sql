BEGIN;
--
-- Create model Category
--
CREATE TABLE "catalog_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(100) NOT NULL UNIQUE, "slug" varchar(120) NOT NULL UNIQUE, "description" text NOT NULL, "parent_id" bigint NULL REFERENCES "catalog_category" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Product
--
CREATE TABLE "catalog_product" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "slug" varchar(220) NOT NULL UNIQUE, "description" text NOT NULL, "sku" varchar(100) NOT NULL, "brand" varchar(100) NOT NULL, "price" decimal NOT NULL, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "in_stock" bool NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "category_id" bigint NOT NULL REFERENCES "catalog_category" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model ProductVariation
--
CREATE TABLE "catalog_productvariation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL, "value" varchar(50) NOT NULL, "sku" varchar(100) NOT NULL, "price" decimal NOT NULL, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "in_stock" bool NOT NULL, "product_id" bigint NOT NULL REFERENCES "catalog_product" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create index catalog_cat_name_39f70b_idx on field(s) name of model category
--
CREATE INDEX "catalog_cat_name_39f70b_idx" ON "catalog_category" ("name");
--
-- Create index catalog_cat_slug_695af4_idx on field(s) slug of model category
--
CREATE INDEX "catalog_cat_slug_695af4_idx" ON "catalog_category" ("slug");
--
-- Create index catalog_pro_price_2d2a4c_idx on field(s) price of model product
--
CREATE INDEX "catalog_pro_price_2d2a4c_idx" ON "catalog_product" ("price");
--
-- Create index catalog_pro_in_stoc_18ac32_idx on field(s) in_stock, price of model product
--
CREATE INDEX "catalog_pro_in_stoc_18ac32_idx" ON "catalog_product" ("in_stock", "price");
--
-- Create index catalog_pro_categor_5a4a66_idx on field(s) category, price of model product
--
CREATE INDEX "catalog_pro_categor_5a4a66_idx" ON "catalog_product" ("category_id", "price");
--
-- Alter unique_together for productvariation (1 constraint(s))
--
CREATE UNIQUE INDEX "catalog_productvariation_product_id_name_value_7f9b9554_uniq" ON "catalog_productvariation" ("product_id", "name", "value");
CREATE INDEX "catalog_category_parent_id_f61bd017" ON "catalog_category" ("parent_id");
CREATE INDEX "catalog_product_name_924af5bc" ON "catalog_product" ("name");
CREATE INDEX "catalog_product_price_1347cb30" ON "catalog_product" ("price");
CREATE INDEX "catalog_product_quantity_754a3ecc" ON "catalog_product" ("quantity");
CREATE INDEX "catalog_product_in_stock_12f749c1" ON "catalog_product" ("in_stock");
CREATE INDEX "catalog_product_created_at_ea90ae72" ON "catalog_product" ("created_at");
CREATE INDEX "catalog_product_category_id_35bf920b" ON "catalog_product" ("category_id");
CREATE INDEX "catalog_productvariation_product_id_926584a9" ON "catalog_productvariation" ("product_id");
COMMIT;
