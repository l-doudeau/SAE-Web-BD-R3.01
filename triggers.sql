drop trigger if exists verifPoids;
drop trigger if exists ajoutPersonneCollectif;
drop trigger if exists ajoutPersonneHoraire;
drop trigger if exists verifHeureRepos;
drop trigger if exists verifHeureReservation;
drop trigger if exists verifHeuresMaxCours;

delimiter | 

create trigger verifPoids before insert on RESERVER for each row
    begin 
        declare poidsup decimal(3.3);
        declare poidsPersonne decimal(3.3);
        declare msg VARCHAR(300);
        select poids into poidsPersonne from PERSONNE where idp = new.idp;
        select poidssup into poidsup from PONEYS where idpo = new.idpo;
        if poidsup < poidsPersonne then
            set msg = concat(" Réservation impossible car le poids supporté par le poney d'id : ", new.idpo," est inférieur au poids de la personne d'id : ", new.idp);
            signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
    end |


create trigger verifHeureReservation before insert on RESERVER for each ROW
begin
  declare heureNew int;
  declare msg VARCHAR(300);
  declare fini INT default false;
  declare lesReservations cursor for
  select TIME(new.jmahms) as heureNew from RESERVER;
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;

  OPEN lesReservations;
    boucle_reservations: LOOP
    FETCH lesReservations INTO heureNew;
      IF fini THEN
        LEAVE boucle_reservations;
      END IF;
      if heureNew < TIME("08:00:00") or heureNew > TIME("20:00:00") then
        set msg = concat(" Réservation impossible car elles ne sont possibles qu'entre 8 heures et 20 heures.", new.idp, new.idpo);
        signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
    end LOOP;
  close lesReservations;
end |


-- trigger qui permet de verifier la duree du cours, qu'elle ne soit pas trop petite ou trop grande

create trigger verifHeuresMaxCours before insert on RESERVER for each row
BEGIN
  declare msg VARCHAR(300);
  declare fini int DEFAULT false;
  declare dureeNew int;
  declare lesReservations cursor for
  select TIME(new.duree) as dureeNew from RESERVER;

  DECLARE CONTINUE handler for not found set fini = TRUE;

  open lesReservations;
    boucle_reservations : LOOP
    FETCH lesReservations INTO dureeNew;
      IF fini THEN
        LEAVE boucle_reservations;
      END IF;

      IF dureeNew < TIME("00:30:00") or dureeNew > TIME("02:00:00") then
        set msg = concat("Réservation impossible car un cours dure entre 30min et 2 heures.", new.idp, new.idpo);
        signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
    end LOOP;
  close lesReservations;
end |


-- trigger permettant que si le cours est un cours collectif, le nombre de personne max est de 10

create trigger ajoutPersonneCollectif before insert on RESERVER for each row
begin
  declare nbmax int;
  declare nbPersonnes int;
  declare typeCours VARCHAR(42);
  declare mes VARCHAR(100);
  set nbmax = 10;
  select IFNULL(count(idp),0) into nbPersonnes from RESERVER where idc = new.idc and jmahms = new.jmahms;
  select typec into typeCours from COURS where idc = new.idc;
  if typeCours = "Collectif" then
    if nbPersonnes + 1 > nbmax then
      set mes = concat ("Inscription impossible à l'activité avec l'id : ", new.idc, " car elle est complète");
      signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
  if typeCours = "Individuel" then
    if nbPersonnes <> 0 then
    set mes = concat ("Inscription impossible à l'activité avec l'id : ", new.idc, " car elle est complète");
    signal SQLSTATE '45000' set MESSAGE_TEXT = mes;
    end if;
  end if;
end |


-- permet de vérifier que le client n'a pas déja un cours au horaire de sa nouvelle réservation

CREATE TRIGGER ajoutPersonneHoraire BEFORE INSERT ON RESERVER
FOR EACH ROW
BEGIN
    DECLARE done INT DEFAULT FALSE;
    declare msg VARCHAR(300);
    declare debutAncien time;
    declare dureeAncien time;
    declare debutNew time;
    declare dureeNew time;
    DECLARE lesReservations CURSOR FOR select TIME(jmahms) as debutAncien, TIME(duree) as dureeAncien, TIME(new.jmahms) as debutNew, TIME(new.duree) as dureeNew from RESERVER where idp = new.idp and year(jmahms) = year(new.jmahms) and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN lesReservations;
        boucle_reservations: LOOP
            FETCH lesReservations INTO debutAncien, dureeAncien, debutNew, dureeNew;
            IF done THEN
              LEAVE boucle_reservations;
            END IF;
            IF (debutAncien > debutNew and ADDTIME(debutNew, dureeNew) > debutAncien or debutAncien < debutNew and debutNew < ADDTIME(debutAncien, dureeAncien)) then 
              set msg = concat ("Inscription impossible à l'activité car le même client à déja un cours à cette heure");
              signal SQLSTATE '45000' set MESSAGE_TEXT = msg; 
            END IF;
        END LOOP;
    CLOSE lesReservations;
