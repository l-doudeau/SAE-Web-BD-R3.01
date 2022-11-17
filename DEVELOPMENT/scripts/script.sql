-- DROP DATABASE IF EXISTS GRAND_GALOP;
CREATE DATABASE IF NOT EXISTS GRAND_GALOP DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE GRAND_GALOP;

-- supression des tables avant des les créées

drop table if exists RESERVER;
drop table if exists PONEYS;
drop table if exists COURS;
drop table if exists CLIENT;
drop table if exists MONITEUR;
drop table if exists PERSONNE;
drop table if exists ANCIEN_RESERVER;
drop table if exists ANCIEN_PONEYS;
drop table if exists ANCIEN_COURS;
drop table if exists ANCIEN_CLIENT;
drop table if exists ANCIEN_MONITEUR;
drop table if exists ANCIEN_PERSONNE;

-- création des tables


CREATE TABLE PERSONNE (
  id int,
  nomp VARCHAR(42),
  prenomp VARCHAR(42),
  ddn date,
  poids decimal(3.3),
  adressemail VARCHAR(42),
  adresse VARCHAR(42),
  code_postal int,
  ville VARCHAR(20),
  numerotel VARCHAR(20),
  mdp VARCHAR(42),
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE MONITEUR (
  id int,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE CLIENT (
  id int,
  cotisationA boolean,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;  


CREATE TABLE COURS (
  idc int,
  nomc VARCHAR(42),
  descc VARCHAR(300),
  typec VARCHAR(42),
  prix decimal(4.2),
  PRIMARY KEY (idc)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE PONEYS (
  idpo int,
  nomp VARCHAR(42),
  poidssup decimal(3.3),
  PRIMARY KEY (idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE RESERVER (
  jmahms datetime,
  id int,
  idc int,
  idpo int,
  duree time,
  a_paye boolean,
  PRIMARY KEY (jmahms, id, idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE ANCIEN_PERSONNE (
  id int,
  nomp VARCHAR(42),
  prenomp VARCHAR(42),
  ddn date,
  poids decimal(3.3),
  adressemail VARCHAR(42),
  adresse VARCHAR(42),
  code_postal int,
  ville VARCHAR(20),
  numerotel VARCHAR(20),
  mdp VARCHAR(42),
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE ANCIEN_MONITEUR (
  id int,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE ANCIEN_CLIENT (
  id int,
  cotisationA boolean,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;  


CREATE TABLE ANCIEN_COURS (
  idc int,
  nomc VARCHAR(42),
  descc VARCHAR(300),
  typec VARCHAR(42),
  prix decimal(4.2),
  PRIMARY KEY (idc)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE ANCIEN_PONEYS (
  idpo int,
  nomp VARCHAR(42),
  poidssup decimal(3.3),
  PRIMARY KEY (idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE ANCIEN_RESERVER (

  jmahms datetime,
  id int,
  idc int,
  idpo int,
  duree time,
  a_paye boolean,
  PRIMARY KEY (jmahms, id, idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- les contraintes

ALTER TABLE MONITEUR ADD FOREIGN KEY (id) REFERENCES PERSONNE (id);
ALTER TABLE CLIENT ADD FOREIGN KEY (id) REFERENCES PERSONNE (id);

ALTER TABLE RESERVER ADD FOREIGN KEY (idpo) REFERENCES PONEYS (idpo);
ALTER TABLE RESERVER ADD FOREIGN KEY (idc) REFERENCES COURS (idc);
