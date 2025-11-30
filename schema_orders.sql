BEGIN;
--
-- Create model Cart
--
CREATE TABLE "orders_cart" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "checked_out" bool NOT NULL, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Order
--
CREATE TABLE "orders_order" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "total_amount" decimal NOT NULL, "address" varchar(255) NOT NULL, "phone_number" varchar(20) NOT NULL, "payment_method" varchar(30) NOT NULL, "status" varchar(20) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model OrderItem
--
CREATE TABLE "orders_orderitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "price" decimal NOT NULL, "order_id" bigint NOT NULL REFERENCES "orders_order" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "catalog_product" ("id") DEFERRABLE INITIALLY DEFERRED, "variation_id" bigint NULL REFERENCES "catalog_productvariation" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model Shipment
--
CREATE TABLE "orders_shipment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "tracking_number" varchar(100) NULL, "carrier" varchar(100) NOT NULL, "status" varchar(20) NOT NULL, "shipped_at" datetime NULL, "expected_delivery" date NULL, "delivered_at" datetime NULL, "order_id" bigint NOT NULL UNIQUE REFERENCES "orders_order" ("id") DEFERRABLE INITIALLY DEFERRED);
--
-- Create model CartItem
--
CREATE TABLE "orders_cartitem" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quantity" integer unsigned NOT NULL CHECK ("quantity" >= 0), "price" decimal NOT NULL, "cart_id" bigint NOT NULL REFERENCES "orders_cart" ("id") DEFERRABLE INITIALLY DEFERRED, "product_id" bigint NOT NULL REFERENCES "catalog_product" ("id") DEFERRABLE INITIALLY DEFERRED, "variation_id" bigint NULL REFERENCES "catalog_productvariation" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "orders_cart_user_id_121a069e" ON "orders_cart" ("user_id");
CREATE INDEX "orders_order_user_id_e9b59eb1" ON "orders_order" ("user_id");
CREATE INDEX "orders_orderitem_order_id_fe61a34d" ON "orders_orderitem" ("order_id");
CREATE INDEX "orders_orderitem_product_id_afe4254a" ON "orders_orderitem" ("product_id");
CREATE INDEX "orders_orderitem_variation_id_330c4eac" ON "orders_orderitem" ("variation_id");
CREATE UNIQUE INDEX "orders_cartitem_cart_id_product_id_variation_id_16267a3f_uniq" ON "orders_cartitem" ("cart_id", "product_id", "variation_id");
CREATE INDEX "orders_cartitem_cart_id_529df5fa" ON "orders_cartitem" ("cart_id");
CREATE INDEX "orders_cartitem_product_id_55063ee7" ON "orders_cartitem" ("product_id");
CREATE INDEX "orders_cartitem_variation_id_c7b91521" ON "orders_cartitem" ("variation_id");
COMMIT;