END |


-- trigger sur le repos des chevaux

create trigger verifHeureRepos before insert on RESERVER for each row
begin
  declare msg VARCHAR(300);
  declare debutAncien time;
  declare dureeAncien time ;
  declare debutNew time;
  declare dureeNew time;
  declare fini int DEFAULT FALSE;
  declare heureRepos cursor for 
  select TIME(duree) as dureeAncien, TIME(new.jmahms) as debutNew, TIME(jmahms) as debutAncien, TIME(new.duree) as dureeNew
  from RESERVER 
  where idpo = new.idpo and year(jmahms) = year(new.jmahms) 
  and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;

  open heureRepos;
    boucle_heure : LOOP
      FETCH heureRepos into dureeAncien, debutNew, debutAncien, dureeNew;
      IF fini THEN
        LEAVE boucle_heure;
      END IF;
      if TIMEDIFF(debutNew, debutAncien) = TIME("02:00:00") then
        if dureeAncien = TIME("02:00:00") then
          set msg = concat ("Inscription impossible à l'activité car le cheval n'a pas eu le temps de se reposer");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
      end if;
      if TIMEDIFF(debutAncien, debutNew) = TIME("02:00:00") then
        if dureeNew = TIME("02:00:00") then
          set msg = concat ("Inscription impossible à l'activité car le cheval n'a pas eu le temps de se reposer");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
      end if;
    END LOOP;
  CLOSE heureRepos;
end |

delimiter |

create or replace trigger verifPayement before insert on RESERVER for each row
 begin 
  declare msg VARCHAR(90);
  declare verifPayementAnnuel boolean;
  declare verifPayementCours boolean;
  declare fini boolean DEFAULT false;

  DECLARE lesReservations CURSOR FOR 
  select cotisationA, a_paye
  from CLIENT natural join RESERVER;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = true;

  open lesReservations;
    boucle_heure : LOOP
      FETCH lesReservations into verifPayementAnnuel, verifPayementCours;
      IF fini THEN
        LEAVE boucle_heure;
      END IF;

      

      if (verifPayementAnnuel = false) and (verifPayementCours = true) then 
          set msg = concat ("Inscription impossible à l'activité : ", new.idp, ", car la cotisation anuelle n'est pas payé");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
      if (verifPayementAnnuel = true) and (verifPayementCours = false) then 
          set msg = concat ("Inscription impossible à l'activité : " , new.idp, ", car le payement du cours n'est pas effectués");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
      if (verifPayementAnnuel = false) or (verifPayementCours = false) then 
          set msg = concat ("Inscription impossible à l'activité : ", new.idp, ", car la cotisation anuelle n'est pas payé et le payement du cours n'est pas effectués");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;
    end LOOP;
  close lesReservations;
end |

delimiter ;


delimiter |

create trigger verifPayementFonctionnel before insert on RESERVER for each row
begin
  declare msg VARCHAR(300);
  declare cotistationAnnuelle boolean;
  declare payementCours boolean ;
  declare fini int DEFAULT FALSE;
  declare lesReservations cursor for 
  select cotisationA as cotistationAnnuelle, a_paye as payementCours
  from RESERVER natural join CLIENT
  where idp = new.idp;

  DECLARE CONTINUE HANDLER FOR NOT FOUND SET fini = TRUE;

  open lesReservations;
    boucle_heure : LOOP
      FETCH lesReservations into cotistationAnnuelle, payementCours;
      IF fini THEN
        LEAVE boucle_heure;
      END IF;
        if cotistationAnnuelle = false or payementCours = false then
          set msg = concat (" idp", new.idp, " cotA ",cotistationAnnuelle, " PayCours",payementCours);
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
        end if;
    END LOOP;
  CLOSE lesReservations;
end |

delimiter ;

--Inscription impossible à l'activité car la cotisation annuelle ou le payement du cours n'a pas encore était effectué
  --select a_paye into verifPayementCours from CLIENT natural join RESERVER where new.idp = idp;