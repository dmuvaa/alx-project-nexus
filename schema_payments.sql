BEGIN;
--
-- Create model Payment
--
CREATE TABLE "payments_payment" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "phone_number" varchar(15) NOT NULL, "amount" decimal NOT NULL, "transaction_id" varchar(100) NULL UNIQUE, "status" varchar(20) NOT NULL, "method" varchar(30) NOT NULL, "description" varchar(255) NOT NULL, "created_at" datetime NOT NULL, "updated_at" datetime NOT NULL, "order_id" bigint NULL REFERENCES "orders_order" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "payments_payment_order_id_22c479b7" ON "payments_payment" ("order_id");
CREATE INDEX "payments_payment_user_id_f9db060a" ON "payments_payment" ("user_id");
COMMIT;
