drop trigger if exists verifPoids;
drop trigger if exists ajoutPersonneCollectif;
drop trigger if exists ajoutPersonneHoraire;
drop trigger if exists verifHeureRepos;

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

-- version mauvaise

-- delimiter |

-- create trigger ajoutPersonneHoraire before insert on RESERVER for each row
-- begin 
--   declare msg VARCHAR(300);
--   declare debutAncien time;
--   declare dureeAncien time;
--   declare debutNew time;
--   declare dureeNew time;
--   declare fini boolean default false;
--   declare lesReservations cursor for
--     select TIME(jmahms), TIME(duree) 
--     from RESERVER 
--     where idp = new.idp and year(jmahms) = year(new.jmahms) 
--     and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);
--   declare continue handler for not found set fini = true;
--     select TIME(new.jmahms)into debutNew
--     from RESERVER 
--     where idp = new.idp and year(jmahms) = year(new.jmahms) and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);
--     select TIME(new.duree) into dureeNew
--     from RESERVER 
--     where idp = new.idp and year(jmahms) = year(new.jmahms) and month(jmahms) = month(new.jmahms) and day(jmahms) = day(new.jmahms);
--   open lesReservations;
--   while not fini do
--     fetch lesReservations into debutAncien, dureeAncien;
--     if not fini then
--       if (debutAncien > debutNew and ADDTIME(debutNew, dureeNew) > debutAncien or debutAncien < debutNew and debutNew < ADDTIME(debutAncien, dureeAncien)) then 
--         set msg = concat ("Inscription impossible à l'activité car le même client à déja un cours à cette heure");
--         signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
--       end if;
--     end if;
--   end while;
--   close lesReservations;
-- end |

-- delimiter ;


-- bonne version

DROP TRIGGER IF EXISTS ajoutPersonneHoraire2;
CREATE TRIGGER ajoutPersonneHoraire2 BEFORE INSERT ON RESERVER
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

delimiter |
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
delimiter;