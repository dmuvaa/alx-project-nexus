BEGIN;
--
-- Create model UserProfile
--
CREATE TABLE "users_userprofile" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "phone" varchar(20) NOT NULL, "address" varchar(255) NOT NULL, "user_id" integer NOT NULL UNIQUE REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
COMMIT;
