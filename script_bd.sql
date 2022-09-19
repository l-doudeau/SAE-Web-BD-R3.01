/*CREATE DATABASE IF NOT EXISTS GRAND_GALOP DEFAULT CHARACTER SET UTF8MB4 COLLATE utf8_general_ci;
USE GRAND_GALOP;
*/


-- supression des tables avant des les créées

drop table if exists RESERVER;
drop table if exists PONEYS;
drop table if exists COURS;
drop table if exists CLIENT;
drop table if exists MONITEUR;
drop table if exists PERSONNE;

-- création des tables

CREATE TABLE CLIENT (
  idp int,
  cotisationA boolean,
  PRIMARY KEY (idp)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE COURS (
  idc int,
  nomc VARCHAR(42),
  descc VARCHAR(42),
  typec VARCHAR(42),
  prix decimal(4,2),
  PRIMARY KEY (idc)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;



CREATE TABLE MONITEUR (
  idp int,
  PRIMARY KEY (idp)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE PERSONNE (
  idp int,
  nomp VARCHAR(42),
  prenomp VARCHAR(42),
  ddn date,
  poids decimal(3.3),
  adressemail VARCHAR(42),
  adresse VARCHAR(42),
  code_postal int,
  ville VARCHAR(20),
  numerotel int,
  mdp VARCHAR(42),
  PRIMARY KEY (idp)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE PONEYS (
  idpo int,
  nomp VARCHAR(42),
  poidssup decimal(3.3),
  PRIMARY KEY (idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE RESERVER (

  jmahms datetime,
  idp int,
  idc int,
  idpo int,
  duree time,
  a_paye boolean,
  PRIMARY KEY (jmahms, idp, idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- les contraintes

ALTER TABLE MONITEUR ADD FOREIGN KEY (idp) REFERENCES PERSONNE (idp);
ALTER TABLE CLIENT ADD FOREIGN KEY (idp) REFERENCES PERSONNE (idp);

ALTER TABLE RESERVER ADD FOREIGN KEY (idpo) REFERENCES PONEYS (idpo);
ALTER TABLE RESERVER ADD FOREIGN KEY (idc) REFERENCES COURS (idc);