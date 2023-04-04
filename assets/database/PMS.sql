BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "PaymentType" (
	"id"	INTEGER,
	"payType"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ProductCategory" (
	"id"	INTEGER,
	"productType"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "UserRole" (
	"id"	INTEGER,
	"role"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "City" (
	"id"	INTEGER,
	"name"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ShipmentType" (
	"id"	INTEGER,
	"type"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Designation" (
	"id"	INTEGER,
	"desgType"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "UserDetail" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"phno"	INTEGER NOT NULL UNIQUE,
	"address"	TEXT NOT NULL,
	"desgId"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Depot" (
	"id"	INTEGER,
	"cityId"	INTEGER NOT NULL,
	"address"	TEXT NOT NULL,
	"manager"	INTEGER NOT NULL,
	FOREIGN KEY("cityId") REFERENCES "City"("id") ON DELETE CASCADE,
	FOREIGN KEY("manager") REFERENCES "UserDetail"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Parcel" (
	"id"	INTEGER,
	"paymentType"	INTEGER NOT NULL,
	"weight"	NUMERIC,
	"length"	NUMERIC,
	"breadth"	NUMERIC,
	"height"	NUMERIC,
	"productType"	INTEGER NOT NULL,
	"deliverTo"	INTEGER NOT NULL,
	"datetime"	TEXT NOT NULL,
	FOREIGN KEY("productType") REFERENCES "ProductCategory"("id") ON DELETE CASCADE,
	FOREIGN KEY("deliverTo") REFERENCES "UserDetail"("id") ON DELETE CASCADE,
	FOREIGN KEY("paymentType") REFERENCES "PaymentType"("id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "ParcelAction" (
	"id"	INTEGER,
	"action"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Delivery" (
	"id"	INTEGER,
	"agentId"	INTEGER NOT NULL,
	"userId"	INTEGER NOT NULL,
	"parcelId"	INTEGER NOT NULL UNIQUE,
	"datetime"	TEXT NOT NULL,
	FOREIGN KEY("userId") REFERENCES "UserDetail"("id") ON DELETE CASCADE,
	FOREIGN KEY("parcelId") REFERENCES "Parcel"("id") ON DELETE CASCADE,
	FOREIGN KEY("agentId") REFERENCES "UserDetail"("id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "Authentication" (
	"userId"	INTEGER NOT NULL,
	"password"	TEXT NOT NULL,
	"userType"	INTEGER NOT NULL,
	FOREIGN KEY("userId") REFERENCES "UserDetail"("id") ON DELETE CASCADE,
	PRIMARY KEY("userId"),
	FOREIGN KEY("userType") REFERENCES "UserRole"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ParcelActionTaken" (
	"id"	INTEGER,
	"parcelId"	INTEGER NOT NULL UNIQUE,
	"actionId"	INTEGER NOT NULL,
	"datetime"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("actionId") REFERENCES "ParcelAction"("id") ON DELETE CASCADE,
	FOREIGN KEY("parcelId") REFERENCES "Parcel"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "ParcelLocation" (
	"id"	INTEGER,
	"parcelId"	INTEGER NOT NULL,
	"depotId"	INTEGER NOT NULL,
	"shipType"	INTEGER NOT NULL,
	"datetime"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("parcelId") REFERENCES "Parcel"("id") ON DELETE CASCADE,
	FOREIGN KEY("depotId") REFERENCES "Depot"("id") ON DELETE CASCADE,
	FOREIGN KEY("shipType") REFERENCES "ShipmentType"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Pickup" (
	"id"	INTEGER,
	"agentId"	INTEGER NOT NULL,
	"parcelId"	INTEGER NOT NULL UNIQUE,
	"location"	TEXT NOT NULL,
	"datetime"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("parcelId") REFERENCES "Parcel"("id") ON DELETE CASCADE,
	FOREIGN KEY("agentId") REFERENCES "UserDetail"("id") ON DELETE CASCADE
);
INSERT OR IGNORE INTO "PaymentType" ("id","payType") VALUES (1,'COD'),
 (2,'Paid');
INSERT OR IGNORE INTO "ProductCategory" ("id","productType") VALUES (1,'Books'),
 (2,'Electronics'),
 (3,'Furniture'),
 (4,'Garments'),
 (5,'Grocery'),
 (6,'Laptop'),
 (7,'Mobile'),
 (8,'Sprots'),
 (9,'Toy');
INSERT OR IGNORE INTO "UserRole" ("id","role") VALUES (1,'Admin'),
 (2,'Agent'),
 (3,'Customer'),
 (4,'Manager');
INSERT OR IGNORE INTO "ShipmentType" ("id","type") VALUES (1,'Dispatched'),
 (2,'Received');
INSERT OR IGNORE INTO "Designation" ("id","desgType") VALUES (1,'Mr.'),
 (2,'Mrs.'),
 (3,'Ms.'),
 (4,'Sister');
INSERT OR IGNORE INTO "UserDetail" ("id","name","phno","address","desgId") VALUES (100001,'Default Admin',9999999999,'Admin Address',1),
 (100002,'Default Manager',9999999998,'Manager Address',2),
 (100003,'Default Agent',9999999997,'Agent Address',3),
 (100004,'Default Customer',9999999996,'Customer Address',4);
INSERT OR IGNORE INTO "ParcelAction" ("id","action") VALUES (1,'Picked up'),
 (2,'In transit'),
 (3,'Delivered'),
 (4,'Returned');
INSERT OR IGNORE INTO "Authentication" ("userId","password","userType") VALUES (100001,'Default@123',1),
 (100002,'Default@123',4),
 (100003,'Default@123',2),
 (100004,'Default@123',3);
INSERT OR IGNORE INTO "sqlite_sequence" VALUES("Parcel", 10000000),
("Depot", 100),
("City", 100);
COMMIT;
