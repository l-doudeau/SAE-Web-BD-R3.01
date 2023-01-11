DROP DATABASE IF EXISTS GRAND_GALOP;
CREATE DATABASE IF NOT EXISTS GRAND_GALOP DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE GRAND_GALOP;

-- supression des tables avant des les créées
drop table if exists reserver;
drop table if exists poney;
drop table if exists cours;
drop table if exists client;
drop table if exists moniteur;
drop table if exists personne;
drop table if exists ancien_reserver;
drop table if exists ancien_poney;
drop table if exists ancien_cours;
drop table if exists ancien_client;
drop table if exists ancien_moniteur;
drop table if exists ancien_personne;

-- création des tables


CREATE TABLE personne (
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


CREATE TABLE admin (
  id int,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE moniteur (
  id int,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE client (
  id int,
  cotisationA boolean,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;  


CREATE TABLE cours (
  idc int,
  jmahms datetime,
  nomc VARCHAR(42),
  descc VARCHAR(300),
  typec VARCHAR(20),
  duree time,
  prix decimal(4.2),
  id int,
  url_image VARCHAR(500),
  PRIMARY KEY (idc)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE poney (
  idpo int,
  nomp VARCHAR(42),
  poidssup decimal(3.3),
  url_image VARCHAR(500),
  PRIMARY KEY (idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE reserver (
  id int,
  idc int,
  idpo int,
  a_paye boolean,
  PRIMARY KEY (idc, id, idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE ancien_personne (
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


CREATE TABLE ancien_moniteur (
  id int,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE ancien_client (
  id int,
  cotisationA boolean,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;  


CREATE TABLE ancien_cours (
  idc int,
  jmahms datetime,
  nomc VARCHAR(42),
  descc VARCHAR(300),
  typec VARCHAR(42),
  prix decimal(4.2),
  duree time,
  id int,
  PRIMARY KEY (idc)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE ancien_poney (
  idpo int,
  nomp VARCHAR(42),
  poidssup decimal(3.3),
  PRIMARY KEY (idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE ancien_reserver (
  id int,
  idc int,
  idpo int,
  a_paye boolean,
  PRIMARY KEY (idc, id, idpo)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- les contraintes

ALTER TABLE moniteur ADD FOREIGN KEY (id) REFERENCES personne (id);
ALTER TABLE client ADD FOREIGN KEY (id) REFERENCES personne (id);
ALTER TABLE cours ADD FOREIGN KEY (id) REFERENCES moniteur (id);

ALTER TABLE reserver ADD FOREIGN KEY (idpo) REFERENCES poney (idpo);
ALTER TABLE reserver ADD FOREIGN KEY (idc) REFERENCES cours (idc);


-- suppressions des triggers 

drop trigger if exists verifPoids;
drop trigger if exists ajoutPersonneCollectif;
drop trigger if exists ajoutPersonneHoraire;
drop trigger if exists verifHeureRepos;
drop trigger if exists verifHeureReservation;
drop trigger if exists verifHeuresMaxcours;
drop trigger if exists verifPayement;
drop trigger if exists verifPersonneReserveDansClient;
drop trigger if exists verifPoidsUpdate;
drop trigger if exists verifHeureReservationUpdate;
drop trigger if exists verifHeuresMaxcoursUpdate;
drop trigger if exists ajoutPersonneCollectifUpdate;
drop trigger if exists ajoutPersonneHoraireUpdate;
drop trigger if exists verifPayementUpdate;
drop trigger if exists verifPersonneReserveDansClientUpdate;
drop trigger if exists ajouteTableAncienPersonne;
drop trigger if exists ajouteTableAncienClient;
drop trigger if exists ajouteTableAncienMoniteur;
drop trigger if exists ajouteTableAnciencours;
drop trigger if exists ajouteTableAncienPoney;
drop trigger if exists ajouteTableAncienReserver;


-- les triggers 

delimiter | 

-- trigger permettant de verifier que le client ait reserver un poney pouvant soutenir son poids (insert)

create trigger verifPoids before insert on reserver for each row
    begin 
        declare poidsup decimal(3.3);
        declare poidsPersonne decimal(3.3);
        declare msg VARCHAR(300);
        select poids into poidsPersonne from personne where id = new.id;
        select poidssup into poidsup from poney where idpo = new.idpo;
        if poidsup < poidsPersonne then
            set msg = concat(" Réservation impossible car le poids supporté par le poney d'id : ", new.idpo," est inférieur au poids de la personne d'id : ", new.id);
            signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
    end |


-- trigger permettant de verifier que le client ait reserver un poney pouvant soutenir son poids (update)

create trigger verifPoidsUpdate before update on reserver for each row
    begin 
        declare poidsup decimal(3.3);
        declare poidsPersonne decimal(3.3);
        declare msg VARCHAR(300);
        select poids into poidsPersonne from personne where id = new.id;
        select poidssup into poidsup from poney where idpo = new.idpo;
        if poidsup < poidsPersonne then
            set msg = concat(" Réservation impossible car le poids supporté par le poney d'id : ", new.idpo," est inférieur au poids de la personne d'id : ", new.id);
            signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
    end |


-- verifie que les horaires de la reservation du cours sont conformes au horaires du club (insert)

create trigger verifHeurecoursInsert before insert on cours for each ROW
begin
  declare msg VARCHAR(300);
      if TIME(new.jmahms)< TIME("08:00:00") or TIME(new.jmahms) > TIME("20:00:00") then
        set msg = concat("cours impossible car les cours n'ont lieux qu'entre 8 heures et 20 heures. ", "ID Personne : ", new.id,  ", ID cours : ", new.idc);
        signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
end |


-- verifie que les horaires de la reservation du cours sont conformes au horaires du club (update)

create trigger verifHeurecoursUpdate before update on cours for each ROW
begin
  declare msg VARCHAR(300);
      if TIME(new.jmahms)< TIME("08:00:00") or TIME(new.jmahms) > TIME("20:00:00") then
        set msg = concat("cours impossible car les cours n'ont lieux qu'entre 8 heures et 20 heures. ", "ID Personne : ", new.id,  ", ID cours : ", new.idc);
        signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
end |


-- trigger qui permet de verifier la duree du cours, qu'elle ne soit comprise entre 30min et 2h (insert)

create trigger verifHeuresMaxcours before insert on cours for each row
BEGIN
  declare msg VARCHAR(300);
      IF new.duree < TIME("00:30:00") or new.duree > TIME("02:00:00") then
        set msg = concat("cours impossible car un cours dure entre 30min et 2 heures.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
end |


-- trigger qui permet de verifier la duree du cours, qu'elle ne soit comprise entre 30min et 2h (update)

create trigger verifHeuresMaxcoursUpdate before update on cours for each row
BEGIN
  declare msg VARCHAR(300);
      IF new.duree < TIME("00:30:00") or new.duree > TIME("02:00:00") then
        set msg = concat("Réservation impossible car un cours dure entre 30min et 2 heures.");
        signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
end |


-- trigger permettant que si le cours est un cours collectif, le nombre de personne max est de 10 (insert)

create trigger ajoutPersonneCollectif before insert on reserver for each row
begin
  declare nbmax int default 10;
  declare nbPersonnes int;
  declare typecours VARCHAR(42);
  declare mes VARCHAR(100);
  select IFNULL(count(id),0) into nbPersonnes from reserver where idc = new.idc;
  select typec into typecours from cours where idc = new.idc;
  if typecours = "Collectif" then
    if nbPersonnes + 1 > nbmax then
      set mes = concat ("Inscription impossible à l'activité avec l'id : ", new.idc, " car elle est complète");
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
  if typecours = "Individuel" then
    if nbPersonnes <> 0 then
    set mes = concat ("Inscription impossible à l'activité avec l'id : ", new.idc, " car elle est complète");
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
end |


-- permet de vérifier que le client n'a pas déja un cours au horaire de sa nouvelle réservation (insert)

CREATE TRIGGER ajoutPersonneHoraire BEFORE INSERT ON reserver FOR EACH ROW
BEGIN
    DECLARE done INT DEFAULT FALSE;
    declare msg VARCHAR(300);
    declare debutAncien time;
    declare dureeAncien time;
    declare debutNew time;
    declare dureeNew time;
    
    DECLARE lesReservations CURSOR FOR select time(cours.jmahms) as debutAncien, TIME(cours.duree) as dureeAncien
    from reserver inner join cours on reserver.idc = cours.idc
    where reserver.id = new.id and cours.jmahms = (select jmahms from cours where idc = new.idc);
    
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
	set debutNew = (select TIME(jmahms) from cours where idc = new.idc);
    set dureeNew = (select TIME(jmahms) from cours where idc = new.idc);
    OPEN lesReservations;
        boucle_reservations: LOOP
            FETCH lesReservations INTO debutAncien, dureeAncien;
            IF done THEN
              LEAVE boucle_reservations;
            END IF;
            IF (debutAncien >= debutNew and ADDTIME(debutNew, dureeNew) > debutAncien or debutAncien < debutNew and debutNew < ADDTIME(debutAncien, dureeAncien)) then 
              set msg = concat ("Inscription impossible à l'activité car le même client à déja un cours à cette heure");
              signal SQLSTATE '45000' set MESSAGE_TEXT = msg; 
            END IF;
        END LOOP;
    CLOSE lesReservations;
END |


-- CREATE TRIGGER ajoutMoniteurHoraire BEFORE INSERT ON reserver FOR EACH ROW
-- BEGIN
--     DECLARE done INT DEFAULT FALSE;
--     declare msg VARCHAR(300);
--     declare debutAncien time;
--     declare dureeAncien time;
--     declare debutNew time;
--     declare dureeNew time;
--     DECLARE lesReservations CURSOR FOR select TIME(jmahms) as debutAncien, TIME(duree) as dureeAncien, TIME(new.jmahms) as debutNew, TIME(new.duree) as dureeNew 
--     from reserver inner join cours
--     where cours.idc = reserver.idc and year(jmahms) = year(new.jmahms) and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);
--     DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

--     OPEN lesReservations;
--         boucle_reservations: LOOP
--             FETCH lesReservations INTO debutAncien, dureeAncien, debutNew, dureeNew;
--             IF done THEN
--               LEAVE boucle_reservations;
--             END IF;
--             IF (debutAncien >= debutNew and ADDTIME(debutNew, dureeNew) > debutAncien or debutAncien < debutNew and debutNew < ADDTIME(debutAncien, dureeAncien)) then 
--               set msg = concat ("Inscription impossible à l'activité car le moniteur encadre un autre cours à cette heure");
--               signal SQLSTATE '45000' set MESSAGE_TEXT = msg; 
--             END IF;
--         END LOOP;
--     CLOSE lesReservations;
-- END |



-- trigger qui vérifie lors d'une reservation que le repos du poney est respecté (insert)

create trigger verifHeureRepos before insert on reserver for each row
begin
  declare msg VARCHAR(300);
  declare debutAncien time;
  declare dureeAncien time ;
  declare debutNew time;
  declare dureeNew time;
  declare fini int DEFAULT FALSE;
  declare heureRepos cursor for 
  select TIME(duree) as dureeAncien, TIME(jmahms) as debutAncien
  from reserver inner join cours on reserver.idc = cours.idc
  where idpo = new.idpo and DATE(cours.jmahms) = (select DATE(jmahms) from cours where idc = new.idc);

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;
 
  set debutNew = (select TIME(jmahms) from cours where idc = new.idc);
  set dureeNew = (select TIME(duree) from cours where idc = new.idc);
  
  open heureRepos;
    boucle_heure : LOOP
      FETCH heureRepos into dureeAncien, debutAncien;
      IF fini THEN
        LEAVE boucle_heure;
      END IF;
      if debutAncien <= debutNew and debutNew < TIME(debutAncien+dureeAncien)  
        or debutAncien >= debutNew and debutAncien < TIME(debutNew+dureeNew) then
        set msg = concat ("Inscription impossible à l'activité car le cheval est déja en cours" ," - Heure du cours existant : ", debutAncien);
        signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
      if TIMEDIFF(debutNew, debutAncien) < TIME("03:00:00") and debutNew >= debutAncien then
        if dureeAncien = TIME("02:00:00") then
          set msg = concat ("Inscription impossible à l'activité car le cheval n'aura pas eu le temps de se reposer");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
      end if;
      if TIMEDIFF(debutAncien, debutNew) < TIME("03:00:00") and debutNew <= debutAncien then
        if dureeNew = TIME("02:00:00") then
          set msg = concat ("Inscription impossible à l'activité car le cheval n'aura pas eu le temps de se reposer");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
      end if;
    END LOOP;
  CLOSE heureRepos;
end |



-- create trigger verifUniquePoneyParcours before insert on reserver for each row
--   begin 
--     declare msg VARCHAR(300);

--     if exists(select )


-- trigger permettant de vérifier que lors d'une réservation, le client a bien payé sa cotisation annuel et son cours (insert) 

create trigger verifPayement before insert on reserver for each row
begin
  declare msg VARCHAR(300);
  declare cotistationAnnuelle boolean;
  set cotistationAnnuelle = (select cotisationA as cotistationAnnuelle
  from client
  where id = new.id);
	if cotistationAnnuelle = false then
	  set msg = concat ("Impossible de réserver l'activité : ", new.idc, ", car la cotisation annuel n'est pas réglé");
	  signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
  end if;
end |


-- trigger permettant de vérifier que lors de la modification d'une réservation, le client a bien payé sa cotisation annuel et son cours (update)

create trigger verifPayementUpdate before update on reserver for each row
begin
  declare msg VARCHAR(300);
  declare cotistationAnnuelle boolean;
  declare payementcours boolean ;
  declare fini int DEFAULT FALSE;
  declare lesReservations cursor for 
  select cotisationA as cotistationAnnuelle, new.a_paye as payementcours
  from client
  where id = new.id;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;

  open lesReservations;
    boucle_heure : LOOP
      FETCH lesReservations into cotistationAnnuelle, payementcours;
      IF fini THEN
        LEAVE boucle_heure;
      END IF;
        if cotistationAnnuelle = false and payementcours = true then
          set msg = concat ("Impossible de réserver l'activité : ", new.idc, ", car la cotisation annuel n'est pas réglé");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
    END LOOP;
  CLOSE lesReservations;
end |


-- trigger verifiant que la personne qui souhaite réserver un cours, soit bien inscrite en tant que cliente (insert)

create trigger verifPersonneReserveDansClient before insert on reserver for each row
  begin 
    declare msg VARCHAR(300);
    declare dansClient int;
    declare pasDansClient int default 0;
    select ifnull(count(new.id), 0) as dansClient into dansClient from client where new.id = id;

    if pasDansClient = dansClient then
      set msg = concat ("Inscription impossible à l'activité car la personne : ", new.id, " n'est pas inscrite en tant que cliente");
      signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
    end if; 
  end |


-- trigger verifiant que la personne qui souhaite réserver un cours, soit bien inscrite en tant que cliente (update)

create trigger verifPersonneReserveDansClientUpdate before update on reserver for each row
  begin 
    declare msg VARCHAR(300);
    declare dansClient int;
    declare pasDansClient int default 0;
    select ifnull(count(new.id), 0) as dansClient into dansClient from client where new.id = id;

    if pasDansClient = dansClient then
      set msg = concat ("Inscription impossible à l'activité car la personne : ", new.id, " n'est pas inscrite en tant que cliente");
      signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
    end if; 
  end |

-- trigger qui vérifie lors d'une réservation que la date du cours n'est pas dépasée (insert)

create trigger verifcoursPasCommence before insert on cours for each row
  begin
    declare msg VARCHAR(300);
    if new.jmahms < now() then
      set msg = concat ("Inscription impossible de la réservation car la date est dépasée", new.jmahms);
      signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
    end if;
  end |


-- trigger qui vérifie lors d'une réservation que la date du cours n'est pas dépasée (update)

create trigger verifcoursPasCommenceUpdate before update on cours for each row
  begin
    declare msg VARCHAR(300);
    if new.jmahms < now() then
      set msg = concat ("Inscription impossible de la réservation car la date est dépasée", new.jmahms);
      signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
    end if;
  end |

-- trigger qui ajoute dans les table de conservation (ancienne table), lorsqu'il y a une suppression de donnée


create trigger ajouteTableAncienPersonne before delete on personne for each row
  begin
    INSERT INTO ancien_personne(id, nomp, prenomp, ddn, poids, adressemail, adresse, code_postal, ville, numerotel, mdp)
    VALUES (old.id, old.nomp, old.prenomp, old.ddn, old.poids, old.adressemail, old.adresse, old.code_postal, old.ville, old.numerotel, old.mdp);
  END |


create trigger ajouteTableAncienClient before delete on client for each row
  begin
      INSERT INTO ancien_client(id, cotisationA) VALUES(old.id, old.cotisationA);
  END |


create trigger ajouteTableAncienMoniteur before delete on moniteur for each row
  begin
      INSERT INTO ancien_moniteur(id) VALUES(old.id);
  END |


create trigger ajouteTableAnciencours before delete on cours for each row
  begin
      INSERT INTO ancien_cours(idc,jmahms,duree, nomc, descc, typec, prix) VALUES(old.idc,old.jmahms,old.duree, old.nomc, old.descc, old.typec , old.prix);
  END |


create trigger ajouteTableAncienPoney before delete on poney for each row
  begin
      INSERT INTO ancien_poney(idpo, nomp, poidssup) VALUES(old.idpo, old.nomp, old.poidssup);
  END |


create trigger ajouteTableAncienReserver before delete on reserver for each row
  begin
      INSERT INTO ancien_reserver(id, idc, idpo, a_paye) VALUES(old.id, old.idc, old.idpo, old.a_paye);
  END |

delimiter ;
